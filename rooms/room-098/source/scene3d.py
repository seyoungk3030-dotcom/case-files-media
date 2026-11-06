"""ROOM 098 3D sprites: a wooden board with copper wires on a grid, a battery on the left (+ at the top), bulbs on
small sockets (glass globes), and knife switches (closed = lever down, open = lever raised). a*: lit bulbs glow
warm yellow, dark bulbs stay grey."""
import math, os, sys, time
import bpy
import numpy as np
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
S = 1.45


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def rod(a, b, r, m):
    a, b = np.array(a, float), np.array(b, float); d = b - a; L = np.linalg.norm(d)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=tuple((a + b) / 2), vertices=16); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(tuple(d / L))); o.data.materials.append(m)


def P(n): return np.array([(n[0] - 2) * S, (n[1] - 1) * S, 0.0])


def scene(k, after):
    wood = b3d.mat('wood', (0.05, 0.07, 0.12), rough=0.6, coat=0.1); cu = b3d.mat('cu', (0.95, 0.55, 0.3), rough=0.3, metal=0.6); glow(cu, (0.95, 0.5, 0.25), 0.35)
    sock = b3d.mat('sock', (0.12, 0.13, 0.16), rough=0.4, metal=0.3); glass = b3d.mat('glass', (0.22, 0.25, 0.32), rough=0.15, coat=0.8)
    on = b3d.mat('on', (1.0, 0.75, 0.2), rough=0.2); glow(on, (1.0, 0.65, 0.1), 2.2)
    steel = b3d.mat('steel', (0.85, 0.87, 0.9), rough=0.2, metal=1.0); red = b3d.mat('red', (0.85, 0.12, 0.1), rough=0.4)
    blk = b3d.mat('blk', (0.06, 0.06, 0.07), rough=0.4); ink = b3d.mat('ink', (0.95, 0.96, 0.98), rough=0.5); glow(ink, (0.95, 0.96, 0.98), 0.4)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.15)); o = bpy.context.object; o.scale = (4 * S + 1.6, 2 * S + 1.4, 0.3); o.data.materials.append(wood); b3d.bevel(o, 0.08)
    a, b = P((0, 0)), P((0, 2))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.36, depth=1.5, location=tuple((a + b) / 2 + [0, 0, 0.36]), rotation=(math.radians(90), 0, 0)); bpy.context.object.data.materials.append(red)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.37, depth=0.5, location=tuple((a + b) / 2 + [0, -0.5, 0.36]), rotation=(math.radians(90), 0, 0)); bpy.context.object.data.materials.append(blk)
    rod(a, a + [0, 0.62, 0], 0.05, cu); rod(b, b - [0, 0.62, 0], 0.05, cu)
    text('+', tuple(b + [-0.55, -0.35, 0.05]), 0.5, ink); text('−', tuple(a + [-0.55, 0.35, 0.05]), 0.5, ink)
    lit = iter(RES[k]); nodes = set()
    for t, n1, n2 in BOARDS[k]:
        p, q = P(n1), P(n2); mid = (p + q) / 2; d = (q - p) / np.linalg.norm(q - p); nodes |= {n1, n2}
        if t == 'W': rod(p, q, 0.07, cu)
        elif t == 'B':
            on_ = next(lit); rod(p, mid - d * 0.3, 0.07, cu); rod(mid + d * 0.3, q, 0.07, cu)
            bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.22, location=tuple(mid + [0, 0, 0.11])); bpy.context.object.data.materials.append(sock)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=tuple(mid + [0, 0, 0.36])); bpy.context.object.data.materials.append(on if after and on_ else glass)
        else:
            rod(p, mid - d * 0.35, 0.07, cu); rod(mid + d * 0.35, q, 0.07, cu)
            for e in (mid - d * 0.35, mid + d * 0.35):
                bpy.ops.mesh.primitive_cube_add(size=0.2, location=tuple(e + [0, 0, 0.1])); bpy.context.object.data.materials.append(sock)
            hinge = mid - d * 0.35 + [0, 0, 0.2]
            ang = 0 if t == 'S1' else math.radians(50); perp = np.array([-d[1], d[0], 0.0])
            tip = hinge + (d * math.cos(ang) + perp * math.sin(ang)) * 0.75 + np.array([0, 0, 0.0 if t == 'S1' else 0.25])
            rod(hinge, tip, 0.07, steel)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=tuple(tip + [0, 0, 0.05])); bpy.context.object.data.materials.append(red)
    for n in nodes:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.06, location=tuple(P(n) + [0, 0, 0.03])); bpy.context.object.data.materials.append(cu)
    b3d.stack_camera((0, 0.15, 0.2), 4 * S + 1.9, az=0.0, el=78.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 640), 40); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
