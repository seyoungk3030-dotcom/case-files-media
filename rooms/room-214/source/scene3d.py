"""ROOM 214 3D sprites: a red die and a blue die (size 1) on a dark felt dice mat; the question view is zoomed in 2x on the one example roll. p*: one example roll that makes the board's sum.
a*: every red/blue roll that makes the sum, red on the left of each pair, in rows of three, with a mint ring under
each pair. Same camera for every board."""
import os, sys, time
import bpy
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, SHOW, pairs
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
RED, BLUE, WHITE = (0.82, 0.1, 0.1), (0.1, 0.32, 0.85), (0.97, 0.97, 0.97)
# right-handed die: 1-2-3 counter-clockwise around their shared corner; pick front/right for each top value
SIDE = {1: (2, 3), 2: (1, 4), 3: (1, 2), 4: (1, 5), 5: (1, 3), 6: (2, 4)}


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def faces(top):
    f, r = SIDE[top]
    return {(0, 0, 1): top, (0, 0, -1): 7 - top, (0, -1, 0): f, (0, 1, 0): 7 - f, (1, 0, 0): r, (-1, 0, 0): 7 - r}


def pair(x, y, r, b, ring=None):
    b3d.die(np.eye(3), (x - 0.56, y, 0.5), faces=faces(r), body=RED, pip=WHITE)
    b3d.die(np.eye(3), (x + 0.56, y, 0.5), faces=faces(b), body=BLUE, pip=WHITE)
    if ring:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.01)); o = bpy.context.object; o.scale = (2.5, 1.4, 0.02)
        o.data.materials.append(ring)


def grid(n):
    rows = [n] if n <= 3 else ([2, 2] if n == 4 else [3, n - 3])
    out = []
    for i, m in enumerate(rows):
        y = 0 if len(rows) == 1 else (0.85 if i == 0 else -0.85)
        for j in range(m): out.append(((j - (m - 1) / 2) * 2.85, y))
    return out


def scene(key, after):
    table = b3d.mat('table', (0.2, 0.16, 0.13), rough=0.9, coat=0.0)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.1)); t = bpy.context.object; t.scale = (8.6, 3.7, 0.2)
    bpy.ops.object.transform_apply(scale=True); t.data.materials.append(table); b3d.bevel(t, 0.12, 3)
    if after:
        mint = glowm('mint', (0.2, 0.95, 0.65), 1.6)
        for (x, y), (r, b) in zip(grid(len(pairs(BOARDS[key]))), pairs(BOARDS[key])): pair(x, y, r, b, mint)
    else:
        pair(0, 0, *SHOW[key])
    b3d.stack_camera((0, 0, 0.3), 8.9 if after else 4.4, az=0.0, el=74.0)


only = sys.argv[1:]
for key in 'ABCD':
    for kind in 'pa':
        nm = kind + key
        if only and nm not in only: continue
        b3d.reset((900, 420), 48); b3d.lights(10)
        t0 = time.time(); scene(key, kind == 'a')
        b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t0, 1), flush=True)
