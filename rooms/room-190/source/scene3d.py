"""ROOM 190 3D sprites: one road between a house (left) and an office building (right). The upper lane holds the car
going there (to the right), the lower lane the same car coming back (to the left). Each car carries a yellow plate with its speed. p*: question. a*: answer,
the road glows mint and the round-trip average speed floats above it."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def box(m, loc, scale, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def text(s, loc, size, m, rot=(math.pi / 2, 0, 0)):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def car(x, y, face, body, glass, tire):
    box(body, (x, y, 0.2), (0.7, 0.36, 0.2), 0.06); box(glass, (x - 0.04 * face, y, 0.38), (0.36, 0.3, 0.17), 0.05)
    for dx in (-0.22, 0.22):
        for dy in (-0.17, 0.17):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.07, location=(x + dx, y + dy, 0.1), rotation=(math.pi / 2, 0, 0), vertices=24)
            bpy.context.object.data.materials.append(tire)


def arrow(m, x, y, face):
    box(m, (x, y, 0.025), (0.5, 0.06, 0.02))
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.13, depth=0.03, location=(x + 0.3 * face, y, 0.025), rotation=(0, 0, -math.pi / 2 if face > 0 else math.pi / 2))
    bpy.context.object.data.materials.append(m)


def plate(x, y, z, v, m, ink):
    box(m, (x, y, z), (0.72 if v < 100 else 0.92, 0.08, 0.4), 0.05)
    text(str(v), (x, y - 0.05, z), 0.32, ink)


def scene(key, after):
    a, b = BOARDS[key]
    road = glowm('road', (0.1, 0.55, 0.4), 0.15) if after else b3d.mat('road', (0.16, 0.17, 0.2), rough=0.8, coat=0)
    paint = b3d.mat('paint', (0.92, 0.9, 0.82), rough=0.6, coat=0); grass = b3d.mat('grass', (0.2, 0.36, 0.24), rough=0.9, coat=0)
    blue = b3d.mat('blue', (0.15, 0.4, 0.95), rough=0.25); glass = b3d.mat('glass', (0.55, 0.75, 0.9), rough=0.1, coat=0)
    tire = b3d.mat('tire', (0.05, 0.05, 0.06), rough=0.7, coat=0); red = b3d.mat('red', (0.85, 0.1, 0.1), rough=0.4, coat=0)
    white = glowm('white', (0.95, 0.95, 0.95), 0.6); ink = b3d.mat('ink', (0.05, 0.05, 0.07), rough=0.5, coat=0)
    wall = b3d.mat('wall', (0.9, 0.82, 0.68), rough=0.7, coat=0); roof = b3d.mat('roof', (0.7, 0.25, 0.2), rough=0.6, coat=0)
    tower = b3d.mat('tower', (0.55, 0.62, 0.72), rough=0.4, metal=0.3, coat=0); win = glowm('win', (1.0, 0.85, 0.45), 0.8)
    yel = glowm('yel', (1.0, 0.8, 0.2), 1.0); mint = glowm('mint', (0.2, 0.95, 0.65), 0.5)
    box(grass, (0, 0, -0.06), (4.9, 2.4, 0.1)); box(road, (0, 0, 0.0), (3.2, 1.7, 0.02))
    for i in range(6): box(paint, (-1.25 + i * 0.5, 0, 0.015), (0.25, 0.04, 0.01))
    box(wall, (-1.95, 0.2, 0.3), (0.6, 0.6, 0.6), 0.02)
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.52, depth=0.4, location=(-1.95, 0.2, 0.8), rotation=(0, 0, math.pi / 4)); bpy.context.object.data.materials.append(roof)
    box(tower, (1.95, 0.2, 0.7), (0.6, 0.6, 1.4), 0.02)
    for r in range(4):
        for c in (-0.15, 0.15): box(win, (1.95 + c, -0.11, 0.3 + r * 0.3), (0.16, 0.02, 0.14))
    car(-1.0, 0.42, 1, blue, glass, tire); arrow(yel, -0.05, 0.42, 1); plate(-1.0, 0.42, 0.9, a, yel, ink)
    car(1.0, -0.42, -1, blue, glass, tire); arrow(yel, 0.05, -0.42, -1); plate(1.0, -0.42, 0.9, b, yel, ink)
    if after: text(str(GOOD[key] * 10), (0, 0.1, 1.7), 0.6, mint)
    b3d.stack_camera((0, 0, 0.55), 4.7, az=0.0, el=50.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((900, 640), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
