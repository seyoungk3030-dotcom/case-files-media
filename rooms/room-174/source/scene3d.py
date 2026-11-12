"""ROOM 174 3D sprites: a stone well cut open from the front, with a metre scale on its left wall (0 at the bottom, the
depth at the rim), a snail at the bottom and a sign above: daytime climb and night slide. p*: as above. a*: the
snail sitting on the rim, its zigzag path drawn on the back wall (mint dots = daytime highs, coral = night lows) and the
day count on the sign."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
M = 0.32; IW = 0.95; WT = 0.22  # metre in scene units, inner width, wall thickness


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def box(loc, scale, m, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def text(s, loc, size, m, align='CENTER'):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = align; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def ball(loc, r, m, sc=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=32, ring_count=16); o = bpy.context.object; o.scale = sc
    bpy.ops.object.shade_smooth(); o.data.materials.append(m); return o


def snail(x, z, shell, bodym, ink):
    ball((x, -0.05, z + 0.07), 0.07, bodym, (2.4, 1, 0.8))
    ball((x - 0.04, -0.05, z + 0.2), 0.13, shell)
    bpy.ops.mesh.primitive_torus_add(location=(x - 0.04, -0.12, z + 0.2), rotation=(math.pi / 2, 0, 0), major_radius=0.07, minor_radius=0.022)
    bpy.context.object.data.materials.append(bodym)
    for dx in (0.12, 0.17):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.14, location=(x + dx, -0.05, z + 0.16), rotation=(0, 0.35, 0)); bpy.context.object.data.materials.append(bodym)
        ball((x + dx + 0.024, -0.05, z + 0.23), 0.022, ink)


def scene(k, after):
    H, U, D = BOARDS[k]; top = H * M
    stone = b3d.mat('stone', (0.2, 0.19, 0.18), rough=0.8, coat=0); back = b3d.mat('back', (0.12, 0.12, 0.13), rough=0.9, coat=0)
    mud = b3d.mat('mud', (0.3, 0.22, 0.15), rough=0.9, coat=0); ink = b3d.mat('ink', (0.05, 0.05, 0.07), rough=0.5, coat=0)
    white = b3d.mat('white', (0.97, 0.97, 0.95), rough=0.5, coat=0); sign = b3d.mat('sign', (0.03, 0.035, 0.05), rough=0.4, coat=0.3)
    shell = b3d.mat('shell', (0.95, 0.6, 0.25), rough=0.3, coat=0.6); bodym = b3d.mat('bodym', (0.85, 0.8, 0.55), rough=0.4, coat=0.3)
    yel = glowm('yel', (1.0, 0.8, 0.2), 1.6); mint = glowm('mint', (0.15, 0.85, 0.6), 2.0); coral = glowm('coral', (1.0, 0.4, 0.35), 2.0)
    for sx in (-1, 1): box((sx * (IW / 2 + WT / 2), 0, top / 2 - 0.1), (WT, 0.6, top + 0.2), stone, 0.03)
    box((0, 0.3, top / 2 - 0.1), (IW + 2 * WT, 0.06, top + 0.2), back)
    box((0, 0, -0.15), (IW + 2 * WT, 0.6, 0.1), mud)
    for i in range(H + 1):  # metre scale on the inside of the left wall
        z = i * M; box((-IW / 2 + 0.07, 0.24, z), (0.14 if i % H else 0.2, 0.02, 0.018), white)
        text(str(i), (-IW / 2 - WT / 2, -0.31, z), 0.16, white)
    text('m', (-IW / 2 - WT / 2, -0.31, top + 0.2), 0.14, white)
    box((0, 0, top + 0.62), (1.45, 0.08, 0.78), sign, 0.04)
    if after: text(f'{GOOD[k]}일째', (0, -0.05, top + 0.8), 0.3, mint); text('탈출', (0, -0.05, top + 0.45), 0.3, mint)
    else: text(f'낮 +{U}m', (0, -0.05, top + 0.8), 0.3, yel); text(f'밤 -{D}m', (0, -0.05, top + 0.45), 0.3, yel)
    if after:
        h, pts, day = 0, [(0.0, 0)], 0
        while True:
            day += 1; h += U; pts.append((h if h < H else H, 1))
            if h >= H: break
            h -= D; pts.append((h, 0))
        n = len(pts); xs = [-IW / 2 + 0.25 + (IW - 0.45) * i / (n - 1) for i in range(n)]
        for i in range(n - 1):
            a = (xs[i], pts[i][0] * M); b = (xs[i + 1], pts[i + 1][0] * M); ln = math.dist(a, b)
            bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=ln, location=((a[0] + b[0]) / 2, 0.25, (a[1] + b[1]) / 2),
                                                rotation=(0, math.atan2(b[0] - a[0], b[1] - a[1]), 0))
            bpy.context.object.data.materials.append(white)
        for i, (z, up) in enumerate(pts[1:], 1): ball((xs[i], 0.24, z * M), 0.045, mint if up else coral)
        snail(IW / 2 - 0.12, top + 0.06, shell, bodym, ink)
    else:
        snail(0.0, -0.1, shell, bodym, ink)
    b3d.stack_camera((0.0, 0, 9 * M / 2 + 0.3), 9 * M + 1.9, az=0.0, el=6.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((800, 1000), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
