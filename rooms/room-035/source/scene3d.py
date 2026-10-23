"""ROOM 035 3D sprites: towers 1-4 (cube stacks, same camera as view.py) with label points for '앞'/'오른쪽',
and silhouettes A-D as flat tile panels."""
import json, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d, view
from verify import TOWERS, SIL
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
COL = {1: b3d.PAL['mint'], 2: b3d.PAL['amber'], 3: b3d.PAL['coral'], 4: (0.38, 0.30, 0.95)}


def project(pts):
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    bpy.context.view_layer.update(); sc = bpy.context.scene; out = []
    for k, p in pts:
        v = world_to_camera_view(sc, sc.camera, Vector(p))
        out.append({'key': k, 'x': round(v.x * sc.render.resolution_x, 1), 'y': round((1 - v.y) * sc.render.resolution_y, 1)})
    return out


def cells(d, s):
    """Filled (col, row-from-bottom) cells of a silhouette drawn on a 3x3 panel."""
    if d == 'top': return [(i, j) for j in range(3) for i in range(3) if s[j * 3 + i]]
    return [(i, z) for i in range(3) for z in range(s[i])]


only = sys.argv[1:]
for n, t in TOWERS.items():
    if only and f't{n}' not in only: continue
    tt = time.time(); b3d.reset((560, 600), 48); b3d.lights(3)
    b3d.cubestack([list(t[j * 3:j * 3 + 3]) for j in range(3)], COL[n]); b3d.stack_camera((1.5, 1.5, 1.0), 6.0, view.AZ, view.EL)
    json.dump(project([('front', (1.5, -0.45, -0.3)), ('right', (3.45, 1.5, -0.3))]), open(f'{OUT}/t{n}.json', 'w'))
    b3d.render(f'{OUT}/t{n}.png'); print('t', n, round(time.time() - tt, 1))
from verify import front, right
EXTRA = {'exF': ('front', front(TOWERS[1])), 'exR': ('right', right(TOWERS[1]))}
for k, (d, s) in list(SIL.items()) + list(EXTRA.items()):
    if only and k not in only: continue
    b3d.reset((420, 420), 32); b3d.lights(3)
    b3d.stack_camera((1.5, 1.5, 0), 3.9, 0.0, 90.0)
    full = b3d.mat('full', (0.92, 0.94, 0.98), rough=0.3, coat=0.5); empty = b3d.mat('empty', (0.12, 0.16, 0.23), rough=0.8, coat=0.0)
    fill = set(cells(d, s))
    for i in range(3):
        for j in range(3):
            on = (i, j) in fill
            bpy.ops.mesh.primitive_cube_add(size=1, location=(i + 0.5, j + 0.5, 0.12 if on else 0.0)); o = bpy.context.object
            o.scale = (0.92, 0.92, 0.24 if on else 0.04); o.data.materials.append(full if on else empty); b3d.bevel(o, 0.05 if on else 0.01, 3)
    b3d.render(f'{OUT}/sil-{k}.png'); print('sil', k)
