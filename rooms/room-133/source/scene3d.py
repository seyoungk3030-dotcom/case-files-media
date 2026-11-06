"""ROOM 133 3D sprites: a stack of six golden pancakes on a white plate, front view from slightly above, each with its
number on the front edge (every number has its own pancake size). p*: the starting stack. a*: the stack after all the
spatula flips; the top pancake gets a mint ring."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
TH = 0.24


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def rad(n): return 0.92 + 0.03 * n


def scene(k, after):
    stack = RES[k] if after else BOARDS[k]['stack']
    cake = b3d.mat('cake', (0.85, 0.55, 0.2), rough=0.7, coat=0); top = b3d.mat('top', (0.62, 0.33, 0.08), rough=0.6, coat=0.2)
    plate = b3d.mat('plate', (0.92, 0.93, 0.95), rough=0.3, coat=0.4); ink = b3d.mat('ink', (0.12, 0.06, 0.02), rough=0.6, coat=0)
    tag = b3d.mat('tag', (0.98, 0.95, 0.85), rough=0.6, coat=0); mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.8)
    bpy.ops.mesh.primitive_cylinder_add(radius=1.75, depth=0.08, location=(0, 0, 0.04), vertices=96); o = bpy.context.object; o.data.materials.append(plate); b3d.bevel(o, 0.03)
    for i, n in enumerate(reversed(stack)):
        z = 0.1 + TH / 2 + i * TH; r = rad(n)
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=TH - 0.02, location=(0, 0, z), vertices=96); o = bpy.context.object
        o.data.materials.append(cake); o.data.materials.append(top); b3d.bevel(o, 0.06, 4)
        for p in o.data.polygons:
            if p.normal.z > 0.9 or p.normal.z < -0.9: p.material_index = 1
        bpy.ops.mesh.primitive_cylinder_add(radius=0.16, depth=0.04, location=(0, -1.32, z), rotation=(math.radians(90), 0, 0), vertices=32)
        bpy.context.object.data.materials.append(tag); text(str(n), (0, -1.35, z), 0.2, ink)
        if after and i == len(stack) - 1:
            bpy.ops.mesh.primitive_torus_add(location=(0, 0, z), major_radius=r + 0.08, minor_radius=0.035, major_segments=96)
            bpy.context.object.data.materials.append(mint)
    b3d.stack_camera((0, 0, 0.85), 4.0, az=0.0, el=20.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 700), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
