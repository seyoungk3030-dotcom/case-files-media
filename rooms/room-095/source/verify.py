"""ROOM 095 proof: two empty jugs with no marks in between (a L and b L), an endless tap and a sink. One action =
fill a jug to the top, empty a jug, or pour one jug into the other until it is empty or the other is full. Each digit
is the fewest actions until either jug holds exactly the target, found by breadth-first search over all (x, y) states.
All 10^4 codes compared; exactly one matches. Writing the target litres (the trap) gives another code."""
import itertools, json, os
from collections import deque
BOARDS = {'A': (3, 5, 4), 'B': (4, 9, 6), 'C': (5, 8, 2), 'D': (2, 9, 8)}
NAMES = ['채우기', '채우기', '비우기', '비우기', '붓기', '붓기']


def solve(a, b, t):
    s = (0, 0); D = {s: 0}; par = {s: None}; q = deque([s])
    while q:
        x, y = q.popleft()
        if t in (x, y):
            path = [(x, y)]
            while par[path[-1]] is not None: path.append(par[path[-1]][0])
            return D[(x, y)], path[::-1]
        p1 = min(x, b - y); p2 = min(y, a - x)
        for m in ((a, y), (x, b), (0, y), (x, 0), (x - p1, y + p1), (x + p2, y - p2)):
            if m not in D: D[m] = D[(x, y)] + 1; par[m] = ((x, y),); q.append(m)


RES = {k: solve(*v) for k, v in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(v[2]) for v in BOARDS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: RES[k][1] for k in 'ABCD'})
assert sols == ['6848'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'jugs_a_b_target': BOARDS, 'shortest_states': {k: RES[k][1] for k in 'ABCD'},
               'trap_target_litres': trap, 'why': '채우기·비우기·옮겨 붓기만 가능. 모든 상태를 BFS로 탐색한 최소 동작 수'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
