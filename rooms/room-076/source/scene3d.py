"""ROOM 076 3D sprites, one small diorama per trap question: A shirts on a clothesline under a sun, B a row of
5 machines each with a part, C three eggs in a pot on a stove, D a running track with runners 1 and 2 and you (coral)
right behind runner 2. a*: the same scene with a glowing badge object (clock / tick) handled in the cards."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
import b3d
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
X90 = (math.radians(90), 0, 0)


def label(s, loc, size, m, rot=X90):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.03; t.data.materials.append(m)


def box(loc, scale, m, bev=0.04, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def cyl(loc, r, d, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, rotation=rot); o = bpy.context.object; o.data.materials.append(m); return o


def ball(loc, r, m, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=48, ring_count=24); o = bpy.context.object
    o.scale = scale; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def glow(m, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
    q.inputs['Emission Strength'].default_value = s; return m


def shirt(x, z, m):
    box((x, 0, z), (0.7, 0.12, 0.85), m, 0.08)
    for s in (-1, 1): box((x + s * 0.45, 0, z + 0.25), (0.35, 0.11, 0.3), m, 0.07, rot=(0, math.radians(-30 * s), 0))
    box((x - 0.12, 0.02, z + 0.45), (0.06, 0.16, 0.18), b3d.mat('peg', (0.95, 0.75, 0.2), rough=0.4), 0.02)
    box((x + 0.12, 0.02, z + 0.45), (0.06, 0.16, 0.18), b3d.mat('peg', (0.95, 0.75, 0.2), rough=0.4), 0.02)


def sA():
    pole = b3d.mat('pole', (0.6, 0.62, 0.68), rough=0.3, metal=0.6)
    for x in (-2.0, 2.0): cyl((x, 0, 1.0), 0.06, 2.0, pole)
    cyl((0, 0, 1.95), 0.015, 4.0, b3d.mat('rope', (0.9, 0.9, 0.85)), rot=(0, math.radians(90), 0))
    for x, c in zip((-1.2, 0, 1.2), [(0.35, 0.6, 0.95), (0.95, 0.42, 0.35), (0.3, 0.78, 0.55)]): shirt(x, 1.48, b3d.mat(f's{x}', c, rough=0.6, coat=0.1))
    ball((1.9, 0.4, 2.8), 0.38, glow(b3d.mat('sun', (1.0, 0.75, 0.15), rough=0.4), 1.2))
    b3d.stack_camera((0, 0, 1.6), 5.4, az=0.0, el=8.0)


def sB():
    body = b3d.mat('mach', (0.45, 0.55, 0.95), rough=0.35, coat=0.6); dark = b3d.mat('dk', (0.12, 0.15, 0.22), rough=0.3)
    part = b3d.mat('part', (0.98, 0.72, 0.2), rough=0.3, metal=0.4); belt = b3d.mat('belt', (0.2, 0.21, 0.25), rough=0.8)
    for i in range(5):
        x = -2.4 + i * 1.2
        box((x, 0, 0.55), (0.9, 0.8, 1.1), body, 0.1); box((x, -0.41, 0.75), (0.5, 0.02, 0.35), dark, 0.03)
        cyl((x, -0.43, 0.75), 0.11, 0.04, part, rot=X90)
        bpy.ops.mesh.primitive_torus_add(location=(x, -0.62, 0.2), rotation=X90, major_radius=0.14, minor_radius=0.06)
        bpy.context.object.data.materials.append(part)
    box((0, -0.62, 0.06), (6.2, 0.4, 0.08), belt, 0.02)
    b3d.stack_camera((0, 0, 0.6), 6.4, az=0.0, el=14.0)


def sC():
    pot = b3d.mat('pot', (0.85, 0.3, 0.3), rough=0.25, coat=0.8); water = b3d.mat('water', (0.55, 0.8, 1.0), rough=0.05, coat=1.0)
    egg = b3d.mat('egg', (0.98, 0.93, 0.82), rough=0.45); stove = b3d.mat('stove', (0.22, 0.24, 0.3), rough=0.4)
    fire = glow(b3d.mat('fire', (0.3, 0.55, 1.0), rough=0.4), 2.0)
    box((0, 0, 0.12), (3.2, 2.0, 0.24), stove, 0.06)
    bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0.3), major_radius=0.85, minor_radius=0.04); bpy.context.object.data.materials.append(fire)
    bpy.ops.mesh.primitive_cylinder_add(radius=1.05, depth=0.9, location=(0, 0, 0.8)); p = bpy.context.object; p.data.materials.append(pot)
    m = p.modifiers.new('s', 'SOLIDIFY'); m.thickness = 0.06; bpy.ops.object.shade_smooth()
    bm = p.data; [f for f in bm.polygons]
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='DESELECT'); bpy.ops.object.mode_set(mode='OBJECT')
    for f in p.data.polygons: f.select = f.normal.z > 0.9
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.delete(type='FACE'); bpy.ops.object.mode_set(mode='OBJECT')
    for s in (-1, 1): box((s * 1.2, 0, 1.15), (0.3, 0.12, 0.08), pot, 0.03)
    cyl((0, 0, 1.05), 0.98, 0.04, water)
    for x, y in ((-0.45, 0.1), (0.4, 0.2), (0, -0.35)): ball((x, y, 1.12), 0.25, egg, (1, 1, 1.3))
    b3d.stack_camera((0, 0, 0.8), 4.2, az=0.0, el=38.0)


def runner(x, m, num, ink):
    ball((x, 0, 1.55), 0.22, m); box((x, 0, 1.0), (0.42, 0.3, 0.7), m, 0.12)
    box((x - 0.12, 0, 0.35), (0.14, 0.14, 0.6), m, 0.05, rot=(0, math.radians(18), 0))
    box((x + 0.12, 0, 0.35), (0.14, 0.14, 0.6), m, 0.05, rot=(0, math.radians(-18), 0))
    if num:
        box((x, -0.16, 1.02), (0.3, 0.02, 0.3), b3d.mat('bib', (0.97, 0.98, 1.0), rough=0.5), 0.02)
        label(num, (x, -0.19, 1.02), 0.26, ink)


def sD():
    track = b3d.mat('track', (0.85, 0.38, 0.3), rough=0.8, coat=0); line = b3d.mat('ln', (0.97, 0.97, 0.97), rough=0.6, coat=0)
    ink = b3d.mat('ink', (0.06, 0.09, 0.18), rough=0.4)
    box((0, 0, -0.05), (6.6, 1.6, 0.1), track, 0.01)
    for y in (-0.7, 0.7): box((0, y, 0.002), (6.6, 0.04, 0.004), line, 0.002)
    runner(2.2, b3d.mat('r1', (0.95, 0.8, 0.25), rough=0.4, coat=0.5), '1', ink)
    runner(0.3, b3d.mat('r2', (0.35, 0.6, 0.95), rough=0.4, coat=0.5), '2', ink)
    runner(-1.0, b3d.mat('me', (0.98, 0.45, 0.4), rough=0.4, coat=0.5), '', ink)
    for i in range(3): box((-1.6 - i * 0.3, -0.05, 1.0 + (i - 1) * 0.18), (0.22, 0.03, 0.04), line, 0.01)
    b3d.stack_camera((0.5, 0, 0.9), 5.6, az=0.0, el=8.0)


only = sys.argv[1:]
for k, f in zip('ABCD', (sA, sB, sC, sD)):
    if only and k not in only: continue
    b3d.reset((1000, 640), 40); b3d.lights(8)
    t = time.time(); f(); b3d.render(f'{OUT}/p{k}.png'); print('p' + k, round(time.time() - t, 1), flush=True)
