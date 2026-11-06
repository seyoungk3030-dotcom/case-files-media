"""ROOM 144 3D sprites: two throws of four yut sticks on a straw mat, seen from above at a slant. Flat side up = pale
wood, round back up = dark bark. The 빽도 stick has a red 빽 mark on its flat side. p*: the throws. a*: each throw's
name and step count float above it in mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, NAME, value
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
EL = 58.0; L = 1.5; W = 0.3


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m, rx=None):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - EL) if rx is None else rx, 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def stick(x, y, flat, back, ang, M):
    if flat:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.07)); o = bpy.context.object; o.scale = (W, L, 0.14); o.rotation_euler = (0, 0, ang)
        o.data.materials.append(M['flat']); b3d.bevel(o, 0.05, 3)
        for dy in (-0.45, 0.45):
            for s in (1, -1):
                bpy.ops.mesh.primitive_cube_add(size=1, location=(x + dy * math.sin(-ang), y + dy * math.cos(ang), 0.142)); o = bpy.context.object
                o.scale = (0.03, 0.2, 0.004); o.rotation_euler = (0, 0, ang + s * math.radians(40)); o.data.materials.append(M['mark'])
        if back:
            text('빽', (x, y, 0.15), 0.36, M['red'], rx=0); bpy.context.object.rotation_euler = (0, 0, ang)
    else:
        bpy.ops.mesh.primitive_cylinder_add(radius=W / 2 + 0.01, depth=L, location=(x, y, 0.08), rotation=(math.radians(90), 0, ang), vertices=40)
        o = bpy.context.object; o.scale = (1, 1, 1); o.data.materials.append(M['bark']); b3d.bevel(o, 0.05, 3)


def scene(k, after):
    M = {'flat': b3d.mat('flat', (0.62, 0.46, 0.26), rough=0.8, coat=0), 'bark': b3d.mat('bark', (0.3, 0.15, 0.06), rough=0.7, coat=0.1),
         'mark': b3d.mat('mark', (0.35, 0.2, 0.08), rough=0.8, coat=0), 'red': b3d.mat('red', (0.85, 0.08, 0.06), rough=0.5, coat=0)}
    M['flat'].node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0.1
    mat_ = b3d.mat('straw', (0.2, 0.15, 0.07), rough=0.95, coat=0); mat_.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0
    rim = b3d.mat('rim', (0.25, 0.12, 0.05), rough=0.8, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.2)
    ink = b3d.mat('ink', (0.97, 0.97, 1.0), rough=0.6, coat=0); glow(ink, (0.97, 0.97, 1.0), 0.5)
    bpy.ops.mesh.primitive_cylinder_add(radius=2.45, depth=0.06, location=(0, 0, -0.03), vertices=96); o = bpy.context.object; o.scale = (1.0, 0.78, 1); o.data.materials.append(mat_)
    bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0), major_radius=2.45, minor_radius=0.06, major_segments=96); o = bpy.context.object; o.scale = (1.0, 0.78, 1); o.data.materials.append(rim)
    jit = [(-0.06, 0.05, 6), (0.04, -0.08, -4), (-0.03, 0.06, 3), (0.05, -0.04, -7)]
    for g, t in enumerate(BOARDS[k]):
        gx = -1.2 + 2.4 * g
        text(f'{g + 1}번째', (gx, -1.35, 0.05), 0.26, ink)
        for i, ch in enumerate(t):
            dx, dy, a = jit[(i + g) % 4]
            stick(gx + (i - 1.5) * 0.44 + dx, 0.12 + dy, ch == 'F', i == 0, math.radians(a), M)
        if after:
            v = value(t); text(f'{NAME[v]} {v:+d}', (gx, 1.3, 0.35), 0.38, mint)
    b3d.stack_camera((0, 0.0, 0.1), 5.2, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
