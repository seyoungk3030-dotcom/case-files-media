"""ROOM 155 3D sprites: a champagne tower of 10 coupe glasses (rows 1-2-3-4) seen from the front, with a bottle tilted
over the top glass and a label of how many glass-worths are poured. p*: empty glasses. a*: champagne levels after
pouring, mint rings on the completely full glasses."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, LEVEL, ROWS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
SPX = 0.92; SPZ = 0.62; EL = 8.0; D = 0.3; R0, R1 = 0.08, 0.42


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - EL), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def glass(x, z, f, mg, ml, ring=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.025, location=(x, 0, z + 0.0125), vertices=32); bpy.context.object.data.materials.append(mg)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.028, depth=0.27, location=(x, 0, z + 0.15), vertices=16); bpy.context.object.data.materials.append(mg)
    zb = z + 0.28
    bpy.ops.mesh.primitive_cone_add(radius1=R0, radius2=R1, depth=D, location=(x, 0, zb + D / 2), vertices=48, end_fill_type='NOTHING')
    o = bpy.context.object; o.data.materials.append(mg); m = o.modifiers.new('s', 'SOLIDIFY'); m.thickness = 0.012
    if f > 0:
        h = D * (0.1 + 0.68 * float(f)) if f < 1 else D * 0.97; rt = R0 + (R1 - R0) * h / D
        bpy.ops.mesh.primitive_cone_add(radius1=R0 - 0.005, radius2=rt - 0.012, depth=h, location=(x, 0, zb + h / 2), vertices=48); bpy.context.object.data.materials.append(ml)
    if ring:
        bpy.ops.mesh.primitive_torus_add(location=(x, 0, zb + D), major_radius=R1 + 0.02, minor_radius=0.028, major_segments=48); bpy.context.object.data.materials.append(ring)


def scene(k, after):
    lv = LEVEL[k]
    mg = b3d.mat('glass', (0.85, 0.92, 1.0), rough=0.05, coat=0.5); mg.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.4
    ml = b3d.mat('liq', (0.95, 0.72, 0.2), rough=0.15, coat=0.3); glow(ml, (0.95, 0.7, 0.2), 0.6)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.8)
    btl = b3d.mat('btl', (0.05, 0.22, 0.12), rough=0.2, coat=0.6); foil = b3d.mat('foil', (0.85, 0.65, 0.2), rough=0.3, metal=0.8)
    yel = b3d.mat('yel', (1.0, 0.8, 0.2), rough=0.4, coat=0); glow(yel, (1.0, 0.8, 0.2), 1.5)
    for r in range(ROWS):
        for c in range(r + 1):
            f = lv[r][c] if after else 0
            glass((c - r / 2) * SPX, (ROWS - 1 - r) * SPZ, f, mg, ml, mint if after and f == 1 else None)
    top = (ROWS - 1) * SPZ + 0.6
    piv = bpy.data.objects.new('piv', None); bpy.context.collection.objects.link(piv)
    parts = []
    bpy.ops.mesh.primitive_cylinder_add(radius=0.16, depth=0.7, location=(0, 0, 0.35), vertices=32); parts.append(bpy.context.object); bpy.context.object.data.materials.append(btl)
    bpy.ops.mesh.primitive_cone_add(radius1=0.16, radius2=0.06, depth=0.22, location=(0, 0, 0.81), vertices=32); parts.append(bpy.context.object); bpy.context.object.data.materials.append(btl)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.065, depth=0.2, location=(0, 0, 1.0), vertices=32); parts.append(bpy.context.object); bpy.context.object.data.materials.append(foil)
    for o in parts: o.parent = piv
    piv.location = (-0.8, 0, top + 0.6); piv.rotation_euler = (0, math.radians(118), 0)
    if not after:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.32, location=(0.07, 0, top - 0.02), vertices=12); bpy.context.object.data.materials.append(ml)
    text(f'{BOARDS[k]}잔', (-1.25, -0.3, top - 0.25), 0.42, yel)
    b3d.stack_camera((0, 0, 1.25), 4.3, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((820, 860), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
