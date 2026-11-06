"""ROOM 146 3D sprites, seen from the front: identical rubber balloons on short necks above one brass air pipe, each
with a numbered tag and its own tap (red handle across the neck = closed, along the neck = open). p*: the start
sizes. a*: sizes after the open taps are opened; a coral ring shows each balloon's starting size and the one that grew
gets a mint ring."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, END, GROW
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
EL = 8.0; R0 = 0.33; GAP = 2.0; ZP = 0.0
COLS = [(0.95, 0.35, 0.3), (0.3, 0.6, 0.95), (0.95, 0.75, 0.2), (0.6, 0.4, 0.9)]


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - EL), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def cyl(loc, r, d, m, rot=(0, 0, 0), v=24):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, rotation=rot, vertices=v); bpy.context.object.data.materials.append(m); return bpy.context.object


def ring(x, z, r, m, w=0.025):
    bpy.ops.mesh.primitive_torus_add(location=(x, -0.05 - r * 0.0, z), rotation=(math.radians(90 - EL), 0, 0), major_radius=r, minor_radius=w, major_segments=64)
    bpy.context.object.data.materials.append(m)


def scene(k, after):
    b = BOARDS[k]; labs = list(b); n = len(labs)
    brass = b3d.mat('brass', (0.75, 0.55, 0.2), rough=0.3, metal=0.9, coat=0); red = b3d.mat('red', (0.85, 0.1, 0.08), rough=0.4, coat=0); grn = b3d.mat('grn', (0.1, 0.7, 0.25), rough=0.4, coat=0)
    ink = b3d.mat('ink', (0.97, 0.97, 1.0), rough=0.6, coat=0); glow(ink, (0.97, 0.97, 1.0), 0.6)
    tag = b3d.mat('tag', (0.1, 0.12, 0.16), rough=0.6, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.5)
    cor = b3d.mat('cor', (0.95, 0.42, 0.35), rough=0.5, coat=0); glow(cor, (0.95, 0.42, 0.35), 1.2)
    xs = [(i - (n - 1) / 2) * GAP for i in range(n)]
    cyl((0, 0, ZP), 0.09, xs[-1] - xs[0] + 1.0, brass, rot=(0, math.radians(90), 0))
    for e in (xs[0] - 0.5, xs[-1] + 0.5): bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(e, 0, ZP)); bpy.context.object.data.materials.append(brass)
    for i, lab in enumerate(labs):
        L0, op = b[lab]; L = END[k].get(lab, L0) if after else L0; r = L * R0; x = xs[i]
        cyl((x, 0, ZP + 0.25), 0.06, 0.5, brass)
        hz = ZP + 0.3
        hm = red if not op else grn
        cyl((x, -0.1, hz), 0.05, 0.5, hm, rot=(0, math.radians(90), 0) if not op else (0, 0, 0))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(x, -0.1, hz)); bpy.context.object.data.materials.append(hm)
        cz = ZP + 0.5 + r * 0.95
        bpy.ops.mesh.primitive_cone_add(radius1=0.03, radius2=0.12, depth=0.14, location=(x, 0, ZP + 0.52)); bpy.context.object.data.materials.append(b3d.mat(f'b{i}', COLS[i % 4], rough=0.35, coat=0.6))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(x, 0, cz), segments=48, ring_count=24); o = bpy.context.object
        o.scale = (1, 1, 1.12); o.data.materials.append(b3d.mat(f'b{i}', COLS[i % 4], rough=0.35, coat=0.6))
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, -0.2, ZP - 0.45)); o = bpy.context.object; o.scale = (0.5, 0.05, 0.42); o.data.materials.append(tag); b3d.bevel(o, 0.05)
        text(str(lab), (x, -0.26, ZP - 0.45), 0.36, ink)
        if after:
            r0 = L0 * R0; ring(x, ZP + 0.5 + r0 * 0.95, r0 * 1.06, cor)
            if lab in GROW[k]: ring(x, cz, r * 1.12, mint, 0.04)
    b3d.stack_camera((0, 0, 1.25), max(n * GAP + 0.6, 6.4), az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((960, 600), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
