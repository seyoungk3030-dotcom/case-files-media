"""ROOM 067 3D sprites: front view, springs hanging from a wooden ceiling bar (series = one under another, parallel = two
side by side holding a small bar), a stack of weights, and a tile ruler on the right whose 0 is the weight's bottom before
loading (0.2 per tile). p*: springs at rest, '추 N개'. a*: every stage stretched, weight bottom on the answer tick (amber)."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, res
from fractions import Fraction as F
EX = (('s',), 2)   # rules-card example: one spring, 2 weights -> 2 tiles
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U, LS, CON, PH, TOP = 0.2, 0.55, 0.08, 0.11, 0.0
X90 = (math.radians(90), 0, 0)


def label(s, x, z, size, m, y=-0.4, ax='CENTER'):
    bpy.ops.object.text_add(location=(x, y, z), rotation=X90); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = ax; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def box(loc, scale, m, bev=0.015):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 2); return o


def spring(x, z0, length, m, coils=5, r=0.11, wire=0.022):
    cu = bpy.data.curves.new('spr', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = wire; cu.bevel_resolution = 4
    sp = cu.splines.new('POLY'); n = coils * 24; sp.points.add(n)
    for i in range(n + 1):
        t = i / n; a = 2 * math.pi * coils * t
        sp.points[i].co = (x + r * math.cos(a), r * math.sin(a), z0 - length * t, 1)
    o = bpy.data.objects.new('spr', cu); bpy.context.collection.objects.link(o); o.data.materials.append(m)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.05, location=(x, 0, z0 + 0.02)); bpy.context.object.data.materials.append(m)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.05, location=(x, 0, z0 - length - 0.02)); bpy.context.object.data.materials.append(m)


def rig(stages, w, after, M):
    z = TOP
    for st in stages:
        s = F(w, 2) if st == 's' and False else (F(w, 2) if st == 'p' else F(w))
        L = LS + (float(s) * U if after else 0)
        if st == 's':
            spring(0, z, L, M['spring']); z -= L + CON
            bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.035, location=(0, 0, z + CON / 2))
            bpy.context.object.data.materials.append(M['bar'])
        else:
            for xx in (-0.2, 0.2): spring(xx, z, L, M['spring'])
            z -= L + 0.04; box((0, 0, z), (0.56, 0.12, 0.05), M['bar']); z -= CON
    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=CON, location=(0, 0, z + CON / 2)); bpy.context.object.data.materials.append(M['steel'])
    for i in range(w):
        box((0, 0, z - PH * (i + 0.5)), (0.34, 0.24, PH * 0.9), M['coral'] if i % 2 == 0 else M['coral2'], 0.02)
    return z - PH * w


def rest_bottom(stages, w):
    z = TOP
    for st in stages: z -= LS + CON + (0.04 if st == 'p' else 0)
    return z - PH * w


def scene(k, after):
    stages, w = EX if k == 'X' else BOARDS[k]
    M = {'spring': b3d.mat('spring', b3d.PAL['mint'], rough=0.25, metal=0.3, coat=0.5), 'steel': b3d.mat('steel', (0.80, 0.83, 0.88), rough=0.25, metal=1.0, coat=0.0), 'bar': b3d.mat('bar', (0.30, 0.34, 0.42), rough=0.4),
         'coral': b3d.mat('coral', (0.90, 0.30, 0.24), rough=0.35, coat=0.5), 'coral2': b3d.mat('coral2', (0.96, 0.45, 0.35), rough=0.35, coat=0.5)}
    wood = b3d.mat('wood', (0.45, 0.32, 0.22), rough=0.6, coat=0.1); tick = b3d.mat('tick', (0.85, 0.88, 0.94), rough=0.5)
    amber = b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3); white = b3d.mat('white', (0.96, 0.97, 0.99), rough=0.4)
    soft = b3d.mat('soft', (0.70, 0.75, 0.85), rough=0.5); mint = b3d.mat('mint', b3d.PAL['mint'], rough=0.3, coat=0.5)
    for p in (amber, mint):
        q = p.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
        q.inputs['Emission Strength'].default_value = 0.5
    box((0.1, 0, TOP + 0.07), (1.5, 0.4, 0.14), wood, 0.03)
    z0 = rest_bottom(stages, w); d = 2 if k == 'X' else res[k]
    bot = rig(stages, w, after, M)
    box((0.62, 0, z0 - 4.5 * U), (0.05, 0.05, 9.6 * U), M['bar'], 0.01)
    for i in range(10):
        hot = after and i == d
        box((0.56, -0.04, z0 - i * U), (0.12 if not hot else 0.2, 0.03, 0.018 if not hot else 0.03), amber if hot else tick, 0.004)
        label(str(i), 0.76, z0 - i * U, 0.2, amber if hot else soft, ax='LEFT')
    if after:
        label(f'{d}칸', -0.6, bot + 0.05, 0.3, amber)
    else:
        label(f'추 {w}개', -0.66, z0 + PH * w / 2, 0.24, white)
        box((0.0, -0.13, z0), (0.9, 0.005, 0.006), mint, 0.001)
    b3d.stack_camera((0.12, 0, -1.95), 4.6, az=0.0, el=3.0)


only = sys.argv[1:]
for k in 'ABCDX':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((640, 1000), 40); b3d.lights(5)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
