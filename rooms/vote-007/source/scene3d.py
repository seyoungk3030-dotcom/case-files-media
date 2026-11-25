"""VOTE 007 sprite: two identical glasses of cola side by side; the left holds one big ice cube, the right the same
amount of crushed ice; labels A and B are not drawn (the options name them)."""
import math, os, random, sys
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
import b3d
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
random.seed(3)


def clear(name, c, a, rough=0.05):
    m = b3d.mat(name, c, rough=rough, coat=0.5); m.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = a; return m


b3d.reset((1000, 800), 40); b3d.lights(3)
glass = clear('glass', (0.85, 0.93, 1.0), 0.18); cola = clear('cola', (0.12, 0.04, 0.015), 0.92, 0.1); ice = clear('ice', (0.9, 0.96, 1.0), 0.7, 0.15)
for x in (-1.0, 1.0):
    bpy.ops.mesh.primitive_cone_add(radius1=0.6, radius2=0.7, depth=1.9, location=(x, 0, 0.95), vertices=64); bpy.context.object.data.materials.append(glass)
    bpy.ops.mesh.primitive_cone_add(radius1=0.56, radius2=0.64, depth=1.4, location=(x, 0, 0.75), vertices=64); bpy.context.object.data.materials.append(cola)
bpy.ops.mesh.primitive_cube_add(size=0.82, location=(-1.0, 0, 1.25), rotation=(0.2, 0.1, 0.4)); o = bpy.context.object; o.data.materials.append(ice); b3d.bevel(o, 0.08, 3)
for i in range(70):
    a = random.uniform(0, 6.28); r = random.uniform(0, 0.5); z = random.uniform(1.0, 1.55)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=random.uniform(0.06, 0.11), location=(1.0 + r * math.cos(a), r * math.sin(a), z))
    bpy.context.object.data.materials.append(ice)
b3d.stack_camera((0, 0, 0.95), 3.6, az=0.0, el=18.0)
b3d.render(f'{OUT}/ice2.png'); print('ok')
