"""NumPy re-implementation of the notebook's MusicTransformerDecoder (inference only).

Mirrors notebook cells 36-42: relative global attention with skewing, post-LN decoder layers,
keras_hub SinePositionEncoding, look-ahead + pad mask. Weights come from model.weights.h5.
"""
import h5py
import numpy as np

VOCAB, D, HEADS, MAXLEN, PAD = 391, 256, 4, 2048, 388
HD = D // HEADS


def load(path):
    f = h5py.File(path, 'r')
    g = lambda k: np.array(f[k], dtype=np.float32)
    layers = []
    for i in range(6):
        p = 'decoder/decode_layers/decoder_layer' + ('' if i == 0 else f'_{i}') + '/'
        a = p + 'relative_global_attention_1/'
        layers.append({k: (g(a + k + '/vars/0'), g(a + k + '/vars/1')) for k in
                       ('query_dense', 'key_dense', 'value_dense', 'output_dense')}
                      | {'rel': g(a + 'vars/0'),
                         'pre': (g(p + 'feed_forward_network_pre/vars/0'), g(p + 'feed_forward_network_pre/vars/1')),
                         'pos': (g(p + 'feed_forward_network_pos/vars/0'), g(p + 'feed_forward_network_pos/vars/1')),
                         'ln1': (g(p + 'layer_normalization_1/vars/0'), g(p + 'layer_normalization_1/vars/1')),
                         'ln2': (g(p + 'layer_normalization_2/vars/0'), g(p + 'layer_normalization_2/vars/1'))})
    return {'emb': g('decoder/embedding/vars/0'), 'fc': (g('fc/vars/0'), g('fc/vars/1')), 'layers': layers}


def dense(x, wb):
    return x @ wb[0] + wb[1]


def ln(x, gb, eps=1e-6):
    m = x.mean(-1, keepdims=True)
    v = ((x - m) ** 2).mean(-1, keepdims=True)
    return (x - m) / np.sqrt(v + eps) * gb[0] + gb[1]


def sine_pe(positions):
    i = np.arange(D)
    timescales = np.power(np.float32(1 / 10000), (2 * (i // 2)).astype(np.float32) / D)
    ang = positions[:, None].astype(np.float32) * timescales[None, :]
    cos_mask = (i % 2).astype(np.float32)
    return np.sin(ang) * (1 - cos_mask) + np.cos(ang) * cos_mask


def embed(W, tokens, start=0):
    x = W['emb'][tokens] * np.sqrt(np.float32(D))
    return x + sine_pe(np.arange(start, start + len(tokens)))


def heads(x):  # (L, D) -> (H, L, HD)
    return x.reshape(len(x), HEADS, HD).transpose(1, 0, 2)


def softmax(z):
    z = z - z.max(-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(-1, keepdims=True)


def forward_full(W, tokens):
    """Logits for every position, exactly as the Keras model computes them (with skewing)."""
    tokens = np.asarray(tokens)
    L = len(tokens)
    mask = np.triu(np.ones((L, L), np.float32), 1)
    mask = np.maximum(mask, (tokens == PAD)[None, :].astype(np.float32))
    x = embed(W, tokens)
    for P in W['layers']:
        q, k, v = (heads(dense(x, P[n])) for n in ('query_dense', 'key_dense', 'value_dense'))
        scores = q @ k.transpose(0, 2, 1)
        rel = np.einsum('hld,md->hlm', q, P['rel'][MAXLEN - L:])
        rel = rel * np.flip(np.tri(L, L, dtype=np.float32), axis=1)
        rel = np.pad(rel, ((0, 0), (0, 0), (1, 0))).reshape(HEADS, L + 1, L)[:, 1:, :]
        logits = (scores + rel) / np.sqrt(np.float32(HD)) + mask * -1e9
        att = softmax(logits) @ v
        att = dense(att.transpose(1, 0, 2).reshape(L, D), P['output_dense'])
        a_norm = ln(att + x, P['ln1'])
        ffn = dense(np.maximum(dense(att, P['pre']), 0), P['pos'])  # notebook feeds the un-normalized attention output
        x = ln(a_norm + ffn, P['ln2'])
    return dense(x, W['fc'])


class Stepper:
    """Incremental decoding with cached keys/values; equals forward_full for the newest position."""

    def __init__(self, W):
        self.W, self.k, self.v, self.n = W, [[] for _ in range(6)], [[] for _ in range(6)], 0

    def step(self, token):
        W, i = self.W, self.n
        x = embed(W, np.array([token]), start=i)
        for li, P in enumerate(W['layers']):
            q = heads(dense(x, P['query_dense']))[:, 0]               # (H, HD)
            self.k[li].append(heads(dense(x, P['key_dense']))[:, 0])
            self.v[li].append(heads(dense(x, P['value_dense']))[:, 0])
            K, V = np.stack(self.k[li], 1), np.stack(self.v[li], 1)   # (H, i+1, HD)
            rel_rows = P['rel'][MAXLEN - 1 - i: MAXLEN]                 # row for key j = MAXLEN-1-(i-j)
            logits = (np.einsum('hd,hjd->hj', q, K) + q @ rel_rows.T) / np.sqrt(np.float32(HD))
            att = np.einsum('hj,hjd->hd', softmax(logits), V).reshape(1, D)
            att = dense(att, P['output_dense'])
            a_norm = ln(att + x, P['ln1'])
            ffn = dense(np.maximum(dense(att, P['pre']), 0), P['pos'])
            x = ln(a_norm + ffn, P['ln2'])
        self.n += 1
        return dense(x, W['fc'])[0]


def generate(W, seed, n_new, top_k=5, rng=None):
    rng = rng or np.random.default_rng(42)
    st, out = Stepper(W), list(seed)
    for t in seed[:-1]:
        st.step(t)
    logits = st.step(seed[-1])
    for _ in range(n_new):
        idx = np.argpartition(logits, -top_k)[-top_k:]
        p = softmax(logits[idx])
        tok = int(idx[rng.choice(top_k, p=p)])
        out.append(tok)
        if len(out) >= MAXLEN:
            break
        logits = st.step(tok)
    return out
