"""ROOM 138 3D sprites: seen from above at a slant, a blue river between two grassy banks; a boat with the farmer and
`cap` empty seats waits at the left bank; the items stand on the left bank as coloured name chips, with amber arrows
from eater to eaten. p*: everyone on the left. a*: everyone (farmer and boat too) safely on the right bank, chips mint."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
AZ, EL = 0.0, 52.0
COL = {'늑대': (0.55, 0.58, 0.65), '염소': (0.95, 0.95, 0.92), '양배추': (0.45, 0.8, 0.35), '고양이': (0.95, 0.6, 0.25), '쥐': (0.75, 0.72, 0.7),
       '쌀': (0.95, 0.9, 0.75), '여우': (0.95, 0.45, 0.15), '닭': (0.98, 0.85, 0.4), '옥수수': (0.98, 0.8, 0.2), '수박': (0.3, 0.7, 0.35)}


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def facing(): return (math.radians(90 - EL), 0, math.radians(AZ))


def cam_dir(): return Vector((math.sin(math.radians(AZ)) * math.cos(math.radians(EL)), -math.cos(math.radians(AZ)) * math.cos(math.radians(EL)), math.sin(math.radians(EL))))


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=facing()); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def rod(a, b, r, m, v=12):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=v); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y'); o.data.materials.append(m); return o


def box(m, c, s, bev=0.03):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev)
    return o


def token(name, c, m, ink, ring=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=0.08, location=c, rotation=facing(), vertices=40); bpy.context.object.data.materials.append(m)
    if ring:
        bpy.ops.mesh.primitive_torus_add(location=c - cam_dir() * 0.02, rotation=facing(), major_radius=0.46, minor_radius=0.04); bpy.context.object.data.materials.append(ring)
    text(name, c + cam_dir() * 0.05, 0.27 if len(name) < 3 else 0.21, ink)


def scene(k, after):
    b = BOARDS[k]; items = b['items']; n = len(items)
    grass = b3d.mat('grass', (0.03, 0.09, 0.05), rough=0.9, coat=0); water = b3d.mat('water', (0.02, 0.1, 0.3), rough=0.15, coat=0.3)
    wood = b3d.mat('wood', (0.6, 0.38, 0.18), rough=0.6, coat=0); seat = b3d.mat('seat', (0.85, 0.75, 0.55), rough=0.6, coat=0)
    ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0); amber = b3d.mat('amber', (0.95, 0.5, 0.05), rough=0.5, coat=0); glow(amber, (0.95, 0.5, 0.05), 0.5)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.4); farmer = b3d.mat('farmer', (0.25, 0.5, 0.95), rough=0.5, coat=0)
    H = 1.35 * n + 1.0
    box(grass, (-2.45, 0, -0.15), (2.3, H, 0.3)); box(grass, (2.45, 0, -0.15), (2.3, H, 0.3)); box(water, (0, 0, -0.22), (2.6, H, 0.16), 0.0)
    side = 1 if after else -1; bx = side * 0.75
    box(wood, (bx, -H / 2 + 0.9, 0.0), (1.0, 2.0 + 0.3 * b['cap'], 0.22), 0.08)
    for i in range(b['cap']): box(seat, (bx, -H / 2 + 0.75 - 0.6 * i + 0.3 * b['cap'], 0.14), (0.7, 0.32, 0.06), 0.02)
    fp = Vector((bx, -H / 2 + 1.5 + 0.3 * b['cap'], 0.6))
    bpy.ops.mesh.primitive_cone_add(radius1=0.28, depth=0.6, location=fp + Vector((0, 0, -0.1))); bpy.context.object.data.materials.append(farmer)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=fp + Vector((0, 0, 0.32))); o = bpy.context.object; o.data.materials.append(seat)
    for p in o.data.polygons: p.use_smooth = True
    pos = {}
    for i, it in enumerate(items):
        y = (n - 1) / 2 * 1.35 - i * 1.35 + 0.4; c = Vector((side * 2.55, y, 0.5)); pos[it] = c
        m = b3d.mat(f't{i}', COL[it], rough=0.5, coat=0); token(it, c, m, ink, mint if after else None)
    if not after:
        for a, bb in b['eats']:
            p, q = pos[a], pos[bb]; d = (q - p).normalized(); s0 = p + d * 0.45 + Vector((0.72, 0, 0)); s1 = q - d * 0.62 + Vector((0.72, 0, 0))
            rod(s0, s1, 0.055, amber)
            bpy.ops.mesh.primitive_cone_add(radius1=0.16, depth=0.3, location=s1 + d * 0.1); o = bpy.context.object; o.data.materials.append(amber)
            o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y')
    b3d.stack_camera((0, 0, 0.2), max(8.4, H * 1.15), az=AZ, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
