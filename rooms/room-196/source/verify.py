"""ROOM 196 proof (기름 아끼기): each car drives 60 km. Its fuel economy goes from old to new km/L. Fuel used = 60 / km/L,
so the litres saved are 60/old - 60/new. Digit = litres saved (all whole numbers). All 10^4 codes compared; exactly one
matches. The trap: thinking the biggest km/L jump saves the most (B doubles 15 -> 30 but saves only 2 L)."""
import itertools, json, os
from fractions import Fraction as F

KM = 60
BOARDS = {'A': (4, 6), 'B': (15, 30), 'C': (3, 4), 'D': (12, 15)}  # km/L before, after


def used(e): return F(KM, e)


GOOD = {}
for k, (a, b) in BOARDS.items():
    s = used(a) - used(b); assert s.denominator == 1 and 0 < s < 10, (k, s); GOOD[k] = int(s)
TRAP = {k: (b - a) % 10 for k, (a, b) in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAP[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(code[i] != trap[i] for i in range(4))
assert max(BOARDS, key=lambda k: BOARDS[k][1] - BOARDS[k][0]) == 'B' and GOOD['B'] < GOOD['A']
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'km': KM, 'boards': BOARDS,
               'litres': {k: [int(used(a)), int(used(b))] for k, (a, b) in BOARDS.items()}, 'trap_code_kmL_gain': trap,
               'why': '쓰는 기름 = 거리 ÷ 연비. 연비가 낮은 차일수록 조금만 올라도 기름이 많이 줄어요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
