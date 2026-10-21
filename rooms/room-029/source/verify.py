"""ROOM 029 proof: four cube stacks on 3x3 floors seen from one camera (source/view.py). Rules: cubes stand only on
the 3x3 floor, nothing floats (every column is solid), and nothing is hidden that does not have to be there.
For each stack, try all 4^9 = 262,144 heightmaps, keep those that show exactly the same visible cubes, and take
the smallest. It must be one heightmap, the drawn one. The code is the cube counts of A, B, C, D."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import view
STACKS = {  # heights row by row: front row first, left column first
    'A': (2, 0, 0, 2, 1, 0, 2, 0, 0),
    'B': (0, 0, 0, 0, 1, 0, 0, 3, 1),
    'C': (0, 3, 2, 0, 3, 1, 0, 0, 0),
    'D': (0, 1, 0, 1, 0, 0, 3, 1, 0),
}
H, F, V = view.all_visible_sets()
cnt = H.sum(1).astype(int); res = {}
for k, h in STACKS.items():
    n = int(np.where((H == np.array(h)).all(1))[0][0])
    same = np.where((V == V[n]).all(1))[0]
    mins = same[cnt[same] == cnt[same].min()]
    vis = int(V[n].sum())
    res[k] = {'heights': [list(h[r * 3:(r + 1) * 3]) for r in range(3)], 'same_view_heightmaps': int(len(same)),
              'min_count': int(cnt[same].min()), 'min_heightmaps': int(len(mins)), 'visible_cubes': vis,
              'hidden_supports': int(cnt[n]) - vis}
    print(k, res[k])
    assert len(mins) == 1 and mins[0] == n and res[k]['hidden_supports'] >= 1
code = ''.join(str(res[k]['min_count']) for k in 'ABCD'); trap = ''.join(str(res[k]['visible_cubes']) for k in 'ABCD')
print('code', code, 'trap (visible only)', trap)
assert code == '7596' and trap != code
json.dump({'unique_answer': code, 'heightmaps_tested_per_stack': 4 ** 9, 'stacks': res, 'trap_visible_only': trap,
           'why': 'a visible cube above the floor needs every cube under it, and the rule allows nothing else in hidden places'},
          open(os.path.join(HERE, '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
