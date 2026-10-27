"""ROOM 048 3D sprites: 'mirror' is a wall mirror whose reflection shows the clock reversed (numbers flipped, hands
mirrored); 'real' is the same clock as it really is, for the answer. Optional argv after '--': names to render."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import REAL, angles
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)


def box(m, loc, size, rot=(0, 0, 0), parent=None, bev=0.02):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
    o.scale = size; o.rotation_euler = rot; o.data.materials.append(m); b3d.bevel(o, bev, 2)
    if parent: o.parent = parent
    return o


def clock(parent, font, M):
    R = 1.6
    bpy.ops.mesh.primitive_cylinder_add(radius=R + 0.14, depth=0.3, location=(0, 0.05, 0), rotation=(math.pi / 2, 0, 0), vertices=96)
    o = bpy.context.object; o.data.materials.append(M['rim']); b3d.bevel(o, 0.08, 3); o.parent = parent
    bpy.ops.mesh.primitive_cylinder_add(radius=R, depth=0.3, location=(0, 0.0, 0), rotation=(math.pi / 2, 0, 0), vertices=96)
    o = bpy.context.object; o.data.materials.append(M['face']); o.parent = parent
    for i in range(60):
        a = math.radians(i * 6); big = i % 5 == 0; r = R - (0.16 if big else 0.1)
        box(M['ink'], (math.sin(a) * r, -0.16, math.cos(a) * r), (0.05 if big else 0.025, 0.02, 0.2 if big else 0.09), (0, a, 0), parent, 0.005)
    for n in range(1, 13):
        a = math.radians(n * 30); r = R - 0.55
        bpy.ops.object.text_add(location=(math.sin(a) * r, -0.16, math.cos(a) * r), rotation=(math.pi / 2, 0, 0)); t = bpy.context.object
        t.data.font = font; t.data.body = str(n); t.data.size = 0.42; t.data.extrude = 0.01
        t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.materials.append(M['ink']); t.parent = parent
    ha, ma = angles(*REAL)
    for ang, L, w, m in ((ha, 0.85, 0.11, M['hour']), (ma, 1.3, 0.07, M['minute'])):
        a = math.radians(ang)
        box(m, (math.sin(a) * L * 0.42, -0.22 if m is M['minute'] else -0.19, math.cos(a) * L * 0.42), (w, 0.03, L), (0, a, 0), parent, 0.01)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.1, location=(0, -0.25, 0), rotation=(math.pi / 2, 0, 0))
    o = bpy.context.object; o.data.materials.append(M['cap']); o.parent = parent


def scene(name):
    b3d.reset((900, 1000), 48); b3d.lights(6)
    font = bpy.data.fonts.load(os.path.join(HERE, '../../../kit/fonts/P-Bold.otf'))
    b3d.stack_camera((0, 0, 0), 5.2, 0.0, 6.0)
    M = {'rim': b3d.mat('rim', b3d.PAL['mint'], rough=0.3, coat=0.5), 'face': b3d.mat('face', (0.95, 0.94, 0.90), rough=0.45, coat=0.2),
         'ink': b3d.mat('ink', (0.08, 0.10, 0.15), rough=0.4, coat=0.1), 'hour': b3d.mat('hour', (0.10, 0.13, 0.20), rough=0.35, coat=0.4),
         'minute': b3d.mat('minute', b3d.PAL['coral'], rough=0.3, coat=0.5), 'cap': b3d.mat('cap', (0.95, 0.62, 0.10), rough=0.3, coat=0.5)}
    root = bpy.data.objects.new('root', None); bpy.context.collection.objects.link(root)
    if name == 'mirror':
        frame = b3d.mat('frame', (0.80, 0.66, 0.40), rough=0.3, metal=0.8, coat=0.3)
        glass = b3d.mat('glass', (0.55, 0.70, 0.80), rough=0.08, metal=0.3, coat=0.8)
        W, H = 4.1, 4.5
        box(glass, (0, 0.35, 0), (W, 0.06, H), bev=0.02)
        for x, z, sx, sz in ((0, H / 2, W + 0.3, 0.3), (0, -H / 2, W + 0.3, 0.3), (W / 2, 0, 0.3, H + 0.3), (-W / 2, 0, 0.3, H + 0.3)):
            box(frame, (x, 0.2, z), (sx, 0.32, sz), bev=0.08)
        for i in range(3):   # a few light streaks on the glass
            box(b3d.mat(f'sh{i}', (1, 1, 1), rough=0.05, coat=0), (-1.3 + i * 0.35, 0.3, 1.2 - i * 0.2), (0.06, 0.01, 0.9), (0, math.radians(35), 0), bev=0.0)
        root.scale = (-0.86, 0.86, 0.86)
    clock(root, font, M)


names = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['mirror', 'real']
for name in names:
    t = time.time(); scene(name); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
