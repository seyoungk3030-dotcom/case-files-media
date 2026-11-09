"""ROOM 165 proof: pancakes. Each pancake must be cooked on both sides; one side takes 1 minute. The pan holds k
pancakes at a time; any pancake can be flipped, taken out or put back at each minute. For each board (k, n pancakes) a
breadth-first search over states (how many pancakes have 0, 1, 2 sides done) finds the minimum number of minutes.
Digit = that minimum. All 10^4 codes compared; exactly one matches. The trap: cooking pancakes in full batches, both
sides at once per batch (2 * ceil(n / k) minutes), which leaves the pan half empty in the last batch."""
import itertools, json, math, os
from collections import deque

BOARDS = {'A': {'k': 2, 'n': 3}, 'B': {'k': 2, 'n': 7}, 'C': {'k': 3, 'n': 4}, 'D': {'k': 4, 'n': 6}}


def best(k, n):
    start, goal = (n, 0, 0), (0, 0, n); seen = {start: 0}; q = deque([start]); prev = {start: None}
    while q:
        s = q.popleft()
        if s == goal: break
        z, o, t = s
        for a in range(z + 1):
            for b in range(o + 1):
                if 0 < a + b <= k:
                    ns = (z - a, o - b + a, t + b)
                    if ns not in seen: seen[ns] = seen[s] + 1; prev[ns] = (s, a, b); q.append(ns)
    plan = []; s = goal
    while prev[s]: s0, a, b = prev[s]; plan.append((a, b)); s = s0
    return seen[goal], plan[::-1]


GOOD = {}; PLAN = {}; TRAPV = {}
for key, b in BOARDS.items():
    GOOD[key], PLAN[key] = best(b['k'], b['n'])
    assert GOOD[key] == math.ceil(2 * b['n'] / b['k'])
    TRAPV[key] = 2 * math.ceil(b['n'] / b['k'])
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, PLAN)
assert len(sols) == 1 and all(GOOD[k] < TRAPV[k] for k in 'ABCD')
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'minutes': GOOD, 'plans': PLAN,
               'trap_batches': trap,
               'why': '한 판씩 양면을 다 굽지 말고, 팬이 비는 칸 없이 계속 채워 구우면 시간이 줄어요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
