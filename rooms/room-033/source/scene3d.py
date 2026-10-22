"""ROOM 033 3D sprites: the hanging mobile and a one-bar example. Label positions for 2D tags go to .build-3d/*.json."""
import json, math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BARS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
UNIT = {'T': 1.6, 'P': 0.5, 'Q': 0.5, 'R': 0.4}
DROP = {'P': 1.5, 'Q': 1.5, 'R': 1.4}           # string length from parent bar to sub-bar
OBJ = {'A': ('sphere', 'mint'), 'B': ('cube', 'coral'), 'C': ('pyramid', 'amber'), 'D': ('star', 'pearl'), 'K': ('weight', 'steel')}


def cyl(p0, p1, rad, m):
    (x0, z0), (x1, z1) = p0, p1; L = math.hypot(x1 - x0, z1 - z0)
    bpy.ops.mesh.primitive_cylinder_add(radius=rad, depth=L, vertices=24, location=((x0 + x1) / 2, 0, (z0 + z1) / 2))
    o = bpy.context.object; o.rotation_euler = (0, math.atan2(x1 - x0, z1 - z0), 0); o.data.materials.append(m)
    return o


def ball(x, z, r, m):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=24, ring_count=12, location=(x, 0, z)); bpy.context.object.data.materials.append(m)


def weight(m, x, top, label_z):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.38, depth=0.55, vertices=48, location=(x, 0, top - 0.3))
    o = bpy.context.object; o.data.materials.append(m); b3d.bevel(o, 0.06, 3)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.1, minor_radius=0.03, location=(x, 0, top + 0.02), rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.materials.append(m)


def bar(name, x, z, M, tags, depth=0):
    l, a, r, b = BARS[name]; u = UNIT[name]
    cyl((x - a * u - 0.06, z), (x + b * u + 0.06, z), 0.05, M['rod'])
    ball(x, z + 0.02, 0.1, M['pivot'])
    for k in range(-a, b + 1):
        if k: ball(x + k * u, z, 0.075, M['bead'])
    tags += [{'key': f'{name}L', 'text': str(a), 'x': x - a * u / 2, 'z': z + 0.3},
             {'key': f'{name}R', 'text': str(b), 'x': x + b * u / 2, 'z': z + 0.3}]
    for item, cx in ((l, x - a * u), (r, x + b * u)):
        if item in BARS:
            zz = z - DROP[item]; cyl((cx, z), (cx, zz), 0.014, M['string']); bar(item, cx, zz, M, tags)
        else:
            kind, col = OBJ[item]; top = z - 0.9
            cyl((cx, z), (cx, top), 0.014, M['string'])
            if kind == 'weight': weight(M['steel'], cx, top, 0); bottom = top - 0.6
            elif kind == 'star': b3d.star(M[col], cx, top - 0.81, 0.5); bottom = top - 0.85
            elif kind == 'sphere': b3d.sphere(M[col], cx, top - 0.84, 0.42); bottom = top - 0.84
            elif kind == 'cube': b3d.cube(M[col], cx, top - 0.78, 0.74); bottom = top - 0.8
            else: b3d.pyramid(M[col], cx, top - 0.85, 0.5, 0.85); bottom = top - 0.85
            tags.append({'key': item, 'text': '9' if item == 'K' else item, 'x': cx, 'z': bottom - 0.32})


def mats():
    M = b3d.mats()
    M['rod'] = b3d.mat('rod', (0.75, 0.78, 0.84), rough=0.25, metal=0.9, coat=0.0)
    M['bead'] = b3d.mat('bead', (1.0, 0.78, 0.25), rough=0.25, coat=0.5)
    M['pivot'] = b3d.mat('pivot', (0.15, 0.18, 0.24), rough=0.3, metal=0.8, coat=0.0)
    M['string'] = b3d.mat('string', (0.85, 0.87, 0.9), rough=0.6, coat=0.0)
    return M


def project(tags):
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    sc = bpy.context.scene; out = []
    for t in tags:
        v = world_to_camera_view(sc, sc.camera, Vector((t['x'], 0, t['z'])))
        out.append({'key': t['key'], 'text': t['text'], 'x': round(v.x * sc.render.resolution_x, 1), 'y': round((1 - v.y) * sc.render.resolution_y, 1)})
    return out


only = sys.argv[1:]
if not only or 'mobile' in only:
    t = time.time(); b3d.reset((1000, 900), 64); b3d.lights(8)
    b3d.stack_camera((-1.0, 0, 3.6), 9.3, 0.0, 4.0)
    M = mats(); tags = []
    cyl((0, 6.0), (0, 7.2), 0.014, M['string'])
    bar('T', 0.0, 6.0, M, tags)
    json.dump(project(tags), open(f'{OUT}/mobile.json', 'w')); b3d.render(f'{OUT}/mobile.png'); print('mobile', round(time.time() - t, 1))
if not only or 'ex' in only:
    b3d.reset((800, 460), 48); b3d.lights(4)
    b3d.stack_camera((-0.45, 0, 1.4), 4.6, 0.0, 4.0)
    M = mats(); u = 0.45
    cyl((-3 * u - 0.06, 2.0), (u + 0.06, 2.0), 0.05, M['rod']); ball(0, 2.02, 0.1, M['pivot']); cyl((0, 2.0), (0, 2.6), 0.014, M['string'])
    for k in (-3, -2, -1, 1): ball(k * u, 2.0, 0.075, M['bead'])
    cyl((-3 * u, 2.0), (-3 * u, 1.3), 0.014, M['string']); b3d.sphere(M['mint'], -3 * u, 0.62, 0.34)
    cyl((u, 2.0), (u, 1.3), 0.014, M['string']); weight(M['steel'], u, 1.3, 0)
    json.dump(project([{'key': 'L', 'text': '2', 'x': -3 * u, 'z': 0.3}, {'key': 'R', 'text': '6', 'x': u, 'z': 0.42},
                       {'key': 'dL', 'text': '3', 'x': -1.5 * u, 'z': 2.3}, {'key': 'dR', 'text': '1', 'x': u / 2, 'z': 2.3}]),
              open(f'{OUT}/ex.json', 'w'))
    b3d.render(f'{OUT}/ex.png'); print('ex')
