"""ROOM 039 proof: a tray has four holes A-D, each shaped like four joined squares, and four loose pieces 1-4.
Pieces may turn but not flip (their top is painted). Code = the piece that fits hole A, B, C, D.
All 4! assignments are tested; exactly one fits. Allowing flips makes the L and J pieces fit both L/J holes (trap)."""
import itertools, json, os
L = {(0, 0), (0, 1), (0, 2), (1, 0)}; J = {(1, 0), (1, 1), (1, 2), (0, 0)}
T = {(0, 1), (1, 1), (2, 1), (1, 0)}; S = {(0, 0), (1, 0), (1, 1), (2, 1)}


def norm(c):
    mx, my = min(x for x, _ in c), min(y for _, y in c); return frozenset((x - mx, y - my) for x, y in c)


def rot(c, k):
    for _ in range(k): c = {(y, -x) for x, y in c}
    return norm(c)


def turns(c, flip=False):
    out = {rot(c, k) for k in range(4)}
    return out | ({rot({(-x, y) for x, y in c}, k) for k in range(4)} if flip else set())


HOLES = {'A': rot(L, 0), 'B': rot(T, 2), 'C': rot(J, 0), 'D': rot(S, 1)}
PIECES = {1: rot(J, 1), 2: rot(S, 0), 3: rot(L, 2), 4: rot(T, 1)}


def solve(flip):
    return [''.join(map(str, p)) for p in itertools.permutations(PIECES)
            if all(HOLES[h] in turns(PIECES[n], flip) for h, n in zip('ABCD', p))]


sols, loose = solve(False), solve(True)
print('solutions', sols, 'with flips', loose)
assert sols == ['3412'] and len(loose) > 1
json.dump({'unique_answer': sols[0], 'assignments_tested': 24, 'with_flips_allowed': loose, 'trap': '1432',
           'holes': {k: sorted(v) for k, v in HOLES.items()}, 'pieces': {k: sorted(v) for k, v in PIECES.items()},
           'why': 'A는 L 모양 → 3번(L을 뒤집지 않고 돌린 것) · B는 T → 4번 · C는 J → 1번 · D는 S → 2번'},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
