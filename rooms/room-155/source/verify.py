"""ROOM 155 proof: a champagne tower of 10 glasses (rows of 1, 2, 3, 4). Champagne is poured into the top glass; a glass
holds exactly one glass-worth, and whatever overflows is split half and half into the two glasses right under it (the
bottom row spills onto the table). The bottle label says how many glass-worths are poured. Simulated exactly with
fractions. Digit = how many glasses end up completely full. All 10^4 codes compared; exactly one matches. The trap:
assuming the tower fills glass by glass, row by row (as many full glasses as glass-worths poured)."""
import itertools, json, os
from fractions import Fraction as F
ROWS = 4
BOARDS = {'A': 8, 'B': 4, 'C': 9, 'D': 6}


def pour(n):
    a = [[F(0)] * (r + 1) for r in range(ROWS)]; a[0][0] = F(n)
    for r in range(ROWS):
        for c in range(r + 1):
            if a[r][c] > 1:
                ex = a[r][c] - 1; a[r][c] = F(1)
                if r + 1 < ROWS: a[r + 1][c] += ex / 2; a[r + 1][c + 1] += ex / 2
    return a


LEVEL = {k: pour(n) for k, n in BOARDS.items()}
code = ''.join(str(sum(x == 1 for row in LEVEL[k] for x in row)) for k in 'ABCD')
trap = ''.join(str(min(n, 10)) for n in BOARDS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['6384'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'poured': BOARDS,
               'levels': {k: [[str(x) for x in row] for row in v] for k, v in LEVEL.items()}, 'trap_row_by_row': trap,
               'why': '가운데 잔은 위에서 두 잔이 넘겨 주고, 가장자리 잔은 한 잔만 넘겨 줘요. 그래서 가운데가 먼저 차고 가장자리는 덜 차요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
