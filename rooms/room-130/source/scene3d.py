"""ROOM 130 3D sprites: front view of a tall glass jar with coloured layers (honey, soap, water, oil), each labelled
with its name and density, a 0-9 ruler on the left. p*: the object with its density hangs above the jar. a*: the
object rests on top of the first layer denser than itself, with a mint ring and a mint tick on the ruler."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, LIQ
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
R, U, Z0 = 0.95, 0.4, 0.12
COL = [(0.8, 0.42, 0.03), (0.15, 0.7, 0.3), (0.15, 0.45, 0.95), (0.95, 0.82, 0.2)]
ALPHA = [0.92, 0.8, 0.45, 0.75]
OBJ = {'포도': (0.4, 0.12, 0.45), '플라스틱 구슬': (0.95, 0.4, 0.65), '고무 공': (0.9, 0.18, 0.15), '나무 구슬': (0.7, 0.48, 0.25)}


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m, ax='CENTER'):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = ax; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def box(m, c, s, bev=0.02):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def scene(k, after):
    b = BOARDS[k]; name, d = b['obj']; rest = RES[k]
    glass = b3d.mat('glass', (0.85, 0.92, 1.0), rough=0.15, coat=0); glass.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.1
    ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0); white = b3d.mat('white', (0.96, 0.97, 1.0), rough=0.5, coat=0); glow(white, (0.96, 0.97, 1.0), 0.5)
    pole = b3d.mat('pole', (0.05, 0.06, 0.09), rough=0.6, coat=0); base = b3d.mat('base', (0.08, 0.09, 0.13), rough=0.6, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.5)
    om = b3d.mat('obj', OBJ[name], rough=0.35, coat=0.4)
    box(base, (0, 0, -0.08), (3.4, 2.4, 0.16), 0.05)
    bpy.ops.mesh.primitive_cylinder_add(radius=R + 0.05, depth=9 * U + 0.6, location=(0, 0, (9 * U + 0.6) / 2), vertices=64)
    o = bpy.context.object; o.data.materials.append(glass); o.visible_glossy = False; o.visible_shadow = False
    z = Z0
    for i, ((lname, ld), h) in enumerate(zip(LIQ, b['h'])):
        m = b3d.mat(f'l{i}', COL[i], rough=0.25, coat=0); m.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = ALPHA[i]
        bpy.ops.mesh.primitive_cylinder_add(radius=R, depth=h * U - 0.01, location=(0, 0, z + h * U / 2), vertices=64)
        o = bpy.context.object; o.data.materials.append(m); o.visible_shadow = False
        box(pole, (0.45, -R - 0.06, z + h * U / 2), (1.05, 0.02, min(0.34, h * U - 0.06)), 0.03)
        text(f'{lname} {ld}', (0.45, -R - 0.08, z + h * U / 2), 0.22, white)
        z += h * U
    box(pole, (-R - 0.42, 0, Z0 + 4.5 * U), (0.32, 0.12, 9 * U + 0.3), 0.02)
    for m_ in range(10):
        zz = Z0 + m_ * U; hit = after and m_ == rest
        box(mint if hit else white, (-R - 0.27, -0.07, zz), (0.16, 0.02, 0.03), 0.0)
        text(str(m_), (-R - 0.5, -0.08, zz), 0.2, mint if hit else white)
    r = 0.24
    if after:
        zc = Z0 + rest * U + (r * 0.55 if rest > 0 else r)
        if rest == 9: zc = Z0 + 9 * U + r * 0.3
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(-0.4, -R + r + 0.05, zc)); o = bpy.context.object; o.data.materials.append(om)
        for p in o.data.polygons: p.use_smooth = True
        bpy.ops.mesh.primitive_torus_add(location=(-0.4, -R - 0.12, zc), rotation=(math.radians(90), 0, 0), major_radius=r + 0.1, minor_radius=0.03)
        bpy.context.object.data.materials.append(mint)
    else:
        zc = Z0 + 9 * U + 0.95
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(0, 0, zc)); o = bpy.context.object; o.data.materials.append(om)
        for p in o.data.polygons: p.use_smooth = True
        box(pole, (0, -0.3, zc + 0.45), (1.9, 0.02, 0.34), 0.05)
        text(f'{name} {d}', (0, -0.32, zc + 0.45), 0.22, white)
    b3d.stack_camera((0, 0, 2.65), 6.3, az=0.0, el=6.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((760, 1000), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
