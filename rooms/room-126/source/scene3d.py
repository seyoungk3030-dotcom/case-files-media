"""ROOM 126 3D sprites: front view of a steel threaded rod (ridges = thin rings, q per ruler step) next to a 0-9
ruler. A hex nut with an amber pointer sits on it. p*: the nut at its start mark. a*: a faint ghost at the start and
the nut at its end mark with a mint pointer."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U, Z0, RX = 0.5, 0.45, 1.25


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def box(m, c, s, bev=0.03):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def nut(z, m, pm):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.46, depth=0.3, location=(0, 0, z), vertices=6, rotation=(0, 0, math.radians(30)))
    o = bpy.context.object; o.data.materials.append(m); b3d.bevel(o, 0.03)
    box(pm, ((0.46 + RX - 0.3) / 2 + 0.05, -0.02, z), (RX - 0.3 - 0.46 + 0.2, 0.06, 0.07), 0.01)
    bpy.ops.mesh.primitive_cone_add(radius1=0.09, depth=0.18, location=(RX - 0.32, -0.02, z), rotation=(0, math.radians(90), 0), vertices=3)
    bpy.context.object.data.materials.append(pm)


def scene(k, after):
    b = BOARDS[k]; q = b['q']; end = RES[k][0]
    steel = b3d.mat('steel', (0.62, 0.65, 0.7), rough=0.3, metal=0.9, coat=0); ridge = b3d.mat('ridge', (0.78, 0.8, 0.84), rough=0.25, metal=0.9, coat=0)
    nutm = b3d.mat('nut', (0.55, 0.57, 0.6), rough=0.35, metal=0.85, coat=0); amber = b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0.1)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.5)
    wood = b3d.mat('ruler', (0.9, 0.86, 0.74), rough=0.6, coat=0); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    base = b3d.mat('base', (0.08, 0.09, 0.13), rough=0.6, coat=0)
    ghost = b3d.mat('ghost', (0.55, 0.57, 0.6), rough=0.4, coat=0)
    g = ghost.node_tree.nodes['Principled BSDF']; g.inputs['Alpha'].default_value = 0.22
    top = Z0 + 9 * U + 0.5
    box(base, (0.55, 0, -0.1), (3.0, 1.4, 0.2), 0.05)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=top, location=(0, 0, top / 2), vertices=32); bpy.context.object.data.materials.append(steel)
    n = int((top - 0.15) / (U / q))
    for i in range(n + 1):
        z = Z0 - math.floor(Z0 / (U / q)) * (U / q) + i * U / q
        if z > top - 0.05: break
        bpy.ops.mesh.primitive_torus_add(location=(0, 0, z), rotation=(math.radians(4), 0, 0), major_radius=0.235, minor_radius=0.035, major_segments=32, minor_segments=8)
        bpy.context.object.data.materials.append(ridge)
    box(wood, (RX + 0.27, 0.05, top / 2), (0.72, 0.12, top), 0.02)
    for m in range(10):
        z = Z0 + m * U
        box(ink, (RX + 0.02, -0.02, z), (0.2, 0.02, 0.035), 0.0)
        text(str(m), (RX + 0.38, -0.03, z), 0.36, ink)
    if after:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.46, depth=0.3, location=(0, 0, Z0 + b['start'] * U), vertices=6, rotation=(0, 0, math.radians(30)))
        bpy.context.object.data.materials.append(ghost)
        nut(Z0 + end * U, nutm, mint)
    else:
        nut(Z0 + b['start'] * U, nutm, amber)
    b3d.stack_camera((0.6, 0, top / 2), 6.4, az=0.0, el=4.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((620, 1000), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
