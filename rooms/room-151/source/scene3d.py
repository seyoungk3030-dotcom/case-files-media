"""ROOM 151 3D sprites: playing cards lying on green felt, seen from above at a slant. A card shows either a colour
(red or blue) or a black number on white. p*: the cards. a*: every card that must be turned over gets a mint frame and
lifts slightly at one end."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, MUST
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
EL = 58.0; CW, CH = 0.78, 1.1


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m, rx=0.0):
    bpy.ops.object.text_add(location=loc, rotation=(rx, 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.005; t.data.materials.append(m); return t


def box(m, c, s, rot=(0, 0, 0), bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.rotation_euler = rot; o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def scene(k, after):
    b = BOARDS[k]; must = set(MUST[k]); n = len(b); per = 4 if n > 6 else 3
    felt = b3d.mat('felt', (0.01, 0.09, 0.045), rough=1.0, coat=0); felt.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0
    white = b3d.mat('white', (0.85, 0.85, 0.82), rough=0.5, coat=0); ink = b3d.mat('ink', (0.03, 0.03, 0.04), rough=0.6, coat=0)
    red = b3d.mat('red', (0.8, 0.07, 0.07), rough=0.45, coat=0); blue = b3d.mat('blue', (0.08, 0.25, 0.85), rough=0.45, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.5)
    rows = (n + per - 1) // per
    box(felt, (0, 0, -0.04), (per * 1.05 + 0.6, rows * 1.4 + 0.5, 0.08), bev=0.06)
    for i, f in enumerate(b):
        r, c = divmod(i, per); cnt = min(per, n - r * per)
        x = (c - (cnt - 1) / 2) * 1.05; y = ((rows - 1) / 2 - r) * 1.4
        lift = after and i in must; tilt = math.radians(14) if lift else 0.0; z = 0.012 + (0.13 if lift else 0)
        box(white, (x, y, z), (CW, CH, 0.02), rot=(tilt, 0, 0), bev=0.05)
        if f in 'RB':
            box(red if f == 'R' else blue, (x, y, z + 0.012), (CW - 0.12, CH - 0.12, 0.004), rot=(tilt, 0, 0), bev=0.04)
        else:
            text(f, (x, y, z + 0.02), 0.62, ink, rx=tilt)
        if lift:
            for dx, dy, a, bb in ((0, CH / 2 + 0.05, CW + 0.14, 0.04), (0, -CH / 2 - 0.05, CW + 0.14, 0.04), (CW / 2 + 0.05, 0, 0.04, CH + 0.14), (-CW / 2 - 0.05, 0, 0.04, CH + 0.14)):
                box(mint, (x + dx, y + dy, 0.01), (a, bb, 0.02), bev=0.005)
    b3d.stack_camera((0, 0, 0.05), max(per * 1.05 + 0.9, 3.9), az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
