"""ROOM 062 3D sprites: pin-tumbler lock cutaway with three keys underneath, front view.
'pA'..'pD' = lock without key (pins resting on the floor) and three numbered keys lined up with the pins.
'aA'..'aD' = the opening key inserted: every pin top sits on the glowing yellow shear line."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import PINS, keys, opens, H
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U = 0.3; S = H * U; XS = [-1.0 + 0.5 * i for i in range(5)]


def label(s, x, z, size, m, y=-0.35):
    bpy.ops.object.text_add(location=(x, y, z), rotation=(math.radians(90), 0, 0))
    t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.03; t.data.materials.append(m)


def box(x0, x1, z0, z1, m, d=0.3, y=0.0, bev=0.02):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, y, (z0 + z1) / 2)); o = bpy.context.object
    o.scale = (x1 - x0, d, z1 - z0); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 2)


def cyl(x, z0, z1, r, m):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=z1 - z0, vertices=24, location=(x, 0, (z0 + z1) / 2))
    bpy.context.object.data.materials.append(m)


def key(base, teeth, num, M, txt):
    box(-1.35, 1.45, base - 0.3, base, M['steel'], 0.12)
    for x, t in zip(XS, teeth):
        box(x - 0.18, x + 0.18, base - 0.01, base + t * U, M['steel'], 0.12, bev=0.01)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.5, minor_radius=0.09, location=(-2.0, 0, base - 0.15), rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.materials.append(M['steel'])
    box(-1.55, -1.33, base - 0.25, base - 0.05, M['steel'], 0.12, bev=0.0)
    label(str(num), -2.0, base - 0.15, 0.82, txt, y=-0.15)


def lock(M, teeth=None, glow=False):
    floor = 0.0 if teeth is None else 0.0
    box(-1.6, 1.6, S, S + 1.05, M['house'], 0.5, y=0.1)
    box(-1.6, 1.6, -0.45, S, M['plug'], 0.5, y=0.1)
    box(-1.62, 1.62, S - 0.025, S + 0.025, M['amber'] if glow else M['line'], 0.55, y=0.0, bev=0.0)
    for x, p, t in zip(XS, PINS['_k'], teeth or [0] * 5):
        b = t * U if teeth else floor
        cyl(x, b, b + p * U, 0.15, M['pin_on'] if glow else M['pin'])
        cyl(x, b + p * U, S + 1.0, 0.05, M['spring'])


def scene(k, after):
    PINS['_k'] = PINS[k]
    steel = b3d.mat('steel', (0.78, 0.80, 0.84), rough=0.25, metal=0.85)
    M = {'steel': steel,
         'house': b3d.mat('house', (0.35, 0.40, 0.50), rough=0.4, coat=0.2), 'plug': b3d.mat('plug', (0.60, 0.68, 0.80), rough=0.3),
         'pin': b3d.mat('pin', (0.85, 0.66, 0.28), rough=0.25, metal=0.8), 'pin_on': b3d.mat('pin_on', (0.98, 0.70, 0.20), rough=0.2, metal=0.6),
         'spring': b3d.mat('spring', (0.55, 0.58, 0.62), rough=0.4, metal=0.6), 'line': b3d.mat('line', (0.98, 0.84, 0.20), rough=0.3),
         'amber': b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3)}
    for n in ('house', 'plug'):
        M[n].node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.30 if n == 'house' else 0.22
    for n in ('line', 'amber', 'pin_on'):
        q = M[n].node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
        q.inputs['Emission Strength'].default_value = 0.6 if n != 'pin_on' else 0.25
    white = b3d.mat('white', b3d.PAL['mint'], rough=0.3)
    q = white.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value; q.inputs['Emission Strength'].default_value = 0.9
    if after:
        b3d.stack_camera((-0.3, 0, 1.0), 4.4, az=0.0, el=8.0)
        (num, t), = [(n, t) for n, t in keys(k) if opens(k, t)]
        lock(M, t, glow=True); key(0.0, t, num, M, white)
    else:
        b3d.stack_camera((-0.45, 0, -1.5), 8.9, az=0.0, el=8.0)
        lock(M)
        for j, (num, t) in enumerate(keys(k)):
            key(-1.55 - j * 1.75, t, num, M, white)
    b3d.floor().location.z = -7.0


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((560, 1000) if not after else (620, 640), 48); b3d.lights(7)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
