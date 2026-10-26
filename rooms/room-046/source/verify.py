"""ROOM 046 proof: each block A-D (width x depth x height in small cubes) is dipped whole in paint, so every outside
face is painted (bottom too), then cut into small cubes. Code = small cubes with no paint at all, A-D, counted cube by
cube. The trap forgets that the bottom was painted too."""
import json, os, itertools
BLOCKS = {'A': (5, 3, 3), 'B': (4, 4, 3), 'C': (3, 3, 3), 'D': (4, 4, 4)}


def unpainted(w, d, h, bottom=True):
    n = 0
    for x, y, z in itertools.product(range(w), range(d), range(h)):
        out = x in (0, w - 1) or y in (0, d - 1) or z == h - 1 or (bottom and z == 0)
        n += not out
    return n


res = {k: unpainted(*v) for k, v in BLOCKS.items()}
code = ''.join(str(res[k]) for k in 'ABCD')
trap = {k: unpainted(*v, bottom=False) for k, v in BLOCKS.items()}
print(res, code, trap)
assert code == '3418' and all(res[k] < 10 for k in res)
json.dump({'unique_answer': code, 'blocks_wdh': BLOCKS, 'unpainted': res, 'trap_bottom_forgotten': trap,
           'why': '칠 안 된 큐브 = 겉 한 겹을 모든 방향에서 벗긴 속: (가로-2)×(세로-2)×(높이-2). A 3×1×1=3, B 2×2×1=4, C 1, D 2×2×2=8'},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
