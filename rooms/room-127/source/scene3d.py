"""ROOM 127 3D sprites: a cardboard box with a unit grid, an ant at the front-bottom-left corner and a sugar cube at
the back-top-right corner. Four coloured routes over the front, top and right faces, each with a number badge.
p*: all four routes. a*: the shortest route glows mint, the others turn grey."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, lengths
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
AZ, EL = 33.0, 30.0
COLS = [(0.95, 0.55, 0.08), (0.95, 0.25, 0.3), (0.25, 0.55, 1.0), (0.7, 0.35, 0.95)]


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - EL), 0, math.radians(AZ))); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def rod(a, b, r, m):
    a, b = Vector(a), Vector(b); d = b - a
    if d.length < 1e-6: return
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=12); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y'); o.data.materials.append(m)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=b, segments=12, ring_count=8); bpy.context.object.data.materials.append(m)


def routes(x, y, z):
    return [[(0, 0, 0), (x * z / (y + z), 0, z), (x, y, z)], [(0, 0, 0), (x, 0, z * x / (x + y)), (x, y, z)],
            [(0, 0, 0), (x, 0, z), (x, y, z)], [(0, 0, 0), (0, 0, z), (x, y, z)]]


def lift(p, x, y, z, e):
    o = [0.0, 0.0, 0.0]
    if abs(p[1]) < 1e-6: o[1] -= e
    if abs(p[2] - z) < 1e-6: o[2] += e
    if abs(p[0] - x) < 1e-6: o[0] += e
    if abs(p[0]) < 1e-6 and abs(p[1]) < 1e-6: o[0] -= e
    return tuple(a + b for a, b in zip(p, o))


def mid(pts, f):
    segs = [(Vector(a), Vector(b)) for a, b in zip(pts, pts[1:])]; tot = sum((b - a).length for a, b in segs); h = tot * f
    for a, b in segs:
        if h <= (b - a).length: return a + (b - a) * (h / (b - a).length)
        h -= (b - a).length


def scene(k, after):
    bd = BOARDS[k]; x, y, z = bd['size']; L = lengths(x, y, z); best = min(range(4), key=L.__getitem__)
    card = b3d.mat('card', (0.78, 0.6, 0.38), rough=0.75, coat=0); line = b3d.mat('line', (0.42, 0.3, 0.17), rough=0.8, coat=0)
    ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0); white = b3d.mat('sugar', (0.97, 0.97, 0.95), rough=0.5, coat=0)
    grey = b3d.mat('grey', (0.45, 0.47, 0.52), rough=0.6, coat=0); mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.0)
    base = b3d.mat('base', (0.08, 0.09, 0.13), rough=0.6, coat=0)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x / 2, y / 2, z / 2)); o = bpy.context.object; o.scale = (x, y, z); o.data.materials.append(card)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x / 2, y / 2, -0.06)); o = bpy.context.object; o.scale = (x + 1.6, y + 1.6, 0.12); o.data.materials.append(base); b3d.bevel(o, 0.05)
    r = 0.012
    for i in range(x + 1):
        rod((i, -0.005, 0), (i, -0.005, z), r, line); rod((i, 0, z + 0.005), (i, y, z + 0.005), r, line)
    for j in range(z + 1):
        rod((0, -0.005, j), (x, -0.005, j), r, line); rod((x + 0.005, 0, j), (x + 0.005, y, j), r, line)
    for j in range(y + 1):
        rod((0, j, z + 0.005), (x, j, z + 0.005), r, line); rod((x + 0.005, j, 0), (x + 0.005, j, z), r, line)
    bpy.ops.mesh.primitive_cube_add(size=0.26, location=(x - 0.16, y - 0.16, z + 0.13)); bpy.context.object.data.materials.append(white)
    for n, (dx, s) in enumerate([(0.0, 0.07), (0.1, 0.055), (0.19, 0.075)]):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=s, location=(0.08 + dx * 0.7, -0.08, 0.06 + dx * 0.7)); bpy.context.object.data.materials.append(ink)
    for i, pts in enumerate(routes(x, y, z)):
        if after:
            m = mint if i == best else grey; rr = 0.05 if i == best else 0.025
        else:
            m = b3d.mat(f'r{i}', COLS[i], rough=0.4, coat=0); glow(m, COLS[i], 0.4); rr = 0.04
        e = 0.03 + 0.012 * i
        lp = [lift(p, x, y, z, e) for p in pts]
        for a, b in zip(lp, lp[1:]): rod(a, b, rr, m)
        if after and i != best: continue
        c = mid(lp, [0.3, 0.62, 0.86, 0.2][i]); d = Vector((math.sin(math.radians(AZ)) * math.cos(math.radians(EL)), -math.cos(math.radians(AZ)) * math.cos(math.radians(EL)), math.sin(math.radians(EL))))
        c = c + d * 0.25
        bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.04, location=c, rotation=(math.radians(90 - EL), 0, math.radians(AZ)), vertices=32)
        bpy.context.object.data.materials.append(m); text(str(bd['labels'][i]), c + d * 0.03, 0.3, ink)
    b3d.stack_camera((x / 2, y / 2, z / 2), 6.2, az=AZ, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
