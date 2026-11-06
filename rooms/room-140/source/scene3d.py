"""ROOM 140 3D sprites: a wooden triangle board with 10 numbered holes (bowling-pin order, 10 reads 0) and ivory pegs,
seen from above at a slant. p*: the starting pegs. a*: the one peg left is mint in its hole; the starting pegs that are
gone leave faint coral rings."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, POS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
SP = 0.95; EL = 62.0


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def xy(n):
    r, i = POS[n]; return ((i - r / 2) * SP, (1.5 - r) * SP * math.sqrt(3) / 2)


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - EL), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def peg(n, m):
    x, y = xy(n)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.42, location=(x, y, 0.21), vertices=32); bpy.context.object.data.materials.append(m)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=(x, y, 0.46), segments=32, ring_count=16); bpy.context.object.data.materials.append(m)


def scene(k, after):
    wood = b3d.mat('wood', (0.26, 0.14, 0.07), rough=0.8, coat=0); hole = b3d.mat('hole', (0.02, 0.015, 0.01), rough=1.0, coat=0)
    ivory = b3d.mat('ivory', (0.72, 0.66, 0.5), rough=0.45, coat=0); mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.35, coat=0); glow(mint, (0.15, 0.85, 0.6), 0.6)
    ink = b3d.mat('ink', (0.98, 0.85, 0.35), rough=0.6, coat=0); glow(ink, (0.98, 0.85, 0.35), 0.5)
    ring = b3d.mat('ring', (0.9, 0.35, 0.3), rough=0.5, coat=0); glow(ring, (0.9, 0.35, 0.3), 0.8)
    # board: rounded triangle prism
    R = 2.75
    bpy.ops.mesh.primitive_cylinder_add(radius=R, depth=0.24, vertices=3, location=(0, -0.41, -0.12), rotation=(0, 0, 0))
    o = bpy.context.object; o.data.materials.append(wood); b3d.bevel(o, 0.3, 6)
    for n in range(1, 11):
        x, y = xy(n)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.02, location=(x, y, 0.005), vertices=32); bpy.context.object.data.materials.append(hole)
        text(str(n % 10), (x + 0.32, y - 0.24, 0.03), 0.3, ink)
    if not after:
        for n in BOARDS[k]: peg(n, ivory)
    else:
        last = RES[k][0] or 10
        for n in BOARDS[k]:
            if n != last:
                x, y = xy(n); bpy.ops.mesh.primitive_torus_add(location=(x, y, 0.03), major_radius=0.2, minor_radius=0.025, major_segments=40); bpy.context.object.data.materials.append(ring)
        peg(last, mint)
    b3d.stack_camera((0, -0.35, 0.1), 5.3, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
