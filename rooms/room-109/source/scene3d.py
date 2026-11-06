"""ROOM 109 3D sprites: a cut-away block of sea water (see-through front) with either a wooden pier post or a tall boat,
a rope ladder with wooden rungs on its front, and a striped tide pole whose glowing mint band marks the coming high
tide. a*: the water has risen to the band; a boat (and its ladder) floats up with it; rungs above water turn mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, rungs
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def box(m, c, s, bev=0.03):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def scene(k, after):
    kind, z0, g, n, rise = BOARDS[k]; lift = rise if (after and kind == 'boat') else 0.0; level = rise if after else 0.0
    sea = b3d.mat('sea', (0.03, 0.18, 0.45), rough=0.1, coat=0.2); sq = sea.node_tree.nodes['Principled BSDF']; sq.inputs['Alpha'].default_value = 0.55
    wood = b3d.mat('wood', (0.42, 0.26, 0.12), rough=0.7, coat=0); rung = b3d.mat('rung', (0.85, 0.62, 0.30), rough=0.6, coat=0)
    rope = b3d.mat('rope', (0.75, 0.70, 0.60), rough=0.8, coat=0); hull = b3d.mat('hull', (0.55, 0.12, 0.09), rough=0.45, coat=0.3)
    deck = b3d.mat('deck', (0.6, 0.62, 0.66), rough=0.5, coat=0.2); white = b3d.mat('white', (0.7, 0.72, 0.76), rough=0.5, coat=0)
    dark = b3d.mat('dark', (0.06, 0.07, 0.1), rough=0.6, coat=0); grey = b3d.mat('grey', (0.35, 0.38, 0.45), rough=0.6, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.6)
    box(dark, (0, 0.2, -1.75), (6.4, 2.6, 0.1))
    box(sea, (0, 0.2, (level - 1.7) / 2), (6.3, 2.5, level + 1.7), 0.01)
    if kind == 'pier':
        box(wood, (0.3, 0.55, 0.6), (0.9, 0.9, 4.6))
        box(wood, (0.3, 0.55, 2.95), (2.4, 1.4, 0.18))
    else:
        box(hull, (0.3, 0.75, 0.7 + lift), (3.6, 1.5, 2.8), 0.15)
        box(deck, (0.3, 0.75, 2.12 + lift), (3.7, 1.6, 0.08))
        box(white, (0.9, 0.75, 2.55 + lift), (1.2, 1.0, 0.8), 0.08)
    zs = [z + lift for z in rungs(k)]; top = zs[-1] + 0.2
    for x in (-0.05, 0.65):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=top - zs[0] + 0.15, location=(x, -0.06, (top + zs[0] - 0.15) / 2), vertices=12)
        bpy.context.object.data.materials.append(rope)
    for z in zs:
        m = (mint if z > level else grey) if after else rung
        bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.84, location=(0.3, -0.1, z), rotation=(0, math.radians(90), 0), vertices=16)
        bpy.context.object.data.materials.append(m)
    for i in range(14):
        box(white if i % 2 == 0 else dark, (-2.3, -0.4, -1.6 + 0.3 * i + 0.15), (0.16, 0.16, 0.3), 0.01)
    bpy.ops.mesh.primitive_torus_add(location=(-2.3, -0.4, rise), major_radius=0.17, minor_radius=0.045); bpy.context.object.data.materials.append(mint)
    box(mint, (-1.95, -0.4, rise), (0.55, 0.04, 0.04), 0.005)
    b3d.stack_camera((-0.1, 0, 0.6), 6.9, az=18.0, el=10.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 1000), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
