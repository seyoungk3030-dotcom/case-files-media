"""ROOM 087 3D sprites: a row of paper cups on a wooden shelf, upright (open mouth on top, dark inside visible) or
upside down (mouth on the shelf)."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
COL = {'A': (0.95, 0.4, 0.45), 'B': (0.3, 0.6, 0.95), 'C': (0.3, 0.75, 0.5), 'D': (0.75, 0.5, 0.95)}


def cup(x, up, m, inner):
    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=0.28 if up else 0.4, radius2=0.4 if up else 0.28, depth=0.9, location=(x, 0, 0.45))
    o = bpy.context.object; o.data.materials.append(m); bpy.ops.object.shade_smooth()
    if up:
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.36, depth=0.02, location=(x, 0, 0.9)); bpy.context.object.data.materials.append(inner)
        bpy.ops.mesh.primitive_torus_add(location=(x, 0, 0.9), major_radius=0.4, minor_radius=0.03); bpy.context.object.data.materials.append(m)
    else:
        bpy.ops.mesh.primitive_torus_add(location=(x, 0, 0.03), major_radius=0.4, minor_radius=0.03); bpy.context.object.data.materials.append(m)


def scene(k):
    cups, kk = BOARDS[k]; n = len(cups)
    m = b3d.mat('cup', COL[k], rough=0.4, coat=0.4); inner = b3d.mat('in', tuple(c * 0.35 for c in COL[k]), rough=0.6, coat=0)
    wood = b3d.mat('wood', (0.6, 0.42, 0.28), rough=0.5, coat=0.2)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.06)); o = bpy.context.object; o.scale = (7.4, 1.3, 0.12); o.data.materials.append(wood)
    for i, c in enumerate(cups): cup((i - (n - 1) / 2) * 1.05, c == 'U', m, inner)
    b3d.stack_camera((0, 0, 0.4), 7.6, az=0.0, el=24.0)


for k in 'ABCD':
    b3d.reset((1200, 340), 40); b3d.lights(6)
    t = time.time(); scene(k); b3d.render(f'{OUT}/p{k}.png'); print('p' + k, round(time.time() - t, 1), flush=True)
