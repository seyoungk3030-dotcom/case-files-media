"""ROOM 159 3D sprites: a toy railway seen from the front. The exit tunnel is on the left, a turntable in the middle
with a short dead-end side track going back to a red buffer, and a train of 5 numbered cars on the right (starred cars
carry a yellow star on the roof). p*: the start. a*: all 5 cars lined up left of the turntable in the order they went
through the exit (front = nearest the tunnel); the 3rd car glows mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, ORDER
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
EL = 30.0; TT = -0.5; L = 0.86; P = 1.0
COLS = [(0.18, 0.42, 0.9), (0.9, 0.36, 0.3), (0.55, 0.3, 0.85), (0.95, 0.6, 0.15), (0.92, 0.45, 0.68)]


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m, rot=None):
    bpy.ops.object.text_add(location=loc, rotation=rot or (math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def box(loc, scale, m, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev)
    return o


def rails(x0, x1, y0, y1, M):
    dx, dy = x1 - x0, y1 - y0; ln = math.hypot(dx, dy); ux, uy = dx / ln, dy / ln; nx, ny = -uy, ux; ang = math.atan2(dy, dx)
    n = int(ln / 0.32)
    for i in range(n + 1):
        t = i * ln / n; o = box((x0 + ux * t, y0 + uy * t, 0.02), (0.1, 0.62, 0.04), M['tie']); o.rotation_euler = (0, 0, ang)
    for s in (-0.22, 0.22):
        o = box((x0 + dx / 2 + nx * s, y0 + dy / 2 + ny * s, 0.07), (ln, 0.05, 0.06), M['rail']); o.rotation_euler = (0, 0, ang)


def car(x, num, star, body, M, y=0.0):
    box((x, y, 0.42), (L, 0.62, 0.46), body, 0.06); box((x, y, 0.68), (L - 0.08, 0.66, 0.06), M['roof'], 0.02)
    for dx in (-0.26, 0.26):
        for dy in (-0.3, 0.3):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.06, location=(x + dx, y + dy, 0.16), rotation=(math.pi / 2, 0, 0), vertices=20)
            bpy.context.object.data.materials.append(M['wheel'])
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.02, location=(x, y - 0.32, 0.43), rotation=(math.pi / 2, 0, 0), vertices=32)
    bpy.context.object.data.materials.append(M['plate'])
    text(str(num), (x, y - 0.335, 0.43), 0.4, M['ink'])
    if star:
        o = b3d.star(M['star'], x, 0.71, r=0.2, depth=0.08); o.location.y = y


def scene(k, after):
    M = {'ground': b3d.mat('ground', (0.12, 0.13, 0.15), rough=0.9, coat=0), 'tie': b3d.mat('tie', (0.32, 0.2, 0.12), rough=0.8, coat=0),
         'rail': b3d.mat('rail', (0.75, 0.76, 0.8), rough=0.3, metal=1.0, coat=0), 'wheel': b3d.mat('wheel', (0.08, 0.08, 0.09), rough=0.5, coat=0),
         'roof': b3d.mat('roof', (0.9, 0.9, 0.92), rough=0.4, coat=0), 'plate': b3d.mat('plate', (0.97, 0.97, 0.97), rough=0.4, coat=0),
         'ink': b3d.mat('ink', (0.06, 0.07, 0.1), rough=0.8, coat=0), 'star': b3d.mat('star', (1.0, 0.82, 0.15), rough=0.3, coat=0),
         'tt': b3d.mat('tt', (0.42, 0.44, 0.48), rough=0.4, metal=0.6, coat=0), 'buf': b3d.mat('buf', (0.85, 0.15, 0.12), rough=0.4, coat=0),
         'stone': b3d.mat('stone', (0.35, 0.32, 0.3), rough=0.9, coat=0), 'hole': b3d.mat('hole', (0.01, 0.01, 0.01), rough=1, coat=0),
         'yel': b3d.mat('yel', (0.98, 0.85, 0.3), rough=0.5, coat=0)}
    glow(M['star'], (1.0, 0.8, 0.1), 0.8); glow(M['yel'], (0.98, 0.85, 0.3), 0.6)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.0)
    bodies = [b3d.mat(f'b{i}', c, rough=0.35, coat=0.3) for i, c in enumerate(COLS)]
    box((-0.35, 0.6, -0.06), (12.4, 3.4, 0.1), M['ground'], 0.04)
    rails(-6.2, 5.4, 0, 0, M); rails(TT, TT, 0.55, 2.3, M)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.56, depth=0.06, location=(TT, 0, 0.06), vertices=48); bpy.context.object.data.materials.append(M['tt'])
    box((TT, 2.35, 0.2), (0.7, 0.16, 0.3), M['buf'], 0.03)
    # exit sign at the left end: a post with a yellow board '← 출구'
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=1.3, location=(-5.9, 0.75, 0.65), vertices=16); bpy.context.object.data.materials.append(M['stone'])
    box((-5.9, 0.7, 1.35), (1.5, 0.08, 0.55), M['yel'], 0.04)
    text('← 출구', (-5.9, 0.65, 1.35), 0.36, M['ink'])
    cars = BOARDS[k]; col = {n: bodies[i] for i, (n, s) in enumerate(cars)}; st = dict(cars)
    if not after:
        for i, (n, s) in enumerate(cars): car(TT + 1.15 + i * P, n, s, col[n], M)
    else:
        for i, n in enumerate(ORDER[k]): car(-5.45 + i * P, n, st[n], mint if i == 2 else col[n], M)
    b3d.stack_camera((-0.35, 0.6, 0.6), 12.8, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1200, 400), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
