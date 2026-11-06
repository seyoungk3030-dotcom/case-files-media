"""ROOM 142 proof: snakes and ladders on a 5x5 board (squares 1-25, snaking up from the bottom-left). The token starts on
square 1. Each turn YOU choose the die roll (1-6) - the best possible luck. Landing on a ladder's foot climbs to its top;
landing on a snake's head slides to its tail. A roll that would pass 25 is not allowed to move the token (it stays).
Breadth-first search over every choice gives the fewest rolls to reach 25 exactly. All 10^4 codes compared; exactly
one matches. The trap: always rolling the biggest number you can (6, or exactly what is left)."""
import itertools, json, os
from collections import deque
END = 25
BOARDS = {'A': {2: 16, 3: 13, 19: 14, 23: 8}, 'B': {19: 10, 22: 14}, 'C': {4: 20, 17: 23, 12: 16, 18: 10}, 'D': {8: 16, 10: 15, 13: 9, 22: 3}}


def step(p, r, J):
    q = p + r
    return p if q > END else J.get(q, q)


def best(J):
    prev = {1: None}; q = deque([1])
    while q:
        p = q.popleft()
        if p == END:
            path = []
            while prev[p] is not None: p, r = prev[p]; path.append(r)
            return path[::-1]
        for r in range(1, 7):
            n = step(p, r, J)
            if n not in prev: prev[n] = (p, r); q.append(n)


def greedy(J):
    p = 1
    for t in range(1, 30):
        p = step(p, 6 if p + 6 <= END else END - p, J)
        if p == END: return t


for J in BOARDS.values(): assert all(a not in J for a in J.values()) and 1 not in J and END not in J
ROLLS = {k: best(J) for k, J in BOARDS.items()}
code = ''.join(str(len(ROLLS[k])) for k in 'ABCD'); trap = ''.join(str(greedy(BOARDS[k])) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, ROLLS)
assert sols == ['3524'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': {k: {str(a): b for a, b in J.items()} for k, J in BOARDS.items()}, 'rolls': ROLLS,
               'trap_always_six': trap, 'why': '무조건 큰 수가 좋은 게 아니에요. 사다리 발판에 맞춰 작게 굴리고, 뱀 머리는 피해야 해요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
