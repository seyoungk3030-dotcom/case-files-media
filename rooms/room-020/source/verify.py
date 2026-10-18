"""ROOM 020 proof: thermal smudges on a phone-style keypad. Enumerate every 4-digit code 0000-9999 and keep those
that use exactly the four warm keys once each, start on the coldest key, end on the hottest key, and move only to an
up/down/left/right neighbour between presses."""
import json, os
POS = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (1, 0), 5: (1, 1), 6: (1, 2), 7: (2, 0), 8: (2, 1), 9: (2, 2), 0: (3, 1)}
WARM = {5, 6, 8, 9}
HOTTEST, COLDEST = 6, 9          # 5 and 8 look equally warm


def adj(a, b):
    (r1, c1), (r2, c2) = POS[a], POS[b]
    return abs(r1 - r2) + abs(c1 - c2) == 1


ok, trap = [], []
for n in range(10000):
    d = [int(x) for x in f'{n:04d}']
    if set(d) != WARM or len(set(d)) != 4: continue
    if d[0] != COLDEST or d[-1] != HOTTEST: continue
    trap.append(f'{n:04d}')
    if all(adj(a, b) for a, b in zip(d, d[1:])): ok.append(f'{n:04d}')
print(trap, ok)
assert ok == ['9856']
json.dump({'unique_answer': ok[0], 'codes_tested': 10000, 'heat_only_candidates': trap,
           'rule_that_breaks_tie': 'orthogonal adjacency (9-5 is diagonal)'},
          open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
