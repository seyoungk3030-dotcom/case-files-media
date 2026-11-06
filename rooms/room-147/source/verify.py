"""ROOM 147 proof: walking on a floating raft. A person stands on the left end of a raft at dock mark s and walks to
the right end (raft length L marks). Water drag is negligible, so nothing pushes the person+raft system sideways: its
centre of mass stays put. With the raft weighing M people, the person moves L*M/(M+1) marks to the right while the raft
slides L/(M+1) to the left. Digit = the dock mark the person ends at. All 10^4 codes compared; exactly one matches.
The trap: s + L (as if the raft were tied to the dock)."""
import itertools, json, os
from fractions import Fraction as F
BOARDS = {'A': {'s': 1, 'L': 6, 'M': 2}, 'B': {'s': 0, 'L': 8, 'M': 3}, 'C': {'s': 2, 'L': 4, 'M': 1}, 'D': {'s': 3, 'L': 5, 'M': 4}}


def end(b):
    p = F(b['s']) + F(b['L'] * b['M'], b['M'] + 1); assert p.denominator == 1; return int(p)


def raft_shift(b): return F(b['L'], b['M'] + 1)


for b in BOARDS.values():  # centre of mass check: person (1) and raft (M) about the same point before and after
    r0 = b['s'] + F(b['L'], 2); p1 = end(b); r1 = r0 - raft_shift(b)
    assert (b['s'] + b['M'] * r0) == (p1 + b['M'] * r1)
code = ''.join(str(end(BOARDS[k])) for k in 'ABCD'); trap = ''.join(str(b['s'] + b['L']) for b in BOARDS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['5647'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'raft_shift': {k: str(raft_shift(b)) for k, b in BOARDS.items()},
               'trap_raft_fixed': trap, 'why': '사람이 앞으로 걸으면 뗏목은 뒤로 밀려요. 둘의 무게중심은 제자리라서, 가벼운 쪽이 더 많이 움직여요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
