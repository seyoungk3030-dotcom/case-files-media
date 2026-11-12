"""ROOM 176 3D sprites: a chocolate bar of R x C squares lying on its opened foil wrapper, seen from the front and above.
p*: the whole bar with its grooves. a*: every square snapped apart and spread out a little."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
S = 0.62; G = 0.05  # square pitch, groove width


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def box(loc, scale, m, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def scene(k, after):
    R, C = BOARDS[k]
    choc = b3d.mat('choc', (0.16, 0.075, 0.035), rough=0.35, coat=0.5); dark = b3d.mat('dark', (0.11, 0.05, 0.025), rough=0.5, coat=0.2)
    foil = b3d.mat('foil', (0.85, 0.86, 0.9), rough=0.25, metal=0.8); paper = b3d.mat('paper', (0.85, 0.15, 0.2), rough=0.5, coat=0.2)
    mint = glowm('mint', (0.15, 0.85, 0.6), 1.8)
    W, H = C * S, R * S; sp = 0.22 if after else 0.0
    box((0, 0, -0.01), (W + 0.7 + sp * (C - 1), H + 0.7 + sp * (R - 1), 0.02), foil)
    box((0, H / 2 + 0.55 + sp * (R - 1) / 2, -0.005), (W + 0.9 + sp * (C - 1), 0.5, 0.03), paper, 0.01)
    for r in range(R):
        for c in range(C):
            x = (c - (C - 1) / 2) * (S + sp); y = (r - (R - 1) / 2) * (S + sp)
            box((x, y, 0.07), (S - (0.0 if after else 0.0), S, 0.1), dark, 0.01) if not after else None
            box((x, y, 0.15 if not after else 0.1), (S - G * 2, S - G * 2, 0.1), choc, 0.04)
            if after: box((x, y, 0.04), (S, S, 0.08), dark, 0.02)
    b3d.stack_camera((0, 0.1, 0), 4.4, az=0.0, el=55.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((900, 800), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
