"""ROOM 134 proof: a ball runs round a circular track (radius R) and leaves it through a gap. Once nothing pushes it
sideways it goes in a straight line along the TANGENT at the exit point (Newton's first law). Four numbered pins
stand at the same distance from the exit point: along the tangent, 28 degrees curved inward (as if it kept turning),
35 degrees outward, and straight outward (radial, the 'thrown out' idea). Digit = the number on the pin in the
tangent direction. All 10^4 codes are compared; exactly one matches. The trap: the radial pin."""
import itertools, json, math, os

R, D = 1.4, 2.0
OFFS = {'tangent': 0, 'inward': 28, 'outward': -35, 'radial': -90}
BOARDS = {'A': {'exit': 90, 'dir': 1, 'pins': {'tangent': 6, 'inward': 2, 'outward': 9, 'radial': 4}},
          'B': {'exit': 0, 'dir': -1, 'pins': {'tangent': 1, 'inward': 8, 'outward': 3, 'radial': 7}},
          'C': {'exit': 225, 'dir': 1, 'pins': {'tangent': 8, 'inward': 5, 'outward': 0, 'radial': 2}},
          'D': {'exit': 135, 'dir': -1, 'pins': {'tangent': 4, 'inward': 9, 'outward': 6, 'radial': 1}}}


def pins(b):
    """Pin positions: rotate the tangent by the offset, toward the centre for positive offsets."""
    a = math.radians(b['exit']); p = (R * math.cos(a), R * math.sin(a)); s = b['dir']
    t = math.atan2(s * math.cos(a), -s * math.sin(a)); out = {}
    for kind, off in OFFS.items():
        ang = t + s * math.radians(off); out[kind] = (p[0] + D * math.cos(ang), p[1] + D * math.sin(ang))
    return p, out


def solve(b): return b['pins']['tangent'], b['pins']['radial']


RES = {k: solve(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if all(int(c[i]) == BOARDS[k]['pins']['tangent'] for i, k in enumerate('ABCD'))]
for k, b in BOARDS.items():
    p, q = pins(b); a = math.radians(b['exit'])
    rad = (q['radial'][0] - p[0], q['radial'][1] - p[1]); assert abs(rad[0] * math.sin(a) - rad[1] * math.cos(a)) < 1e-9 and rad[0] * math.cos(a) + rad[1] * math.sin(a) > 0
    assert len(set(b['pins'].values())) == 4
print('answer', code, 'trap', trap)
assert sols == ['6184'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'trap_radial': trap,
               'why': '틈으로 나간 공은 더 이상 휘게 하는 벽이 없어서, 나간 순간의 방향(접선)으로 곧게 굴러가요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
