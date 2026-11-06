"""ROOM 096 3D sprites: three side-by-side ball tracks per board (same start height, same finish), coloured rails on
thin posts, a steel ball at each start and a chequered flag at each finish; numbered plates under the tracks. a*: the
balls are shown where they are at the moment the winner finishes, and the winner glows with a '1등' sign."""
import math, os, sys, time
import bpy
import numpy as np
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, L, H, G, y
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
GAP = 2.75; RB = 0.11


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.03; t.data.materials.append(m)


def rod(a, b, r, m):
    a, b = np.array(a, float), np.array(b, float); d = b - a; L_ = np.linalg.norm(d)
    if L_ < 1e-6: return
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L_, location=tuple((a + b) / 2), vertices=12); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(tuple(d / L_))); o.data.materials.append(m)


def x_at(a, b, T, n=20000):
    t = 0; px, py = 0, y(a, b, 0)
    for i in range(1, n + 1):
        x = L * i / n; yy = y(a, b, x); ym = (yy + py) / 2
        t += math.hypot(x - px, yy - py) / math.sqrt(max(1e-12, 2 * G * (H - ym))); px, py = x, yy
        if t >= T: return x
    return L


def scene(k, after):
    cols = [(0.98, 0.42, 0.38), (0.99, 0.72, 0.18), (0.30, 0.60, 1.0)]
    floor = b3d.mat('floor', (0.07, 0.09, 0.15), rough=0.6); post = b3d.mat('post', (0.35, 0.38, 0.45), rough=0.4, metal=0.6)
    steel = b3d.mat('steel', (0.85, 0.87, 0.9), rough=0.15, metal=1.0); ink = b3d.mat('ink', (0.95, 0.96, 0.98), rough=0.5); glow(ink, (0.95, 0.96, 0.98), 0.4)
    gold = b3d.mat('gold', (1.0, 0.75, 0.15), rough=0.2, metal=0.6); glow(gold, (1.0, 0.7, 0.1), 1.2)
    flagw = b3d.mat('fw', (0.95, 0.95, 0.95), rough=0.5); flagk = b3d.mat('fk', (0.05, 0.05, 0.05), rough=0.5)
    times = [t for t, _ in RES[k]]; win = min(range(3), key=lambda i: times[i])
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.95)); o = bpy.context.object; o.scale = (3 * GAP + 0.4, 1.6, 0.2); o.data.materials.append(floor); b3d.bevel(o, 0.05)
    for i, (a, b) in enumerate(BOARDS[k]):
        ox = (i - 1) * GAP - L / 2; m = b3d.mat(f't{i}', cols[i], rough=0.35); glow(m, cols[i], 0.25)
        pts = [(ox + L * j / 60, 0, y(a, b, L * j / 60)) for j in range(61)]
        for p, q in zip(pts, pts[1:]): rod(p, q, 0.05, m)
        for j in (0, 15, 30, 45, 60): rod((pts[j][0], 0.12, -0.85), (pts[j][0], 0.12, pts[j][2] - 0.05), 0.025, post)
        rod((ox + L, 0, 0), (ox + L, 0, 0.75), 0.02, post)
        for r_ in range(2):
            for c_ in range(3):
                bpy.ops.mesh.primitive_cube_add(size=0.1, location=(ox + L + 0.07 + c_ * 0.1, 0, 0.7 - r_ * 0.1)); bpy.context.object.data.materials.append(flagw if (r_ + c_) % 2 else flagk)
        if not after: bx = 0.0
        else: bx = L if i == win else x_at(a, b, times[win])
        by = y(a, b, bx); sl = (y(a, b, min(L, bx + 1e-3)) - y(a, b, max(0, bx - 1e-3))) / 2e-3; nz = 1 / math.sqrt(1 + sl * sl)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=RB, location=(ox + bx - sl * nz * (RB + 0.05), 0, by + nz * (RB + 0.05)))
        bpy.context.object.data.materials.append(gold if after and i == win else steel)
        text(str(i + 1), (ox + L / 2, -0.85, -0.62), 0.42, ink)
        if after and i == win: text('1등', (ox + L - 0.1, -0.2, 1.05), 0.36, gold)
    b3d.stack_camera((0, 0, 0.25), 3 * GAP + 0.5, az=0.0, el=6.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1300, 420), 40); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
