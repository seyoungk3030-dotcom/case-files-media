"""ROOM 190 proof: round-trip average speed. A car drives the same road there and back. Average speed = total distance /
total time = 2ab/(a+b) (harmonic mean), not (a+b)/2: the slow leg takes longer, so it weighs more. Digit = average speed
in km/h divided by 10 (every board's average is a whole multiple of 10; the distance cancels out, so it is not given).
All 10^4 codes compared; exactly one matches. The trap: averaging the two speeds."""
import itertools, json, os
from fractions import Fraction as Fr

BOARDS = {'A': (60, 20), 'B': (40, 120), 'C': (50, 50), 'D': (120, 60)}  # km/h there, back


def avg(a, b, trap=False):
    v = Fr(a + b, 2) if trap else Fr(2 * a * b, a + b)
    assert v.denominator == 1 and v % 10 == 0 and 10 <= v <= 90; return int(v // 10)


GOOD = {k: avg(*v) for k, v in BOARDS.items()}; TRAPV = {k: avg(*v, trap=True) for k, v in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
for k, (a, b) in BOARDS.items():  # check with a real distance: 60 km each way
    t = Fr(60, a) + Fr(60, b); assert Fr(120) / t == GOOD[k] * 10
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and sum(GOOD[k] != TRAPV[k] for k in 'ABCD') == 3
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards_there_back_kmh': BOARDS,
               'average_kmh': {k: GOOD[k] * 10 for k in 'ABCD'}, 'trap_mean_of_speeds': trap,
               'example': 'A: 60km 길을 60km/h로 1시간, 20km/h로 3시간 = 120km/4시간 = 30km/h',
               'why': '평균 속도는 전체 거리 ÷ 전체 시간이라 느린 쪽에 더 오래 머물러요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
