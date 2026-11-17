"""ROOM 177 3D sprites: small stone staircases with a red carpet runner glued over every riser and tread, seen from the
front-left. White brackets give the total height and the total depth. p*: question. a*: answer, the carpet glows mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, box as bbox
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
WID, CW, T = 1.0, 0.56, 0.012


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.4, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def box(m, x0, x1, z0, z1, y0=-WID / 2, y1=WID / 2):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)); o = bpy.context.object
    o.scale = (x1 - x0, y1 - y0, z1 - z0); o.data.materials.append(m); return o


def cyl(m, a, b, r=0.012):
    dx, dy, dz = (b[i] - a[i] for i in range(3)); L = math.sqrt(dx * dx + dy * dy + dz * dz)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=tuple((a[i] + b[i]) / 2 for i in range(3)), vertices=16)
    o = bpy.context.object; o.rotation_euler = (0, math.acos(dz / L), math.atan2(dy, dx)); o.data.materials.append(m)


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.pi / 2, 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def fmt(v): v = float(v); return f'{v:g}m'


def scene(k, after):
    p = BOARDS[k]; H, D = map(float, bbox(p))
    stone = b3d.mat('stone', (0.17, 0.18, 0.21), rough=0.7, coat=0); floor = b3d.mat('floor', (0.12, 0.13, 0.17), rough=0.8, coat=0)
    red = b3d.mat('red', (0.75, 0.08, 0.1), rough=0.8, coat=0); mint = glowm('mint', (0.2, 0.9, 0.62), 0.8); wh = glowm('wh', (0.96, 0.97, 1.0), 0.8)
    cm = mint if after else red
    s = max(H, D)
    box(floor, -0.2 * s - 0.2, D + 0.45 * s + 0.4, -0.04, 0, -WID / 2 - 0.45, WID / 2 + 0.3)
    x, z = 0.0, 0.0
    for r, t in p:
        r, t = float(r), float(t); zn = z + r
        if r > 0: box(cm, x - T, x, z, zn + T, -CW / 2, CW / 2)
        else: box(cm, x, x + T, zn, z + T, -CW / 2, CW / 2)
        if t > 0:
            box(stone, x, x + t, 0, zn); box(cm, x, x + t, zn, zn + T, -CW / 2, CW / 2)
        x, z = x + t, zn
    a = 0.06 * s + 0.03; fy = -WID / 2 - 0.05
    xs, zz0, xe = 0.0, 0.0, 0.0
    for r, t in p:
        zz0 += float(r); xs += float(t)
        if abs(zz0 - H) < 1e-9: xe = xs
    bx = xe + 0.08 * s + 0.08
    cyl(wh, (bx, fy, 0), (bx, fy, H)); [cyl(wh, (bx - a / 2, fy, zz), (bx + a / 2, fy, zz)) for zz in (0, H)]
    text(fmt(H), (bx + 0.16 * s + 0.12, fy, H / 2), 0.13 * s + 0.08, wh)
    dy = -WID / 2 - 0.3
    cyl(wh, (0, dy, 0.02), (D, dy, 0.02)); [cyl(wh, (xx, dy - a / 2, 0.02), (xx, dy + a / 2, 0.02)) for xx in (0, D)]
    text(fmt(D), (D / 2, dy - 0.25, -0.1 * s - 0.05), 0.13 * s + 0.08, wh)
    b3d.stack_camera((D / 2 + 0.1 * s, -0.2, H / 2 - 0.12 * s), 1.45 * s + 1.0, az=-30.0, el=18.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((700, 560), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
