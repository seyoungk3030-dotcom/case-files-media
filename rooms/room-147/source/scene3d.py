"""ROOM 147 3D sprites: a raft on still water beside a dock with marks 0-9, a little coral figure standing at the raft's
left end, seen from the front at a low slant. p*: start, with a yellow arrow along the raft. a*: the raft slid left
(faint coral outline where it was), the figure (mint) at the right end, a mint drop line to its dock mark."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, end, raft_shift
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U = 0.55; EL = 36.0


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - EL), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def X(mark): return (mark - 4.5) * U


def box(m, c, s, bev=0.03):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def figure(x, m, y=-0.42):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.66, location=(x, y, 0.55), vertices=24); o = bpy.context.object; o.data.materials.append(m); b3d.bevel(o, 0.08)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.19, location=(x, y, 1.05), segments=24, ring_count=12); bpy.context.object.data.materials.append(m)
    for dx in (-0.08, 0.08):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.34, location=(x + dx, y, 0.17), vertices=12); bpy.context.object.data.materials.append(m)


def raft(x0, x1, m, z=0.0):
    n = 5
    for i in range(n):
        y = (i - (n - 1) / 2) * 0.22
        bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=x1 - x0, location=((x0 + x1) / 2, y, z - 0.02), rotation=(0, math.radians(90), 0), vertices=20)
        bpy.context.object.data.materials.append(m)


def scene(k, after):
    b = BOARDS[k]
    water = b3d.mat('water', (0.03, 0.12, 0.2), rough=0.15, coat=0); dock = b3d.mat('dock', (0.32, 0.2, 0.1), rough=0.8, coat=0)
    log = b3d.mat('log', (0.55, 0.36, 0.16), rough=0.7, coat=0); cor = b3d.mat('cor', (0.95, 0.42, 0.35), rough=0.5, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.0)
    ghost = b3d.mat('ghost', (0.95, 0.42, 0.35), rough=0.5, coat=0); glow(ghost, (0.95, 0.42, 0.35), 0.8)
    ink = b3d.mat('ink', (0.98, 0.85, 0.35), rough=0.6, coat=0); glow(ink, (0.98, 0.85, 0.35), 0.6)
    yel = b3d.mat('yel', (1.0, 0.8, 0.2), rough=0.4, coat=0); glow(yel, (1.0, 0.8, 0.2), 1.2)
    box(water, (0, 0.2, -0.12), (6.6, 2.6, 0.06), 0.02)
    box(dock, (0, 1.2, 0.05), (6.6, 0.6, 0.18), 0.03)
    for n in range(10):
        box(ink, (X(n), 0.95, 0.15), (0.03, 0.12, 0.02), 0.005); text(str(n), (X(n), 1.15, 0.3), 0.3, ink)
    x0 = X(b['s']) - 0.25; x1 = X(b['s'] + b['L']) + 0.25
    if not after:
        raft(x0, x1, log); figure(X(b['s']), cor)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=b['L'] * U - 0.6, location=((X(b['s']) + X(b['s'] + b['L'])) / 2, -0.75, 0.1), rotation=(0, math.radians(90), 0), vertices=16)
        bpy.context.object.data.materials.append(yel)
        bpy.ops.mesh.primitive_cone_add(radius1=0.12, depth=0.25, location=(X(b['s'] + b['L']) - 0.2, -0.75, 0.1), rotation=(0, math.radians(90), 0), vertices=24); bpy.context.object.data.materials.append(yel)
    else:
        sh = float(raft_shift(b)) * U
        for xa, xb in ((x0, x1),):
            for x in (xa, xb):
                box(ghost, (x, 0, 0.05), (0.03, 1.1, 0.03), 0.005)
            box(ghost, ((xa + xb) / 2, -0.55, 0.05), (xb - xa, 0.03, 0.03), 0.005); box(ghost, ((xa + xb) / 2, 0.55, 0.05), (xb - xa, 0.03, 0.03), 0.005)
        raft(x0 - sh, x1 - sh, log); xe = X(end(b)); figure(xe, mint)
        for t in range(6):
            box(mint, (xe, 0.35 + t * 0.1, 0.12), (0.03, 0.05, 0.02), 0.005)
    b3d.stack_camera((0, 0.2, 0.35), 6.8, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((960, 600), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
