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


def cubestack(hm, col, ghost=(), hidden_col=None, n=3):
    """hm[row][col] heights, row 0 = front (y=0), col 0 = left (x=0). Cubes are unit size on an n x n floor.
    Cells in ghost (i, j, k) are hidden cubes: they get hidden_col, every other cube turns see-through."""
    tile = mat('tile', (0.62, 0.68, 0.78), rough=0.5, coat=0.0)
    base = mat('base', (0.20, 0.26, 0.36), rough=0.5, coat=0.0)
    solid = mat('cube', col, rough=0.3, coat=0.5)
    glass = mat('glass', col, rough=0.2, coat=0.0)
    hidm = mat('hid', hidden_col or col)
    q = hidm.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*(hidden_col or col), 1)
    q.inputs['Emission Strength'].default_value = 1.4
    if ghost:
        p = glass.node_tree.nodes['Principled BSDF']; p.inputs['Alpha'].default_value = 0.11
    bpy.ops.mesh.primitive_cube_add(size=1, location=(n / 2, n / 2, -0.16))
    b = bpy.context.object; b.scale = (n + 0.3, n + 0.3, 0.3); b.data.materials.append(base); bevel(b, 0.06)
    for i in range(n):
        for j in range(n):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(i + 0.5, j + 0.5, -0.02))
            t = bpy.context.object; t.scale = (0.94, 0.94, 0.04); t.data.materials.append(tile)
            for k in range(hm[j][i]):
                bpy.ops.mesh.primitive_cube_add(size=0.985, location=(i + 0.5, j + 0.5, k + 0.5))
                c = bpy.context.object
                hid = (i, j, k) in ghost
                c.data.materials.append(hidm if hid else (glass if ghost else solid))
                bevel(c, 0.07, 3)


def stack_camera(center, scale, az=33.0, el=30.0):
    """Orthographic camera from the front-right-top; matches the visibility model in a room's view.py."""
    d = (math.sin(math.radians(az)) * math.cos(math.radians(el)), -math.cos(math.radians(az)) * math.cos(math.radians(el)),
         math.sin(math.radians(el)))
    bpy.ops.object.camera_add(location=tuple(c + 30 * x for c, x in zip(center, d)))
    cam = bpy.context.object; cam.data.type = 'ORTHO'; cam.data.ortho_scale = scale; cam.data.clip_end = 100
    tgt = bpy.data.objects.new('tgt', None); bpy.context.collection.objects.link(tgt); tgt.location = center
    c = cam.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
    bpy.context.scene.camera = cam
    return cam


PIPS = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        5: [(-1, -1), (-1, 1), (0, 0), (1, -1), (1, 1)], 6: [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)]}


def die(R, loc=(0, 0, 0.5), faces=None, body=(0.92, 0.90, 0.84), pip=(0.06, 0.07, 0.10), glow=None):
    """A standard die (rounded cube of size 1) rotated by the 3x3 matrix R about its centre at loc.
    faces maps unrotated outward normals to numbers (default: 1 up, 2 front, 3 right). glow: (normal in world,
    colour) lights up the pips of the face pointing that way."""
    from mathutils import Matrix
    faces = faces or {(0, 0, 1): 1, (0, 0, -1): 6, (0, -1, 0): 2, (0, 1, 0): 5, (1, 0, 0): 3, (-1, 0, 0): 4}
    root = bpy.data.objects.new('die', None); bpy.context.collection.objects.link(root)
    bpy.ops.mesh.primitive_cube_add(size=1)
    b = bpy.context.object; b.data.materials.append(mat('die', body, rough=0.25, coat=0.7)); bevel(b, 0.13, 6)
    for p in b.data.polygons: p.use_smooth = True
    b.parent = root
    pm = mat('pip', pip, rough=0.4, coat=0.3)
    gm = None
    if glow:
        gm = mat('pipglow', glow[1], rough=0.3, coat=0.0)
        q = gm.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*glow[1], 1)
        q.inputs['Emission Strength'].default_value = 2.5
    for n, num in faces.items():
        n = tuple(n); ax = [i for i in range(3) if n[i] == 0]
        world_n = tuple(int(v) for v in (R @ __import__('numpy').array(n)))
        m = gm if glow and world_n == tuple(glow[0]) else pm
        for u, v in PIPS[num]:
            pos = [0.0, 0.0, 0.0]; pos[ax[0]] = u * 0.25; pos[ax[1]] = v * 0.25
            for i in range(3):
                if n[i]: pos[i] = n[i] * 0.497
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.085, segments=24, ring_count=12, location=pos)
            s = bpy.context.object; sc = [1, 1, 1]
            for i in range(3):
                if n[i]: sc[i] = 0.35
            s.scale = sc; s.data.materials.append(m)
            for p in s.data.polygons: p.use_smooth = True
            s.parent = root
    M = Matrix(((float(R[0][0]), float(R[0][1]), float(R[0][2]), loc[0]), (float(R[1][0]), float(R[1][1]), float(R[1][2]), loc[1]),
                (float(R[2][0]), float(R[2][1]), float(R[2][2]), loc[2]), (0, 0, 0, 1)))
    root.matrix_world = M
    return root


def gear(n, m=0.12, loc=(0, 0, 0), theta=0.0, mt=None, thick=0.22, hub=None):
    """Spur gear lying flat: n teeth, module m (pitch radius m*n/2), centre loc (bottom face at loc z), rotated
    theta radians; tooth k is centred at angle theta + 2*pi*k/n. Returns the gear object."""
    r = m * n / 2; ra, rf = r + m, r - 1.2 * m
    pts = []
    for k in range(n):
        c = theta + 2 * math.pi * k / n; w = math.pi / n
        for a, rr in ((c - w * 1.0, rf), (c - w * 0.55, rf), (c - w * 0.32, ra), (c + w * 0.32, ra), (c + w * 0.55, rf), (c + w * 1.0, rf)):
            pts.append((math.cos(a) * rr, math.sin(a) * rr))
    me = bpy.data.meshes.new('gear'); bm = bmesh.new()
    vs = [bm.verts.new((x, y, 0)) for x, y in pts[:-1] if True]
    bmesh.ops.remove_doubles(bm, verts=vs, dist=1e-5)
    f = bm.faces.new(bm.verts)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    bmesh.ops.translate(bm, verts=[v for v in ext['geom'] if isinstance(v, bmesh.types.BMVert)], vec=(0, 0, thick))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('gear', me); bpy.context.collection.objects.link(o)
    o.location = loc; o.data.materials.append(mt)
    bevel(o, 0.018, 2)
    bpy.ops.mesh.primitive_cylinder_add(radius=max(0.09, r * 0.28), depth=thick + 0.06, vertices=48,
                                        location=(loc[0], loc[1], loc[2] + thick / 2))
    h = bpy.context.object; h.data.materials.append(hub or mt); bevel(h, 0.02, 2)
    return o


MESH_SIGN = 1


def mesh_angle(c2, n2, c3, n3, th2, m=0.12):
    """Rotation for gear 3 so it meshes with gear 2 (centres c2, c3; teeth n2, n3; gear 2 rotated th2)."""
    psi = math.atan2(c3[1] - c2[1], c3[0] - c2[0]); r2, r3 = m * n2 / 2, m * n3 / 2
    step = 2 * math.pi / n2; u = r2 * ((psi - th2) % step)
    if u > r2 * step / 2: u -= r2 * step
    return psi + math.pi + math.pi / n3 + MESH_SIGN * u / r3
