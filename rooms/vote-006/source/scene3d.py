"""VOTE 006 sprite: two bathroom scales side by side, a toy figure standing on two feet on the left one and on one foot
(other leg bent up) on the right one; both displays show '?'."""
import math, os, sys
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
import b3d
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.4, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def box(m, loc, sc, bev=0.02, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def limb(m, p, q, r):
    dx, dz = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dz)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=((p[0] + q[0]) / 2, p[2], (p[1] + q[1]) / 2), rotation=(0, math.atan2(dx, dz), 0))
    bpy.context.object.data.materials.append(m)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(q[0], p[2], q[1])); bpy.context.object.data.materials.append(m)


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts.load(FONT); t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def person(x, one_foot):
    skin = b3d.mat('skin', (0.95, 0.75, 0.6), rough=0.5, coat=0); shirt = b3d.mat('shirt', (0.25, 0.55, 0.95), rough=0.5, coat=0.2)
    pants = b3d.mat('pants', (0.2, 0.22, 0.3), rough=0.6, coat=0)
    z0 = 0.2
    sx = 0.0 if one_foot else -0.16
    limb(pants, (x + sx, z0 + 1.0, 0), (x + sx, z0 + 0.06, 0), 0.1)
    if one_foot: limb(pants, (x + 0.16, z0 + 1.0, 0), (x + 0.42, z0 + 0.62, 0), 0.1); limb(pants, (x + 0.42, z0 + 0.62, 0), (x + 0.2, z0 + 0.32, 0), 0.09)
    else: limb(pants, (x + 0.16, z0 + 1.0, 0), (x + 0.16, z0 + 0.06, 0), 0.1)
    box(shirt, (x, 0, z0 + 1.4), (0.6, 0.3, 0.85), 0.1)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(x, 0, z0 + 2.1)); bpy.context.object.data.materials.append(skin)
    for s in (-1, 1): limb(shirt, (x + s * 0.38, z0 + 1.75, 0), (x + s * (0.75 if one_foot else 0.45), z0 + (1.55 if one_foot else 1.05), 0), 0.08)


b3d.reset((1000, 800), 64); b3d.lights(3)
for x, one in ((-1.1, False), (1.1, True)):
    box(b3d.mat('scale', (0.92, 0.93, 0.95), rough=0.3, coat=0.8), (x, 0, 0.1), (1.3, 1.1, 0.2), 0.08)
    box(b3d.mat('disp', (0.05, 0.08, 0.1), rough=0.3, coat=0), (x, -0.56, 0.1), (0.6, 0.02, 0.16), 0.01)
    text('? kg', (x, -0.58, 0.1), 0.15, glowm('lcd', (0.3, 1.0, 0.6), 1.2))
    person(x, one)
b3d.stack_camera((0, 0, 1.15), 4.2, az=0.0, el=12.0)
b3d.render(f'{OUT}/scales.png'); print('ok')
