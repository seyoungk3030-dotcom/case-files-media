"""ROOM 164 3D sprites: a 3x3 jigsaw on a dark tray with one empty slot (top) and four numbered loose pieces in a row below,
seen from above at a slant. p*: the start. a*: the fitting piece sits in the slot, turned the right way, glowing mint;
its place among the loose pieces is empty."""
import math, os, sys, time
import bpy, bmesh
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
S = 1.0; EL = 62.0; X0 = 0.0; Y0 = 0.95
COLS = [(0.95, 0.55, 0.25), (0.35, 0.6, 0.95), (0.95, 0.8, 0.25), (0.6, 0.4, 0.9), (0.4, 0.8, 0.45), (0.95, 0.45, 0.6), (0.95, 0.62, 0.5), (0.85, 0.65, 0.45), (0.65, 0.7, 0.95)]
LOOSE = [(0.25, 0.1, 0.05), (0.6, 0.62, 0.66), (0.98, 0.5, 0.45), (0.55, 0.45, 0.85)]


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def outline(p):
    top, right, bot, left = p; h = S / 2 * 0.98
    sides = [((-h, -h), (h, -h), (0, -1), bot), ((h, -h), (h, h), (1, 0), right), ((h, h), (-h, h), (0, 1), top), ((-h, h), (-h, -h), (-1, 0), left)]
    pts = []
    for (ax, ay), (bx, by), (nx, ny), st in sides:
        pts.append((ax, ay))
        if st == 'F': continue
        mx, my = (ax + bx) / 2, (ay + by) / 2; tx, ty = (bx - ax) / (2 * h), (by - ay) / (2 * h)
        sg = 1 if st == 'T' else -1; r = 0.16; cx, cy = mx + sg * nx * 0.13, my + sg * ny * 0.13
        p0 = (mx - tx * 0.09, my - ty * 0.09); p1 = (mx + tx * 0.09, my + ty * 0.09)
        a0 = math.atan2(p0[1] - cy, p0[0] - cx); a1 = math.atan2(p1[1] - cy, p1[0] - cx)
        # sweep the long way round (through the bump side)
        mid = math.atan2(sg * ny, sg * nx)
        d = (a1 - a0) % (2 * math.pi)
        if not (0 < (mid - a0) % (2 * math.pi) < d): d -= 2 * math.pi
        pts.append(p0)
        for i in range(1, 20):
            a = a0 + d * i / 20; pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        pts.append(p1)
    return pts


def piece(p, x, y, m, z=0.0, th=0.16, sc=1.0):
    me = bpy.data.meshes.new('pc'); bm = bmesh.new()
    vs = [bm.verts.new((px, py, 0)) for px, py in outline(p)]
    f = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    bmesh.ops.translate(bm, verts=[v for v in ext['geom'] if isinstance(v, bmesh.types.BMVert)], vec=(0, 0, th))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('pc', me); bpy.context.collection.objects.link(o); o.location = (x, y, z); o.scale = (sc, sc, 1); o.data.materials.append(m)
    b3d.bevel(o, 0.025, 2)
    return o


def label(d, x, y, z, M):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.24, depth=0.03, location=(x, y, z), vertices=32); bpy.context.object.data.materials.append(M['plate'])
    bpy.ops.object.text_add(location=(x, y, z + 0.02)); t = bpy.context.object; t.data.body = str(d)
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = 0.36; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(M['ink'])


def scene(k, after):
    b = BOARDS[k]; hr, hc = b['hole']
    M = {'tray': b3d.mat('tray', (0.1, 0.11, 0.14), rough=0.8, coat=0), 'slot': b3d.mat('slot', (0.03, 0.03, 0.05), rough=1, coat=0),
         'plate': b3d.mat('plate', (0.98, 0.82, 0.25), rough=0.4, coat=0), 'ink': b3d.mat('ink', (0.06, 0.07, 0.1), rough=0.8, coat=0),
         'frame': b3d.mat('frame', (0.45, 0.3, 0.18), rough=0.7, coat=0)}
    mint = b3d.mat('mint', (0.0, 0.62, 0.4), rough=0.3, coat=0); glow(mint, (0.05, 0.8, 0.5), 0.9)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(X0, Y0, -0.06)); o = bpy.context.object; o.scale = (3.5, 3.5, 0.12); o.data.materials.append(M['tray']); b3d.bevel(o, 0.05)
    for sx, sy, w, d in ((0, 1.72, 3.56, 0.12), (0, -1.72, 3.56, 0.12), (1.72, 0, 0.12, 3.32), (-1.72, 0, 0.12, 3.32)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(X0 + sx, Y0 + sy, 0.08)); o = bpy.context.object; o.scale = (w, d, 0.2); o.data.materials.append(M['frame'])
    bpy.ops.mesh.primitive_cube_add(size=1, location=(X0 + (hc - 1) * S, Y0 + (1 - hr) * S, 0.001)); o = bpy.context.object; o.scale = (S * 0.9, S * 0.9, 0.002); o.data.materials.append(M['slot'])
    i = 0
    for r in range(3):
        for c in range(3):
            if (r, c) == (hr, hc):
                if after: piece(tuple(b['need']), X0 + (c - 1) * S, Y0 + (1 - r) * S, mint)
                continue
            piece(tuple(b['grid'][f'{r}{c}']), X0 + (c - 1) * S, Y0 + (1 - r) * S, b3d.mat(f'p{i}', COLS[i % len(COLS)], rough=0.45, coat=0.2)); i += 1
    for j, p in enumerate(b['loose']):
        if after and j == GOOD[k]: continue
        x = (j - 1.5) * 1.42; y = -1.75
        piece(tuple(p), x, y, b3d.mat(f'l{j}', (0.92, 0.9, 0.85), rough=0.5, coat=0.2), sc=1.0)
        label(b['digits'][j], x, y, 0.18, M)
    b3d.stack_camera((0.0, -0.15, 0), 6.5, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 900), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
