"""ROOM 086 3D sprites: a cosy desk against a wall (shelf of books and a pencil cup, wall clock, framed sun picture,
lamp, mug, toy cube, ball, potted plant) built from the item lists in verify.py. p1 = picture 1, p2 = picture 2,
a2 = picture 2 with amber rings around every difference."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import ITEMS, EDIT, D
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
X90 = (math.radians(90), 0, 0)
C = {'red': (0.9, 0.2, 0.25), 'yellow': (0.98, 0.8, 0.2), 'blue': (0.2, 0.45, 0.95), 'green': (0.2, 0.75, 0.4), 'purple': (0.6, 0.35, 0.9),
     'teal': (0.15, 0.7, 0.7), 'coral': (0.95, 0.5, 0.4), 'white': (0.95, 0.95, 0.93), 'amber': (0.98, 0.6, 0.1)}


def box(loc, scale, m, bev=0.04, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def cyl(loc, r, d, m, rot=(0, 0, 0), v=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, rotation=rot, vertices=v); o = bpy.context.object; o.data.materials.append(m)
    bpy.ops.object.shade_smooth(); return o


def ball(loc, r, m, sc=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=48, ring_count=24); o = bpy.context.object; o.scale = sc
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


M = {}


def mat(c):
    if c not in M: M[c] = b3d.mat(c, C[c], rough=0.35, coat=0.5)
    return M[c]


def item(kind, pos, s, col, Z):
    x, z = pos; z += Z; m = mat(col)
    if kind == 'book': box((x, 0, z + 0.4 * s), (0.26, 0.6, 0.8 * s), m, 0.03)
    elif kind == 'lamp':
        cyl((x, 0, z + 0.05), 0.3, 0.1, m); cyl((x, 0, z + 0.4), 0.045, 0.7, mat('white'))
        bpy.ops.mesh.primitive_cone_add(radius1=0.42, radius2=0.16, depth=0.4, location=(x, 0, z + 0.85)); bpy.context.object.data.materials.append(m)
    elif kind == 'plant':
        cyl((x, 0, z + 0.3 * s), 0.35 * s, 0.6 * s, m)
        for dx, dz in ((0, 0.95), (-0.25, 0.8), (0.25, 0.82), (0, 0.65)): ball((x + dx * s, 0, z + dz * s), 0.25 * s, mat('green'))
    elif kind == 'clock':
        cyl((x, 0.25, z), 0.42 * s, 0.1, mat('white'), rot=X90); bpy.ops.mesh.primitive_torus_add(location=(x, 0.2, z), rotation=X90, major_radius=0.42 * s, minor_radius=0.04)
        bpy.context.object.data.materials.append(mat('red'))
        box((x, 0.18, z + 0.13 * s), (0.04, 0.02, 0.26 * s), mat('purple'), 0.01); box((x + 0.1 * s, 0.18, z), (0.2 * s, 0.02, 0.04), mat('purple'), 0.01)
    elif kind == 'mug':
        cyl((x, 0, z + 0.25), 0.22, 0.5, mat('coral') if False else mat('blue'))
        bpy.ops.mesh.primitive_torus_add(location=(x + 0.25, 0, z + 0.25), rotation=X90, major_radius=0.12, minor_radius=0.04); bpy.context.object.data.materials.append(mat('blue'))
    elif kind == 'frame': box((x, 0.25, z), (1.0, 0.06, 0.75), mat('white'), 0.03); box((x, 0.2, z), (0.86, 0.05, 0.6), mat('teal'), 0.02)
    elif kind == 'sun': cyl((x, 0.16, z), 0.17, 0.04, mat('amber'), rot=X90)
    elif kind == 'ball': ball((x, 0, z + 0.25 * s), 0.25 * s, m)
    elif kind == 'cube': box((x, 0, z + 0.2), (0.4, 0.4, 0.4), m, 0.05, rot=(0, 0, math.radians(20)))
    elif kind == 'pencils':
        cyl((x, 0, z + 0.25), 0.18, 0.5, m)
        for i, c in enumerate(('red', 'yellow', 'green')): cyl((x - 0.08 + i * 0.08, 0, z + 0.6), 0.03, 0.5, mat(c), rot=(0, math.radians(-12 + i * 12), 0), v=12)


def scene(items, rings):
    wall = b3d.mat('wall', (0.86, 0.84, 0.92), rough=0.8, coat=0); desk = b3d.mat('desk', (0.72, 0.5, 0.32), rough=0.5, coat=0.3)
    box((0, 0.5, 1.4), (7.4, 0.1, 3.6), wall, 0.02); box((0, 0, -0.1), (7.0, 1.4, 0.2), desk, 0.04)
    box((-1.2, 0.2, 1.17), (4.4, 0.6, 0.06), desk, 0.02)
    for n, (kind, pos, s, col) in items.items(): item(kind, pos, s, col, 0.0)
    amb = b3d.mat('ring', (0.98, 0.62, 0.12), rough=0.3); q = amb.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (0.98, 0.62, 0.12, 1); q.inputs['Emission Strength'].default_value = 1.0
    for n in rings:
        kind, (x, z), s, c = ITEMS[n] if n not in items else items[n]
        cz = z + {'book': 0.4, 'lamp': 0.5, 'plant': 0.6, 'clock': 0.0, 'mug': 0.25, 'frame': 0.0, 'sun': 0.0, 'ball': 0.3, 'cube': 0.2, 'pencils': 0.4}[kind]
        r = {'lamp': 0.6, 'plant': 0.7, 'clock': 0.48, 'sun': 0.26, 'book': 0.42}.get(kind, 0.36)
        bpy.ops.mesh.primitive_torus_add(location=(x, -0.9, cz), rotation=X90, major_radius=r, minor_radius=0.035); bpy.context.object.data.materials.append(amb)
        if n == 'mug':
            bpy.ops.mesh.primitive_torus_add(location=(ITEMS['mug'][1][0], -0.9, 0.25), rotation=X90, major_radius=0.36, minor_radius=0.035); bpy.context.object.data.materials.append(amb)
    b3d.stack_camera((0, 0, 1.25), 7.2, az=0.0, el=6.0)


only = sys.argv[1:]
for name, items, rings in (('p1', ITEMS, []), ('p2', EDIT, []), ('a2', EDIT, [n for v in D.values() for n in v])):
    if only and name not in only: continue
    M.clear(); b3d.reset((1200, 620), 48); b3d.lights(7)
    t = time.time(); scene(items, rings); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
