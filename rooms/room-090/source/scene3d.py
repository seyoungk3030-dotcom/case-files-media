"""ROOM 090 3D sprites: equal wooden blocks stacked off the edge of a dark table, seen from the front against a wall
with a grid (one square = a quarter block) and a coral line at the table edge. a*: the blocks that fall turn coral and
glow; the blocks that stay keep their colour."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, W
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
U = 0.36; H = 0.46
COLS = [(0.85, 0.55, 0.25), (0.20, 0.50, 0.90), (0.95, 0.72, 0.10), (0.20, 0.70, 0.45), (0.55, 0.38, 0.90), (0.10, 0.65, 0.75), (0.90, 0.50, 0.65)]


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def box(m, x, z, sx, sy, sz, y=0.0, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z)); o = bpy.context.object; o.scale = (sx, sy, sz); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev)
    return o


def scene(k, after):
    c = BOARDS[k]; nf, lvl = RES[k]
    wall = b3d.mat('wall', (0.03, 0.04, 0.07), rough=0.9, coat=0); line = b3d.mat('line', (0.2, 0.24, 0.32), rough=0.9, coat=0); glow(line, (0.3, 0.36, 0.5), 0.15)
    edge = b3d.mat('edge', (0.98, 0.45, 0.38), rough=0.5, coat=0); glow(edge, (0.98, 0.45, 0.38), 1.0)
    table = b3d.mat('table', (0.30, 0.20, 0.14), rough=0.5, coat=0.3); red = b3d.mat('fall', (0.9, 0.08, 0.06), rough=0.4); glow(red, (1.0, 0.12, 0.08), 0.5)
    top = 7 * H
    xl, xr = -8 * U, 8 * U
    box(wall, 0, top / 2 + 0.2, xr - xl, 0.05, top + 1.2, y=0.75)
    for g in range(-8, 9):
        box(edge if g == 0 else line, g * U, top / 2 + 0.2, 0.02 if g else 0.06, 0.02, top + 1.2, y=0.71 if g else 0.6)
    box(table, (xl + 0) / 2 - 0.3, -0.35, -xl + 0.6, 1.4, 0.7, bev=0.03)
    for i, x in enumerate(c):
        m = red if after and lvl is not None and i >= lvl else b3d.mat(f'b{i}', COLS[i % len(COLS)], rough=0.45, coat=0.3)
        box(m, x * U, i * H + H / 2, W * U - 0.02, 0.9, H - 0.02, bev=0.03)
    b3d.stack_camera((0, 0, top / 2 - 0.05), max(xr - xl + 0.3, (top + 1.0) * 800 / 760), az=0.0, el=6.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((800, 760), 40); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
