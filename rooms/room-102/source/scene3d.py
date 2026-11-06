"""ROOM 102 3D sprites: four identical glass bottles in a row with different water levels, a number in front of each.
A blow board has a big mint '후~' on the left; a tap board has a steel spoon. a*: the highest-pitched bottle's water
glows mint and the others turn grey."""
import math, os, sys, time
import bpy, bmesh
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, H
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
XS = [-1.875, -0.625, 0.625, 1.875]


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m, rot=(0, 0, 0)):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.04; t.data.materials.append(m)


def bottle(x, m):
    prof = [(0.001, 0.0), (0.42, 0.0), (0.46, 0.05), (0.46, H), (0.42, H + 0.14), (0.2, H + 0.42), (0.16, H + 0.5),
            (0.16, H + 0.82), (0.19, H + 0.86), (0.16, H + 0.9)]
    me = bpy.data.meshes.new('b'); bm = bmesh.new(); vs = [bm.verts.new((r, 0, z)) for r, z in prof]
    for a, b in zip(vs, vs[1:]): bm.edges.new((a, b))
    bmesh.ops.spin(bm, geom=bm.verts[:] + bm.edges[:], cent=(0, 0, 0), axis=(0, 0, 1), angle=2 * math.pi, steps=64)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-5); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('b', me); bpy.context.collection.objects.link(o); o.location = (x, 0, 0)
    o.modifiers.new('s', 'SOLIDIFY').thickness = 0.03
    for p in me.polygons: p.use_smooth = True
    o.data.materials.append(m)


def spoon(m, mint):
    from mathutils import Vector
    a, b = Vector((-0.2, 0, 3.55)), Vector((1.3, 0, 3.55)); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(radius=0.065, depth=d.length, location=(a + b) / 2, vertices=24); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized()); o.data.materials.append(m)
    c = b + d.normalized() * 0.3
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.34, location=c, segments=48, ring_count=24); o = bpy.context.object
    o.scale = (0.62, 0.62, 1.0); o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = True
    text('톡!', (-1.15, 0, 3.55), 0.8, mint, rot=(math.radians(90), 0, 0))


def scene(k, after):
    mode, levels = BOARDS[k]
    table = b3d.mat('table', (0.05, 0.06, 0.1), rough=0.7, coat=0)
    glass = b3d.mat('glass', (0.85, 0.95, 1.0), rough=0.04, coat=0.5)
    gq = glass.node_tree.nodes['Principled BSDF']; gq.inputs['Transmission Weight'].default_value = 1.0; gq.inputs['IOR'].default_value = 1.45
    water = b3d.mat('water', (0.12, 0.45, 0.95), rough=0.15, coat=0.3); grey = b3d.mat('grey', (0.3, 0.32, 0.38), rough=0.5)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.2)
    white = b3d.mat('white', (0.92, 0.93, 0.96), rough=0.5, coat=0); steel = b3d.mat('steel', (0.75, 0.78, 0.82), rough=0.2, metal=1.0)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.0, 0.3, -0.06)); o = bpy.context.object; o.scale = (5.6, 2.2, 0.12)
    o.data.materials.append(table); b3d.bevel(o, 0.04)
    for i, (x, l) in enumerate(zip(XS, levels)):
        bottle(x, glass)
        wm = (mint if i + 1 == RES[k] else grey) if after else water
        bpy.ops.mesh.primitive_cylinder_add(radius=0.425, depth=l * H, location=(x, 0, 0.03 + l * H / 2), vertices=64)
        o = bpy.context.object; o.data.materials.append(wm)
        for p in o.data.polygons: p.use_smooth = True
        text(str(i + 1), (x, -0.85, 0.02), 0.5, white, rot=(math.radians(90), 0, 0))
    if mode == 'blow': text('후~', (0, 0, 3.55), 0.85, mint, rot=(math.radians(90), 0, 0))
    else: spoon(steel, mint)
    b3d.stack_camera((0, 0, 1.75), 5.9, az=0.0, el=10.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 760), 40); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
