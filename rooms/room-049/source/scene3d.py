"""ROOM 049 3D sprites: 'pipes' is a board with taps A-D on top, six glass cups 1-6 below, and four tangled pipes in
one colour (each at its own depth, so they pass over and under each other). 'answer' gives each pipe and the cup it
fills its own colour. Optional argv after '--': names to render."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import CUPS, TAPS, Z, PIPES, trace
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
COLS = {'A': (0.95, 0.62, 0.10), 'B': (0.05, 0.62, 0.48), 'C': (0.90, 0.16, 0.13), 'D': (0.25, 0.45, 0.95)}
DEPTH = {'A': -0.45, 'B': -0.25, 'C': -0.65, 'D': -0.05}


def text(font, s, loc, m, size):
    bpy.ops.object.text_add(location=loc, rotation=(math.pi / 2, 0, 0)); t = bpy.context.object
    t.data.font = font; t.data.body = s; t.data.size = size; t.data.extrude = 0.02
    t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.materials.append(m); return t


def pipe(k, m):
    cu = bpy.data.curves.new(k, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.11; cu.bevel_resolution = 6
    sp = cu.splines.new('NURBS'); pts = list(zip(PIPES[k], Z)); sp.points.add(len(pts) - 1)
    for p, (x, z) in zip(sp.points, pts): p.co = (x, DEPTH[k], z, 1)
    sp.order_u = 4; sp.use_endpoint_u = True; sp.resolution_u = 24
    o = bpy.data.objects.new(k, cu); bpy.context.collection.objects.link(o); o.data.materials.append(m)


def scene(name):
    ans = name == 'answer'
    b3d.reset((1000, 1050), 40); b3d.lights(7)
    font = bpy.data.fonts.load(os.path.join(HERE, '../../../kit/fonts/P-Bold.otf'))
    b3d.stack_camera((0, 0, 0.3), 9.6, 0.0, 8.0)
    board = b3d.mat('board', (0.20, 0.26, 0.36), rough=0.6, coat=0.1)
    steel = b3d.mat('steel', (0.75, 0.78, 0.82), rough=0.3, metal=0.9, coat=0.2)
    gray = b3d.mat('gray', (0.78, 0.80, 0.84), rough=0.35, metal=0.2, coat=0.4)
    ink = b3d.mat('ink', (0.08, 0.10, 0.15), rough=0.4, coat=0.1)
    white = b3d.mat('white', (0.95, 0.95, 0.93), rough=0.4, coat=0.2)
    glass = b3d.mat('glass', (0.80, 0.90, 0.98), rough=0.05, coat=0.0)
    p = glass.node_tree.nodes['Principled BSDF']; p.inputs['Alpha'].default_value = 0.35
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.25, 0.35)); o = bpy.context.object
    o.scale = (9.4, 0.2, 6.6); o.data.materials.append(board); b3d.bevel(o, 0.12, 3)
    got = {trace(k)[0]: k for k in 'ABCD'}
    for k, x in TAPS.items():   # tap: a pipe stub with a handle and a letter disc above
        bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.5, location=(x, DEPTH[k], 2.95)); o = bpy.context.object; o.data.materials.append(steel)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=0.12, location=(x, -0.1, 3.35), rotation=(math.pi / 2, 0, 0)); o = bpy.context.object
        o.data.materials.append(b3d.mat('t' + k, COLS[k], rough=0.3, coat=0.5) if ans else white); b3d.bevel(o, 0.03, 2)
        text(font, k, (x, -0.17, 3.33), ink, 0.48)
    for n, x in CUPS.items():
        k = got.get(n)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.55, depth=1.0, location=(x, -0.3, -2.4), vertices=48); o = bpy.context.object
        o.data.materials.append(glass)
        if ans and k:
            w = b3d.mat('w' + k, COLS[k], rough=0.2, coat=0.3)
            bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=0.6, location=(x, -0.3, -2.6), vertices=48); bpy.context.object.data.materials.append(w)
        text(font, str(n), (x, -0.95, -3.3), ink if not ans else ink, 0.5)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.34, depth=0.08, location=(x, -0.9, -3.3), rotation=(math.pi / 2, 0, 0)); o = bpy.context.object
        o.data.materials.append(white)
    for k in 'ABCD':
        pipe(k, b3d.mat('p' + k, COLS[k], rough=0.3, coat=0.5) if ans else gray)


names = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['pipes', 'answer']
for name in names:
    t = time.time(); scene(name); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
