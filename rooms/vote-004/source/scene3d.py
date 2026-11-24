"""VOTE 004 sprite: a tall glass of ice water on a wooden coaster, with water droplets beaded on the outside and a small
wet ring on the coaster."""
import math, os, random, sys
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
import b3d
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
random.seed(7)


def clear(name, c, a, rough=0.05):
    m = b3d.mat(name, c, rough=rough, coat=0.5); m.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = a; return m


b3d.reset((700, 900), 64); b3d.lights(3)
bpy.ops.mesh.primitive_cylinder_add(radius=1.1, depth=0.12, location=(0, 0, 0.06), vertices=64); bpy.context.object.data.materials.append(b3d.mat('coaster', (0.6, 0.4, 0.22), rough=0.6, coat=0.2))
bpy.ops.mesh.primitive_cylinder_add(radius=0.82, depth=0.01, location=(0, 0, 0.125), vertices=64); bpy.context.object.data.materials.append(clear('wet', (0.35, 0.22, 0.12), 0.7, 0.02))
R0, R1, H = 0.62, 0.72, 2.2
bpy.ops.mesh.primitive_cone_add(radius1=R0, radius2=R1, depth=H, location=(0, 0, 0.12 + H / 2), vertices=64); g = bpy.context.object
g.data.materials.append(clear('glass', (0.85, 0.93, 1.0), 0.18))
bpy.ops.mesh.primitive_cone_add(radius1=R0 - 0.05, radius2=R0 - 0.05 + (R1 - R0) * 0.75, depth=H * 0.75, location=(0, 0, 0.17 + H * 0.375), vertices=64)
bpy.context.object.data.materials.append(clear('water', (0.5, 0.75, 1.0), 0.35))
ice = clear('ice', (0.9, 0.96, 1.0), 0.6, 0.15)
for i in range(7):
    a = random.uniform(0, 6.28); r = random.uniform(0, 0.3)
    bpy.ops.mesh.primitive_cube_add(size=0.38, location=(r * math.cos(a), r * math.sin(a), 0.6 + i * 0.22), rotation=(random.random(), random.random(), random.random()))
    o = bpy.context.object; o.data.materials.append(ice); b3d.bevel(o, 0.05, 3)
drop = clear('drop', (0.85, 0.95, 1.0), 0.4, 0.0)
for i in range(160):
    z = random.uniform(0.3, 0.12 + H * 0.78); r = R0 + (R1 - R0) * (z - 0.12) / H + 0.02
    a = random.uniform(math.radians(200), math.radians(340))
    s = random.uniform(0.014, 0.034)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=s, location=(r * math.cos(a), r * math.sin(a), z)); o = bpy.context.object
    o.rotation_euler = (0, 0, a); o.scale = (0.45, 1, 1.3); o.data.materials.append(drop); [setattr(p, 'use_smooth', True) for p in o.data.polygons]
b3d.stack_camera((0, 0, 1.25), 2.8, az=0.0, el=12.0)
b3d.render(f'{OUT}/glass.png'); print('ok')
