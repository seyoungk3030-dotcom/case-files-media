"""ROOM 179 3D sprites: a shop counter with a wrapped gift box and its upright price tag. The tag shows the
original price and two percent stickers stuck on one after the other, with an empty final-price slot.
p*: before (slot shows ?). a*: after, the slot glows mint with the real final price."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
BOXC = {'A': (0.2, 0.45, 0.8), 'B': (0.85, 0.35, 0.55), 'C': (0.25, 0.65, 0.4), 'D': (0.9, 0.6, 0.15)}


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def box(loc, sc, m, rot=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=(0, 0, rot)); o = bpy.context.object; o.scale = sc; o.data.materials.append(m)
    bpy.ops.object.modifier_add(type='BEVEL'); o.modifiers['Bevel'].width = min(min(sc) * 0.15, 0.05); o.modifiers['Bevel'].segments = 3; return o


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.pi / 2, 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def scene(k, after):
    price, st = BOARDS[k]
    wood = b3d.mat('wood', (0.5, 0.3, 0.16), rough=0.45, coat=0.4); card = b3d.mat('card', (0.97, 0.96, 0.92), rough=0.6, coat=0)
    ink = b3d.mat('ink', (0.06, 0.06, 0.08), rough=0.5, coat=0); white = b3d.mat('white', (1, 1, 1), rough=0.4, coat=0)
    red = b3d.mat('red', (0.85, 0.12, 0.12), rough=0.35, coat=0.3); blue = b3d.mat('blue', (0.12, 0.3, 0.85), rough=0.35, coat=0.3)
    slot = b3d.mat('slot', (0.45, 0.46, 0.5), rough=0.6, coat=0); mint = glowm('mint', (0.15, 0.85, 0.6), 1.6)
    gift = b3d.mat('gift', BOXC[k], rough=0.4, coat=0.3); rib = b3d.mat('rib', (1.0, 0.85, 0.3), rough=0.3, coat=0.4)
    box((0, 0.3, -0.1), (4.2, 2.4, 0.2), wood)
    # gift box at the back left
    box((-1.15, 0.7, 0.6), (1.2, 1.2, 1.2), gift, 0.25)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-1.15, 0.7, 0.6), rotation=(0, 0, 0.25)); o = bpy.context.object; o.scale = (1.22, 0.18, 1.22); o.data.materials.append(rib)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-1.15, 0.7, 0.6), rotation=(0, 0, 0.25)); o = bpy.context.object; o.scale = (0.18, 1.22, 1.22); o.data.materials.append(rib)
    # upright price tag on a small stand
    tx, ty = 0.55, -0.25
    box((tx, ty + 0.12, 0.05), (0.9, 0.5, 0.1), b3d.mat('stand', (0.15, 0.15, 0.17), rough=0.4, metal=0.5, coat=0))
    box((tx, ty, 1.45), (1.75, 0.06, 2.8), card)
    text(f'{price}', (tx, ty - 0.05, 2.45), 0.62, ink)
    for i, s in enumerate(st):
        z = 1.72 - i * 0.62
        box((tx, ty - 0.05, z), (1.45, 0.04, 0.48), red if s > 0 else blue)
        text(f'{s:+d}%', (tx, ty - 0.08, z), 0.42, white)
    if after:
        box((tx, ty - 0.05, 0.42), (1.5, 0.04, 0.55), mint); text(f'{int(GOOD[k])}', (tx, ty - 0.08, 0.42), 0.5, ink)
    else:
        box((tx, ty - 0.05, 0.42), (1.5, 0.04, 0.55), slot); text('?', (tx, ty - 0.08, 0.42), 0.5, ink)
    b3d.stack_camera((-0.25, 0.1, 1.25), 3.7, az=0.0, el=14.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((820, 820), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
