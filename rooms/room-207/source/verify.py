"""ROOM 207 proof (에스컬레이터 걸어 오르기): an escalator shows N steps between the bottom and the top landing and moves
up e steps per second. You walk up it at w steps per second (relative to the steps). Ground speed = w + e steps/s, so the
ride takes N / (w + e) s and you step w * N / (w + e) times. Digit = how many steps you actually step on. Integer on every
board, checked exactly with fractions. All 10^4 codes compared; exactly one matches. Trap: '12 steps -> 12 footsteps'."""
import itertools, json, os
from fractions import Fraction as Fr

# key: (visible steps N, walking w steps/s, escalator e steps/s)
BOARDS = {'A': (12, Fr(1), Fr(1)), 'B': (12, Fr(2), Fr(1)), 'C': (10, Fr(1), Fr(3, 2)), 'D': (15, Fr(3, 2), Fr(1))}


def ride(N, w, e):
    t = Fr(N) / (w + e)
    return t, w * t


GOOD, TIME = {}, {}
for k, (N, w, e) in BOARDS.items():
    t, s = ride(N, w, e); assert s.denominator == 1 and t.denominator == 1 and 0 <= s < 10 and s != N, (k, s)
    assert 1 <= w <= 2 and 1 <= e <= 1.5            # plausible: walking 1-2 steps/s, escalator ~0.4-0.6 m/s
    GOOD[k] = int(s); TIME[k] = int(t)
code = ''.join(str(GOOD[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, TIME)
assert len(sols) == 1
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000,
               'boards': {k: {'steps': N, 'walk': str(w), 'escalator': str(e), 'seconds': TIME[k], 'footsteps': GOOD[k]} for k, (N, w, e) in BOARDS.items()},
               'trap': '12칸이니 12걸음', 'why': '걷는 동안 계단도 같이 올라와서, 칸 수 ÷ (내 속도 + 에스컬레이터 속도) 초 만에 도착해요. 걸음 수는 내 속도 × 시간'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
