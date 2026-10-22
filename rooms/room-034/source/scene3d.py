"""ROOM 034 3D sprites: the matchstick number (start), the answer with the moved match glowing and a ghost where it
came from, and the 0-9 digit chart. Answer badge positions go to .build-3d/start.json."""
import json, math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import SEG, START
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
PITCH = 1.75
ENDS = {'a': ((0, 2), (1, 2)), 'g': ((0, 1), (1, 1)), 'd': ((0, 0), (1, 0)), 'f': ((0, 1), (0, 2)),
        'b': ((1, 1), (1, 2)), 'e': ((0, 0), (0, 1)), 'c': ((1, 0), (1, 1))}


def mats():
    M = {'wood': b3d.mat('wood', (0.93, 0.72, 0.42), rough=0.55, coat=0.2), 'head': b3d.mat('head', (0.85, 0.10, 0.08), rough=0.4, coat=0.5),
         'felt': b3d.mat('felt', (0.08, 0.20, 0.17), rough=0.9, coat=0.0)}
    g = b3d.mat('glow', (0.2, 0.95, 0.75), rough=0.4, coat=0.3); p = g.node_tree.nodes['Principled BSDF']
    p.inputs['Emission Color'].default_value = (0.2, 0.95, 0.75, 1); p.inputs['Emission Strength'].default_value = 0.45; M['glow'] = g
    gh = b3d.mat('ghost', (1, 1, 1), rough=0.5, coat=0.0); gh.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.22; M['ghost'] = gh
    return M


def match(x0, y0, seg, M, body=None, head=True):
    (ax, ay), (bx, by) = ENDS[seg]
    cx, cy = x0 + (ax + bx) / 2, y0 + (ay + by) / 2; horiz = ay == by; L = 0.84
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, 0.05)); o = bpy.context.object
    o.scale = (L, 0.09, 0.09) if horiz else (0.09, L, 0.09); o.data.materials.append(body or M['wood']); b3d.bevel(o, 0.02, 2)
    if head:
        hx, hy = (cx + L / 2, cy) if horiz else (cx, cy + L / 2)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.085, location=(hx, hy, 0.06)); o = bpy.context.object
        o.scale = (1.35, 1, 1) if horiz else (1, 1.35, 1); o.data.materials.append(M['head'])


def mat_bg(w, h, cx, cy, M):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, -0.08)); o = bpy.context.object
    o.scale = (w, h, 0.12); o.data.materials.append(M['felt']); b3d.bevel(o, 0.08, 4)


def number(n, M, glow=None, ghost=None, y0=0.0):
    for k, ch in enumerate(n):
        for s in SEG[int(ch)]:
            match(k * PITCH - (0.5 if ch == '1' and k else 0), y0, s, M, M['glow'] if glow == (k, s) else None)
    if ghost: match(ghost[0] * PITCH, y0, ghost[1], M, M['ghost'], head=False)


def marks(n):
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    sc = bpy.context.scene; out = []
    for k, key in zip(range(len(n)), 'ABCD'):
        v = world_to_camera_view(sc, sc.camera, Vector((k * PITCH + 0.5, 2.55, 0.1)))
        out.append({'key': key, 'x': round(v.x * sc.render.resolution_x, 1), 'y': round((1 - v.y) * sc.render.resolution_y, 1)})
    return out


only = sys.argv[1:]
W = 3 * PITCH + 1
for name in ('start', 'answer'):
    if only and name not in only: continue
    t = time.time(); b3d.reset((1000, 620), 64); b3d.lights(6)
    b3d.stack_camera((W / 2, 1.0, 0), 7.6, 0.0, 52.0)
    M = mats(); mat_bg(W + 1.0, 3.3, W / 2, 1.0, M)
    if name == 'start': number(START, M); json.dump(marks(START), open(f'{OUT}/start.json', 'w'))
    else: number('7510', M, glow=(0, 'a'), ghost=(1, 'e'))
    b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1))
if not only or 'chart' in only:
    b3d.reset((1000, 470), 48); b3d.lights(10)
    W5 = 4 * PITCH + 1
    b3d.stack_camera((W5 / 2, 0.05, 0), 15.0, 0.0, 60.0)
    M = mats(); mat_bg(W5 + 1.2, 6.6, W5 / 2, 0.05, M)
    number('01234', M, y0=0.75); number('56789', M, y0=-2.65)
    b3d.render(f'{OUT}/chart.png'); print('chart')
