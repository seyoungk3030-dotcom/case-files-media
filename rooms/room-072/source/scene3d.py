"""ROOM 072 3D sprites: front view of a 5-wide block well. p*: the stack (slate cubes) and the coral piece above its drop
column with a down arrow. a*: what is left after the full rows vanish (cubes in mint), 'N개' amber on top."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, PIECES, R, res, W
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
C = 0.3; X90 = (math.radians(90), 0, 0); TOPROW = 9


def label(s, x, z, size, m, y=-0.3):
    bpy.ops.object.text_add(location=(x, y, z), rotation=X90); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def box(loc, scale, m, bev=0.02):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def cell(x, y, m): box(((x - (W - 1) / 2) * C, 0, (y + 0.5) * C), (C * 0.94, C * 0.94, C * 0.94), m, 0.035)


def glow(m, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
    q.inputs['Emission Strength'].default_value = s; return m


def scene(k, after):
    rows, piece, col = BOARDS[k]
    slate = b3d.mat('slate', (0.42, 0.50, 0.68), rough=0.3, coat=0.6); coral = b3d.mat('coral', (0.92, 0.32, 0.26), rough=0.3, coat=0.6)
    mint = b3d.mat('mint', b3d.PAL['mint'], rough=0.3, coat=0.6); frame = b3d.mat('frame', (0.30, 0.34, 0.44), rough=0.4)
    back = b3d.mat('back', (0.12, 0.15, 0.22), rough=0.7, coat=0); amber = glow(b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3), 0.7)
    white = b3d.mat('white', (0.96, 0.97, 0.99), rough=0.4)
    w = W * C; h = TOPROW * C
    box((0, 0.2, h / 2), (w, 0.04, h), back, 0.005)
    for sgn in (-1, 1): box((sgn * (w / 2 + 0.06), 0, h / 2), (0.12, 0.42, h + 0.12), frame, 0.03)
    box((0, 0, -0.06), (w + 0.24, 0.42, 0.12), frame, 0.03)
    if after:
        for x, y in R[k][2]: cell(x, y, mint)
        top = max([y for _, y in R[k][2]] + [-1]) + 1
        label(f'{res[k]}개', 0, top * C + 0.32, 0.3, amber)
    else:
        for y, r in enumerate(rows):
            for x, ch in enumerate(r):
                if ch == 'X': cell(x, y, slate)
        base = TOPROW - 1 - max(dy for _, dy in PIECES[piece])
        for dx, dy in PIECES[piece]: cell(col + dx, base + dy, coral)
        xs = [col + dx for dx, _ in PIECES[piece]]; xm = ((min(xs) + max(xs)) / 2 - (W - 1) / 2) * C
        label('↓', xm, (base - 0.6) * C, 0.32, white)
    b3d.stack_camera((0, 0, 1.38), 3.15, az=0.0, el=4.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((700, 1000), 40); b3d.lights(5)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
