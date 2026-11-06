"""ROOM 134 3D sprites: seen from above at a slant, a ball runs round a circular double-rail track with a gap; four
numbered pins stand outside the gap. p*: the ball on the track with an amber arrow showing which way it runs. a*: a
mint dotted line from the exit point straight along the tangent to the pin it hits, which glows."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, R, pins
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
AZ, EL, GAP, W = 0.0, 58.0, 55, 0.17


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


def arc(rr, a0, a1, z, m, n=64):
    pts = [Vector((rr * math.cos(math.radians(a0 + (a1 - a0) * i / n)), rr * math.sin(math.radians(a0 + (a1 - a0) * i / n)), z)) for i in range(n + 1)]
    for p, q in zip(pts, pts[1:]): rod(p, q, 0.035, m, 8)


def scene(k, after):
    b = BOARDS[k]; s = b['dir']; ex = b['exit']; P, Q = pins(b); P = Vector((*P, 0.12))
    floor = b3d.mat('floor', (0.035, 0.04, 0.06), rough=0.9, coat=0); rail = b3d.mat('rail', (0.75, 0.77, 0.82), rough=0.3, metal=0.9, coat=0)
    ball = b3d.mat('ball', (0.9, 0.2, 0.18), rough=0.25, coat=0.6); chip = b3d.mat('chip', (0.94, 0.95, 0.97), rough=0.5, coat=0)
    ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0); post = b3d.mat('post', (0.35, 0.37, 0.42), rough=0.4, metal=0.5, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.6)
    amber = b3d.mat('amber', (0.95, 0.55, 0.06), rough=0.5, coat=0); glow(amber, (0.95, 0.55, 0.06), 0.6)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.06)); o = bpy.context.object; o.scale = (7.6, 7.6, 0.12); o.data.materials.append(floor); b3d.bevel(o, 0.1)
    a0, a1 = (ex, ex - 360 + GAP) if s == 1 else (ex, ex + 360 - GAP)
    for rr in (R - W, R + W): arc(rr, a1, a0, 0.12, rail, 96)
    if after:
        t = (Vector((*Q['tangent'], 0.12)) - P).normalized(); L = (Vector((*Q['tangent'], 0.12)) - P).length - 0.35
        for i in range(int(L / 0.18)): bpy.ops.mesh.primitive_uv_sphere_add(radius=0.045, location=P + t * (0.1 + 0.18 * i)); bpy.context.object.data.materials.append(mint)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.17, location=P + t * (L - 0.05) + Vector((0, 0, 0.01))); o = bpy.context.object; o.data.materials.append(ball)
        for p in o.data.polygons: p.use_smooth = True
    else:
        ab = math.radians(ex - s * 110); bp = Vector((R * math.cos(ab), R * math.sin(ab), 0.13))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.17, location=bp); o = bpy.context.object; o.data.materials.append(ball)
        for p in o.data.polygons: p.use_smooth = True
        td = Vector((-s * math.sin(ab), s * math.cos(ab), 0)); c = bp + td * 0.45 + Vector((0, 0, 0.12))
        rod(c - td * 0.18, c + td * 0.12, 0.035, amber)
        bpy.ops.mesh.primitive_cone_add(radius1=0.09, depth=0.18, location=c + td * 0.2); o = bpy.context.object; o.data.materials.append(amber)
        o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = td.to_track_quat('Z', 'Y')
    for kind, q in Q.items():
        hit = after and kind == 'tangent'; c = Vector((*q, 0))
        rod(c, c + Vector((0, 0, 0.4)), 0.08, post)
        tc = c + Vector((0, 0, 0.62))
        bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.05, location=tc, rotation=facing(), vertices=32); bpy.context.object.data.materials.append(mint if hit else chip)
        text(str(b['pins'][kind]), tc + cam_dir() * 0.03, 0.36, ink)
    b3d.stack_camera((0, 0, 0.2), 7.9, az=AZ, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
