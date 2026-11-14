"""ROOM 182 3D sprites: sneakers scattered on a front-door mat, seen from straight above. Left and right shoes are
mirror images (big-toe bulge on the inner side). p*: question. a*: answer, each shoe shows L or R, paired shoes
glow mint underneath and leftover shoes are dimmed."""
import math, os, sys, time
import bpy, bmesh
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
COL = {'red': (0.85, 0.15, 0.15), 'blue': (0.15, 0.4, 0.9), 'yellow': (0.98, 0.78, 0.1)}
SC, LEN = 1.25, 1.05  # grid unit, shoe length
# LEFT shoe outline (toe up): medial edge on +x with the big-toe bulge, lateral edge on -x
RIGHT_EDGE = [(-0.5, 0.0), (-0.45, 0.1), (-0.3, 0.11), (-0.15, 0.08), (0.0, 0.1), (0.15, 0.14), (0.3, 0.15), (0.42, 0.14), (0.5, 0.09)]
LEFT_EDGE = [(-0.45, -0.1), (-0.3, -0.14), (-0.1, -0.2), (0.1, -0.25), (0.25, -0.24), (0.38, -0.18), (0.47, -0.07)]


def outline(side):
    pts = [(x, y) for y, x in RIGHT_EDGE] + [(x, y) for y, x in reversed(LEFT_EDGE)]
    if side == 'R': pts = [(-x, y) for x, y in reversed(pts)]
    return pts


def prism(pts, z0, h, m, sc=1.0, name='p'):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    vs = [bm.verts.new((x * sc, y * sc, z0)) for x, y in pts]; f = bm.faces.new(vs)
    bmesh.ops.recalc_face_normals(bm, faces=[f])
    if f.normal.z < 0: f.normal_flip()
    r = bmesh.ops.extrude_face_region(bm, geom=[f]); top = [v for v in r['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, h), verts=top); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o); o.data.materials.append(m)
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.modifier_add(type='BEVEL'); o.modifiers['Bevel'].width = 0.02; o.modifiers['Bevel'].segments = 2
    return o


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def scene(k, after):
    shoes = BOARDS[k]
    mat_ = b3d.mat('mat', (0.32, 0.27, 0.22), rough=0.9, coat=0); sole = b3d.mat('sole', (0.96, 0.96, 0.94), rough=0.5, coat=0)
    dark = b3d.mat('dark', (0.08, 0.08, 0.1), rough=0.6, coat=0); lace = b3d.mat('lace', (1, 1, 1), rough=0.5, coat=0)
    grey = b3d.mat('grey', (0.45, 0.45, 0.48), rough=0.5, coat=0); mint = glowm('mint', (0.15, 0.85, 0.6), 1.2)
    ink = b3d.mat('ink', (0.05, 0.05, 0.07), rough=0.5, coat=0)
    xs = [s[2] for s in shoes]; ys = [s[3] for s in shoes]; cx0 = (min(xs) + max(xs)) / 2 * SC; cy0 = (min(ys) + max(ys)) / 2 * SC
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.03)); o = bpy.context.object
    o.scale = ((max(xs) - min(xs)) * SC + 1.4, (max(ys) - min(ys)) * SC + 1.4, 0.06); o.data.materials.append(mat_)
    paired = set()
    if after:
        for c in COL:
            Ls = [i for i, s in enumerate(shoes) if s[0] == c and s[1] == 'L']; Rs = [i for i, s in enumerate(shoes) if s[0] == c and s[1] == 'R']
            for a, b in zip(Ls, Rs): paired |= {a, b}
    for i, (c, side, gx, gy, hd) in enumerate(shoes):
        objs = []
        dim = 0.45 if after and i not in paired else 1.0
        upper = b3d.mat(f'u{i}', tuple(v * dim for v in COL[c]), rough=0.35, coat=0.4)
        pts = [(x * LEN, y * LEN) for x, y in outline(side)]
        if after and i in paired: objs.append(prism(pts, -0.01, 0.02, mint, 1.12, f'g{i}'))
        objs.append(prism(pts, 0.0, 0.07, sole, 1.0, f's{i}'))
        objs.append(prism(pts, 0.07, 0.17, upper, 0.9, f'u{i}'))
        sx = 0.02 if side == 'L' else -0.02
        bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.02, location=(sx * LEN, -0.24 * LEN, 0.245)); o = bpy.context.object; o.scale = (1.0, 1.5, 1); o.data.materials.append(dark); objs.append(o)
        for j in range(3):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(sx * LEN, (-0.02 + j * 0.09) * LEN, 0.245)); o = bpy.context.object; o.scale = (0.14 * LEN, 0.025, 0.015); o.data.materials.append(lace); objs.append(o)
        if after:
            bpy.ops.object.text_add(location=(sx * LEN, 0.27 * LEN, 0.26)); t = bpy.context.object; t.data.body = side
            t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
            t.data.size = 0.2; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.005; t.data.materials.append(ink); objs.append(t)
        bpy.ops.object.empty_add(location=(gx * SC - cx0, gy * SC - cy0, 0), rotation=(0, 0, math.radians(-hd))); e = bpy.context.object
        for o in objs: o.parent = e
    b3d.stack_camera((0, 0, 0), max((max(xs) - min(xs)) * SC + 1.5, ((max(ys) - min(ys)) * SC + 1.5) * 1.6), az=0.0, el=89.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((960, 600), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
