"""ROOM 121 proof: hang it on a pin. A flat wooden plate made of equal squares (uniform weight) hangs freely from a
pin through the middle of one square. It swings until its centre of mass is straight below the pin. Four numbered
corners are marked; the digit is the one that ends up LOWEST. 'Down' after hanging = the direction pin -> centre
of mass, so the lowest mark has the largest projection on it (each win kept >= 0.35 square ahead). All 10^4 codes
are compared; exactly one matches. The trap: the mark that is lowest in the picture before it is let go."""
import itertools, json, math, os

BOARDS = {'A': {'cells': [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [1, 3], [2, 2]], 'pin': [0.5, 1.5], 'marks': {8: [0, 3], 6: [2, 4], 3: [1, 4], 7: [0, 0]}},
          'B': {'cells': [[0, 0], [0, 1], [1, 0], [1, 1], [2, 0], [2, 1], [2, 2]], 'pin': [2.5, 1.5], 'marks': {5: [2, 3], 4: [0, 2], 3: [3, 0], 9: [3, 3]}},
          'C': {'cells': [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 2], [3, 2]], 'pin': [0.5, 0.5], 'marks': {5: [4, 3], 8: [0, 0], 1: [4, 2], 2: [0, 3]}},
          'D': {'cells': [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [2, 1]], 'pin': [2.5, 1.5], 'marks': {9: [1, 3], 3: [2, 0], 5: [3, 2], 8: [3, 1]}}}


def com(b): n = len(b['cells']); return (sum(x + 0.5 for x, y in b['cells']) / n, sum(y + 0.5 for x, y in b['cells']) / n)


def solve(b):
    cx, cy = com(b); px, py = b['pin']; d = math.hypot(cx - px, cy - py); ux, uy = (cx - px) / d, (cy - py) / d
    depth = sorted(((m[0] - px) * ux + (m[1] - py) * uy, n) for n, m in b['marks'].items())[::-1]
    assert depth[0][0] - depth[1][0] >= 0.35 and d >= 0.6
    low = sorted((m[1], n) for n, m in b['marks'].items())
    return depth[0][1], low[0][1], math.degrees(math.atan2(ux, -uy))


RES = {k: solve(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['6459'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'centre_of_mass': {k: com(b) for k, b in BOARDS.items()},
               'trap_lowest_before': trap, 'why': '매달린 물체는 무게중심이 못 바로 아래에 올 때까지 돌아가요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
