"""ROOM 104 3D sprites: an upright blue drop-disc rack (7 columns x 6 rows of round holes) with red and yellow discs
resting at the bottom of each column, column numbers on top. a*: red's winning disc sits in its column and a glowing
mint bar runs through the four in a row."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, C, RN
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.04; t.data.materials.append(m)


def X(c): return c - (C - 1) / 2


def Z(r): return 0.75 + r


def disc(c, r, m):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.39, depth=0.2, location=(X(c), 0, Z(r)), rotation=(math.radians(90), 0, 0), vertices=48)
    o = bpy.context.object; o.data.materials.append(m); b3d.bevel(o, 0.03)


def scene(k, after):
    blue = b3d.mat('blue', (0.025, 0.10, 0.36), rough=0.45, coat=0.3); red = b3d.mat('red', (0.72, 0.04, 0.03), rough=0.35, coat=0.3)
    yel = b3d.mat('yel', (0.90, 0.62, 0.03), rough=0.35, coat=0.3); white = b3d.mat('white', (0.92, 0.93, 0.96), rough=0.5, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.5)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.25 + RN / 2)); fr = bpy.context.object; fr.scale = (C + 0.4, 0.34, RN + 0.5)
    fr.data.materials.append(blue)
    for c in range(C):
        for r in range(RN):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=1, location=(X(c), 0, Z(r)), rotation=(math.radians(90), 0, 0), vertices=48)
            h = bpy.context.object; mod = fr.modifiers.new('h', 'BOOLEAN'); mod.object = h; mod.operation = 'DIFFERENCE'; mod.solver = 'MANIFOLD'
            bpy.context.view_layer.objects.active = fr; bpy.ops.object.modifier_apply(modifier=mod.name); bpy.data.objects.remove(h)
    b3d.bevel(fr, 0.03)
    for side in (-1, 1):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(side * (C / 2 + 0.35), 0, 0.2)); o = bpy.context.object; o.scale = (0.5, 1.4, 0.4)
        o.data.materials.append(blue); b3d.bevel(o, 0.05)
    for r, row in enumerate(BOARDS[k]):
        for c, ch in enumerate(row):
            if ch != '.': disc(c, r, red if ch == 'R' else yel)
    for c in range(C): text(str(c + 1), (X(c), 0, Z(RN) + 0.15), 0.62, white)
    if after:
        col, row, line = RES[k][0]; disc(col - 1, row, red)
        (r0, c0), (r1, c1) = line[0][0], line[0][-1]
        a, b = Vector((X(c0), -0.28, Z(r0))), Vector((X(c1), -0.28, Z(r1))); d = b - a; a -= d.normalized() * 0.35; b += d.normalized() * 0.35; d = b - a
        bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=d.length, location=(a + b) / 2, vertices=24); o = bpy.context.object
        o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized()); o.data.materials.append(mint)
        bpy.ops.mesh.primitive_torus_add(location=(X(col - 1), -0.12, Z(row)), rotation=(math.radians(90), 0, 0), major_radius=0.45, minor_radius=0.05)
        bpy.context.object.data.materials.append(mint)
    b3d.stack_camera((0, 0, 3.6), 8.6, az=14.0, el=10.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((960, 860), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
