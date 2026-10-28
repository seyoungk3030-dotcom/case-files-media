"""ROOM 052 proof: a 4-3-2-1 block pyramid where every block is the sum of the two blocks under it. Shown numbers are
fixed; A B C D and one blank block (E) are unknown. The bottom row fixes every block above it, so trying every whole
value 0-99 for the two unknown bottom blocks covers every possible pyramid; exactly one fits the shown numbers."""
import itertools, json, os
SHOWN = {(0, 0): 3, (0, 2): 2, (1, 1): 7, (2, 0): 15, (3, 0): 28}
UNK = {(0, 1): 'A', (0, 3): 'B', (1, 0): 'C', (1, 2): 'D', (2, 1): 'E'}


def fits(g):
    return all(g[(r, i)] == g[(r - 1, i)] + g[(r - 1, i + 1)] for r in (1, 2, 3) for i in range(4 - r))


sols = []
for a, b in itertools.product(range(100), repeat=2):     # the bottom row fixes every block above it
    g = {(0, 0): 3, (0, 1): a, (0, 2): 2, (0, 3): b}
    for r in (1, 2, 3):
        for i in range(4 - r): g[(r, i)] = g[(r - 1, i)] + g[(r - 1, i + 1)]
    if all(g[k] == v for k, v in SHOWN.items()) and all(0 <= g[k] <= 99 for k in UNK): sols.append(g)
g = sols[0]; code = ''.join(str(g[k]) for k in sorted(UNK, key=UNK.get) if UNK[k] != 'E')
print(len(sols), code, {UNK[k]: g[k] for k in UNK})
assert len(sols) == 1 and code == '5486'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'bottom_rows_tested': 100 * 100, 'shown': {f'{r},{i}': v for (r, i), v in SHOWN.items()},
               'grid': {f'{r},{i}': v for (r, i), v in g.items()}, 'blank_E': g[(2, 1)],
               'why': 'C = 15 − 7 = 8 · A = 7 − 2 = 5 · 빈칸 = 28 − 15 = 13 · D = 13 − 7 = 6 · B = 6 − 2 = 4'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
