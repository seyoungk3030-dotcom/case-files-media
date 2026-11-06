"""ROOM 142 3D sprites: a 5x5 snakes-and-ladders board seen from above at a slant: numbered squares 1-25 snaking up from
the bottom-left, wooden ladders and green snakes, a red token on square 1. p*: the board. a*: the fewest-rolls route:
each landing square (after any ladder or snake) carries a mint ring and its roll number."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, ROLLS, step
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
SP = 0.8; EL = 62.0


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - EL), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def pos(n):
    r, c = divmod(n - 1, 5)
    if r % 2: c = 4 - c
    return ((c - 2) * SP, (r - 2) * SP)


def rod(p, q, r, m, z=0.09):
    (x1, y1), (x2, y2) = p, q; L = math.hypot(x2 - x1, y2 - y1)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=((x1 + x2) / 2, (y1 + y2) / 2, z), vertices=12,
                                        rotation=(0, math.radians(90), math.atan2(y2 - y1, x2 - x1))); bpy.context.object.data.materials.append(m)


def ladder(a, b, m):
    (x1, y1), (x2, y2) = pos(a), pos(b); L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L; nx, ny = -uy * 0.13, ux * 0.13
    for s in (1, -1): rod((x1 + s * nx, y1 + s * ny), (x2 + s * nx, y2 + s * ny), 0.03, m)
    k = int(L / 0.22)
    for i in range(1, k):
        t = i / k; cx, cy = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t; rod((cx + nx, cy + ny), (cx - nx, cy - ny), 0.022, m)


def snake(h, t, m, head):
    (x1, y1), (x2, y2) = pos(h), pos(t); L = math.hypot(x2 - x1, y2 - y1); nx, ny = -(y2 - y1) / L, (x2 - x1) / L
    cu = bpy.data.curves.new('s', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.055; cu.bevel_resolution = 4
    sp = cu.splines.new('POLY'); N = 40; sp.points.add(N - 1)
    for i in range(N):
        u = i / (N - 1); w = 0.28 * math.sin(u * 3 * math.pi) * (1 - 0.3 * u)
        sp.points[i].co = (x1 + (x2 - x1) * u + nx * w, y1 + (y2 - y1) * u + ny * w, 0.1, 1)
    o = bpy.data.objects.new('s', cu); bpy.context.collection.objects.link(o); o.data.materials.append(m)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, location=(x1, y1, 0.12), segments=20, ring_count=10); bpy.context.object.scale = (1.2, 1.2, 0.7); bpy.context.object.data.materials.append(head)


def scene(k, after):
    J = BOARDS[k]
    t1 = b3d.mat('t1', (0.34, 0.26, 0.16), rough=0.9, coat=0); t2 = b3d.mat('t2', (0.14, 0.22, 0.24), rough=0.9, coat=0)
    for m in (t1, t2): m.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0.1
    frame = b3d.mat('frame', (0.12, 0.08, 0.05), rough=0.7, coat=0); ink = b3d.mat('ink', (0.95, 0.9, 0.8), rough=0.8, coat=0); glow(ink, (0.95, 0.9, 0.8), 0.3)
    wood = b3d.mat('wood', (0.85, 0.55, 0.2), rough=0.5, coat=0); green = b3d.mat('green', (0.1, 0.6, 0.15), rough=0.4, coat=0.3)
    head = b3d.mat('head', (0.05, 0.45, 0.1), rough=0.4, coat=0.3); red = b3d.mat('red', (0.85, 0.1, 0.1), rough=0.3, coat=0.4)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.5)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.08)); o = bpy.context.object; o.scale = (5 * SP + 0.3, 5 * SP + 0.3, 0.14); o.data.materials.append(frame); b3d.bevel(o, 0.06)
    for n in range(1, 26):
        x, y = pos(n); bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.0)); o = bpy.context.object; o.scale = (SP - 0.03, SP - 0.03, 0.02); o.data.materials.append(t1 if n % 2 else t2)
        text(str(n), (x - 0.2, y + 0.2, 0.02), 0.2, ink)
    for a, b in J.items():
        if b > a: ladder(a, b, wood)
        else: snake(a, b, green, head)
    x, y = pos(1); bpy.ops.mesh.primitive_cylinder_add(radius=0.16, depth=0.18, location=(x + 0.1, y - 0.08, 0.1), vertices=32); bpy.context.object.data.materials.append(red)
    if after:
        p = 1
        for i, r in enumerate(ROLLS[k], 1):
            p = step(p, r, J); x, y = pos(p)
            bpy.ops.mesh.primitive_torus_add(location=(x, y, 0.05), major_radius=0.33, minor_radius=0.03, major_segments=40); bpy.context.object.data.materials.append(mint)
            text(f'{i}', (x + 0.12, y - 0.12, 0.32), 0.3, mint)
    b3d.stack_camera((0, -0.05, 0.05), 4.6, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
