"""ROOM 165 3D sprites: a frying pan with k dashed spots (how many pancakes fit at once) next to a plate with a stack of
n raw pancakes and a paper tag behind naming both numbers. p*: before. a*: after, every pancake golden brown on the
plate and the pan empty."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
EL = 50.0; PR = 0.4
SPOTS = {2: [(-0.45, 0), (0.45, 0)], 3: [(0, 0.5), (-0.46, -0.27), (0.46, -0.27)], 4: [(-0.45, 0.45), (0.45, 0.45), (-0.45, -0.45), (0.45, -0.45)]}


def box(loc, scale, m, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 5)
    return o


def cyl(loc, r, d, m, bev=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=r, depth=d, location=loc); o = bpy.context.object; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 4)
    return o


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - 20), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def scene(key, after):
    b = BOARDS[key]; k, n = b['k'], b['n']
    pan = b3d.mat('pan', (0.08, 0.08, 0.09), rough=0.35, metal=0.6, coat=0); handle = b3d.mat('handle', (0.25, 0.14, 0.07), rough=0.6, coat=0)
    plate = b3d.mat('plate', (0.95, 0.95, 0.93), rough=0.25, coat=0.4); paper = b3d.mat('paper', (0.98, 0.93, 0.78), rough=0.7, coat=0)
    ink = b3d.mat('ink', (0.1, 0.08, 0.06), rough=0.8, coat=0)
    raw = b3d.mat('raw', (0.97, 0.88, 0.6), rough=0.8, coat=0); raw2 = b3d.mat('raw2', (0.9, 0.76, 0.45), rough=0.8, coat=0); gold2 = b3d.mat('gold2', (0.62, 0.33, 0.1), rough=0.6, coat=0); gold = b3d.mat('gold', (0.78, 0.45, 0.14), rough=0.6, coat=0)
    spot = b3d.mat('spot', (0.15, 0.85, 0.6), rough=0.4, coat=0)
    q = spot.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (0.15, 0.85, 0.6, 1); q.inputs['Emission Strength'].default_value = 1.2
    R = max(math.hypot(x, y) for x, y in SPOTS[k]) + PR + 0.12; px = -0.2 - R
    cyl((px, 0, 0.06), R + 0.08, 0.12, pan, 0.03); cyl((px, 0, 0.13), R, 0.04, pan)
    box((px - R - 0.5, 0, 0.12), (0.8, 0.18, 0.08), handle, 0.04)
    if not after:
        for x, y in SPOTS[k]:
            bpy.ops.mesh.primitive_torus_add(location=(px + x, y, 0.16), major_radius=PR - 0.02, minor_radius=0.025, major_segments=48)
            bpy.context.object.data.materials.append(spot)
    cx = 1.05
    cyl((cx, 0, 0.03), 0.62, 0.06, plate, 0.02)
    for i in range(n):
        cyl((cx, 0, 0.11 + i * 0.12), PR + 0.03 * ((i % 2) - 0.5), 0.1, (gold, gold2)[i % 2] if after else (raw, raw2)[i % 2], 0.035)
    tx = (px - R - 0.9 + cx + 0.62) / 2
    o = box((tx, 1.55, 0.55), (3.6, 0.05, 0.7), paper, 0.03); o.rotation_euler = (math.radians(-20), 0, 0)
    text(f'{n}장 · 팬에 {k}장씩', (tx, 1.51, 0.57), 0.44, ink)
    b3d.stack_camera((tx, 0.3, 0.4), 6.0, az=0.0, el=EL)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((1000, 760), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
