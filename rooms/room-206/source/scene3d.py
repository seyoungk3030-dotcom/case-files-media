"""ROOM 206 3D sprites, true scale in cm: a glass tank 20 x 20 cm inside with water 8 cm deep, a toy boat (14 x 8 x 6 cm,
100 g) whose draft is (100 + load) / 112 cm. p*: the object sits on the deck. a*: the object is in the water (sunk to the
bottom, or floating for wood), the boat rides higher, the water stands lower by the proven amount; the old level is a
coral line, the new level a mint line."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, drop_mm
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
H0, TH = 8.0, 14.0
K = 40 ** (1 / 3) / 10 ** (1 / 3)   # objects are 4x the volume of the first draft


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def clear(name, c, a):
    m = b3d.mat(name, c, rough=0.05, coat=0); m.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = a
    return m


def box(m, loc, sc, bev=0.0, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def obj(key, x, y, z0):
    nm, V, rho = BOARDS[key]
    if key == 'A':
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.68 * K, location=(x, y, z0 + 1.3 * K)); o = bpy.context.object
        o.scale = (1.15, 1.0, 0.78); o.data.materials.append(b3d.mat('stone', (0.7, 0.7, 0.72), rough=0.8, coat=0))
    elif key == 'B':
        box(b3d.mat('wood', (0.95, 0.7, 0.4), rough=0.6, coat=0), (x, y, z0 + 1.0 * K), (2.5 * K, 2.0 * K, 2.0 * K), 0.08)
    elif key == 'C':
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=1.55 * K, depth=1.6 * K, location=(x, y, z0 + 0.8 * K))
        bpy.context.object.data.materials.append(b3d.mat('iron', (0.55, 0.57, 0.6), rough=0.3, metal=1.0, coat=0)); b3d.bevel(bpy.context.object, 0.08, 2)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.7 * K, depth=1.62 * K, location=(x, y, z0 + 0.8 * K)); bpy.context.object.data.materials.append(b3d.mat('hole', (0.05, 0.05, 0.06), rough=0.9, coat=0))
    else:
        bpy.ops.mesh.primitive_cylinder_add(radius=1.1 * K, depth=2.6 * K, location=(x, y, z0 + 1.3 * K))
        bpy.context.object.data.materials.append(b3d.mat('copper', (0.85, 0.45, 0.25), rough=0.25, metal=1.0, coat=0)); b3d.bevel(bpy.context.object, 0.15, 3)
        bpy.ops.mesh.primitive_torus_add(major_radius=0.4 * K, minor_radius=0.12 * K, location=(x, y, z0 + 2.85 * K), rotation=(math.pi / 2, 0, 0))
        bpy.context.object.data.materials.append(b3d.mat('copper2', (0.85, 0.45, 0.25), rough=0.25, metal=1.0, coat=0))


def scene(key, after):
    nm, V, rho = BOARDS[key]; m = float(V * rho); d = float(drop_mm(V, rho)) / 10
    h = H0 - d if after else H0
    edge = b3d.mat('edge', (0.7, 0.8, 0.88), rough=0.2, metal=0.6, coat=0); S = 10.15
    for sx in (-1, 1):
        for sy in (-1, 1): box(edge, (sx * S, sy * S, TH / 2), (0.3, 0.3, TH))
    for sx in (-1, 1):
        box(edge, (0, sx * S, TH), (20.6, 0.3, 0.3)); box(edge, (sx * S, 0, TH), (0.3, 20.6, 0.3))
    box(b3d.mat('base', (0.2, 0.22, 0.28), rough=0.6, coat=0), (0, 0, -0.4), (21.5, 21.5, 0.8), 0.15)
    box(clear('water', (0.12, 0.38, 0.8), 0.6), (0, 0, h / 2), (20.0, 20.0, h))
    for i in range(0, 14):   # ruler on the front left edge, cm ticks
        box(b3d.mat('tick', (1, 1, 1), rough=0.5, coat=0), (-9.0, -10.2, i), (1.4 if i % 5 == 0 else 0.8, 0.05, 0.1))
    draft = (100 + (0 if after else m)) / 112; bz = h - draft
    hull = b3d.mat('hull', (0.85, 0.28, 0.2), rough=0.5, coat=0.3)
    box(hull, (1.5, 3.0, bz + 3.0), (14.0, 8.0, 6.0), 0.6)
    box(b3d.mat('deck', (0.75, 0.68, 0.58), rough=0.6, coat=0), (1.5, 3.0, bz + 6.0), (13.0, 7.0, 0.1))
    if not after: obj(key, 1.5, 3.0, bz + 6.05)
    elif rho < 1:
        dr = m / (2.5 * 2.0 * K * K); obj(key, -4.0, -5.5, h - dr)
    else: obj(key, -4.0, -5.5, 0.0)
    if after:
        box(glowm('old', (1.0, 0.45, 0.35), 3.0), (0, -10.4, H0), (20.6, 0.1, 0.16))
        box(glowm('new', (0.2, 0.95, 0.65), 3.0), (0, -10.4, h), (20.6, 0.1, 0.16))
    b3d.stack_camera((0, 0, 7.0), 30.0, az=18.0, el=26.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((700, 700), 48); b3d.lights(3)
        t0 = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t0, 1), flush=True)
