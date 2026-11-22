"""ROOM 204 3D sprites: a side view of a field. Left: a small house and a person counting. Right: a storm cloud with a
lightning bolt hitting a tree. The strike sits 0.38 scene units per second of delay from the person, so the drawings
keep true proportion to each other (all boards share one camera). a*: a mint ruler on the ground with the distance."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, km
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
XP, SC = -2.7, 0.38


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def box(m, loc, sc, bev=0.03, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def seg(m, p, q, w):
    dx, dz = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dz)
    box(m, ((p[0] + q[0]) / 2, -0.1, (p[1] + q[1]) / 2), (w, w, L + w * 0.8), 0, rot=(0, math.atan2(dx, dz), 0))


def ball(m, loc, r):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=32, ring_count=16); o = bpy.context.object
    o.data.materials.append(m); [setattr(p, 'use_smooth', True) for p in o.data.polygons]; return o


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.pi / 2, 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def scene(key, after):
    t = BOARDS[key]; xb = XP + SC * t
    grass = b3d.mat('grass', (0.18, 0.42, 0.2), rough=0.8, coat=0)
    box(grass, (0, 0, -0.08), (7.2, 1.2, 0.16), 0.03)
    # house
    box(b3d.mat('wallh', (0.92, 0.85, 0.72), rough=0.6, coat=0), (XP - 0.55, 0.15, 0.3), (0.6, 0.5, 0.6), 0.02)
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.5, radius2=0, depth=0.4, location=(XP - 0.55, 0.15, 0.8), rotation=(0, 0, math.pi / 4))
    bpy.context.object.data.materials.append(b3d.mat('roof', (0.75, 0.22, 0.18), rough=0.5, coat=0.2))
    box(glowm('win', (1.0, 0.8, 0.4), 1.2), (XP - 0.55, -0.11, 0.35), (0.18, 0.02, 0.18), 0)
    # person
    skin = b3d.mat('skin', (0.95, 0.75, 0.6), rough=0.5, coat=0); coat = b3d.mat('coat', (0.2, 0.45, 0.9), rough=0.5, coat=0.2)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.42, location=(XP, -0.1, 0.21)); bpy.context.object.data.materials.append(coat)
    ball(skin, (XP, -0.1, 0.52), 0.1)
    box(coat, (XP + 0.1, -0.1, 0.36), (0.18, 0.05, 0.05), 0.0, rot=(0, -0.6, 0))
    ball(glowm('watch', (1.0, 0.75, 0.2), 1.0), (XP + 0.2, -0.12, 0.43), 0.05)
    # cloud and bolt
    cl = b3d.mat('cloud', (0.09, 0.1, 0.14), rough=0.9, coat=0)
    for dx, dz, r in ((-0.5, 0.0, 0.32), (-0.1, 0.12, 0.42), (0.35, 0.05, 0.36), (0.7, -0.05, 0.26), (0.1, -0.1, 0.3)):
        ball(cl, (xb + dx, 0.1, 2.35 + dz), r)
    pts = [(xb + 0.05, 2.1), (xb - 0.18, 1.55), (xb + 0.12, 1.4), (xb - 0.12, 0.8), (xb + 0.08, 0.68), (xb - 0.02, 0.35)]
    bolt = glowm('bolt', (1.0, 0.78, 0.1), 1.3)
    for p, q in zip(pts, pts[1:]): seg(bolt, p, q, 0.07)
    # tree hit
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.3, location=(xb, 0.0, 0.15)); bpy.context.object.data.materials.append(b3d.mat('trunk', (0.4, 0.25, 0.12), rough=0.7, coat=0))
    ball(b3d.mat('leaf', (0.12, 0.35, 0.16), rough=0.7, coat=0), (xb, 0.0, 0.38), 0.17)
    if after:
        mint = glowm('mint', (0.2, 0.95, 0.65), 2.0)
        box(mint, ((XP + xb) / 2, -0.5, 0.03), (xb - XP, 0.06, 0.04), 0.0)
        for x in (XP, xb): box(mint, (x, -0.5, 0.1), (0.04, 0.06, 0.2), 0.0)
    b3d.stack_camera((0, 0, 1.2), 7.4, az=0.0, el=8.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((900, 420), 40); b3d.lights(3)
        t0 = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t0, 1), flush=True)
