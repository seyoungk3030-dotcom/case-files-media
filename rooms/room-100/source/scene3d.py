"""ROOM 100 3D sprites: two ropes per board lying on a dark table, seen from above, each a thick coloured tube that
passes over or under itself at every crossing, with its two loose ends pointing outward. a*: ropes that stay knotted
sit on a glowing mint disc; ropes that come undone turn grey."""
import math, os, sys, time
import bpy
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, base, crossings
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
COLS = [(0.98, 0.45, 0.35), (0.98, 0.75, 0.2), (0.35, 0.65, 1.0)]
SC = 0.43


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def rope_points(kind, ov):
    X = crossings(kind); bumps = []
    for (t1, t2, _, _), o in zip(X, ov): bumps += [(t1, 1 if o else -1), (t2, -1 if o else 1)]
    def z(t):
        v = 0
        for tc, sg in bumps:
            d = (t - tc + math.pi) % (2 * math.pi) - math.pi; v += sg * 0.55 * math.exp(-(d / 0.18) ** 2)
        return v
    ts = [2 * math.pi * i / 720 for i in range(720)]
    tstar = max(ts, key=lambda t: math.hypot(*base(kind, t)))
    pts = []
    for i in range(1, 700):
        t = tstar + 0.12 + (2 * math.pi - 0.24) * i / 700; x, y = base(kind, t); pts.append(np.array([x, y, z(t)]))
    for end, sgn in ((0, -1), (-1, 1)):
        p = pts[end]; r = p[:2] / np.linalg.norm(p[:2]); tail = []
        for j in range(1, 14): q = p + np.array([r[0], r[1], 0]) * 0.07 * j; tail.append(q)
        pts = (tail[::-1] + pts) if end == 0 else (pts + tail)
    return [p * [SC, SC, SC * 0.9] for p in pts]


def tube(pts, m, x0):
    cu = bpy.data.curves.new('r', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.085; cu.bevel_resolution = 6
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for i, p in enumerate(pts): sp.points[i].co = (p[0] + x0, p[1], p[2] + 0.35, 1)
    o = bpy.data.objects.new('r', cu); bpy.context.collection.objects.link(o); o.data.materials.append(m)


def scene(k, after):
    table = b3d.mat('table', (0.04, 0.05, 0.09), rough=0.8, coat=0); grey = b3d.mat('grey', (0.35, 0.37, 0.42), rough=0.6)
    mint = b3d.mat('mint', (0.15, 0.75, 0.5), rough=0.6, coat=0); glow(mint, (0.15, 0.75, 0.5), 0.5)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.05)); o = bpy.context.object; o.scale = (6.8, 3.5, 0.1); o.data.materials.append(table); b3d.bevel(o, 0.06)
    for i, ((kind, ov), kn) in enumerate(zip(BOARDS[k], RES[k])):
        x0 = (i - 0.5) * 3.3; m = b3d.mat(f'c{i}', COLS[i], rough=0.55, coat=0.1)
        if after and kn:
            bpy.ops.mesh.primitive_cylinder_add(radius=1.5, depth=0.04, location=(x0, 0, 0.02), vertices=96); bpy.context.object.data.materials.append(mint)
        tube(rope_points(kind, ov), grey if after and not kn else m, x0)
    b3d.stack_camera((0, 0, 0), 7.0, az=0.0, el=84.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 520), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
