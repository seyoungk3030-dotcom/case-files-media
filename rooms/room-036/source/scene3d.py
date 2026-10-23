"""ROOM 036 3D sprites: four upside-down cups on spots 1-4, at the start (A B C D) and at the end (answer).
Spot label positions go to .build-3d/<name>.json."""
import json, math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import SWAPS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
COL = {'A': b3d.PAL['mint'], 'B': b3d.PAL['amber'], 'C': b3d.PAL['coral'], 'D': (0.38, 0.30, 0.95)}
GAP = 1.55


def cup(x, m, rim):
    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=0.56, radius2=0.40, depth=1.05, location=(x, 0, 0.6))
    o = bpy.context.object; o.data.materials.append(m); b3d.bevel(o, 0.05, 4)
    for poly in o.data.polygons: poly.use_smooth = True
    bpy.ops.mesh.primitive_torus_add(major_radius=0.56, minor_radius=0.05, location=(x, 0, 0.09)); bpy.context.object.data.materials.append(rim)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(x, 0, 1.17)); bpy.context.object.data.materials.append(rim)


def scene(order):
    b3d.reset((1000, 520), 64); b3d.lights(6)
    b3d.stack_camera((GAP * 1.5, 0, 0.55), 6.9, 0.0, 18.0)
    spot = b3d.mat('spot', (0.80, 0.84, 0.92), rough=0.4, coat=0.2); rim = b3d.mat('rim', (0.95, 0.95, 0.97), rough=0.25, coat=0.6)
    for k in range(4):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.7, depth=0.04, vertices=64, location=(k * GAP, 0, 0.02))
        bpy.context.object.data.materials.append(spot)
    for k, c in enumerate(order): cup(k * GAP, b3d.mat(c, COL[c], rough=0.25, coat=0.7), rim)
    b3d.floor()
    bpy.context.view_layer.update()
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    sc = bpy.context.scene; out = []
    for k in range(4):
        for key, z, y in ((str(k + 1), 0.0, -0.95), (order[k], 0.62, -0.5)):
            v = world_to_camera_view(sc, sc.camera, Vector((k * GAP, y, z)))
            out.append({'key': key, 'x': round(v.x * sc.render.resolution_x, 1), 'y': round((1 - v.y) * sc.render.resolution_y, 1)})
    return out


def final():
    spot = {1: 'A', 2: 'B', 3: 'C', 4: 'D'}
    for a, b in SWAPS: spot[a], spot[b] = spot[b], spot[a]
    return ''.join(spot[k] for k in range(1, 5))


for name, order in (('start', 'ABCD'), ('final', final())):
    t = time.time(); pts = scene(order); json.dump(pts, open(f'{OUT}/{name}.json', 'w'))
    b3d.render(f'{OUT}/{name}.png'); print(name, order, round(time.time() - t, 1))
