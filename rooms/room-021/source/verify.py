"""ROOM 021 proof: fold a cube net. Roll a virtual cube across the net (each net square lands on the face touching
the floor) to find which squares end up opposite each other, then test every 4-digit code 0000-9999 against
'digit k = the number on the face opposite the k-th marked square'."""
import json, os
NET = {(0, 0): 3, (0, 1): 8, (1, 1): 5, (1, 2): 1, (1, 3): 6, (2, 3): 4}
MARK = [('A', (0, 1)), ('B', (1, 2)), ('C', (0, 0)), ('D', (2, 3))]
OPP = {'D': 'U', 'U': 'D', 'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}


def roll(s, dr, dc):
    s = dict(s)
    if dc == 1: s['D'], s['E'], s['U'], s['W'] = s['E'], s['U'], s['W'], s['D']
    if dc == -1: s['D'], s['W'], s['U'], s['E'] = s['W'], s['U'], s['E'], s['D']
    if dr == 1: s['D'], s['S'], s['U'], s['N'] = s['S'], s['U'], s['N'], s['D']
    if dr == -1: s['D'], s['N'], s['U'], s['S'] = s['N'], s['U'], s['S'], s['D']
    return s


face = {}
start = (1, 2); stack = [(start, {k: k for k in OPP})]
while stack:
    cell, st = stack.pop()
    if cell in face: continue
    face[cell] = st['D']
    for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        nb = (cell[0] + dr, cell[1] + dc)
        if nb in NET and nb not in face: stack.append((nb, roll(st, dr, dc)))
assert sorted(face.values()) == sorted(OPP), face          # six different faces: it really is a cube net
by_face = {f: c for c, f in face.items()}
opp_cell = {c: by_face[OPP[f]] for c, f in face.items()}
pairs = sorted({tuple(sorted((NET[c], NET[o]))) for c, o in opp_cell.items()})
want = [NET[opp_cell[c]] for _, c in MARK]
ok = [f'{n:04d}' for n in range(10000) if [int(x) for x in f'{n:04d}'] == want]
print(pairs, ok)
assert len(ok) == 1
json.dump({'unique_answer': ok[0], 'codes_tested': 10000, 'opposite_pairs': [list(p) for p in pairs],
           'net': {f'r{r}c{c}': v for (r, c), v in NET.items()}, 'marked': {k: NET[c] for k, c in MARK}},
          open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
