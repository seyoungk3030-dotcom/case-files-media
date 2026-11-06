"""ROOM 117 3D sprites: a clear glass of water on a coaster, a ruler 0-9 beside it. Ice cubes float in the water,
sit on a steel rack across the rim, or hold a dark stone frozen inside. a*: all the ice has melted; the water stands
at the new level (mint line), a grey line shows the old level, and a stone lies on the bottom."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, FIN
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U, Z0, R = 0.3, 0.2, 1.05


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def box(m, c, s, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def side(g): return 0.42 * (g / 100) ** (1 / 3)


def scene(k, after):
    b = BOARDS[k]
    floor = b3d.mat('floor', (0.07, 0.09, 0.15), rough=0.7, coat=0); coaster = b3d.mat('coaster', (0.35, 0.22, 0.12), rough=0.6, coat=0.1)
    tick = b3d.mat('tick', (0.8, 0.83, 0.9), rough=0.5, coat=0); glow(tick, (0.8, 0.83, 0.9), 1.5)
    pole = b3d.mat('pole', (0.03, 0.035, 0.05), rough=0.6, coat=0); grey = b3d.mat('grey', (0.6, 0.62, 0.7), rough=0.5, coat=0); glow(grey, (0.6, 0.62, 0.7), 1.0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.5)
    glass = b3d.mat('glass', (0.8, 0.9, 1.0), rough=0.3, coat=0); glass.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.12
    water = b3d.mat('water', (0.08, 0.35, 0.85), rough=0.3, coat=0); water.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.6
    ice = b3d.mat('ice', (0.75, 0.9, 1.0), rough=0.15, coat=0.5); ice.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.4
    stone = b3d.mat('stone', (0.12, 0.11, 0.1), rough=0.8, coat=0); steel = b3d.mat('steel', (0.6, 0.63, 0.7), rough=0.3, metal=0.8, coat=0)
    box(floor, (0, 0, -0.06), (5.0, 2.4, 0.12), 0.03)
    bpy.ops.mesh.primitive_cylinder_add(radius=R + 0.2, depth=0.12, location=(0, 0, 0.06), vertices=64); bpy.context.object.data.materials.append(coaster)
    Hg = 10.4 * U
    bpy.ops.mesh.primitive_cylinder_add(radius=R, depth=Hg, location=(0, 0, Z0 + Hg / 2 - 0.08), vertices=64); o = bpy.context.object
    o.data.materials.append(glass); o.modifiers.new('s', 'SOLIDIFY').thickness = 0.04; o.visible_shadow = False; o.visible_glossy = False
    for p in o.data.polygons: p.use_smooth = True
    box(pole, (-R - 0.55, 0.1, Z0 + 4.6 * U), (0.5, 0.25, 10 * U), 0.03)
    for n in range(10):
        z = Z0 + n * U; box(tick, (-R - 0.22, -0.05, z), (0.16, 0.02, 0.025), 0.0); text(str(n), (-R - 0.6, -0.05, z), 0.22, tick)
    lv = FIN[k] if after else b['level']
    if lv > 0:
        bpy.ops.mesh.primitive_cylinder_add(radius=R - 0.05, depth=lv * U, location=(0, 0, Z0 + lv * U / 2), vertices=64); o = bpy.context.object
        o.data.materials.append(water); o.visible_shadow = False
        for p in o.data.polygons: p.use_smooth = True
    if after:
        box(grey, (-0.05, -R - 0.05, Z0 + b['level'] * U), (2 * R + 0.5, 0.02, 0.02), 0.0)
        box(mint, (-0.3, -R - 0.08, Z0 + FIN[k] * U), (2 * R + 1.0, 0.02, 0.035), 0.0)
    rack = False; xs = [-0.35, 0.4] if len(b['items']) > 1 else [0.0]
    for it, x in zip(b['items'], xs if len(b['items']) > 1 else [0.0]):
        s = side(it['ice'])
        if it['kind'] == 'rack':
            rack = True
            if not after:
                box(ice, (0.45 if len(b['items']) > 1 else 0, 0, Z0 + Hg + 0.02 + s / 2), (s, s, s), 0.06)
            continue
        if it['kind'] == 'stone':
            zc = Z0 + b['level'] * U - 0.9 * s + s / 2
            if not after:
                box(ice, (x, 0, zc), (s * 1.15, s * 1.15, s * 1.15), 0.06)
                bpy.ops.mesh.primitive_uv_sphere_add(radius=0.16, location=(x, 0, zc)); o = bpy.context.object; o.scale = (1.3, 1, 0.8); o.data.materials.append(stone)
            else:
                bpy.ops.mesh.primitive_uv_sphere_add(radius=0.16, location=(x, 0, Z0 + 0.13)); o = bpy.context.object; o.scale = (1.3, 1, 0.8); o.data.materials.append(stone)
            continue
        if not after: box(ice, (-0.35 if len(b['items']) > 1 else x, 0, Z0 + b['level'] * U - 0.85 * s + s / 2), (s, s, s), 0.06)
    if rack:
        for dx in (-0.6, -0.3, 0, 0.3, 0.6):
            box(steel, (dx, 0, Z0 + Hg + 0.0), (0.03, 2 * R + 0.1, 0.03), 0.0)
        box(steel, (0, 0, Z0 + Hg), (2 * R + 0.1, 0.03, 0.03), 0.0)
    b3d.stack_camera((-0.45, 0, 1.75), 4.6, az=0.0, el=8.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 1000), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
