"""ROOM 091 proof: tiny warehouse puzzles. The worker walks up, down, left or right and can only PUSH the box (never
pull it, never through walls #). Each digit is the fewest pushes that get the box onto the goal G, found by a 0-1
breadth-first search over (worker, box) positions (walking costs 0, a push costs 1). All 10^4 codes compared; exactly
one matches. The straight-line grid distance from box to goal (the trap) gives another code."""
import itertools, json, os
from collections import deque
BOARDS = {'A': ['#..P.#', 'GB#.#.', '......', '....#.', '.....#'],
          'B': ['...#..', '..B.#.', '..#...', '..P...', '#.#..G'],
          'C': ['#....G', '#..B..', '#..#.#', '.P#...', '.#..##'],
          'D': ['#....P', '..B.#.', '.#....', '..#...', '#G....']}
DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def find(G, ch): return next((r, c) for r, row in enumerate(G) for c, x in enumerate(row) if x == ch)


def solve(G):
    H, W = len(G), len(G[0]); p, b, g = find(G, 'P'), find(G, 'B'), find(G, 'G')
    free = lambda q: 0 <= q[0] < H and 0 <= q[1] < W and G[q[0]][q[1]] != '#'
    D = {(p, b): 0}; par = {(p, b): None}; dq = deque([(p, b)])
    while dq:
        s = dq.popleft(); pp, bb = s; d = D[s]
        if bb == g:
            path = [bb]
            while par[s] is not None:
                s = par[s]
                if s[1] != path[-1]: path.append(s[1])
            return d, path[::-1]
        for dr, dc in DIRS:
            n = (pp[0] + dr, pp[1] + dc)
            if not free(n): continue
            if n == bb:
                nb = (bb[0] + dr, bb[1] + dc)
                if not free(nb): continue
                t, w = (n, nb), 1
            else: t, w = (n, bb), 0
            if t not in D or D[t] > d + w:
                D[t] = d + w; par[t] = s; (dq.append if w else dq.appendleft)(t)


RES = {k: solve(v) for k, v in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD')
trap = ''.join(str(abs(find(v, 'B')[0] - find(v, 'G')[0]) + abs(find(v, 'B')[1] - find(v, 'G')[1])) for k, v in BOARDS.items())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: RES[k][1] for k in 'ABCD'})
assert sols == ['3856'] and trap != code and all(len(RES[k][1]) - 1 == RES[k][0] for k in 'ABCD')
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'box_paths': {k: RES[k][1] for k in 'ABCD'},
               'trap_grid_distance': trap, 'why': '상자는 밀기만 돼요. 밀려면 상자 반대편에 서야 해서 벽이 막으면 돌아가야 해요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
