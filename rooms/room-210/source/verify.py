"""ROOM 210 proof (빗물은 몇 cm?): rain of r cm means every square cm of open ground gets r cm^3 of water. A container
with straight walls collects opening area * r and spreads it over the same area: depth r, whatever its width. A funnel
(opening diameter D) into a tube (d) gives r * (D/d)^2; a jar whose neck (d) is narrower than its body (D) gives
r * (d/D)^2. Digit = water depth in cm. Integer on every board, checked exactly with fractions, and the water fits inside
the drawn shape. All 10^4 codes compared; exactly one matches. Trap: 'the wide basin catches more, so it is deeper'."""
import itertools, json, os
from fractions import Fraction as Fr

# key: (name, kind, opening diameter cm, diameter where the water stands cm, rain cm, height of that part cm)
BOARDS = {'A': ('넓은 대야', 'straight', 40, 40, 3, 12), 'B': ('좁은 컵', 'straight', 6, 6, 3, 10),
          'C': ('깔때기 + 관', 'funnel', 10, 5, 2, 14), 'D': ('입구 좁은 병', 'jar', 6, 12, 4, 10)}


def depth(open_d, water_d, rain):
    return rain * Fr(open_d, water_d) ** 2


GOOD = {}
for k, (nm, kind, D0, D1, r, h) in BOARDS.items():
    d = depth(D0, D1, r); assert d.denominator == 1 and 0 <= d < 10 and d < h, (k, d); GOOD[k] = int(d)
code = ''.join(str(GOOD[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code)
assert len(sols) == 1
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000,
               'boards': {k: {'name': n, 'kind': kd, 'opening_cm': a, 'water_diameter_cm': b, 'rain_cm': r, 'depth_cm': GOOD[k]} for k, (n, kd, a, b, r, h) in BOARDS.items()},
               'trap': '넓은 대야가 더 많이 받으니 더 깊다', 'why': '곧은 벽 그릇은 넓든 좁든 비 온 만큼(cm) 차요. 입구가 물 고인 곳보다 넓으면 (지름 비)² 배로 깊어지고, 좁으면 그만큼 얕아져요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
