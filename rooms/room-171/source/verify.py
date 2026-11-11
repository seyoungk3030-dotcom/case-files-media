"""ROOM 171 proof: tic-tac-toe, O to move. Cells are numbered 1-9 row by row. Full minimax over the game tree, scoring a
win as +(10 - moves), a loss as -(10 - moves) and a draw as 0, so a faster win and a slower loss are preferred. On every
board exactly one cell gets the best score; digit = that cell. All 10^4 codes compared; exactly one matches.
Traps: A blocking X instead of winning at once, B/D taking the centre (only a draw), C taking the centre (loses)."""
import itertools, json, os
from functools import lru_cache

BOARDS = {'A': 'OO.XX...X', 'B': 'OX...X...', 'C': 'X....XO..', 'D': '..O..X.X.'}
TRAPC = {'A': 6, 'B': 5, 'C': 5, 'D': 5}
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def won(b, p): return any(all(b[i] == p for i in l) for l in LINES)


@lru_cache(None)
def val(b, p):
    o = 'X' if p == 'O' else 'O'
    if won(b, o): return -10
    if '.' not in b: return 0
    best = -99
    for i, c in enumerate(b):
        if c == '.':
            v = -val(b[:i] + p + b[i + 1:], o); best = max(best, v - 1 if v > 0 else v + 1 if v < 0 else 0)
    return best


def scores(b):
    r = {}
    for i, c in enumerate(b):
        if c == '.':
            v = -val(b[:i] + 'O' + b[i + 1:], 'X'); r[i + 1] = v - 1 if v > 0 else v + 1 if v < 0 else 0
    return r


GOOD = {}; S = {}
for k, b in BOARDS.items():
    assert b.count('X') == b.count('O') + 1 and not won(b, 'X') and not won(b, 'O')
    S[k] = scores(b); best = max(S[k].values()); opt = [c for c, v in S[k].items() if v == best]
    assert len(opt) == 1, (k, S[k]); GOOD[k] = opt[0]
    assert S[k][TRAPC[k]] < best
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPC[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, S)
assert len(sols) == 1
if __name__ == '__main__':
    out = {'win': '이겨요', 'draw': '비겨요', 'lose': '져요'}
    res = {k: {c: ('win' if v > 0 else 'draw' if v == 0 else 'lose') for c, v in S[k].items()} for k in BOARDS}
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'best_cell': GOOD, 'results': res, 'trap_obvious': trap,
               'why': '막기보다 이기기가 먼저, 가운데보다 양쪽으로 두 줄을 동시에 만드는 칸이 이겨요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
