"""ROOM 162 3D sprites: a pile of logs seen from the cut ends, lying between two stakes on grass-dark ground. The log to
be pulled has a red ring painted on its end and a rope tied round it. p*: the pile. a*: the pulled log is gone (dashed
coral ring where it was), logs that roll off stay in place but turn grey-pink, the logs that stay keep
their colour."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
R = 0.3; EL = 12.0


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def pos(r, i, n0):
    return ((i + r / 2 - (n0 - 1) / 2) * 2 * R, R + r * R * math.sqrt(3))


def log(x, z, bark, cut, ringm=None, ghost=False):
    bpy.ops.mesh.primitive_cylinder_add(radius=R * 0.97, depth=1.6, location=(x, 0.8, z), rotation=(math.pi / 2, 0, 0), vertices=40)
    bpy.context.object.data.materials.append(bark)
    bpy.ops.mesh.primitive_cylinder_add(radius=R * 0.86, depth=0.02, location=(x, -0.005, z), rotation=(math.pi / 2, 0, 0), vertices=40)
    bpy.context.object.data.materials.append(cut)
    for rr in (0.55, 0.3):
        bpy.ops.mesh.primitive_torus_add(location=(x, -0.02, z), rotation=(math.pi / 2, 0, 0), major_radius=R * rr, minor_radius=0.008, major_segments=40)
        bpy.context.object.data.materials.append(bark)
    if ringm:
        bpy.ops.mesh.primitive_torus_add(location=(x, -0.03, z), rotation=(math.pi / 2, 0, 0), major_radius=R * 0.72, minor_radius=0.03, major_segments=48)
        bpy.context.object.data.materials.append(ringm)


def scene(k, after):
    b = BOARDS[k]; fallen = set(RES[k][0]); n0 = len(b['rows'][0])
    bark = b3d.mat('bark', (0.28, 0.16, 0.08), rough=0.9, coat=0); cut = b3d.mat('cut', (0.72, 0.48, 0.25), rough=0.7, coat=0)
    fcut = b3d.mat('fcut', (0.55, 0.45, 0.5), rough=0.8, coat=0); fbark = b3d.mat('fbark', (0.3, 0.26, 0.3), rough=0.9, coat=0)
    red = b3d.mat('red', (0.95, 0.15, 0.12), rough=0.4, coat=0); glow(red, (0.95, 0.15, 0.1), 0.3)
    coral = b3d.mat('coral', (0.95, 0.45, 0.35), rough=0.4, coat=0); glow(coral, (0.95, 0.4, 0.3), 0.4)
    ground = b3d.mat('ground', (0.13, 0.17, 0.12), rough=0.95, coat=0); stake = b3d.mat('stake', (0.45, 0.3, 0.18), rough=0.8, coat=0)
    W = n0 * 2 * R + 0.5
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.8, -0.05)); o = bpy.context.object; o.scale = (W + 0.2, 2.2, 0.1); o.data.materials.append(ground)
    for sx in (-1, 1):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=1.2, location=(sx * (n0 * R + 0.08), -0.05, 0.6), vertices=16); bpy.context.object.data.materials.append(stake)
    nf = 0
    for r, row in enumerate(b['rows']):
        for i in row:
            x, z = pos(r, i, n0)
            if (r, i) == b['pull']:
                if after:
                    bpy.ops.mesh.primitive_torus_add(location=(x, -0.02, z), rotation=(math.pi / 2, 0, 0), major_radius=R * 0.9, minor_radius=0.025, major_segments=48)
                    bpy.context.object.data.materials.append(coral)
                else:
                    log(x, z, bark, red, red)
            elif after and (r, i) in fallen:
                log(x, z, fbark, fcut)
            else:
                log(x, z, bark, cut)
    b3d.stack_camera((0, 0, 1.2), W + 0.5, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 700), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
