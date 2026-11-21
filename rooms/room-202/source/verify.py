"""ROOM 202 proof (몇 초 만에 땅에?): a ball leaves a rooftop of height h, either just let go or thrown straight sideways
at u m/s; it may be a heavy or a light ball (no air resistance, g = 10 m/s^2). The time to the ground comes only from the
fall: h = 5 t^2, so t = sqrt(h / 5); the sideways speed and the weight change nothing. The flight is also simulated in small
steps for x and z to check it. Digit = seconds. All 10^4 codes compared, exactly one matches. Trap: time growing with the
height itself (4 times higher = 4 times longer) -> 9164."""
import itertools, json, math, os

G = 10
# key: (height m, sideways speed m/s, ball)
BOARDS = {'A': (45, 15, '야구공'), 'B': (5, 0, '볼링공'), 'C': (80, 0, '탁구공'), 'D': (20, 10, '테니스공')}


def t_exact(h):
    t = math.isqrt(2 * h // G); assert G * t * t == 2 * h; return t


def t_sim(h, u, dt=1e-4):
    x = z = 0.0; vz = 0.0; t = 0.0
    while z < h: vz += G * dt; z += vz * dt; x += u * dt; t += dt
    return t


GOOD = {}
for k, (h, u, _) in BOARDS.items():
    t = t_exact(h); assert abs(t_sim(h, u) - t) < 0.01 and abs(t_sim(h, 0) - t_sim(h, u)) < 1e-9; GOOD[k] = t
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str((h // 5) % 10) for h, _, _ in (BOARDS[k] for k in 'ABCD'))
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and code != trap
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'g': G, 'boards': BOARDS, 'seconds': GOOD, 'trap_linear_height': trap,
               'landing_x': {k: BOARDS[k][1] * GOOD[k] for k in BOARDS},
               'why': '떨어지는 시간은 높이로만 정해져요. 옆으로 던져도, 무거워도 같아요. 높이 4배면 시간은 2배'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
