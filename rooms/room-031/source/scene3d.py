"""ROOM 031 3D sprites: the gear train (plus label positions for 2D tags) and a two-gear example."""
import json, math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import TEETH
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
M_ = 0.1; UP = 0.55
COL = {'S': (0.55, 0.60, 0.68), 'A': b3d.PAL['mint'], 'B': b3d.PAL['amber'], 'B2': b3d.PAL['amber'],
       'C': (0.42, 0.40, 0.95), 'D': b3d.PAL['coral']}


def r(k): return M_ * TEETH[k] / 2


def place():
    """Centres: each next gear sits at pitch distance in the given direction."""
    c = {'S': (0.0, 0.0)}
    for k, prev, deg in (('A', 'S', -25), ('B', 'A', -100), ('B2', None, 0), ('C', 'B2', -155), ('D', 'C', -170)):
        if prev is None: c[k] = c['B']; continue
        d = r(prev) + r(k); a = math.radians(deg); c[k] = (c[prev][0] + d * math.cos(a), c[prev][1] + d * math.sin(a))
    return c


def build(keys, cen, tags):
    M = b3d.mats(); hub = b3d.mat('hub', (0.15, 0.18, 0.24), rough=0.35, metal=0.8, coat=0)
    steel = b3d.mat('st', (0.72, 0.76, 0.82), rough=0.3, metal=0.35, coat=0.4)
    xs = [cen[k][0] for k in keys]; ys = [cen[k][1] for k in keys]
    b3d.floor()
    th = {}; objs = {}
    for k in keys:
        z = UP if k in ('B2', 'C', 'D') else 0.0
        if k == 'S': th[k] = 0.05
        elif k == 'B2': th[k] = 0.2
        else:
            prev = {'A': 'S', 'B': 'A', 'C': 'B2', 'D': 'C'}[k]
            th[k] = b3d.mesh_angle(cen[prev], TEETH[prev], cen[k], TEETH[k], th[prev], M_)
        mt = steel if k == 'S' else b3d.mat(k, COL[k], rough=0.3, coat=0.5)
        objs[k] = b3d.gear(TEETH[k], M_, (cen[k][0], cen[k][1], z), th[k], mt, hub=hub)
        if z:   # axle down to the board
            bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=z, location=(cen[k][0], cen[k][1], z / 2))
            bpy.context.object.data.materials.append(hub)
    bpy.context.view_layer.update()
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    sc = bpy.context.scene; out = []
    for k in tags:
        z = (UP if k in ('B2', 'C', 'D') else 0.0) + 0.28
        px, py = cen[k]
        if k == 'B':   # B's centre is under its small upper gear: tag the visible rim instead
            px, py = px + r(k) * 0.72 * math.cos(math.radians(-35)), py + r(k) * 0.72 * math.sin(math.radians(-35))
        v = world_to_camera_view(sc, sc.camera, Vector((px, py, z)))
        out.append({'key': k, 'x': round(v.x * sc.render.resolution_x, 1), 'y': round((1 - v.y) * sc.render.resolution_y, 1)})
    return out


only = sys.argv[1:]
cen = place()
keys = ['S', 'A', 'B', 'B2', 'C', 'D']
if not only or 'train' in only:
    t = time.time(); b3d.reset((1000, 1050), 64); b3d.lights(4)
    x0 = min(cen[k][0] - r(k) for k in keys); x1 = max(cen[k][0] + r(k) for k in keys)
    y0 = min(cen[k][1] - r(k) for k in keys); y1 = max(cen[k][1] + r(k) for k in keys)
    b3d.stack_camera(((x0 + x1) / 2, (y0 + y1) / 2 - 0.25, 0.2), max(x1 - x0, y1 - y0) * 1.0, 0.0, 50.0)
    tags = build(keys, cen, ['S', 'A', 'B', 'B2', 'C', 'D'])
    json.dump(tags, open(f'{OUT}/train.json', 'w')); b3d.render(f'{OUT}/train.png'); print('train', round(time.time() - t, 1))
if not only or 'ex' in only:
    TEETH.update({'X': 12, 'Y': 6}); COL.update({'X': b3d.PAL['mint'], 'Y': b3d.PAL['coral']})
    c = {'X': (0, 0), 'Y': (M_ * 9, 0)}
    b3d.reset((700, 420), 48); b3d.lights(2)
    b3d.stack_camera((0.5, 0, 0.1), 2.6, 0.0, 55.0)
    hub = b3d.mat('hub', (0.15, 0.18, 0.24), rough=0.35, metal=0.8, coat=0)
    b3d.gear(12, M_, (0, 0, 0), 0.0, b3d.mat('x', COL['X'], coat=0.5), hub=hub)
    b3d.gear(6, M_, (c['Y'][0], 0, 0), b3d.mesh_angle(c['X'], 12, c['Y'], 6, 0.0, M_), b3d.mat('y', COL['Y'], coat=0.5), hub=hub)
    b3d.floor(); b3d.render(f'{OUT}/ex.png'); print('ex')
