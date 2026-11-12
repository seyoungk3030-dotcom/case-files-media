"""ROOM 175 3D sprites: a ruler lying on the desk seen from above and in front, with an object resting against its top
edge (pencil, crayon, eraser, key). Ticks every 0.5 cm along the top edge, numbers every cm. B is a broken ruler with a
jagged left end, C shows the blank margin before 0, D lies upside down so its numbers fall from left to right.
p*: as above. a*: mint marks on the ticks under both ends of the object and a mint bar with the true length."""
import math, os, sys, time
import bpy, bmesh
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD, mark_at
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U = 0.3; RW = 0.85; X0 = -6.5 * U  # one cm in scene units, ruler width; scene x of the ruler's left end (13 cm ruler centred)


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def box(loc, scale, m, bev=0.0, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.004; t.data.materials.append(m)


def X(cm): return X0 + cm * U


def cyl_x(a, b, r, m, y, z, verts=32, cone_to=None):
    if cone_to is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=b - a, location=((a + b) / 2, y, z), rotation=(0, math.pi / 2, 0), vertices=verts)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r, radius2=cone_to, depth=b - a, location=((a + b) / 2, y, z), rotation=(0, math.pi / 2, 0), vertices=verts)
    o = bpy.context.object; o.data.materials.append(m); return o


def ruler(b, plastic, ink):
    L = b['length']; broken = b['margin'] == 0 and b['first'] > 0
    me = bpy.data.meshes.new('r'); bm = bmesh.new()
    left = [(-0.3 * U, -RW / 2), (-0.05 * U, -RW / 4), (-0.4 * U, 0), (-0.12 * U, RW / 4), (0, RW / 2)] if broken else [(0, -RW / 2), (0, RW / 2)]
    outline = [(X(0) + dx, y) for dx, y in left[::-1]]  # top-left down to bottom-left
    outline = [(X(0) + dx, y) for dx, y in left] [::-1]
    pts = [(X(0) + left[0][0], -RW / 2), (X(L), -RW / 2), (X(L), RW / 2)] + [(X(0) + dx, y) for dx, y in left[::-1][:-1]]
    vb = [bm.verts.new((x, y, 0)) for x, y in pts]; vt = [bm.verts.new((x, y, 0.06)) for x, y in pts]
    bm.faces.new(vb[::-1]); bm.faces.new(vt)
    for i in range(len(pts)):
        j = (i + 1) % len(pts); bm.faces.new((vb[i], vb[j], vt[j], vt[i]))
    bm.normal_update(); bm.to_mesh(me); o = bpy.data.objects.new('r', me); bpy.context.collection.objects.link(o); o.data.materials.append(plastic)
    k = 0
    while True:  # ticks every half cm from the first printed mark, both ways, within the ruler
        for sgn in ((1,) if k == 0 else (1, -1)):
            x = b['margin'] + sgn * k * 0.5
            if not (0.05 <= x <= L - 0.05) and not (broken and abs(x) < 1e-6): continue
            full = abs((x - b['margin']) % 1) < 1e-6; h = 0.34 if full else 0.18
            box((X(x), RW / 2 - h / 2, 0.065), (0.022, h, 0.01), ink)
            if full:
                n = mark_at(b, x)
                if n >= 0: text(str(int(n)), (X(x), RW / 2 - 0.5, 0.07), 0.17, ink)
        k += 1
        if k > 2 * L + 2: break


def obj(b, mats, y):
    a, c = X(b['x0']), X(b['x1']); kind = b['obj']; z = 0.11
    if kind == 'pencil':
        cyl_x(a, c - 0.55 * U * 2, 0.11, mats['yellow'], y, z, verts=6)
        cyl_x(c - 1.1 * U, c - 0.25 * U, 0.105, mats['wood'], y, z, cone_to=0.035)
        cyl_x(c - 0.25 * U, c, 0.035, mats['lead'], y, z, cone_to=0.002)
        cyl_x(a - 0.0, a + 0.35 * U, 0.112, mats['pink'], y, z)
    elif kind == 'crayon':
        cyl_x(a, c - 0.6 * U, 0.12, mats['blue'], y, z + 0.01)
        cyl_x(a + 0.6 * U, c - 0.9 * U, 0.125, mats['paper'], y, z + 0.01)
        cyl_x(c - 0.6 * U, c, 0.12, mats['blue'], y, z + 0.01, cone_to=0.035)
    elif kind == 'eraser':
        box(((a + c) / 2, y + 0.02, 0.13), (c - a, 0.42, 0.26), mats['white'], 0.04)
        box((a + 0.62 * (c - a), y + 0.02, 0.135), (0.5 * (c - a), 0.44, 0.27), mats['blue'], 0.02)
    else:  # key: ring at the left, blade with teeth to the right
        y += 0.12
        bpy.ops.mesh.primitive_torus_add(location=(a + 0.3, y, 0.05), major_radius=0.22, minor_radius=0.08); bpy.context.object.data.materials.append(mats['brass'])
        box(((a + 0.58 + c) / 2, y, 0.05), (c - a - 0.58, 0.15, 0.08), mats['brass'], 0.02)
        for i in range(4): box((a + 1.2 + i * 0.32, y - 0.1, 0.05), (0.14, 0.1, 0.08), mats['brass'])
        bpy.ops.mesh.primitive_cone_add(radius1=0.085, radius2=0.0, depth=0.0001, location=(c, y, 0.05)); bpy.context.object.data.materials.append(mats['brass'])


def scene(k, after):
    b = BOARDS[k]
    plastic = b3d.mat('plastic', (0.98, 0.86, 0.45), rough=0.35, coat=0.4) if b['dir'] > 0 else b3d.mat('plastic', (0.7, 0.88, 0.95), rough=0.35, coat=0.4)
    ink = b3d.mat('ink', (0.06, 0.06, 0.08), rough=0.5, coat=0); mint = glowm('mint', (0.15, 0.85, 0.6), 2.0)
    mats = dict(yellow=b3d.mat('y', (1.0, 0.75, 0.1), rough=0.4, coat=0.5), wood=b3d.mat('w', (0.9, 0.72, 0.5), rough=0.7, coat=0),
                lead=b3d.mat('l', (0.15, 0.15, 0.17), rough=0.4, coat=0), pink=b3d.mat('p', (1.0, 0.5, 0.6), rough=0.5, coat=0.2),
                blue=b3d.mat('b', (0.2, 0.45, 0.95), rough=0.5, coat=0.2), paper=b3d.mat('pa', (0.95, 0.95, 0.9), rough=0.7, coat=0),
                white=b3d.mat('wh', (0.97, 0.97, 0.97), rough=0.6, coat=0), brass=b3d.mat('br', (0.95, 0.75, 0.3), rough=0.4, metal=0.5))
    ruler(b, plastic, ink)
    y = RW / 2 + 0.2; obj(b, mats, y)
    if after:
        for x in (b['x0'], b['x1']): box((X(x), RW / 2 - 0.19, 0.075), (0.06, 0.38, 0.012), mint)
        box(((X(b['x0']) + X(b['x1'])) / 2, -RW / 2 + 0.1, 0.065), (X(b['x1']) - X(b['x0']), 0.07, 0.012), mint)
    b3d.stack_camera((0, 0.0, 0), 4.3, az=0.0, el=62.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((1300, 560), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
