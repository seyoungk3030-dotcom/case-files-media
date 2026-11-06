"""ROOM 154 3D sprites: a 3x3 panel of square push buttons, each with a dome lamp (lit = glowing yellow, off = grey glass),
seen from above at a slant. p*: the start. a*: every lamp off, mint rings on the buttons to press."""
import os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, SOL, N
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
SP = 1.0; EL = 55.0


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def xy(r, c): return ((c - 1) * SP, (1 - r) * SP)


def scene(k, after):
    g = BOARDS[k]; press = set(SOL[k][0])
    body = b3d.mat('body', (0.12, 0.14, 0.2), rough=0.5, coat=0.2); btn = b3d.mat('btn', (0.3, 0.33, 0.42), rough=0.35, coat=0.3)
    on = b3d.mat('on', (1.0, 0.8, 0.25), rough=0.2, coat=0.3); glow(on, (1.0, 0.7, 0.15), 2.5)
    off = b3d.mat('off', (0.08, 0.09, 0.11), rough=0.15, coat=0.6)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.5)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.15)); o = bpy.context.object; o.scale = (3 * SP + 0.3, 3 * SP + 0.3, 0.3); o.data.materials.append(body); b3d.bevel(o, 0.08)
    for r in range(N):
        for c in range(N):
            x, y = xy(r, c)
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.08)); o = bpy.context.object; o.scale = (0.8, 0.8, 0.16); o.data.materials.append(btn); b3d.bevel(o, 0.06)
            lit = g[r][c] == '1' and not after
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(x, y, 0.16), segments=32, ring_count=16); o = bpy.context.object; o.scale = (1, 1, 0.75)
            o.data.materials.append(on if lit else off)
            if after and (r, c) in press:
                bpy.ops.mesh.primitive_torus_add(location=(x, y, 0.2), major_radius=0.48, minor_radius=0.04, major_segments=48); bpy.context.object.data.materials.append(mint)
    b3d.stack_camera((0, 0.05, 0.0), 4.3, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
