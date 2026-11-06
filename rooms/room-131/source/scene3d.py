"""ROOM 131 3D sprites: front view of a dark light box with three windows. Behind each window a lamp panel carries a
digit; the window is covered by a stack of polarising sheets, shown as a row of tiles under it (a white bar = the
sheet's axis). p*: lamp off, every digit equally dim behind grey film. a*: lamp on; the window whose stack has no
right-angle neighbours glows with a mint frame, the others go black."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, lit
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
WX, WS, ZW, ZT, T = 2.05, 1.35, 1.95, 0.72, 0.42


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def matte(m):
    p = m.node_tree.nodes['Principled BSDF']; p.inputs['Roughness'].default_value = 1.0
    if 'Specular IOR Level' in p.inputs: p.inputs['Specular IOR Level'].default_value = 0.0
    return m


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def box(m, c, s, bev=0.02, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c, rotation=rot); o = bpy.context.object; o.scale = s; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev)
    return o


def scene(k, after):
    b = BOARDS[k]
    case = matte(b3d.mat('case', (0.03, 0.035, 0.05), rough=1, coat=0)); tile = matte(b3d.mat('tile', (0.12, 0.14, 0.2), rough=1, coat=0))
    bar = b3d.mat('bar', (0.95, 0.96, 1.0), rough=0.5, coat=0); glow(bar, (0.95, 0.96, 1.0), 0.8)
    off = matte(b3d.mat('off', (0.25, 0.27, 0.32), rough=1, coat=0)); dig_off = matte(b3d.mat('digoff', (0.025, 0.028, 0.04), rough=1, coat=0))
    on = b3d.mat('on', (1.0, 0.95, 0.8), rough=0.5, coat=0); glow(on, (1.0, 0.93, 0.75), 3.0); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    black = matte(b3d.mat('black', (0.004, 0.004, 0.006), rough=1, coat=0)); dig_dark = matte(b3d.mat('digdark', (0.02, 0.02, 0.03), rough=1, coat=0))
    film = b3d.mat('film', (0.3, 0.33, 0.4), rough=0.3, coat=0); film.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.35
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.0)
    box(case, (0, 0.2, 1.35), (6.6, 0.4, 2.7), 0.06)
    for i, w in enumerate(b):
        x = (i - 1) * WX; L = lit(w['s'])
        panel, dig = ((on, ink) if L else (black, dig_dark)) if after else (off, dig_off)
        box(panel, (x, -0.02, ZW), (WS, 0.04, WS), 0.0)
        text(str(w['d']), (x, -0.06, ZW), 0.95, dig)
        if not after: box(film, (x, -0.12, ZW), (WS + 0.08, 0.02, WS + 0.08), 0.0)
        if after and L:
            for dz in (-1, 1): box(mint, (x, -0.16, ZW + dz * (WS / 2 + 0.07)), (WS + 0.24, 0.04, 0.1), 0.0); box(mint, (x + dz * (WS / 2 + 0.07), -0.16, ZW), (0.1, 0.04, WS + 0.24), 0.0)
        n = len(w['s']); x0 = x - (n - 1) * (T + 0.06) / 2
        for j, ang in enumerate(w['s']):
            tx = x0 + j * (T + 0.06)
            box(tile, (tx, -0.04, ZT), (T, 0.04, T), 0.03)
            box(bar, (tx, -0.08, ZT), (T * 0.8 if ang % 90 == 0 else T * 1.0, 0.02, 0.05), 0.0, (0, math.radians(-ang), 0))
    b3d.stack_camera((0, 0, 1.35), 7.0, az=0.0, el=8.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 440), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
