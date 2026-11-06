"""ROOM 089 proof: tower-of-hanoi positions. Move one disc at a time (the top disc of a peg), never onto a smaller disc.
Each digit is the fewest moves to stack every disc on the right peg (peg 3), found by breadth-first search over all
legal positions. All 10^4 codes compared; exactly one matches. Counting the discs not yet on peg 3 (the trap) gives
another code."""
import itertools, json, os
from collections import deque
# disc 0 is the smallest; value = peg (0 left, 1 middle, 2 right / goal)
BOARDS = {'A': (2, 1, 0), 'B': (0, 1, 2, 2), 'C': (2, 0, 0, 1), 'D': (2, 0, 0)}


def moves(s):
    n = len(s)
    for a in range(3):
        da = [i for i in range(n) if s[i] == a]
        if not da: continue
        d = min(da)
        for b in range(3):
            if b == a: continue
            db = [i for i in range(n) if s[i] == b]
            if db and min(db) < d: continue
            t = list(s); t[d] = b; yield tuple(t)


def dist(s):
    goal = tuple([2] * len(s)); D = {s: 0}; q = deque([s]); prev = {s: None}
    while q:
        u = q.popleft()
        if u == goal:
            path = [u]
            while prev[path[-1]] is not None: path.append(prev[path[-1]])
            return D[u], path[::-1]
        for t in moves(u):
            if t not in D: D[t] = D[u] + 1; prev[t] = u; q.append(t)


RES = {k: dist(v) for k, v in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(sum(p != 2 for p in BOARDS[k])) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['5296'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards_disc_pegs': BOARDS, 'trap_discs_off_goal': trap,
               'shortest_paths': {k: RES[k][1] for k in 'ABCD'},
               'why': '한 번에 맨 위 원판 하나만, 작은 원판 위에 큰 원판은 금지. 모든 경우를 BFS로 탐색한 최소 이동 수'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
