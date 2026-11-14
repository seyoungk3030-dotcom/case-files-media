"""ROOM 180 3D sprites: a 10-key section of a toy keyboard that starts on a random note, seen from the player's side.
One white key is pressed down and glows yellow. p*: question. a*: answer, every white key shows its solfege number
(도1 ... 시7) and the pressed key glows mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, N, BLACK_AFTER
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
KW, KL = 0.5, 2.4
BODY = {'A': (0.75, 0.15, 0.2), 'B': (0.15, 0.35, 0.7), 'C': (0.2, 0.5, 0.35), 'D': (0.85, 0.5, 0.12)}


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def box(loc, sc, m, rot=(0, 0, 0), bev=0.02):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = sc; o.data.materials.append(m)
    if bev:
        bpy.ops.object.modifier_add(type='BEVEL'); o.modifiers['Bevel'].width = bev; o.modifiers['Bevel'].segments = 2
    return o


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.005; t.data.materials.append(m)


def scene(k, after):
    s, press = BOARDS[k]
    ivory = b3d.mat('ivory', (0.96, 0.95, 0.92), rough=0.25, coat=0.6); ebony = b3d.mat('ebony', (0.05, 0.05, 0.06), rough=0.2, coat=0.8)
    body = b3d.mat('body', BODY[k], rough=0.35, coat=0.5); ink = b3d.mat('ink', (0.08, 0.08, 0.1), rough=0.5, coat=0)
    yel = glowm('yel', (1.0, 0.78, 0.15), 1.4); mint = glowm('mint', (0.15, 0.85, 0.6), 1.4)
    W = N * KW; x0 = -W / 2
    box((0, 0.35, -0.2), (W + 0.7, KL + 1.3, 0.3), body, bev=0.08)        # case
    box((0, KL / 2 + 0.45, 0.1), (W + 0.7, 0.6, 0.35), body, bev=0.06)    # back panel
    for side in (-1, 1):
        box((side * (W / 2 + 0.2), 0.1, 0.05), (0.32, KL + 0.4, 0.25), body, bev=0.05)  # cheek blocks
    for i in range(N):
        cx = x0 + KW * (i + 0.5); down = i == press
        m = (mint if after else yel) if down else ivory
        rot = (0, 0, 0)
        box((cx, 0, 0.0 - (0.07 if down else 0)), (KW - 0.04, KL, 0.22), m, rot)
        if after:
            text(str((s + i) % 7 + 1), (cx, -KL / 2 + 0.3, 0.13 - (0.05 if down else 0)), 0.3, ink)
    for j in range(N - 1):
        if (s + j) % 7 in BLACK_AFTER:
            box((x0 + KW * (j + 1), 0.45, 0.2), (0.3, 1.45, 0.2), ebony)
    b3d.stack_camera((0, 0.25, 0), 6.4, az=0.0, el=55.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((1000, 620), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
