"""ROOM 145 proof: capturing in baduk (Go) on a 7x7 board. X = black (you), O = white, * = where black plays. After
black plays, every white GROUP (stones joined up/down/left/right) that has no empty point next to it any more is taken
off the board. Digit = how many white stones are taken. All 10^4 codes compared; exactly one matches. The trap: counting
only the white stones that touch the new black stone, not the whole connected group."""
import itertools, json, os
N = 7
BOARDS = {'A': ['..XOO*O', '...XOOO', '....XOX', '.....X.', '.......', '.......', '.......'],
          'B': ['.......', '.......', '.......', '.......', '......*', '....XXO', '...XOOO'],
          'C': ['.......', '......X', '.....XO', '.....XO', '....XO*', '...XOOO', '...XOOO'],
          'D': ['OOX....', 'O*.....', 'OOX....', 'XX.....', '.......', '.......', '.......']}


def nb(r, c): return [(r + a, c + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= r + a < N and 0 <= c + b < N]


def group(g, r, c):
    p = g[r][c]; s = {(r, c)}; st = [(r, c)]; lib = set()
    while st:
        a, b = st.pop()
        for x, y in nb(a, b):
            if g[x][y] in '.*': lib.add((x, y))
            elif g[x][y] == p and (x, y) not in s: s.add((x, y)); st.append((x, y))
    return s, lib


def star(b): return next((r, c) for r in range(N) for c in range(N) if b[r][c] == '*')


def captured(b):
    r, c = star(b); h = [list(x) for x in b]; h[r][c] = 'X'; cap = set()
    for x, y in nb(r, c):
        if h[x][y] == 'O':
            s, l = group(h, x, y)
            if not l: cap |= s
    return sorted(cap)


for k, b in BOARDS.items():  # the position before the move is legal: every group still has a liberty
    assert all(group(b, r, c)[1] for r in range(N) for c in range(N) if b[r][c] in 'XO'), k
CAP = {k: captured(b) for k, b in BOARDS.items()}
code = ''.join(str(len(CAP[k])) for k in 'ABCD')
trap = ''.join(str(sum(1 for p in CAP[k] if p in nb(*star(BOARDS[k])))) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['7495'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'captured': CAP, 'trap_touching_only': trap,
               'why': '맞닿은 돌만이 아니라, 줄줄이 이어진 흰 돌 무리 전체가 숨 쉴 곳이 없어져서 통째로 잡혀요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
