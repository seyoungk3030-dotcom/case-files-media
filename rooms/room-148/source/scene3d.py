"""ROOM 148 3D sprites: a 5x5 wooden tray of sand-block stacks (0-3 blocks), seen from above at a slant; a yellow ring
marks the square that gets one more block. p*: the start. a*: the settled tray after every collapse, with mint rings on
the squares that collapsed."""
import os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, N
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
SP = 0.62; EL = 46.0; H = 0.17


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def xy(r, c): return ((c - 2) * SP, (2 - r) * SP)


def ring(r, c, m, rad=0.27):
    x, y = xy(r, c); bpy.ops.mesh.primitive_torus_add(location=(x, y, 0.02), major_radius=rad, minor_radius=0.03, major_segments=48); bpy.context.object.data.materials.append(m)


def scene(k, after):
    b = BOARDS[k]; order, fin = RES[k]; top = set(order)
    g = fin if after else [[int(ch) for ch in row] for row in b['g']]
    wood = b3d.mat('wood', (0.32, 0.2, 0.09), rough=0.8, coat=0); wood.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0.1
    cellm = b3d.mat('cell', (0.13, 0.09, 0.05), rough=1.0, coat=0)
    sands = [b3d.mat(f's{i}', col, rough=0.9, coat=0) for i, col in enumerate([(0.75, 0.55, 0.25), (0.85, 0.35, 0.12), (0.55, 0.12, 0.08)])]
    for s in sands: s.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0.1
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.5)
    yel = b3d.mat('yel', (1.0, 0.8, 0.2), rough=0.4, coat=0); glow(yel, (1.0, 0.8, 0.2), 1.5)
    S = N * SP
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.12)); o = bpy.context.object; o.scale = (S + 0.3, S + 0.3, 0.24); o.data.materials.append(wood); b3d.bevel(o, 0.05)
    for r in range(N):
        for c in range(N):
            x, y = xy(r, c)
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.003)); o = bpy.context.object; o.scale = (SP - 0.06, SP - 0.06, 0.006); o.data.materials.append(cellm)
            for i in range(g[r][c]):
                bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, H / 2 + i * H + 0.01)); o = bpy.context.object
                o.scale = (0.36, 0.36, H - 0.035); o.rotation_euler = (0, 0, 0.06 * ((r * 7 + c * 3 + i) % 3 - 1)); o.data.materials.append(sands[i]); b3d.bevel(o, 0.02)
            if after and (r, c) in top: ring(r, c, mint)
            if not after and (r, c) == b['star']: ring(r, c, yel, rad=0.29)
    b3d.stack_camera((0, 0.05, 0.2), 4.6, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
