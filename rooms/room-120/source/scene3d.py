"""ROOM 120 3D sprites: side view of a toy track: a straight ramp with amber start marks 1-9 (1 ruler unit apart in
height) curving into a flat run and a vertical loop of the board's diameter. A grey dashed line marks the loop top.
A coral ice sled waits at the top of the ramp. a*: the sled sits at the lowest mark that makes the loop (tag turns
mint), a mint dashed line shows the needed height and the loop glows mint."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, lowest
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U, XT, XB, Y = 0.36, -3.4, -0.9, 0.0
SLOPE = 9.6 * U / (XB - XT)


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def box(m, c, s, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def tube(pts, r, m):
    cu = bpy.data.curves.new('t', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = r; cu.bevel_resolution = 4
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for i, q in enumerate(pts): sp.points[i].co = (*q, 1)
    o = bpy.data.objects.new('t', cu); bpy.context.collection.objects.link(o); o.data.materials.append(m); return o


def rod(a, b, r, m):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=10); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y'); o.data.materials.append(m); o.visible_shadow = False


def dashed_h(x0, x1, z, r, m, y=-0.2, seg=0.16, gap=0.12):
    x = x0
    while x < x1: rod((x, y, z), (min(x + seg, x1), y, z), r, m); x += seg + gap


def ramp_x(z): return XB - z / SLOPE


def scene(k, after):
    D = BOARDS[k]['D'] * U; ans = lowest(BOARDS[k]['D'])
    floor = b3d.mat('floor', (0.06, 0.07, 0.11), rough=0.7, coat=0); track = b3d.mat('track', (0.2, 0.45, 0.95), rough=0.35, coat=0.3)
    leg = b3d.mat('leg', (0.14, 0.15, 0.2), rough=0.5, coat=0); grey = b3d.mat('grey', (0.6, 0.63, 0.7), rough=0.5, coat=0); glow(grey, (0.6, 0.63, 0.7), 0.9)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.5)
    amber = b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0.1); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    coral = b3d.mat('coral', (0.95, 0.35, 0.3), rough=0.35, coat=0.4)
    box(floor, (0.2, 0, -0.08), (7.8, 1.4, 0.16), 0.03)
    R0 = 0.5; zt = 9.6 * U
    pts = [(XT + (XB - R0 - XT) * i / 20, Y, zt - SLOPE * (XB - R0 - XT) * i / 20 + 0.06) for i in range(21)]
    a = math.atan(SLOPE)
    for i in range(1, 13):    # smooth bend into the flat
        f = i / 12; th = a * (1 - f); pts.append((XB - R0 + R0 * math.sin(a) * f * 1.6, Y, 0.06 + SLOPE * R0 * (1 - f) ** 2 * 0.5))
    xl = 1.4; pts.append((xl - 0.1, Y, 0.06))
    r = D / 2
    for i in range(0, 61):
        th = 2 * math.pi * i / 60
        pts.append((xl + r * math.sin(th), Y - 0.28 * i / 60, 0.06 + r - r * math.cos(th)))
    pts.append((xl + 1.3, Y - 0.28, 0.06))
    tube(pts, 0.05, mint if after else track)
    for x in (XT + 0.3, XT + 1.2, XT + 2.0): z = zt - SLOPE * (x - XT); box(leg, (x, Y + 0.25, z / 2), (0.06, 0.06, z), 0.01)
    for n in range(1, 10):
        z = n * U; x = ramp_x(z) - 0.38
        box(mint if (after and n == ans) else amber, (x, Y - 0.25, z), (0.36, 0.05, 0.3), 0.05); text(str(n), (x, Y - 0.29, z), 0.22, ink)
        box(grey, (ramp_x(z) - 0.12, Y - 0.1, z), (0.14, 0.02, 0.02), 0.0)
    dashed_h(ramp_x(D), xl + r + 0.3, D + 0.06, 0.016, grey)
    sz = ans * U if after else 9 * U
    sx = ramp_x(sz) + 0.12
    o = box(coral, (sx, Y, sz + 0.2), (0.34, 0.24, 0.16), 0.05); o.rotation_euler = (0, math.atan(SLOPE), 0)
    if after: dashed_h(ramp_x(1.25 * D), xl + r + 0.3, 1.25 * D + 0.06, 0.02, mint)
    b3d.stack_camera((-0.95, 0, 1.85), 7.2, az=0.0, el=6.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 900), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
