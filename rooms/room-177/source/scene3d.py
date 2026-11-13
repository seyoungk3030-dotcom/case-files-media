"""ROOM 177 3D sprites, side view at sea: either a ship with a rope ladder hanging down its hull, or a stone pier with a
steel ladder bolted to it. Rungs every 30 cm, the sea is see-through so rungs under water show tinted, and a sign says
how far the tide will rise. p*: now. a*: after the tide: the sea is higher (white line = old level), the ship has risen
with it, rungs under water glow mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GAP, rungs
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
Z0 = -1.4  # sea floor


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def box(loc, scale, m, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def bar(a, b, r, m, verts=16):
    d = [b[i] - a[i] for i in range(3)]; ln = math.sqrt(sum(x * x for x in d))
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=ln, location=tuple((a[i] + b[i]) / 2 for i in range(3)), vertices=verts)
    o = bpy.context.object; o.rotation_mode = 'QUATERNION'
    from mathutils import Vector
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(d).normalized()); o.data.materials.append(m); return o


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def scene(k, after):
    holder, under, tide = BOARDS[k]
    sea = b3d.mat('sea', (0.1, 0.45, 0.75), rough=0.1, coat=0.3); sea.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.3
    hull = b3d.mat('hull', (0.75, 0.15, 0.15), rough=0.4, coat=0.4); deck = b3d.mat('deck', (0.95, 0.95, 0.93), rough=0.5, coat=0.2)
    stone = b3d.mat('stone', (0.34, 0.34, 0.37), rough=0.85, coat=0); steel = b3d.mat('steel', (0.75, 0.77, 0.8), rough=0.3, metal=0.8)
    rope = b3d.mat('rope', (0.85, 0.72, 0.45), rough=0.8, coat=0); wood = b3d.mat('wood', (0.6, 0.4, 0.22), rough=0.6, coat=0.2)
    sign = b3d.mat('sign', (0.04, 0.045, 0.06), rough=0.4, coat=0.3); yel = glowm('yel', (1.0, 0.8, 0.2), 1.6)
    mint = glowm('mint', (0.15, 0.85, 0.6), 2.0); white = glowm('white', (1, 1, 1), 1.5); sand = b3d.mat('sand', (0.7, 0.62, 0.45), rough=0.9, coat=0)
    water = tide / 100 if after else 0.0; lift = tide / 100 if (after and holder == 'ship') else 0.0
    hs = [h / 100 + lift for h in rungs(under)]
    box((0, 0.3, Z0 - 0.05), (3.2, 1.6, 0.1), sand)
    if holder == 'ship':
        top = 0.95 + lift
        box((0, 0.6, (lift - 0.75 + top) / 2), (2.0, 1.1, top - (lift - 0.75)), hull, 0.06)
        box((0, 0.6, top + 0.04), (2.05, 1.15, 0.08), deck)
        box((0.45, 0.6, top + 0.25), (0.8, 0.6, 0.36), deck, 0.05)
        rail, rr, rm = rope, 0.02, wood
    else:
        top = 1.15
        box((0, 0.6, (Z0 + top) / 2), (2.0, 1.1, top - Z0), stone, 0.04)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.25, location=(0.6, 0.45, top + 0.12)); bpy.context.object.data.materials.append(steel)
        rail, rr, rm = steel, 0.028, steel
    for sx in (-0.27, 0.27): bar((sx, -0.02, min(hs) - 0.08), (sx, -0.02, top), rr, rail)
    for h in hs:
        if h > top - 0.05: continue
        bar((-0.27, -0.03, h), (0.27, -0.03, h), 0.03, mint if (after and h < water) else rm)
    box((0, 0.3, (Z0 + water) / 2), (3.2, 1.6, water - Z0), sea)
    if after: box((0, -0.52, 0.0), (3.2, 0.01, 0.025), white)
    box((0, 0.3, 2.3), (1.9, 0.08, 0.5), sign, 0.04)
    text(f'밀물 +{tide}cm', (0, 0.22, 2.3), 0.28, yel)
    b3d.stack_camera((0, 0, 0.55), 4.02, az=0.0, el=8.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((800, 1000), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
