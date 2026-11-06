"""ROOM 083 3D sprites: a glass water tank; five blocks built from 1 cm cubes with a weight tag above each. p*: the
blocks wait in a row on the rim above the water. a*: the blocks dropped in: floaters sit at the surface sunk by the
fraction weight/volume and glow amber, sinkers lie on the bottom and turn grey."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import TANKS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
X90 = (math.radians(90), 0, 0)
U = 0.42
COLS = [(0.85, 0.2, 0.3), (0.15, 0.4, 0.9), (0.1, 0.6, 0.35), (0.55, 0.25, 0.85), (0.9, 0.5, 0.1)]


def box(loc, scale, m, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def label(s, x, z, size, m, y=-0.3):
    bpy.ops.object.text_add(location=(x, y, z), rotation=X90); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def glassy(name, col, a):
    m = b3d.mat(name, col, rough=0.08, coat=0.8); p = m.node_tree.nodes['Principled BSDF']; p.inputs['Alpha'].default_value = a
    try: m.surface_render_method = 'BLENDED'
    except Exception: m.blend_method = 'BLEND'
    return m


def block(x, z0, s, m):
    for i in range(s):
        for j in range(s):
            for kk in range(s): box((x + (i - (s - 1) / 2) * U, (j - (s - 1) / 2) * U, z0 + (kk + 0.5) * U), (U * 0.97, U * 0.97, U * 0.97), m, 0.035)


def scene(k, after):
    blocks = TANKS[k]; W, H, WL = 7.6, 2.0, 1.55
    water = glassy('water', (0.35, 0.65, 0.98), 0.35); glass = glassy('glass', (0.85, 0.92, 1.0), 0.12)
    tag = b3d.mat('tag', (0.97, 0.98, 1.0), rough=0.4); ink = b3d.mat('ink', (0.06, 0.09, 0.18), rough=0.4)
    grey = b3d.mat('grey', (0.45, 0.48, 0.55), rough=0.5); rim = b3d.mat('rim', (0.3, 0.33, 0.42), rough=0.4)
    hot = b3d.mat('hot', (0.98, 0.66, 0.12), rough=0.3); q = hot.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (0.98, 0.66, 0.12, 1); q.inputs['Emission Strength'].default_value = 0.4
    if after:
        box((0, 0, H / 2), (W, 1.6, H), glass, 0.05); box((0, 0, WL / 2), (W - 0.08, 1.52, WL), water, 0.03)
        box((0, 0, -0.06), (W + 0.2, 1.8, 0.12), rim, 0.03)
    else:
        box((0, 0, -0.06), (W, 1.2, 0.12), rim, 0.03)
    wd = [max(s * U, 1.0) for s, g in blocks]; tot = sum(wd) + 0.3 * (len(wd) - 1); x = -tot / 2; xs = []
    for w in wd: xs.append(x + w / 2); x += w + 0.3
    for i, ((s, g), bx) in enumerate(zip(blocks, xs)):
        h = s * U; fl = g < s ** 3
        if not after: z0 = 0.0
        elif fl: z0 = WL - h * g / s ** 3
        else: z0 = 0.02
        m = b3d.mat(f'c{i}', COLS[i], rough=0.35, coat=0.5)
        block(bx, z0, s, (hot if fl else grey) if after else m)
        gtxt = (f'{g:g}g')
        ty = (H + 0.05 if after else 0.0) + 3 * U + 0.4
        box((bx, -0.25, ty), (0.95, 0.05, 0.42), tag, 0.06); label(gtxt, bx, ty, 0.3, ink, -0.29)
    if after: b3d.stack_camera((0, 0, 1.95), 9.6, az=0.0, el=10.0)
    else: b3d.stack_camera((0, 0, 0.85), 9.6, az=0.0, el=10.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1300, 560) if after else (1300, 300), 40); b3d.lights(6)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
