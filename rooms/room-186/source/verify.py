"""ROOM 186 proof (블록 걸치기 2, sequel to ROOM 090 by the user's choice 2026-11-16): blocks of equal size stacked off
the edge of a table, but the dark iron block weighs as much as 3 wooden blocks. Block width = 4 grid squares; c = block
centre in grid squares, the table edge is x = 0 (table under x < 0). A stack is safe at a level when the weighted centre
of mass of all blocks above that level lies over the block (or table) below it. The lowest level that fails tips, and
every block from there up falls. Each digit is how many blocks fall. Ties are avoided, also for the trap. All 10^4 codes
compared; exactly one matches. The trap: ROOM 090's rule with every block weighing the same."""
import itertools, json, os
from fractions import Fraction as F
W, HEAVY = 4, 3
BOARDS = {'A': ([1, 1, 0, -1], 3), 'B': ([-1, -1, 0, 1], 3), 'C': ([-1, 0, -2, 1, 4], 2), 'D': ([-1, -2, 1, 0, 3], 0)}  # centres bottom-up, iron index


def falls(c, w):
    n = len(c)
    for j in range(n):
        com = F(sum(a * b for a, b in zip(c[j:], w[j:])), sum(w[j:])); lo, hi = (None, F(0)) if j == 0 else (F(c[j - 1] - W // 2), F(c[j - 1] + W // 2))
        assert com != hi and com != lo, 'tie'
        assert lo is None or com >= lo, 'tips back onto the table'
        if com > hi: return n - j, j
    return 0, None


def weights(k): c, h = BOARDS[k]; return [HEAVY if i == h else 1 for i in range(len(c))]


for c, h in BOARDS.values():
    assert c[0] - W // 2 < 0 and all(abs(a - b) < W for a, b in zip(c, c[1:]))  # every block rests on the one below
RES = {k: falls(BOARDS[k][0], weights(k)) for k in 'ABCD'}; TR = {k: falls(BOARDS[k][0], [1] * len(BOARDS[k][0])) for k in 'ABCD'}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(TR[k][0]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, RES)
assert len(sols) == 1 and all(RES[k][0] != TR[k][0] for k in 'ABCD')
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'block_centres_bottom_up': {k: v[0] for k, v in BOARDS.items()},
               'iron_block_index': {k: v[1] for k, v in BOARDS.items()}, 'iron_weight': HEAVY, 'block_width': W,
               'falls_from_level': {k: RES[k][1] for k in 'ABCD'}, 'trap_equal_weights': trap,
               'why': '쇠 블록은 나무 블록 3개 무게라서 무게중심을 자기 쪽으로 끌어당겨요. 위 묶음의 무게중심이 받침 밖이면 그 층부터 떨어져요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
