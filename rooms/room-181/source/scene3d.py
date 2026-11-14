"""ROOM 181 3D sprites: a kitchen shelf of jam jars (upright, lid on top) and squeeze bottles (standing upside down on
their flip lid). A yellow arrow wraps around the front of every lid, showing which way it is being twisted, seen from
the viewer above. p*: question. a*: answer, arrows of lids that come off turn mint, the rest turn red."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, opens
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
JAM = [(0.7, 0.1, 0.2), (0.95, 0.55, 0.1), (0.45, 0.15, 0.45)]
SQZ = [(0.85, 0.12, 0.1), (0.95, 0.8, 0.15), (0.2, 0.5, 0.85), (0.3, 0.7, 0.4)]


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def cyl(loc, r, d, m, v=48, r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, vertices=v)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r, radius2=r2, depth=d, location=loc, vertices=v)
    o = bpy.context.object; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def arrow(cx, z, r, ccw, m):
    a0, a1 = (205, 335) if ccw else (335, 205); n = 12
    for i in range(n):
        a = math.radians(a0 + (a1 - a0) * (i + 0.5) / (n + 1.5)); x, y = cx + r * math.cos(a), r * math.sin(a)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z), rotation=(0, 0, a)); o = bpy.context.object; o.scale = (0.08, 0.1, 0.07); o.data.materials.append(m)
    ah = math.radians(a1); x, y = cx + r * math.cos(ah), r * math.sin(ah)
    tang = ah + (math.pi / 2 if ccw else -math.pi / 2)
    bpy.ops.mesh.primitive_cone_add(radius1=0.17, depth=0.34, location=(x, y, z), rotation=(0, math.pi / 2, tang)); bpy.context.object.data.materials.append(m)


def scene(k, after):
    items = BOARDS[k]; n = len(items); sp = 1.05
    wood = b3d.mat('wood', (0.55, 0.36, 0.2), rough=0.5, coat=0.3)
    lidm = b3d.mat('lid', (0.75, 0.72, 0.68), rough=0.45, metal=0.5, coat=0); flip = b3d.mat('flip', (0.96, 0.96, 0.95), rough=0.35, coat=0.3)
    yel = glowm('yel', (1.0, 0.7, 0.05), 0.5); mint = glowm('mint', (0.05, 0.8, 0.5), 0.5); red = glowm('red', (0.9, 0.1, 0.1), 0.5)
    W = n * sp + 0.4
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.1, -0.08)); o = bpy.context.object; o.scale = (W, 1.5, 0.16); o.data.materials.append(wood)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.9, 0.85)); o = bpy.context.object; o.scale = (W, 0.1, 1.9); o.data.materials.append(b3d.mat('wall', (0.3, 0.36, 0.42), rough=0.7, coat=0))
    for i, it in enumerate(items):
        cx = (i - (n - 1) / 2) * sp; kind, a = it
        m = (mint if opens(it) else red) if after else yel
        if kind == 'J':
            jm = b3d.mat(f'j{i}', JAM[i % 3], rough=0.2, coat=0.8)
            cyl((cx, 0, 0.42), 0.38, 0.84, jm)
            cyl((cx, 0, 0.75), 0.36, 0.08, b3d.mat(f'lab{i}', (0.97, 0.94, 0.85), rough=0.6, coat=0), r2=0.36)
            cyl((cx, 0, 0.93), 0.41, 0.2, lidm, 64)
            arrow(cx, 0.93, 0.55, a == 'L', m)
        else:
            bm = b3d.mat(f'b{i}', SQZ[i % 4], rough=0.25, coat=0.6)
            cyl((cx, 0, 0.13), 0.3, 0.26, flip, 64)                    # flip lid on the shelf
            cyl((cx, 0, 0.36), 0.22, 0.2, bm, 48, r2=0.36)             # shoulder (narrow at the lid)
            cyl((cx, 0, 0.98), 0.36, 1.05, bm)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.36, location=(cx, 0, 1.5)); o = bpy.context.object; o.scale = (1, 1, 0.35); o.data.materials.append(bm); bpy.ops.object.shade_smooth()
            arrow(cx, 0.13, 0.45, a == 'L', m)
    b3d.stack_camera((0, 0, 0.75), 7.4, az=0.0, el=38.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((1000, 560), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
