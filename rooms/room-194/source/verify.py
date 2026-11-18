"""ROOM 194 proof (편의점 행사): each board is one convenience-store deal bought exactly once. The real discount is
(full price of everything you take home - what you pay) / full price of everything you take home. 2+1 = pay 2 of 3
(33%), second-one-half-price = pay 1.5 of 2 (25%), 1+1 = pay 1 of 2 (50%), third-one-half-price = pay 2.5 of 3 (16.7%).
Digit = tens digit of that percent. All 10^4 codes compared; exactly one matches. The trap: reading any 'half price'
deal as 50% off."""
import itertools, json, os
from fractions import Fraction as F

# name, items taken, items paid (fractions allowed), product
BOARDS = {'A': ('2+1', 3, F(2), '캔커피'), 'B': ('두 번째 반값', 2, F(3, 2), '아이스크림'), 'C': ('1+1', 2, F(1), '우유'), 'D': ('세 번째 반값', 3, F(5, 2), '컵라면')}


def pct(take, pay): return (take - pay) / take * 100


GOOD = {k: int(pct(t, p)) // 10 for k, (n, t, p, _) in BOARDS.items()}
for k, (n, t, p, _) in BOARDS.items():
    v = pct(t, p); assert abs(v - round(v / 10) * 10) >= 1.5 or v == int(v), (k, v)
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join('5' if '반값' in BOARDS[k][0] else str(GOOD[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and code != trap
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'deals': {k: [v[0], v[1], str(v[2]), v[3]] for k, v in BOARDS.items()},
               'percent': {k: round(float(pct(v[1], v[2])), 1) for k, v in BOARDS.items()}, 'trap_half_price_read_as_50': trap,
               'why': '할인율 = 공짜로 받은 몫 ÷ 가져간 전체 개수. 두 번째 반값은 2개 중 0.5개가 공짜라서 25%'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
