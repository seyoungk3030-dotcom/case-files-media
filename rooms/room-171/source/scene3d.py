"""ROOM 171 3D sprites: a wooden tic-tac-toe board seen from above at a slant, red X pieces and blue O rings, the empty
cells carrying their number 1-9, and a small 'O 차례' tag. p*: the position. a*: a ghost blue O with a mint ring on the
best cell."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
EL = 58.0; C = 0.82


def box(loc, scale, m, rz=0.0, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=(0, 0, rz)); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 4)
    return o


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(0, 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.005; t.data.materials.append(m)


def glowm(name, c, s, alpha=1.0):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    if alpha < 1: q.inputs['Alpha'].default_value = alpha
    return m


def xpiece(x, y, m):
    box((x, y, 0.16), (0.62, 0.14, 0.16), m, math.pi / 4, 0.04); box((x, y, 0.165), (0.62, 0.14, 0.17), m, -math.pi / 4, 0.0)


def opiece(x, y, m):
    bpy.ops.mesh.primitive_torus_add(location=(x, y, 0.16), major_radius=0.24, minor_radius=0.08, major_segments=48); bpy.context.object.data.materials.append(m)


def scene(key, after):
    b = BOARDS[key]
    wood = b3d.mat('wood', (0.78, 0.58, 0.36), rough=0.6, coat=0); line = b3d.mat('line', (0.35, 0.2, 0.1), rough=0.6, coat=0)
    red = b3d.mat('red', (0.85, 0.12, 0.1), rough=0.3, coat=0.5); blue = b3d.mat('blue', (0.1, 0.35, 0.9), rough=0.3, coat=0.5)
    num = b3d.mat('num', (0.45, 0.3, 0.18), rough=0.7, coat=0); mint = glowm('mint', (0.15, 0.85, 0.6), 2.2)
    paper = b3d.mat('paper', (0.98, 0.93, 0.78), rough=0.7, coat=0); ink = b3d.mat('ink', (0.1, 0.08, 0.06), rough=0.8, coat=0)
    box((0, 0, 0), (3 * C + 0.3, 3 * C + 0.3, 0.12), wood, bev=0.05)
    for i in (-0.5, 0.5):
        box((i * C, 0, 0.07), (0.05, 3 * C, 0.02), line); box((0, i * C, 0.07), (3 * C, 0.05, 0.02), line)
    for idx, ch in enumerate(b):
        r, c = divmod(idx, 3); x, y = (c - 1) * C, (1 - r) * C
        if ch == 'X': xpiece(x, y, red)
        elif ch == 'O': opiece(x, y, blue)
        elif after and idx + 1 == GOOD[key]:
            opiece(x, y, blue)
            bpy.ops.mesh.primitive_torus_add(location=(x, y, 0.08), major_radius=0.37, minor_radius=0.03, major_segments=48); bpy.context.object.data.materials.append(mint)
        else: text(str(idx + 1), (x, y, 0.07), 0.34, num)
    box((0, 1.9, 0.12), (1.5, 0.5, 0.06), paper, bev=0.03)
    text('O 차례', (0, 1.9, 0.16), 0.3, ink)
    b3d.stack_camera((0, 0.3, 0), 3.7, az=0.0, el=EL)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((900, 1000), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
