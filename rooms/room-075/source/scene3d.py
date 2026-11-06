"""ROOM 075 3D sprites: a symmetric city bus on a road seen from the side, a numbered bus stop at each end.
Doors (front and middle) are drawn only when the bus's right side faces us. a*: an amber arrow along the road towards
the stop it reaches, that stop's sign glowing."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
X90 = (math.radians(90), 0, 0)


def label(s, x, z, size, m, y=-0.6):
    bpy.ops.object.text_add(location=(x, y, z), rotation=X90); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def box(loc, scale, m, bev=0.03):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def glow(m, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
    q.inputs['Emission Strength'].default_value = s; return m


def stop(x, n, M, hot):
    box((x, 0.5, 0.75), (0.07, 0.07, 1.5), M['pole'], 0.01)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=0.06, location=(x, 0.43, 1.62), rotation=X90)
    bpy.context.object.data.materials.append(M['amber'] if hot else M['sign'])
    label(str(n), x, 1.62, 0.6, M['ink'], y=0.39)


def scene(k, after):
    doors, l, r = BOARDS[k]
    M = {'pole': b3d.mat('pole', (0.55, 0.58, 0.64), rough=0.3, metal=0.6), 'sign': b3d.mat('sign', (0.92, 0.94, 0.97), rough=0.3, coat=0.5),
         'amber': glow(b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3), 0.8), 'ink': b3d.mat('ink', (0.06, 0.09, 0.18), rough=0.4)}
    body = b3d.mat('body', {'A': (0.20, 0.72, 0.45), 'B': (0.95, 0.42, 0.35), 'C': (0.30, 0.55, 0.95), 'D': (0.75, 0.45, 0.90)}[k], rough=0.3, coat=0.7); win = b3d.mat('win', (0.10, 0.14, 0.22), rough=0.1, coat=0.8)
    door = b3d.mat('door', (0.12, 0.16, 0.24), rough=0.15, coat=0.8); frame = b3d.mat('frame', (0.85, 0.87, 0.9), rough=0.3)
    tyre = b3d.mat('tyre', (0.05, 0.05, 0.06), rough=0.7); hub = b3d.mat('hub', (0.7, 0.72, 0.76), rough=0.3, metal=0.6)
    road = b3d.mat('road', (0.20, 0.21, 0.25), rough=0.85, coat=0); line = b3d.mat('line', (0.95, 0.85, 0.3), rough=0.6, coat=0)
    box((0, 0.2, -0.05), (8.4, 1.6, 0.1), road, 0.01)
    for i in range(-3, 4): box((i * 1.2, -0.55, 0.002), (0.6, 0.06, 0.004), line, 0.002)
    L, H = 4.2, 1.25
    box((0, 0, 0.25 + H / 2), (L, 1.0, H), body, 0.16)
    wins = [-1.5, -0.9, -0.3, 0.3, 0.9, 1.5]
    if doors:   # Korean city bus: front door at the front end (our right), middle door
        dpos = [1.7, -0.15]; wins = [w for w in wins if min(abs(w - d) for d in dpos) > 0.45]
        for d in dpos:
            box((d, -0.505, 0.25 + 0.55), (0.5, 0.02, 1.02), frame, 0.01); box((d, -0.515, 0.25 + 0.55), (0.42, 0.02, 0.96), door, 0.01)
            box((d, -0.525, 0.25 + 0.55), (0.02, 0.02, 0.96), frame, 0.002)
    for w in wins: box((w, -0.505, 0.25 + 0.82), (0.5, 0.02, 0.45), win, 0.03)
    for wx in (-1.35, 1.35):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.2, location=(wx, -0.45, 0.3), rotation=X90); bpy.context.object.data.materials.append(tyre)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.21, location=(wx, -0.46, 0.3), rotation=X90); bpy.context.object.data.materials.append(hub)
    goal = r if doors else l
    stop(-3.55, l, M, after and goal == l); stop(3.55, r, M, after and goal == r)
    if after:
        sgn = 1 if doors else -1
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.8, location=(sgn * 2.75, -0.7, 0.8), rotation=(0, math.radians(90), 0))
        bpy.context.object.data.materials.append(M['amber'])
        bpy.ops.mesh.primitive_cone_add(radius1=0.16, depth=0.35, location=(sgn * 3.25, -0.7, 0.8), rotation=(0, math.radians(90 * sgn), 0))
        bpy.context.object.data.materials.append(M['amber'])
    b3d.stack_camera((0, 0, 0.95), 8.2, az=0.0, el=6.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1200, 460), 40); b3d.lights(8)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
