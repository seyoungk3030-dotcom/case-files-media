"""ROOM 136 3D sprites: a three-lane ramp sloping down to the right with a finish line; in each lane an object (iron
ring, wooden ball, wooden cylinder, hollow plastic ball or ice block) with a number chip and a name/weight label.
p*: everything at the start line. a*: the moment the winner crosses the finish (others placed by their acceleration
1/(1+k)), the winner's chip glows mint."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, K
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
AZ, EL, LEN, TH, X0, XF = 28.0, 30.0, 5.2, math.radians(16), 0.45, 4.6
NAME = {'ring': '쇠고리', 'ball': '나무 공', 'cyl': '나무 원기둥', 'shell': '속 빈 공', 'ice': '얼음 조각'}


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def facing(): return (math.radians(90 - EL), 0, math.radians(AZ))


def cam_dir(): return Vector((math.sin(math.radians(AZ)) * math.cos(math.radians(EL)), -math.cos(math.radians(AZ)) * math.cos(math.radians(EL)), math.sin(math.radians(EL))))


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=facing()); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


DIR = Vector((0, -math.cos(TH), -math.sin(TH))); NRM = Vector((0, -math.sin(TH), math.cos(TH))); TOP = Vector((0, 0, LEN * math.sin(TH) + 0.25))


def surf(s, y): return TOP + DIR * s + Vector((y, 0, 0))


def obj(o, s, y, after, mats):
    kind = o['kind']; r = 0.12 + 0.2 * o['size']; c = surf(s, y) + NRM * (r if kind != 'ice' else r * 0.8)
    if kind == 'ring':
        bpy.ops.mesh.primitive_torus_add(location=c, rotation=(0, math.radians(90), 0), major_radius=r - 0.05, minor_radius=0.05, major_segments=48); bpy.context.object.data.materials.append(mats['iron'])
    elif kind in ('ball', 'shell'):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=c, segments=48, ring_count=24); ob = bpy.context.object; ob.data.materials.append(mats['wood' if kind == 'ball' else 'shell'])
        for p in ob.data.polygons: p.use_smooth = True
        if kind == 'shell':
            bpy.ops.mesh.primitive_torus_add(location=c, rotation=(0, math.radians(90), 0), major_radius=r, minor_radius=0.025); bpy.context.object.data.materials.append(mats['iron'])
    elif kind == 'cyl':
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=0.5, location=c, rotation=(0, math.radians(90), 0), vertices=48); bpy.context.object.data.materials.append(mats['wood'])
    else:
        bpy.ops.mesh.primitive_cube_add(size=1.6 * r, location=c, rotation=(TH, 0, 0)); ob = bpy.context.object; ob.data.materials.append(mats['ice']); b3d.bevel(ob, 0.04)
    return c, r


def scene(k, after):
    b = BOARDS[k]; kw = min(K[o['kind']] for o in b)
    mats = {'iron': b3d.mat('iron', (0.4, 0.42, 0.46), rough=0.3, metal=0.9, coat=0), 'wood': b3d.mat('wood', (0.8, 0.55, 0.28), rough=0.5, coat=0.2),
            'shell': b3d.mat('shell', (0.95, 0.4, 0.55), rough=0.2, coat=0.6), 'ice': b3d.mat('ice', (0.75, 0.9, 1.0), rough=0.1, coat=0.5)}
    mats['ice'].node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.6
    ramp = b3d.mat('ramp', (0.07, 0.085, 0.13), rough=0.6, coat=0); lane = b3d.mat('lane', (0.45, 0.5, 0.6), rough=0.5, coat=0)
    chip = b3d.mat('chip', (0.94, 0.95, 0.97), rough=0.5, coat=0); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    white = b3d.mat('white', (0.92, 0.93, 0.96), rough=0.5, coat=0); glow(white, (0.92, 0.93, 0.96), 0.4)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.6); amber = b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0)
    mid = surf(LEN / 2, 0) - NRM * 0.08
    bpy.ops.mesh.primitive_cube_add(size=1, location=mid, rotation=(TH, 0, 0)); o = bpy.context.object; o.scale = (3.0, LEN, 0.16); o.data.materials.append(ramp)
    for y in (-0.5, 0.5):
        bpy.ops.mesh.primitive_cube_add(size=1, location=surf(LEN / 2, y) + NRM * 0.02, rotation=(TH, 0, 0)); o = bpy.context.object; o.scale = (0.03, LEN, 0.04); o.data.materials.append(lane)
    for s_, m_ in ((X0 - 0.3, amber), (XF, white)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=surf(s_, 0) + NRM * 0.01, rotation=(TH, 0, 0)); o = bpy.context.object; o.scale = (3.0, 0.06, 0.02); o.data.materials.append(m_)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.25, TOP.z / 2 - 0.1)); o = bpy.context.object; o.scale = (3.0, 0.5, TOP.z - 0.2); o.data.materials.append(lane)
    for i, o in enumerate(b):
        y = (i - 1) * 1.0; s = X0 + ((XF - X0) * (1 + kw) / (1 + K[o['kind']]) if after else 0)
        c, r = obj(o, s, y, after, mats)
        cp = c + Vector((0, 0, r + 0.42)); hit = after and K[o['kind']] == kw
        bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.05, location=cp, rotation=facing(), vertices=32); bpy.context.object.data.materials.append(mint if hit else chip)
        text(str(o['n']), cp + cam_dir() * 0.03, 0.27, ink)
        if not after: text(f"{NAME[o['kind']]} {o['kg']:g}kg", cp + Vector((0, 0, 0.36)), 0.15, white)
    b3d.stack_camera((0, -2.0, 1.25), 7.4, az=AZ, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 640), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
