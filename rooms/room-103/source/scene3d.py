"""ROOM 103 3D sprites: a wooden block tower, three blocks per layer, layers crossed, some blocks already pulled.
Seen from the front-right so every layer shows its three block ends on one face. Four blocks carry painted numbers.
a*: the one safe block slides half out and glows mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
L, W, T = 1.5, 0.48, 0.3


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m, rot):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def scene(k, after):
    b = BOARDS[k]; lab = {v: n for n, v in b['num'].items()}; win = b['num'][RES[k][0]]
    woods = [b3d.mat(f'w{i}', c, rough=0.6, coat=0.1) for i, c in enumerate([(0.78, 0.55, 0.30), (0.70, 0.47, 0.24)])]
    tag = b3d.mat('tag', (0.95, 0.62, 0.12), rough=0.5, coat=0.1); ink = b3d.mat('ink', (0.05, 0.06, 0.1), rough=0.6, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 0.8)
    base = b3d.mat('base', (0.10, 0.12, 0.18), rough=0.7, coat=0)
    bpy.ops.mesh.primitive_cylinder_add(radius=1.5, depth=0.1, location=(0, 0, -0.05), vertices=96); bpy.context.object.data.materials.append(base)
    for li, row in enumerate(b['layers']):
        z = T / 2 + li * T
        for p, c in enumerate(row):
            if c != '#': continue
            off = (p - 1) * 0.5; along_x = li % 2 == 0
            pulled = after and (li, p) == win; out = 0.85 if pulled else 0
            loc = (out, off, z) if along_x else (off, -out, z)
            m = mint if pulled else (tag if (li, p) in lab else woods[(li + p) % 2])
            bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
            o.scale = (L, W, T * 0.96) if along_x else (W, L, T * 0.96); o.data.materials.append(m); b3d.bevel(o, 0.025)
            if (li, p) in lab:
                n = str(lab[(li, p)])
                if along_x: text(n, (loc[0] + L / 2 + 0.002, off, z), 0.26, ink, (math.radians(90), 0, math.radians(90)))
                else: text(n, (off, loc[1] - L / 2 - 0.002, z), 0.26, ink, (math.radians(90), 0, 0))
    b3d.stack_camera((0.25, -0.2, 0.95), 3.6, az=38.0, el=20.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((700, 860), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
