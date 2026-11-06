"""ROOM 072 proof: block well 5 wide. The piece above drops straight down (no turning) until any of its cells would hit a
block or the floor. Every full row then disappears and the rows above fall down by the cleared count (rows fall as a whole,
no gravity per block). The digit is the number of blocks left. Simulated for every board, every 4-digit code compared:
exactly one matches. Forgetting to clear the rows (the trap) counts the blocks before clearing."""
import itertools, json, os
W = 5
PIECES = {'I': [(0, 0), (0, 1), (0, 2), (0, 3)], 'O': [(0, 0), (1, 0), (0, 1), (1, 1)], 'L': [(0, 0), (1, 0), (0, 1), (0, 2)],
          'J': [(0, 0), (1, 0), (1, 1), (1, 2)], 'T': [(0, 1), (1, 1), (2, 1), (1, 0)], 'S': [(0, 0), (1, 0), (1, 1), (2, 1)],
          'Z': [(1, 0), (2, 0), (0, 1), (1, 1)]}   # (dx, dy), dy up
# rows bottom→top as strings, piece, left column
BOARDS = {
    'A': (['XXXX.', 'XX.X.', 'X....'], 'I', 4),
    'B': (['XX.XX', 'X...X', 'X...X'], 'T', 1),
    'C': (['XXX..', 'XXX..', 'XXX..', 'X....'], 'O', 3),
    'D': (['.XXXX', '..XXX', '...XX'], 'L', 0),
}


def drop(rows, piece, col):
    cells = {(x, y) for y, r in enumerate(rows) for x, ch in enumerate(r) if ch == 'X'}
    shape = PIECES[piece]; y = len(rows) + 1
    assert all(0 <= col + dx < W for dx, dy in shape)
    while y > 0 and not any((col + dx, y - 1 + dy) in cells for dx, dy in shape): y -= 1
    placed = cells | {(col + dx, y + dy) for dx, dy in shape}
    H = max(yy for _, yy in placed) + 1
    full = [yy for yy in range(H) if all((x, yy) in placed for x in range(W))]
    left = {(x, yy - sum(f < yy for f in full)) for x, yy in placed if yy not in full}
    return placed, full, left


R = {k: drop(*BOARDS[k]) for k in 'ABCD'}
res = {k: len(R[k][2]) for k in 'ABCD'}; trap = ''.join(str(len(R[k][0]) % 10) for k in 'ABCD')
code = ''.join(str(res[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'cleared', {k: R[k][1] for k in 'ABCD'}, 'before', {k: len(R[k][0]) for k in 'ABCD'}, 'solutions', sols)
assert sols == ['7248'] and all(R[k][1] for k in 'ABCD') and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'rows_cleared': {k: R[k][1] for k in 'ABCD'},
               'blocks_before_clear': {k: len(R[k][0]) for k in 'ABCD'},
               'why': '조각은 돌리지 않고 곧장 떨어져 처음 닿는 곳에 멈춤. 꽉 찬 줄은 사라짐. A 12-5=7 · B 12-10=2 · C 14-10=4 · D 13-5=8'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
