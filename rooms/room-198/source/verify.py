"""ROOM 198 proof (엘리베이터 저울): a 5 kg watermelon sits on a kitchen scale on the floor of a lift. When the lift's speed
changes it does so by 2 m/s every second (g = 10 m/s^2). The scale reads the push N = m(g + a) / g, with a the lift's
acceleration (up = +). Speeding up while going up or slowing down while going down both mean a = +2 (reads 6); steady
motion a = 0 (reads 5); slowing while going up or speeding up while going down a = -2 (reads 4).
All 10^4 codes compared, exactly one matches. Traps: 'a scale always shows the true weight' (5555) and 'up is heavier,
down is lighter' (6446)."""
import itertools, json, os
from fractions import Fraction as F

M, G, ACC = 5, 10, 2
# key: (direction of motion, speed change)
BOARDS = {'A': ('up', 'faster'), 'B': ('down', 'steady'), 'C': ('down', 'slower'), 'D': ('up', 'slower')}


def accel(d, ch):
    if ch == 'steady': return 0
    sgn = 1 if d == 'up' else -1          # velocity sign
    return sgn * ACC if ch == 'faster' else -sgn * ACC


def reading(d, ch): return F(M * (G + accel(d, ch)), G)


GOOD = {k: reading(*v) for k, v in BOARDS.items()}
for k, r in GOOD.items(): assert r.denominator == 1 and 0 <= r < 10
code = ''.join(str(int(GOOD[k])) for k in 'ABCD')
trap1 = str(M) * 4
trap2 = ''.join(str(M + (1 if BOARDS[k][0] == 'up' else -1) * (0 if BOARDS[k][1] == 'steady' else 1)) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'traps', trap1, trap2)
assert len(sols) == 1 and code not in (trap1, trap2)
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'mass_kg': M, 'g': G, 'accel': ACC, 'boards': BOARDS,
               'readings': {k: int(v) for k, v in GOOD.items()}, 'trap_true_weight': trap1, 'trap_up_heavy_down_light': trap2,
               'why': '저울은 바닥이 미는 힘을 재요. 위로 빨라지거나 아래로 가다 멈출 때 더 세게 밀어요(더 무거움)'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
