"""ROOM 121 3D sprites: a flat wooden plate of squares on a steel pin sticking out of a dark wall bracket, held in
the drawn position; four amber number chips on its corners. a*: the plate has swung free about the pin until its
centre of mass (mint dot) is straight below it; a mint dashed plumb line runs down from the pin and the lowest
chip gets a mint ring."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, com
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
S, PZ = 0.55, 0.0


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m); return t


def box(m, c, s, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def scene(k, after):
    b = BOARDS[k]; px, py = b['pin']; ans = RES[k][0]
    wall = b3d.mat('wall', (0.02, 0.025, 0.04), rough=0.8, coat=0); wood = b3d.mat('wood', (0.55, 0.36, 0.18), rough=0.6, coat=0.1)
    wood2 = b3d.mat('wood2', (0.47, 0.30, 0.15), rough=0.6, coat=0.1); steel = b3d.mat('steel', (0.6, 0.63, 0.7), rough=0.3, metal=0.8, coat=0)
    amber = b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0.1); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.5)
    dark = b3d.mat('dark', (0.12, 0.13, 0.18), rough=0.5, coat=0.1)
    box(wall, (0, 0.5, -0.6), (9.0, 0.1, 9.0), 0.0)
    box(dark, (0, 0.38, PZ), (0.6, 0.14, 0.6), 0.05)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.7, location=(0, 0.05, PZ), rotation=(math.radians(90), 0, 0), vertices=24)
    bpy.context.object.data.materials.append(steel)
    piv = bpy.data.objects.new('piv', None); bpy.context.collection.objects.link(piv); piv.location = (0, 0, PZ)
    objs = []
    for i, (x, y) in enumerate(b['cells']):
        o = box(wood if (x + y) % 2 else wood2, ((x + 0.5 - px) * S, 0, PZ + (y + 0.5 - py) * S), (S * 0.99, 0.12, S * 0.99), 0.01); objs.append(o)
    cx, cy = com(b); alpha = (-math.pi / 2 - math.atan2(cy - py, cx - px)) if after else 0.0
    def rot(u, v): return u * math.cos(alpha) - v * math.sin(alpha), u * math.sin(alpha) + v * math.cos(alpha)
    for n, (x, y) in b['marks'].items():
        u, v = rot((x - px) * S, (y - py) * S); c = (u, -0.1, PZ + v)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.05, location=c, rotation=(math.radians(90), 0, 0), vertices=40)
        o = bpy.context.object; o.data.materials.append(amber)
        text(str(n), (c[0], -0.14, c[2]), 0.26, ink)
        if after and n == ans:
            bpy.ops.mesh.primitive_torus_add(location=(c[0], -0.12, c[2]), rotation=(math.radians(90), 0, 0), major_radius=0.27, minor_radius=0.035)
            o = bpy.context.object; o.data.materials.append(mint)
    if after:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=((cx - px) * S, -0.12, PZ + (cy - py) * S)); o = bpy.context.object; o.data.materials.append(mint); objs.append(o)
    for o in objs:
        o.parent = piv; o.location = Vector(o.location) - piv.location
    if after:
        a = math.atan2(cy - py, cx - px); alpha = -math.pi / 2 - a      # CCW turn that sends the centre of mass straight down
        piv.rotation_euler = (0, -alpha, 0)
        z = PZ - 0.25
        while z > PZ - 3.4:
            box(mint, (0, -0.2, z - 0.09), (0.03, 0.02, 0.18), 0.0); z -= 0.3
    b3d.stack_camera((0, 0, PZ - 0.3), 4.3, az=0.0, el=0.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 1000), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
