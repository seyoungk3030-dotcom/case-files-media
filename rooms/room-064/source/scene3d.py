"""ROOM 064 3D sprites: a row of eight bar magnets (red N / blue S halves, letters on the front face).
'pA'..'pD' = row as placed (evenly spaced). 'aA'..'aD' = after settling: sticking magnets close up, pushing ends open wide gaps."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import ROWS, OPP, joints
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
L, W, Hh = 0.9, 0.34, 0.3


def label(s, x, z, size, m):
    bpy.ops.object.text_add(location=(x, -W / 2 - 0.005, z), rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.005; t.data.materials.append(m)


def half(x, pole, M):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, Hh / 2)); o = bpy.context.object
    o.scale = (L / 2, W, Hh); o.data.materials.append(M[pole]); b3d.bevel(o, 0.02, 2)
    label(pole, x, Hh / 2, 0.22, M['txt'])


def scene(k, after):
    s = ROWS[k]
    M = {'N': b3d.mat('N', (0.88, 0.22, 0.20), rough=0.3, coat=0.5), 'S': b3d.mat('S', (0.18, 0.42, 0.90), rough=0.3, coat=0.5),
         'txt': b3d.mat('txt', (0.97, 0.97, 0.99), rough=0.4)}
    js = joints(s); xs = [0.0]
    for j in js: xs.append(xs[-1] + L + ((0.0 if j else 0.55) if after else 0.12))
    off = (xs[-1] + L) / 2
    for x0, p in zip(xs, s):
        x = x0 - off
        half(x + L / 4, p, M); half(x + 3 * L / 4, OPP[p], M)
    span = xs[-1] + L
    b3d.stack_camera((0, 0, 0.1), span + 0.5, az=0.0, el=28.0)
    b3d.floor().location.z = -0.01


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1400, 260), 40); b3d.lights(8)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
