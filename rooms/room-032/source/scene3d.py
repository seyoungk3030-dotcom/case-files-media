"""ROOM 032 3D sprites: the mirror board (lamps 1-4, targets A-D) with and without the traced beams, and a
one-mirror example. Label positions for 2D tags go to .build-3d/board.json."""
import json, math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import MIRRORS, TARGETS, trace
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
Z = 0.32
LAMP = {1: (0.05, 0.72, 0.56), 2: (1.0, 0.55, 0.05), 3: (0.38, 0.22, 1.0), 4: (1.0, 0.22, 0.30)}


def xy(r, c): return c + 0.5, 3.5 - r


def target_xy(t):
    s, i = t
    return {'T': (i + 0.5, 4.75), 'B': (i + 0.5, -0.75), 'R': (4.75, 3.5 - i)}[s]


def glow(name, col, strength):
    m = b3d.mat(name, col, rough=0.3, coat=0.3); p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Emission Color'].default_value = (*col, 1); p.inputs['Emission Strength'].default_value = strength
    return m


def box(loc, scale, m, rz=0.0, bev=0.03):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
    o.scale = scale; o.rotation_euler = (0, 0, rz); o.data.materials.append(m); b3d.bevel(o, bev, 3)
    return o


def mirror(x, y, kind, m, edge, base):
    rz = math.radians(45 if kind == '/' else -45)
    box((x, y, Z), (0.92, 0.07, 0.5), m, rz, 0.02)
    box((x, y, Z + 0.26), (0.92, 0.09, 0.03), edge, rz, 0.01)
    box((x, y, 0.06), (0.5, 0.22, 0.1), base, rz)


def cyl(a, b, rad, m):
    (x0, y0), (x1, y1) = a, b; L = math.hypot(x1 - x0, y1 - y0)
    bpy.ops.mesh.primitive_cylinder_add(radius=rad, depth=L, location=((x0 + x1) / 2, (y0 + y1) / 2, Z))
    o = bpy.context.object; o.rotation_euler = (0, math.radians(90), math.atan2(y1 - y0, x1 - x0)); o.data.materials.append(m)


def lamp(row, n):
    x, y = -0.75, 3.5 - row
    body = b3d.mat(f'lamp{n}', (0.20, 0.24, 0.32), rough=0.35, metal=0.6, coat=0.3)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.55, location=(x, y, Z))
    o = bpy.context.object; o.rotation_euler = (0, math.radians(90), 0); o.data.materials.append(body); b3d.bevel(o, 0.04, 3)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.16, depth=0.04, location=(x + 0.285, y, Z))
    o = bpy.context.object; o.rotation_euler = (0, math.radians(90), 0); o.data.materials.append(glow(f'lens{n}', LAMP[n], 0.7))
    box((x, y, 0.06), (0.3, 0.36, 0.12), body)
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.09, depth=0.22, location=(x + 0.5, y, Z))
    o = bpy.context.object; o.rotation_euler = (0, math.radians(90), 0); o.data.materials.append(glow(f'arrow{n}', LAMP[n], 0.6))


def target(k, col, lit):
    x, y = target_xy(TARGETS[k])
    ped = b3d.mat(f'ped{k}', (0.20, 0.24, 0.32), rough=0.35, metal=0.6, coat=0.3)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.26, depth=0.16, location=(x, y, 0.08)); o = bpy.context.object
    o.data.materials.append(ped); b3d.bevel(o, 0.03, 3)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.24, location=(x, y, 0.38)); o = bpy.context.object
    o.scale = (1, 1, 1.35); o.data.materials.append(glow(f'gem{k}', col, 0.9) if lit else b3d.mat(f'gem{k}', (0.85, 0.88, 0.95), rough=0.15, coat=0.8))


def scene(beams):
    b3d.lights(6)
    tile = b3d.mat('tile', (0.26, 0.32, 0.42), rough=0.5, coat=0.0); base = b3d.mat('base', (0.10, 0.13, 0.19), rough=0.5, coat=0.0)
    mm = glow('mirror', (0.55, 0.85, 1.0), 0.35); edge = glow('edge', (0.75, 0.95, 1.0), 2.5)
    box((2, 2, -0.15), (4.3, 4.3, 0.3), base, 0, 0.06)
    for r in range(4):
        for c in range(4):
            x, y = xy(r, c); box((x, y, 0.0), (0.94, 0.94, 0.04), tile, 0, 0.01)
    for (r, c), kind in MIRRORS.items(): mirror(*xy(r, c), kind, mm, edge, base)
    hit = {}
    for row in range(4):
        n = row + 1; lamp(row, n)
        path, ex = trace(row); k = next(k for k, t in TARGETS.items() if t == ex); hit[k] = n
        if beams:
            pts = [(-0.45, 3.5 - row)] + [xy(r, c) for r, c, d in path if (r, c) in MIRRORS] + [target_xy(ex)]
            bm = glow(f'beam{n}', LAMP[n], 1.0)
            for a, b in zip(pts, pts[1:]): cyl(a, b, 0.05, bm)
    for k in TARGETS: target(k, LAMP[hit[k]], beams)
    b3d.floor()


def marks():
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    sc = bpy.context.scene; out = []
    pts = [(str(n), -0.75, 3.5 - (n - 1), 0.75) for n in range(1, 5)] + [(k, *target_xy(t), 1.05) for k, t in TARGETS.items()]
    for k, x, y, z in pts:
        v = world_to_camera_view(sc, sc.camera, Vector((x, y, z)))
        out.append({'key': k, 'x': round(v.x * sc.render.resolution_x, 1), 'y': round((1 - v.y) * sc.render.resolution_y, 1)})
    return out


only = sys.argv[1:]
for name, beams in (('board', False), ('beams', True)):
    if only and name not in only: continue
    t = time.time(); b3d.reset((1000, 1000), 64)
    b3d.stack_camera((2.0, 2.05, 0.2), 7.0, 0.0, 58.0)
    scene(beams)
    if name == 'board': json.dump(marks(), open(f'{OUT}/board.json', 'w'))
    b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1))
if not only or 'ex' in only:
    b3d.reset((800, 460), 48); b3d.lights(3)
    b3d.stack_camera((0.9, 0.9, 0.2), 3.0, 0.0, 58.0)
    tile = b3d.mat('tile', (0.26, 0.32, 0.42), rough=0.5, coat=0.0); base = b3d.mat('base', (0.10, 0.13, 0.19), rough=0.5, coat=0.0)
    box((0.9, 0.9, -0.1), (1.0, 1.0, 0.2), base, 0, 0.04); box((0.9, 0.9, 0.02), (0.94, 0.94, 0.04), tile, 0, 0.01)
    mirror(0.9, 0.9, '/', glow('mirror', (0.55, 0.85, 1.0), 0.35), glow('edge', (0.75, 0.95, 1.0), 2.5), base)
    bm = glow('b', LAMP[1], 1.0); cyl((-0.6, 0.9), (0.9, 0.9), 0.05, bm); cyl((0.9, 0.9), (0.9, 2.0), 0.05, bm)
    b3d.floor(); b3d.render(f'{OUT}/ex.png'); print('ex')
