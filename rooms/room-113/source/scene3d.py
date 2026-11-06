"""ROOM 113 3D sprites: side view of a tall ruler (0-16) beside a floor. A coloured ball waits at its drop height
with a dashed drop line; the first bounce is drawn as a dashed arc with a thin guide line from its top to the ruler.
An amber sign asks for the k-th bounce. a*: the later bounces are drawn too; the asked one is mint, with a mint ball
at its top and a mint guide line to the ruler."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, H
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U, RAD, X0, Y = 0.3, 0.17, 0.45, -0.3
COL = {'coral': (0.95, 0.35, 0.3), 'blue': (0.2, 0.45, 0.95), 'amber': (0.95, 0.6, 0.08), 'green': (0.45, 0.8, 0.2)}


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m, ax='CENTER'):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = ax; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def box(m, c, s, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def rod(a, b, r, m):
    a, b = Vector(a), Vector(b); d = b - a
    if d.length < 1e-4: return
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=10); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y'); o.data.materials.append(m)
    o.visible_shadow = False


def dashed(pts, r, m, on=2, off=1):
    for i in range(len(pts) - 1):
        if i % (on + off) < on: rod(pts[i], pts[i + 1], r, m)


def ball(c, m, r=RAD):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=c, segments=40, ring_count=20); o = bpy.context.object; o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = True


def width(h): return 0.5 * math.sqrt(float(h))


def arc(x, h, n=36):
    w = width(h); return [(x + w * i / n, Y, RAD + float(h) * U * (1 - (2 * i / n - 1) ** 2)) for i in range(n + 1)], x + w


def scene(k, after):
    b = BOARDS[k]; hs = H[k]; ask = b['ask']
    floor = b3d.mat('floor', (0.07, 0.09, 0.15), rough=0.7, coat=0); pole = b3d.mat('pole', (0.03, 0.035, 0.05), rough=0.6, coat=0)
    tick = b3d.mat('tick', (0.8, 0.83, 0.9), rough=0.5, coat=0); glow(tick, (0.8, 0.83, 0.9), 1.5)
    line = b3d.mat('line', (0.85, 0.88, 0.95), rough=0.5, coat=0); glow(line, (0.85, 0.88, 0.95), 0.9)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.5)
    amber = b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0.1); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    bm = b3d.mat('ball', COL[b['color']], rough=0.35, coat=0.4)
    box(floor, (2.0, 0, -0.08), (6.4, 1.6, 0.16), 0.03)
    box(pole, (-0.55, 0, 16 * U / 2 + 0.25), (0.62, 0.3, 16 * U + 0.5), 0.04)
    for n in range(17):
        z = RAD + n * U
        box(tick, (-0.2, -0.16, z), (0.14 if n % 2 else 0.22, 0.02, 0.025), 0.0)
        text(str(n), (-0.62, -0.17, z), 0.2, tick)
    # drop
    top = RAD + b['drop'] * U
    dashed([(X0, Y, top - (top - RAD) * i / 24) for i in range(25)], 0.02, line)
    ball((X0, Y, top), bm)
    box(ink, (X0 + 0.75, Y - 0.05, top), (0.85, 0.04, 0.58), 0.08); text(str(b['drop']), (X0 + 0.75, Y - 0.09, top), 0.5, tick)
    x = X0; last = ask if after else 1
    for i in range(1, last + 1):
        pts, xn = arc(x, hs[i]); m = mint if (after and i == ask) else line
        dashed(pts, 0.03 if m is mint else 0.02, m)
        apex = (x + width(hs[i]) / 2, Y, RAD + float(hs[i]) * U)
        if i == 1 or (after and i == ask):
            dashed([(-0.2 + (apex[0] + 0.2) * j / 24, Y + 0.02, apex[2]) for j in range(25)], 0.014, m, 1, 1)
        if i == 1:
            box(ink, (apex[0] + 0.62, Y - 0.05, apex[2] + 0.3), (0.85, 0.04, 0.58), 0.08); text(str(hs[1]), (apex[0] + 0.62, Y - 0.09, apex[2] + 0.3), 0.5, tick)
        if after and i == ask: ball(apex, mint, RAD * 1.05)
        x = xn
    box(amber, (3.35, -0.2, 4.55), (2.2, 0.06, 0.8), 0.08); text(f'{ask}번째 튀면?', (3.35, -0.25, 4.55), 0.4, ink)
    b3d.stack_camera((1.85, 0, 2.7), 6.4, az=0.0, el=4.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 1000), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
