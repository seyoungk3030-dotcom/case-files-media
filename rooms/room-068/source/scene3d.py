"""ROOM 068 3D sprites: a 5x5 tilt tray seen from the front and above. Dark blocks, numbers printed on floor cells,
a steel ball at the start, the tilt order as arrows in front of the tray. a*: amber path through every stop and the
ball on the final cell, whose number glows amber."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, DIR, N, slide
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
S = 0.5
ARROW = {'U': '↑', 'D': '↓', 'L': '←', 'R': '→'}


def xy(c, r): return ((c - 2) * S, (2 - r) * S)


def text(s, loc, size, m, rot=(0, 0, 0)):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def box(loc, scale, m, bev=0.03):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def stops(bl, st, mv):
    pts = [st]
    for i in range(len(mv)): pts.append(slide(bl, st, mv[:i + 1]))
    return pts


def scene(k, after):
    bl, st, mv, num = BOARDS[k]
    wood = b3d.mat('wood', (0.50, 0.36, 0.24), rough=0.55, coat=0.2); floor = b3d.mat('fl', (0.86, 0.88, 0.92), rough=0.5, coat=0.1)
    blk = b3d.mat('blk', (0.18, 0.22, 0.32), rough=0.35, coat=0.5); steel = b3d.mat('ball', (0.92, 0.28, 0.22), rough=0.2, coat=0.8)
    ink = b3d.mat('ink', (0.20, 0.30, 0.50), rough=0.5, coat=0.0); amber = b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3)
    white = b3d.mat('white', (0.96, 0.97, 0.99), rough=0.4); mint = b3d.mat('mint', b3d.PAL['mint'], rough=0.3, coat=0.5)
    for p in (amber, mint):
        q = p.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
        q.inputs['Emission Strength'].default_value = 0.8
    W = N * S
    box((0, 0, -0.06), (W + 0.3, W + 0.3, 0.12), wood, 0.04)
    box((0, 0, 0.005), (W, W, 0.01), floor, 0.003)
    for sgn in (-1, 1):
        box((0, sgn * (W / 2 + 0.075), 0.1), (W + 0.3, 0.15, 0.2), wood, 0.03)
        box((sgn * (W / 2 + 0.075), 0, 0.1), (0.15, W, 0.2), wood, 0.03)
    for i in range(1, N):   # faint grid
        box(((i - 2.5) * S, 0, 0.012), (0.012, W, 0.004), b3d.mat('g', (0.70, 0.74, 0.82), rough=0.6, coat=0), 0.001)
        box((0, (i - 2.5) * S, 0.012), (W, 0.012, 0.004), b3d.mat('g', (0.70, 0.74, 0.82), rough=0.6, coat=0), 0.001)
    for c, r in bl:
        x, y = xy(c, r); box((x, y, 0.14), (S * 0.92, S * 0.92, 0.28), blk, 0.05)
    end = slide(bl, st, mv)
    for (c, r), d in num.items():
        x, y = xy(c, r); hot = after and (c, r) == end
        text(str(d), (x, y, 0.09), 0.34, amber if hot else ink)
    if after:
        pts = stops(bl, st, mv)
        for (c0, r0), (c1, r1) in zip(pts, pts[1:]):
            (x0, y0), (x1, y1) = xy(c0, r0), xy(c1, r1); L = math.hypot(x1 - x0, y1 - y0)
            if L < 1e-6: continue
            bpy.ops.mesh.primitive_cylinder_add(radius=0.022, depth=L, location=((x0 + x1) / 2, (y0 + y1) / 2, 0.035),
                                                rotation=(0, math.radians(90), math.atan2(y1 - y0, x1 - x0)))
            bpy.context.object.data.materials.append(amber)
        x, y = xy(*st); bpy.ops.mesh.primitive_torus_add(major_radius=0.13, minor_radius=0.02, location=(x, y, 0.03))
        bpy.context.object.data.materials.append(white)
        x, y = xy(*end)
        bpy.ops.mesh.primitive_torus_add(major_radius=0.22, minor_radius=0.03, location=(x, y, 0.03)); bpy.context.object.data.materials.append(amber)
    else:
        x, y = xy(*st); bpy.ops.mesh.primitive_uv_sphere_add(radius=0.19, location=(x, y, 0.2), segments=48, ring_count=24)
        bpy.context.object.data.materials.append(steel)
        for p in bpy.context.object.data.polygons: p.use_smooth = True
    # tilt order in front of the tray
    for i, m in enumerate(mv):
        x = (i - (len(mv) - 1) / 2) * 0.75
        bpy.ops.mesh.primitive_cylinder_add(radius=0.27, depth=0.06, location=(x, -W / 2 - 0.62, 0.03)); bpy.context.object.data.materials.append(mint)
        text(ARROW[m], (x, -W / 2 - 0.62, 0.07), 0.38, white)
        if i < len(mv) - 1: text('·', (x + 0.375, -W / 2 - 0.62, 0.02), 0.3, white)
    b3d.stack_camera((0, -0.4, 0), 4.2, az=0.0, el=68.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 900), 40); b3d.lights(5)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
