"""VOTE 005 sprite: a table edge with a long paper strip hanging over it, a full glass of juice standing on the strip,
and a coral speed arrow showing the strip being yanked out sideways."""
import math, os, sys
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
import b3d
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.4, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def clear(name, c, a, rough=0.05):
    m = b3d.mat(name, c, rough=rough, coat=0.5); m.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = a; return m


def box(m, loc, sc, bev=0.02, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


b3d.reset((900, 700), 64); b3d.lights(3)
box(b3d.mat('table', (0.55, 0.36, 0.2), rough=0.5, coat=0.4), (-0.6, 0, -0.1), (3.2, 1.8, 0.2), 0.03)
paper = b3d.mat('paper', (0.95, 0.95, 0.92), rough=0.7, coat=0)
box(paper, (0.1, 0, 0.006), (2.4, 0.5, 0.012), 0)
box(paper, (1.31, 0, -0.25), (0.012, 0.5, 0.5), 0)
bpy.ops.mesh.primitive_cone_add(radius1=0.3, radius2=0.36, depth=0.95, location=(-0.4, 0, 0.49), vertices=64); bpy.context.object.data.materials.append(clear('glass', (0.85, 0.93, 1.0), 0.2))
bpy.ops.mesh.primitive_cone_add(radius1=0.27, radius2=0.32, depth=0.72, location=(-0.4, 0, 0.39), vertices=64); bpy.context.object.data.materials.append(clear('juice', (1.0, 0.6, 0.1), 0.85, 0.1))
arrow = glowm('arrow', (0.95, 0.25, 0.2), 0.5)
box(arrow, (1.75, -0.0, -0.25), (0.7, 0.08, 0.08), 0)
bpy.ops.mesh.primitive_cone_add(radius1=0.16, radius2=0, depth=0.3, location=(2.2, 0, -0.25), rotation=(0, math.pi / 2, 0)); bpy.context.object.data.materials.append(arrow)
for k, z in enumerate((-0.05, -0.45)):
    box(arrow, (1.7, 0, z), (0.4 - 0.1 * k, 0.05, 0.04), 0)
b3d.stack_camera((0.2, 0, 0.2), 3.8, az=-20.0, el=18.0)
b3d.render(f'{OUT}/paper.png'); print('ok')
