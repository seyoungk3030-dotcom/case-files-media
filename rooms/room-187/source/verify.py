"""ROOM 187 proof: the full-length mirror. To see yourself from the top of your head to your feet in a flat wall
mirror, light from your head and from your feet must bounce off the mirror into your eye. By the law of reflection
the bounce point lies halfway (in height) between the eye and the point seen, so the head bounces at (eye+h)/2 and
the feet at eye/2: the mirror must be exactly h/2 tall, wherever your eyes are and however far away you stand.
Digit = minimum mirror tiles (1 tile = 20 cm, placed at any height) = (h/2)/20. All 10^4 codes compared; exactly one
matches. The trap: a mirror as tall as you (h/20 tiles), or thinking distance changes it."""
import itertools, json, math, os

TILE = 20
BOARDS = {'A': (80, 1.0), 'B': (160, 2.0), 'C': (120, 0.6), 'D': (160, 0.5)}  # height cm, distance to the wall m


def eye(h): return h * 0.93


def bounce(eye_z, d, z):
    """Point on the wall (x=0) where light from height z at x=-d reaches an eye at height eye_z at x=-d (law of
    reflection: mirror the eye behind the wall, intersect the straight line)."""
    t = d / (d + d); return z + (eye_z - z) * t


def need(h, d):
    e = eye(h); top, bot = bounce(e, d, h), bounce(e, d, 0); return top - bot, bot, top


GOOD = {}
for k, (h, d) in BOARDS.items():
    L, bot, top = need(h, d)
    assert abs(L - h / 2) < 1e-9
    for dd in (0.3, 1, 5, 50): assert abs(need(h, dd)[0] - L) < 1e-9  # distance never matters
    GOOD[k] = math.ceil(L / TILE - 1e-9)
TRAPV = {k: math.ceil(h / TILE) for k, (h, d) in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[k] != TRAPV[k] for k in 'ABCD') and all(0 < g < 10 for g in GOOD.values())
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'tile_cm': TILE,
               'boards': {k: {'height_cm': h, 'distance_m': d, 'mirror_cm': [round(need(h, d)[1], 1), round(need(h, d)[2], 1)]} for k, (h, d) in BOARDS.items()},
               'tiles': GOOD, 'trap_full_height': trap,
               'why': '머리와 발에서 온 빛은 눈 높이와의 딱 중간에서 반사돼요. 그래서 거울은 키의 절반이면 되고, 거리는 상관없어요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
