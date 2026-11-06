"""ROOM 139 proof: coin shapes on a table, packed like a honeycomb (triangular lattice: a coin at (x, r) with x + r
even, rows r, half-coin steps x). The task is to turn each shape upside down (or flip the T) by sliding as few coins
as possible; the finished shape may sit anywhere. Coins that already sit where the new shape needs them stay, so the
least number of moves = coins - the largest overlap of the shape with any shifted copy of its flipped self (searched
over every lattice shift). Digit = that minimum. All 10^4 codes are compared; exactly one matches. The trap: 'move the
whole bottom row' (the longest row's coin count)."""
import itertools, json, os


def tri(n): return sorted((x, r) for r in range(n) for x in range(-r, r + 1, 2))


T_SHAPE = [(0, 0), (2, 0), (4, 0), (6, 0), (8, 0), (5, 1), (4, 2), (5, 3), (4, 4)]
BOARDS = {'A': {'coins': tri(4), 'flip': 'rot'}, 'B': {'coins': T_SHAPE, 'flip': 'vert'}, 'C': {'coins': tri(5), 'flip': 'rot'}, 'D': {'coins': tri(6), 'flip': 'rot'}}
F = {'rot': lambda p: (-p[0], -p[1]), 'vert': lambda p: (p[0], -p[1])}


def solve(b):
    S = set(map(tuple, b['coins'])); T = [F[b['flip']](p) for p in S]; best = (0, None)
    for dx in range(-24, 25):
        for dr in range(-14, 15):
            if (dx + dr) % 2: continue
            tgt = {(x + dx, r + dr) for x, r in T}; o = len(S & tgt)
            if o > best[0]: best = (o, sorted(tgt))
    rows = {}
    for x, r in S: rows[r] = rows.get(r, 0) + 1
    return len(S) - best[0], max(rows.values()), best[1]


RES = {k: solve(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if all(int(c[i]) == solve(BOARDS[k])[0] for i, k in enumerate('ABCD'))]
print('answer', code, 'trap', trap)
assert sols == ['3457'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': {k: {'coins': [list(p) for p in b['coins']], 'flip': b['flip']} for k, b in BOARDS.items()},
               'targets': {k: v[2] for k, v in RES.items()}, 'trap_bottom_row': trap,
               'why': '가운데 동전들은 그대로 두고, 바깥 모서리 동전만 옮기면 가장 적게 움직여요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
