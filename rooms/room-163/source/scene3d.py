"""ROOM 163 3D sprites: an open wooden drawer of single socks (red, blue, yellow, green) seen from above at a slant, with
a paper tag behind it naming the goal. p*: the full drawer. a*: the unluckiest draw: the pulled socks lie in a row in
front of the drawer in the order they came out, the last one (the sock that finally meets the goal) has a mint ring."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, SEQ
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
EL = 52.0; SX = 0.44
RGB = {'R': (0.9, 0.15, 0.13), 'B': (0.15, 0.4, 0.92), 'Y': (0.98, 0.8, 0.12), 'G': (0.2, 0.72, 0.3)}


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def box(loc, scale, m, bev=0.0, rz=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=(0, 0, rz)); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 5)
    return o


def sock(x, y, m, cuff, rz=0.0):
    c, s = math.cos(rz), math.sin(rz)
    def at(dx, dy): return (x + dx * c - dy * s, y + dx * s + dy * c)
    box((*at(0, 0.08), 0.07), (0.24, 0.52, 0.1), m, 0.09, rz)
    box((*at(0.07, -0.22), 0.07), (0.38, 0.22, 0.1), m, 0.09, rz)
    box((*at(0, 0.33), 0.075), (0.25, 0.08, 0.1), cuff, 0.04, rz)


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - EL + 20), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def scene(k, after):
    b = BOARDS[k]
    wood = b3d.mat('wood', (0.45, 0.28, 0.15), rough=0.7, coat=0); inner = b3d.mat('inner', (0.2, 0.13, 0.08), rough=0.9, coat=0)
    cuff = b3d.mat('cuff', (0.95, 0.95, 0.95), rough=0.6, coat=0); paper = b3d.mat('paper', (0.98, 0.93, 0.78), rough=0.7, coat=0)
    ink = b3d.mat('ink', (0.1, 0.08, 0.06), rough=0.8, coat=0); table = b3d.mat('table', (0.12, 0.13, 0.16), rough=0.8, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.4)
    M = {c: b3d.mat(c, v, rough=0.85, coat=0) for c, v in RGB.items()}
    # drawer: 6 x 2 slots
    DW, DD = 6 * SX + 0.3, 2 * 0.8 + 0.3
    box((0, 0.6, 0.04), (DW, DD, 0.08), inner)
    for sx in (-1, 1): box((sx * (DW / 2 + 0.05), 0.6, 0.2), (0.1, DD + 0.2, 0.4), wood, 0.02)
    for sy in (-1, 1): box((0, 0.6 + sy * (DD / 2 + 0.05), 0.2), (DW + 0.2, 0.1, 0.4), wood, 0.02)
    box((0, 0.6 - DD / 2 - 0.12, 0.26), (0.5, 0.06, 0.1), wood, 0.03)
    # tag behind the drawer
    o = box((0, 0.6 + DD / 2 + 0.35, 0.6), (2.9, 0.05, 0.75), paper, 0.03); o.rotation_euler = (math.radians(-20), 0, 0)
    text(b['tag'], (0, 0.6 + DD / 2 + 0.31, 0.62), 0.52, ink)
    socks = [c for c in b['socks'] for _ in range(b['socks'][c])]
    left = dict(b['socks'])
    if after:
        for c in SEQ[k]: left[c] -= 1
    inside = [c for c in b['socks'] for _ in range(left[c])]
    order = [c for c in socks]  # fixed slot order, pulled ones leave holes
    taken = dict((c, b['socks'][c] - left[c]) for c in b['socks'])
    slot = 0
    for c in order:
        x = (slot % 6 - 2.5) * SX; y = 0.6 + (0.4 if slot < 6 else -0.4)
        if taken[c] > 0 and after: taken[c] -= 1
        else: sock(x, y, M[c], cuff, 0.12 if slot % 2 else -0.08)
        slot += 1
    if after:
        n = len(SEQ[k])
        for i, c in enumerate(SEQ[k]):
            x = (i % 5 - 2) * 0.56; y = -0.95 - (i // 5) * 0.85
            sock(x, y, M[c], cuff)
            if i == n - 1:
                bpy.ops.mesh.primitive_torus_add(location=(x + 0.05, y - 0.05, 0.02), major_radius=0.36, minor_radius=0.03, major_segments=48)
                bpy.context.object.data.materials.append(mint)
    b3d.stack_camera((0, -0.1, 0.4), 4.5, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 1000), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
