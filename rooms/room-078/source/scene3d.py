"""ROOM 078 3D sprites: a glassy cube (faint faces, solid edges) with three coral dots on it. a*: the cross-section
polygon through the dots, filled amber, its corners marked."""
import math, os, sys, time
import bpy, bmesh
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import POINTS, V, EDGES, section
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
COLS = {'A': (0.35, 0.6, 0.95), 'B': (0.3, 0.78, 0.6), 'C': (0.7, 0.5, 0.95), 'D': (0.95, 0.5, 0.6)}


def rod(a, b, r, m):
    a, b = np.array(a, float), np.array(b, float); d = b - a; L = np.linalg.norm(d)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=tuple((a + b) / 2)); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; from mathutils import Vector; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(tuple(d / L)))
    o.data.materials.append(m)


def ball(p, r, m):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=tuple(map(float, p)), segments=32, ring_count=16)
    bpy.context.object.data.materials.append(m); bpy.ops.object.shade_smooth()


def glassy(name, col, a):
    m = b3d.mat(name, col, rough=0.15, coat=0.6); p = m.node_tree.nodes['Principled BSDF']; p.inputs['Alpha'].default_value = a
    try: m.surface_render_method = 'BLENDED'
    except Exception: m.blend_method = 'BLEND'
    return m


def poly(pts, m):
    me = bpy.data.meshes.new('sec'); bm = bmesh.new(); vs = [bm.verts.new(tuple(map(float, q))) for q in pts]; bm.faces.new(vs)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); o = bpy.data.objects.new('sec', me)
    bpy.context.collection.objects.link(o); o.data.materials.append(m)
    o.modifiers.new('s', 'SOLIDIFY').thickness = 0.03


def scene(k, after):
    edge = b3d.mat('edge', COLS[k], rough=0.3, coat=0.6); face = glassy('face', COLS[k], 0.12)
    dot = b3d.mat('dot', (0.98, 0.35, 0.3), rough=0.3, coat=0.7)
    for m, e in ((edge, 0.35), (dot, 0.6)):
        q0 = m.node_tree.nodes['Principled BSDF']; q0.inputs['Emission Color'].default_value = q0.inputs['Base Color'].default_value; q0.inputs['Emission Strength'].default_value = e
    amb = glassy('amb', (0.98, 0.68, 0.12), 0.85); q = amb.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (0.98, 0.68, 0.12, 1); q.inputs['Emission Strength'].default_value = 0.5
    bpy.ops.mesh.primitive_cube_add(size=2, location=(1, 1, 1)); bpy.context.object.data.materials.append(face)
    for a, b in EDGES: rod(V[a], V[b], 0.035, edge)
    for v in V: ball(v, 0.05, edge)
    if after:
        n, pts = section(POINTS[k]); poly(pts, amb)
        for p in pts: ball(p, 0.09, b3d.mat('cn', (0.98, 0.68, 0.12), rough=0.3))
    for p in POINTS[k]: ball(p, 0.13, dot)
    az, el = (165.0, 18.0) if k == 'D' else (105.0, 28.0)
    b3d.stack_camera((1, 1, 1), 4.0, az=az, el=el)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((800, 800), 48); b3d.lights(5)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
