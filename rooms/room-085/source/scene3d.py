"""ROOM 085 3D sprites, one small diorama per riddle (side views, front = right): A a bus pulling away with a helium
balloon tied to the floor; B the same bus with a hanging strap; C a bicycle with a string on the bottom pedal pulled
backward; D a boat holding a stone in a water tank. a*: the outcome (balloon leans forward, strap swings back, bike
rolled back, stone on the bottom and the water lower than the dashed old level), shown with amber accents."""
import math, os, sys, time
import bpy
import numpy as np
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
X90 = (math.radians(90), 0, 0)


def box(loc, scale, m, bev=0.04, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def rod(a, b, r, m):
    a, b = np.array(a, float), np.array(b, float); d = b - a; L = np.linalg.norm(d)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=tuple((a + b) / 2)); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(tuple(d / L))); o.data.materials.append(m)


def ball(p, r, m, sc=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=p, segments=48, ring_count=24); o = bpy.context.object; o.scale = sc
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def arrow(a, b, m, r=0.07):
    rod(a, b, r, m); a, b = np.array(a, float), np.array(b, float); d = (b - a) / np.linalg.norm(b - a)
    bpy.ops.mesh.primitive_cone_add(radius1=r * 2.8, depth=r * 5, location=tuple(b + d * r * 2.5)); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(tuple(d))); o.data.materials.append(m)


def glassy(name, col, a):
    m = b3d.mat(name, col, rough=0.08, coat=0.8); p = m.node_tree.nodes['Principled BSDF']; p.inputs['Alpha'].default_value = a
    try: m.surface_render_method = 'BLENDED'
    except Exception: m.blend_method = 'BLEND'
    return m


def mats():
    M = {n: b3d.mat(n, c, rough=0.35, coat=0.5) for n, c in {'bus': (0.25, 0.6, 0.95), 'dark': (0.12, 0.13, 0.17), 'hub': (0.75, 0.77, 0.8),
         'red': (0.95, 0.25, 0.3), 'str': (0.95, 0.95, 0.95), 'frame': (0.3, 0.75, 0.5), 'wood': (0.7, 0.45, 0.25), 'stone': (0.45, 0.47, 0.52),
         'skin': (0.98, 0.8, 0.65)}.items()}
    M['amb'] = b3d.mat('amb', (0.98, 0.62, 0.12), rough=0.3); q = M['amb'].node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (0.98, 0.62, 0.12, 1); q.inputs['Emission Strength'].default_value = 0.6
    M['glass'] = glassy('glass', (0.8, 0.9, 1.0), 0.15); M['water'] = glassy('water', (0.3, 0.6, 0.98), 0.45)
    return M


def wheel(x, z, r, M, w=0.18):
    bpy.ops.mesh.primitive_torus_add(location=(x, 0, z), rotation=X90, major_radius=r, minor_radius=w / 2); bpy.context.object.data.materials.append(M['dark'])
    bpy.ops.mesh.primitive_cylinder_add(radius=r * 0.35, depth=w * 0.8, location=(x, 0, z), rotation=X90); bpy.context.object.data.materials.append(M['hub'])


def bus(M):
    box((0, 0, 0.45), (4.4, 1.4, 0.1), M['bus'], 0.03); box((0, 0, 2.15), (4.4, 1.4, 0.1), M['bus'], 0.03)
    box((-2.15, 0, 1.3), (0.1, 1.4, 1.8), M['bus'], 0.03); box((2.15, 0, 1.3), (0.1, 1.4, 1.8), M['bus'], 0.03)
    box((0, 0.68, 1.3), (4.4, 0.04, 1.8), M['glass'], 0.01)
    box((2.25, -0.4, 0.75), (0.08, 0.25, 0.18), M['amb'], 0.03)
    wheel(-1.4, 0.32, 0.32, M, 0.3); wheel(1.4, 0.32, 0.32, M, 0.3)


def sA(after, M):
    bus(M); ang = math.radians(22) if after else 0
    top = (0.0 + 1.1 * math.sin(ang), 0, 0.5 + 1.1 * math.cos(ang))
    rod((0, 0, 0.5), top, 0.012, M['str']); ball((top[0] + 0.3 * math.sin(ang), 0, top[2] + 0.3 * math.cos(ang)), 0.32, M['amb'] if after else M['red'], (1, 1, 1.15))
    arrow((-1.0, -0.9, 2.7), (1.0, -0.9, 2.7), M['amb'] if not after else M['hub'], 0.08)
    b3d.stack_camera((0, 0, 1.45), 5.6, az=0.0, el=6.0)


def sB(after, M):
    bus(M); ang = math.radians(-22) if after else 0
    rod((-1.6, 0, 2.0), (1.6, 0, 2.0), 0.04, M['hub'])
    end = (1.0 * math.sin(ang), 0, 2.0 - 1.0 * math.cos(ang))
    rod((0, 0, 2.0), end, 0.05, M['amb'] if after else M['red'])
    bpy.ops.mesh.primitive_torus_add(location=(end[0] + 0.12 * math.sin(ang), 0, end[2] - 0.12 * math.cos(ang)), rotation=(math.radians(90), ang, 0), major_radius=0.14, minor_radius=0.035)
    bpy.context.object.data.materials.append(M['amb'] if after else M['red'])
    arrow((-1.0, -0.9, 2.7), (1.0, -0.9, 2.7), M['amb'] if not after else M['hub'], 0.08)
    b3d.stack_camera((0, 0, 1.45), 5.6, az=0.0, el=6.0)


def sC(after, M):
    dx = -0.9 if after else 0.0; R = 0.62
    box((0, 0, -0.03), (6.0, 1.0, 0.06), M['hub'], 0.01)
    wheel(-1.05 + dx, R, R, M, 0.1); wheel(1.05 + dx, R, R, M, 0.1)
    bb = (0.0 + dx, 0, R); seat = (-0.3 + dx, 0, 1.55); head = (0.85 + dx, 0, 1.45)
    for a, b in ((bb, seat), (bb, head), (seat, head), (bb, (-1.05 + dx, 0, R)), (seat, (-1.05 + dx, 0, R)), (head, (1.05 + dx, 0, R))):
        rod(a, b, 0.045, M['frame'])
    box((seat[0], 0, seat[2] + 0.06), (0.4, 0.14, 0.08), M['dark'], 0.03); rod(head, (head[0] + 0.15, 0, head[2] + 0.15), 0.035, M['dark'])
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.06, location=(bb[0], -0.08, R), rotation=X90); bpy.context.object.data.materials.append(M['hub'])
    pedal = (bb[0], -0.1, R - 0.32); rod((bb[0], -0.1, R), pedal, 0.03, M['hub']); box(pedal, (0.22, 0.12, 0.05), M['dark'], 0.02)
    rod(pedal, (-2.3 + dx, -0.1, R - 0.32), 0.015, M['str'])
    ball((-2.4 + dx, -0.1, R - 0.32), 0.12, M['skin'])
    if not after: arrow((-2.6, -0.3, 0.05), (-3.0, -0.3, 0.05), M['amb'], 0.06)
    else: arrow((1.6, -0.3, 1.9), (0.6, -0.3, 1.9), M['amb'], 0.07)
    b3d.stack_camera((0, 0, 0.9), 6.4, az=0.0, el=6.0)


def sD(after, M):
    W, H = 3.6, 1.8; lvl0, lvl = 1.0, (0.88 if after else 1.0)
    box((0, 0, H / 2), (W, 1.2, H), M['glass'], 0.03); box((0, 0, lvl / 2), (W - 0.06, 1.14, lvl), M['water'], 0.02)
    box((0, 0, -0.04), (W + 0.15, 1.35, 0.08), M['dark'], 0.02)
    if after:
        for i in range(8): box((-W / 2 - 0.1 + i * 0.25, -0.62, lvl0), (0.14, 0.02, 0.03), M['amb'], 0.005)
    bz = lvl + (0.1 if not after else 0.18)
    box((-0.2, 0, bz), (1.4, 0.7, 0.2), M['wood'], 0.08); box((-0.2, 0, bz + 0.2), (1.4, 0.7, 0.06), M['wood'], 0.03)
    ball((-0.2, 0, bz + 0.38), 0.24, M['stone'], (1.2, 1, 0.9)) if not after else ball((0.9, 0, 0.2), 0.24, M['stone'], (1.2, 1, 0.9))
    if not after: arrow((0.25, -0.3, bz + 0.55), (0.95, -0.3, bz + 0.2), M['amb'], 0.05)
    b3d.stack_camera((0, 0, 0.95), 4.6, az=0.0, el=8.0)


only = sys.argv[1:]
for k, f in zip('ABCD', (sA, sB, sC, sD)):
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 620), 40); b3d.lights(6)
        t = time.time(); f(after, mats()); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
