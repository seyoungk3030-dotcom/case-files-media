"""ROOM 082 3D sprites: a wooden 5x5 pegboard seen from the front-top, a coloured rubber band stretched round some
pegs. a*: the area inside the band filled with glowing amber and faint unit grid lines."""
import math, os, sys, time
import bpy, bmesh
import numpy as np
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BANDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
COLS = {'A': (0.95, 0.35, 0.45), 'B': (0.3, 0.55, 0.98), 'C': (0.25, 0.75, 0.5), 'D': (0.7, 0.4, 0.95)}
S = 1.0; Z = 0.32


def box(loc, scale, m, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def P(x, y, z=Z): return Vector(((x - 2) * S, (y - 2) * S, z))


def band(pts, m):
    c = Vector((sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts), 0))
    cv = bpy.data.curves.new('band', 'CURVE'); cv.dimensions = '3D'; cv.bevel_depth = 0.075; cv.bevel_resolution = 4
    sp = cv.splines.new('POLY'); sp.points.add(len(pts) - 1); sp.use_cyclic_u = True
    for i, (x, y) in enumerate(pts):
        v = P(x, y); d = Vector((x, y, 0)) - c; d.normalize(); v += d * 0.09
        sp.points[i].co = (v.x, v.y, v.z, 1)
    o = bpy.data.objects.new('band', cv); bpy.context.collection.objects.link(o); o.data.materials.append(m)


def fill(pts, m):
    me = bpy.data.meshes.new('f'); bm = bmesh.new(); vs = [bm.verts.new(P(x, y, 0.13)) for x, y in pts]; bm.faces.new(vs)
    bm.to_mesh(me); o = bpy.data.objects.new('f', me); bpy.context.collection.objects.link(o); o.data.materials.append(m)


def scene(k, after):
    wood = b3d.mat('wood', (0.5, 0.33, 0.2), rough=0.6, coat=0.2); peg = b3d.mat('peg', (0.85, 0.87, 0.9), rough=0.25, metal=0.7)
    rub = b3d.mat('rub', COLS[k], rough=0.4, coat=0.4); q = rub.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*COLS[k], 1); q.inputs['Emission Strength'].default_value = 0.5; line = b3d.mat('line', (0.36, 0.23, 0.14), rough=0.7, coat=0)
    box((0, 0, 0), (5.0, 5.0, 0.24), wood, 0.12)
    for i in range(5):
        box(((i - 2) * S, 0, 0.122), (0.025, 4.2, 0.004), line, 0.002); box((0, (i - 2) * S, 0.122), (4.2, 0.025, 0.004), line, 0.002)
    for x in range(5):
        for y in range(5):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.5, location=(*P(x, y, 0.3)[:2], 0.3)); bpy.context.object.data.materials.append(peg)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, location=(*P(x, y)[:2], 0.56)); bpy.context.object.data.materials.append(peg); bpy.ops.object.shade_smooth()
    band(BANDS[k], rub)
    if after:
        amb = b3d.mat('amb', (0.98, 0.66, 0.12), rough=0.4); q = amb.node_tree.nodes['Principled BSDF']
        q.inputs['Emission Color'].default_value = (0.98, 0.66, 0.12, 1); q.inputs['Emission Strength'].default_value = 0.25
        fill(BANDS[k], amb)
    b3d.stack_camera((0, 0.1, 0.2), 5.5, az=0.0, el=58.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((800, 760), 40); b3d.lights(4)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
