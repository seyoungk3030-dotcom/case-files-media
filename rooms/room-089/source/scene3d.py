"""ROOM 089 3D sprites: a wooden tower-of-hanoi board with three pegs and colored discs, seen slightly from above.
The right peg stands on a mint goal pad with a flag. a*: the same position with the goal pad and flag lit."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
RAD = [0.55, 0.82, 1.09, 1.36]; TH = 0.36; PX = [-3.4, 0.0, 3.4]
COLS = [(0.98, 0.42, 0.38), (0.99, 0.72, 0.18), (0.62, 0.45, 0.98), (0.30, 0.55, 0.98)]


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def scene(k, after):
    s = BOARDS[k]; n = len(s)
    wood = b3d.mat('wood', (0.42, 0.26, 0.15), rough=0.55, coat=0.2); peg = b3d.mat('peg', (0.62, 0.42, 0.26), rough=0.5)
    pad = b3d.mat('pad', (0.25, 0.85, 0.66), rough=0.4); glow(pad, (0.25, 0.85, 0.66), 1.2 if after else 0.35)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.2)); o = bpy.context.object; o.scale = (10.6, 3.2, 0.4)
    o.data.materials.append(wood); b3d.bevel(o, 0.08)
    bpy.ops.mesh.primitive_cylinder_add(radius=1.5, depth=0.06, location=(PX[2], 0, 0.02), vertices=64); bpy.context.object.data.materials.append(pad)
    for x in PX:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=2.2, location=(x, 0, 1.1), vertices=24); bpy.context.object.data.materials.append(peg)
    for p in range(3):
        z = 0.05
        for d in sorted((i for i in range(n) if s[i] == p), reverse=True):
            m = b3d.mat(f'd{d}', COLS[d], rough=0.3, coat=0.5)
            bpy.ops.mesh.primitive_cylinder_add(radius=RAD[d], depth=TH, location=(PX[p], 0, z + TH / 2), vertices=64)
            o = bpy.context.object; o.data.materials.append(m); b3d.bevel(o, 0.06); z += TH
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.01, location=(0, 0, -5))
    fl = b3d.mat('flag', (0.25, 0.85, 0.66), rough=0.4); glow(fl, (0.25, 0.85, 0.66), 1.0 if after else 0.3)
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.42, depth=0.06, location=(PX[2] + 0.38, 0, 2.05), rotation=(math.radians(90), 0, math.radians(90)))
    o = bpy.context.object; o.rotation_euler = (math.radians(90), math.radians(-90), 0); o.data.materials.append(fl)
    b3d.stack_camera((0, 0, 0.75), 11.2, az=0.0, el=16.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1300, 420), 40); b3d.lights(6)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
