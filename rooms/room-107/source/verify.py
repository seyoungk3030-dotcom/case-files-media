"""ROOM 107 proof: moon phases. Top view of Earth with eight numbered moon spots around it (counter-clockwise, seen
from above the north pole) and the sun far away in a given direction. A person on Earth faces the moon with their
head toward the north (+z). The moon's lit fraction is (1 + cos g) / 2 where g is the angle at the moon between the
sun and Earth, and the lit part sits on the person's right when the sun is on their right. Each board shows the moon
'as seen from Earth' (rendered from that spot); its digit is the number of the spot that looks like that. All eight
spots look different, so one spot matches; all 10^4 codes are compared and exactly one matches. The trap: the
mirror-image spot (same shape, lit on the other side) gives another code."""
import itertools, json, math, os

R_ORB = 1.0


def spot(i, start): a = math.radians(start + 45 * (i - 1)); return (math.cos(a), math.sin(a))


def look(i, start, sun):
    mx, my = spot(i, start); s = (math.cos(math.radians(sun)), math.sin(math.radians(sun)))
    f = (mx, my); right = (f[1], -f[0])                      # facing f with head +z: right = f x z
    to_earth = (-mx, -my); cos_g = s[0] * to_earth[0] + s[1] * to_earth[1]
    frac = round((1 + cos_g) / 2, 6); side = s[0] * right[0] + s[1] * right[1]
    return frac, (0 if abs(side) < 1e-9 else (1 if side > 0 else -1))   # +1: lit on the right


# board: sun direction (degrees, from Earth), angle of spot 1, target spot (the picture shown)
BOARDS = {'A': {'sun': 180, 'start': 90, 'target': 4}, 'B': {'sun': 90, 'start': 0, 'target': 6},
          'C': {'sun': 0, 'start': 225, 'target': 2}, 'D': {'sun': 270, 'start': 135, 'target': 5}}


def solve(k):
    b = BOARDS[k]; looks = {i: look(i, b['start'], b['sun']) for i in range(1, 9)}
    assert len(set(looks.values())) == 8
    t = looks[b['target']]; assert 0.1 < t[0] < 0.9, (k, t)       # never a full or new moon
    match = [i for i, v in looks.items() if v == t]; mirror = [i for i, v in looks.items() if v == (t[0], -t[1])]
    return match, mirror, looks


RES = {k: solve(k) for k in 'ABCD'}
assert all(len(v[0]) == 1 and len(v[1]) == 1 for v in RES.values())
code = ''.join(str(RES[k][0][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1][0]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: RES[k][2][BOARDS[k]['target']] for k in 'ABCD'})
assert sols == [code] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'looks': {k: RES[k][2] for k in 'ABCD'}, 'trap_mirror_spot': trap,
               'why': '달은 늘 해 쪽 절반이 밝아요. 지구에서 달을 볼 때 해가 오른쪽에 있으면 오른쪽이 밝게 보여요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
