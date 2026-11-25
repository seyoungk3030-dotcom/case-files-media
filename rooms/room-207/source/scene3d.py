"""ROOM 207 3D sprites: a side view of an escalator, one unit = one 40 cm tread, rise 0.58 (about 30 degrees), with a
person to true scale (1.7 m = 4.25 units). p*: the person stands on the bottom landing. a*: the person is on the top
landing and the treads they stepped on glow mint; seen from the ground those footsteps fall every (w+e)/w treads, so
there are exactly w*N/(w+e) of them, the proven digit. Same camera for every board so the reel keeps one scale."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
R = 0.58


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def box(m, loc, sc, bev=0.0, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def cyl(m, loc, r, d, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, rotation=rot); o = bpy.context.object; o.data.materials.append(m)
    return o


def person(x, z):
    skin = glowm('skin', (0.95, 0.75, 0.6), 0.35, 0.6); shirt = glowm('shirt', (0.25, 0.55, 0.95), 0.35, 0.6)
    pants = b3d.mat('pants', (0.18, 0.2, 0.3), rough=0.7, coat=0)
    for dx in (-0.22, 0.22): cyl(pants, (x + dx * 0.6, 0.0, z + 1.0), 0.2, 2.0)
    box(shirt, (x, 0, z + 2.75), (0.8, 0.9, 1.6), 0.25)
    for dy in (-0.55, 0.55): cyl(shirt, (x + 0.05, dy, z + 2.6), 0.14, 1.4)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.42, location=(x, 0, z + 3.9)); o = bpy.context.object; o.data.materials.append(skin)
    bpy.ops.object.shade_smooth()


def scene(key, after):
    N, w, e = BOARDS[key]; s = GOOD[key]
    metal = b3d.mat('metal', (0.72, 0.75, 0.8), rough=0.3, metal=0.7, coat=0); tread = b3d.mat('tread', (0.6, 0.63, 0.68), rough=0.5, metal=0.4, coat=0)
    side = b3d.mat('side', (0.3, 0.33, 0.4), rough=0.5, coat=0); rail = b3d.mat('rail', (0.08, 0.08, 0.1), rough=0.4, coat=0.3)
    land = b3d.mat('land', (0.62, 0.6, 0.56), rough=0.7, coat=0); mint = glowm('mint', (0.2, 0.95, 0.65), 2.5)
    yel = glowm('yel', (1.0, 0.8, 0.15), 0.6)
    top = (N + 1) * R
    box(land, (-1.6, 0, -0.3), (3.2, 2.6, 0.6), 0.05)
    box(land, (N + 1.6, 0, top - 0.3), (3.2, 2.6, 0.6), 0.05)
    lit = {math.ceil(k * (w + e) / w) - 1 for k in range(1, s + 1)} if after else set()
    assert not after or len(lit) == s
    for i in range(N):
        z = (i + 1) * R
        box(tread, (i + 0.5, 0, z - 0.06), (0.96, 2.0, 0.12), 0.02)
        box(yel, (i + 0.07, 0, z + 0.005), (0.1, 2.0, 0.03), 0)
        box(metal, (i + 0.98, 0, z - R / 2), (0.05, 2.0, R), 0)          # riser
        if i in lit: box(mint, (i + 0.5, 0, z + 0.02), (0.8, 1.6, 0.05), 0.01)
    a = math.atan2(R, 1.0); L = math.hypot(N + 0.6, (N + 0.6) * R)
    box(side, ((N) / 2, 1.15, (N + 1) * R / 2 + 0.2), (L, 0.18, 1.3), 0.05, rot=(0, -a, 0))
    box(side, ((N) / 2, 0, (N + 1) * R / 2 - 1.2), (L, 2.4, 0.9), 0.05, rot=(0, -a, 0))
    for y in (-1.15, 1.15):
        box(rail, ((N) / 2, y, (N + 1) * R / 2 + 1.9), (L + 1.6, 0.22, 0.16), 0.05, rot=(0, -a, 0))
        for xx in (-0.6, N + 0.6):
            zz = 0 if xx < 0 else top; cyl(side, (xx, y, zz + 1.0), 0.09, 2.0)
    if after: person(N + 1.4, top)
    else: person(-1.4, 0.0)
    b3d.stack_camera((7.5, 0, 5.6), 22.0, az=16.0, el=30.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((900, 760), 48); b3d.lights(18)
        t0 = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t0, 1), flush=True)
