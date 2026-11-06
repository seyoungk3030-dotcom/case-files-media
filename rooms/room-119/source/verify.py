"""ROOM 119 proof: cut the pendulum string. A ball on a string (length L, pivot height P) swings between +-T0 (the
dashed arc). At the moment shown (angle T, moving in the arrow's direction) the string is cut. From then on the
ball flies like a thrown ball: it leaves along the circle's tangent with speed v = sqrt(2 g L (cos T - cos T0))
(energy), then falls under gravity. Nine numbered slots on the floor; the landing slot is the digit. Every landing
is kept well inside its slot (25-75 % of its width). All 10^4 codes are compared; exactly one matches. The trap:
'it drops straight down' (the slot right under the cut point)."""
import itertools, json, math, os

P, L, G, W, X0, R = 4.2, 2.4, 9.8, 0.55, -2.475, 0.15
BOARDS = {'A': {'T0': 50, 'T': -10, 'dir': 1}, 'B': {'T0': 60, 'T': -30, 'dir': 1},
          'C': {'T0': 30, 'T': 15, 'dir': -1}, 'D': {'T0': 50, 'T': -45, 'dir': 1}}


def flight(b, n=40):
    t0, t = math.radians(b['T0']), math.radians(b['T'])
    v = math.sqrt(2 * G * L * (math.cos(t) - math.cos(t0)))
    x, z = L * math.sin(t), P - L * math.cos(t); vx, vz = b['dir'] * v * math.cos(t), b['dir'] * v * math.sin(t)
    T = (vz + math.sqrt(vz * vz + 2 * G * (z - R))) / G
    return [(x + vx * T * i / n, z + vz * T * i / n - G * (T * i / n) ** 2 / 2) for i in range(n + 1)]


def slot(x):
    u = (x - X0) / W; return math.floor(u) + 1, u - math.floor(u)


RES = {}
for k, b in BOARDS.items():
    path = flight(b); n, f = slot(path[-1][0]); m, f2 = slot(path[0][0])
    assert 1 <= n <= 9 and 0.25 < f < 0.75 and 0.2 < f2 < 0.8 and n != m and abs(b['T']) < b['T0']
    RES[k] = (n, m)
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['8643'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'landing_slot': {k: v[0] for k, v in RES.items()},
               'trap_straight_down': trap, 'why': '끊는 순간 공은 원의 접선 방향으로 날아가요. 그 속도로 포물선을 그리며 떨어져요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
