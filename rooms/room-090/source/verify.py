"""ROOM 090 proof: equal blocks stacked off the edge of a table. Block width = 4 grid squares; c = block centre in
grid squares, the table edge is x = 0 (table under x < 0). A stack is safe at a level when the centre of mass of all
blocks above that level lies over the block (or table) below it. The lowest level that fails tips, and every block
from there up falls. Each digit is how many blocks fall. Ties (centre exactly on an edge) are avoided. All 10^4 codes
compared; exactly one matches. Counting the blocks that stick out past the table edge (the trap) gives another code."""
import itertools, json, os
from fractions import Fraction as F
W = 4
BOARDS = {'A': [-3, -2, 1, 0], 'B': [0, -2, 1, -1, -1, 0], 'C': [-2, -1, 1, 2, 3], 'D': [-2, -1, -1, 0, -2, 0, 1]}


def falls(c):
    n = len(c)
    for j in range(n):
        com = F(sum(c[j:]), n - j); lo, hi = (None, F(0)) if j == 0 else (F(c[j - 1] - W // 2), F(c[j - 1] + W // 2))
        assert com != hi and com != lo, 'tie'
        if com > hi or (lo is not None and com < lo): return n - j, j
    return 0, None


RES = {k: falls(v) for k, v in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(sum(x + W // 2 > 0 for x in BOARDS[k])) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, RES)
assert sols == ['3052'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'block_centres_bottom_up': BOARDS, 'block_width': W,
               'falls_from_level': {k: RES[k][1] for k in 'ABCD'}, 'trap_blocks_past_edge': trap,
               'why': '어떤 층이든 그 위 블록 전체의 무게중심이 아래 받침 위에 있어야 버텨요. 가장 먼저 무너지는 층부터 위는 전부 떨어져요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
