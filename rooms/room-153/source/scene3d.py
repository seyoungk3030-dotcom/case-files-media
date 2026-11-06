"""ROOM 153 3D sprites: a wooden ruler stick (0-10 cm) with ants walking on it, a white arrow over each ant showing which
way it walks; one ant is red. p*: the start. a*: the red ant falling off the end it really leaves from (mint ring)."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, L
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U = 0.62; EL = 30.0


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def X(p): return (p - L / 2) * U


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - EL), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def ball(loc, sc, m):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=loc, segments=24, ring_count=12); o = bpy.context.object; o.scale = sc; o.data.materials.append(m); return o


def ant(x, d, m, z=0.2, tilt=0.0):
    parts = []
    for dx, sc in ((-0.17, (0.12, 0.08, 0.075)), (0.0, (0.07, 0.055, 0.055)), (0.13, (0.07, 0.065, 0.06))):
        parts.append(ball((x + d * dx, 0, z + 0.07), sc, m))
    for i, dx in enumerate((-0.04, 0.0, 0.04)):
        for s in (-1, 1):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.2, location=(x + d * dx * 1.5 + d * (i - 1) * 0.03, s * 0.08, z + 0.035), vertices=8)
            o = bpy.context.object; o.rotation_euler = (s * 1.05, 0, d * (i - 1) * 0.5); o.data.materials.append(m); parts.append(o)
    for s in (-1, 1):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=0.16, location=(x + d * 0.24, s * 0.04, z + 0.15), vertices=8)
        o = bpy.context.object; o.rotation_euler = (s * 0.5, d * 0.9, 0); o.data.materials.append(m); parts.append(o)
    if tilt:
        piv = bpy.data.objects.new('piv', None); bpy.context.collection.objects.link(piv); piv.location = (x, 0, z)
        for o in parts: o.parent = piv; o.matrix_parent_inverse = piv.matrix_world.inverted()
        piv.rotation_euler = (0, -d * tilt, 0)


def arrow(x, d, m):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.26, location=(x - d * 0.04, 0, 0.62)); o = bpy.context.object
    o.rotation_euler = (0, math.pi / 2, 0); o.data.materials.append(m)
    bpy.ops.mesh.primitive_cone_add(radius1=0.075, depth=0.14, location=(x + d * 0.14, 0, 0.62), vertices=24); o = bpy.context.object
    o.rotation_euler = (0, d * math.pi / 2, 0); o.data.materials.append(m)


def scene(k, after):
    b = BOARDS[k]
    wood = b3d.mat('wood', (0.55, 0.36, 0.16), rough=0.7, coat=0); wood.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0.15
    ink = b3d.mat('ink', (0.08, 0.05, 0.03), rough=1.0, coat=0); wht = b3d.mat('wht', (0.95, 0.95, 0.95), rough=0.5, coat=0); glow(wht, (1, 1, 1), 0.6)
    blk = b3d.mat('blk', (0.03, 0.03, 0.035), rough=0.35, coat=0.3); red = b3d.mat('red', (0.9, 0.08, 0.06), rough=0.35, coat=0.3); glow(red, (0.9, 0.1, 0.05), 0.4)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.5)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.09)); o = bpy.context.object; o.scale = (L * U + 0.08, 0.5, 0.18); o.data.materials.append(wood); b3d.bevel(o, 0.02)
    for p in range(L + 1):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(X(p), -0.17, 0.181)); o = bpy.context.object; o.scale = (0.025, 0.16 if p % 5 else 0.24, 0.004); o.data.materials.append(ink)
        text(str(p), (X(p), -0.48, 0.05), 0.2, wht)
    if not after:
        for i, (p, d) in enumerate(zip(b['pos'], b['dir'])):
            ant(X(p), d, red if i == b['red'] else blk); arrow(X(p), d, red if i == b['red'] else wht)
    else:
        t, side = RES[k]; x = X(0) + 0.05 if side == 'L' else X(L) - 0.05; d = -1 if side == 'L' else 1
        ant(x, d, red)
        bpy.ops.mesh.primitive_cone_add(radius1=0.09, depth=0.18, location=(x + d * 0.45, 0, 0.0), vertices=24, rotation=(math.pi, 0, 0)); bpy.context.object.data.materials.append(mint)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.3, location=(x + d * 0.45, 0, 0.22)); bpy.context.object.data.materials.append(mint)
        bpy.ops.mesh.primitive_torus_add(location=(x, 0, 0.27), major_radius=0.36, minor_radius=0.035, major_segments=48, rotation=(math.radians(90 - EL), 0, 0))
        bpy.context.object.data.materials.append(mint)
    b3d.stack_camera((0, -0.1, 0.25), L * U + 1.8, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1200, 330), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
