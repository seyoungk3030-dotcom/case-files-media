"""VOTE 001 sprite: a white fridge with its door swung open, cold blue light and mist at the front, shelves inside, and
the warm vent grille at the bottom glowing orange with heat shimmer rising (the hint: heat comes out too)."""
import math, os, sys
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
import b3d
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)


def glowm(name, c, s, alpha=1.0):
    m = b3d.mat(name, c, rough=0.4, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; q.inputs['Alpha'].default_value = alpha
    return m


def box(m, loc, sc, bev=0.02, rz=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=(0, 0, rz)); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


b3d.reset((800, 900), 64); b3d.lights(3)
white = b3d.mat('white', (0.78, 0.8, 0.84), rough=0.35, coat=0.5); inner = b3d.mat('inner', (0.85, 0.92, 1.0), rough=0.5, coat=0)
W, D, H = 0.7, 0.65, 1.8
box(white, (0, 0.03, H / 2 + 0.08), (W, 0.06, H), 0.01)                       # back
for sx in (-1, 1): box(white, (sx * (W / 2 - 0.03), -D / 2 + 0.06, H / 2 + 0.08), (0.06, D, H), 0.01)
box(white, (0, -D / 2 + 0.06, H + 0.05), (W, D, 0.06), 0.02); box(white, (0, -D / 2 + 0.06, 0.11), (W, D, 0.06), 0.01)
box(white, (0, -D / 2 + 0.06, 1.2), (W, D, 0.05), 0.01)                       # freezer divider
box(glowm('innerlight', (0.55, 0.75, 1.0), 0.5), (0, -0.02, 0.66), (W - 0.14, 0.02, 1.0), 0)
for z in (0.45, 0.8): box(b3d.mat('shelf', (0.8, 0.9, 1.0), rough=0.05, coat=0), (0, -D / 2 + 0.06, z), (W - 0.12, D - 0.1, 0.015), 0)
for x, z, c in ((-0.15, 0.53, (0.95, 0.3, 0.25)), (0.12, 0.53, (0.3, 0.75, 0.35)), (-0.05, 0.88, (0.98, 0.85, 0.3)), (0.18, 0.9, (0.95, 0.95, 0.95))):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.14, location=(x, -0.3, z)); bpy.context.object.data.materials.append(b3d.mat(f'f{x}', c, rough=0.4, coat=0.4))
hx, hy = W / 2, -0.62; ang = math.radians(-105)
box(white, (hx + math.cos(ang) * W / 2, hy + math.sin(ang) * W / 2, 0.66), (W, 0.07, 1.06), 0.02, rz=ang)
box(white, (0, -0.625, 1.5), (W, 0.07, 0.58), 0.02)
box(b3d.mat('handle', (0.6, 0.62, 0.66), rough=0.2, metal=1, coat=0), (-0.28, -0.67, 1.5), (0.03, 0.04, 0.3), 0.01)
box(glowm('vent', (1.0, 0.25, 0.03), 1.5), (0, -0.6, 0.05), (W - 0.08, 0.02, 0.08), 0)
for i, x in enumerate((-0.2, 0.0, 0.2)):
    for j in range(5):
        z = 0.12 + j * 0.06; xx = x + 0.03 * math.sin(j * 1.5 + i)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.022, location=(xx, -0.68, z)); bpy.context.object.data.materials.append(glowm(f'h{i}{j}', (1.0, 0.3, 0.05), 1.2, 0.9 - j * 0.15))
mist = glowm('mist', (0.6, 0.8, 1.0), 0.3, 0.18)
for k in range(6):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.07 + 0.02 * (k % 3), location=(-0.2 + 0.05 * k, -0.75 - 0.03 * (k % 2), 0.95 - 0.1 * k)); bpy.context.object.data.materials.append(mist)
b3d.stack_camera((0.0, -0.3, 0.95), 2.0, az=-28.0, el=10.0)
b3d.render(f'{OUT}/fridge.png'); print('ok')
