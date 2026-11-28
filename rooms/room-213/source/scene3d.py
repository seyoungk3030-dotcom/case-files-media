"""ROOM 213 3D sprites, centimetres: D cells (6.1 cm long, 3.4 cm across, 1.5 V like any alkaline cell) lie end to end in one open holder, in series.
The + end of a cell is the gold half with the small nub. A voltmeter above has its red lead on the right end plate and
its black lead on the left end plate. p*: the holder and a blank meter. a*: each cell gets a glowing strip under it,
mint for nub-to-the-right (+1.5 V) and coral for backwards (-1.5 V), and the meter screen lights mint.
Same camera for every board, so a longer row really is longer."""
import os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
L, R = 6.1, 1.7
K = L / 5.0   # cell parts were laid out for a 5 cm cell


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def box(m, loc, sc, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def rod(m, p, q, r, v=32):
    from mathutils import Vector
    d = Vector(q) - Vector(p); bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d.length, location=(Vector(p) + Vector(q)) / 2)
    o = bpy.context.object; o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d)
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def cell(M, x0, right):
    """One AA cell from x0 to x0 + L; right=True puts the + nub on the right."""
    z = R + 0.05; s = 1 if right else -1; c = x0 + L / 2
    rod(M['black'], (c - s * 2.45 * K, 0, z), (c + s * 0.2 * K, 0, z), R, 48)            # black (-) half
    rod(M['gold'], (c + s * 0.2 * K, 0, z), (c + s * 2.3 * K, 0, z), R, 48)              # gold (+) half
    rod(M['steel'], (c - s * 2.5 * K, 0, z), (c - s * 2.45 * K, 0, z), R * 0.92, 48)     # flat - cap
    rod(M['steel'], (c + s * 2.2 * K, 0, z), (c + s * 2.5 * K, 0, z), R * 0.3)           # + nub
    rod(M['steel'], (c + s * 2.28 * K, 0, z), (c + s * 2.32 * K, 0, z), R * 0.85, 48)    # + shoulder
    sign(M['white'], '+', c + s * 1.25 * K, z)
    sign(M['white'], '-', c - s * 1.25 * K, z)


def sign(m, t, x, z):
    """A printed sign on the side of the cell that faces the camera (26 degrees above the horizon)."""
    import math
    a = math.radians(26); d = (0, -math.cos(a), math.sin(a)); r = R + 0.035
    for sx, sz in ((1.6, 0.4), (0.4, 1.6)) if t == '+' else ((1.6, 0.4),):
        o = box(m, (x, d[1] * r, z + d[2] * r), (sx, 0.05, sz)); o.rotation_euler = (a, 0, 0)


def scene(key, after):
    s = BOARDS[key]; n = len(s)
    M = {'black': b3d.mat('black', (0.06, 0.07, 0.09), rough=0.35, coat=0.6), 'gold': b3d.mat('gold', (0.95, 0.62, 0.12), rough=0.3, metal=0.6, coat=0.4),
         'steel': b3d.mat('steel', (0.8, 0.82, 0.86), rough=0.2, metal=1.0, coat=0),
         'white': glowm('wsign', (1, 1, 1), 0.8, 0.5)}
    tray = b3d.mat('tray', (0.88, 0.89, 0.92), rough=0.5, coat=0.2); plate = b3d.mat('plate', (0.75, 0.77, 0.8), rough=0.25, metal=1.0, coat=0)
    red = b3d.mat('red', (0.85, 0.08, 0.08), rough=0.4, coat=0.3); blk = b3d.mat('blk', (0.08, 0.08, 0.1), rough=0.4, coat=0.3)
    mint = glowm('mint', (0.2, 0.95, 0.65), 2.5); coral = glowm('coral', (1.0, 0.35, 0.3), 2.5)
    W = n * L; xe = W / 2 + 0.35
    box(tray, (0, 0, -0.3), (W + 1.8, 4.4, 0.6), 0.15)
    for sgn in (-1, 1):
        box(tray, (sgn * (xe + 0.35), 0, 1.9), (0.5, 4.4, 4.4), 0.12)
        box(plate, (sgn * xe, 0, R + 0.05), (0.12, 2.6, 2.6), 0.03)
    for i, ch in enumerate(s):
        x0 = -W / 2 + i * L; cell(M, x0, ch == '+')
        if after: box(mint if ch == '+' else coral, (x0 + L / 2, -2.25, 0.02), (L - 0.8, 0.2, 0.3), 0.05)
    body = b3d.mat('meter', (0.98, 0.78, 0.15), rough=0.4, coat=0.4)
    box(body, (0, 0.4, 9.2), (9.0, 1.6, 3.8), 0.45)
    box(glowm('scr', (0.2, 0.95, 0.65), 1.2) if after else b3d.mat('scr', (0.16, 0.2, 0.18), rough=0.3, coat=0.5), (0, -0.45, 9.6), (6.6, 0.2, 1.9), 0.1)
    for sgn, m in ((1, red), (-1, blk)):
        p0 = (sgn * (xe + 0.65), 0, 3.6); p1 = (sgn * (xe + 0.65), 0, 6.0); p2 = (sgn * 4.4, 0.1, 7.8)
        rod(m, p0, p1, 0.22); rod(m, p1, p2, 0.22); rod(m, (sgn * 2.8, -0.2, 7.9), (sgn * 2.8, -0.2, 7.0), 0.4)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=p1); bpy.context.object.data.materials.append(m)
    b3d.stack_camera((0, 0, 5.0), 52.5, az=0.0, el=26.0)


only = sys.argv[1:]
for key in 'ABCD':
    for kind in 'pa':
        nm = kind + key
        if only and nm not in only: continue
        b3d.reset((900, 420), 48); b3d.lights(30)
        t0 = time.time(); scene(key, kind == 'a')
        b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t0, 1), flush=True)
