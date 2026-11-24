"""VOTE 002 sprite: a glass bowl of ice cubes, a salt shaker tilted above it with salt grains falling, and a thermometer
standing in the ice (its red column at a neutral middle height, so it does not give the answer away)."""
import math, os, random, sys
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
import b3d
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
random.seed(4)


def glowm(name, c, s, alpha=1.0):
    m = b3d.mat(name, c, rough=0.4, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; q.inputs['Alpha'].default_value = alpha
    return m


def clear(name, c, a, rough=0.05):
    m = b3d.mat(name, c, rough=rough, coat=0.3); m.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = a; return m


b3d.reset((800, 800), 64); b3d.lights(3)
bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=0.7, location=(0, 0, 0.35), vertices=64); bowl = bpy.context.object
bowl.data.materials.append(clear('bowl', (0.75, 0.85, 0.95), 0.25)); sm = bowl.modifiers.new('s', 'SOLIDIFY'); sm.thickness = 0.05
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='DESELECT'); bpy.ops.object.mode_set(mode='OBJECT')
for f in bowl.data.polygons:
    if f.normal.z > 0.9: f.select = True
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.delete(type='FACE'); bpy.ops.object.mode_set(mode='OBJECT')
ice = clear('ice', (0.8, 0.92, 1.0), 0.55, 0.15)
for i in range(14):
    a = random.uniform(0, 2 * math.pi); r = random.uniform(0, 0.65); z = 0.2 + random.uniform(0, 0.45)
    bpy.ops.mesh.primitive_cube_add(size=0.34, location=(r * math.cos(a), r * math.sin(a), z), rotation=(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))
    o = bpy.context.object; o.data.materials.append(ice); b3d.bevel(o, 0.05, 3)
shaker = b3d.mat('shaker', (0.95, 0.95, 0.97), rough=0.3, coat=0.4); cap = b3d.mat('cap', (0.7, 0.72, 0.76), rough=0.2, metal=1.0, coat=0)
bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.6, location=(0.35, 0, 1.75), rotation=(0, math.radians(140), 0)); bpy.context.object.data.materials.append(shaker); b3d.bevel(bpy.context.object, 0.05, 3)
bpy.ops.mesh.primitive_cylinder_add(radius=0.23, depth=0.12, location=(0.12, 0, 1.53), rotation=(0, math.radians(140), 0)); bpy.context.object.data.materials.append(cap)
salt = glowm('salt', (1, 1, 1), 0.8)
for i in range(40):
    x = 0.0 + random.uniform(-0.18, 0.18) - 0.05; z = 0.7 + random.uniform(0, 0.75)
    bpy.ops.mesh.primitive_cube_add(size=0.035, location=(x, random.uniform(-0.15, 0.15), z)); bpy.context.object.data.materials.append(salt)
bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=1.6, location=(-0.6, -0.1, 0.95)); bpy.context.object.data.materials.append(clear('tglass', (0.9, 0.95, 1.0), 0.35))
bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.8, location=(-0.6, -0.1, 0.6)); bpy.context.object.data.materials.append(glowm('red', (0.95, 0.15, 0.1), 0.8))
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(-0.6, -0.1, 0.2)); bpy.context.object.data.materials.append(glowm('red2', (0.95, 0.15, 0.1), 0.8))
for j in range(7): 
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.6 + 0.08, -0.17, 0.45 + j * 0.15)); o = bpy.context.object; o.scale = (0.06, 0.01, 0.012); o.data.materials.append(b3d.mat('tk', (0.2, 0.2, 0.25), coat=0))
b3d.stack_camera((0, 0, 0.95), 2.6, az=-10.0, el=18.0)
b3d.render(f'{OUT}/ice.png'); print('ok')
