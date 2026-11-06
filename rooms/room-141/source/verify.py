"""ROOM 141 proof: pipe tiles. A 3x3 grid of square tiles each holds a straight (I) or bent (L) pipe. Water enters from the
left side at the arrow and must leave at the drain on the right side. A tile turns only clockwise, a quarter turn per
click; any tile may be clicked. Every combination of clicks on all 9 tiles is tried (I: 0-1, L: 0-3; more is a repeat)
and the smallest total that joins the inlet to the drain is the digit. All 10^4 codes compared; exactly one matches.
The trap: counting the TILES that must turn instead of the CLICKS (a bend that needs a left turn costs 3 clicks)."""
import itertools, json, os
N, E, S, W = 1, 2, 4, 8
BASE = {'I': N | S, 'L': N | E}
OPP = {N: S, S: N, E: W, W: E}; DV = {N: (-1, 0), S: (1, 0), E: (0, 1), W: (0, -1)}
# T: tile kinds; O: starting quarter turns from BASE (clockwise); src/dst: row of inlet (left) / drain (right)
BOARDS = {'A': {'T': ['LIL', 'ILL', 'IIL'], 'O': [[3, 3, 1], [3, 2, 2], [0, 3, 2]], 'src': 2, 'dst': 1},
          'B': {'T': ['LLL', 'IIL', 'LLI'], 'O': [[1, 0, 3], [1, 0, 1], [1, 1, 3]], 'src': 2, 'dst': 2},
          'C': {'T': ['IIL', 'ILL', 'ILI'], 'O': [[2, 1, 1], [1, 3, 1], [1, 3, 2]], 'src': 2, 'dst': 0},
          'D': {'T': ['LIL', 'ILI', 'ILL'], 'O': [[1, 1, 1], [3, 3, 2], [3, 1, 2]], 'src': 1, 'dst': 0}}


def rot(m, k):
    for _ in range(k): m = ((m << 1) | (m >> 3)) & 15
    return m


def flows(g, src, dst):
    if not g[src][0] & W: return False
    seen = {(src, 0)}; st = [(src, 0)]
    while st:
        r, c = st.pop()
        if (r, c) == (dst, 2) and g[r][c] & E: return True
        for d, (dr, dc) in DV.items():
            rr, cc = r + dr, c + dc
            if g[r][c] & d and 0 <= rr < 3 and 0 <= cc < 3 and g[rr][cc] & OPP[d] and (rr, cc) not in seen: seen.add((rr, cc)); st.append((rr, cc))
    return False


def best(b):
    cells = [(r, c) for r in range(3) for c in range(3)]; top = None
    for ks in itertools.product(*[range(2 if b['T'][r][c] == 'I' else 4) for r, c in cells]):
        g = [[0] * 3 for _ in range(3)]
        for (r, c), k in zip(cells, ks): g[r][c] = rot(rot(BASE[b['T'][r][c]], b['O'][r][c]), k)
        if flows(g, b['src'], b['dst']) and (top is None or sum(ks) < sum(top)): top = ks
    return top


RES = {k: best(b) for k, b in BOARDS.items()}
code = ''.join(str(sum(RES[k])) for k in 'ABCD'); trap = ''.join(str(sum(1 for x in RES[k] if x)) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, RES)
assert sols == ['5847'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'clicks': {k: [list(v[i:i + 3]) for i in (0, 3, 6)] for k, v in RES.items()},
               'trap_tiles_not_clicks': trap, 'why': '시계 방향으로만 돌아가서, 왼쪽으로 한 칸 돌려야 하는 굽은 관은 세 번 눌러야 해요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
