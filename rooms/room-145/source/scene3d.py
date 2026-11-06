"""ROOM 145 3D sprites: a small wooden baduk board (7x7 lines) with black and white stones, seen from above at a slant;
a yellow ring marks where black plays. p*: the position. a*: the new black stone (mint ring) and coral rings where the
captured white stones were taken off."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, CAP, N, star
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
SP = 0.6; EL = 62.0


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def xy(r, c): return ((c - 3) * SP, (3 - r) * SP)


def stone(r, c, m):
    x, y = xy(r, c); bpy.ops.mesh.primitive_uv_sphere_add(radius=0.27, location=(x, y, 0.07), segments=40, ring_count=20)
    o = bpy.context.object; o.scale = (1, 1, 0.38); o.data.materials.append(m)


def ring(r, c, m, z=0.12, rad=0.29):
    x, y = xy(r, c); bpy.ops.mesh.primitive_torus_add(location=(x, y, z), major_radius=rad, minor_radius=0.03, major_segments=48); bpy.context.object.data.materials.append(m)


def scene(k, after):
    b = BOARDS[k]; cap = set(map(tuple, CAP[k]))
    wood = b3d.mat('wood', (0.4, 0.25, 0.1), rough=0.75, coat=0); wood.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0.1
    line = b3d.mat('line', (0.05, 0.03, 0.02), rough=1.0, coat=0)
    blk = b3d.mat('blk', (0.025, 0.025, 0.03), rough=0.3, coat=0.4); wht = b3d.mat('wht', (0.86, 0.86, 0.83), rough=0.3, coat=0.3)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.5)
    yel = b3d.mat('yel', (1.0, 0.8, 0.2), rough=0.4, coat=0); glow(yel, (1.0, 0.8, 0.2), 1.5)
    cor = b3d.mat('cor', (0.95, 0.4, 0.35), rough=0.4, coat=0); glow(cor, (0.95, 0.4, 0.35), 1.2)
    S = (N - 1) * SP
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.15)); o = bpy.context.object; o.scale = (S + 0.8, S + 0.8, 0.3); o.data.materials.append(wood); b3d.bevel(o, 0.05)
    for i in range(N):
        v = (i - 3) * SP
        bpy.ops.mesh.primitive_cube_add(size=1, location=(v, 0, 0.002)); o = bpy.context.object; o.scale = (0.025, S + 0.025, 0.004); o.data.materials.append(line)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, v, 0.002)); o = bpy.context.object; o.scale = (S + 0.025, 0.025, 0.004); o.data.materials.append(line)
    for r in range(N):
        for c in range(N):
            ch = b[r][c]
            if ch == '*':
                if after: stone(r, c, blk); ring(r, c, mint)
                else: ring(r, c, yel, z=0.02, rad=0.22)
            elif ch == 'X': stone(r, c, blk)
            elif ch == 'O':
                if after and (r, c) in cap: ring(r, c, cor, z=0.02, rad=0.22)
                else: stone(r, c, wht)
    b3d.stack_camera((0, -0.05, 0.0), 5.0, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
