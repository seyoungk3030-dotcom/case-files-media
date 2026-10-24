"""ROOM 040 3D sprites: a marble drop with three arrow switches (top, left, right) and bins 1-4.
'start' shows the switches as they begin with marbles A-D waiting; 'end' shows where the marbles land.
Label points (bins 1-4, marbles A-D) go to .build-3d/<name>.json."""
import json, math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import START, states, code
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
MCOL = {'A': b3d.PAL['mint'], 'B': b3d.PAL['amber'], 'C': b3d.PAL['coral'], 'D': (0.38, 0.30, 0.95)}
SW = {'T': (0, 5.5), 'L': (-2, 3.3), 'R': (2, 3.3)}
BIN = {1: -3, 2: -1, 3: 1, 4: 3}; BZ = 0.9; MR = 0.3


def tube(a, b, m, r=0.09, y=0.0):
    a, b = Vector((a[0], y, a[1])), Vector((b[0], y, b[1])); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, vertices=24, location=(a + b) / 2)
    o = bpy.context.object; o.rotation_euler = d.to_track_quat('Z', 'Y').to_euler(); o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = True


def switch(x, z, way, M):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.62, depth=0.3, vertices=64, location=(x, 0, z), rotation=(math.radians(90), 0, 0))
    o = bpy.context.object; o.data.materials.append(M['disk']); b3d.bevel(o, 0.06, 4)
    ang = math.radians(-45 if way == 'L' else 45)          # arrow points down-left or down-right
    dx, dz = math.sin(ang), -math.cos(ang)
    tube((x - dx * 0.4, z - dz * 0.4), (x + dx * 0.12, z + dz * 0.12), M['arrow'], 0.11, -0.3)
    bpy.ops.mesh.primitive_cone_add(radius1=0.27, radius2=0, depth=0.42, vertices=32, location=(x + dx * 0.3, -0.3, z + dz * 0.3))
    c = bpy.context.object; c.rotation_euler = Vector((dx, 0, dz)).to_track_quat('Z', 'Y').to_euler(); c.data.materials.append(M['arrow'])
    for obj in (c,):
        for p in obj.data.polygons: p.use_smooth = True


def marble(x, z, k):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=MR, segments=48, ring_count=24, location=(x, -0.1, z))
    o = bpy.context.object; o.data.materials.append(b3d.mat(k, MCOL[k], rough=0.15, coat=0.9))
    for p in o.data.polygons: p.use_smooth = True


def scene(sw, where):
    res = (1000, 1050); b3d.reset(res, 48); b3d.lights(6)
    for o in bpy.data.objects:
        if o.type == 'LIGHT': o.location.z += 3
    b3d.stack_camera((0.3, 0, 3.6), 9.4, 0.0, 6.0)
    M = {'disk': b3d.mat('disk', (0.93, 0.93, 0.95), rough=0.3, coat=0.5), 'arrow': b3d.mat('arrow', (0.95, 0.60, 0.10), rough=0.3, coat=0.5),
         'rail': b3d.mat('rail', (0.62, 0.68, 0.78), rough=0.3, metal=1.0, coat=0.0), 'bin': b3d.mat('bin', (0.30, 0.38, 0.52), rough=0.4, coat=0.3)}
    tube((0, 7.0), SW['T'], M['rail'])
    for k in 'LR': tube(SW['T'], SW[k], M['rail'])
    for n, x in BIN.items(): tube(SW['L' if n < 3 else 'R'], (x, BZ + 0.75), M['rail'])
    for k, (x, z) in SW.items(): switch(x, z, sw[k], M)
    for n, x in BIN.items():   # open-top bin: back, bottom and two walls
        for loc, sc in (((x, 0.25, BZ), (1.5, 0.12, 1.3)), ((x, -0.1, BZ - 0.6), (1.5, 0.8, 0.12)),
                        ((x - 0.7, -0.1, BZ), (0.12, 0.8, 1.3)), ((x + 0.7, -0.1, BZ), (0.12, 0.8, 1.3))):
            bpy.ops.mesh.primitive_cube_add(size=1, location=loc); b = bpy.context.object; b.scale = sc; b.data.materials.append(M['bin']); b3d.bevel(b, 0.04, 3)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(2.0, -0.1, 7.0 - MR - 0.08)); s = bpy.context.object
    s.scale = (3.8, 0.7, 0.12); s.data.materials.append(M['bin']); b3d.bevel(s, 0.04, 3)
    pos = {}
    for k in 'ABCD':
        if where[k] == 0: pos[k] = (0.75 + 'ABCD'.index(k) * 0.85, 7.0)
        else:
            same = [j for j in 'ABCD' if where[j] == where[k]]
            pos[k] = (BIN[where[k]] + (same.index(k) - (len(same) - 1) / 2) * 0.65, BZ - 0.6 + 0.06 + MR)
        marble(*pos[k], k)
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; bpy.context.view_layer.update(); out = []
    pts = {str(n): (x, BZ - 1.15) for n, x in BIN.items()} | {k: (x, z + 0.62) for k, (x, z) in pos.items()}
    for key, (x, z) in pts.items():
        v = world_to_camera_view(sc, sc.camera, Vector((x, -0.4, z)))
        out.append({'key': key, 'x': round(v.x * res[0], 1), 'y': round((1 - v.y) * res[1], 1)})
    return out


jobs = [('start', START, {k: 0 for k in 'ABCD'}), ('end', states[4], {k: int(c) for k, c in zip('ABCD', code)})]
for name, sw, where in jobs:
    t = time.time(); pts = scene(sw, where); json.dump(pts, open(f'{OUT}/{name}.json', 'w'))
    b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
