"""ROOM 184 3D sprites: a hardcover book lying open on a desk, some sheets torn out between the two visible pages.
Page numbers sit in the bottom outer corners (even on the left, odd on the right). p*: question. a*: answer, the torn
sheets float above the book, each showing its front/back page numbers."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
COVER = {'A': (0.6, 0.12, 0.12), 'B': (0.1, 0.3, 0.6), 'C': (0.15, 0.45, 0.25), 'D': (0.45, 0.25, 0.55)}
PW, PD = 1.6, 2.2


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def box(loc, sc, m, rot=(0, 0, 0), bev=0.01):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = sc; o.data.materials.append(m)
    if bev:
        bpy.ops.object.modifier_add(type='BEVEL'); o.modifiers['Bevel'].width = bev; o.modifiers['Bevel'].segments = 2
    return o


def text(s, loc, size, m, rot=(0, 0, 0)):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.004; t.data.materials.append(m); return t


def scene(k, after):
    L, R = BOARDS[k]
    cover = b3d.mat('cover', COVER[k], rough=0.5, coat=0.3); paper = b3d.mat('paper', (0.82, 0.8, 0.74), rough=0.7, coat=0)
    edge = b3d.mat('edge', (0.88, 0.85, 0.76), rough=0.8, coat=0); line = b3d.mat('line', (0.62, 0.62, 0.64), rough=0.8, coat=0)
    ink = b3d.mat('ink', (0.08, 0.08, 0.1), rough=0.5, coat=0); mintp = glowm('mintp', (0.45, 0.9, 0.7), 0.12)
    box((0, 0, 0.02), (2 * PW + 0.3, PD + 0.25, 0.04), cover)
    for side in (-1, 1):
        cx = side * (PW / 2 + 0.03); tilt = 0.0
        box((cx, 0, 0.11), (PW, PD, 0.14), edge, rot=(0, tilt, 0))
        box((cx, 0, 0.181), (PW - 0.02, PD - 0.02, 0.004), paper, rot=(0, tilt, 0), bev=0)
        for j in range(9):  # lines of text
            ln = PW - 0.45 if j % 4 != 3 else PW * 0.5
            box((cx - (PW - 0.45 - ln) / 2, 0.75 - j * 0.17, 0.19), (ln, 0.05, 0.004), line, rot=(0, tilt, 0), bev=0)
        num = L if side < 0 else R
        text(str(num), (cx + side * (PW / 2 - 0.3), -PD / 2 + 0.25, 0.19), 0.3, ink)
    if after:
        miss = list(range(L + 1, R)); sheets = [(miss[i], miss[i + 1]) for i in range(0, len(miss), 2)]; n = len(sheets)
        for i, (a, b) in enumerate(sheets):
            x = (i - (n - 1) / 2) * 0.82
            box((x, 0.35, 0.75), (0.7, 0.8, 0.01), mintp, rot=(math.radians(8), 0, math.radians(6 * (i % 2 * 2 - 1))))
            text(f'{a}·{b}', (x, 0.35, 0.77), 0.22, ink, rot=(math.radians(8), 0, math.radians(6 * (i % 2 * 2 - 1))))
    b3d.stack_camera((0, 0.05, 0.25), 4.3, az=0.0, el=55.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((960, 640), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
