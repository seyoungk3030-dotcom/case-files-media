"""ROOM 160 3D sprites: a 6x6 parking lot seen from above at a slant, low walls with a gap on the right of row 2 (the
exit, mint arrow outside). Cars are rounded blocks two or three cells long; the red car must get out. p*: the start.
a*: the lot after the shortest solution: the red car glows mint outside the exit, cars that had to move keep their
colour, cars that never moved turn grey."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, PATH, MOVED, N
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
S = 0.62; EL = 58.0
COLS = [(0.2, 0.45, 0.95), (0.98, 0.7, 0.15), (0.55, 0.3, 0.9), (0.2, 0.75, 0.85), (0.95, 0.45, 0.7), (0.45, 0.8, 0.3), (0.95, 0.55, 0.25)]


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def box(loc, scale, m, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 4)
    return o


def X(k): return (k - (N - 1) / 2) * S
def Y(r): return ((N - 1) / 2 - r) * S


def car(o, l, r, k, m, glass):
    cx = X(k + (l - 1) / 2) if o == 'h' else X(k); cy = Y(r) if o == 'h' else Y(r + (l - 1) / 2)
    lx, ly = (l * S - 0.1, S - 0.12) if o == 'h' else (S - 0.12, l * S - 0.1)
    box((cx, cy, 0.17), (lx, ly, 0.26), m, 0.08)
    gx, gy = (lx * 0.55, ly * 0.8) if o == 'h' else (lx * 0.8, ly * 0.55)
    box((cx, cy, 0.33), (gx, gy, 0.1), glass, 0.04)


def scene(k, after):
    lot = b3d.mat('lot', (0.2, 0.21, 0.24), rough=0.85, coat=0); line = b3d.mat('line', (0.85, 0.85, 0.8), rough=0.6, coat=0)
    wall = b3d.mat('wall', (0.55, 0.57, 0.62), rough=0.6, coat=0); glass = b3d.mat('glass', (0.08, 0.1, 0.14), rough=0.15, coat=0.5)
    red = b3d.mat('red', (0.92, 0.12, 0.1), rough=0.3, coat=0.4); grey = b3d.mat('grey', (0.32, 0.33, 0.36), rough=0.7, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.6)
    bodies = [b3d.mat(f'c{i}', c, rough=0.3, coat=0.4) for i, c in enumerate(COLS)]
    W = N * S
    box((0, 0, -0.04), (W, W, 0.08), lot)
    for i in range(1, N):
        box((X(i) - S / 2, 0, 0.003), (0.012, W, 0.006), line); box((0, Y(i) + S / 2, 0.003), (W, 0.012, 0.006), line)
    t = 0.14; h = 0.3
    box((0, W / 2 + t / 2, h / 2), (W + 2 * t, t, h), wall, 0.03); box((0, -W / 2 - t / 2, h / 2), (W + 2 * t, t, h), wall, 0.03)
    box((-W / 2 - t / 2, 0, h / 2), (t, W, h), wall, 0.03)
    top = Y(2) + S / 2; bot = Y(2) - S / 2
    box((W / 2 + t / 2, (W / 2 + top) / 2, h / 2), (t, W / 2 - top, h), wall, 0.03)
    box((W / 2 + t / 2, (bot - W / 2) / 2, h / 2), (t, bot + W / 2, h), wall, 0.03)
    # exit arrow outside the gap
    if not after:
        bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.22, depth=0.04, location=(W / 2 + 0.45, Y(2), 0.02), rotation=(0, 0, -math.pi / 2))
        bpy.context.object.data.materials.append(mint)
    cars = BOARDS[k]; st = PATH[k][-1] if after else PATH[k][0]
    for i, (o, l, _, _) in enumerate(cars):
        r, c = st[i]
        if i == 0:
            car(o, l, r, c + (1.6 if after else 0), mint if after else red, glass)
        else:
            car(o, l, r, c, (bodies[(i - 1) % len(bodies)] if (not after or i in MOVED[k]) else grey), glass)
    b3d.stack_camera((0.55, 0.1, 0), W + 1.9, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 900), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
