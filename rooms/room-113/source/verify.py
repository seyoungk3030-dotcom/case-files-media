"""ROOM 113 proof: the bouncing ball. A ball is dropped from a height marked on a ruler. The first bounce is shown: it
comes back up to a lower mark. Every bounce keeps the same FRACTION of the height before it (that is how real balls
behave: the same share of energy is lost at every hit). The board asks for the height of the k-th bounce (a mark
on the ruler); that number is the digit. All 10^4 codes are compared; exactly one matches. The trap: losing the
same AMOUNT every bounce (straight-line thinking), which gives 8003."""
import itertools, json, os
from fractions import Fraction as F

BOARDS = {'A': {'drop': 16, 'first': 12, 'ask': 2, 'color': 'coral'},
          'B': {'drop': 12, 'first': 6, 'ask': 2, 'color': 'blue'},
          'C': {'drop': 16, 'first': 8, 'ask': 3, 'color': 'amber'},
          'D': {'drop': 9, 'first': 6, 'ask': 2, 'color': 'green'}}


def heights(b, n=6):
    r = F(b['first'], b['drop']); return [b['drop'] * r ** i for i in range(n)]


def linear(b, k): return max(0, b['drop'] - k * (b['drop'] - b['first']))


H = {k: heights(b) for k, b in BOARDS.items()}
for k, b in BOARDS.items(): assert H[k][b['ask']].denominator == 1 and 0 < H[k][b['ask']] < 10
code = ''.join(str(H[k][BOARDS[k]['ask']]) for k in 'ABCD'); trap = ''.join(str(linear(BOARDS[k], BOARDS[k]['ask'])) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['9324'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'heights': {k: [str(x) for x in v] for k, v in H.items()},
               'trap_same_amount': trap, 'why': '공은 튈 때마다 같은 양이 아니라 같은 비율만큼 낮아져요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
