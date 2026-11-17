"""ROOM 191 3D sprites: a ball (orange, bowling ball, Earth, Moon; not to scale) with a rope ring lifted evenly off its
equator. p*: question, the gap under the rope is unknown. a*: answer, the gap glows as a mint ring (its size in cm is
written on the cards). The camera looks down steeply so the even gap reads as a ring."""
import math, os, random, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
R = 1.0; RR = 1.2


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def ball(m, r=R, loc=(0, 0, 0), seg=64):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=seg // 2)
    o = bpy.context.object; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def patch(m, r, theta, phi, size, flat=0.35):
    d = (math.cos(phi) * math.cos(theta), math.cos(phi) * math.sin(theta), math.sin(phi))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=size, location=tuple(R * x for x in d), segments=24, ring_count=12)
    o = bpy.context.object; o.scale = (1, 1, flat); o.rotation_euler = (0, math.pi / 2 - phi, theta); o.data.materials.append(m)
    bpy.ops.object.shade_smooth()


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.pi / 2, 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def scene(key, after):
    name = BOARDS[key][0]; random.seed(7)
    if name == '귤':
        ball(b3d.mat('peel', (1.0, 0.45, 0.05), rough=0.55, coat=0.2))
        ball(b3d.mat('stem', (0.25, 0.45, 0.15), rough=0.6, coat=0), 0.09, (0, 0.05, 0.98), 16)
    elif name == '볼링공':
        ball(b3d.mat('bowl', (0.12, 0.2, 0.55), rough=0.12, coat=1.0)); hole = b3d.mat('hole', (0.02, 0.02, 0.03), rough=0.9, coat=0)
        for th, ph in ((-1.85, 0.95), (-1.57, 1.1), (-1.29, 0.95)): patch(hole, R, th, ph, 0.1, 0.25)
    elif name == '지구':
        ball(b3d.mat('sea', (0.08, 0.35, 0.85), rough=0.3, coat=0.3)); land = b3d.mat('land', (0.2, 0.6, 0.25), rough=0.7, coat=0)
        for th, ph, s in ((-1.2, 0.75, 0.45), (-2.4, 0.45, 0.38), (-0.3, 0.4, 0.3), (0.9, 0.7, 0.4), (2.2, 0.55, 0.32)): patch(land, R, th, ph, s, 0.12)
        ice = b3d.mat('ice', (0.95, 0.97, 1.0), rough=0.5, coat=0); patch(ice, R, 1.0, 1.4, 0.22, 0.1)
    else:
        ball(b3d.mat('moon', (0.4, 0.4, 0.39), rough=0.85, coat=0)); cr = b3d.mat('crater', (0.24, 0.24, 0.24), rough=0.9, coat=0)
        for th, ph, s in ((-1.3, 0.8, 0.22), (-2.3, 0.5, 0.3), (-0.4, 0.45, 0.18), (0.6, 1.1, 0.15), (2.0, 0.6, 0.2), (1.2, 0.35, 0.16)): patch(cr, R, th, ph, s, 0.08)
    rope = b3d.mat('rope', (0.85, 0.65, 0.35), rough=0.8, coat=0)
    bpy.ops.mesh.primitive_torus_add(major_radius=RR, minor_radius=0.04, major_segments=128, minor_segments=12); bpy.context.object.data.materials.append(rope)
    bpy.ops.object.shade_smooth()
    if after:
        mint = glowm('mint', (0.2, 0.95, 0.65), 0.6)
        bpy.ops.mesh.primitive_cylinder_add(radius=RR - 0.02, depth=0.03, vertices=128); o = bpy.context.object
        bpy.ops.mesh.primitive_cylinder_add(radius=R + 0.005, depth=0.2, vertices=128); h = bpy.context.object
        mod = o.modifiers.new('cut', 'BOOLEAN'); mod.object = h; mod.operation = 'DIFFERENCE'
        bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier='cut'); bpy.data.objects.remove(h)
        o.data.materials.clear(); o.data.materials.append(mint)
    b3d.stack_camera((0, 0, 0.0), 2.75, az=0.0, el=72.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((700, 700), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t, 1), flush=True)
