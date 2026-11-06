"""ROOM 149 3D sprites: a street lamp at ground mark 0 and a wooden stick standing on a long ground strip with marks
0-9, seen from the side. Lamp height and stick height are shown by tick rungs (1 rung = 1 mark). p*: lamp off. a*: lamp
on (a real point light, so the stick throws its real shadow), with a mint ray from the bulb over the stick's top and a
mint ring at the shadow's tip."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, tip
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U = 0.45; EL = 28.0


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - EL), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def box(m, c, s, bev=0.02):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def rod(p, q, r, m):
    (x1, z1), (x2, z2) = p, q; L = math.hypot(x2 - x1, z2 - z1)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=((x1 + x2) / 2, 0, (z1 + z2) / 2), rotation=(0, math.atan2(x2 - x1, z2 - z1), 0), vertices=16)
    bpy.context.object.data.materials.append(m)


def scene(k, after):
    b = BOARDS[k]; H, h, d = b['H'] * U, b['h'] * U, b['d'] * U
    ground = b3d.mat('ground', (0.24, 0.25, 0.28), rough=1.0, coat=0); ground.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0
    pole = b3d.mat('pole', (0.25, 0.27, 0.3), rough=0.4, metal=0.7, coat=0); wood = b3d.mat('wood', (0.6, 0.38, 0.18), rough=0.6, coat=0)
    ink = b3d.mat('ink', (0.98, 0.85, 0.35), rough=0.6, coat=0); glow(ink, (0.98, 0.85, 0.35), 0.6)
    bulb = b3d.mat('bulb', (1.0, 0.85, 0.5), rough=0.3, coat=0); glow(bulb, (1.0, 0.8, 0.4), 6.0 if after else 0.0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.2)
    box(ground, (4.5 * U, 0.3, -0.05), (10.6 * U, 1.6, 0.1))
    for n in range(10):
        box(ink, (n * U, -0.35, 0.005), (0.03, 0.14, 0.01), 0.004); text(str(n), (n * U, -0.62, 0.02), 0.26, ink)
    rod((0, 0), (0, H), 0.05, pole); rod((0, H), (0.12, H + 0.06), 0.04, pole)
    bpy.ops.mesh.primitive_cone_add(radius1=0.16, radius2=0.05, depth=0.16, location=(0.0, 0, H + 0.12), vertices=32); bpy.context.object.data.materials.append(pole)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(0, 0, H), segments=24, ring_count=12); bpy.context.object.data.materials.append(bulb); bpy.context.object.visible_shadow = False
    for z in range(1, b['H']):
        box(ink, (-0.09, -0.02, z * U), (0.1, 0.02, 0.02), 0.003)
    box(wood, (d, 0, h / 2), (0.1, 0.1, h), 0.02)
    for z in range(1, b['h']):
        box(ink, (d - 0.09, -0.06, z * U), (0.08, 0.02, 0.02), 0.003)
    if after:
        bpy.ops.object.light_add(type='POINT', location=(0, 0, H - 0.001)); L = bpy.context.object; L.data.energy = 1600; L.data.shadow_soft_size = 0.01
        L.data.color = (1.0, 0.85, 0.6)
        xt = tip(b) * U
        shade = b3d.mat('shade', (0.01, 0.01, 0.015), rough=1.0, coat=0); shade.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0
        bpy.ops.mesh.primitive_cube_add(size=1, location=((d + xt) / 2, 0, 0.003)); o = bpy.context.object; o.scale = (xt - d, 0.2, 0.006); o.data.materials.append(shade)
        rod((0, H), (xt, 0), 0.012, mint); bpy.context.object.visible_shadow = False
        bpy.ops.mesh.primitive_torus_add(location=(xt, 0, 0.01), major_radius=0.12, minor_radius=0.02, major_segments=40); bpy.context.object.data.materials.append(mint)
    b3d.stack_camera((2.0, 0, 1.55), 5.3, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
