"""ROOM 037 3D sprites: a pile of five sticks (A B C D and a white one), plus a two-stick example for the rules card.
Label points (stick ends, crossings) go to .build-3d/<name>.json."""
import json, math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import STICKS, TRUE, pairs
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
COL = {'A': b3d.PAL['mint'], 'B': b3d.PAL['amber'], 'C': b3d.PAL['coral'], 'D': (0.38, 0.30, 0.95), 'G': (0.80, 0.82, 0.86)}
R, STEP = 0.16, 0.34


def stick(seg, z, m):
    x1, y1, x2, y2 = seg; L = math.hypot(x2 - x1, y2 - y1); ang = math.atan2(y2 - y1, x2 - x1)
    bpy.ops.mesh.primitive_cylinder_add(radius=R, depth=L - 2 * R, vertices=48, location=((x1 + x2) / 2, (y1 + y2) / 2, z),
                                        rotation=(0, math.radians(90), ang))
    o = bpy.context.object; o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = True
    for t in (0, 1):   # rounded caps
        cx, cy = x1 + (x2 - x1) * (R / L + t * (1 - 2 * R / L)), y1 + (y2 - y1) * (R / L + t * (1 - 2 * R / L))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=R, segments=32, ring_count=16, location=(cx, cy, z))
        bpy.context.object.data.materials.append(m)
        for p in bpy.context.object.data.polygons: p.use_smooth = True


def scene(sticks, order, center, scale, res):
    b3d.reset(res, 64); b3d.lights(7)
    bpy.ops.object.light_add(type='AREA', location=(center[0] + 2, 3, 9)); L = bpy.context.object.data; L.energy = 900; L.size = 8
    b3d.stack_camera(center, scale, 0.0, 58.0)
    base = b3d.mat('base', (0.20, 0.26, 0.36), rough=0.55, coat=0.0)
    xs = [v for s in sticks.values() for v in (s[0], s[2])]; ys = [v for s in sticks.values() for v in (s[1], s[3])]
    bpy.ops.mesh.primitive_cube_add(size=1, location=((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, -0.12))
    b = bpy.context.object; b.scale = (max(xs) - min(xs) + 1.2, max(ys) - min(ys) + 1.2, 0.2); b.data.materials.append(base); b3d.bevel(b, 0.08)
    for k in sticks:
        stick(sticks[k], R + (len(order) - 1 - order.index(k)) * STEP, b3d.mat(k, COL[k], rough=0.3, coat=0.7))
    b3d.floor(); bpy.context.view_layer.update()
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    sc = bpy.context.scene; out = []

    def px(key, x, y, z):
        v = world_to_camera_view(sc, sc.camera, Vector((x, y, z)))
        out.append({'key': key, 'x': round(v.x * res[0], 1), 'y': round((1 - v.y) * res[1], 1)})
    for k, (x1, y1, x2, y2) in sticks.items():
        L = math.hypot(x2 - x1, y2 - y1); z = R + (len(order) - 1 - order.index(k)) * STEP
        if k == 'C' and len(sticks) > 2: x1, y1, x2, y2 = x2, y2, x1, y1   # C's left end sits next to A's
        px(k, x1 - (x2 - x1) / L * 0.55, y1 - (y2 - y1) / L * 0.55, z)       # just beyond the first end (C: the far end)
    return out


jobs = [('pile', STICKS, TRUE, (0.05, 0.0, 0.3), 9.4, (1000, 760)),
        ('example', {'C': (-2.0, -0.9, 2.0, 0.9), 'D': (-2.0, 0.9, 2.0, -0.9)}, 'DC', (0, 0, 0.3), 5.6, (900, 470))]
for name, st, order, c, s, res in jobs:
    t = time.time(); pts = scene(st, order, c, s, res); json.dump(pts, open(f'{OUT}/{name}.json', 'w'))
    b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1))
