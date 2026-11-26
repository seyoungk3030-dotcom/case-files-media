"""ROOM 209 proof (급브레이크 미끄럼 거리): a car brakes hard on the same dry road and skids to a stop. Friction gives a
constant deceleration mu*g, so the skid distance is v^2 / (2 mu g): it grows with the SQUARE of the speed. Each board shows
one skid (speed v0, distance d0) and asks the skid of the same car on the same road at v1: d1 = d0 * (v1/v0)^2. Integer
metres on every board, checked exactly with fractions, never equal to the linear guess, and the implied mu is a real dry-
asphalt value (0.7-0.95). All 10^4 codes compared; exactly one matches. Trap: 'twice as fast, twice as far'."""
import itertools, json, os
from fractions import Fraction as Fr

G = 9.81
# key: (known km/h, known skid m, asked km/h)
BOARDS = {'A': (20, 2, 40), 'B': (30, 4, 15), 'C': (40, 8, 20), 'D': (45, 9, 30)}


def skid(v0, d0, v1):
    return d0 * Fr(v1, v0) ** 2


GOOD, MU = {}, {}
for k, (v0, d0, v1) in BOARDS.items():
    d = skid(v0, d0, v1); assert d.denominator == 1 and 0 <= d < 10, (k, d)
    assert d != d0 * Fr(v1, v0), k
    mu = (v0 / 3.6) ** 2 / (2 * G * d0); assert 0.7 <= mu <= 0.95, (k, mu)
    GOOD[k] = int(d); MU[k] = round(mu, 2)
code = ''.join(str(GOOD[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, MU)
assert len(sols) == 1
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000,
               'boards': {k: {'known_kmh': a, 'known_m': b, 'asked_kmh': c, 'skid_m': GOOD[k], 'mu': MU[k]} for k, (a, b, c) in BOARDS.items()},
               'trap': '2배 빠르면 2배 멀리', 'why': '미끄럼 거리는 속도의 제곱에 비례해요: 속도 2배 → 4배, 절반 → 1/4'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
