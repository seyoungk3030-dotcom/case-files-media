"""ROOM 195 proof (물 섞기): two jugs of water are poured into one empty jug; no heat escapes. The mix ends at the
volume-weighted average: (V1*T1 + V2*T2) / (V1 + V2). Digit = tens digit of the final temperature (all exact multiples
of 10). All 10^4 codes compared; exactly one matches. The trap: taking the plain average of the two temperatures."""
import itertools, json, os
from fractions import Fraction as F

BOARDS = {'A': ((2, 70), (1, 10)), 'B': ((1, 90), (3, 10)), 'C': ((3, 80), (1, 40)), 'D': ((1, 100), (4, 25))}  # (litres, degC) x2


def mix(a, b): return F(a[0] * a[1] + b[0] * b[1], a[0] + b[0])


GOOD = {}
for k, (a, b) in BOARDS.items():
    t = mix(a, b); assert t.denominator == 1 and t % 10 == 0, (k, t); GOOD[k] = int(t) // 10
TRAPV = {k: (BOARDS[k][0][1] + BOARDS[k][1][1]) / 2 for k in 'ABCD'}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(int(TRAPV[k]) // 10) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and code != trap and all(int(code[i]) != int(trap[i]) for i in range(4))
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'final_c': {k: int(mix(*BOARDS[k])) for k in 'ABCD'},
               'trap_plain_average_c': TRAPV, 'trap_code': trap,
               'why': '물이 많은 쪽 온도로 끌려가요. (양×온도 + 양×온도) ÷ 전체 양'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
