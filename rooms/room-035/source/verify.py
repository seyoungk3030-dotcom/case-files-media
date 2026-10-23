"""ROOM 035 proof: four cube towers 1-4 (3x3 heightmaps, seen from the front-right-top) and four silhouettes A-D, each
labelled with the side it is seen from (front, right, top). Code = the tower number each silhouette belongs to.
1) Each tower's heightmap is the only one that looks exactly like the picture (view.py visibility, all 4^9 maps).
2) Every 4-digit code with digits 1..4 is tested; exactly one matches all four silhouettes.
3) Reading the right-side view as if seen from the left (mirrored) no longer gives that code."""
import itertools, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view

TOWERS = {1: (3, 0, 0, 2, 0, 1, 0, 0, 1), 2: (2, 0, 0, 1, 0, 1, 0, 1, 1),
          3: (3, 0, 1, 1, 0, 1, 0, 1, 0), 4: (1, 2, 0, 2, 0, 1, 0, 0, 1)}   # row by row, row 0 = front, col 0 = left


def hm(t): return [t[j * 3:j * 3 + 3] for j in range(3)]
def front(t): return tuple(max(hm(t)[j][i] for j in range(3)) for i in range(3))   # left -> right
def right(t): return tuple(max(hm(t)[j][i] for i in range(3)) for j in range(3))   # front (left) -> back (right)
def top(t): return tuple(int(hm(t)[j][i] > 0) for j in range(3) for i in range(3))


VIEW = {'front': front, 'right': right, 'top': top}
SIL = {'A': ('front', front(TOWERS[2])), 'B': ('right', right(TOWERS[4])), 'C': ('top', top(TOWERS[1])), 'D': ('front', front(TOWERS[3]))}

H, F, V = view.all_visible_sets()
key = {tuple(int(x) for x in H[k]): V[k].tobytes() for k in range(len(H))}
from collections import Counter
cnt = Counter(key.values())
for n, t in TOWERS.items(): assert cnt[key[t]] == 1, n

sols = [''.join(c) for c in itertools.product('1234', repeat=4)
        if all(VIEW[d](TOWERS[int(c[i])]) == s for i, (d, s) in enumerate(SIL.values()))]
mirror = [''.join(c) for c in itertools.product('1234', repeat=4)
          if all((VIEW[d](TOWERS[int(c[i])])[::-1] if d == 'right' else VIEW[d](TOWERS[int(c[i])])) == s for i, (d, s) in enumerate(SIL.values()))]
print('solutions', sols, 'right view mirrored', mirror)
assert sols == ['2413'] and '2413' not in mirror
json.dump({'unique_answer': sols[0], 'codes_tested': 4 ** 4, 'towers': TOWERS, 'silhouettes': SIL, 'right_view_mirrored': mirror,
           'why': 'A(앞) = 2번, B(오른쪽) = 4번, C(위) = 1번, D(앞) = 3번'},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
