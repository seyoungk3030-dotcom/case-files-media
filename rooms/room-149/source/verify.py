"""ROOM 149 proof: a street lamp's shadow. A small bulb sits at height H on a pole standing at ground mark 0. A stick of
height h stands at mark d. Light leaves the bulb in straight lines, so the line from the bulb over the stick's top
meets the ground at x = d * H / (H - h) (similar triangles). Digit = the ground mark where the tip of the stick's
shadow falls. All 10^4 codes compared; exactly one matches. The trap: 'the shadow is as long as the stick' (d + h)."""
import itertools, json, os
from fractions import Fraction as F
BOARDS = {'A': {'H': 6, 'h': 2, 'd': 2}, 'B': {'H': 6, 'h': 3, 'd': 4}, 'C': {'H': 8, 'h': 2, 'd': 3}, 'D': {'H': 4, 'h': 2, 'd': 3}}


def tip(b): x = F(b['d'] * b['H'], b['H'] - b['h']); assert x.denominator == 1 and x <= 9; return int(x)


code = ''.join(str(tip(BOARDS[k])) for k in 'ABCD'); trap = ''.join(str(b['d'] + b['h']) for b in BOARDS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['3846'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'trap_shadow_equals_height': trap,
               'why': '전구에서 막대 끝을 지나는 직선이 땅에 닿는 곳이 그림자 끝이에요. 막대가 전구 높이에 가까울수록 그림자가 길어져요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
