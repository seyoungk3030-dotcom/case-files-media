"""ROOM 202 3D sprites, side view: a building of the board's height (drawn the same size every time; height on the card),
a ball at the roof edge and an amber arrow showing how it leaves (straight down = let go, sideways = thrown).
a*: the mint dotted path to where it lands, drawn to the same scale as the building."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD, G
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
H = 3.0
BALL = {'야구공': ((0.95, 0.95, 0.92), 0.12), '볼링공': ((0.12, 0.12, 0.35), 0.17), '탁구공': ((1.0, 0.55, 0.15), 0.09), '테니스공': ((0.8, 0.95, 0.2), 0.12)}


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def box(m, loc, sc, bev=0.03):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def arrow(m, p, d, L=0.6):
    import mathutils
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=L - 0.18, location=(p[0] + d[0] * (L - 0.18) / 2, 0, p[1] + d[1] * (L - 0.18) / 2), vertices=16)
    o = bpy.context.object; o.rotation_euler = (0, math.atan2(d[0], d[1]), 0); o.data.materials.append(m)
    bpy.ops.mesh.primitive_cone_add(radius1=0.1, radius2=0, depth=0.18, location=(p[0] + d[0] * (L - 0.09), 0, p[1] + d[1] * (L - 0.09)), vertices=24)
    o = bpy.context.object; o.rotation_euler = (0, math.atan2(d[0], d[1]), 0); o.data.materials.append(m)


def scene(key, after):
    h, u, ball = BOARDS[key]; s = H / h; t = GOOD[key]
    wall = b3d.mat('bld', (0.22, 0.28, 0.42), rough=0.4, coat=0.3); win = glowm('win', (1.0, 0.82, 0.45), 1.8)
    ground = b3d.mat('ground', (0.3, 0.5, 0.25), rough=0.8, coat=0)
    box(ground, (1.3, 0, -0.06), (4.6, 1.4, 0.12), 0.02)
    box(wall, (-0.5, 0.1, H / 2), (1.0, 1.0, H), 0.04)
    box(b3d.mat('roof', (0.35, 0.38, 0.45), rough=0.4, coat=0), (-0.5, 0.1, H + 0.04), (1.08, 1.08, 0.08), 0.02)
    fl = max(2, round(h / 3)); fh = H / fl   # about 3 m per floor, so the windows show how tall it is
    for i in range(fl):
        for x in (-0.75, -0.25): box(win, (x, -0.405, (i + 0.5) * fh), (0.26, 0.02, min(0.6 * fh, 0.5)), min(0.01, 0.1 * fh))
    col, r = BALL[ball]
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(r + 0.04, 0, H + 0.08 + r), segments=48, ring_count=24)
    o = bpy.context.object; o.data.materials.append(b3d.mat('ball', col, rough=0.3, coat=0.6)); bpy.ops.object.shade_smooth()
    am = glowm('amber', (1.0, 0.72, 0.2), 1.4); p0 = (r + 0.04, H + 0.08 + r)
    if u: arrow(am, (p0[0] + r + 0.05, p0[1]), (1, 0))
    else: arrow(am, (p0[0] + r + 0.25, p0[1] - 0.05), (0, -1))
    if after:
        mint = glowm('mint', (0.2, 0.95, 0.65), 1.6); n = 26
        for i in range(2, n + 1):
            tt = t * i / n; x = p0[0] + u * tt * s; z = p0[1] - 0.5 * G * tt * tt * s
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=(x, 0, max(z, 0.04)), segments=12, ring_count=8)
            bpy.context.object.data.materials.append(mint)
    b3d.stack_camera((1.2, 0, 1.6), 4.6, az=12.0, el=8.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((700, 700), 40); b3d.lights(3)
        t0 = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t0, 1), flush=True)
