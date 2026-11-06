"""ROOM 142 proof: Connect Four, 7 columns x 6 rows, gravity. Rows are listed from the BOTTOM. X = yellow (you, to
move), O = red. A disc dropped in a column falls to the lowest empty cell. Digit = the one column (1-7) where yellow's
drop makes four in a row (row, column or diagonal) right now; every column is tried and exactly one wins. All 10^4
codes compared; exactly one matches. The trap: a column with a tempting gap HIGHER up - the disc cannot stop there,
it falls to the bottom of the gap."""
import itertools, json, os
R, C = 6, 7
BOARDS = {'A': ['.OXXOXO', '.O.XO.O', '...XX..', '.......', '.......', '.......'],
          'B': ['X..OXX.', 'O..OOX.', '...OX..', '...XO..', '.......', '.......'],
          'C': ['X.XXOOO', 'X.O.XOO', '.....X.', '.......', '.......', '.......'],
          'D': ['O.O.OXX', '....OXX', '....OX.', '....X..', '....O..', '.......']}


def four(g, p):
    return any(all(0 <= r + i * dr < R and 0 <= c + i * dc < C and g[r + i * dr][c + i * dc] == p for i in range(4))
               for r in range(R) for c in range(C) for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)))


def land(g, c): return next((r for r in range(R) if g[r][c] == '.'), None)


def with_(g, r, c, p): h = [list(x) for x in g]; h[r][c] = p; return h


def wins(g, p): return [c + 1 for c in range(C) if land(g, c) is not None and four(with_(g, land(g, c), c, p), p)]


def floating(g, p): return sorted({c + 1 for c in range(C) if land(g, c) is not None for r in range(land(g, c) + 1, R) if four(with_(g, r, c, p), p)} - set(wins(g, p)))


for k, g in BOARDS.items():
    assert not four(g, 'X') and not four(g, 'O') and len(wins(g, 'X')) == 1 and not wins(g, 'O'), k
    assert all(not (g[r][c] != '.' and g[r - 1][c] == '.') for r in range(1, R) for c in range(C)), k  # no floating discs
code = ''.join(str(wins(BOARDS[k], 'X')[0]) for k in 'ABCD'); trap = ''.join(str(floating(BOARDS[k], 'X')[0]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: floating(g, 'X') for k, g in BOARDS.items()})
assert sols == ['4726'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'land_row': {k: land(BOARDS[k], int(code['ABCD'.index(k)]) - 1) for k in 'ABCD'},
               'trap_floating_gap': trap, 'why': '원판은 떨어져서 그 줄 맨 아래 빈칸에 멈춰요. 공중에 뜬 빈칸에는 넣을 수 없어요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
