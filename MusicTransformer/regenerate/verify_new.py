# Share of generated notes that also appear (same pitch, same time ±0.05 s, best time shift) in a reference piece.
# Usage: python verify_new.py <generated.mid> <reference.mid or dir of .mid>
import glob, os, sys
import pretty_midi

def notes(path):
    pm = pretty_midi.PrettyMIDI(path)
    return sorted(((n.pitch, n.start) for i in pm.instruments for n in i.notes), key=lambda x: x[1])

def overlap(g, c):
    idx = {(p, round(s * 20)) for p, s in c}
    best = 0
    for sh in {round((s - g[0][1]) * 20) / 20 for p, s in c if p == g[0][0]}:
        best = max(best, sum(any((p, round((s + sh) * 20) + d) in idx for d in (-1, 0, 1)) for p, s in g))
    return best

g = notes(sys.argv[1])
refs = sorted(glob.glob(os.path.join(sys.argv[2], '*.mid'))) if os.path.isdir(sys.argv[2]) else [sys.argv[2]]
res = max((overlap(g, notes(r)), r) for r in refs)
print('generated notes %d | best overlap %d (%.1f%%) with %s' % (len(g), res[0], 100 * res[0] / len(g), os.path.basename(res[1])))
