"""ROOM 127 proof: an ant at the front-bottom-left corner of a box (grid of unit squares) wants the sugar at the
back-top-right corner. Four routes over the visible faces are drawn, each with a number:
 R1 straight across the front face then straight across the top (unfolded: one line, sqrt(x^2 + (y+z)^2)),
 R2 straight across the front face then the right face (sqrt((x+y)^2 + z^2)),
 R3 the front face's diagonal then along the top-right edge (sqrt(x^2+z^2) + y),
 R4 straight up the front-left edge then the top face's diagonal (z + sqrt(x^2+y^2)).
Digit = the number on the shortest route. All 10^4 codes are compared; exactly one matches. The trap: the
'diagonal then edge' route R3, which feels direct."""
import itertools, json, math, os

BOARDS = {'A': {'size': [3, 1, 2], 'labels': [7, 2, 5, 9]},
          'B': {'size': [1, 3, 2], 'labels': [4, 1, 8, 6]},
          'C': {'size': [2, 2, 1], 'labels': [3, 6, 2, 8]},
          'D': {'size': [2, 1, 3], 'labels': [5, 9, 4, 1]}}


def lengths(x, y, z):
    return [math.hypot(x, y + z), math.hypot(x + y, z), math.hypot(x, z) + y, z + math.hypot(x, y)]


def solve(b):
    L = lengths(*b['size']); order = sorted(range(4), key=L.__getitem__); assert L[order[1]] - L[order[0]] > 0.15
    assert len(set(b['labels'])) == 4
    return b['labels'][order[0]], b['labels'][2], [round(v, 2) for v in L]


RES = {k: solve(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4))
        if all(int(c[i]) == BOARDS[k]['labels'][min(range(4), key=lengths(*BOARDS[k]['size']).__getitem__)] for i, k in enumerate('ABCD'))]
print('answer', code, 'trap', trap, {k: v[2] for k, v in RES.items()})
assert sols == ['7139'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'route_lengths': {k: v[2] for k, v in RES.items()},
               'trap_diagonal_then_edge': trap,
               'why': '상자를 펼치면 가장 짧은 길은 한 번에 그은 곧은 선이에요. 어느 두 면을 펼치느냐에 따라 길이가 달라요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
