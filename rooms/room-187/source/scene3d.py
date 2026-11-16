"""ROOM 187 3D sprites: a person stands in front of a wall, seen from the side at an angle. Tags give their height and
their distance to the wall. p*: question, a '?' on the wall. a*: answer, the smallest mirror (h/2 tall, made of 20 cm
tiles) glued at the right height, with the light paths head -> mirror -> eye and feet -> mirror -> eye in yellow."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, need, eye, TILE
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
WALL = 2.0


def glowm(name, c, s, rough=0.3, metal=0.0):
    m = b3d.mat(name, c, rough=rough, metal=metal, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def box(m, loc, scale):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale; o.data.materials.append(m); return o


def cyl(m, a, b, r):
    a, b = [complex(*p) for p in ((a[0], a[1]), (b[0], b[1]))] if False else (a, b)
    dx, dy, dz = b[0] - a[0], b[1] - a[1], b[2] - a[2]; L = math.sqrt(dx * dx + dy * dy + dz * dz)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2), vertices=24)
    o = bpy.context.object; o.rotation_euler = (0, math.acos(dz / L), math.atan2(dy, dx)); o.data.materials.append(m); return o


def text(s, loc, size, m, rot=(math.pi / 2, 0, 0)):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def person(x, h, skin, cloth, dark):
    s = h / 1.6
    for dy in (-0.07 * s, 0.07 * s):
        cyl(cloth, (x, dy, 0.0), (x, dy, 0.48 * h), 0.055 * s)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15 * s, location=(x, 0, 0.66 * h)); o = bpy.context.object; o.scale = (0.8, 1.0, 1.25 * 0.82 * h / (1.6 * 0.82) / s); o.data.materials.append(cloth); bpy.ops.object.shade_smooth()
    o.scale = (0.75, 1.0, (0.2 * h) / (0.15 * s))
    for dy in (-0.2 * s, 0.2 * s):
        cyl(cloth, (x, dy, 0.8 * h), (x + 0.03 * s, dy * 1.05, 0.5 * h), 0.04 * s)
    cyl(skin, (x, 0, 0.82 * h), (x, 0, 0.87 * h), 0.04 * s)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.07 * h, location=(x, 0, 0.93 * h)); o = bpy.context.object; o.data.materials.append(skin); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.012 * h, location=(x + 0.062 * h, -0.025 * h, eye(h) / 100 * 100 * 0 + 0.93 * h)); bpy.context.object.data.materials.append(dark)
    bpy.ops.mesh.primitive_cone_add(radius1=0.014 * h, depth=0.03 * h, location=(x + 0.075 * h, 0, 0.915 * h), rotation=(0, math.pi / 2, 0)); bpy.context.object.data.materials.append(skin)


def scene(k, after):
    hcm, d = BOARDS[k]; h = hcm / 100; e = eye(hcm) / 100; x = -d
    wall = b3d.mat('wall', (0.16, 0.18, 0.24), rough=0.8, coat=0); floor = b3d.mat('floor', (0.30, 0.20, 0.13), rough=0.5, coat=0.2)
    skin = b3d.mat('skin', (0.95, 0.75, 0.6), rough=0.5, coat=0); cloth = b3d.mat('cloth', (0.2, 0.45, 0.85), rough=0.5, coat=0.1)
    dark = b3d.mat('dark', (0.03, 0.03, 0.04), rough=0.4, coat=0); wh = glowm('wh', (0.96, 0.97, 1.0), 0.8)
    yel = glowm('yel', (1.0, 0.8, 0.15), 2.0); mir = glowm('mir', (0.55, 0.95, 0.85), 0.9, rough=0.05, metal=0.6); seam = b3d.mat('seam', (0.1, 0.12, 0.14), rough=0.5, coat=0)
    box(wall, (0.06, 0, WALL / 2), (0.12, 1.2, WALL))
    box(floor, (-1.25, 0, -0.03), (2.7, 1.2, 0.06))
    person(x, h, skin, cloth, dark)
    # height tag: bar behind the person, label above it
    bx = x - 0.32
    cyl(wh, (bx, -0.3, 0.0), (bx, -0.3, h), 0.012)
    for z in (0.0, h): cyl(wh, (bx - 0.06, -0.3, z), (bx + 0.06, -0.3, z), 0.012)
    text(f'{hcm}cm', (bx, -0.3, h + 0.17), 0.24, wh)
    # distance tag on the floor, from the person's front to the wall
    cyl(yel if False else wh, (x + 0.08, -0.45, 0.02), (-0.01, -0.45, 0.02), 0.012)
    text(f'{d:g}m', ((x + 0.08) / 2, -0.45, 0.2), 0.24, wh)
    if not after:
        text('?', (-0.01, 0, 1.0), 0.5, wh, rot=(math.pi / 2, 0, -math.pi / 2))
    else:
        L, bot, top = need(hcm, d); bot /= 100; top /= 100; n = round(L / TILE)
        box(mir, (-0.012, 0, (bot + top) / 2), (0.02, 0.5, top - bot))
        for i in range(1, n): box(seam, (-0.025, 0, bot + i * TILE / 100), (0.012, 0.5, 0.012))
        fx = x + 0.07 * h; ex = x + 0.07 * h
        for z0, zb in ((h, top), (0.0, bot)):
            cyl(yel, (fx, 0, z0), (-0.03, 0, zb), 0.01); cyl(yel, (-0.03, 0, zb), (ex, 0, e), 0.01)
    b3d.stack_camera((-1.05, 0, 1.0), 3.3, az=-28.0, el=6.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((800, 760), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
