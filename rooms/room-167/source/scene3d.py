"""ROOM 167 3D sprites: two wooden trays side by side on a table, each with pizzas drawn to scale (diameter in cm) and
a paper tag behind it with its number and size. p*: before. a*: the tray with more pizza gets a mint ring, the other
is dimmed."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
EL = 55.0; S = 0.04  # metres per cm in the scene
ARR = {1: [(0, 0)], 2: [(-0.5, 0), (0.5, 0)], 3: [(0, 0.48), (-0.5, -0.4), (0.5, -0.4)], 4: [(-0.5, 0.5), (0.5, 0.5), (-0.5, -0.5), (0.5, -0.5)]}


def box(loc, scale, m, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 4)
    return o


def cyl(loc, r, d, m, v=64, bev=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d, location=loc); o = bpy.context.object; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def pizza(x, y, r, M):
    cyl((x, y, 0.08), r, 0.06, M['crust'], 64, 0.02); cyl((x, y, 0.115), r * 0.86, 0.02, M['sauce'])
    cyl((x, y, 0.125), r * 0.8, 0.012, M['cheese'])
    for i in range(int(4 + r * 8)):
        a = i * 2.39996; rr = r * 0.62 * math.sqrt((i + 0.5) / (4 + r * 8))
        cyl((x + rr * math.cos(a), y + rr * math.sin(a), 0.135), r * 0.11, 0.012, M['pep'], 24)


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(70), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def scene(key, after):
    b = BOARDS[key]
    M = {'crust': b3d.mat('crust', (0.85, 0.6, 0.3), rough=0.7, coat=0), 'sauce': b3d.mat('sauce', (0.55, 0.06, 0.03), rough=0.6, coat=0),
         'cheese': b3d.mat('cheese', (0.95, 0.7, 0.2), rough=0.5, coat=0), 'pep': b3d.mat('pep', (0.4, 0.04, 0.03), rough=0.5, coat=0)}
    wood = b3d.mat('wood', (0.5, 0.32, 0.17), rough=0.6, coat=0); table = b3d.mat('table', (0.55, 0.47, 0.38), rough=0.8, coat=0)
    paper = b3d.mat('paper', (0.98, 0.93, 0.78), rough=0.7, coat=0); ink = b3d.mat('ink', (0.1, 0.08, 0.06), rough=0.8, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0)
    q = mint.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (0.15, 0.85, 0.6, 1); q.inputs['Emission Strength'].default_value = 1.4
    box((0, 0, -0.04), (4.6, 2.6, 0.08), table, 0.04)
    for side, cx in (('L', -1.12), ('R', 1.12)):
        tag, n, d = b[side]; r = d / 2 * S
        box((cx, -0.05, 0.02), (2.05, 1.9, 0.05), wood, 0.03)
        sp = max(2 * r + 0.06, 0.1)
        for ax, ay in ARR[n]: pizza(cx + ax * sp, -0.05 + ay * sp * (0.95 if n == 3 else 1), r, M)
        if after and tag == GOOD[key]:
            bpy.ops.mesh.primitive_torus_add(location=(cx, -0.05, 0.05), major_radius=0.9, minor_radius=0.035, major_segments=64); t = bpy.context.object; t.scale = (1.05, 0.98, 1); t.data.materials.append(mint)
        o = box((cx, 1.25, 0.42), (1.9, 0.05, 0.62), paper, 0.03); o.rotation_euler = (math.radians(-20), 0, 0)
        text(f'{tag}번 · {d}cm × {n}', (cx, 1.21, 0.44), 0.3, ink)
    b3d.stack_camera((0, 0.15, 0.3), 5.4, az=0.0, el=EL)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((1000, 760), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
