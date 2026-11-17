"""ROOM 177 proof (replaces the old 밀물과 사다리, which repeated ROOM 109's mechanic): a carpet runner glued to a
staircase covers every riser (the vertical faces) and every tread (the flat tops). Laid flat it is exactly the sum of
all rises and all treads, so for stairs that only go up its length is total height + total depth, however many steps
there are and however uneven they are. Digit = carpet length in metres. All 10^4
codes compared; exactly one matches. The trap: the straight slope, sqrt(H^2 + D^2), rounded."""
import itertools, json, math, os
from fractions import Fraction as Fr

# profile from the bottom-left: (vertical change, horizontal run) per step, in metres
BOARDS = {'A': [(Fr(1, 2), Fr(1, 2))] * 2,
          'B': [(Fr(1, 5), Fr(1)), (Fr(1, 2), Fr(1)), (Fr(3, 10), Fr(1))],
          'C': [(Fr(1, 10), Fr(1, 2)), (Fr(2, 5), Fr(1, 4)), (Fr(1, 5), Fr(1)), (Fr(3, 10), Fr(1, 4))],
          'D': [(Fr(1, 8), Fr(1, 8))] * 8}


def carpet(p): return sum(abs(r) + t for r, t in p)


def box(p):
    z = 0; zs = [0]
    for r, t in p: z += r; zs.append(z)
    return max(zs), sum(t for _, t in p)


GOOD = {k: carpet(v) for k, v in BOARDS.items()}
assert all(g.denominator == 1 for g in GOOD.values())
TRAPV = {k: round(math.hypot(*map(float, box(v)))) for k, v in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[k] != TRAPV[k] for k in 'ABCD') and code == '2432'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000,
               'boards_rise_run_m': {k: [[str(r), str(t)] for r, t in v] for k, v in BOARDS.items()},
               'height_depth_m': {k: [str(x) for x in box(v)] for k, v in BOARDS.items()},
               'carpet_m': {k: int(v) for k, v in GOOD.items()}, 'trap_straight_slope': trap,
               'why': '카펫은 계단의 세로면과 윗면을 모두 덮어요. 펼치면 높이를 다 더한 것과 깊이를 다 더한 것의 합이에요. 계단 수는 상관없어요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
