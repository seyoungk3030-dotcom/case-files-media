"""ROOM 071 3D sprites: a thin and a thick candle on a tray in front of a tile wall (lines every 0.22, numbered).
p*: both full and lit, '6칸'/'7칸' labels. a*: the first one burnt out (wax puddle), the other at what is left, amber."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, res
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U = 0.22
X90 = (math.radians(90), 0, 0)


def label(s, x, z, size, m, y=-0.6):
    bpy.ops.object.text_add(location=(x, y, z), rotation=X90); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def box(loc, scale, m, bev=0.02):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 2); return o


def glow(m, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
    q.inputs['Emission Strength'].default_value = s; return m


def candle(x, r, tiles, wax, wick, flame, lit=True):
    h = tiles * U
    if h <= 0:
        bpy.ops.mesh.primitive_cylinder_add(radius=r * 1.6, depth=0.03, location=(x, 0, 0.015)); bpy.context.object.data.materials.append(wax); return
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, vertices=48, location=(x, 0, h / 2)); o = bpy.context.object
    o.data.materials.append(wax); b3d.bevel(o, 0.015, 2)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.08, location=(x, 0, h + 0.04)); bpy.context.object.data.materials.append(wick)
    if lit:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(x, 0, h + 0.14)); f = bpy.context.object; f.scale = (1, 1, 1.9)
        f.data.materials.append(flame)


def scene(k, after):
    thin, thick = BOARDS[k]; v, first = res[k]; v = int(v)
    wax_t = b3d.mat('waxt', (0.98, 0.93, 0.80), rough=0.4, coat=0.3); wax_k = b3d.mat('waxk', (0.92, 0.42, 0.40), rough=0.4, coat=0.3)
    wick = b3d.mat('wick', (0.1, 0.1, 0.1), rough=0.8); flame = glow(b3d.mat('flame', (1.0, 0.55, 0.10), rough=0.5), 1.6)
    wall = b3d.mat('wall', (0.20, 0.25, 0.36), rough=0.6, coat=0); line = b3d.mat('line', (0.55, 0.62, 0.75), rough=0.6, coat=0)
    wood = b3d.mat('wood', (0.45, 0.32, 0.22), rough=0.6, coat=0.1); white = b3d.mat('white', (0.96, 0.97, 0.99), rough=0.4)
    soft = b3d.mat('soft', (0.75, 0.80, 0.90), rough=0.5); amber = glow(b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3), 0.7)
    box((0, 0.45, 1.15), (2.4, 0.05, 2.5), wall, 0.01)
    for i in range(1, 10):
        box((0.05, 0.41, i * U), (2.2, 0.02, 0.012), line, 0.002); label(str(i), -1.05, i * U, 0.15, soft, y=0.38)
    box((0, 0, -0.06), (2.4, 0.9, 0.12), wood, 0.03)
    xt, xk = -0.42, 0.45
    if after:
        if first == 'thin':
            candle(xt, 0.08, 0, wax_t, wick, flame); candle(xk, 0.2, v, wax_k, wick, flame)
            label(f'{v}칸', xk, v * U + 0.52, 0.28, amber); box((xk, 0.4, v * U), (0.6, 0.03, 0.025), amber, 0.004)
            label('꺼짐', xt, 0.3, 0.2, soft)
        else:
            candle(xk, 0.2, 0, wax_k, wick, flame); candle(xt, 0.08, v, wax_t, wick, flame)
            label(f'{v}칸', xt, v * U + 0.52, 0.28, amber); box((xt, 0.4, v * U), (0.5, 0.03, 0.025), amber, 0.004)
            label('꺼짐', xk, 0.3, 0.2, soft)
    else:
        candle(xt, 0.08, thin, wax_t, wick, flame); candle(xk, 0.2, thick, wax_k, wick, flame)
        label(f'{thin}칸', xt, thin * U + 0.5, 0.24, white); label(f'{thick}칸', xk, thick * U + 0.5, 0.24, white)
    label('얇은 초', xt, -0.2, 0.2, white, y=-0.48); label('굵은 초', xk, -0.2, 0.2, white, y=-0.48)
    b3d.stack_camera((0.0, 0, 1.08), 2.85, az=0.0, el=8.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((820, 900), 40); b3d.lights(5)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
