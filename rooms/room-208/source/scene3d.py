"""ROOM 208 3D sprites: one kimbap roll (laver, rice, egg, carrot, spinach, ham) on a cutting board, the same length on
every board. p*: the roll cut into the known n pieces. a*: the roll cut into the asked m pieces, each of the m - 1 cut
planes glowing mint, so the number of cuts can be counted. Same camera for every board so the reel keeps one scale."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
L, R, GAP = 11.0, 1.0, 0.75
ROT = (0, math.pi / 2, 0)


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def cyl(m, loc, r, d, v=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d, location=loc, rotation=ROT); o = bpy.context.object
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


FILL = [((0.98, 0.82, 0.2), (0.0, 0.32)), ((1.0, 0.5, 0.15), (-0.32, -0.05)), ((0.25, 0.6, 0.2), (0.3, -0.12)),
        ((0.95, 0.55, 0.6), (-0.02, -0.38)), ((0.55, 0.35, 0.2), (0.05, 0.0))]


def roll(n, glow):
    lav = b3d.mat('laver', (0.02, 0.03, 0.025), rough=0.75, coat=0); rice = glowm('rice', (0.95, 0.95, 0.92), 0.35, 0.8)
    fm = [glowm(f'f{i}', c, 0.5, 0.6) for i, (c, _) in enumerate(FILL)]; mint = glowm('mint', (0.2, 0.95, 0.65), 3.0)
    d = (L - (n - 1) * GAP) / n
    for i in range(n):
        x = -L / 2 + d / 2 + i * (d + GAP)
        cyl(lav, (x, 0, R), R, d); cyl(rice, (x, 0, R), R * 0.92, d + 0.03)
        for j, (c, (dy, dz)) in enumerate(FILL): cyl(fm[j], (x, dy, R + dz), 0.17 if j != 4 else 0.12, d + 0.06, 16)
        if glow and i < n - 1:
            bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=R * 1.15, depth=0.05, location=(x + d / 2 + GAP / 2, 0, R), rotation=ROT)
            bpy.context.object.data.materials.append(mint)


def scene(key, after):
    n, T, m = BOARDS[key]
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.25)); o = bpy.context.object; o.scale = (L + 2.4, 4.2, 0.5)
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(b3d.mat('board', (0.85, 0.62, 0.38), rough=0.6, coat=0.1)); b3d.bevel(o, 0.12, 3)
    roll(m if after else n, after)
    b3d.stack_camera((0, 0, 0.8), 14.0, az=42.0, el=26.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((900, 560), 48); b3d.lights(12)
        t0 = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t0, 1), flush=True)
