"""ROOM 077 3D sprites: a Ferris wheel (rim, spokes, A-frame legs) with 8 hanging cabins, a digit on each cabin.
p*: before the turn. a*: after the turn, the cabin now at the top glows amber."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import WHEELS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
X90 = (math.radians(90), 0, 0)
COLS = {'A': (0.95, 0.45, 0.55), 'B': (0.35, 0.6, 0.95), 'C': (0.3, 0.78, 0.6), 'D': (0.7, 0.5, 0.95)}


def label(s, x, z, size, m, y):
    bpy.ops.object.text_add(location=(x, y, z), rotation=X90); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def box(loc, scale, m, bev=0.04, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def scene(k, after):
    cab, t = WHEELS[k]
    steel = b3d.mat('steel', (0.85, 0.87, 0.92), rough=0.3, metal=0.5); col = b3d.mat('col', COLS[k], rough=0.35, coat=0.6)
    hot = b3d.mat('hot', (0.98, 0.65, 0.1), rough=0.3); q = hot.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (0.98, 0.65, 0.1, 1); q.inputs['Emission Strength'].default_value = 0.7
    ink = b3d.mat('ink', (0.06, 0.09, 0.18), rough=0.4); face = b3d.mat('face', (0.97, 0.98, 1.0), rough=0.4)
    R, H = 2.0, 2.6
    bpy.ops.mesh.primitive_torus_add(location=(0, 0.15, H), rotation=X90, major_radius=R, minor_radius=0.05); bpy.context.object.data.materials.append(steel)
    for i in range(8):
        a = math.radians(i * 45)
        box((R / 2 * math.sin(a), 0.15, H + R / 2 * math.cos(a)), (0.04, 0.04, R), steel, 0.01, rot=(0, a, 0))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.4, location=(0, 0.15, H), rotation=X90); bpy.context.object.data.materials.append(col)
    for s in (-1, 1): box((s * 0.75, 0.35, H / 2), (0.09, 0.09, H * 1.15), steel, 0.02, rot=(0, math.radians(-16 * s), 0))
    box((0, 0.35, 0.03), (2.4, 0.5, 0.06), steel, 0.02)
    shift = t if after else 0
    for i in range(8):
        a = math.radians((i + shift) * 45); x, z = R * math.sin(a), H + R * math.cos(a)
        on_top = after and (i + shift) % 8 == 0
        box((x, 0.1, z - 0.08), (0.03, 0.03, 0.2), steel, 0.005)
        box((x, 0, z - 0.5), (0.8, 0.5, 0.7), hot if on_top else col, 0.12)
        box((x, -0.255, z - 0.5), (0.62, 0.02, 0.56), face, 0.06)
        label(str(cab[i]), x, z - 0.5, 0.55, ink, -0.27)
    b3d.stack_camera((0, 0, H - 0.15), 6.3, az=0.0, el=4.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 900), 40); b3d.lights(8)
        tt = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - tt, 1), flush=True)
