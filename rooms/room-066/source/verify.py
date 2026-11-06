"""ROOM 066 proof: a spool (wheel radius R, axle radius r = R/2) rolls without slipping on the floor; its thread leaves the
axle horizontally, from the bottom or the top of the axle, towards the hand. Rolling at speed v, the floor contact point is
at rest, so a point at height h above the floor moves at v*h/R. The thread's tangent point (bottom of axle h = R - r, top
h = R + r) moves at the hand's speed, so the hand pulling L makes the spool roll d = L*R/(R-r) (bottom, thread winds up)
or d = L*R/(R+r) (top, thread unwinds). Every 4-digit code is compared; exactly one matches. 'Moves as far as pulled'
gives the trap, and ignoring top/bottom fails."""
import itertools, json, os
from fractions import Fraction as F
R, r = F(2), F(1)
BOARDS = {'A': ('bottom', 3), 'B': ('top', 6), 'C': ('bottom', 4), 'D': ('top', 3)}   # where the thread leaves the axle, tiles pulled


def roll(side, L):
    h = R - r if side == 'bottom' else R + r    # height of the tangent point above the floor
    return L * R / h                            # tangent point speed = v*h/R


res = {}
for k, (s, L) in BOARDS.items():
    d = roll(s, L); assert d.denominator == 1, (k, d); res[k] = int(d)
code = ''.join(str(res[k]) for k in 'ABCD'); trap = ''.join(str(BOARDS[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
alt = [roll('bottom', L) for _, L in BOARDS.values()]   # ignoring which side the thread leaves
print('answer', code, 'trap', trap, 'solutions', sols, 'all-bottom', alt)
assert sols == ['6482'] and trap == '3643' and ''.join(map(str, alt)) != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'wheel_axle_radius': [2, 1],
               'boards_side_pulled': BOARDS, 'rolled': res, 'trap_same_as_pulled': trap,
               'why': '바닥 닿은 점은 정지, 축 아래쪽은 실패 속도의 1/2, 위쪽은 3/2로 움직임. 아래 실: 당긴 길이×2, 위 실: ×2/3. A 3×2=6 · B 6×2/3=4 · C 4×2=8 · D 3×2/3=2'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
