"""ROOM 045 3D sprites: per setup A-D a row of gears on the floor ('gA'..'gD'): the driver (left, amber) with a dotted
quarter-turn clockwise arrow, the last gear (mint) with a coral arrow pointing at 1 on a 1-4 dial, teeth counts in
front of every gear. Answer sprites ('hA'..'hD') turn every gear by its real amount, the arrow ending on the answer
(start direction kept as a faint ghost). Same camera scale for all. Optional argv after '--': names to render."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import SETUPS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
M_ = 0.09
FONT = None


def r(n): return M_ * n / 2


def text(s, x, y, z, m, size=0.26):
    bpy.ops.object.text_add(location=(x, y, z)); o = bpy.context.object
    o.data.font = FONT; o.data.body = s; o.data.size = size; o.data.extrude = 0.012; o.data.align_x = 'CENTER'; o.data.align_y = 'CENTER'
    o.data.materials.append(m); return o


def arrow(x, y, ang, z, m, L, w=0.07):
    ux, uy = math.cos(ang), math.sin(ang)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x + ux * L * 0.38, y + uy * L * 0.38, z))
    b = bpy.context.object; b.scale = (L * 0.76, w, 0.035); b.rotation_euler = (0, 0, ang); b.data.materials.append(m)
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=w * 2.2, radius2=w * 2.2, depth=0.035, location=(x + ux * L * 0.86, y + uy * L * 0.86, z))
    c = bpy.context.object; c.rotation_euler = (0, 0, ang - math.pi / 2); c.data.materials.append(m)


def scene(k, answer):
    teeth = SETUPS[k]
    D = (math.cos(math.radians(225)), math.sin(math.radians(225)))   # the row runs from the last gear down-left
    pos, d = [(0.0, 0.0)], 0.0
    for i in range(len(teeth) - 2, -1, -1):
        d += r(teeth[i]) + r(teeth[i + 1]); pos.insert(0, (D[0] * d, D[1] * d))
    xs0 = [p[0] - r(n) for p, n in zip(pos, teeth)] + [r(teeth[-1]) + 0.35]
    ys0 = [p[1] - r(n) for p, n in zip(pos, teeth)] + [r(teeth[-1]) + 0.35]
    cx, cy = (min(xs0) + 0.85) / 2, (min(ys0) + 0.85) / 2
    global FONT
    b3d.reset((900, 900), 40); b3d.lights(5)
    FONT = bpy.data.fonts.load(os.path.join(HERE, '../../../kit/fonts/P-Bold.otf'))
    b3d.stack_camera((-1.3, -1.4, 0), 4.9, 0.0, 62.0)
    hub = b3d.mat('hub', (0.15, 0.18, 0.24), rough=0.35, metal=0.8, coat=0)
    amber = b3d.mat('amber', (0.95, 0.62, 0.10), rough=0.3, coat=0.5)
    steel = b3d.mat('steel', (0.72, 0.76, 0.82), rough=0.3, metal=0.35, coat=0.4)
    mint = b3d.mat('mint', b3d.PAL['mint'], rough=0.3, coat=0.5)
    coral = b3d.mat('coral', b3d.PAL['coral'], rough=0.3, coat=0.5)
    ghost = b3d.mat('ghost', (0.75, 0.78, 0.84), rough=0.5, coat=0)
    white = b3d.mat('white', (0.93, 0.95, 0.98), rough=0.5, coat=0)
    ink = b3d.mat('ink', (0.06, 0.09, 0.15), rough=0.5, coat=0)
    trav = b3d.mat('trav', (0.95, 0.62, 0.10), rough=0.4)
    # rotation of each gear (radians, + = anticlockwise) when the driver turns a quarter turn clockwise
    rot, q = [], -math.pi / 2
    for i, n in enumerate(teeth):
        if i: q = -q * teeth[i - 1] / n
        rot.append(q if answer else 0.0)
    th = []
    for i, n in enumerate(teeth):
        if i == 0: th.append(0.13)
        else: th.append(b3d.mesh_angle(pos[i - 1], teeth[i - 1], pos[i], n, th[i - 1], M_))
    for i, n in enumerate(teeth):
        mt = amber if i == 0 else mint if i == len(teeth) - 1 else steel
        b3d.gear(n, M_, (*pos[i], 0), th[i] + rot[i], mt, hub=hub, thick=0.2)
        cr = max(0.2, r(n) * 0.28 + 0.03)   # white cap on the hub with the teeth count
        bpy.ops.mesh.primitive_cylinder_add(radius=cr, depth=0.03, vertices=48, location=(*pos[i], 0.245))
        bpy.context.object.data.materials.append(white)
        if i < len(teeth) - 1: text(str(n), pos[i][0], pos[i][1], 0.26, ink, 0.26 if n > 12 else 0.2)
    xf, rf = 0.0, r(teeth[-1]); top = 0.2 + 0.06
    text(str(teeth[-1]), 0, 0, 0.26, ink, 0.2)
    for ang, m, w, z in ([(math.pi / 2, ghost, 0.045, top - 0.005)] if answer else []) + [(math.pi / 2 + rot[-1], coral, 0.07, top + 0.02)]:
        arrow(0.21 * math.cos(ang), 0.21 * math.sin(ang), ang, z, m, 0.52, w)   # pointer from the cap's edge outwards
    for d, (dx, dy) in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):   # dial 1 up, 2 right, 3 down, 4 left
        R = 1.0
        text(str(d + 1), xf + dx * R, dy * R, 0.01, white, 0.26)
    (x0, y0), r0 = pos[0], r(teeth[0]) + 0.22     # quarter turn clockwise on the driver: from 6 o'clock to 9 o'clock
    for i in range(12):
        a = math.radians(280 - i * 6.5)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=(x0 + r0 * math.cos(a), y0 + r0 * math.sin(a), 0.05))
        bpy.context.object.data.materials.append(trav)
    a = math.radians(280 - 12 * 6.5)
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.1, radius2=0.1, depth=0.04, location=(x0 + r0 * math.cos(a), y0 + r0 * math.sin(a), 0.05))
    c = bpy.context.object; c.rotation_euler = (0, 0, a - math.pi); c.data.materials.append(trav)
    b3d.floor()


names = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [p + k for k in 'ABCD' for p in 'gh']
for name in names:
    t = time.time(); scene(name[1], name[0] == 'h'); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
