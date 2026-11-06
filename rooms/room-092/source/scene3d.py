"""ROOM 092 3D sprites: a brass music-box drum with silver pins, a steel comb on top whose teeth are numbered 1-9 on a
plate behind, a wooden case, and a big amber arrow in front of the drum's left end showing which way the front turns. a*: the first
three notes are marked 1 2 3 next to their pins; the third pin and its tooth glow coral."""
import math, os, sys, time
import bpy
import numpy as np
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, order
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
R0 = 1.0; TX = lambda t: (t - 5) * 0.5; Y90 = (0, math.radians(90), 0)


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m, rot=(math.radians(90), 0, 0)):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def rod(a, b, r, m):
    a, b = np.array(a, float), np.array(b, float); d = b - a; L = np.linalg.norm(d)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=tuple((a + b) / 2), vertices=16); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(tuple(d / L))); o.data.materials.append(m)
    return o


def box(m, x, y, z, sx, sy, sz, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z)); o = bpy.context.object; o.scale = (sx, sy, sz); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev)


def scene(k, after):
    d, pins = BOARDS[k]; ordr = order(k)
    brass = b3d.mat('brass', (0.62, 0.42, 0.14), rough=0.5, metal=0.5, coat=0.1); steel = b3d.mat('steel', (0.8, 0.82, 0.86), rough=0.25, metal=0.9)
    wood = b3d.mat('wood', (0.30, 0.17, 0.09), rough=0.5, coat=0.3); plate = b3d.mat('plate', (0.08, 0.1, 0.16), rough=0.6, coat=0)
    ink = b3d.mat('ink', (0.95, 0.96, 0.98), rough=0.5, coat=0); glow(ink, (0.95, 0.96, 0.98), 0.3)
    amb = b3d.mat('amb', (0.98, 0.62, 0.12), rough=0.3); glow(amb, (0.98, 0.62, 0.12), 0.8)
    red = b3d.mat('red', (0.95, 0.12, 0.1), rough=0.3); glow(red, (1.0, 0.2, 0.15), 0.5)
    mint = b3d.mat('mint', (0.1, 0.8, 0.5), rough=0.3); glow(mint, (0.2, 0.9, 0.6), 0.4)
    box(wood, 0, 0.3, -1.45, 6.6, 3.0, 0.5, bev=0.06)
    for sx in (-2.95, 2.95): box(wood, sx, 0.3, -0.6, 0.3, 1.2, 1.5, bev=0.04)
    bpy.ops.mesh.primitive_cylinder_add(radius=R0, depth=5.0, location=(0, 0, 0), rotation=Y90, vertices=96); bpy.context.object.data.materials.append(brass)
    rod((-2.95, 0, 0), (2.95, 0, 0), 0.12, steel)
    box(steel, 0, 0.55, R0 + 0.28, 4.9, 0.6, 0.12, bev=0.02)
    box(plate, 0, 0.95, R0 + 0.95, 4.9, 0.08, 0.9, bev=0.03)
    third = ordr[2]; pinm = b3d.mat('pin', (0.05, 0.07, 0.12), rough=0.3, metal=0.3)
    for t in range(1, 10):
        x = TX(t); m = red if after and t == third else steel
        box(m, x, 0.18, R0 + 0.16, 0.28, 0.75, 0.06)
        text(str(t), (x, 0.9, R0 + 0.95), 0.5, red if after and t == third else ink)
    for t, a in pins:
        th = math.radians(a); p = np.array([TX(t), -math.sin(th), math.cos(th)])
        m = red if after and t == third else (mint if after and t in ordr[:2] else pinm)
        rod(tuple(p * [1, R0 - 0.05, R0 - 0.05]), tuple(p * [1, R0 + 0.2, R0 + 0.2]), 0.09, m)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, location=tuple(p * [1, R0 + 0.2, R0 + 0.2])); bpy.context.object.data.materials.append(m)
        if after and t in ordr[:3]:
            text(str(ordr.index(t) + 1), (TX(t) + 0.32, -1.3, math.cos(th) * 1.1), 0.42, m)
    z0, z1 = (-0.85, 0.85) if d == 'up' else (0.85, -0.85)
    rod((-2.62, -1.25, z0), (-2.62, -1.25, z1 * 0.72), 0.09, amb)
    bpy.ops.mesh.primitive_cone_add(radius1=0.26, depth=0.45, location=(-2.62, -1.25, z1), rotation=(0 if d == 'up' else math.pi, 0, 0)); bpy.context.object.data.materials.append(amb)
    b3d.stack_camera((0, 0, 0.35), 7.3, az=0.0, el=14.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1100, 700), 40); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
