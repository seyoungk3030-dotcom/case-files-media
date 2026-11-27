"""ROOM 211 proof (호스 끝을 손가락으로 막으면): the tap sends a fixed amount of water per minute Q through the hose. All of
it leaves through the opening of area A, so the jet speed is v = Q / A (Q in L/min = 1000/60 cm^3/s, A in cm^2). Pressing a
thumb over the end makes A smaller, so the same water must leave faster. Digit = jet speed in m/s. Integer on every board,
checked exactly with fractions. The jet range from 1 m height, v*sqrt(2h/g), is only used for the drawing. All 10^4 codes
compared; exactly one matches. Trap: 'blocking the hose lets less water out, so it is slower'."""
import itertools, json, math, os
from fractions import Fraction as Fr

H = 1.0
# key: (label, flow L/min, opening cm^2, thumb)
BOARDS = {'A': ('손 안 댐', 12, Fr(2), False), 'B': ('손가락으로 막음', 12, Fr(1, 2), True),
          'C': ('수도 더 세게 + 막음', 18, Fr(1, 2), True), 'D': ('더 좁게 막음', 12, Fr(1, 4), True)}


def speed(q, a):
    return Fr(q * 1000, 60) / a / 100      # cm/s -> m/s


GOOD, RANGE = {}, {}
for k, (lb, q, a, th) in BOARDS.items():
    v = speed(q, a); assert v.denominator == 1 and 0 <= v < 10, (k, v)
    GOOD[k] = int(v); RANGE[k] = round(float(v) * math.sqrt(2 * H / 9.81), 2)
code = ''.join(str(GOOD[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, RANGE)
assert len(sols) == 1
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000,
               'boards': {k: {'label': lb, 'flow_L_min': q, 'opening_cm2': str(a), 'speed_m_s': GOOD[k], 'range_m_from_1m': RANGE[k]} for k, (lb, q, a, th) in BOARDS.items()},
               'trap': '막으면 물이 덜 나와서 느려진다', 'why': '1초에 나오는 물의 양은 같으니, 구멍 넓이가 1/4이 되면 물은 4배 빨라야 다 빠져나가요 (속도 = 양 ÷ 넓이)'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
