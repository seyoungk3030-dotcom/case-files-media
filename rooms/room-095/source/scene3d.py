"""ROOM 095 3D sprites: two clear glass jugs of different sizes (capacity in litres on the front), a brass tap above,
and a mint target tag. The jugs have no marks in between. a*: the final state of the shortest solution, with blue
water in each jug and the target amount glowing."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
UH = 0.34; RJ = 0.62


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.03; t.data.materials.append(m)


def scene(k, after):
    a, b, t = BOARDS[k]; fin = RES[k][1][-1]
    glass = b3d.mat('glass', (0.85, 0.92, 1.0), rough=0.05, coat=0); q = glass.node_tree.nodes['Principled BSDF']
    q.inputs['Transmission Weight'].default_value = 1.0; q.inputs['IOR'].default_value = 1.2
    rim = b3d.mat('rim', (0.85, 0.9, 0.98), rough=0.2); glow(rim, (0.8, 0.9, 1.0), 0.4)
    water = b3d.mat('water', (0.15, 0.5, 1.0), rough=0.1, coat=0); glow(water, (0.15, 0.45, 1.0), 0.5)
    ink = b3d.mat('ink', (0.95, 0.96, 0.98), rough=0.5, coat=0); glow(ink, (0.95, 0.96, 0.98), 0.5)
    mint = b3d.mat('mint', (0.2, 0.9, 0.62), rough=0.4); glow(mint, (0.2, 0.9, 0.62), 0.9)
    shelf = b3d.mat('shelf', (0.10, 0.12, 0.2), rough=0.5); brass = b3d.mat('brass', (0.75, 0.55, 0.2), rough=0.3, metal=0.8)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.2, -0.1)); o = bpy.context.object; o.scale = (6.0, 2.0, 0.2); o.data.materials.append(shelf); b3d.bevel(o, 0.05)
    for cap, x, amt in ((a, -1.3, fin[0]), (b, 1.3, fin[1])):
        h = cap * UH
        bpy.ops.mesh.primitive_cylinder_add(radius=RJ, depth=h, location=(x, 0, h / 2), vertices=64); g = bpy.context.object; g.data.materials.append(glass)
        sol = g.modifiers.new('s', 'SOLIDIFY'); sol.thickness = 0.04
        bpy.ops.mesh.primitive_torus_add(location=(x, 0, h), major_radius=RJ, minor_radius=0.035); bpy.context.object.data.materials.append(rim)
        bpy.ops.mesh.primitive_torus_add(location=(x, 0, 0.02), major_radius=RJ, minor_radius=0.035); bpy.context.object.data.materials.append(rim)
        text(f'{cap}L', (x, -RJ - 0.05, -0.55), 0.55, ink)
        if after and amt:
            bpy.ops.mesh.primitive_cylinder_add(radius=RJ - 0.06, depth=amt * UH - 0.03, location=(x, 0, (amt * UH) / 2 + 0.02), vertices=64)
            bpy.context.object.data.materials.append(water)
            text(f'{amt}L', (x, -RJ - 0.2, amt * UH / 2), 0.42, mint if amt == t else ink)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-1.3, -0.95, 3.0)); o = bpy.context.object; o.scale = (1.9, 0.08, 0.75); o.data.materials.append(mint); b3d.bevel(o, 0.06)
    text(f'목표 {t}L', (-1.3, -1.02, 3.0), 0.5, b3d.mat('dk', (0.03, 0.05, 0.08), rough=0.5))
    b3d.stack_camera((0, 0, 1.75), 5.6, az=0.0, el=10.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((620, 700), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
