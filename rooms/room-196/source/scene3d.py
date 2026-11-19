"""ROOM 196 3D sprites: a small car on a road strip under a sign that shows its fuel economy before -> after (km/L).
a*: the sign shows the litres used for 60 km before -> after, in mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, used
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
COL = {'A': (0.85, 0.2, 0.18), 'B': (0.15, 0.45, 0.9), 'C': (0.95, 0.7, 0.12), 'D': (0.2, 0.7, 0.45)}


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def box(m, loc, sc, bev=0.06):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m); b3d.bevel(o, bev, 4); return o


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.pi / 2, 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.015; t.data.materials.append(m)


def car(c):
    body = b3d.mat('body', c, rough=0.25, coat=0.8); glass = b3d.mat('glass', (0.12, 0.16, 0.24), rough=0.05, coat=0.5)
    tyre = b3d.mat('tyre', (0.05, 0.05, 0.06), rough=0.7, coat=0); rim = b3d.mat('rim', (0.8, 0.82, 0.86), rough=0.2, metal=1.0, coat=0)
    lamp = glowm('lamp', (1.0, 0.92, 0.6), 2.0)
    box(body, (0, 0, 0.42), (2.0, 0.9, 0.42), 0.12)
    box(body, (-0.1, 0, 0.82), (1.1, 0.8, 0.42), 0.14)
    box(glass, (-0.1, -0.005, 0.84), (1.0, 0.82, 0.32), 0.1)
    for x in (-0.65, 0.65):
        for y in (-0.42, 0.42):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.24, depth=0.18, location=(x, y, 0.24), rotation=(math.pi / 2, 0, 0)); o = bpy.context.object
            o.data.materials.append(tyre); bpy.ops.object.shade_smooth()
            bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.2, location=(x, y, 0.24), rotation=(math.pi / 2, 0, 0)); bpy.context.object.data.materials.append(rim)
    box(lamp, (1.0, -0.3, 0.48), (0.04, 0.16, 0.08), 0.02); box(lamp, (1.0, 0.3, 0.48), (0.04, 0.16, 0.08), 0.02)


def scene(key, after):
    a, b = BOARDS[key]
    road = b3d.mat('road', (0.16, 0.17, 0.2), rough=0.8, coat=0); line = glowm('line', (0.95, 0.95, 0.9), 0.4)
    box(road, (0, 0, -0.05), (3.2, 1.6, 0.1), 0.02)
    for x in (-1.2, 0, 1.2): box(line, (x, 0.65, 0.005), (0.6, 0.06, 0.01), 0.005)
    car(COL[key])
    panel = b3d.mat('panel', (0.07, 0.09, 0.14), rough=0.4, coat=0); pole = b3d.mat('pole', (0.6, 0.62, 0.66), rough=0.3, metal=1.0, coat=0)
    box(panel, (0, 0.6, 1.85), (2.9, 0.08, 0.78), 0.05)
    for x in (-1.25, 1.25): box(pole, (x, 0.66, 0.75), (0.07, 0.07, 1.5), 0.02)
    if after:
        s = f'{int(used(a))}L → {int(used(b))}L'; m = glowm('mint', (0.2, 0.95, 0.65), 1.2)
    else:
        s = f'{a} → {b}'; m = glowm('wt', (0.97, 0.97, 1.0), 0.6)
    text(s, (0, 0.54, 1.92), 0.5, m)
    text('60km 쓴 기름' if after else 'km/L', (0, 0.54, 1.58), 0.22, glowm('soft', (1.0, 0.82, 0.3), 0.8))
    b3d.stack_camera((0, 0, 1.0), 3.4, az=18.0, el=10.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((700, 640), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t, 1), flush=True)
