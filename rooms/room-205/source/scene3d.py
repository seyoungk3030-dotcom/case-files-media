"""ROOM 205 3D sprites: side view of a bicycle's drive side, true to scale (wheel radius 340 mm = 1 unit, chain pitch
12.7 mm, so a chainring's pitch radius is teeth*12.7/(2*pi) mm): back wheel with its rear cog, chainstay and seat tube,
front chainring with crank and pedal, and the chain over both. a*: the back wheel's tyre glows mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
U = 1 / 340.0   # units per mm
WX, WZ = -0.75, 1.0          # back hub
BX, BZ = WX + 420 * U * 1.0, WZ - 70 * U   # bottom bracket: chainstay 420 mm, drop 70 mm


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def rod(m, p, q, r, y=0.0):
    dx, dz = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dz)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=((p[0] + q[0]) / 2, y, (p[1] + q[1]) / 2), rotation=(0, math.atan2(dx, dz), 0))
    o = bpy.context.object; o.data.materials.append(m); [setattr(f, 'use_smooth', True) for f in o.data.polygons]; return o


def torus(m, c, R, r, y):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=(c[0], y, c[1]), rotation=(math.pi / 2, 0, 0), major_segments=96, minor_segments=16)
    o = bpy.context.object; o.data.materials.append(m); [setattr(f, 'use_smooth', True) for f in o.data.polygons]; return o


def gear(m, c, n, y):
    r = n * 12.7 / (2 * math.pi) * U
    bpy.ops.mesh.primitive_cylinder_add(radius=r * 0.93, depth=0.025, location=(c[0], y, c[1]), rotation=(math.pi / 2, 0, 0), vertices=64)
    bpy.context.object.data.materials.append(m)
    for i in range(n):
        a = 2 * math.pi * i / n
        bpy.ops.mesh.primitive_cube_add(size=1, location=(c[0] + r * math.cos(a), y, c[1] + r * math.sin(a)), rotation=(0, -a, 0))
        o = bpy.context.object; o.scale = (0.022, 0.025, 0.016); o.data.materials.append(m)
    return r


def scene(key, after):
    F, R, P = BOARDS[key]
    frame = b3d.mat('frame', (0.85, 0.2, 0.25), rough=0.3, coat=0.8); steel = b3d.mat('steel', (0.75, 0.77, 0.8), rough=0.25, metal=1.0, coat=0)
    tyre = glowm('mint', (0.2, 0.95, 0.65), 1.6) if after else b3d.mat('tyre', (0.06, 0.06, 0.07), rough=0.8, coat=0)
    chainm = b3d.mat('chain', (0.35, 0.36, 0.4), rough=0.35, metal=0.9, coat=0)
    torus(tyre, (WX, WZ), 0.95, 0.06, 0.05); torus(steel, (WX, WZ), 0.86, 0.025, 0.05)
    for i in range(16):
        a = math.pi * 2 * i / 16; rod(steel, (WX, WZ), (WX + 0.86 * math.cos(a), WZ + 0.86 * math.sin(a)), 0.007, 0.05)
    rod(frame, (WX, WZ), (BX, BZ), 0.035, 0.12); rod(frame, (BX, BZ), (BX - 0.15, BZ + 1.05), 0.045, 0.12); rod(frame, (WX, WZ), (BX - 0.14, BZ + 0.98), 0.03, 0.12)
    rr = gear(b3d.mat('cog', (0.9, 0.72, 0.2), rough=0.25, metal=1.0, coat=0), (WX, WZ), R, -0.02)
    rf = gear(steel, (BX, BZ), F, -0.02)
    for s in (1, -1): rod(chainm, (WX, WZ + s * rr), (BX, BZ + s * rf), 0.013, -0.045)
    ca = math.radians(-60); px, pz = BX + 0.5 * math.cos(ca), BZ + 0.5 * math.sin(ca)
    rod(b3d.mat('crank', (0.15, 0.15, 0.18), rough=0.3, metal=0.6, coat=0), (BX, BZ), (px, pz), 0.03, -0.09)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(px, -0.16, pz)); o = bpy.context.object; o.scale = (0.26, 0.12, 0.06)
    o.data.materials.append(b3d.mat('pedal', (0.15, 0.15, 0.18), rough=0.5, coat=0)); b3d.bevel(o, 0.02, 3)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(BX, -0.11, BZ)); bpy.context.object.data.materials.append(steel)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(WX, -0.06, WZ)); bpy.context.object.data.materials.append(steel)
    b3d.stack_camera((-0.3, 0, 1.0), 3.3, az=0.0, el=4.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((700, 620), 40); b3d.lights(3)
        t0 = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t0, 1), flush=True)
