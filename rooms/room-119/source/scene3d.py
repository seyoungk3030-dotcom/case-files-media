"""ROOM 119 3D sprites: front view of a pendulum: a beam, a string from the pivot to a coral ball at the moment shown,
a faint dashed arc for the swing range, an amber arrow for the direction of motion, red scissors on the string, and
nine numbered slots on the floor. a*: the string is cut, a mint dashed path shows the flight, the ball lies in the
landing slot and that slot's tag turns mint."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, flight, P, L, W, X0, R
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
Y = -0.1


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def box(m, c, s, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def rod(a, b, r, m):
    a, b = Vector(a), Vector(b); d = b - a
    if d.length < 1e-4: return
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=10); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y'); o.data.materials.append(m); o.visible_shadow = False
    return o


def dashed(pts, r, m, on=1, off=1):
    for i in range(len(pts) - 1):
        if i % (on + off) < on: rod(pts[i], pts[i + 1], r, m)


def ball(c, m, r=R):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=c, segments=40, ring_count=20); o = bpy.context.object; o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = True


def scene(k, after):
    b = BOARDS[k]; t = math.radians(b['T']); land = RES[k][0]
    dark = b3d.mat('dark', (0.12, 0.13, 0.18), rough=0.5, coat=0.1); floor = b3d.mat('floor', (0.06, 0.07, 0.11), rough=0.7, coat=0)
    line = b3d.mat('line', (0.6, 0.63, 0.7), rough=0.5, coat=0); glow(line, (0.6, 0.63, 0.7), 0.7)
    string = b3d.mat('string', (0.9, 0.9, 0.85), rough=0.6, coat=0); coral = b3d.mat('coral', (0.95, 0.35, 0.3), rough=0.35, coat=0.4)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.5)
    amber = b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0.1); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    red = b3d.mat('red', (0.9, 0.15, 0.15), rough=0.4, coat=0.2); glow(red, (0.9, 0.15, 0.15), 0.8)
    box(dark, (0, 0, P + 0.12), (1.4, 0.4, 0.16), 0.03); bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.4, location=(0, 0, P), rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.materials.append(dark)
    t0 = math.radians(b['T0'])
    dashed([(L * math.sin(-t0 + 2 * t0 * i / 40), Y + 0.1, P - L * math.cos(-t0 + 2 * t0 * i / 40)) for i in range(41)], 0.015, line)
    bx, bz = L * math.sin(t), P - L * math.cos(t)
    # floor and slots
    box(floor, (0, 0, -0.08), (W * 9 + 0.6, 1.2, 0.16), 0.03)
    for i in range(10): box(dark, (X0 + i * W, 0, 0.12), (0.05, 1.0, 0.24), 0.01)
    for n in range(1, 10):
        cx = X0 + (n - 0.5) * W
        box(mint if (after and n == land) else amber, (cx, -0.62, -0.02), (0.42, 0.05, 0.36), 0.06); text(str(n), (cx, -0.66, -0.02), 0.26, ink)
    if not after:
        rod((0, Y, P), (bx, Y, bz), 0.018, string); ball((bx, Y, bz), coral)
        mx, mz = bx * 0.55, P - (P - bz) * 0.55
        for s in (-1, 1):
            o = box(red, (mx, Y - 0.15, mz), (0.42, 0.03, 0.06), 0.01); o.rotation_euler = (0, s * math.radians(45), 0)
        d = b['dir']; tx, tz = d * math.cos(t), d * math.sin(t)
        a0 = (bx + tx * 0.28, Y - 0.1, bz + tz * 0.28); a1 = (bx + tx * 0.62, Y - 0.1, bz + tz * 0.62)
        rod(a0, a1, 0.04, amber)
        bpy.ops.mesh.primitive_cone_add(radius1=0.11, depth=0.22, location=(bx + tx * 0.72, Y - 0.1, bz + tz * 0.72), vertices=24)
        o = bpy.context.object; o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((tx, 0, tz)).to_track_quat('Z', 'Y'); o.data.materials.append(amber)
    else:
        rod((0, Y, P), (bx * 0.55, Y, P - (P - bz) * 0.55), 0.018, string)
        path = flight(b); dashed([(x, Y, z) for x, z in path], 0.03, mint)
        ball((bx, Y, bz), line, R * 0.8); ball((path[-1][0], Y, R + 0.05), mint)
    b3d.stack_camera((0, 0, 2.15), 5.9, az=0.0, el=6.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 1000), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
