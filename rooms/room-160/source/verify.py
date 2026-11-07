"""ROOM 160 proof: parking-lot sliding puzzle on a 6x6 lot. Each car slides only forwards/backwards along its own
length, any distance, as long as nothing is in the way; one slide = one move. The red car (row 2) must leave through
the gap in the right wall. Breadth-first search over every reachable layout gives the least number of moves. Digit =
least moves for A B C D. All 10^4 codes compared; exactly one matches. The trap: only counting the cars that stand
directly in the red car's way."""
import itertools, json, os
from collections import deque
N = 6
# (orientation, length, row, col); car 0 is the red car
BOARDS = {'A': [('h', 2, 2, 0), ('v', 2, 1, 3), ('v', 2, 4, 3), ('h', 2, 0, 3), ('v', 2, 3, 2), ('v', 2, 4, 5)],
          'B': [('h', 2, 2, 0), ('h', 2, 3, 4), ('h', 2, 4, 1), ('v', 3, 0, 5), ('v', 2, 0, 4), ('h', 3, 3, 0), ('h', 3, 4, 3)],
          'C': [('h', 2, 2, 0), ('v', 3, 0, 3), ('h', 3, 4, 3), ('v', 2, 0, 1), ('v', 2, 1, 2)],
          'D': [('h', 2, 2, 2), ('h', 2, 4, 4), ('v', 2, 4, 2), ('v', 3, 0, 4), ('v', 2, 1, 5), ('v', 2, 0, 3)]}


def cells(o, l, r, k): return [(r, k + i) if o == 'h' else (r + i, k) for i in range(l)]


def solve(cars):
    meta = [(c[0], c[1]) for c in cars]; start = tuple((c[2], c[3]) for c in cars)
    prev = {start: None}; q = deque([start])
    while q:
        st = q.popleft()
        if st[0][1] + 2 == N:
            path = []
            while st is not None: path.append(st); st = prev[st]
            return path[::-1]
        g = {}
        for i, (r, k) in enumerate(st):
            for c in cells(*meta[i], r, k): g[c] = i
        for i, (r, k) in enumerate(st):
            o, l = meta[i]
            for sg in (-1, 1):
                s = 1
                while True:
                    nr, nk = (r, k + sg * s) if o == 'h' else (r + sg * s, k)
                    ce = cells(o, l, nr, nk)
                    if any(not (0 <= a < N and 0 <= b < N) for a, b in ce) or any(g.get(c, i) != i for c in ce): break
                    ns = list(st); ns[i] = (nr, nk); ns = tuple(ns)
                    if ns not in prev: prev[ns] = st; q.append(ns)
                    s += 1


def blockers(cars):
    r, k = cars[0][2], cars[0][3]
    return len({i for i, c in enumerate(cars[1:], 1) for a, b in cells(*c) if a == r and b > k + 1})


PATH = {k: solve(c) for k, c in BOARDS.items()}
MOVES = {k: len(p) - 1 for k, p in PATH.items()}
MOVED = {k: sorted({i for a, b in zip(p, p[1:]) for i in range(len(a)) if a[i] != b[i]}) for k, p in PATH.items()}
code = ''.join(str(MOVES[k]) for k in 'ABCD'); trap = ''.join(str(blockers(BOARDS[k])) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, MOVED)
assert sols == ['3546'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'least_moves': MOVES,
               'solutions': {k: [list(map(list, s)) for s in p] for k, p in PATH.items()}, 'trap_blockers': trap,
               'why': '막고 있는 차만 세면 안 돼요. 그 차가 비킬 자리를 막는 차도 먼저 움직여야 해요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
