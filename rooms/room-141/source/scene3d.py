"""ROOM 141 3D sprites: a 3x3 board of square tiles, each with a copper pipe (straight or bent), seen from above at a
slant. A blue inlet arrow on the left, a drain cup on the right. p*: start. a*: every tile is turned to the cheapest
fix, the joined pipes glow mint (water), and each clicked tile shows its click count."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, BASE, rot, N, E, S, W, OPP, DV
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
TS = 1.0; EL = 60.0
VEC = {N: (0, 1), E: (1, 0), S: (0, -1), W: (-1, 0)}


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - EL), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def cxy(r, c): return ((c - 1) * TS, (1 - r) * TS)


def arm(x, y, d, m, rad=0.12, z=0.16, ln=TS / 2):
    vx, vy = VEC[d]; bpy.ops.mesh.primitive_cylinder_add(radius=rad, depth=ln, location=(x + vx * ln / 2, y + vy * ln / 2, z), vertices=32,
                                                          rotation=(math.radians(90) if vy else 0, math.radians(90) if vx else 0, 0))
    bpy.context.object.data.materials.append(m)


def path_cells(g, src, dst):
    seen = {(src, 0)}; st = [(src, 0)]
    while st:
        r, c = st.pop()
        for d, (dr, dc) in DV.items():
            rr, cc = r + dr, c + dc
            if g[r][c] & d and 0 <= rr < 3 and 0 <= cc < 3 and g[rr][cc] & OPP[d] and (rr, cc) not in seen: seen.add((rr, cc)); st.append((rr, cc))
    return seen


def scene(k, after):
    b = BOARDS[k]; ks = RES[k]
    base = b3d.mat('base', (0.03, 0.04, 0.06), rough=0.9, coat=0); tile = b3d.mat('tile', (0.2, 0.22, 0.27), rough=1.0, coat=0); tile.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0
    copper = b3d.mat('copper', (0.78, 0.42, 0.22), rough=0.35, metal=0.8, coat=0)
    water = b3d.mat('water', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(water, (0.15, 0.85, 0.6), 0.9)
    blue = b3d.mat('blue', (0.25, 0.6, 1.0), rough=0.4, coat=0); glow(blue, (0.25, 0.6, 1.0), 0.8)
    ink = b3d.mat('ink', (0.98, 0.85, 0.35), rough=0.6, coat=0); glow(ink, (0.98, 0.85, 0.35), 0.8)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.06)); o = bpy.context.object; o.scale = (3.3, 3.3, 0.12); o.data.materials.append(base); b3d.bevel(o, 0.06)
    g = [[0] * 3 for _ in range(3)]
    for r in range(3):
        for c in range(3):
            g[r][c] = rot(rot(BASE[b['T'][r][c]], b['O'][r][c]), ks[3 * r + c] if after else 0)
    wet = path_cells(g, b['src'], b['dst']) if after else set()
    for r in range(3):
        for c in range(3):
            x, y = cxy(r, c)
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.03)); o = bpy.context.object; o.scale = (TS - 0.06, TS - 0.06, 0.06); o.data.materials.append(tile); b3d.bevel(o, 0.04)
            m = water if (r, c) in wet else copper
            for d in (N, E, S, W):
                if g[r][c] & d: arm(x, y, d, m, ln=TS / 2 - 0.03)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(x, y, 0.16), segments=32, ring_count=16); bpy.context.object.data.materials.append(m)
            if after and ks[3 * r + c]:
                text(f'+{ks[3 * r + c]}', (x + 0.28, y + 0.3, 0.25), 0.36, ink)
    # inlet arrow on the left of src row, drain on the right of dst row
    x, y = cxy(b['src'], 0); x -= TS / 2
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.5, location=(x - 0.3, y, 0.16), rotation=(0, math.radians(90), 0), vertices=32); bpy.context.object.data.materials.append(blue)
    bpy.ops.mesh.primitive_cone_add(radius1=0.22, depth=0.3, location=(x - 0.02, y, 0.16), rotation=(0, math.radians(90), 0), vertices=32); bpy.context.object.data.materials.append(blue)
    x, y = cxy(b['dst'], 2); x += TS / 2
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.3, location=(x + 0.35, y, 0.15), vertices=48); bpy.context.object.data.materials.append(blue)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.19, depth=0.05, location=(x + 0.35, y, 0.29), vertices=48); bpy.context.object.data.materials.append(base)
    b3d.stack_camera((0, -0.1, 0.1), 4.4, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
