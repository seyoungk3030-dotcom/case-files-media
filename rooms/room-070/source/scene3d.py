"""ROOM 070 3D sprites: a 3x3 sliding-tile tray seen from the front and above, a glowing mint frame around the star cell,
and the push order as numbered chips in front. a*: tiles after the pushes, the star cell's tile number amber."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, PUSH, STAR, END
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
S = 0.8


def xy(r, c): return ((c - 1) * S, (1 - r) * S)


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.015; t.data.materials.append(m)


def box(loc, scale, m, bev=0.03):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def glow(m, s=0.8):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
    q.inputs['Emission Strength'].default_value = s; return m


def scene(k, after):
    g = END[k] if after else BOARDS[k]; sr, sc = STAR[k]
    wood = b3d.mat('wood', (0.45, 0.32, 0.22), rough=0.55, coat=0.2); base = b3d.mat('base', (0.16, 0.20, 0.30), rough=0.5)
    tile = b3d.mat('tile', (0.95, 0.92, 0.84), rough=0.3, coat=0.7); ink = b3d.mat('ink', (0.16, 0.22, 0.36), rough=0.5, coat=0)
    mint = glow(b3d.mat('mint', b3d.PAL['mint'], rough=0.3, coat=0.5)); amber = glow(b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3))
    star_tile = b3d.mat('st', (0.99, 0.96, 0.86), rough=0.3, coat=0.7)
    W = 3 * S
    box((0, 0, -0.08), (W + 0.36, W + 0.36, 0.16), wood, 0.05); box((0, 0, 0.005), (W, W, 0.01), base, 0.003)
    for sgn in (-1, 1):
        box((0, sgn * (W / 2 + 0.09), 0.12), (W + 0.36, 0.18, 0.24), wood, 0.04); box((sgn * (W / 2 + 0.09), 0, 0.12), (0.18, W, 0.24), wood, 0.04)
    x, y = xy(sr, sc)
    for dx, dy, sx, sy in ((0, S / 2 - 0.03, S - 0.02, 0.05), (0, -S / 2 + 0.03, S - 0.02, 0.05), (S / 2 - 0.03, 0, 0.05, S - 0.02), (-S / 2 + 0.03, 0, 0.05, S - 0.02)):
        box((x + dx, y + dy, 0.03), (sx, sy, 0.04), mint, 0.005)
    for r in range(3):
        for c in range(3):
            t = g[r][c]
            if not t: continue
            x, y = xy(r, c); star = (r, c) == (sr, sc)
            box((x, y, 0.13), (S * 0.84, S * 0.84, 0.24), amber if (after and star) else tile, 0.06)
            text(str(t), (x, y, 0.255), 0.46, ink)
    n = len(PUSH[k])
    for i, t in enumerate(PUSH[k]):
        x = (i - (n - 1) / 2) * 0.95
        bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.07, location=(x, -W / 2 - 0.7, 0.035)); bpy.context.object.data.materials.append(mint)
        text(str(t), (x, -W / 2 - 0.7, 0.08), 0.4, b3d.mat('w', (0.98, 0.99, 1.0), rough=0.4))
        if i < n - 1: text('→', (x + 0.475, -W / 2 - 0.7, 0.02), 0.26, b3d.mat('w2', (0.9, 0.93, 0.98), rough=0.4))
    b3d.stack_camera((0, -0.45, 0), 4.2, az=0.0, el=62.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 900), 40); b3d.lights(5)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
