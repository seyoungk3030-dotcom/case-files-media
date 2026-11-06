"""ROOM 115 proof: connected tanks. Square tanks of different widths (footprint w x w... here the front width w, all
the same depth) stand side by side, joined at the bottom by one pipe with closed valves. Each holds water up to a
mark on the ruler. Open the valves: water flows until every tank has the same level (communicating vessels). The
amount of water is kept, so the common level L solves sum(w_i * (h_i - L)) = 0, i.e. L = sum(w_i h_i) / sum(w_i).
Digit = L. All 10^4 codes are compared; exactly one matches. The trap: the plain average of the heights (ignoring
that a wide tank holds more water per mark)."""
import itertools, json, os
from fractions import Fraction as F

BOARDS = {'A': {'w': [2, 1], 'h': [0, 6]},
          'B': {'w': [1, 2], 'h': [2, 8]},
          'C': {'w': [2, 1, 3], 'h': [8, 2, 8]},
          'D': {'w': [1, 3, 2], 'h': [7, 1, 4]}}


def level(b): return F(sum(w * h for w, h in zip(b['w'], b['h'])), sum(b['w']))


LV = {k: level(b) for k, b in BOARDS.items()}
assert all(v.denominator == 1 for v in LV.values())
code = ''.join(str(LV[k]) for k in 'ABCD'); trap = ''.join(str(F(sum(BOARDS[k]['h']), len(BOARDS[k]['h']))) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['2673'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'level': {k: str(v) for k, v in LV.items()},
               'trap_plain_average': trap, 'why': '물의 양은 그대로라서 넓은 통일수록 수위에 더 큰 영향을 줘요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
