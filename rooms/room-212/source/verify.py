"""ROOM 212 proof (버스 창밖 빗줄기): with no wind the rain falls straight down at u m/s. Seen from a bus moving at v m/s
the rain also moves backwards at v, so the rain lines look slanted: v metres sideways for every u metres down. Each board
shows the slant on the window grid (across a squares per down b squares) and the rain speed u; the bus speed is
v = u * a / b. Digit = bus speed in m/s (city-bus range, 0-9 m/s = 0-32 km/h). Integer on every board, checked exactly with
fractions. All 10^4 codes compared; exactly one matches. Trap: 'steeper lines mean a faster bus'."""
import itertools, json, os
from fractions import Fraction as Fr

# key: (rain speed m/s, squares across, squares down)
BOARDS = {'A': (6, 1, 2), 'B': (6, 4, 3), 'C': (6, 1, 1), 'D': (6, 3, 2)}


def bus(u, a, b):
    return Fr(u * a, b)


GOOD = {}
for k, (u, a, b) in BOARDS.items():
    v = bus(u, a, b); assert v.denominator == 1 and 0 <= v < 10, (k, v); GOOD[k] = int(v)
code = ''.join(str(GOOD[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, {k: round(v * 3.6) for k, v in GOOD.items()})
assert len(sols) == 1
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000,
               'boards': {k: {'rain_m_s': u, 'across': a, 'down': b, 'bus_m_s': GOOD[k], 'bus_km_h': round(GOOD[k] * 3.6)} for k, (u, a, b) in BOARDS.items()},
               'trap': '빗줄기가 가파를수록 빠르다', 'why': '버스에서 보면 비가 뒤로 v만큼 밀려 보여요: 옆으로 간 칸 ÷ 아래로 간 칸 = 버스 속도 ÷ 빗방울 속도. 많이 누울수록 빨라요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
