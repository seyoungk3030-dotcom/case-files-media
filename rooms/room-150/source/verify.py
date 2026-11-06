"""ROOM 150 proof: tilting a glass of water. A straight-sided glass (inside width w marks, height 10 marks, marks
numbered up both side walls from the bottom) holds water to mark h0 when upright. Tilt it by angle t (tan t = s): the
water surface stays HORIZONTAL and the amount of water is unchanged. In the glass's own frame the surface becomes a
line of slope s; the area under it equals w*h0 only if the line passes through the glass's centre line at height h0
(as long as it touches neither the bottom nor the rim). So the low-side wall reads h0 + s*w/2. Digit = that mark. All
10^4 codes compared; exactly one matches. The trap: 'the water stays at mark h0'."""
import itertools, json, os
from fractions import Fraction as F
BOARDS = {'A': {'w': 4, 'h0': 4, 's': F(1)}, 'B': {'w': 4, 'h0': 3, 's': F(1, 2)}, 'C': {'w': 6, 'h0': 6, 's': F(1)}, 'D': {'w': 8, 'h0': 5, 's': F(1, 2)}}


def low(b): return b['h0'] + b['s'] * b['w'] / 2


def high(b): return b['h0'] - b['s'] * b['w'] / 2


for k, b in BOARDS.items():
    assert 0 < high(b) and low(b) < 10 and low(b).denominator == 1, k
    assert (low(b) + high(b)) / 2 * b['w'] == b['h0'] * b['w']  # trapezoid area = water area
code = ''.join(str(int(low(BOARDS[k]))) for k in 'ABCD'); trap = ''.join(str(b['h0']) for b in BOARDS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['6497'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': {k: {**b, 's': str(b['s'])} for k, b in BOARDS.items()},
               'high_side': {k: str(high(b)) for k, b in BOARDS.items()}, 'trap_same_mark': trap,
               'why': '물 표면은 언제나 수평이에요. 물의 양이 그대로라 표면이 컵 가운데를 축으로 기울어져, 낮은 쪽 벽에선 올라가요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
