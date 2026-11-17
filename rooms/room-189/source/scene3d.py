"""ROOM 189 3D sprites: a thick steel ring standing upright and four steel balls in a row under it, each ball drawn at
its size relative to the hole (before heating), with its diameter in mm written below. The ring is drawn in the state
it is in: grey at room temperature, glowing when red-hot (the answer view shows it after heating or cooling). p*: question. a*: answer, balls that pass the changed hole glow mint, the rest coral."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from fractions import Fraction as Fr
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
RH = 0.42; ZR = 1.15


def glowm(name, c, s, rough=0.4, metal=0.0):
    m = b3d.mat(name, c, rough=rough, metal=metal, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.pi / 2, 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def washer(m, inner, outer, depth):
    bpy.ops.mesh.primitive_cylinder_add(radius=outer, depth=depth, location=(0, 0, ZR), rotation=(math.pi / 2, 0, 0), vertices=128)
    o = bpy.context.object
    bpy.ops.mesh.primitive_cylinder_add(radius=inner, depth=depth * 2, location=(0, 0, ZR), rotation=(math.pi / 2, 0, 0), vertices=128)
    h = bpy.context.object; mod = o.modifiers.new('cut', 'BOOLEAN'); mod.object = h; mod.operation = 'DIFFERENCE'
    bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier='cut'); bpy.data.objects.remove(h)
    o.data.materials.clear(); o.data.materials.append(m); b3d.bevel(o, 0.02, 3); bpy.ops.object.shade_smooth(); return o


def scene(key, after):
    hole, s, balls = BOARDS[key]
    steel = b3d.mat('steel', (0.7, 0.72, 0.76), rough=0.3, metal=0.7, coat=0)
    hot = glowm('hot', (0.95, 0.14, 0.02), 0.6, rough=0.5, metal=0.0) if (s > 0) == after else b3d.mat('ring', (0.5, 0.52, 0.56), rough=0.35, metal=0.8, coat=0)
    mint = glowm('mint', (0.2, 0.85, 0.6), 0.3, rough=0.3); coral = glowm('coral', (1.0, 0.3, 0.25), 0.45, rough=0.3)
    white = glowm('white', (0.95, 0.95, 0.97), 1.0)
    washer(hot, RH, RH * 1.75, 0.28)
    hn = Fr(hole) * Fr(101, 100) ** s
    for i, b in enumerate(balls):
        x = (i - 1.5) * 0.98; r = RH * float(Fr(b) / Fr(hole))
        m = (mint if Fr(b) < hn else coral) if after else steel
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(x, 0, -0.1), segments=64, ring_count=32)
        o = bpy.context.object; o.data.materials.append(m); bpy.ops.object.shade_smooth()
        text(b, (x, -0.3, -0.8), 0.32, white)
    b3d.stack_camera((0, 0, 0.35), 4.3, az=0.0, el=6.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((760, 760), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
