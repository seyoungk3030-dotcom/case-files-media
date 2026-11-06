"""ROOM 122 proof: compass beside a bar magnet. Top view. One bar magnet (red N half, blue S half) lies on the table
at the centre, turned to the board's angle; a compass sits at the marked spot. The compass needle's red tip points
ALONG the magnet's field there: out of N, round, into S. The field is computed from two poles (+ at the N end,
- at the S end, inverse-square). The 8 directions are numbered 1 (up) to 8 clockwise; each needle is within 6
degrees of its direction. Digit = the direction number. All 10^4 codes are compared; exactly one matches. The
trap: the opposite direction (thinking the red N tip is pulled toward the magnet's N)."""
import itertools, json, math, os

H = 0.9
BOARDS = {'A': {'angle': -45, 'compass': [-1.6, -1.6]}, 'B': {'angle': -135, 'compass': [1.6, -1.6]},
          'C': {'angle': 180, 'compass': [-2.2, 0.0]}, 'D': {'angle': -90, 'compass': [0.0, -2.2]}}


def field(b):
    a = math.radians(b['angle']); dx, dy = math.cos(a) * H, math.sin(a) * H; px, py = b['compass']; bx = by = 0.0
    for q, (x, y) in ((1, (dx, dy)), (-1, (-dx, -dy))):
        rx, ry = px - x, py - y; r = math.hypot(rx, ry); bx += q * rx / r ** 3; by += q * ry / r ** 3
    return bx, by


def dirnum(bx, by):
    deg = (90 - math.degrees(math.atan2(by, bx))) % 360; k = round(deg / 45) % 8
    off = abs(((deg - 45 * k) + 180) % 360 - 180); return k + 1, off


RES = {k: dirnum(*field(b)) for k, b in BOARDS.items()}
assert all(off < 6 for _, off in RES.values())
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str((RES[k][0] + 3) % 8 + 1) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['8275'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'needle_dir': {k: v[0] for k, v in RES.items()},
               'trap_opposite': trap, 'why': '나침반의 빨간 N은 자석의 S 쪽으로 끌려요. 자석 옆에서는 자석과 반대 방향, 끝에서는 같은 방향을 가리켜요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
