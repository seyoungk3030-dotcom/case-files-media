"""ROOM 111 proof: the appearing coin. Cut-away side view of a cup: inside from x = 0 (near wall, the eye's side) to
x = W, bottom y = 0, rim y = H. The eye is fixed at (EX, EY) up and to the left. Coins (points on the bottom) are
numbered. Empty cup: a coin is seen if the straight line to the eye clears the near rim corner (0, H). With water up
to y = h (index 1.33) the light from the coin bends at the surface (Snell's law); the coin is seen if the bent path
reaches the eye and clears the rim. Each digit is the number of the one coin that is hidden now but appears after
the water is poured. All 10^4 codes are compared; exactly one matches. The trap: the coin that is already visible."""
import itertools, json, math, os

N_W = 1.33


def seen_dry(eye, H, xc):
    ex, ey = eye; t = (0 - ex) / (xc - ex); y_at0 = ey + t * (0 - ey); return y_at0 >= H


def seen_wet(eye, H, h, W, xc):
    ex, ey = eye
    def snell(s):    # n_w sin(theta_w) - sin(theta_a) where angles from the vertical
        dw = math.atan2(s - xc, h); da = math.atan2(ex - s, ey - h); return N_W * math.sin(dw) - math.sin(da)
    lo, hi = min(xc, ex) - 5, max(xc, ex) + 5
    a, b = ex, xc            # the surface point lies between the eye's x and the coin's x
    if snell(a) * snell(b) > 0: return False, None
    for _ in range(200):
        m = (a + b) / 2
        if snell(a) * snell(m) <= 0: b = m
        else: a = m
    s = (a + b) / 2
    if not (0 <= s <= W): return False, s
    t = (0 - s) / (ex - s); y_at0 = h + t * (ey - h)       # air segment must clear the rim at x = 0
    return y_at0 >= H, s


# eye, cup (W, H), water level h, coins: number -> x
BOARDS = {'A': {'eye': (-2.2, 4.8), 'W': 3.4, 'H': 2.4, 'h': 2.2, 'coins': {1: 1.8, 2: 0.4, 3: 2.9, 4: 1.15}},
          'B': {'eye': (-2.0, 3.6), 'W': 3.4, 'H': 2.0, 'h': 1.8, 'coins': {1: 3.2, 2: 0.4, 3: 1.95, 4: 1.15}},
          'C': {'eye': (-2.4, 5.0), 'W': 3.4, 'H': 2.6, 'h': 2.4, 'coins': {1: 3.15, 2: 1.35, 3: 0.4, 4: 2.1}},
          'D': {'eye': (-1.8, 4.0), 'W': 3.4, 'H': 2.2, 'h': 2.0, 'coins': {1: 1.1, 2: 1.8, 3: 0.4, 4: 3.0}}}


def solve(k):
    b = BOARDS[k]; out = {}
    for n, xc in b['coins'].items():
        d = seen_dry(b['eye'], b['H'], xc); w, s = seen_wet(b['eye'], b['H'], b['h'], b['W'], xc); out[n] = (d, w, s)
    new = [n for n, v in out.items() if v[1] and not v[0]]; old = [n for n, v in out.items() if v[0]]
    return new, old, out


def margins(b, xc):
    ex, ey = b['eye']; dry = ey + (0 - ex) / (xc - ex) * (0 - ey) - b['H']
    w, s = seen_wet(ex and b['eye'], b['H'], b['h'], b['W'], xc)
    wet = (b['h'] + (0 - s) / (ex - s) * (ey - b['h']) - b['H']) if s is not None and 0 <= s <= b['W'] else -9
    return dry, wet


RES = {k: solve(k) for k in 'ABCD'}
for k, b in BOARDS.items():      # clear margins so the picture is never borderline (0.15 = a coin's width)
    for n, xc in b['coins'].items():
        dry, wet = margins(b, xc); assert abs(dry) >= 0.15 and abs(wet) >= 0.12, (k, n, dry, wet)
assert all(len(v[0]) == 1 and len(v[1]) == 1 for v in RES.values())
code = ''.join(str(RES[k][0][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1][0]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['1342'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS,
               'seen': {k: {n: {'dry': d, 'wet': w, 'surface_x': s} for n, (d, w, s) in v[2].items()} for k, v in RES.items()},
               'trap_already_visible': trap, 'why': '물에서 나온 빛은 수면에서 꺾여 더 낮게 퍼져요. 그래서 컵 벽에 숨어 있던 동전이 떠올라 보여요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
