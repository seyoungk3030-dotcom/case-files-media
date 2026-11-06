"""ROOM 093 3D sprites: four optical illusions laid on a dark board, seen nearly from above. A Muller-Lyer rods with
fins, B Ebbinghaus orange discs ringed by grey discs, C Jastrow arc blocks, D Ponzo bars on converging rails. Parts are
numbered. a*: the context is taken away and the parts are lined up from the same start, so their true sizes show."""
import math, os, sys, time
import bpy
import numpy as np
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import A, B, C, D, ANS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.03; t.data.materials.append(m)


def rod(a, b, r, m):
    a, b = np.array(a, float), np.array(b, float); d = b - a; L = np.linalg.norm(d)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=tuple((a + b) / 2), vertices=24); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(tuple(d / L))); o.data.materials.append(m)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=tuple(a)); bpy.context.object.data.materials.append(m)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=tuple(b)); bpy.context.object.data.materials.append(m)


def disc(x, y, r, m, h=0.12):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=(x, y, h / 2), vertices=64); o = bpy.context.object; o.data.materials.append(m); b3d.bevel(o, 0.02)


def arc(cx, cy, r0, r1, a0, a1, m, h=0.14):
    bm_v = []; n = 40
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n); bm_v.append((math.cos(a), math.sin(a)))
    verts = []
    for z in (0, h):
        for c, s in bm_v: verts.append((cx + r1 * c, cy + r1 * s, z))
        for c, s in bm_v: verts.append((cx + r0 * c, cy + r0 * s, z))
    N = n + 1; faces = []
    def V(z, ring, i): return z * 2 * N + ring * N + i
    for i in range(n):
        faces.append((V(1, 0, i), V(1, 0, i + 1), V(1, 1, i + 1), V(1, 1, i)))
        faces.append((V(0, 0, i), V(0, 1, i), V(0, 1, i + 1), V(0, 0, i + 1)))
        faces.append((V(0, 0, i), V(0, 0, i + 1), V(1, 0, i + 1), V(1, 0, i)))
        faces.append((V(0, 1, i), V(1, 1, i), V(1, 1, i + 1), V(0, 1, i + 1)))
    faces.append((V(0, 0, 0), V(1, 0, 0), V(1, 1, 0), V(0, 1, 0))); faces.append((V(0, 0, n), V(0, 1, n), V(1, 1, n), V(1, 0, n)))
    me = bpy.data.meshes.new('arc'); me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new('arc', me); bpy.context.collection.objects.link(o); o.data.materials.append(m)
    bpy.context.view_layer.objects.active = o; o.select_set(True); bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False); bpy.ops.object.mode_set(mode='OBJECT'); o.select_set(False)


def scene(k, after):
    board = b3d.mat('board', (0.02, 0.025, 0.045), rough=0.8, coat=0)
    ink = b3d.mat('ink', (0.95, 0.96, 0.98), rough=0.5, coat=0); glow(ink, (0.95, 0.96, 0.98), 0.5)
    col = [b3d.mat(f'c{i}', c, rough=0.35) for i, c in enumerate([(0.98, 0.55, 0.15), (0.25, 0.6, 1.0), (0.98, 0.35, 0.4)])]
    grey = b3d.mat('grey', (0.55, 0.58, 0.66), rough=0.5); rail = b3d.mat('rail', (0.55, 0.58, 0.66), rough=0.4, metal=0.5)
    mint = b3d.mat('mint', (0.2, 0.9, 0.62), rough=0.4); glow(mint, (0.2, 0.9, 0.62), 0.7)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.1)); o = bpy.context.object; o.scale = (8.6, 6.4, 0.2); o.data.materials.append(board); b3d.bevel(o, 0.08)
    if k == 'A':
        ys = {1: 1.9, 2: 0.0, 3: -1.9}
        for n, (L, f) in A.items():
            y = ys[n]; x0, x1 = (-L / 2, L / 2) if not after else (-2.6, -2.6 + L)
            rod((x0, y, 0.12), (x1, y, 0.12), 0.09, col[n - 1])
            if not after:
                for xe, sg in ((x0, -1), (x1, 1)):
                    dx = 0.55 * (-sg if f == 'out' else sg)
                    for dy in (0.5, -0.5): rod((xe, y, 0.12), (xe + dx, y + dy, 0.12), 0.07, col[n - 1])
            else:
                rod((-2.6, y - 0.45, 0.12), (-2.6, y + 0.45, 0.12), 0.03, mint)
            text(str(n), (-3.1, y, 0.15), 0.7, ink)
        if after: rod((-2.6 + A[1][0], 2.6, 0.12), (-2.6 + A[1][0], -2.6, 0.12), 0.035, mint)
    if k == 'B':
        P = {1: (-2.7, 1.0), 2: (-0.4, -1.3), 3: (2.2, 0.6)} if not after else {1: (-2.2, 0), 2: (0, 0), 3: (2.2, 0)}
        for n, (r, rr) in B.items():
            x, y = P[n]; disc(x, y, r, col[0])
            if not after:
                dist = r + rr + 0.18; cnt = 8 if rr < 0.4 else 6
                for i in range(cnt):
                    a = 2 * math.pi * i / cnt; disc(x + dist * math.cos(a), y + dist * math.sin(a), rr, grey)
            text(str(n), (x, y, 0.2), 0.45, b3d.mat('dk', (0.06, 0.07, 0.1), rough=0.5))
            if after: rod((x - r, y - 0.8, 0.14), (x + r, y - 0.8, 0.14), 0.04, mint)
    if k == 'C':
        for n, cy in ((1, -3.4), (2, -2.15), (3, -0.9)):
            arc(0, cy, 2.4, 3.6, 55, 125, col[n - 1]); text(str(n), (0, cy + 3.0, 0.2), 0.5, ink)
        if after:
            for sg in (-1, 1):
                for r in (2.4, 3.6): rod((sg * r * math.cos(math.radians(55)), 2.9, 0.2), (sg * r * math.cos(math.radians(55)), -2.0, 0.2), 0.03, mint)
    if k == 'D':
        if not after:
            for sg in (-1, 1): rod((sg * 3.4, -2.8, 0.06), (sg * 0.35, 2.8, 0.06), 0.08, rail)
            for i in range(9):
                t = i / 8; y = -2.8 + 5.6 * t; w = 3.4 * (1 - t) + 0.35 * t
                rod((-w - 0.3, y, 0.03), (w + 0.3, y, 0.03), 0.04, grey)
        for n, (L, h) in D.items():
            y = -2.8 + 5.6 * h
            x0 = -L / 2 if not after else -2.0
            rod((x0, y, 0.2), (x0 + L, y, 0.2), 0.12, col[n - 1])
            text(str(n), (-3.1 if after else -3.3, y, 0.2), 0.6, ink)
        if after:
            rod((-2.0, 3.0, 0.15), (-2.0, -3.0, 0.15), 0.03, mint); rod((-2.0 + D[3][0], 3.0, 0.15), (-2.0 + D[3][0], -3.0, 0.15), 0.03, mint)
    b3d.stack_camera((0, 0.0, 0), 8.9, az=0.0, el=72.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 700), 40); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
