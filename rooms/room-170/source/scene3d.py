"""ROOM 170 3D sprites: a round wall clock seen from the front with 60 small ticks and the numbers 1-12, its hands
taken off, and a digital tag on top showing the time. p*: no hands. a*: both hands in their true places (the hour hand
crept past its number) and the ticks between them glowing mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, ticks
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
R = 1.25


def box(loc, scale, m, rot=(0, 0, 0), bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 4)
    return o


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def at(tick, r):  # clock face lies in the x-z plane, facing -y; tick 0 at the top, clockwise
    a = tick / 60 * 2 * math.pi; return r * math.sin(a), r * math.cos(a)


def hand(tick, length, width, m, y):
    a = tick / 60 * 2 * math.pi; x, z = at(tick, length / 2)
    box((x, y, z), (width, 0.03, length), m, rot=(0, a, 0))


def scene(key, after):
    h, mnt = BOARDS[key]; th, tm = ticks(h, mnt)
    rim = b3d.mat('rim', (0.12, 0.13, 0.16), rough=0.4, coat=0.4); face = b3d.mat('face', (0.97, 0.96, 0.92), rough=0.6, coat=0)
    ink = b3d.mat('ink', (0.08, 0.08, 0.1), rough=0.6, coat=0); red = b3d.mat('red', (0.8, 0.1, 0.08), rough=0.4, coat=0)
    lcd = b3d.mat('lcd', (0.05, 0.06, 0.07), rough=0.3, coat=0.3); digit = glowm('digit', (1.0, 0.75, 0.2), 2.5)
    mint = glowm('mint', (0.15, 0.85, 0.6), 2.5)
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=R + 0.12, depth=0.16, location=(0, 0.05, 0), rotation=(math.pi / 2, 0, 0)); bpy.context.object.data.materials.append(rim)
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=R, depth=0.05, location=(0, -0.05, 0), rotation=(math.pi / 2, 0, 0)); bpy.context.object.data.materials.append(face)
    lo, hi = sorted((th, tm)); between = set()
    if hi - lo <= 30: between = set(range(lo + 1, hi))
    else: between = set(range(hi + 1, 60)) | set(range(0, lo))
    for k in range(60):
        big = k % 5 == 0; r0 = R - (0.17 if big else 0.1); x, z = at(k, (R - 0.04 + r0) / 2)
        box((x, -0.085, z), (0.035 if big else 0.018, 0.02, (R - 0.04) - r0), ink, rot=(0, k / 60 * 2 * math.pi, 0))
    for n in range(1, 13):
        x, z = at(n * 5, R - 0.36); text(str(n), (x, -0.09, z), 0.22, ink)
    if after:
        a0, a1 = (lo, hi) if hi - lo <= 30 else (hi, lo + 60)
        n = int((a1 - a0) * 8)
        for i in range(n + 1):
            tk = a0 + (a1 - a0) * i / max(n, 1); x, z = at(tk, R - 0.06)
            box((x, -0.11, z), (0.06, 0.02, 0.06), mint, rot=(0, tk / 60 * 2 * math.pi, 0))
        hand(th, R * 0.55, 0.09, ink, -0.12); hand(tm, R * 0.85, 0.05, red, -0.14)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.06, location=(0, -0.15, 0), rotation=(math.pi / 2, 0, 0)); bpy.context.object.data.materials.append(ink)
    box((0, 0, R + 0.5), (1.5, 0.18, 0.55), lcd, bev=0.04)
    text(f'{h}:{mnt:02d}', (0, -0.1, R + 0.5), 0.42, digit)
    b3d.stack_camera((0, 0, 0.4), 3.7, az=0.0, el=4.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((900, 1000), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
