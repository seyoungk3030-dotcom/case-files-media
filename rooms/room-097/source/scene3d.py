"""ROOM 097 3D sprites: a round layer cake seen from the front and above, with straight knife cuts drawn as dark
grooves across the pink top and down the sides; cake D also has a groove all around the side for a horizontal cut.
a*: every top piece gets a mint number; cake D shows '×2' for the horizontal cut."""
import math, os, sys, time
import bpy
import numpy as np
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, P
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
R = 1.6; HC = 1.1


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m, rot=(0, 0, 0)):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.03; t.data.materials.append(m)


def rod(a, b, r, m):
    a, b = np.array(a, float), np.array(b, float); d = b - a; L = np.linalg.norm(d)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=tuple((a + b) / 2), vertices=12); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(tuple(d / L))); o.data.materials.append(m)


def scene(k, after):
    ch, hz = BOARDS[k]
    sponge = b3d.mat('sponge', (0.72, 0.48, 0.25), rough=0.8, coat=0); cream = b3d.mat('cream', (0.85, 0.82, 0.78), rough=0.6, coat=0)
    top = b3d.mat('top', (0.80, 0.28, 0.40), rough=0.55, coat=0.1); cut = b3d.mat('cut', (0.04, 0.02, 0.03), rough=0.8, coat=0)
    plate = b3d.mat('plate', (0.45, 0.48, 0.56), rough=0.25, coat=0.6); berry = b3d.mat('berry', (0.85, 0.08, 0.12), rough=0.3)
    mint = b3d.mat('mint', (0.03, 0.05, 0.12), rough=0.4)
    bpy.ops.mesh.primitive_cylinder_add(radius=R + 0.45, depth=0.08, location=(0, 0, -0.04), vertices=96); bpy.context.object.data.materials.append(plate)
    bpy.ops.mesh.primitive_cylinder_add(radius=R, depth=HC / 2 - 0.04, location=(0, 0, HC / 4 - 0.02), vertices=96); bpy.context.object.data.materials.append(sponge)
    bpy.ops.mesh.primitive_cylinder_add(radius=R, depth=0.08, location=(0, 0, HC / 2), vertices=96); bpy.context.object.data.materials.append(cream)
    bpy.ops.mesh.primitive_cylinder_add(radius=R, depth=HC / 2 - 0.04, location=(0, 0, 3 * HC / 4 + 0.02), vertices=96); bpy.context.object.data.materials.append(sponge)
    bpy.ops.mesh.primitive_cylinder_add(radius=R + 0.01, depth=0.08, location=(0, 0, HC), vertices=96); bpy.context.object.data.materials.append(top)
    for a, b in ch:
        p, q = np.array(P(a)) * (R + 0.005), np.array(P(b)) * (R + 0.005)
        rod((p[0], p[1], HC + 0.05), (q[0], q[1], HC + 0.05), 0.022, cut)
        for e in (p, q): rod((e[0], e[1], 0.02), (e[0], e[1], HC + 0.05), 0.022, cut)
    if hz:
        bpy.ops.mesh.primitive_torus_add(location=(0, 0, HC / 2), major_radius=R + 0.005, minor_radius=0.03, major_segments=96); bpy.context.object.data.materials.append(cut)
    if after:
        for x, y, n in RES[k][1]:
            pass
        for idx, (x, y, n) in enumerate(sorted(RES[k][1], key=lambda c: (-c[1], c[0]))):
            text(str(idx + 1), (x * R, y * R, HC + 0.1), 0.46, mint)
    b3d.stack_camera((0, 0, 0.45), 4.6, az=0.0, el=52.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((760, 700), 40); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
