"""ROOM 188 proof: the toilet roll. A roll of paper wound on a core of diameter k: the paper's length is proportional
to the area of its end face, pi/4 (D^2 - k^2), because the sheet has a constant thickness. Using the same amount every
day, a roll that shrank from diameter F to c in N days lasts N (c^2 - k^2) / (F^2 - c^2) more days. Digit = days left.
All 10^4 codes compared; exactly one matches. The trap: shrinking the diameter at a steady speed, N (c - k) / (F - c)."""
import itertools, json, os
from fractions import Fraction as Fr

BOARDS = {'A': (4, 12, 8, 5), 'B': (3, 9, 7, 4), 'C': (5, 13, 11, 3), 'D': (4, 10, 8, 3)}  # core k, full F, now c (cm), days used N


def left(k, F, c, N): return Fr(N * (c * c - k * k), F * F - c * c)


def trap_left(k, F, c, N): return Fr(N * (c - k), F - c)


GOOD = {key: left(*v) for key, v in BOARDS.items()}; TRAPV = {key: trap_left(*v) for key, v in BOARDS.items()}
assert all(g.denominator == 1 and 0 < g < 10 for g in GOOD.values()) and all(t.denominator == 1 and 0 < t < 10 for t in TRAPV.values())
code = ''.join(str(GOOD[x]) for x in 'ABCD'); trap = ''.join(str(TRAPV[x]) for x in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[x] != TRAPV[x] for x in 'ABCD')
assert all(k < c < F for k, F, c, N in BOARDS.values())
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards_core_full_now_days': BOARDS,
               'days_left': {x: int(v) for x, v in GOOD.items()}, 'trap_diameter_linear': trap,
               'why': '휴지 길이는 지름이 아니라 휴지 단면의 넓이에 비례해요. 바깥쪽 한 바퀴가 안쪽보다 훨씬 길어요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
