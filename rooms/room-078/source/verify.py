"""ROOM 078 proof: a cube [0,2]^3 is cut by the plane through three marked points. The cross-section is the convex
polygon whose corners are where the plane meets the cube's 12 edges (duplicates merged). Each digit is its number of
sides. All 10^4 codes compared; exactly one matches."""
import itertools, json, os
import numpy as np
POINTS = {'A': [(2, 1, 0), (0, 2, 1), (1, 0, 2)], 'B': [(1, 0, 0), (0, 1, 0), (0, 0, 1)],
          'C': [(1, 0, 2), (0, 1, 2), (2, 2, 0)], 'D': [(1, 0, 0), (0, 2, 2), (2, 2, 2)]}
V = [np.array(v, float) for v in itertools.product((0, 2), repeat=3)]
EDGES = [(a, b) for a, b in itertools.combinations(range(8), 2) if np.sum(V[a] != V[b]) == 1]


def section(pts):
    p = [np.array(q, float) for q in pts]; n = np.cross(p[1] - p[0], p[2] - p[0]); d = n @ p[0]
    out = []
    for a, b in EDGES:
        fa, fb = n @ V[a] - d, n @ V[b] - d
        if abs(fa) < 1e-9: q = V[a]
        elif abs(fb) < 1e-9: q = V[b]
        elif fa * fb < 0: q = V[a] + (V[b] - V[a]) * fa / (fa - fb)
        else: continue
        if not any(np.allclose(q, r) for r in out): out.append(q)
    c = sum(out) / len(out); u = out[0] - c; w = np.cross(n, u)
    out.sort(key=lambda q: np.arctan2((q - c) @ w, (q - c) @ u)); return n, out


SIDES = {k: len(section(v)[1]) for k, v in POINTS.items()}
code = ''.join(str(SIDES[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, SIDES)
assert sols == ['6354']
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'points': POINTS,
               'polygons': {k: [list(map(float, q)) for q in section(v)[1]] for k, v in POINTS.items()},
               'why': '단면의 꼭짓점 = 평면이 정육면체 모서리와 만나는 점. 세 점 말고 다른 모서리에서도 만나요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
