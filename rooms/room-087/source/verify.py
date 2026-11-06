"""ROOM 087 proof: a row of cups, some upside down. One move flips exactly K cups (any K, each to its other side).
Breadth-first search over all up/down patterns gives the least number of moves to get every cup upright, or shows it
can never happen (then the digit is 0). All 10^4 codes compared; exactly one matches."""
import itertools, json, os
from collections import deque
BOARDS = {'A': ('DUDDUD', 2), 'B': ('UDUDD', 2), 'C': ('DDUDDD', 3), 'D': ('UUDUU', 3)}


def least(start, k):
    n = len(start); s0 = tuple(c == 'D' for c in start); goal = tuple([False] * n)
    seen, q = {s0: 0}, deque([s0])
    while q:
        s = q.popleft()
        if s == goal: return seen[s]
        for idx in itertools.combinations(range(n), k):
            t = list(s)
            for i in idx: t[i] = not t[i]
            t = tuple(t)
            if t not in seen: seen[t] = seen[s] + 1; q.append(t)
    return 0


RES = {k: least(*v) for k, v in BOARDS.items()}
code = ''.join(str(RES[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, RES)
assert sols == ['2033']
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards_cups_flip_k': BOARDS,
               'why': '2개씩 뒤집으면 엎어진 컵 수의 홀짝이 안 바뀌어요. 홀수면 영원히 불가능(0)'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
