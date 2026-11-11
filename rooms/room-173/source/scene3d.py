"""ROOM 173 3D sprites: a pocket calculator or a desk phone lying on the table, seen from the front and above. The
digits are rubbed off every number key; symbol keys (÷ × − + = . on the calculator, * # on the phone) keep their
marks, the calculator has its display and the phone its handset. One key is pressed down and glows yellow.
p*: blank digits. a*: every digit printed back, the pressed key mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, PADS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
P = 0.52; K = 0.42  # key pitch and key size


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def box(loc, scale, m, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 4)
    return o


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.008; t.data.materials.append(m)


def scene(k, after):
    kind, pr, pc = BOARDS[k]; pad = PADS[kind]; rows, cols = len(pad), len(pad[0])
    calc = kind == 'calc'
    shell = b3d.mat('shell', (0.16, 0.17, 0.2) if calc else (0.9, 0.9, 0.88), rough=0.4, coat=0.4)
    keym = b3d.mat('key', (0.93, 0.93, 0.95) if calc else (0.3, 0.32, 0.36), rough=0.4, coat=0.5)
    opm = b3d.mat('op', (0.38, 0.42, 0.5) if calc else (0.3, 0.32, 0.36), rough=0.4, coat=0.5)
    ink = b3d.mat('ink', (0.08, 0.08, 0.1) if calc else (0.97, 0.97, 0.97), rough=0.5, coat=0)
    white = b3d.mat('white', (0.98, 0.98, 0.98), rough=0.5, coat=0)
    hot = glowm('hot', (0.15, 0.85, 0.6), 0.6) if after else glowm('hot', (1.0, 0.62, 0.0), 0.5)
    dark = b3d.mat('dark', (0.05, 0.05, 0.07), rough=0.5, coat=0)
    lcd = b3d.mat('lcd', (0.55, 0.62, 0.5), rough=0.5, coat=0.2)
    W = cols * P + 0.3; top = 1.25 if calc else 1.05; Hh = rows * P + 0.3 + top
    y0 = -Hh / 2 + 0.15 + P / 2  # centre of the bottom key row
    box((0, 0, -0.1), (W, Hh, 0.2), shell, bev=0.08)
    if calc:
        box((0, Hh / 2 - 0.15 - 0.42, 0.01), (W - 0.4, 0.62, 0.04), lcd, bev=0.02)
    else:  # handset lying above the keys, its cord curling down the side
        hs = b3d.mat('hs', (0.25, 0.27, 0.31), rough=0.4, coat=0.4)
        yc = Hh / 2 - 0.15 - 0.4  # handset resting in its cradle on top of the body
        box((0, yc, 0.08), (W - 0.55, 0.3, 0.16), hs, bev=0.07)
        for sx in (-1, 1): box((sx * (W / 2 - 0.42), yc, 0.14), (0.42, 0.62, 0.22), hs, bev=0.1)
    for r in range(rows):
        for c in range(cols):
            lab = pad[r][c]; x = (c - (cols - 1) / 2) * P; y = y0 + (rows - 1 - r) * P
            pressed = (r, c) == (pr, pc); z = 0.02 if pressed else 0.08
            m = hot if pressed else (opm if not lab.isdigit() and calc and lab != '.' else keym)
            box((x, y, z), (K, K, 0.12), m, bev=0.04)
            if not lab.isdigit() or after:
                text(lab, (x, y - 0.01, z + 0.065), 0.26, white if (calc and m is opm) else (dark if pressed else ink))
    b3d.stack_camera((0, 0.15, 0), 3.4, az=0.0, el=58.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((900, 1000), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
