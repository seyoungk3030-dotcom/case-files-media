"""ROOM 123 proof: coloured shadows. Three lamps - red, green, blue - stand in a row (x = -1.6, 0, 1.6) at the same
distance in front of a thin post (x = xo); a white wall stands twice as far from the lamps. Each lamp throws one
shadow of the post on the wall, at x = 2*xo - lamp_x (similar triangles: the shadow is on the far side of the post
from its lamp). Inside a lamp's shadow only the OTHER two lamps shine, so the red lamp's shadow looks cyan (green +
blue), the green lamp's looks magenta, the blue lamp's looks yellow. Nine numbered strips on the wall; each board
asks for one shadow colour; its strip is the digit. All 10^4 codes are compared; exactly one matches. The trap: the
shadow put on the SAME side as its lamp (x = 2*xo + lamp_x)."""
import itertools, json, os

XS, W, X0 = [-1.6, 0.0, 1.6], 0.8, -3.6
COLOR = {'R': '청록', 'G': '자홍', 'B': '노랑'}
BOARDS = {'A': {'order': 'RBG', 'xo': 0.4, 'ask': 'R'}, 'B': {'order': 'BGR', 'xo': -0.8, 'ask': 'B'},
          'C': {'order': 'BRG', 'xo': -0.8, 'ask': 'G'}, 'D': {'order': 'GRB', 'xo': 0.0, 'ask': 'G'}}


def strip(x):
    u = (x - X0) / W; n = int(u // 1) + 1; return n, u - (n - 1)


def solve(b):
    lx = XS[b['order'].index(b['ask'])]; assert lx != 0
    n, f = strip(2 * b['xo'] - lx); t, _ = strip(2 * b['xo'] + lx)
    others = [strip(2 * b['xo'] - x) for x in XS]
    assert all(1 <= m <= 9 and 0.3 < g < 0.7 for m, g in others) and len({m for m, _ in others}) == 3
    return n, t


RES = {k: solve(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['8517'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'asked_colour': {k: COLOR[b['ask']] for k, b in BOARDS.items()},
               'trap_same_side': trap, 'why': '빨강 램프의 그림자엔 초록+파랑만 비쳐서 청록, 초록 그림자는 자홍, 파랑 그림자는 노랑이에요. 그림자는 램프 반대편에 생겨요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
