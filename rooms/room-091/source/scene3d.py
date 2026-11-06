"""ROOM 091 3D sprites: a small warehouse floor seen from the front and above. Dark wall blocks, a wooden crate, a
mint goal square and an amber worker; a low rim marks the edge. a*: coral arrows trace the shortest push path."""
import math, os, sys, time
import bpy
import numpy as np
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def box(m, x, y, z, sx, sy, sz, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z)); o = bpy.context.object; o.scale = (sx, sy, sz); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev)
    return o


def rod(a, b, r, m):
    a, b = np.array(a, float), np.array(b, float); d = b - a; L = np.linalg.norm(d)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=tuple((a + b) / 2), vertices=16); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(tuple(d / L))); o.data.materials.append(m)


def scene(k, after):
    G = BOARDS[k]; H, W = len(G), len(G[0])
    P = lambda r, c: ((c - (W - 1) / 2), ((H - 1) / 2 - r))
    t1 = b3d.mat('t1', (0.42, 0.45, 0.52), rough=0.7, coat=0); t2 = b3d.mat('t2', (0.36, 0.39, 0.46), rough=0.7, coat=0)
    wall = b3d.mat('wall', (0.06, 0.08, 0.14), rough=0.5, coat=0.2); rim = b3d.mat('rim', (0.10, 0.13, 0.22), rough=0.5)
    crate = b3d.mat('crate', (0.72, 0.45, 0.20), rough=0.5, coat=0.2); slat = b3d.mat('slat', (0.50, 0.30, 0.12), rough=0.6)
    goal = b3d.mat('goal', (0.2, 0.85, 0.62), rough=0.4); glow(goal, (0.2, 0.85, 0.62), 0.9)
    amb = b3d.mat('amb', (0.98, 0.62, 0.12), rough=0.35); skin = b3d.mat('skin', (0.98, 0.84, 0.70), rough=0.5)
    red = b3d.mat('red', (0.95, 0.12, 0.10), rough=0.4); glow(red, (1.0, 0.15, 0.1), 0.35)
    box(rim, 0, 0, -0.12, W + 0.5, H + 0.5, 0.2, bev=0.05)
    for r in range(H):
        for c in range(W):
            x, y = P(r, c); ch = G[r][c]
            box(t1 if (r + c) % 2 == 0 else t2, x, y, 0.0, 0.97, 0.97, 0.06)
            if ch == '#': box(wall, x, y, 0.25, 0.96, 0.96, 0.5, bev=0.05)
            if ch == 'G': box(goal, x, y, 0.04, 0.8, 0.8, 0.04)
            if ch == 'B':
                box(crate, x, y, 0.3, 0.78, 0.78, 0.55, bev=0.04)
                for s in (-0.2, 0.2): box(slat, x + s, y, 0.58, 0.1, 0.7, 0.02)
            if ch == 'P':
                bpy.ops.mesh.primitive_cylinder_add(radius=0.24, depth=0.5, location=(x, y, 0.3)); bpy.context.object.data.materials.append(amb)
                bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=(x, y, 0.72)); bpy.context.object.data.materials.append(skin)
    if after:
        path = RES[k][1]
        for a, b in zip(path, path[1:]):
            (x0, y0), (x1, y1) = P(*a), P(*b); z = 0.7
            rod((x0, y0, z), (x0 + (x1 - x0) * 0.72, y0 + (y1 - y0) * 0.72, z), 0.09, red)
            d = np.array([x1 - x0, y1 - y0, 0.0]); tip = np.array([x0, y0, z]) + d * 0.78
            bpy.ops.mesh.primitive_cone_add(radius1=0.22, depth=0.34, location=tuple(tip)); o = bpy.context.object
            o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(tuple(d))); o.data.materials.append(red)
    b3d.stack_camera((0, 0.25, 0.3), W + 1.0, az=0.0, el=68.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((800, 760), 40); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
