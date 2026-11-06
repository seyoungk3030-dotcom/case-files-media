"""ROOM 143 proof: Othello / Reversi on a 6x6 board. X = black (you), O = white, * = the empty square where black is
placed. Every white run that lies in a straight line (row, column OR diagonal) between the new black disc and another
black disc, with no gap, flips to black. Digit = how many white discs flip. All 10^4 codes compared; exactly one
matches. The trap: forgetting the diagonals (counting only rows and columns)."""
import itertools, json, os
N = 6
D8 = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if (dr, dc) != (0, 0)]
BOARDS = {'A': ['.OOO.X', 'O*OXO.', 'OOO.O.', 'XO.O.X', 'XXOOOO', '.OOX.X'],
          'B': ['XXO*.O', 'XOO.OX', 'OX..XX', '..O..O', 'XOOXO.', '.OX...'],
          'C': ['OO.OXX', 'XXX.X.', 'OOOOO.', '..O.O.', 'O..OOO', 'XOOO*X'],
          'D': ['OXXO*.', '.OXOOO', '.XOOXO', 'OO..O.', 'X..O.O', '..OO..']}


def star(b): return next((r, c) for r in range(N) for c in range(N) if b[r][c] == '*')


def flips(b, dirs=D8):
    r, c = star(b); out = []
    for dr, dc in dirs:
        run = []; rr, cc = r + dr, c + dc
        while 0 <= rr < N and 0 <= cc < N and b[rr][cc] == 'O': run.append((rr, cc)); rr += dr; cc += dc
        if run and 0 <= rr < N and 0 <= cc < N and b[rr][cc] == 'X': out += run
    return out


FLIP = {k: flips(b) for k, b in BOARDS.items()}
code = ''.join(str(len(FLIP[k])) for k in 'ABCD')
trap = ''.join(str(len(flips(BOARDS[k], [d for d in D8 if 0 in d]))) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['6395'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'flipped': FLIP, 'trap_no_diagonals': trap,
               'why': '가로·세로뿐 아니라 대각선 네 방향도 확인해야 해요. 여덟 방향 모두 뒤집혀요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
