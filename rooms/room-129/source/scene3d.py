"""ROOM 129 3D sprites: front view of a wooden shelf resting on stacks of blocks, a yellow spirit level on it. The
vial (glass tube with yellow-green liquid) has marks 1-9 below it. p*: no bubble shown (a '?' sits on the vial).
a*: the bubble sits at the higher end's mark with a mint ring."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, mark
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
BH, SPAN, MK = 0.22, 5.2, 0.34


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m, par):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m); t.parent = par


def box(m, c, s, bev=0.02, par=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev)
    if par: o.parent = par
    return o


def scene(k, after):
    b = BOARDS[k]; hl, hr = b['left'] * BH, b['right'] * BH; th = math.atan2(hr - hl, SPAN)
    wood = b3d.mat('wood', (0.55, 0.36, 0.2), rough=0.6, coat=0.1); block = b3d.mat('block', (0.85, 0.62, 0.32), rough=0.6, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.5)
    yel = b3d.mat('level', (0.95, 0.72, 0.08), rough=0.4, coat=0.2); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    glass = b3d.mat('glass', (0.85, 0.95, 1.0), rough=0.1, coat=0); glass.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.18
    liq = b3d.mat('liq', (0.3, 0.7, 0.05), rough=0.2, coat=0); liq.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.55
    air = b3d.mat('air', (0.97, 0.99, 1.0), rough=0.1, coat=0); glow(air, (0.97, 0.99, 1.0), 1.6)
    base = b3d.mat('base', (0.08, 0.09, 0.13), rough=0.6, coat=0); amber = b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0.1)
    box(base, (0, 0, -0.08), (7.0, 1.6, 0.16), 0.05)
    for sx, n in ((-1, b['left']), (1, b['right'])):
        for i in range(n): box(block, (sx * SPAN / 2, 0, BH / 2 + i * BH), (0.5, 0.5, BH - 0.015), 0.02)
    piv = bpy.data.objects.new('piv', None); bpy.context.collection.objects.link(piv)
    piv.location = (0, 0, (hl + hr) / 2 + 0.08); piv.rotation_euler = (0, -th, 0)
    box(wood, (0, 0, 0), (SPAN / math.cos(th) + 0.7, 0.9, 0.16), 0.03, piv)
    box(yel, (0, -0.05, 0.08 + 0.27), (3.9, 0.3, 0.54), 0.04, piv)
    zc = 0.08 + 0.42
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=3.4, location=(0, -0.22, zc), rotation=(0, math.radians(90), 0), vertices=32)
    o = bpy.context.object; o.data.materials.append(glass); o.parent = piv
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=3.36, location=(0, -0.22, zc), rotation=(0, math.radians(90), 0), vertices=32)
    o = bpy.context.object; o.data.materials.append(liq); o.parent = piv
    for m in range(1, 10):
        x = (m - 5) * MK
        box(ink, (x, -0.215, zc + 0.13), (0.025, 0.03, 0.08), 0.0, piv)
        text(str(m), (x, -0.21, 0.08 + 0.17), 0.2, mint if after and m == mark(b) else ink, piv)
    if after:
        x = (mark(b) - 5) * MK
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(x, -0.31, zc + 0.03)); o = bpy.context.object; o.scale = (0.2, 0.035, 0.07); o.data.materials.append(air); o.parent = piv
        bpy.ops.mesh.primitive_torus_add(location=(x, -0.3, zc), rotation=(math.radians(90), 0, 0), major_radius=0.17, minor_radius=0.022); o = bpy.context.object; o.data.materials.append(mint); o.parent = piv
    else:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.16, depth=0.03, location=(0, -0.34, zc + 0.42), rotation=(math.radians(90), 0, 0), vertices=32)
        o = bpy.context.object; o.data.materials.append(amber); o.parent = piv; text('?', (0, -0.36, zc + 0.42), 0.22, ink, piv)
    b3d.stack_camera((0, 0, 1.0), 7.3, az=0.0, el=10.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 560), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
