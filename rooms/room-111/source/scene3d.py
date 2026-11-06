"""ROOM 111 3D sprites: cut-away side view of a dark cup with four gold coins on its bottom, numbered amber tags on
the front of the base, a big eye up and to the left, and a dashed sight line from the eye over the near rim. A mint
line on the back wall marks how high the water will come. a*: the water is in (clear blue) and a mint bent ray runs
from the newly visible coin, bends at the surface and reaches the eye; that coin gets a mint ring."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
D = 1.5   # cup depth (y)


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def box(m, c, s, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def rod(a, b, r, m):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=12); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y'); o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = True
    return o


def dashed(a, b, r, m, seg=0.22, gap=0.14):
    a, b = Vector(a), Vector(b); L = (b - a).length; u = (b - a) / L; t = 0.0
    while t < L:
        rod(a + u * t, a + u * min(t + seg, L), r, m); t += seg + gap


def scene(k, after):
    b = BOARDS[k]; (ex, ez), W, H, h = b['eye'], b['W'], b['H'], b['h']; new = RES[k][0][0]
    cup = b3d.mat('cup', (0.16, 0.19, 0.27), rough=0.55, coat=0.1); back = b3d.mat('back', (0.07, 0.09, 0.14), rough=0.8, coat=0)
    gold = b3d.mat('gold', (0.95, 0.68, 0.16), rough=0.3, coat=0.3); glow(gold, (0.95, 0.65, 0.1), 0.25)
    amber = b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0.1); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.5)
    line = b3d.mat('line', (0.85, 0.88, 0.95), rough=0.5, coat=0); glow(line, (0.85, 0.88, 0.95), 0.8)
    white = b3d.mat('white', (0.95, 0.96, 0.98), rough=0.3, coat=0.3); iris = b3d.mat('iris', (0.1, 0.45, 0.85), rough=0.3, coat=0.3)
    water = b3d.mat('water', (0.25, 0.55, 0.95), rough=0.05, coat=0.3)
    wq = water.node_tree.nodes['Principled BSDF']; wq.inputs['Alpha'].default_value = 0.42; wq.inputs['Specular IOR Level'].default_value = 0.0
    T = 0.16
    box(cup, (-T / 2, 0, H / 2 - 0.3), (T, D, H + 0.6), 0.03)                 # near wall (eye side)
    box(cup, (W + T / 2, 0, H / 2 - 0.3), (T, D, H + 0.6), 0.03)              # far wall
    box(cup, (W / 2, 0, -0.3), (W + 2 * T, D, 0.6), 0.03)                     # base
    box(back, (W / 2, D / 2 - 0.02, H / 2), (W, 0.04, H), 0.0)                # back wall
    box(mint if not after else back, (W / 2, D / 2 - 0.06, h), (W, 0.02, 0.035), 0.0)   # future water level mark
    for n, xc in b['coins'].items():
        bpy.ops.mesh.primitive_cylinder_add(radius=0.17, depth=0.1, location=(xc, -0.1, 0.05), vertices=40)
        bpy.context.object.data.materials.append(gold)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.04, location=(xc, -D / 2 - 0.02, -0.3), rotation=(math.radians(90), 0, 0), vertices=40)
        bpy.context.object.data.materials.append(amber); text(str(n), (xc, -D / 2 - 0.05, -0.3), 0.3, ink)
        if after and n == new:
            bpy.ops.mesh.primitive_torus_add(location=(xc, -0.1, 0.06), major_radius=0.24, minor_radius=0.035); bpy.context.object.data.materials.append(mint)
    # the eye, looking at the near rim
    Y = -0.85; eye = Vector((ex, Y, ez)); look = (Vector((0, Y, H)) - eye).normalized()
    face = Vector((look.x * 0.55, -0.8, look.z * 0.55)).normalized()
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.34, location=eye, segments=48, ring_count=24); o = bpy.context.object; o.data.materials.append(white)
    for p in o.data.polygons: p.use_smooth = True
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.17, location=eye + face * 0.24, segments=32, ring_count=16); o = bpy.context.object; o.data.materials.append(iris)
    o.scale = (1, 1, 1)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.09, location=eye + face * 0.33, segments=24, ring_count=12); bpy.context.object.data.materials.append(ink)
    # dry sight line over the rim, down to the bottom
    rim = Vector((0, Y, H)); u = (rim - eye); t = (0 - eye.z) / u.z; end = eye + u * t
    dashed(eye + look * 0.4, end, 0.025, line)
    if after:
        wo = box(water, (W / 2, -0.04, h / 2), (W - 0.01, D - 0.1, h), 0.0); wo.visible_glossy = False; wo.visible_shadow = False
        s = RES[k][2][new][2]; xc = b['coins'][new]
        rod((xc, Y, 0.1), (s, Y, h), 0.045, mint); rod((s, Y, h), tuple(eye + (Vector((s, Y, h)) - eye).normalized() * 0.36), 0.045, mint)
    b3d.stack_camera((0.55, 0, 2.15), 8.2, az=0.0, el=12.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 1000), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
