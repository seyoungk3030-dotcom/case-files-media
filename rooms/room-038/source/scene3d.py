"""ROOM 038 3D sprites: one dial-lock bar per try (four wheels + four lamps), and the padlock closed (????) and open (code).
Wheel centres go to .build-3d/<name>.json (keys A-D = wheels 1-4)."""
import json, math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import TRIES, LAMPS, CODE
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
GAP = 1.05


def glow(name, col, s):
    m = b3d.mat(name, col, rough=0.2, coat=0.5); p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Emission Color'].default_value = (*col, 1); p.inputs['Emission Strength'].default_value = s
    return m


def rbox(loc, dims, m, bev=0.12):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = dims
    o.data.materials.append(m); b3d.bevel(o, bev, 5); return o


def wheels(digits, z, M):
    for i, d in enumerate(digits):
        x = (i - 1.5) * GAP
        bpy.ops.mesh.primitive_cylinder_add(radius=0.62, depth=0.84, vertices=64, location=(x, 0, z), rotation=(0, math.radians(90), 0))
        o = bpy.context.object; o.data.materials.append(M['wheel']); b3d.bevel(o, 0.06, 4)
        for p in o.data.polygons: p.use_smooth = True
        for k in (-1, 1):   # ridges
            bpy.ops.mesh.primitive_torus_add(major_radius=0.62, minor_radius=0.035, location=(x + k * 0.38, 0, z), rotation=(0, math.radians(90), 0))
            bpy.context.object.data.materials.append(M['ridge'])
        bpy.ops.object.text_add(location=(x, -0.645, z), rotation=(math.radians(90), 0, 0))
        t = bpy.context.object; t.data.body = d; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'
        t.data.size = 0.78; t.data.extrude = 0.03; t.data.materials.append(M['ink'])


def common(res, center, scale):
    b3d.reset(res, 48); b3d.lights(6)
    b3d.stack_camera(center, scale, 0.0, 10.0)
    return {'body': b3d.mat('body', (0.16, 0.20, 0.27), rough=0.35, metal=0.6, coat=0.3),
            'wheel': b3d.mat('wheel', (0.93, 0.91, 0.86), rough=0.3, coat=0.6),
            'ridge': b3d.mat('ridge', (0.70, 0.72, 0.76), rough=0.3, metal=1.0, coat=0.0),
            'ink': b3d.mat('ink', (0.05, 0.06, 0.09), rough=0.5, coat=0.0),
            'steel': b3d.mat('steel', (0.75, 0.78, 0.82), rough=0.22, metal=1.0, coat=0.0),
            'gold': b3d.mat('gold', (0.95, 0.66, 0.18), rough=0.3, metal=0.9, coat=0.3)}


def points(res):
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    sc = bpy.context.scene; bpy.context.view_layer.update(); out = []
    for i, k in enumerate('ABCD'):
        for key, z in ((k, 0.0), (k + 'top', 0.75)):
            v = world_to_camera_view(sc, sc.camera, Vector(((i - 1.5) * GAP, -0.65, z)))
            out.append({'key': key, 'x': round(v.x * res[0], 1), 'y': round((1 - v.y) * res[1], 1)})
    return out


def row(guess, lamps):
    res = (1400, 330); M = common(res, (0.95, 0, 0), 7.4)
    rbox((0.95, 0.15, 0), (6.6, 1.05, 1.0), M['body'])
    wheels(guess, 0, M)
    g, a = lamps; cols = [('g', (0.10, 0.85, 0.40), 0.9)] * g + [('a', (1.0, 0.62, 0.05), 0.9)] * a
    cols += [('o', (0.28, 0.31, 0.36), 0.0)] * (4 - len(cols))
    for j, (n, c, s) in enumerate(cols):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=(2.75 + (j % 2) * 0.5, -0.4, 0.25 - (j // 2) * 0.5))
        o = bpy.context.object; o.data.materials.append(glow(f'l{j}{n}', c, s))
        for p in o.data.polygons: p.use_smooth = True
    return points(res)


def padlock(digits, open_):
    res = (900, 900); M = common(res, (0, 0, 1.5), 7.0)
    rbox((0, 0.6, 0.1), (5.0, 1.2, 2.6), M['gold'], 0.3)
    rbox((0, 0.05, 0), (4.6, 0.4, 1.5), M['body'], 0.1)
    wheels(digits, 0, M)
    lift = 1.1 if open_ else 0.0
    bpy.ops.mesh.primitive_torus_add(major_radius=1.55, minor_radius=0.26, location=(0, 0.6, 1.4 + lift), rotation=(math.radians(90), 0, 0))
    sh = bpy.context.object; sh.data.materials.append(M['steel'])
    for p in sh.data.polygons: p.use_smooth = True
    # hide the lower half of the ring inside the body by a boolean with a box
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.6, 1.4 + lift - 1.2)); cut = bpy.context.object; cut.scale = (4, 2, 2.4)
    mod = sh.modifiers.new('b', 'BOOLEAN'); mod.operation = 'DIFFERENCE'; mod.object = cut; cut.hide_render = True
    for x in (-1.55, 1.55):
        if open_ and x > 0: continue
        bpy.ops.mesh.primitive_cylinder_add(radius=0.26, depth=1.2 + lift, location=(x, 0.6, 1.3 + lift / 2))
        o = bpy.context.object; o.data.materials.append(M['steel'])
        for p in o.data.polygons: p.use_smooth = True
    return points(res)


jobs = [(f'try{i + 1}', lambda i=i: row(TRIES[i], LAMPS[i])) for i in range(4)] + [
        ('lock', lambda: padlock('????', False)), ('open', lambda: padlock(CODE, True))]
only = sys.argv[1:]
for name, fn in jobs:
    if only and name not in only: continue
    t = time.time(); pts = fn(); json.dump(pts, open(f'{OUT}/{name}.json', 'w'))
    b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
