"""ROOM 135 3D sprites: two straight rails rising from a low end (one block) to a high end (two blocks), their gap
widening or narrowing; a wooden solid (double cone, cylinder or hourglass) rests across them in the middle. Number
signs stand at both ends. p*: the solid in the middle. a*: the solid at the end it rolls to, a mint arrow along the
rails and the sign there glowing."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, SHAPES, X, SLOPE, HALF
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
AZ, EL, H0, VS = -18.0, 48.0, 0.3, 3.0     # VS: vertical exaggeration of the rise (drawn only)


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def facing(): return (math.radians(90 - EL), 0, math.radians(AZ))


def cam_dir(): return Vector((math.sin(math.radians(AZ)) * math.cos(math.radians(EL)), -math.cos(math.radians(AZ)) * math.cos(math.radians(EL)), math.sin(math.radians(EL))))


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=facing()); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def rod(a, b, r, m, v=16):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=v); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y'); o.data.materials.append(m); return o


def zr(x): return H0 + SLOPE * VS * x


def solid(shape, c, m, dark):
    f = SHAPES[shape]; n = 24; verts, faces = [], []
    ys = [-HALF + 2 * HALF * i / n for i in range(n + 1)]; seg = 48
    for y in ys:
        r = f(y)
        for j in range(seg): a = 2 * math.pi * j / seg; verts.append((c.x + r * math.cos(a), c.y + y, c.z + r * math.sin(a)))
    for i in range(n):
        for j in range(seg): faces.append([i * seg + j, i * seg + (j + 1) % seg, (i + 1) * seg + (j + 1) % seg, (i + 1) * seg + j])
    for end in (0, n):
        verts.append((c.x, c.y + ys[end], c.z)); ci = len(verts) - 1
        for j in range(seg): faces.append([ci, end * seg + (j + 1) % seg, end * seg + j] if end == 0 else [ci, end * seg + j, end * seg + (j + 1) % seg])
    me = bpy.data.meshes.new('solid'); me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new('solid', me); bpy.context.collection.objects.link(o); o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = True
    bpy.ops.mesh.primitive_torus_add(location=c, rotation=(math.radians(90), 0, 0), major_radius=f(0) + 0.005, minor_radius=0.02); bpy.context.object.data.materials.append(dark)


def scene(k, after):
    b = BOARDS[k]; s0, s1 = b['s']; end_high = RES[k][0] == b['high']
    wood = b3d.mat('wood', (0.8, 0.55, 0.28), rough=0.5, coat=0.2); dark = b3d.mat('dark', (0.35, 0.2, 0.08), rough=0.5, coat=0)
    rail = b3d.mat('rail', (0.75, 0.77, 0.82), rough=0.3, metal=0.9, coat=0); block = b3d.mat('block', (0.22, 0.25, 0.33), rough=0.6, coat=0)
    base = b3d.mat('base', (0.06, 0.07, 0.1), rough=0.7, coat=0); chip = b3d.mat('chip', (0.94, 0.95, 0.97), rough=0.5, coat=0)
    ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0); mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.6)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(X / 2, 0, -0.05)); o = bpy.context.object; o.scale = (X + 2.4, 3.4, 0.1); o.data.materials.append(base); b3d.bevel(o, 0.05)
    for x, nb in ((0.0, 1), (X, 2)):
        for i in range(nb):
            hb = zr(x) / nb
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, hb / 2 + i * hb)); o = bpy.context.object; o.scale = (0.35, 2 * max(s0, s1) + 0.5, hb - 0.02); o.data.materials.append(block); b3d.bevel(o, 0.02)
    for sy in (-1, 1): rod((-0.2, sy * s0, zr(-0.2) + 0.04), (X + 0.2, sy * s1, zr(X + 0.2) + 0.04), 0.045, rail)
    xp = (X - 0.45 if end_high else 0.45) if after else X / 2
    s = s0 + (s1 - s0) * xp / X; c = Vector((xp, 0, zr(xp) + 0.04 + SHAPES[b['shape']](s)))
    solid(b['shape'], c, wood, dark)
    if after:
        d = 1 if end_high else -1; a = Vector((X / 2 - d * 0.6, -max(s0, s1) - 0.6, zr(X / 2) + 0.1)); bb = a + Vector((d * 1.4, 0, 0))
        rod(a, bb, 0.05, mint); bpy.ops.mesh.primitive_cone_add(radius1=0.13, depth=0.3, location=bb + Vector((d * 0.15, 0, 0)), rotation=(0, math.radians(90 * d), 0)); bpy.context.object.data.materials.append(mint)
    for x, num, hi in ((-0.75, b['low'], False), (X + 0.75, b['high'], True)):
        hit = after and hi == end_high; cpos = Vector((x, 0, zr(max(0, min(X, x))) + 0.9))
        rod((x, 0, 0), (x, 0, cpos.z - 0.3), 0.03, block)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.32, depth=0.05, location=cpos, rotation=facing(), vertices=32); bpy.context.object.data.materials.append(mint if hit else chip)
        text(str(num), cpos + cam_dir() * 0.03, 0.4, ink)
    b3d.stack_camera((X / 2, 0, 0.6), 7.4, az=AZ, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 640), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
