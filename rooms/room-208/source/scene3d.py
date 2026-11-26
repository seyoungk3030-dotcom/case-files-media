"""ROOM 208 3D sprites, true scale in metres: a playground swing frame whose top bar sits 0.5 m above the seat's lowest
point, chains of the board's length, and a sitting rider (child or adult, by size). p*: the swing pulled back to the push
angle, with an amber dotted arc to the other side. a*: the same arc in mint with the swing at the bottom. Each board is framed to fit (the chain length is
written under it)."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def box(m, loc, sc, bev=0.0, rot=(0, 0, 0), parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    if parent: o.parent = parent
    return o


def rod(m, p, q, r, parent=None):
    d = [b - a for a, b in zip(p, q)]; ln = math.sqrt(sum(x * x for x in d))
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=ln, location=[(a + b) / 2 for a, b in zip(p, q)]); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; from mathutils import Vector; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(d))
    o.data.materials.append(m); bpy.ops.object.shade_smooth()
    if parent: o.parent = parent
    return o


def ball(m, loc, r, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc); o = bpy.context.object; o.data.materials.append(m); bpy.ops.object.shade_smooth()
    if parent: o.parent = parent
    return o


def scene(key, after):
    who, mass, L, deg = BOARDS[key]; H = L + 0.5; th = math.radians(deg)
    frame = b3d.mat('frame', (0.95, 0.45, 0.2), rough=0.4, coat=0.3); chain = b3d.mat('chain', (0.75, 0.77, 0.8), rough=0.3, metal=0.9, coat=0)
    seat = b3d.mat('seat', (0.15, 0.55, 0.95), rough=0.5, coat=0.2)
    skin = glowm('skin', (0.95, 0.75, 0.6), 0.3, 0.6); shirt = glowm('shirt', (0.95, 0.8, 0.2) if who == '어린이' else (0.35, 0.8, 0.45), 0.3, 0.6)
    pants = b3d.mat('pants', (0.18, 0.2, 0.3), rough=0.7, coat=0)
    for y in (-0.9, 0.9):
        rod(frame, (0, y, H), (0, y * 1.25, 0), 0.06)
        for sx in (-1, 1): rod(frame, (0, y * 1.25, 0), (sx * 0.6, y * 1.25, 0.02), 0.05)
    rod(frame, (0, -1.0, H), (0, 1.0, H), 0.07)
    piv = bpy.data.objects.new('piv', None); bpy.context.collection.objects.link(piv); piv.location = (0, 0, H)
    for y in (-0.25, 0.25): rod(chain, (0, y, 0), (0, y, -L), 0.015, parent=piv)
    box(seat, (0, 0, -L), (0.45, 0.6, 0.05), 0.02, parent=piv)
    s = 0.62 if who == '어린이' else 1.0
    box(shirt, (-0.05 * s, 0, -L + 0.33 * s), (0.28 * s, 0.38 * s, 0.6 * s), 0.08 * s, parent=piv)
    ball(skin, (-0.05 * s, 0, -L + 0.8 * s), 0.15 * s, parent=piv)
    for y in (-0.1, 0.1):
        rod(pants, (-0.05 * s, y * s, -L + 0.08 * s), (0.4 * s, y * s, -L + 0.08 * s), 0.065 * s, parent=piv)
        rod(pants, (0.4 * s, y * s, -L + 0.08 * s), (0.45 * s, y * s, -L - 0.38 * s), 0.06 * s, parent=piv)
    piv.rotation_euler = (0, 0 if after else th, 0)
    dot = glowm('arc', (0.15, 0.9, 0.6) if after else (1.0, 0.7, 0.15), 1.2)
    n = 15
    for i in range(n + 1):
        a = -th + 2 * th * i / n; ball(dot, ((L + 0.12) * math.sin(a), -0.75, H - (L + 0.12) * math.cos(a)), 0.045)
    box(b3d.mat('ground', (0.35, 0.55, 0.3), rough=0.9, coat=0), (0, 0, -0.03), (4.6, 3.2, 0.06), 0.02)
    b3d.stack_camera((0, 0, H / 2 + 0.05), (H + 0.7) * 1.3, az=10.0, el=10.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((760, 760), 48); b3d.lights(6)
        t0 = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t0, 1), flush=True)
