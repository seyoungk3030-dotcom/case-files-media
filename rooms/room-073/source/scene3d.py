"""ROOM 073 3D sprites: a row of parking spaces seen from the aisle at our side. The numbers are painted for drivers on the
far side, so the real number text is rotated 180 degrees on the asphalt. A coral car covers one space ('?' on its roof).
a*: the car is gone, the hidden space shows its painted number in amber."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import REAL, HIDDEN
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
SW, SD = 0.95, 1.7


def text(s, loc, size, m, rz=0.0):
    bpy.ops.object.text_add(location=loc, rotation=(0, 0, rz)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.005; t.data.materials.append(m)


def box(loc, scale, m, bev=0.02):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def glow(m, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
    q.inputs['Emission Strength'].default_value = s; return m


def car(x, y, M):
    box((x, y, 0.28), (SW * 0.78, SD * 0.86, 0.32), M['body'], 0.1)
    box((x, y + 0.08, 0.56), (SW * 0.66, SD * 0.46, 0.28), M['body'], 0.09)
    box((x, y + 0.08, 0.565), (SW * 0.68, SD * 0.40, 0.2), M['glass'], 0.06)
    for dx in (-1, 1):
        for dy in (-1, 1):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.1, location=(x + dx * SW * 0.39, y + dy * SD * 0.28, 0.15), rotation=(0, math.radians(90), 0))
            bpy.context.object.data.materials.append(M['tyre'])
    text('?', (x, y + 0.08, 0.72), 0.42, M['white'])


def scene(k, after):
    real = REAL[k]; n = len(real)
    M = {'body': b3d.mat('body', (0.92, 0.32, 0.26), rough=0.25, coat=0.8), 'glass': b3d.mat('glass', (0.10, 0.14, 0.22), rough=0.1, coat=0.8),
         'tyre': b3d.mat('tyre', (0.05, 0.05, 0.06), rough=0.7), 'white': b3d.mat('white', (0.97, 0.98, 1.0), rough=0.4)}
    asphalt = b3d.mat('asph', (0.16, 0.17, 0.20), rough=0.85, coat=0); paint = b3d.mat('paint', (0.95, 0.95, 0.92), rough=0.6, coat=0)
    amber = glow(b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3), 0.8)
    W = n * SW
    box((0, 0.1, -0.03), (W + 0.6, SD + 1.0, 0.06), asphalt, 0.01)
    for i in range(n + 1): box((-W / 2 + i * SW, 0.0, 0.002), (0.05, SD, 0.004), paint, 0.002)
    box((0, SD / 2, 0.002), (W, 0.05, 0.004), paint, 0.002)
    for i, num in enumerate(reversed(real)):   # our left = the driver's right
        x = -W / 2 + (i + 0.5) * SW
        hid = num == HIDDEN[k]
        if hid and not after: car(x, 0.0, M); continue
        text(f'{num:02d}', (x, -0.35, 0.006), 0.5, amber if hid else paint, rz=math.pi)
    b3d.stack_camera((0, -0.05, 0.2), W + 0.8, az=0.0, el=62.0)


only = sys.argv[1:]
for k in 'AB':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1200, 700), 48); b3d.lights(6)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
