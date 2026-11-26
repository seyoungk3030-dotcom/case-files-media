"""ROOM 209 3D sprites, true scale in metres: a two-lane road with a 1 m ruler along its edge, the skid start line at
x = 0. Back lane: the known car stopped at the end of its known skid (dark marks). Front lane: p* the car with its rear tyres on the start line,
braking (no marks yet); a* the car stopped at the end of the asked skid, marks glowing mint. Same camera for every board."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def box(m, loc, sc, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def car(x, y, col):
    body = b3d.mat(f'body{y}', col, rough=0.3, coat=0.8); glass = b3d.mat('glass', (0.1, 0.15, 0.22), rough=0.1, coat=0.5)
    tyre = b3d.mat('tyre', (0.05, 0.05, 0.06), rough=0.8, coat=0)
    box(body, (x - 2.0, y, 0.62), (4.0, 1.75, 0.7), 0.15)               # front bumper at x
    box(body, (x - 2.3, y, 1.18), (2.2, 1.55, 0.55), 0.18)
    box(glass, (x - 2.3, y, 1.2), (2.25, 1.57, 0.4), 0.12)
    box(glass, (x - 1.15, y, 1.12), (0.08, 1.4, 0.38), 0.03)
    for wx in (x - 0.8, x - 3.2):
        for wy in (y - 0.8, y + 0.8):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.33, depth=0.24, location=(wx, wy, 0.33), rotation=(math.pi / 2, 0, 0))
            bpy.context.object.data.materials.append(tyre)
    return


def marks(x0, x1, y, m):
    if x1 - x0 < 0.05: return
    for wy in (y - 0.8, y + 0.8): box(m, ((x0 + x1) / 2, wy, 0.012), (x1 - x0, 0.22, 0.01))


def scene(key, after):
    v0, d0, v1 = BOARDS[key]; d1 = GOOD[key]
    road = b3d.mat('road', (0.2, 0.21, 0.24), rough=0.85, coat=0); white = glowm('white', (1, 1, 1), 0.6, 0.5)
    box(road, (5.0, 0, -0.05), (16.0, 6.0, 0.1))
    for i in range(-2, 13): box(white, (i * 1.0 + 0.5 - 1.0, 0, 0.005), (0.5, 0.12, 0.01))   # centre dashes
    for i in range(0, 11):
        box(white, (i, -3.05, 0.006), (0.06, 0.5 if i % 5 == 0 else 0.28, 0.012))
    box(glowm('start', (1.0, 0.75, 0.2), 1.2), (0, 0, 0.007), (0.12, 6.0, 0.012))
    dark = b3d.mat('skid', (0.04, 0.04, 0.05), rough=0.9, coat=0); mint = glowm('mint', (0.2, 0.95, 0.65), 1.8)
    marks(0, d0, 1.5, dark); car(d0 + 3.2, 1.5, (0.55, 0.62, 0.72))     # rear tyres end their marks at x = d
    if after: marks(0, d1, -1.5, mint); car(d1 + 3.2, -1.5, (0.9, 0.22, 0.2))
    else: car(3.2, -1.5, (0.9, 0.22, 0.2))
    b3d.stack_camera((5.0, 0, 0.6), 15.5, az=6.0, el=52.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((900, 600), 48); b3d.lights(12)
        t0 = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t0, 1), flush=True)
