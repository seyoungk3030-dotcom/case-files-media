"""ROOM 019 proof: 4x4 mini sudoku (rows, columns and 2x2 boxes each hold 1-4 once). Enumerate every valid grid,
keep those matching the given numbers, and read the code from cells A B C D."""
import itertools, json, os
GIVEN = {(0, 1): 3, (0, 3): 2, (1, 2): 1, (2, 0): 2, (3, 1): 1, (3, 2): 2}
STAR = [('A', (0, 0)), ('B', (1, 3)), ('C', (2, 1)), ('D', (3, 3))]
rows = list(itertools.permutations([1, 2, 3, 4]))
grids = []
for g in itertools.product(rows, repeat=4):
    if all(len({g[r][c] for r in range(4)}) == 4 for c in range(4)) and \
       all(len({g[r][c] for r in (br, br + 1) for c in (bc, bc + 1)}) == 4 for br in (0, 2) for bc in (0, 2)):
        grids.append(g)
match = [g for g in grids if all(g[r][c] == v for (r, c), v in GIVEN.items())]
print(len(grids), len(match), match)
assert len(grids) == 288 and len(match) == 1
code = ''.join(str(match[0][r][c]) for _, (r, c) in STAR)
print(code)
json.dump({'unique_answer': code, 'valid_grids_tested': len(grids), 'solution_grid': [list(r) for r in match[0]],
           'givens': {f'r{r+1}c{c+1}': v for (r, c), v in GIVEN.items()}, 'code_cells': {k: f'r{r+1}c{c+1}' for k, (r, c) in STAR}},
          open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
