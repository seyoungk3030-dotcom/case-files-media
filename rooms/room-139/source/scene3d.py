"""ROOM 139 3D sprites: gold coins on a dark felt table, packed like a honeycomb, seen from above at a slant. p*: the
starting shape. a*: coins that stay are gold; each moved coin leaves a faint ring where it was and lies mint where it
goes, so the mint coins count the moves."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
CR = 0.3; DY = 2 * CR * math.sin(math.radians(60))


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def xy(p): return (p[0] * CR, -p[1] * DY)


def coin(p, m, cx, cy):
    x, y = xy(p); bpy.ops.mesh.primitive_cylinder_add(radius=CR - 0.015, depth=0.07, location=(x - cx, y - cy, 0.035), vertices=48)
    o = bpy.context.object; o.data.materials.append(m); b3d.bevel(o, 0.012, 2)
    bpy.ops.mesh.primitive_torus_add(location=(x - cx, y - cy, 0.072), major_radius=CR - 0.07, minor_radius=0.012, major_segments=48); bpy.context.object.data.materials.append(m)


def scene(k, after):
    S = set(map(tuple, BOARDS[k]['coins'])); T = set(map(tuple, RES[k][2]))
    gold = b3d.mat('gold', (0.85, 0.62, 0.2), rough=0.3, metal=0.9, coat=0); mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.35, metal=0.2, coat=0); glow(mint, (0.15, 0.85, 0.6), 0.25)
    felt = b3d.mat('felt', (0.02, 0.06, 0.05), rough=0.95, coat=0); ring = b3d.mat('ring', (0.9, 0.35, 0.3), rough=0.5, coat=0); glow(ring, (0.9, 0.35, 0.3), 0.6)
    pts = [xy(p) for p in (S | T if after else S)] + [xy(p) for p in S | T]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.05)); o = bpy.context.object; o.scale = (5.6, 5.0, 0.1); o.data.materials.append(felt); b3d.bevel(o, 0.08)
    if not after:
        for p in S: coin(p, gold, cx, cy)
    else:
        for p in S & T: coin(p, gold, cx, cy)
        for p in T - S: coin(p, mint, cx, cy)
        for p in S - T:
            x, y = xy(p); bpy.ops.mesh.primitive_torus_add(location=(x - cx, y - cy, 0.01), major_radius=CR - 0.03, minor_radius=0.025, major_segments=48); bpy.context.object.data.materials.append(ring)
    b3d.stack_camera((0, 0, 0), 5.4, az=0.0, el=68.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
