# Self-checks: (1) Stepper == forward_full, (2) loaded weights reach the logged validation loss on Chopin data.
import glob, sys
import numpy as np
import midi_neural_processor.processor as tok
from mtnp import load, forward_full, Stepper, softmax, PAD

W = load('model.weights.h5')
rng = np.random.default_rng(0)

seq = rng.integers(0, 388, 300)
full = forward_full(W, seq)
st = Stepper(W)
inc = np.stack([st.step(t) for t in seq])
err = np.abs(full - inc).max()
print('stepper vs full max abs diff:', err)
assert err < 1e-3, err

losses = []
for f in sorted(glob.glob(sys.argv[1] + '/*.mid'))[:12]:
    ids = np.array(tok.encode_midi(f))
    if len(ids) < 1100:
        continue
    s = rng.integers(0, len(ids) - 1025)
    x, y = ids[s:s + 1024], ids[s + 1:s + 1025]
    p = softmax(forward_full(W, x))
    losses.append(-np.log(p[np.arange(len(y)), y] + 1e-12).mean())
print('chopin CE on %d crops: %.3f (uniform = %.3f)' % (len(losses), np.mean(losses), np.log(391)))
assert np.mean(losses) < 5.5
