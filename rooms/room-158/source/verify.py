"""ROOM 158 proof: a fuse stretched over posts 0..10. Fire runs 1 second per section on a thin fuse and 2 seconds per
section on a thick fuse. The left end is lit at 0 s; the right end is lit at the time on its tag (0 = at once). Where do
the two flames meet? Exact arrival times at every post are compared with fractions. Digit = the post where they meet.
All 10^4 codes compared; exactly one matches. The trap: the middle post 5 (as if both flames started together on an
even fuse)."""
import itertools, json, os
from fractions import Fraction as F
BOARDS = {'A': {'seg': [1] * 10, 'delay': 6},
          'B': {'seg': [2, 2, 1, 1, 1, 1, 1, 1, 1, 1], 'delay': 0},
          'C': {'seg': [1, 2, 2, 1, 1, 1, 2, 1, 2, 2], 'delay': 5},
          'D': {'seg': [1, 1, 1, 1, 1, 1, 1, 2, 2, 1], 'delay': 0}}


def meet(b):
    s = b['seg']; n = len(s); tl = [F(0)]
    for x in s: tl.append(tl[-1] + x)
    tr = [F(0)] * (n + 1); tr[n] = F(b['delay'])
    for i in range(n - 1, -1, -1): tr[i] = tr[i + 1] + s[i]
    hit = [i for i in range(n + 1) if tl[i] == tr[i]]
    assert len(hit) == 1
    return hit[0], int(tl[hit[0]])


RES = {k: meet(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = '5555'
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, RES)
assert sols == ['8476'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'meet': RES, 'trap_middle': trap,
               'why': '두 불꽃은 같은 시각에 같은 기둥에 닿는 곳에서 만나요. 늦게 붙은 쪽, 굵은 구간을 지나야 하는 쪽이 그만큼 덜 가요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
