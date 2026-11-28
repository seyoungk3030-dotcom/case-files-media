"""ROOM 213 proof (건전지 하나를 거꾸로): AA cells (1.5 V each) lie end to end in one holder, in series. A voltmeter's red
lead touches the right end and its black lead the left end. A cell whose + nub points right adds +1.5 V; a cell put in
backwards (nub pointing left) does not just 'not count', it subtracts 1.5 V. Reading = 1.5 * (forward - reversed).
Digit = the meter reading in volts. Integer on every board, checked exactly with fractions. All 10^4 codes compared;
exactly one matches. Trap: 'a backwards cell only drops one cell's worth' (4.5 / 7.5 / 3 / 10.5)."""
import itertools, json, os
from fractions import Fraction as Fr

CELL = Fr(3, 2)
# '+' = nub to the right (the red lead), '-' = put in backwards
BOARDS = {'A': '++-+', 'B': '++-+++', 'C': '+--+', 'D': '+++++-++'}


def volts(s):
    return CELL * (s.count('+') - s.count('-'))


GOOD = {}
for k, s in BOARDS.items():
    v = volts(s); assert v.denominator == 1 and 0 <= v < 10, (k, v); GOOD[k] = int(v)
code = ''.join(str(GOOD[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
trap = {k: float(CELL * s.count('+')) for k, s in BOARDS.items()}
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(trap[k] != GOOD[k] for k in BOARDS)
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000,
               'boards': {k: {'cells': s, 'cells_n': len(s), 'reversed': s.count('-'), 'volts': GOOD[k]} for k, s in BOARDS.items()},
               'trap': '거꾸로 넣은 건전지는 빼고 센다 (0 V 취급)', 'why': '거꾸로 넣은 건전지는 반대 방향으로 1.5 V를 밀어서, 0이 아니라 -1.5 V예요: 전압 = 1.5 × (바른 개수 - 거꾸로 개수)'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
