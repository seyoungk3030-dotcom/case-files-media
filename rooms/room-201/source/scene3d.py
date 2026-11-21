"""ROOM 201 3D sprites: a poster stands at the left end of a long table with a metre scale (1 m, 2 m, 3 m ticks).
p*: a see-through torch with '?' stands at the board's distance. a*: the answer's torches stacked there, all lit,
and a warm spot on the poster."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')


def glowm(name, c, s, rough=0.4, alpha=1.0):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    if alpha < 1: q.inputs['Alpha'].default_value = alpha
    return m


def box(m, loc, sc, bev=0.03):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def text(s, loc, size, m, rot=(math.pi / 2, 0, 0)):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def torch(x, y, z, body, lens, ring):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.36, location=(x + 0.18, y, z), rotation=(0, math.pi / 2, 0), vertices=32)
    o = bpy.context.object; o.data.materials.append(body); bpy.ops.object.shade_smooth(); b3d.bevel(o, 0.015, 3)
    bpy.ops.mesh.primitive_cone_add(radius1=0.1, radius2=0.07, depth=0.1, location=(x - 0.03, y, z), rotation=(0, math.pi / 2, 0), vertices=32)
    o = bpy.context.object; o.data.materials.append(ring); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_cylinder_add(radius=0.088, depth=0.01, location=(x - 0.085, y, z), rotation=(0, math.pi / 2, 0), vertices=32)
    bpy.context.object.data.materials.append(lens)


def scene(key, after):
    d, b = BOARDS[key]; n = GOOD[key]
    wood = b3d.mat('wood', (0.5, 0.32, 0.18), rough=0.5, coat=0.3); paper = b3d.mat('paper', (0.93, 0.92, 0.88), rough=0.8, coat=0)
    box(wood, (1.6, 0, -0.06), (3.9, 1.3, 0.12), 0.02)
    box(b3d.mat('frame', (0.2, 0.22, 0.26), rough=0.4, coat=0), (-0.15, 0, 0.75), (0.08, 1.0, 1.5), 0.02)
    box(paper, (-0.105, 0, 0.75), (0.01, 0.9, 1.38), 0.004)
    star = glowm('starm', (0.95, 0.35, 0.2), 0.3)
    text('★', (-0.095, 0, 0.75), 0.6, star, rot=(math.pi / 2, 0, math.pi / 2))
    tick = glowm('tick', (0.95, 0.95, 0.9), 0.6); lab = glowm('lab', (1.0, 0.82, 0.3), 0.9)
    box(tick, (1.5, -0.6, 0.005), (3.0, 0.02, 0.01), 0.002)
    for m in (0, 1, 2, 3):
        box(tick, (m, -0.6, 0.005), (0.02, 0.14, 0.01), 0.002)
        if m: text(f'{m}m', (m, -0.62, 0.17), 0.2, lab)
    zc = 0.22 if after else 0.12
    L = d - 0.1 + 0.09
    bpy.ops.mesh.primitive_cone_add(radius1=0.08, radius2=0.42, depth=L, location=((d - 0.1 - 0.09) / 2, 0, (zc + 0.75) / 2), vertices=48)
    o = bpy.context.object; o.rotation_euler = (0, -math.pi / 2 + math.atan2(0.75 - zc, d), 0)
    o.data.materials.append(glowm('beam', (1.0, 0.9, 0.6), 0.5 if after else 0.15, alpha=0.18 if after else 0.08))
    if after:
        body = b3d.mat('tb', (0.15, 0.45, 0.9), rough=0.25, coat=0.8); ring = b3d.mat('ring', (0.8, 0.82, 0.86), rough=0.2, metal=1.0, coat=0)
        lens = glowm('lens', (1.0, 0.92, 0.6), 6.0)
        cols = 1 if n == 1 else (2 if n <= 4 else 3); rows = math.ceil(n / cols)
        for i in range(n):
            r, c = divmod(i, cols); y = (c - (cols - 1) / 2) * 0.22; z = 0.12 + r * 0.2
            torch(d, y, z, body, lens, ring)
        spot = glowm('spot', (1.0, 0.85, 0.45), 0.6 * float(b), alpha=0.6)
        bpy.ops.mesh.primitive_circle_add(radius=0.38, location=(-0.098, 0, 0.75), rotation=(0, math.pi / 2, 0), fill_type='NGON')
        bpy.context.object.data.materials.append(spot)
    else:
        g = glowm('ghost', (0.7, 0.85, 1.0), 0.6, alpha=0.35)
        torch(d, 0, 0.12, g, g, g)
        text('?', (d + 0.1, 0, 0.55), 0.4, glowm('q', (1.0, 0.82, 0.3), 1.2))
    b3d.stack_camera((1.55, 0, 0.75), 4.3, az=22.0, el=16.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((800, 520), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t, 1), flush=True)
