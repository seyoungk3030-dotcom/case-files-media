"""ROOM 122 3D sprites: top view of a dark table with one bar magnet in the middle (red N half with a white N,
blue S half with a white S) turned to the board's angle, and a compass at the marked spot: white face with eight
numbered directions (1 = up, clockwise) and a grey '?' in the middle. a*: the compass shows its needle, red tip
along the magnet's field, and the number it points to turns mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, H
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m, rz=0.0):
    bpy.ops.object.text_add(location=loc, rotation=(0, 0, rz)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def box(m, c, s, bev=0.04, rz=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.rotation_euler = (0, 0, rz); o.data.materials.append(m); b3d.bevel(o, bev); return o


def scene(k, after):
    b = BOARDS[k]; a = math.radians(b['angle']); cx, cy = b['compass']; d = RES[k][0]
    table = b3d.mat('table', (0.04, 0.05, 0.08), rough=0.7, coat=0); red = b3d.mat('red', (0.88, 0.18, 0.16), rough=0.4, coat=0.3)
    blue = b3d.mat('blue', (0.15, 0.35, 0.9), rough=0.4, coat=0.3); white = b3d.mat('white', (0.95, 0.95, 0.95), rough=0.4, coat=0)
    face = b3d.mat('face', (0.9, 0.9, 0.86), rough=0.5, coat=0); rim = b3d.mat('rim', (0.7, 0.55, 0.25), rough=0.3, metal=0.7, coat=0)
    ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0); grey = b3d.mat('grey', (0.55, 0.57, 0.62), rough=0.5, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.0)
    box(table, (0, 0, -0.06), (5.8, 5.8, 0.12), 0.03)
    ux, uy = math.cos(a), math.sin(a)
    box(red, (ux * H / 2, uy * H / 2, 0.15), (H, 0.62, 0.34), 0.04, a); box(blue, (-ux * H / 2, -uy * H / 2, 0.15), (H, 0.62, 0.34), 0.04, a)
    text('N', (ux * H * 0.55, uy * H * 0.55, 0.31), 0.34, white, a - math.pi / 2)
    text('S', (-ux * H * 0.55, -uy * H * 0.55, 0.31), 0.34, white, a - math.pi / 2)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.9, depth=0.16, location=(cx, cy, 0.08), vertices=64); bpy.context.object.data.materials.append(rim)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.82, depth=0.02, location=(cx, cy, 0.17), vertices=64); bpy.context.object.data.materials.append(face)
    for n in range(1, 9):
        th = math.radians(90 - 45 * (n - 1)); x, y = cx + 0.62 * math.cos(th), cy + 0.62 * math.sin(th)
        if after and n == d:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.17, depth=0.02, location=(x, y, 0.185), vertices=32); bpy.context.object.data.materials.append(mint)
        text(str(n), (x, y, 0.19), 0.24, ink)
    if after:
        th = math.radians(90 - 45 * (d - 1)); dx, dy = math.cos(th), math.sin(th)
        bpy.ops.mesh.primitive_cone_add(radius1=0.13, depth=0.46, location=(cx + dx * 0.21, cy + dy * 0.21, 0.22), vertices=4)
        o = bpy.context.object; o.rotation_euler = (0, math.radians(90), th); o.data.materials.append(red)
        bpy.ops.mesh.primitive_cone_add(radius1=0.13, depth=0.46, location=(cx - dx * 0.21, cy - dy * 0.21, 0.22), vertices=4)
        o = bpy.context.object; o.rotation_euler = (0, math.radians(90), th + math.pi); o.data.materials.append(white)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.06, location=(cx, cy, 0.25)); bpy.context.object.data.materials.append(rim)
    else:
        text('?', (cx, cy, 0.19), 0.42, grey)
    b3d.stack_camera((0, 0, 0), 6.9, az=0.0, el=90.0 - 1e-3)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 1000), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
