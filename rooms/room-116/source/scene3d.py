"""ROOM 116 3D sprites: left, a hall wall plate with three toggle switches and amber number tags; a dividing wall;
right, a closed room with three bulbs hanging from the ceiling: one lit (glowing yellow), one dark but warm (dim
orange filament and heat waves), one dark and cold (grey-blue). The asked bulb has an amber '?' tag under it.
a*: that tag turns mint and shows its switch number, and a mint cord links it to its switch."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, owner
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
SX = [-2.75, -2.05, -1.35]; BX = [0.35, 1.45, 2.55]


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def box(m, c, s, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def wave(x, z, m):
    pts = [(x + 0.07 * math.sin(i / 4 * math.pi), -0.3, z + i * 0.04) for i in range(13)]
    cu = bpy.data.curves.new('w', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.018
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for i, q in enumerate(pts): sp.points[i].co = (*q, 1)
    o = bpy.data.objects.new('w', cu); bpy.context.collection.objects.link(o); o.data.materials.append(m)


def scene(k, after):
    b = BOARDS[k]
    wall = b3d.mat('wall', (0.05, 0.06, 0.1), rough=0.8, coat=0); room = b3d.mat('room', (0.025, 0.03, 0.05), rough=0.8, coat=0)
    plate = b3d.mat('plate', (0.85, 0.86, 0.88), rough=0.4, coat=0.1); dark = b3d.mat('dark', (0.12, 0.13, 0.17), rough=0.4, coat=0.2)
    amber = b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0.1); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.5)
    lit = b3d.mat('lit', (1.0, 0.85, 0.4), rough=0.2, coat=0); glow(lit, (1.0, 0.82, 0.35), 12.0)
    warm = b3d.mat('warm', (0.16, 0.07, 0.04), rough=0.3, coat=0.3); glow(warm, (0.8, 0.25, 0.06), 0.35)
    heat = b3d.mat('heat', (1.0, 0.45, 0.1), rough=0.5, coat=0); glow(heat, (1.0, 0.45, 0.1), 3.0)
    cold = b3d.mat('cold', (0.25, 0.3, 0.38), rough=0.3, coat=0.4); metal = b3d.mat('metal', (0.6, 0.62, 0.66), rough=0.3, metal=0.8, coat=0)
    cord = b3d.mat('cord', (0.15, 0.15, 0.17), rough=0.6, coat=0)
    box(wall, (-2.05, 0.3, 1.9), (2.5, 0.1, 4.2), 0.0)
    box(room, (1.45, 0.3, 1.9), (3.6, 0.1, 4.2), 0.0); box(dark, (-0.55, 0.0, 1.9), (0.3, 0.7, 4.2), 0.03)
    box(dark, (1.45, 0.0, 3.95), (3.6, 0.6, 0.12), 0.02)
    box(plate, (-2.05, 0.2, 2.2), (2.2, 0.06, 1.1), 0.08)
    for i, (x, n) in enumerate(zip(SX, b['switches'])):
        on = n == b['second']
        box(dark, (x, 0.12, 2.2), (0.32, 0.08, 0.6), 0.04)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0.02, 2.2 + (0.12 if on else -0.12))); o = bpy.context.object
        o.scale = (0.14, 0.12, 0.26); o.rotation_euler = (math.radians(-25 if on else 25), 0, 0); o.data.materials.append(mint if on else plate); b3d.bevel(o, 0.03)
        box(amber, (x, 0.12, 1.25), (0.5, 0.05, 0.5), 0.08); text(str(n), (x, 0.08, 1.25), 0.36, ink)
    for i, (x, st) in enumerate(zip(BX, b['bulbs'])):
        box(cord, (x, -0.1, 3.4), (0.03, 0.03, 1.0), 0.0)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.3, location=(x, -0.1, 2.82), vertices=32); bpy.context.object.data.materials.append(metal)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.36, location=(x, -0.1, 2.38), segments=48, ring_count=24); o = bpy.context.object
        o.scale = (1, 1, 1.12); o.data.materials.append({'lit': lit, 'warm': warm, 'cold': cold}[st])
        for p in o.data.polygons: p.use_smooth = True
        if st == 'warm':
            for dx in (-0.22, 0, 0.22): wave(x + dx, 2.0 - 0.75 + 0.1 * (dx == 0), heat)
        if i == b['ask']:
            n = owner(b, st)
            box(mint if after else amber, (x, -0.2, 0.75), (0.6, 0.05, 0.6), 0.1); text(str(n) if after else '?', (x, -0.24, 0.75), 0.44, ink)
    b3d.stack_camera((0.0, 0, 2.0), 6.6, az=0.0, el=3.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 760), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
