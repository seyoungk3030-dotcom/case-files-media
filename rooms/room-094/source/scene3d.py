"""ROOM 094 3D sprites: a pool table seen from above, wooden rails with a white diamond at every unit, six black
pockets, and a white cue ball on the bottom rail with an amber arrow showing the 45-degree shot. a*: the ball's path
is drawn in coral with a mint dot at each cushion bounce."""
import math, os, sys, time
import bpy
import numpy as np
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
U = 0.62


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def box(m, x, y, z, sx, sy, sz, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z)); o = bpy.context.object; o.scale = (sx, sy, sz); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev)


def rod(a, b, r, m):
    a, b = np.array(a, float), np.array(b, float); d = b - a; L = np.linalg.norm(d)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=tuple((a + b) / 2), vertices=16); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(tuple(d / L))); o.data.materials.append(m)


def scene(k, after):
    W, H, x0, dx = BOARDS[k]; nb, pk, path = RES[k]
    P = lambda x, y: ((x - W / 2) * U, (y - H / 2) * U)
    felt = b3d.mat('felt', (0.02, 0.32, 0.30), rough=0.9, coat=0); wood = b3d.mat('wood', (0.30, 0.15, 0.07), rough=0.45, coat=0.4)
    dia = b3d.mat('dia', (0.95, 0.95, 0.9), rough=0.3); glow(dia, (0.95, 0.95, 0.9), 0.4)
    hole = b3d.mat('hole', (0.0, 0.0, 0.0), rough=0.9, coat=0); ball = b3d.mat('ball', (0.97, 0.97, 0.95), rough=0.15, coat=1.0)
    amb = b3d.mat('amb', (0.98, 0.62, 0.12), rough=0.3); glow(amb, (0.98, 0.62, 0.12), 0.6)
    red = b3d.mat('red', (0.95, 0.15, 0.12), rough=0.3); glow(red, (1.0, 0.2, 0.15), 0.6)
    mint = b3d.mat('mint', (0.2, 0.9, 0.62), rough=0.3); glow(mint, (0.2, 0.9, 0.62), 0.8)
    w, h = W * U, H * U; R = 0.55
    box(felt, 0, 0, -0.05, w + 0.1, h + 0.1, 0.1)
    box(wood, 0, h / 2 + R / 2, 0.08, w + 2 * R, R, 0.3, bev=0.05); box(wood, 0, -h / 2 - R / 2, 0.08, w + 2 * R, R, 0.3, bev=0.05)
    box(wood, w / 2 + R / 2, 0, 0.08, R, h + 2 * R, 0.3, bev=0.05); box(wood, -w / 2 - R / 2, 0, 0.08, R, h + 2 * R, 0.3, bev=0.05)
    for i in range(1, W):
        if i == W // 2: continue
        x = (i - W / 2) * U
        for y in (h / 2 + R / 2, -h / 2 - R / 2):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.04, location=(x, y, 0.24), vertices=4); bpy.context.object.data.materials.append(dia)
    for j in range(1, H):
        y = (j - H / 2) * U
        for x in (w / 2 + R / 2, -w / 2 - R / 2):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.04, location=(x, y, 0.24), vertices=4); bpy.context.object.data.materials.append(dia)
    for (px, py) in ((0, 0), (W // 2, 0), (W, 0), (W, H), (W // 2, H), (0, H)):
        x, y = P(px, py); bpy.ops.mesh.primitive_cylinder_add(radius=0.24, depth=0.1, location=(x, y, 0.25), vertices=48); bpy.context.object.data.materials.append(hole)
    bx, by = P(x0, 0); by += 0.18
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.17, location=(bx, by, 0.17)); bpy.context.object.data.materials.append(ball)
    if not after:
        e = np.array([bx + dx * 0.9, by + 0.9, 0.17]); rod((bx + dx * 0.2, by + 0.2, 0.17), tuple(e), 0.05, amb)
        d = np.array([dx, 1, 0.0]) / math.sqrt(2)
        bpy.ops.mesh.primitive_cone_add(radius1=0.14, depth=0.28, location=tuple(e + d * 0.12)); o = bpy.context.object
        o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(tuple(d))); o.data.materials.append(amb)
    else:
        pts = [P(*p) for p in path]
        for a, b in zip(pts, pts[1:]): rod((a[0], a[1], 0.12), (b[0], b[1], 0.12), 0.045, red)
        for i in range(1, len(path) - 1):
            (ax, ay), (bx2, by2), (cx, cy) = path[i - 1], path[i], path[i + 1]
            if (bx2 - ax, by2 - ay) != (cx - bx2, cy - by2):
                x, y = P(bx2, by2); bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(x, y, 0.14)); bpy.context.object.data.materials.append(mint)
    b3d.stack_camera((0, 0, 0), 12 * U + 2 * R + 0.5, az=0.0, el=70.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 620), 40); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
