"""3D toy-style props rendered with Blender (pip bpy) as transparent PNG sprites for kit/short.py.
Everything is lit the same way, so sprites from different renders sit together on one frame."""
import math, os
import bpy, bmesh

PAL = {'mint': (0.05, 0.62, 0.48), 'amber': (0.92, 0.36, 0.02), 'coral': (0.90, 0.16, 0.13),
       'pearl': (0.85, 0.85, 0.82), 'steel': (0.55, 0.60, 0.68), 'dark': (0.12, 0.16, 0.22)}


def reset(res=(1000, 400), samples=64):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = res; sc.render.resolution_percentage = 100
    sc.render.film_transparent = True
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'Medium High Contrast'
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (0.05, 0.08, 0.14, 1); bg.inputs[1].default_value = 0.6
    return sc


def mat(name, col, rough=0.28, metal=0.0, coat=0.6):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*col, 1); p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    if 'Coat Weight' in p.inputs: p.inputs['Coat Weight'].default_value = coat
    return m


def _put(obj, m, loc, rot=(0, 0, 0)):
    obj.location = loc; obj.rotation_euler = rot
    obj.data.materials.append(m)
    for poly in obj.data.polygons: poly.use_smooth = True
    return obj


def bevel(obj, w=0.04, seg=4):
    b = obj.modifiers.new('bev', 'BEVEL'); b.width = w; b.segments = seg; b.limit_method = 'ANGLE'
    obj.modifiers.new('wn', 'WEIGHTED_NORMAL')
    return obj


def sphere(m, x, z0, r=0.42):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=64, ring_count=32)
    return _put(bpy.context.object, m, (x, 0, z0 + r))


def cube(m, x, z0, s=0.78):
    bpy.ops.mesh.primitive_cube_add(size=s)
    o = _put(bpy.context.object, m, (x, 0, z0 + s / 2), (0, 0, math.radians(18)))
    for p in o.data.polygons: p.use_smooth = False
    return bevel(o, 0.07)


def pyramid(m, x, z0, r=0.5, h=0.85):
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=r, radius2=0, depth=h)
    o = _put(bpy.context.object, m, (x, 0, z0 + h / 2), (0, 0, math.radians(30)))
    for p in o.data.polygons: p.use_smooth = False
    return bevel(o, 0.05)


def star(m, x, z0, r=0.5, depth=0.26):
    me = bpy.data.meshes.new('star'); bm = bmesh.new()
    vs = [bm.verts.new((math.sin(i * math.pi / 5) * (r if i % 2 == 0 else r * 0.45), 0,
                        math.cos(i * math.pi / 5) * (r if i % 2 == 0 else r * 0.45))) for i in range(10)]
    f = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    bmesh.ops.translate(bm, verts=[v for v in ext['geom'] if isinstance(v, bmesh.types.BMVert)], vec=(0, depth, 0))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('star', me); bpy.context.collection.objects.link(o)
    o.location = (x, -depth / 2, z0 + r * 0.81); o.rotation_euler = (0, 0, math.radians(-12))
    o.data.materials.append(m)
    return bevel(o, 0.045, 3)


SHAPES = {'c': (sphere, 'mint'), 't': (pyramid, 'amber'), 's': (cube, 'coral'), 'r': (star, 'pearl')}


def mats():
    return {k: mat(k, v) for k, v in PAL.items() if k not in ('steel', 'dark')} | {
        'steel': mat('steel', PAL['steel'], rough=0.32, metal=1.0, coat=0.0),
        'dark': mat('dark', PAL['dark'], rough=0.45, metal=0.6, coat=0.0)}


def floor():
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
    o = bpy.context.object; o.is_shadow_catcher = True
    return o


def lights(span=6):
    def area(loc, energy, size, col, rot):
        bpy.ops.object.light_add(type='AREA', location=loc, rotation=rot)
        L = bpy.context.object.data; L.energy = energy; L.size = size; L.color = col
    area((-span * 0.6, -6, 7), 1400, 6, (1.0, 0.92, 0.82), (math.radians(45), 0, math.radians(-25)))
    area((span * 0.8, 4, 5), 900, 5, (0.55, 0.75, 1.0), (math.radians(-60), 0, math.radians(160)))
    area((0, -8, 1.5), 250, 10, (1, 1, 1), (math.radians(85), 0, 0))


def camera(target=(0, 0, 1.25), dist=15, height=4.2, lens=55):
    bpy.ops.object.camera_add(location=(0, -dist, height))
    cam = bpy.context.object; cam.data.lens = lens
    tgt = bpy.data.objects.new('tgt', None); bpy.context.collection.objects.link(tgt); tgt.location = target
    c = cam.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
    bpy.context.scene.camera = cam
    return cam


def seesaw(M, left, right, beam=8.4, height=1.15):
    """left/right: lists of shape keys, each side listed left to right."""
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.7, radius2=0.0, depth=1.0)
    ful = bpy.context.object
    ful.rotation_euler = (math.radians(90), 0, 0); ful.scale = (1, 1.0, 0.5)
    ful.location = (0, 0, 0)
    ful.data.materials.append(M['dark']); bevel(ful, 0.05)
    # stretch triangle into a prism holding the beam
    ful.dimensions = (1.3, height, 0.7); ful.location = (0, 0, height / 2)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.95, depth=0.14, vertices=64, location=(0, 0, 0.07))
    bpy.context.object.data.materials.append(M['dark'])
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, height + 0.09))
    b = bpy.context.object; b.scale = (beam, 0.55, 0.18); b.data.materials.append(M['steel']); bevel(b, 0.06)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.16, location=(0, -0.3, height + 0.09))
    bpy.context.object.data.materials.append(M['amber'])
    top = height + 0.18; placed = []
    for side, keys in ((-1, left), (1, right)):
        n = len(keys); xs = [side * 2.05 + (i - (n - 1) / 2) * 1.05 for i in range(n)]
        for k, x in zip(keys, xs):
            fn, col = SHAPES[k]; placed.append((k, fn(M[col], x, top)))
    return placed


def project(placed):
    """Pixel position of the top centre of each placed shape, for 2D labels drawn over the sprite."""
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    sc = bpy.context.scene; bpy.context.view_layer.update(); out = []
    for k, o in placed:
        pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
        top = Vector((sum(p.x for p in pts) / 8, sum(p.y for p in pts) / 8, max(p.z for p in pts)))
        v = world_to_camera_view(sc, sc.camera, top)
        out.append({'shape': k, 'x': round(v.x * sc.render.resolution_x, 1), 'y': round((1 - v.y) * sc.render.resolution_y, 1)})
    return out


def render(path):
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
