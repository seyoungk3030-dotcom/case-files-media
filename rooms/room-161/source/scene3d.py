"""ROOM 161 3D sprites: an upright wooden ladder board (사다리 타기) seen from the front. Five metal lanes, crossbars
between neighbours, a steel marble above the starting lane (yellow arrow) and five numbered bins at the bottom.
p*: the start. a*: the marble's route glows mint and the marble sits in its bin."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, L, H
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
DX = 0.85; DZ = 0.4; TOP = 4.0; BOT = TOP - (H + 0.5) * DZ; EL = 8.0


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def X(i): return (i - (L - 1) / 2) * DX
def Z(lv): return TOP - (lv + 0.5) * DZ


def rod(p, q, r, m, y=0.0):
    (x0, z0), (x1, z1) = p, q; ln = math.hypot(x1 - x0, z1 - z0)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=ln, location=((x0 + x1) / 2, y, (z0 + z1) / 2), vertices=20)
    o = bpy.context.object; o.rotation_euler = (0, math.atan2(x1 - x0, z1 - z0), 0); o.data.materials.append(m)
    for x, z in (p, q):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(x, y, z), segments=16, ring_count=8); bpy.context.object.data.materials.append(m)


def scene(k, after):
    b = BOARDS[k]; end, pts = RES[k]
    wood = b3d.mat('wood', (0.17, 0.1, 0.06), rough=0.75, coat=0); steel = b3d.mat('steel', (0.8, 0.82, 0.86), rough=0.25, metal=1.0, coat=0)
    bar = b3d.mat('bar', (0.95, 0.6, 0.2), rough=0.4, coat=0.3); binm = b3d.mat('bin', (0.18, 0.2, 0.26), rough=0.5, coat=0)
    wht = b3d.mat('wht', (0.97, 0.97, 0.97), rough=0.5, coat=0); glow(wht, (1, 1, 1), 0.5)
    yel = b3d.mat('yel', (1.0, 0.82, 0.2), rough=0.4, coat=0); glow(yel, (1.0, 0.8, 0.15), 0.8)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.2)
    ball = b3d.mat('ball', (0.9, 0.12, 0.1), rough=0.15, coat=0.8)
    ink = b3d.mat('ink', (0.05, 0.06, 0.08), rough=0.8, coat=0)
    W = (L - 1) * DX + 0.9
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.2, (TOP + 0.55 + BOT - 0.75) / 2)); o = bpy.context.object
    o.scale = (W, 0.12, TOP + 0.55 - BOT + 0.75); o.data.materials.append(wood); b3d.bevel(o, 0.06)
    for i in range(L):
        rod((X(i), TOP), (X(i), BOT), 0.035, steel)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(X(i), -0.05, BOT - 0.33)); o = bpy.context.object; o.scale = (DX - 0.12, 0.42, 0.55)
        o.data.materials.append(mint if after and i == end else binm); b3d.bevel(o, 0.05)
        text(str(b['bins'][i]), (X(i), -0.27, BOT - 0.33), 0.36, ink if after and i == end else wht)
    for lv, i in b['bars']: rod((X(i), Z(lv)), (X(i + 1), Z(lv)), 0.05, bar)
    if not after:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.16, location=(X(b['start']), -0.05, TOP + 0.22), segments=32, ring_count=16); bpy.context.object.data.materials.append(ball)
        bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.12, depth=0.03, location=(X(b['start']) - 0.3, -0.12, TOP + 0.22), rotation=(math.pi / 2, math.pi / 2, 0))
        bpy.context.object.data.materials.append(yel)
    else:
        q = [(X(p), TOP if lv == -1 else (BOT if lv == H else Z(lv))) for p, lv in pts]
        for a, c in zip(q, q[1:]):
            if a != c: rod(a, c, 0.07, mint, y=-0.06)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.16, location=(X(end) + 0.3, -0.35, BOT + 0.12), segments=32, ring_count=16); bpy.context.object.data.materials.append(ball)
    b3d.stack_camera((0, 0, (TOP + 0.5 + BOT - 0.65) / 2), W + 1.0, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((800, 900), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
