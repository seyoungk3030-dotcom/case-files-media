"""ROOM 197 3D sprites, side view: A bicycle wheel, B car tyre (with a bit of the car), C wooden cart wheel, D crawler track.
Each rolls to the right on a road strip; a glowing coral sticker marks the spot asked about.
a*: same scene plus a mint arrow from the sticker whose length is the sticker's ground speed (none when it is 0)."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def box(m, loc, sc, bev=0.06, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m); b3d.bevel(o, bev, 4); return o


def cyl(m, r, depth, loc, rot=(math.pi / 2, 0, 0), smooth=True, verts=64):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=verts); o = bpy.context.object
    o.data.materials.append(m)
    if smooth: bpy.ops.object.shade_smooth()
    return o


def torus(m, R, r, loc):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=(math.pi / 2, 0, 0), major_segments=96, minor_segments=24)
    o = bpy.context.object; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def rod(m, p, q, r):
    dx, dz = q[0] - p[0], q[2] - p[2]; L = math.hypot(dx, dz)
    return cyl(m, r, L, ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2, (p[2] + q[2]) / 2), (0, math.atan2(dx, dz), 0), verts=16)


def sticker(loc):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.13, location=loc); o = bpy.context.object
    o.data.materials.append(glowm('stk', (1.0, 0.22, 0.16), 0.9, rough=0.3)); bpy.ops.object.shade_smooth()


def arrow(base, length, m):
    if length <= 0: return
    shaft = max(length - 0.3, 0.05)
    cyl(m, 0.06, shaft, (base[0] + shaft / 2, base[1], base[2]), (0, math.pi / 2, 0), verts=24)
    bpy.ops.mesh.primitive_cone_add(radius1=0.16, radius2=0, depth=0.3, location=(base[0] + shaft + 0.15, base[1], base[2]), rotation=(0, math.pi / 2, 0))
    bpy.context.object.data.materials.append(m)


rubber = lambda: b3d.mat('tyre', (0.05, 0.05, 0.06), rough=0.7, coat=0)
steel = lambda: b3d.mat('steel', (0.8, 0.82, 0.86), rough=0.2, metal=1.0, coat=0)


def bike():
    t, s = rubber(), steel(); frame = b3d.mat('frame', (0.15, 0.45, 0.9), rough=0.25, coat=0.8)
    torus(t, 0.93, 0.07, (0, 0, 1.0)); torus(s, 0.84, 0.035, (0, 0, 1.0)); cyl(s, 0.1, 0.22, (0, 0, 1.0))
    for i in range(16):
        a = 2 * math.pi * i / 16; rod(s, (0, 0, 1.0), (0.84 * math.cos(a), 0, 1.0 + 0.84 * math.sin(a)), 0.012)
    for y in (-0.12, 0.12): rod(frame, (0, y, 1.0), (-0.55, y, 2.15), 0.04)
    rod(frame, (-0.55, 0, 2.15), (-1.6, 0, 2.05), 0.05); rod(frame, (-0.55, 0, 2.15), (-0.35, 0, 2.3), 0.04)
    return (0, -0.05, 2.0), 'top'


def car():
    t, s = rubber(), steel(); body = b3d.mat('body', (0.85, 0.2, 0.18), rough=0.25, coat=0.8)
    cyl(t, 1.0, 0.55, (0, 0, 1.0)); b3d.bevel(bpy.context.object, 0.12, 6)
    cyl(b3d.mat('rimm', (0.62, 0.64, 0.68), rough=0.55, metal=0.6, coat=0), 0.58, 0.6, (0, 0, 1.0))
    for i in range(5):
        a = 2 * math.pi * i / 5; cyl(t, 0.06, 0.64, (0.3 * math.cos(a), 0, 1.0 + 0.3 * math.sin(a)), verts=16)
    box(body, (-0.2, 0.55, 1.75), (3.0, 0.4, 1.1), 0.15)
    box(b3d.mat('dark', (0.04, 0.04, 0.05), rough=0.8, coat=0), (0, 0.33, 1.15), (2.3, 0.1, 1.3), 0.4)
    return (0, -0.29, 0.06), 'bottom'


def cart():
    wood = b3d.mat('wood', (0.55, 0.33, 0.16), rough=0.6, coat=0.2); dwood = b3d.mat('dwood', (0.36, 0.2, 0.09), rough=0.6, coat=0.2)
    s = steel()
    torus(b3d.mat('iron', (0.2, 0.2, 0.22), rough=0.4, metal=0.8, coat=0), 0.95, 0.05, (0, 0, 1.0))
    torus(wood, 0.86, 0.08, (0, 0, 1.0))
    for i in range(8):
        a = 2 * math.pi * i / 8; rod(wood, (0, 0, 1.0), (0.82 * math.cos(a), 0, 1.0 + 0.82 * math.sin(a)), 0.05)
    cyl(dwood, 0.2, 0.36, (0, 0, 1.0)); cyl(s, 0.08, 0.4, (0, 0, 1.0))
    box(wood, (-0.3, 0.5, 2.15), (3.0, 0.5, 0.2), 0.04)
    box(dwood, (0, 0.35, 1.55), (0.16, 0.12, 1.1), 0.03)
    for x in (-1.6, 1.0): box(dwood, (x, 0.5, 2.45), (0.12, 0.5, 0.45), 0.03)
    return (0, -0.22, 1.0), 'hub'


def crawler():
    t, s = rubber(), steel(); body = b3d.mat('body', (0.95, 0.7, 0.12), rough=0.3, coat=0.7)
    rr, cx = 0.5, 1.15
    for x in (-cx, cx): cyl(s, rr - 0.1, 0.5, (x, 0, rr))
    for x in (-0.4, 0.4): cyl(s, 0.28, 0.46, (x, 0, 0.3))
    # links along a stadium path: top run, right half circle, bottom run, left half circle
    L = 2 * (2 * cx) + 2 * math.pi * rr; n = 46
    for i in range(n):
        d = L * i / n
        if d < 2 * cx: x, z, a = -cx + d, 2 * rr, 0.0
        elif d < 2 * cx + math.pi * rr: th = (d - 2 * cx) / rr; x, z, a = cx + rr * math.sin(th), rr + rr * math.cos(th), th
        elif d < 4 * cx + math.pi * rr: x, z, a = cx - (d - 2 * cx - math.pi * rr), 0.0, math.pi
        else: th = (d - 4 * cx - math.pi * rr) / rr; x, z, a = -cx - rr * math.sin(th), rr - rr * math.cos(th), math.pi + th
        box(t, (x, 0, z + 0.04 * math.cos(a) * 0 ), (0.13, 0.56, 0.08), 0.02, rot=(0, a, 0))
    box(body, (0, 0.05, 1.75), (2.6, 0.9, 0.7), 0.15)
    for x in (-0.7, 0.7): box(s, (x, 0.3, 1.3), (0.2, 0.2, 0.4), 0.03)
    box(b3d.mat('glass', (0.12, 0.16, 0.24), rough=0.05, coat=0.5), (-0.5, -0.02, 2.35), (1.0, 0.8, 0.55), 0.1)
    return (0, -0.3, 1.06), 'track_top'


MAKE = {'A': bike, 'B': car, 'C': cart, 'D': crawler}


def scene(key, after):
    road = b3d.mat('road', (0.16, 0.17, 0.2), rough=0.8, coat=0); line = glowm('line', (0.95, 0.95, 0.9), 0.4)
    box(road, (0, 0, -0.06), (4.6, 1.8, 0.12), 0.02)
    for x in (-1.6, 0, 1.6): box(line, (x, 0.75, 0.005), (0.8, 0.06, 0.01), 0.005)
    loc, spot = MAKE[key](); assert spot == BOARDS[key][2]
    sticker(loc)
    if after:
        arrow((loc[0] + 0.14, loc[1] - 0.12, loc[2]), 0.3 * round(GOOD[key]), glowm('mint', (0.2, 0.95, 0.65), 1.5))
    b3d.stack_camera((0.6, 0, 1.25), 5.4, az=12.0, el=7.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((760, 620), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t, 1), flush=True)
