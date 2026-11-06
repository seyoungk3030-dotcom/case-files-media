"""ROOM 110 3D sprites: a wooden board of square tiles (all the same wood, no checker colours) with a few tiles cut out
(dark holes) and four amber tiles numbered 1-4, seen from the front and above. a*: the right numbered tile is lifted
out (mint ring) and ivory dominoes cover every other square."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, cover, free
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def box(m, c, s, bev=0.03):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def scene(k, after):
    b = BOARDS[k]; R, C = b['size']; take = b['num'][RES[k][0][0] - 1]
    def P(r, c, z=0): return ((c - (C - 1) / 2), ((R - 1) / 2 - r), z)
    base = b3d.mat('base', (0.03, 0.04, 0.07), rough=0.7, coat=0); wood = b3d.mat('wood', (0.55, 0.36, 0.18), rough=0.6, coat=0.1)
    amber = b3d.mat('amber', (0.88, 0.45, 0.06), rough=0.5, coat=0.1); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    ivory = b3d.mat('ivory', (0.86, 0.85, 0.80), rough=0.35, coat=0.4); pip = b3d.mat('pip', (0.08, 0.09, 0.12), rough=0.5, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.6)
    box(base, (0, 0, -0.1), (C + 0.4, R + 0.4, 0.2), 0.05)
    lab = {n: i + 1 for i, n in enumerate(b['num'])}
    for r in range(R):
        for c in range(C):
            if (r, c) in b['holes'] or (after and (r, c) == take): continue
            box(amber if (r, c) in lab else wood, P(r, c, 0.06), (0.94, 0.94, 0.12), 0.04)
            if (r, c) in lab and not after: text(str(lab[(r, c)]), P(r, c, 0.13), 0.62, ink)
    if after:
        bpy.ops.mesh.primitive_torus_add(location=P(*take, 0.02), major_radius=0.36, minor_radius=0.05); bpy.context.object.data.materials.append(mint)
        for (r1, c1), (r2, c2) in cover(set(free(k)) - {take}):
            x1, y1, _ = P(r1, c1); x2, y2, _ = P(r2, c2); horiz = r1 == r2
            box(ivory, ((x1 + x2) / 2, (y1 + y2) / 2, 0.24), (1.84, 0.86, 0.14) if horiz else (0.86, 1.84, 0.14), 0.06)
            box(pip, ((x1 + x2) / 2, (y1 + y2) / 2, 0.31), (0.04, 0.6, 0.01) if horiz else (0.6, 0.04, 0.01), 0.005)
    b3d.stack_camera((0, 0, 0), max(R, C) + 1.6, az=8.0, el=62.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 860), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
