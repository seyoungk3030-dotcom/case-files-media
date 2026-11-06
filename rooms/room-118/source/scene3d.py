"""ROOM 118 3D sprites: two mirror panels standing on a dark round table, hinged at the back and opening toward the
viewer at the board's angle; a coral toy pawn stands on the middle line; an amber tag in front shows the angle and
an amber arc marks it at the hinge. p*: the mirror faces are drawn matte (no reflections, so nothing is given away).
a*: the mirrors become real mirrors and the reflected toys appear."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
LM, HM, HY = 2.3, 1.3, 1.1


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m, rot=(math.radians(90), 0, 0)):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def scene(k, after):
    T = BOARDS[k]['angle']; sc = bpy.context.scene
    sc.cycles.max_bounces = 32; sc.cycles.glossy_bounces = 32; sc.cycles.transparent_max_bounces = 16
    table = b3d.mat('table', (0.035, 0.045, 0.075), rough=0.6, coat=0.1)
    face = b3d.mat('mirror', (0.95, 0.96, 0.98), rough=0.0, metal=1.0, coat=0) if after else b3d.mat('matte', (0.55, 0.6, 0.68), rough=0.55, metal=0.3, coat=0)
    frame = b3d.mat('frame', (0.05, 0.06, 0.09), rough=0.5, coat=0.1)
    toy = b3d.mat('toy', (0.95, 0.35, 0.3), rough=0.35, coat=0.4); amber = b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0.1)
    ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    bpy.ops.mesh.primitive_cylinder_add(radius=2.5, depth=0.12, location=(0, -0.3, -0.06), vertices=96); bpy.context.object.data.materials.append(table)
    for s in (-1, 1):
        a = math.radians(-90 + s * T / 2)          # direction from the hinge toward the viewer side
        dx, dy = math.cos(a), math.sin(a)
        cx, cy = HY + 0 * dx, 0
        bpy.ops.mesh.primitive_cube_add(size=1, location=(LM / 2 * dx, HY + LM / 2 * dy, HM / 2))
        o = bpy.context.object; o.scale = (LM, 0.05, HM); o.rotation_euler = (0, 0, a); o.data.materials.append(face)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(LM / 2 * dx - s * 0.04 * dy, HY + LM / 2 * dy + s * 0.04 * dx, HM / 2))
        o = bpy.context.object; o.scale = (LM, 0.03, HM + 0.04); o.rotation_euler = (0, 0, a); o.data.materials.append(frame)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=HM + 0.1, location=(0, HY, HM / 2), vertices=16); bpy.context.object.data.materials.append(frame)
    # amber arc at the hinge
    n = 24
    for i in range(n):
        a = math.radians(-90 - T / 2 + T * (i + 0.5) / n)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0.55 * math.cos(a), HY + 0.55 * math.sin(a), 0.01)); o = bpy.context.object
        o.scale = (0.05, 0.6 * math.radians(T) / n + 0.01, 0.02); o.rotation_euler = (0, 0, a); o.data.materials.append(amber)
    # toy pawn on the middle line
    ty = HY - 1.15
    bpy.ops.mesh.primitive_cone_add(radius1=0.16, radius2=0.07, depth=0.42, location=(0, ty, 0.21), vertices=32); bpy.context.object.data.materials.append(toy)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(0, ty, 0.5)); o = bpy.context.object; o.data.materials.append(toy)
    for p in o.data.polygons: p.use_smooth = True
    # angle tag in front
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -2.45, 0.3)); o = bpy.context.object; o.scale = (1.1, 0.08, 0.55); o.rotation_euler = (math.radians(-20), 0, 0)
    o.data.materials.append(amber); b3d.bevel(o, 0.08)
    text(f'{T}°', (0, -2.51, 0.3), 0.42, ink, (math.radians(70), 0, 0))
    b3d.stack_camera((0, -0.5, 0.6), 6.4, az=0.0, el=38.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 900), 64); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
