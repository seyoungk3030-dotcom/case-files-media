"""ROOM 081 3D sprites: a 3x3 puzzle cube (dark body, pastel stickers, a digit on every sticker) seen from the
front-right-top, a coral frame around the star cell on the front face and an amber arrow showing the one turn.
a*: the cube after the turn, the sticker now in the star cell glowing amber."""
import math, os, sys, time
import bpy
import numpy as np
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, stickers, turn, at_star
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
FC = {'F': (0.98, 0.55, 0.45), 'R': (0.45, 0.72, 0.98), 'U': (0.98, 0.9, 0.45), 'B': (0.6, 0.9, 0.6), 'L': (0.8, 0.6, 0.95), 'D': (0.95, 0.95, 0.95)}


def box(loc, scale, m, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def orient(o, n, up):
    n, up = Vector(tuple(map(float, n))), Vector(tuple(map(float, up))); x = up.cross(n)
    o.matrix_world = Matrix.Translation(o.location) @ Matrix((x, up, n)).transposed().to_4x4()


def sticker(s, M, ink, hot=False):
    p = s['pos'] + 0.02 * s['n']
    bpy.ops.mesh.primitive_cube_add(size=1, location=tuple(map(float, p))); o = bpy.context.object; o.scale = (0.86, 0.86, 0.03)
    orient(o, s['n'], s['up']); o.scale = (0.86, 0.86, 0.03); o.data.materials.append(M['hot'] if hot else M[s['face']]); b3d.bevel(o, 0.06, 3)
    bpy.ops.object.text_add(location=tuple(map(float, s['pos'] + 0.05 * s['n']))); t = bpy.context.object; t.data.body = str(s['d'])
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = 0.62; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(ink)
    orient(t, s['n'], s['up'])


def arrow(pts, m, r=0.07):
    for a, b in zip(pts, pts[1:]):
        a, b = np.array(a, float), np.array(b, float); d = b - a; L = np.linalg.norm(d)
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=tuple((a + b) / 2)); o = bpy.context.object
        o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(tuple(d / L))); o.data.materials.append(m)
    a, b = np.array(pts[-2], float), np.array(pts[-1], float); d = (b - a) / np.linalg.norm(b - a)
    bpy.ops.mesh.primitive_cone_add(radius1=0.2, depth=0.4, location=tuple(b + d * 0.2)); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(tuple(d))); o.data.materials.append(m)


def scene(k, after):
    move, star, seed = BOARDS[k]
    M = {f: b3d.mat('f' + f, c, rough=0.35, coat=0.5) for f, c in FC.items()}
    for m in M.values():
        q0 = m.node_tree.nodes['Principled BSDF']; q0.inputs['Emission Color'].default_value = q0.inputs['Base Color'].default_value; q0.inputs['Emission Strength'].default_value = 0.35
    M['hot'] = b3d.mat('hot', (0.98, 0.66, 0.1), rough=0.3); q = M['hot'].node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (0.98, 0.66, 0.1, 1); q.inputs['Emission Strength'].default_value = 0.6
    ink = b3d.mat('ink', (0.06, 0.09, 0.18), rough=0.4); body = b3d.mat('body', (0.1, 0.11, 0.14), rough=0.4)
    amb = b3d.mat('amb', (0.98, 0.55, 0.15), rough=0.3); coral = b3d.mat('coral', (0.98, 0.3, 0.35), rough=0.3)
    q = coral.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (0.98, 0.3, 0.35, 1); q.inputs['Emission Strength'].default_value = 0.8
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            for z in (-1, 0, 1): box((x, y, z), (0.98, 0.98, 0.98), body, 0.08)
    st = stickers(seed)
    if after: st = turn(st, move)
    tgt = at_star(st, star) if after else None
    for s in st:
        if s['n'][1] > 0.5 or s['n'][0] < -0.5 or s['n'][2] < -0.5: continue      # hidden faces
        sticker(s, M, ink, hot=after and s is tgt)
    sx, sz = star
    for (dx, dz, w, h) in ((0, 0.5, 1.02, 0.07), (0, -0.5, 1.02, 0.07), (0.5, 0, 0.07, 1.02), (-0.5, 0, 0.07, 1.02)):
        box((sx + dx, -1.6, sz + dz), (w, 0.06, h), coral, 0.02)
    if not after:
        y = -1.75
        if move == 'U': arrow([(1.4, -1.0, 1.85), (-1.4, -1.0, 1.85)], amb)
        elif move == "R'": arrow([(1.95, -1.4, 1.4), (1.95, -1.4, -1.4)], amb)
        else:
            sgn = 1 if move == 'F' else -1; pts = []
            for i in range(10):
                a = math.radians(135 - sgn * i * 9); pts.append((2.0 * math.cos(a), y, 2.0 * math.sin(a)))
            arrow(pts, amb, 0.06)
    b3d.stack_camera((0, 0, 0), 6.6, az=32.0, el=24.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((800, 800), 40); b3d.lights(6)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
