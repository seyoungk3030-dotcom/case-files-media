"""ROOM 143 3D sprites: a green 6x6 Othello board with black and white discs, seen from above at a slant; a yellow ring
marks the square where black goes. p*: the position. a*: the new black disc and every flipped disc carry a mint ring."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, FLIP, N, star
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
SP = 0.62; EL = 62.0


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def xy(r, c): return ((c - 2.5) * SP, (2.5 - r) * SP)


def disc(r, c, top, bot):
    x, y = xy(r, c)
    for z, m in ((0.045, bot), (0.105, top)):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.06, location=(x, y, z), vertices=48); o = bpy.context.object; o.data.materials.append(m); b3d.bevel(o, 0.02, 2)


def ring(r, c, m, z=0.15, rad=0.27):
    x, y = xy(r, c); bpy.ops.mesh.primitive_torus_add(location=(x, y, z), major_radius=rad, minor_radius=0.03, major_segments=48); bpy.context.object.data.materials.append(m)


def scene(k, after):
    b = BOARDS[k]; sr, sc = star(b); fl = set(map(tuple, FLIP[k]))
    green = b3d.mat('green', (0.02, 0.22, 0.1), rough=0.9, coat=0); green.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0
    frame = b3d.mat('frame', (0.05, 0.05, 0.06), rough=0.6, coat=0); line = b3d.mat('line', (0.0, 0.05, 0.02), rough=1.0, coat=0)
    blk = b3d.mat('blk', (0.03, 0.03, 0.035), rough=0.35, coat=0.3); wht = b3d.mat('wht', (0.85, 0.85, 0.82), rough=0.35, coat=0.2)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.5)
    yel = b3d.mat('yel', (1.0, 0.8, 0.2), rough=0.4, coat=0); glow(yel, (1.0, 0.8, 0.2), 1.5)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.08)); o = bpy.context.object; o.scale = (N * SP + 0.35, N * SP + 0.35, 0.14); o.data.materials.append(frame); b3d.bevel(o, 0.05)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.005)); o = bpy.context.object; o.scale = (N * SP, N * SP, 0.02); o.data.materials.append(green)
    for i in range(1, N):
        v = (i - 3) * SP
        bpy.ops.mesh.primitive_cube_add(size=1, location=(v, 0, 0.007)); o = bpy.context.object; o.scale = (0.02, N * SP, 0.004); o.data.materials.append(line)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, v, 0.007)); o = bpy.context.object; o.scale = (N * SP, 0.02, 0.004); o.data.materials.append(line)
    for r in range(N):
        for c in range(N):
            ch = b[r][c]
            if ch == '*':
                if after: disc(r, c, blk, wht); ring(r, c, mint)
                else: ring(r, c, yel, z=0.03, rad=0.22)
            elif ch == 'X': disc(r, c, blk, wht)
            elif ch == 'O':
                if after and (r, c) in fl: disc(r, c, blk, wht); ring(r, c, mint)
                else: disc(r, c, wht, blk)
    b3d.stack_camera((0, -0.05, 0.05), 4.6, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
