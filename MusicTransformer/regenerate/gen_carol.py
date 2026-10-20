# Fixed carol generation: seed = beginning of the carol, sampling (not argmax), no zero padding.
# Saves prompt / generated-only / full MIDI and fails if the model added no notes.
# Usage: python gen_carol.py <carol.mid> <out_prefix> [seed_tokens] [new_tokens]
import sys
import numpy as np
import pretty_midi
import midi_neural_processor.processor as tok
from mtnp import load, generate, PAD

carol, prefix = sys.argv[1], sys.argv[2]
SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 512
NEW = int(sys.argv[4]) if len(sys.argv) > 4 else 1024
TOP_K = int(sys.argv[5]) if len(sys.argv) > 5 else 391  # 391 = sample from the full distribution; top-5 never picks a note for this model

W = load('model.weights.h5')
ids = tok.encode_midi(carol)
seed = list(ids[:SEED])
out = generate(W, seed, NEW, top_k=TOP_K, rng=np.random.default_rng(42))
cont = [t for t in out[len(seed):] if t < PAD]

def save(tokens, path):
    tok.decode_midi(np.array(tokens), path)
    pm = pretty_midi.PrettyMIDI(path)
    return sum(len(i.notes) for i in pm.instruments), round(pm.get_end_time(), 1)

n_p, t_p = save(seed, prefix + '_prompt.mid')
n_g, t_g = save(cont, prefix + '_generated.mid')
n_f, t_f = save(seed + cont, prefix + '_full.mid')
print('tokens: carol', len(ids), 'seed', len(seed), 'new', len(out) - len(seed), 'kept', len(cont))
print('prompt notes %d (%.1fs) | generated notes %d (%.1fs) | full notes %d (%.1fs)' % (n_p, t_p, n_g, t_g, n_f, t_f))
assert n_g > 0, 'model produced no notes'
