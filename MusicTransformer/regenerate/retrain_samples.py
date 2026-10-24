# Copy retrain outputs into the repo and cut the original's next part to the same length, with stats for the README.
import copy, glob, shutil, numpy as np, pretty_midi
R, OUT = 'work/retrain_in/', 'work/co/'
LEVELS = np.array([39, 63, 87, 111])
def notes(pm): return sorted(((n.pitch, n.start) for i in pm.instruments for n in i.notes), key=lambda x: x[1])
def pc(ns):
    h = np.bincount([p % 12 for p, _ in ns], minlength=12).astype(float); return h / np.linalg.norm(h)

prompt = pretty_midi.PrettyMIDI(R + 'prompt.mid')
pend = max(n.end for i in prompt.instruments for n in i.notes)
src = pretty_midi.PrettyMIDI('work/carols41/c33.mid')  # c33 = Christmas Without You (100% match with prompt)
gens = {k: pretty_midi.PrettyMIDI(R + k + '_generated.mid') for k in ('stage1_maestro', 'stage2_chopin', 'stage3_carol')}
glen = max(max(n.end for i in g.instruments for n in i.notes) for g in gens.values())

nxt = pretty_midi.PrettyMIDI(); ins = pretty_midi.Instrument(0)
for i in src.instruments:
    for n in i.notes:
        if pend <= n.start < pend + glen:
            v = int(LEVELS[np.abs(LEVELS - n.velocity).argmin()])
            ins.notes.append(pretty_midi.Note(v, n.pitch, n.start - pend, min(n.end, pend + glen) - pend))
nxt.instruments.append(ins)
ref = pc(notes(nxt))

nxt.write(OUT + 'carol_original_next.mid')
shutil.copy(R + 'prompt.mid', OUT + 'carol_prompt.mid')
for k, g in gens.items():
    shutil.copy(R + k + '_generated.mid', OUT + 'carol_' + k + '.mid')
print('prompt %.1fs, original next window %.1f~%.1fs' % (pend, pend, pend + glen))
for k, pm in [('original_next', nxt)] + list(gens.items()):
    ns = notes(pm); end = max(n.end for i in pm.instruments for n in i.notes)
    print('%-15s notes %3d len %.1fs keysim %.2f range %d~%d nps %.1f' % (k, len(ns), end, pc(ns) @ ref,
          min(p for p, _ in ns), max(p for p, _ in ns), len(ns) / end))
