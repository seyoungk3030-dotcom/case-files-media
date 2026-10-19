"""ROOM 025 proof: 4x4 skyscrapers. Each row and column holds buildings of height 1-4 once; an edge clue is how many
buildings are visible from that side (a taller one hides every shorter one behind it). Enumerate every Latin square,
keep those matching the clues, prove the match is unique and every clue is needed, and read the code from the diagonal."""
import itertools, json, os
CLUES = {('L', 0): 3, ('L', 2): 2, ('L', 3): 2, ('B', 2): 1, ('B', 3): 2}
STAR = [('A', (0, 0)), ('B', (1, 1)), ('C', (2, 2)), ('D', (3, 3))]


def vis(seq):
    top = n = 0
    for v in seq:
        if v > top: top, n = v, n + 1
    return n


def seen(g, side, i):
    col = [g[r][i] for r in range(4)]
    return vis({'L': list(g[i]), 'R': list(g[i])[::-1], 'T': col, 'B': col[::-1]}[side])


rows = list(itertools.permutations([1, 2, 3, 4]))
grids = [g for g in itertools.product(rows, repeat=4) if all(len({g[r][c] for r in range(4)}) == 4 for c in range(4))]
match = [g for g in grids if all(seen(g, s, i) == v for (s, i), v in CLUES.items())]
print(len(grids), len(match), match)
assert len(grids) == 576 and len(match) == 1
for k in CLUES:
    assert sum(all(seen(g, s, i) == v for (s, i), v in CLUES.items() if (s, i) != k) for g in grids) > 1, k
code = ''.join(str(match[0][r][c]) for _, (r, c) in STAR)
print(code)
assert code == '1213'
json.dump({'unique_answer': code, 'latin_squares_tested': len(grids), 'solution_grid': [list(r) for r in match[0]],
           'clues': {f'{s}{i+1}': v for (s, i), v in CLUES.items()}, 'every_clue_needed': True,
           'code_cells': {k: f'r{r+1}c{c+1}' for k, (r, c) in STAR}},
          open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
