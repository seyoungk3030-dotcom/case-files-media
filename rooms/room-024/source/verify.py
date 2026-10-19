"""ROOM 024 proof: 5x5 star placement (one star per row, column and colour region; stars never touch, not even
diagonally). Try every way to put one star in each row (5^5 = 3125) and keep the valid ones. The code is the
column number (1-5) of the star in rows 1-4."""
import itertools, json, os
REG = ['BBBAA', 'BBBAC', 'BBBBC', 'DDDCC', 'DEEEC']
ok = []
for cols in itertools.product(range(5), repeat=5):
    if len(set(cols)) < 5: continue                                   # one per column
    if any(abs(cols[r] - cols[r + 1]) <= 1 for r in range(4)): continue  # no touching (rows differ by 1)
    if len({REG[r][c] for r, c in enumerate(cols)}) < 5: continue      # one per region
    ok.append(cols)
print(ok)
assert len(ok) == 1
code = ''.join(str(c + 1) for c in ok[0][:4])
print(code)
assert code == '4251'
json.dump({'unique_answer': code, 'placements_tested': 5 ** 5, 'star_columns_rows_1_to_5': [c + 1 for c in ok[0]],
           'regions': REG}, open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'),
          ensure_ascii=False, indent=1)
