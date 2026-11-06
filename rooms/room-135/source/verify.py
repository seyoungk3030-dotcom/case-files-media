"""ROOM 135 proof: the 'uphill' double cone. Two straight rails rise from a low end (x = 0) to a high end (x = X) and
their half-gap s(x) changes linearly. A solid of revolution (radius profile r(y) along its axis) rests on both rails
at |y| = s(x), so its axis (= its centre of mass) sits at height h(x) + r(s(x)). Released in the middle it rolls to
whichever end puts its centre of mass LOWER (the height is linear in x here, so it runs all the way). Digit = the
number at that end. All 10^4 codes are compared; exactly one matches. The trap: 'everything rolls downhill' (the low
end's number)."""
import itertools, json, os

X, SLOPE, HALF = 4.0, 0.06, 1.25
SHAPES = {'double_cone': lambda y: 0.7 - 0.6 * abs(y) / HALF, 'cylinder': lambda y: 0.42, 'hourglass': lambda y: 0.18 + 0.4 * abs(y) / HALF}
BOARDS = {'A': {'shape': 'double_cone', 's': [0.25, 1.15], 'low': 3, 'high': 8},
          'B': {'shape': 'cylinder', 's': [0.25, 1.15], 'low': 1, 'high': 6},
          'C': {'shape': 'hourglass', 's': [0.25, 1.15], 'low': 9, 'high': 2},
          'D': {'shape': 'double_cone', 's': [1.15, 0.25], 'low': 7, 'high': 4}}


def axis(b, x):
    s = b['s'][0] + (b['s'][1] - b['s'][0]) * x / X; assert 0 < s < HALF
    return SLOPE * x + SHAPES[b['shape']](s)


def solve(b):
    lo, hi = axis(b, 0), axis(b, X); assert abs(lo - hi) > 0.12
    return (b['high'] if hi < lo else b['low']), b['low'], round(lo, 3), round(hi, 3)


RES = {k: solve(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if all(int(c[i]) == solve(BOARDS[k])[0] for i, k in enumerate('ABCD'))]
print('answer', code, 'trap', trap, {k: v[2:] for k, v in RES.items()})
assert sols == [code] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'axis_height_low_high': {k: v[2:] for k, v in RES.items()},
               'trap_always_downhill': trap, 'why': '굴러가는 물체는 무게중심이 낮아지는 쪽으로 가요. 레일이 벌어지면 쌍뿔은 레일 사이로 쑥 내려앉아요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
