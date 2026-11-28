"""ROOM 215 3D sprites, units of 10 cm: a clear square water jug (12 x 12 x 20 cm) full of water up to 15.5 cm, with a
row of small holes on its right face, all 3 cm above the table. Cap on the neck, or lying on the table beside the jug
when it is off. Board C also has one small hole on the front face near the top, above the water line.
p*: the jug with nothing coming out. a*: a blue stream from every hole that flows (mint ring around those holes, and a
mint ring around the air hole), or coral rings around holes that stay dry. Same camera for every board."""
import os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
HX, HZ, LEVEL = 0.6, 0.3, 1.55


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def clear(name, c, trans, rough=0.05, alpha=1.0):
    m = b3d.mat(name, c, rough=rough, coat=0.3); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Transmission Weight'].default_value = trans; q.inputs['IOR'].default_value = 1.33
    if alpha < 1: q.inputs['Alpha'].default_value = alpha
    return m


def box(m, loc, sc, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def cyl(m, loc, r, d, rot=(0, 0, 0), v=40):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d, location=loc, rotation=rot); o = bpy.context.object
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def ball(m, loc, r):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=16, ring_count=8); o = bpy.context.object
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def ring(m, loc, rot, r=0.075):
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=0.014, location=loc, rotation=rot); bpy.context.object.data.materials.append(m)


def scene(key, after):
    import math
    n, cap, air = BOARDS[key]; flow = GOOD[key] > 0
    table = b3d.mat('table', (0.78, 0.74, 0.68), rough=0.7, coat=0.1)
    shell = clear('shell', (0.85, 0.93, 1.0), 0.92, alpha=0.55); water = clear('water', (0.25, 0.6, 1.0), 0.55, rough=0.1)
    capm = b3d.mat('cap', (0.9, 0.2, 0.15), rough=0.35, coat=0.5); hole = b3d.mat('hole', (0.02, 0.03, 0.05), rough=0.9, coat=0)
    jet = glowm('jet', (0.35, 0.7, 1.0), 0.9, 0.1); mint = glowm('mint', (0.2, 0.95, 0.65), 2.2); coral = glowm('coral', (1.0, 0.3, 0.25), 0.9)
    box(table, (0.5, 0, -0.05), (3.6, 2.2, 0.1), 0.03)
    box(shell, (0, 0, 1.0), (1.2, 1.2, 2.0), 0.12)
    box(water, (0, 0, LEVEL / 2 + 0.03), (1.12, 1.12, LEVEL - 0.03), 0.06)
    cyl(shell, (0, 0, 2.12), 0.27, 0.26)
    if cap: cyl(capm, (0, 0, 2.33), 0.3, 0.2)
    else:
        cyl(capm, (-0.95, -0.55, 0.1), 0.3, 0.2); cyl(hole, (0, 0, 2.25), 0.21, 0.02)     # cap on the table, open neck
    ys = [(-0.38 + 0.76 * i / (n - 1)) if n > 1 else 0.0 for i in range(n)]
    for y in ys:
        cyl(hole, (HX + 0.005, y, HZ), 0.045, 0.02, rot=(0, math.pi / 2, 0), v=24)
        if after:
            ring(mint if flow else coral, (HX + 0.02, y, HZ), (0, math.pi / 2, 0))
            if flow:
                for i in range(1, 15):
                    s = i / 14; ball(jet, (HX + 0.95 * s, y, HZ * (1 - s * s) + 0.01), 0.032)
    if air:
        cyl(hole, (0, -0.605, 1.82), 0.045, 0.02, rot=(math.pi / 2, 0, 0), v=24)
        if after: ring(mint, (0, -0.62, 1.82), (math.pi / 2, 0, 0))
    b3d.stack_camera((0.3, 0, 1.1), 4.1, az=38.0, el=16.0)


only = sys.argv[1:]
for key in 'ABCD':
    for kind in 'pa':
        nm = kind + key
        if only and nm not in only: continue
        b3d.reset((820, 620), 64); b3d.lights(4)
        t0 = time.time(); scene(key, kind == 'a')
        b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t0, 1), flush=True)
