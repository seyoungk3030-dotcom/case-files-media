"""ROOM 124 3D sprites: front view of a Newton's cradle: a dark frame, n steel balls on strings, each with an amber
number tag. p*: k balls are pulled out to the left and j to the right (raised along their swing). a*: after the
hits, j balls are out on the left and k on the right; the innermost right one gets a mint ring."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
R, LS, ZP, SW = 0.3, 2.2, 3.0, math.radians(38)


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
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=8); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y'); o.data.materials.append(m)


def scene(k, after):
    b = BOARDS[k]; nums = b['nums']; n = len(nums); kl, jr = b['left'], b['right']; ans_pos = n - kl
    frame = b3d.mat('frame', (0.12, 0.13, 0.18), rough=0.4, metal=0.4, coat=0.1); steel = b3d.mat('steel', (0.8, 0.82, 0.86), rough=0.3, metal=0.85, coat=0)
    string = b3d.mat('string', (0.85, 0.86, 0.9), rough=0.6, coat=0); amber = b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0.1)
    ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0); mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.5)
    base = b3d.mat('base', (0.08, 0.09, 0.13), rough=0.6, coat=0)
    span = 2 * R * n; x0 = -span / 2 + R
    box(base, (0, 0, -0.1), (span + 4.6, 1.6, 0.2), 0.05)
    for sx in (-1, 1):
        box(frame, (sx * (span / 2 + 1.8), 0, ZP / 2), (0.1, 0.1, ZP + 0.2), 0.02)
    box(frame, (0, 0, ZP + 0.05), (span + 3.7, 0.12, 0.1), 0.02)
    left_up = set(range(jr)) if after else set(range(kl)); right_up = set(range(n - kl, n)) if after else set(range(n - jr, n))
    for i, num in enumerate(nums):
        px = x0 + 2 * R * i; ang = -SW if i in left_up else (SW if i in right_up else 0.0)
        cx, cz = px + LS * math.sin(ang), ZP - LS * math.cos(ang)
        rod((px, 0, ZP), (cx, 0, cz), 0.012, string)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=R, location=(cx, 0, cz), segments=48, ring_count=24); o = bpy.context.object; o.data.materials.append(steel)
        for p in o.data.polygons: p.use_smooth = True
        bpy.ops.mesh.primitive_cylinder_add(radius=0.16, depth=0.04, location=(cx, -R - 0.01, cz), rotation=(math.radians(90), 0, 0), vertices=32)
        bpy.context.object.data.materials.append(amber); text(str(num), (cx, -R - 0.04, cz), 0.22, ink)
        if after and i == ans_pos:
            bpy.ops.mesh.primitive_torus_add(location=(cx, -0.05, cz), rotation=(math.radians(90), 0, 0), major_radius=R + 0.07, minor_radius=0.035)
            bpy.context.object.data.materials.append(mint)
    b3d.stack_camera((0, 0, 1.75), 8.8, az=0.0, el=4.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 720), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
