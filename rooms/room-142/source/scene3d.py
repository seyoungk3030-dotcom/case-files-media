"""ROOM 142 3D sprites: an upright blue Connect Four frame (7 columns x 6 rows), yellow and red discs, column numbers
1-7 on top, seen from the front. p*: the position, yellow to move. a*: yellow's winning disc dropped (mint ring) and
the four in a row outlined in mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, R, C, four, land, with_, code
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
SP = 0.8; EL = 6.0


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - EL), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def xz(r, c): return ((c - 3) * SP, (r - 2.5) * SP)


def disc(r, c, m, y=-0.2):
    x, z = xz(r, c); bpy.ops.mesh.primitive_cylinder_add(radius=0.33, depth=0.14, location=(x, y, z), rotation=(math.radians(90), 0, 0), vertices=48)
    o = bpy.context.object; o.data.materials.append(m); b3d.bevel(o, 0.03, 2)


def ring(r, c, m):
    x, z = xz(r, c); bpy.ops.mesh.primitive_torus_add(location=(x, -0.3, z), rotation=(math.radians(90), 0, 0), major_radius=0.36, minor_radius=0.04, major_segments=48)
    bpy.context.object.data.materials.append(m)


def line(g):
    for r in range(R):
        for c in range(C):
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                cells = [(r + i * dr, c + i * dc) for i in range(4)]
                if all(0 <= a < R and 0 <= b < C and g[a][b] == 'X' for a, b in cells): return cells


def scene(k, after):
    g = BOARDS[k]
    blue = b3d.mat('blue', (0.05, 0.2, 0.75), rough=0.45, coat=0.2); hole = b3d.mat('hole', (0.01, 0.015, 0.03), rough=1.0, coat=0)
    yel = b3d.mat('yel', (1.0, 0.75, 0.05), rough=0.35, coat=0.2); red = b3d.mat('red', (0.85, 0.08, 0.08), rough=0.35, coat=0.2)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.5)
    ink = b3d.mat('ink', (0.97, 0.97, 1.0), rough=0.6, coat=0); glow(ink, (0.97, 0.97, 1.0), 0.6)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0)); o = bpy.context.object; o.scale = (C * SP + 0.3, 0.24, R * SP + 0.3); o.data.materials.append(blue); b3d.bevel(o, 0.08)
    for side in (-1, 1):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(side * (C * SP / 2 + 0.3), 0, -R * SP / 2 - 0.1)); o = bpy.context.object; o.scale = (0.24, 1.2, 0.5); o.data.materials.append(blue); b3d.bevel(o, 0.06)
    if after:
        cc = int(code['ABCD'.index(k)]) - 1; rr = land(g, cc); g2 = with_(g, rr, cc, 'X')
    else:
        g2 = g
    for r in range(R):
        for c in range(C):
            x, z = xz(r, c)
            if g2[r][c] == '.':
                bpy.ops.mesh.primitive_cylinder_add(radius=0.33, depth=0.02, location=(x, -0.125, z), rotation=(math.radians(90), 0, 0), vertices=48); bpy.context.object.data.materials.append(hole)
            else:
                disc(r, c, yel if g2[r][c] == 'X' else red)
    for c in range(C):
        x, z = xz(R, c); text(str(c + 1), (x, -0.2, z - 0.15), 0.42, ink)
    if after:
        for a, b in line(g2): ring(a, b, mint)
    b3d.stack_camera((0, 0, 0.15), 6.9, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
