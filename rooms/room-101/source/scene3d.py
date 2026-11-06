"""ROOM 101 3D sprites: amber bars float in front of a pale wall, seen from the front-right. A lamp in front shines
straight at the wall. p*: only the ceiling light is on, so each bar casts a shadow straight down on the floor (two mint rails mark the
digit's left and right edges); the wall is blank. a*: the sun light casts sharp shadows, and the shadow
on the wall shows the digit; the bars that point at the lamp leave only a dot."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import bars, WALL
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
S = 1.1; T = 0.17


def box(m, c, size, shadow):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = size
    o.data.materials.append(m); b3d.bevel(o, 0.03); o.visible_shadow = shadow; return o


def scene(k, after):
    wall = b3d.mat('wall', (0.40, 0.44, 0.50), rough=0.9, coat=0); flo = b3d.mat('floor', (0.26, 0.29, 0.36), rough=0.8, coat=0)
    amb = b3d.mat('amb', (0.80, 0.36, 0.05), rough=0.45, coat=0.2)
    if not after:
        wq = wall.node_tree.nodes['Principled BSDF']; wq.inputs['Base Color'].default_value = (0, 0, 0, 1); wq.inputs['Roughness'].default_value = 1
        wq.inputs['Emission Color'].default_value = (0.30, 0.33, 0.38, 1); wq.inputs['Emission Strength'].default_value = 1.0
    box(wall, (0.5 * S, WALL * S + 0.05, 1.0 * S), (5.2, 0.1, 3.9), True)
    box(flo, (0.5 * S, 0.3, -0.3), (5.2, 5.6, 0.1), True)
    rail = b3d.mat('rail', (0.15, 0.75, 0.55), rough=0.5, coat=0)
    for x in (0, S): box(rail, (x, 0.3 - 0.2, -0.245), (0.05, 5.0, 0.012), False)
    for p, q in bars(k):
        c = tuple((u + v) / 2 * S for u, v in zip(p, q)); d = [abs(u - v) * S for u, v in zip(p, q)]
        size = tuple((x * 0.84 + T * 0.16) if x > 1e-9 else T for x in d)
        if d[1] > 1e-9: size = (T, d[1], T)
        o = box(amb, c, size, True); o.visible_diffuse = False; o.visible_glossy = False
    lamp = b3d.mat('lamp', (0.18, 0.2, 0.26), rough=0.4, metal=0.6); glass = b3d.mat('glass', (1, 0.9, 0.5), rough=0.2)
    gq = glass.node_tree.nodes['Principled BSDF']; gq.inputs['Emission Color'].default_value = (1, 0.85, 0.4, 1); gq.inputs['Emission Strength'].default_value = 6
    bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=0.9, location=(-0.9, -2.6, 0.2), rotation=(math.radians(90), 0, 0), vertices=48)
    o = bpy.context.object; o.data.materials.append(lamp); o.visible_shadow = False
    bpy.ops.mesh.primitive_cylinder_add(radius=0.36, depth=0.04, location=(-0.9, -2.14, 0.2), rotation=(math.radians(90), 0, 0), vertices=48)
    o = bpy.context.object; o.data.materials.append(glass); o.visible_shadow = False
    bpy.ops.object.light_add(type='SUN', rotation=(0, 0, 0)); L = bpy.context.object.data
    L.energy = 1.6; L.angle = math.radians(0.6)
    if after:
        bpy.ops.object.light_add(type='SUN', rotation=(math.radians(90), 0, 0)); L = bpy.context.object.data
        L.energy = 2.4; L.angle = math.radians(0.6)
    bpy.ops.object.light_add(type='AREA', location=(4, -5, 6), rotation=(math.radians(40), 0, math.radians(35)))
    L = bpy.context.object.data; L.energy = 380; L.size = 6; L.use_shadow = False
    b3d.stack_camera((0.5 * S - 0.35, 0.4, 0.95 * S), 6.9, az=50.0, el=28.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 900), 48)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
