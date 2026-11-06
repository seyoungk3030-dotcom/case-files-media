"""ROOM 125 3D sprites: front view of spring scales in ropes. pulleys: a rope over two pulleys with a weight on each
end and the scale in the middle; wall: rope from a wall hook through the scale over a pulley to one weight; chain:
from a ceiling beam, scale X, block a, scale Y, block b. Weights are iron blocks with amber 'n kg' plates. The asked
scale's dial shows an amber '?'; a*: it shows the reading in mint."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
M = {}


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def box(m, c, s, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def rod(a, b, r, m):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=10); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y'); o.data.materials.append(m)


def scale_(c, vertical, label, mat):
    x, z = c
    body = box(M['body'], (x, 0, z), (0.5, 0.36, 1.1) if vertical else (1.1, 0.36, 0.5), 0.12)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.34, depth=0.04, location=(x, -0.2, z), rotation=(math.radians(90), 0, 0), vertices=48)
    bpy.context.object.data.materials.append(mat if label else M['dial'])
    if label: text(label, (x, -0.23, z), 0.4, M['ink'])
    return (0.55 if vertical else 0.55)


def weight(x, ztop, kg):
    h = 0.45 + 0.07 * kg; box(M['iron'], (x, 0, ztop - h / 2), (0.8, 0.6, h), 0.05)
    box(M['amber'], (x, -0.31, ztop - h / 2), (0.62, 0.03, 0.3), 0.04); text(f'{kg} kg', (x, -0.34, ztop - h / 2), 0.2, M['ink'])


def pulley(x, z):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.28, depth=0.14, location=(x, 0, z), rotation=(math.radians(90), 0, 0), vertices=48)
    bpy.context.object.data.materials.append(M['steel'])
    box(M['frame'], (x, 0.12, z / 2), (0.1, 0.1, z), 0.02)


def scene(k, after):
    b = BOARDS[k]; ans = RES[k][0]
    M.update(body=b3d.mat('body', (0.75, 0.78, 0.84), rough=0.35, metal=0.4, coat=0.2), dial=b3d.mat('dial', (0.95, 0.95, 0.92), rough=0.5, coat=0),
             iron=b3d.mat('iron', (0.15, 0.16, 0.19), rough=0.4, metal=0.6, coat=0), amber=b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0.1),
             ink=b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0), steel=b3d.mat('steel', (0.6, 0.63, 0.7), rough=0.3, metal=0.8, coat=0),
             frame=b3d.mat('frame', (0.12, 0.13, 0.18), rough=0.5, coat=0.1), rope=b3d.mat('rope', (0.85, 0.8, 0.65), rough=0.7, coat=0))
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.2)
    ask_label, ask_mat = (str(ans), mint) if after else ('?', M['amber'])
    box(M['frame'], (0, 0.2, -0.06), (6.2, 1.4, 0.12), 0.03)
    if b['kind'] in ('pulleys', 'wall'):
        zr = 3.0; pr = 0.28
        pulley(2.3, zr - pr)
        if b['kind'] == 'pulleys':
            pulley(-2.3, zr - pr); rod((-2.3, -0.02, zr), (-0.55, -0.02, zr), 0.025, M['rope'])
            rod((-2.3 - pr, -0.02, zr - pr), (-2.3 - pr, -0.02, 1.3), 0.025, M['rope']); weight(-2.3 - pr, 1.3, b['W'])
        else:
            box(M['frame'], (-2.85, 0.1, 1.6), (0.3, 1.0, 3.4), 0.03)
            bpy.ops.mesh.primitive_torus_add(location=(-2.62, -0.02, zr), rotation=(0, math.radians(90), 0), major_radius=0.1, minor_radius=0.03)
            bpy.context.object.data.materials.append(M['steel']); rod((-2.62, -0.02, zr), (-0.55, -0.02, zr), 0.025, M['rope'])
        rod((0.55, -0.02, zr), (2.3, -0.02, zr), 0.025, M['rope'])
        rod((2.3 + pr, -0.02, zr - pr), (2.3 + pr, -0.02, 1.3), 0.025, M['rope']); weight(2.3 + pr, 1.3, b['W'])
        scale_((0, zr), False, ask_label, ask_mat)
    else:
        top = 4.75; box(M['frame'], (0, 0.1, top + 0.1), (2.6, 0.8, 0.2), 0.03)
        a, bb = b['a'], b['b']; z = top
        rod((0, -0.02, z), (0, -0.02, z - 0.25), 0.025, M['rope']); z -= 0.25 + 0.55
        scale_((0, z), True, ask_label if b['ask'] == 'X' else '', ask_mat); text('X', (0.55, -0.2, z + 0.3), 0.26, M['body'])
        z -= 0.55; rod((0, -0.02, z), (0, -0.02, z - 0.2), 0.025, M['rope']); z -= 0.2
        weight(0, z, a); z -= 0.45 + 0.07 * a
        rod((0, -0.02, z), (0, -0.02, z - 0.2), 0.025, M['rope']); z -= 0.2 + 0.55
        scale_((0, z), True, ask_label if b['ask'] == 'Y' else '', ask_mat); text('Y', (0.55, -0.2, z + 0.3), 0.26, M['body'])
        z -= 0.55; rod((0, -0.02, z), (0, -0.02, z - 0.2), 0.025, M['rope']); z -= 0.2
        weight(0, z, bb)
    b3d.stack_camera((0, 0, 2.4), 6.9, az=0.0, el=4.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 1000), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
