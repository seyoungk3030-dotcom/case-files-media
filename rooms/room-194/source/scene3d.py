"""ROOM 194 3D sprites: one convenience-store deal per board on a shelf: canned coffee 2+1, ice cream 'second one half
price', milk 1+1, cup noodles 'third one half price'. A sign over the shelf shows the 2+1 / 1+1 deals; the half-price
deals carry a yellow 50% tag on the item it applies to. a*: the part you got for free glows mint (a whole item, or the
lower half of the half-price item)."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')


def glowm(name, c, s, rough=0.4, alpha=1.0):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    if alpha < 1: q.inputs['Alpha'].default_value = alpha
    return m


def box(m, loc, scale, bev=0.0, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def cyl(m, r, d, loc, r2=None, v=64):
    if r2 is None: bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, vertices=v)
    else: bpy.ops.mesh.primitive_cone_add(radius1=r2, radius2=r, depth=d, location=loc, vertices=v)
    o = bpy.context.object; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def text(s, loc, size, m, rot=(math.pi / 2, 0, 0)):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def item(kind, x):
    """returns item height"""
    if kind == '캔커피':
        cyl(b3d.mat('can', (0.55, 0.32, 0.18), rough=0.25, metal=0.6, coat=0.4), 0.2, 0.62, (x, 0, 0.31))
        cyl(b3d.mat('band', (0.95, 0.9, 0.82), rough=0.4, coat=0.2), 0.203, 0.2, (x, 0, 0.33))
        cyl(b3d.mat('lid', (0.8, 0.8, 0.82), rough=0.25, metal=0.9), 0.17, 0.03, (x, 0, 0.635)); return 0.65
    if kind == '아이스크림':
        cyl(b3d.mat('cup', (0.98, 0.75, 0.82), rough=0.4, coat=0.3), 0.27, 0.42, (x, 0, 0.21), r2=0.2)
        cyl(b3d.mat('icelid', (0.98, 0.98, 1.0), rough=0.3, coat=0.4), 0.29, 0.05, (x, 0, 0.445)); return 0.47
    if kind == '우유':
        w = b3d.mat('milk', (0.96, 0.97, 1.0), rough=0.5, coat=0.2); bl = b3d.mat('milkb', (0.2, 0.45, 0.9), rough=0.5, coat=0.2)
        box(w, (x, 0, 0.36), (0.36, 0.36, 0.72), 0.01); box(bl, (x, -0.181, 0.34), (0.34, 0.005, 0.26))
        rf = b3d.mat('roof', (0.82, 0.86, 0.95), rough=0.5, coat=0.2); box(rf, (x, 0, 0.72), (0.255, 0.355, 0.255), 0.01, rot=(0, math.pi / 4, 0)); box(rf, (x, 0, 0.92), (0.04, 0.36, 0.1)); return 0.97
    cyl(b3d.mat('ramen', (0.92, 0.2, 0.12), rough=0.45, coat=0.3), 0.3, 0.5, (x, 0, 0.25), r2=0.22)
    cyl(b3d.mat('rband', (0.98, 0.95, 0.85), rough=0.4, coat=0.2), 0.285, 0.12, (x, 0, 0.32), r2=0.27)
    cyl(b3d.mat('rlid', (0.85, 0.85, 0.88), rough=0.3, metal=0.6), 0.31, 0.03, (x, 0, 0.515)); return 0.53


def scene(key, after):
    deal, take, pay, kind = BOARDS[key]
    shelf = b3d.mat('shelf', (0.62, 0.64, 0.68), rough=0.4, coat=0.2); back = b3d.mat('back', (0.1, 0.12, 0.17), rough=0.6, coat=0)
    box(shelf, (0, 0, -0.04), (2.6, 1.0, 0.08), 0.02); box(back, (0, 0.5, 0.8), (2.6, 0.04, 1.7))
    box(b3d.mat('lip', (0.95, 0.75, 0.15), rough=0.4, coat=0.2), (0, -0.5, -0.04), (2.6, 0.03, 0.1))
    xs = [-0.75, 0.0, 0.75][:take] if take == 3 else [-0.42, 0.42]
    mint = glowm('mint', (0.25, 0.95, 0.7), 1.0, rough=0.4, alpha=0.55)
    free = take - pay
    for i, x in enumerate(xs):
        h = item(kind, x)
        last = i == len(xs) - 1
        if '+' not in deal and last:
            tg = b3d.mat('tag', (1.0, 0.82, 0.2), rough=0.4, coat=0.2); box(tg, (x, -0.35, h + 0.2), (0.5, 0.03, 0.24), 0.02)
            text('50%', (x, -0.375, h + 0.2), 0.17, b3d.mat('tagt', (0.1, 0.1, 0.12), rough=0.5, coat=0))
        if after and last:
            frac = 1.0 if free >= 1 else 0.5
            cw = 0.75 if kind in ('아이스크림', '컵라면') else 0.6
            box(mint, (x, 0, h * frac / 2), (cw, cw, h * frac + 0.04))
    if '+' in deal:
        sg = b3d.mat('sign', (0.85, 0.08, 0.12), rough=0.4, coat=0.3); box(sg, (0, 0.46, 1.42), (1.0, 0.05, 0.42), 0.04)
        text(deal, (0, 0.425, 1.42), 0.32, b3d.mat('signt', (1, 1, 1), rough=0.4, coat=0))
    b3d.stack_camera((0, 0, 0.7), 2.9, az=0.0, el=14.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((700, 640), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t, 1), flush=True)
