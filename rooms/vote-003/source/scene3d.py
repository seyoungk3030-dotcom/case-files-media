"""VOTE 003 sprite: open scissors seen from above-front, a thick cardboard strip, and two markers on the blade, an amber
'A' dot near the tip and a blue 'B' dot near the screw (the two places to cut)."""
import math, os, sys
import bpy, bmesh
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
import b3d
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.4, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def blade(m, ang, z):
    me = bpy.data.meshes.new('b'); bm = bmesh.new()
    pts = [(-0.3, -0.12), (3.0, -0.02), (3.0, 0.02), (0.0, 0.2), (-0.3, 0.12)]
    vs = [bm.verts.new((x, y, 0)) for x, y in pts]; f = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f]); bmesh.ops.translate(bm, verts=[v for v in ext['geom'] if isinstance(v, bmesh.types.BMVert)], vec=(0, 0, 0.05))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('b', me); bpy.context.collection.objects.link(o); o.location = (0, 0, z); o.rotation_euler = (0, 0, ang)
    o.data.materials.append(m); b3d.bevel(o, 0.01, 2); return o


def handle(m, ang, z):
    a = ang + math.pi; c = (1.45 * math.cos(a), 1.45 * math.sin(a), z)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.55, minor_radius=0.12, location=c, rotation=(0, 0, a)); o = bpy.context.object; o.scale = (1.3, 0.8, 1)
    o.data.materials.append(m)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.6, location=(0.45 * math.cos(a), 0.45 * math.sin(a), z), rotation=(0, math.pi / 2, a)); bpy.context.object.data.materials.append(m)


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts.load(FONT); t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


b3d.reset((900, 700), 64); b3d.lights(3)
steel = b3d.mat('steel', (0.78, 0.8, 0.84), rough=0.25, metal=0.3, coat=0.6); red = b3d.mat('red', (0.9, 0.2, 0.2), rough=0.4, coat=0.6)
op = math.radians(20)
blade(steel, op, 0.1); blade(steel, -op, 0.16); handle(red, op, 0.1); handle(red, -op, 0.16)
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.2, location=(0, 0, 0.15)); bpy.context.object.data.materials.append(b3d.mat('screw', (0.4, 0.4, 0.45), rough=0.2, metal=1, coat=0))
bpy.ops.mesh.primitive_cube_add(size=1, location=(1.75, 0, -0.06)); o = bpy.context.object; o.scale = (0.5, 2.6, 0.08)
o.data.materials.append(b3d.mat('card', (0.72, 0.55, 0.35), rough=0.8, coat=0)); b3d.bevel(o, 0.01, 2)
for x, nm, c in ((2.7, 'A', (1.0, 0.72, 0.2)), (0.7, 'B', (0.35, 0.65, 1.0))):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.14, location=(x, 0, 0.32)); bpy.context.object.data.materials.append(glowm(nm, c, 1.0))
    text(nm, (x, 0.75 if nm == 'A' else 0.55, 0.3), 0.45, glowm(nm + 't', c, 0.8))
b3d.stack_camera((0.7, 0, 0.2), 6.6, az=0.0, el=55.0)
b3d.render(f'{OUT}/scissors.png'); print('ok')
