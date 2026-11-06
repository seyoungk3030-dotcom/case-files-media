"""ROOM 070 proof: 3x3 sliding tiles (numbers 1-8 and one gap). The pushes listed are done in order; each pushed tile is
next to the gap and slides into it. The digit is the number that ends on the star cell. Every push is checked to be legal,
the end position is simulated, every 4-digit code is compared and exactly one matches. Reading the star cell before the
pushes (the trap) gives a different code."""
import itertools, json, os
# grid rows top→bottom, 0 = gap; pushes; star cell (row, col)
BOARDS = {
    'A': ((5, 1, 3), (8, 0, 2), (7, 4, 6)), 'B': ((2, 6, 0), (1, 8, 5), (4, 3, 7)),
    'C': ((3, 7, 1), (6, 5, 8), (0, 2, 4)), 'D': ((8, 2, 4), (1, 6, 0), (5, 7, 3)),
}
PUSH = {'A': (1, 3, 2), 'B': (5, 8, 1), 'C': (6, 5, 7), 'D': (4, 2, 6)}
STAR = {'A': (0, 1), 'B': (1, 1), 'C': (1, 1), 'D': (0, 1)}


def run(g, pushes):
    g = [list(r) for r in g]
    for t in pushes:
        (r0, c0), = [(r, c) for r in range(3) for c in range(3) if g[r][c] == 0]
        (r1, c1), = [(r, c) for r in range(3) for c in range(3) if g[r][c] == t]
        assert abs(r0 - r1) + abs(c0 - c1) == 1, ('illegal push', t)
        g[r0][c0], g[r1][c1] = t, 0
    return g


for k, g in BOARDS.items(): assert sorted(sum(g, ())) == list(range(9)), k
END = {k: run(BOARDS[k], PUSH[k]) for k in 'ABCD'}
res = {k: END[k][STAR[k][0]][STAR[k][1]] for k in 'ABCD'}
before = ''.join(str(BOARDS[k][STAR[k][0]][STAR[k][1]]) for k in 'ABCD')
code = ''.join(str(res[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'before', before, 'solutions', sols)
assert sols == ['3176'] and before == '1852' and all(res.values())
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'start': BOARDS, 'pushes': PUSH, 'star': STAR, 'end': END,
               'trap_star_before': before,
               'why': '밀 때마다 빈칸 위치가 바뀌고, 별 칸에는 다른 타일이 들어옴. A 1→3→2 후 별 3 · B 5→8→1 후 별 1 · C 6→5→7 후 별 7 · D 4→2→6 후 별 6'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
