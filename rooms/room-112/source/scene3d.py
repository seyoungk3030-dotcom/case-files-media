"""ROOM 112 3D sprites: a kitchen scale (display reads 0) with a glass beaker of water on it. Next to it an amber tag
gives the object's weight and volume. Hung boards: a stand beside the scale holds the object on a string above the
water; float/sunk boards: the object waits above the water with no string (it will be let go). A faint mint ghost
shows where the object ends up. a*: the object is in place and the display shows the new reading in mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, READ, sub_frac
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
RB, ZB, ZW = 0.95, 0.42, 1.55       # beaker radius, beaker floor, water surface
K = 0.075


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m, ax='CENTER'):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = ax; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def box(m, c, s, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def cyl(m, c, r, d, v=48, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=c, vertices=v, rotation=rot); o = bpy.context.object; o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = True
    return o


def obj(b, z, mats, ghost=False):
    m = mats['ghost'] if ghost else mats[b['kind'] if b['kind'] != 'hung' else 'stone']
    if b['kind'] == 'float':
        s = 1.05; o = box(m, (0, 0, z + s / 2), (s, s, s), 0.06); top = z + s
    else:
        r = K * b['V'] ** (1 / 3)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=r, location=(0, 0, z + r), subdivisions=4 if b['kind'] == 'sunk' else 2)
        o = bpy.context.object; o.data.materials.append(m); top = z + 2 * r
        if b['kind'] == 'sunk':
            for p in o.data.polygons: p.use_smooth = True
    if ghost: o.visible_shadow = False; o.visible_glossy = False
    return top


def size(b): return 1.05 if b['kind'] == 'float' else 2 * K * b['V'] ** (1 / 3)


def scene(k, after):
    b = BOARDS[k]
    dark = b3d.mat('dark', (0.10, 0.12, 0.17), rough=0.5, coat=0.2); plate = b3d.mat('plate', (0.75, 0.78, 0.84), rough=0.3, metal=0.6, coat=0.2)
    lcd = b3d.mat('lcd', (0.02, 0.03, 0.04), rough=0.3, coat=0.3)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 3.0)
    grey = b3d.mat('grey', (0.6, 0.65, 0.7), rough=0.4, coat=0); glow(grey, (0.6, 0.65, 0.7), 1.2)
    amber = b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0.1); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    glass = b3d.mat('glass', (0.8, 0.9, 1.0), rough=0.3, coat=0); gn = glass.node_tree.nodes['Principled BSDF']; gn.inputs['Alpha'].default_value = 0.16; gn.inputs['Specular IOR Level'].default_value = 0.1
    water = b3d.mat('water', (0.06, 0.28, 0.70), rough=0.3, coat=0); water.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.6
    steel = b3d.mat('steel', (0.55, 0.58, 0.64), rough=0.3, metal=0.8, coat=0); string = b3d.mat('string', (0.9, 0.9, 0.85), rough=0.6, coat=0)
    mats = {'stone': b3d.mat('stone', (0.16, 0.16, 0.18), rough=0.8, coat=0), 'float': b3d.mat('wood', (0.42, 0.22, 0.08), rough=0.6, coat=0.1),
            'sunk': b3d.mat('iron', (0.15, 0.16, 0.18), rough=0.25, metal=0.9, coat=0.2), 'ghost': b3d.mat('ghost', (0.15, 0.85, 0.6), rough=0.5, coat=0)}
    gq = mats['ghost'].node_tree.nodes['Principled BSDF']; gq.inputs['Alpha'].default_value = 0.28; glow(mats['ghost'], (0.15, 0.85, 0.6), 0.6)
    # scale
    box(dark, (0, 0, 0.17), (2.7, 2.2, 0.34), 0.08); box(plate, (0, 0, 0.36), (2.3, 1.9, 0.05), 0.02)
    box(lcd, (0, -1.11, 0.19), (1.7, 0.04, 0.3), 0.02)
    reading = int(READ[k]) if after else 0
    text(f'{reading} g', (0, -1.14, 0.19), 0.28, mint if after else grey)
    # beaker + water
    o = cyl(glass, (0, 0, ZB - 0.03 + 1.1), RB, 2.2, 64); o.modifiers.new('s', 'SOLIDIFY').thickness = 0.04; o.visible_shadow = False; o.visible_glossy = False
    rise = 0.0
    if after:
        f = sub_frac(b); vol = (math.pi * (size(b) / 2) ** 2 * size(b) * 2 / 3 * 2 if b['kind'] != 'float' else size(b) ** 3) * f
        rise = vol / (math.pi * (RB - 0.04) ** 2)
    w = cyl(water, (0, 0, (ZB + ZW + rise) / 2), RB - 0.05, ZW + rise - ZB, 64); w.visible_shadow = False
    # where the object ends up
    s = size(b); f = sub_frac(b); zw = ZW + rise
    zfin = ZB + 0.01 if b['kind'] == 'sunk' else zw - f * s
    if b['kind'] == 'hung' and f >= 1: zfin = zw - s - 0.18
    zup = 3.35
    obj(b, zfin if after else zup, mats)
    if not after: obj(b, (ZB + 0.01 if b['kind'] == 'sunk' else ZW - f * s if f < 1 else ZW - s - 0.18), mats, ghost=True)
    if b['kind'] == 'hung':
        top = (zfin if after else zup) + s
        box(steel, (2.35, 0, 0.06), (0.9, 1.2, 0.12), 0.03); cyl(steel, (2.35, 0, 2.6), 0.06, 5.1, 16)
        cyl(steel, (1.18, 0, 5.1), 0.05, 2.4, 16, (0, math.radians(90), 0)); cyl(string, (0, 0, (5.1 + top) / 2), 0.015, 5.1 - top, 8)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=0.16, depth=0.3, location=(0, -0.2, zup - 0.35), rotation=(math.radians(180), 0, 0))
        bpy.context.object.data.materials.append(mint if not after else ink)
        if after: bpy.data.objects.remove(bpy.context.object)
    # amber tag: weight and volume
    box(amber, (-2.25, -0.2, 3.3), (1.25, 0.06, 0.95), 0.08)
    text(f"{b['m']} g", (-2.25, -0.25, 3.5), 0.3, ink); text(f"{b['V']} cm³", (-2.25, -0.25, 3.1), 0.26, ink)
    b3d.stack_camera((0.2, 0, 2.55), 7.0, az=0.0, el=8.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 1000), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
