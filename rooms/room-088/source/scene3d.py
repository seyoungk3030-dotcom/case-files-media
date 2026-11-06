"""ROOM 088 3D sprites: wheels of different sizes on a board, seen face on, joined by rubber belts (open belts run
along the top and bottom tangents, crossed belts form an X). Wheel 1 has an amber clockwise arrow. a*: every wheel has
an arrow, amber for clockwise, blue for counter-clockwise."""
import math, os, sys, time
import bpy
import numpy as np
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, dirs
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
X90 = (math.radians(90), 0, 0)


def rod(a, b, r, m):
    a, b = np.array(a, float), np.array(b, float); d = b - a; L = np.linalg.norm(d)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=tuple((a + b) / 2), vertices=16); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(tuple(d / L))); o.data.materials.append(m)


def curved_arrow(x, z, r, cw, m, y=-0.32):
    pts = []
    for i in range(14):
        a = math.radians(120 - (i * 17 if cw else -i * 17)); pts.append((x + r * math.cos(a), y, z + r * math.sin(a)))
    for a, b in zip(pts, pts[1:]): rod(a, b, 0.045, m)
    a, b = np.array(pts[-2]), np.array(pts[-1]); d = (b - a) / np.linalg.norm(b - a)
    bpy.ops.mesh.primitive_cone_add(radius1=0.12, depth=0.25, location=tuple(b + d * 0.12)); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(tuple(d))); o.data.materials.append(m)


def tangents(c1, r1, c2, r2, crossed):
    c1, c2 = np.array(c1), np.array(c2); d = c2 - c1; L = np.linalg.norm(d); u = d / L; n = np.array([-u[1], u[0]])
    if not crossed:
        s = (r1 - r2) / L; out = []
        for sg in (1, -1):
            nn = s * u + sg * math.sqrt(1 - s * s) * n; out.append((c1 + r1 * nn, c2 + r2 * nn))
        return out
    s = (r1 + r2) / L; out = []
    for sg in (1, -1):
        nn = s * u + sg * math.sqrt(1 - s * s) * n; out.append((c1 + r1 * nn, c2 - r2 * nn))
    return out


def scene(k, after):
    belts, sizes = BOARDS[k]; d = dirs(belts)
    wood = b3d.mat('wood', (0.08, 0.1, 0.16), rough=0.6, coat=0.1); wheel = b3d.mat('wheel', (0.85, 0.87, 0.92), rough=0.3, metal=0.5)
    hub = b3d.mat('hub', (0.98, 0.45, 0.4), rough=0.3); belt = b3d.mat('belt', (0.95, 0.45, 0.35), rough=0.5, coat=0)
    amb = b3d.mat('amb', (0.98, 0.62, 0.12), rough=0.3); blu = b3d.mat('blu', (0.25, 0.6, 1.0), rough=0.3)
    for m, c in ((amb, (0.98, 0.62, 0.12)), (blu, (0.25, 0.6, 1.0))):
        q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = 0.7
    xs = [0.0]
    for a, b in zip(sizes, sizes[1:]): xs.append(xs[-1] + a + b + 0.75)
    off = (xs[0] - sizes[0] + xs[-1] + sizes[-1]) / 2; xs = [x - off for x in xs]
    zs = [0.0 if i % 2 == 0 else 0.35 for i in range(len(sizes))]
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.3, 0)); o = bpy.context.object; o.scale = (xs[-1] - xs[0] + 2 * max(sizes) + 0.8, 0.1, 2 * max(sizes) + 1.2); o.data.materials.append(wood)
    for x, z, r in zip(xs, zs, sizes):
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=0.22, location=(x, 0, z), rotation=X90, vertices=64); bpy.context.object.data.materials.append(wheel)
        bpy.ops.mesh.primitive_torus_add(location=(x, -0.02, z), rotation=X90, major_radius=r - 0.04, minor_radius=0.05); bpy.context.object.data.materials.append(belt)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.3, location=(x, -0.02, z), rotation=X90); bpy.context.object.data.materials.append(hub)
    for i, b in enumerate(belts):
        for p, q in tangents((xs[i], zs[i]), sizes[i], (xs[i + 1], zs[i + 1]), sizes[i + 1], b == 'X'):
            yy = -0.05 if b == 'O' else (-0.05 if p[1] > zs[i] else -0.16)
            rod((p[0], yy, p[1]), (q[0], yy, q[1]), 0.06, belt)
    for i, (x, z, r) in enumerate(zip(xs, zs, sizes)):
        if i == 0 or after: curved_arrow(x, z, r * 0.6, d[i] > 0, amb if d[i] > 0 else blu)
    b3d.stack_camera((0, 0, 0.15), xs[-1] - xs[0] + 2 * max(sizes) + 1.0, az=0.0, el=0.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1300, 380), 40); b3d.lights(6)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
