"""ROOM 079 3D sprites: a paper card with a seven-segment '8' of glossy red and blue bars, and a tilted sheet of
coloured cellophane leaning on it (the filter). a*: the view through the cellophane: everything tinted the filter
colour, bars of the filter's colour fade into the paper, the other bars go almost black."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import CARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
L = {'a': (0, 1.1, 0), 'g': (0, 0, 0), 'd': (0, -1.1, 0), 'f': (-0.6, 0.55, 1), 'b': (0.6, 0.55, 1), 'e': (-0.6, -0.55, 1), 'c': (0.6, -0.55, 1)}
FC = {'red': (0.95, 0.2, 0.22), 'blue': (0.2, 0.4, 0.98)}


def box(loc, scale, m, bev=0.04, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def scene(k, after):
    flt, blue = CARDS[k]
    if after:
        tint = FC[flt]; paper = b3d.mat('paper', tuple(0.25 + 0.7 * c for c in tint), rough=0.6, coat=0)
        same = b3d.mat('same', tuple(0.22 + 0.7 * c for c in tint), rough=0.6, coat=0); dark = b3d.mat('dark', (0.05, 0.04, 0.06), rough=0.4)
    else:
        paper = b3d.mat('paper', (0.95, 0.94, 0.9), rough=0.6, coat=0)
        red = b3d.mat('red', (0.9, 0.12, 0.12), rough=0.3, coat=0.6); bl = b3d.mat('blue', (0.1, 0.25, 0.9), rough=0.3, coat=0.6)
    box((0, 0, 0), (2.4, 3.2, 0.06), paper, 0.04)
    for s, (x, y, v) in L.items():
        ink_blue = s in blue
        if after: m = (same if (ink_blue == (flt == 'blue')) else dark)
        else: m = bl if ink_blue else red
        box((x, y, 0.06), (0.18, 0.85, 0.06) if v else (0.85, 0.18, 0.06), m, 0.05)
    if not after:
        cel = b3d.mat('cel', FC[flt], rough=0.05, coat=1.0); p = cel.node_tree.nodes['Principled BSDF']; p.inputs['Alpha'].default_value = 0.55
        try: cel.surface_render_method = 'BLENDED'
        except Exception: cel.blend_method = 'BLEND'
        box((1.75, -0.4, 0.5), (1.3, 1.9, 0.02), cel, 0.03, rot=(0, math.radians(-28), math.radians(-12)))
    b3d.stack_camera((0.3 if not after else 0, 0, 0.1), 4.6, az=10.0, el=62.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((800, 800), 48); b3d.lights(5)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
