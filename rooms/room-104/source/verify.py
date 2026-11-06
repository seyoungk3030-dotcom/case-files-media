"""ROOM 104 proof: drop-disc four-in-a-row. Seven columns, six rows, rows listed bottom-up; R = red, Y = yellow. Red
moves next; a dropped disc falls to the lowest empty cell of its column. Each digit is the one column where red's
disc makes four in a row (horizontal, vertical or diagonal) right now. All 10^4 codes are compared; exactly one
matches. The trap: a column that would win only if the disc could float in mid-air (ignoring gravity) gives another
code. Boards came from seeded random play (gen104 seed 104) and are checked here from scratch."""
import itertools, json, os

C, RN = 7, 6
BOARDS = {'A': ['Y.RYYRY', 'R.RR.YY', 'R.YR.R.', '..R..Y.', '.....Y.', '.......'],
          'B': ['YRRYRR.', 'RYYRY..', 'YYRRR..', '..Y.Y..', '..Y....', '..R....'],
          'C': ['YR.RYY.', 'YR.YYR.', 'YR.RR..', 'RY.R...', '.Y.....', '.......'],
          'D': ['.RYYRRY', '..YRR.Y', '..R.Y..', '..R.Y..', '.......', '.......']}
DIRS = ((0, 1), (1, 0), (1, 1), (1, -1))


def grid(k): return [list(r) for r in BOARDS[k]]


def four(g, p):
    return [[(r + i * dr, c + i * dc) for i in range(4)] for r in range(RN) for c in range(C) for dr, dc in DIRS
            if all(0 <= r + i * dr < RN and 0 <= c + i * dc < C and g[r + i * dr][c + i * dc] == p for i in range(4))]


def low(g, c): return next((r for r in range(RN) if g[r][c] == '.'), None)


def legal(g):  # gravity: no floating discs; red to move means equal counts
    assert all(not (g[r][c] != '.' and g[r - 1][c] == '.') for r in range(1, RN) for c in range(C))
    n = sum(r.count('R') for r in g), sum(r.count('Y') for r in g); assert n[0] == n[1] and not four(g, 'R') and not four(g, 'Y')


def wins(k):
    g = grid(k); legal(g); out = []
    for c in range(C):
        r = low(g, c)
        if r is None: continue
        g[r][c] = 'R'
        if four(g, 'R'): out.append((c + 1, r, four(g, 'R')))
        g[r][c] = '.'
    return out


def floating(k):
    g = grid(k); out = set()
    for c in range(C):
        r0 = low(g, c)
        for r in range(r0 + 1 if r0 is not None else RN, RN):
            g[r][c] = 'R'
            if four(g, 'R'): out.add(c + 1)
            g[r][c] = '.'
    return sorted(out - {w[0] for w in wins(k)})


RES = {k: wins(k) for k in 'ABCD'}; TR = {k: floating(k) for k in 'ABCD'}
assert all(len(v) == 1 for v in RES.values()) and all(len(v) == 1 for v in TR.values())
code = ''.join(str(RES[k][0][0]) for k in 'ABCD'); trap = ''.join(str(TR[k][0]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: (v[0][1], v[0][2]) for k, v in RES.items()})
assert sols == ['5274'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'win': {k: {'col': v[0][0], 'row': v[0][1], 'line': v[0][2]} for k, v in RES.items()},
               'trap_floating_column': trap,
               'why': '떨어뜨린 칩은 그 줄의 가장 아래 빈칸까지 내려가요. 공중의 빈칸에 넣는 상상을 하면 함정'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
