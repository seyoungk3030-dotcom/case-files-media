"""ROOM 105 3D sprites: a 6x6 navy and grey board with a white toy knight, white pawns and four amber numbered squares,
seen from the front and above. a*: the knight's middle stop gets a mint ring, the reachable numbered square turns
mint, and two mint arcs trace the two jumps."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, N, jumps
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def P(cell, z=0.0): r, c = cell; return Vector((c - (N - 1) / 2, (N - 1) / 2 - r, z))


def cyl(r, d, loc, m, v=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, vertices=v); o = bpy.context.object; o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = True
    return o


def pawn(cell, m):
    p = P(cell); cyl(0.3, 0.12, p + Vector((0, 0, 0.06)), m); bpy.ops.mesh.primitive_cone_add(radius1=0.22, radius2=0.09, depth=0.42, location=p + Vector((0, 0, 0.33)), vertices=48)
    bpy.context.object.data.materials.append(m)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, location=p + Vector((0, 0, 0.6)), segments=32, ring_count=16); o = bpy.context.object; o.data.materials.append(m)
    for q in o.data.polygons: q.use_smooth = True


def knight(cell, m):
    p = P(cell); cyl(0.36, 0.14, p + Vector((0, 0, 0.07)), m)
    bpy.ops.object.text_add(location=p + Vector((0, 0, 0.78)), rotation=(math.radians(90), 0, 0)); t = bpy.context.object
    t.data.body = '\u265e'; t.data.font = bpy.data.fonts.load('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    t.data.size = 2.1; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.13; t.data.bevel_depth = 0.02
    t.data.materials.append(m)


def arc(a, b, m, h=0.9):
    pts = [a.lerp(b, t) + Vector((0, 0, 0.2 + h * 4 * t * (1 - t))) for t in [i / 30 for i in range(31)]]
    cu = bpy.data.curves.new('a', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.04
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for i, q in enumerate(pts): sp.points[i].co = (*q, 1)
    o = bpy.data.objects.new('a', cu); bpy.context.collection.objects.link(o); o.data.materials.append(m)


def scene(k, after):
    b = BOARDS[k]; win = b['num'][RES[k][0]]; block = set(b['pawns'])
    dark = b3d.mat('dark', (0.06, 0.08, 0.15), rough=0.6, coat=0.1); light = b3d.mat('light', (0.24, 0.27, 0.34), rough=0.6, coat=0.1)
    amber = b3d.mat('amber', (0.85, 0.42, 0.06), rough=0.5, coat=0.1); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    ivory = b3d.mat('ivory', (0.85, 0.83, 0.78), rough=0.35, coat=0.4); frame = b3d.mat('frame', (0.03, 0.04, 0.07), rough=0.6, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.0)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.12)); o = bpy.context.object; o.scale = (N + 0.5, N + 0.5, 0.2); o.data.materials.append(frame); b3d.bevel(o, 0.05)
    lab = {v: n for n, v in b['num'].items()}
    for r in range(N):
        for c in range(N):
            m = amber if (r, c) in lab else (light if (r + c) % 2 == 0 else dark)
            if after and (r, c) == win: m = mint
            bpy.ops.mesh.primitive_cube_add(size=1, location=P((r, c), -0.02)); o = bpy.context.object; o.scale = (0.98, 0.98, 0.04); o.data.materials.append(m)
            if (r, c) in lab: text(str(lab[(r, c)]), P((r, c), 0.01), 0.62, ink)
    knight(b['knight'], ivory)
    for q in b['pawns']: pawn(q, ivory)
    if after:
        mid = next(m for m in jumps(b['knight'], block) if win in jumps(m, block))
        bpy.ops.mesh.primitive_torus_add(location=P(mid, 0.03), major_radius=0.36, minor_radius=0.05); bpy.context.object.data.materials.append(mint)
        arc(P(b['knight']), P(mid), mint); arc(P(mid), P(win), mint)
    b3d.stack_camera((0, 0.1, 0.25), 8.6, az=10.0, el=50.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 800), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
