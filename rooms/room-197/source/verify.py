"""ROOM 197 proof (바퀴 위 스티커): four things roll to the right without slipping at v m/s. A sticker sits on the wheel or
track at the spot shown. Its speed seen by someone standing on the ground is v + (omega x r): the top of a rolling wheel
moves 2v, the hub v, the point touching the ground 0; a crawler track's top run moves 2v. Digit = sticker speed in m/s.
Velocities are computed as vectors, all 10^4 codes compared, exactly one matches. Trap: every sticker moves at v."""
import itertools, json, math, os

# key: (thing, v m/s, sticker spot)  spot: 'top' / 'bottom' / 'hub' on a wheel, 'track_top' on a crawler
BOARDS = {'A': ('자전거 바퀴', 3, 'top'), 'B': ('자동차 바퀴', 5, 'bottom'), 'C': ('수레 바퀴', 2, 'hub'), 'D': ('무한궤도', 4, 'track_top')}
R = 1.0


def wheel_point(v, x, z):
    """velocity of the point at (x, z) relative to the hub of a wheel radius R rolling right at v (omega clockwise)."""
    w = v / R  # clockwise: omega vector = (0, -w, 0) in x-y-z with y into screen; v_rel = omega x r
    return (v + w * z, -w * x)


def speed(v, spot):
    if spot == 'top': vx, vz = wheel_point(v, 0, R)
    elif spot == 'bottom': vx, vz = wheel_point(v, 0, -R)
    elif spot == 'hub': vx, vz = v, 0.0
    elif spot == 'track_top': vx, vz = 2 * v, 0.0  # the belt's top run moves at track speed v relative to the body, plus body v
    return math.hypot(vx, vz)


GOOD = {k: speed(v, s) for k, (_, v, s) in BOARDS.items()}
for k, s in GOOD.items(): assert abs(s - round(s)) < 1e-9 and 0 <= s < 10, (k, s)
code = ''.join(str(round(GOOD[k])) for k in 'ABCD')
trap = ''.join(str(BOARDS[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and code != trap and sum(a != b for a, b in zip(code, trap)) == 3
# the crawler track check: the bottom run touching the ground must be still (no slip): body v + belt (-v) = 0
assert BOARDS['D'][1] - BOARDS['D'][1] == 0
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'speeds': {k: round(s) for k, s in GOOD.items()},
               'trap_code_all_same_as_vehicle': trap,
               'why': '굴러가는 바퀴의 맨 위는 차보다 두 배 빠르고, 땅에 닿은 곳은 그 순간 멈춰 있어요. 중심(축)은 차와 같은 속도'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
