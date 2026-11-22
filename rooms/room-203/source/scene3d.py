"""ROOM 203 3D sprites: a row of n game-show doors. The player's door (leftmost) has an amber marker above it; the host has
opened k other doors (the rightmost ones), each showing an empty room with a grey X. a*: the door(s) the player ends up
with (their own for stay, the other closed ones for switch) glow mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
DOORC = [(0.85, 0.22, 0.2), (0.15, 0.45, 0.9), (0.95, 0.7, 0.12), (0.2, 0.7, 0.45)]


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def box(m, loc, sc, bev=0.03, rz=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=(0, 0, rz)); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.pi / 2, 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def scene(key, after):
    n, k, strat, g = BOARDS[key]; W, Hd, gap = 0.9, 1.7, 0.25
    xs = [(i - (n - 1) / 2) * (W + gap) for i in range(n)]
    opened = set(range(n - k, n)); final = {0} if strat == 'stay' else set(range(1, n - k))
    wall = b3d.mat('wall', (0.16, 0.18, 0.26), rough=0.6, coat=0); frame = b3d.mat('frame', (0.85, 0.78, 0.6), rough=0.3, metal=0.5, coat=0)
    dark = b3d.mat('dark', (0.03, 0.03, 0.05), rough=0.9, coat=0); knob = b3d.mat('knob', (0.95, 0.8, 0.3), rough=0.2, metal=1.0, coat=0)
    span = n * (W + gap) + 0.4
    box(wall, (0, 0.12, Hd / 2 + 0.2), (span, 0.12, Hd + 0.6), 0.03)
    box(b3d.mat('floor', (0.35, 0.3, 0.3), rough=0.6, coat=0.2), (0, -0.4, -0.05), (span, 1.0, 0.1), 0.02)
    mint = glowm('mint', (0.2, 0.95, 0.65), 2.0)
    for i, x in enumerate(xs):
        fm = mint if (after and i in final) else frame
        box(fm, (x, 0.0, Hd + 0.05), (W + 0.14, 0.12, 0.1), 0.02)
        for sx in (-1, 1): box(fm, (x + sx * (W / 2 + 0.035), 0.0, Hd / 2), (0.07, 0.12, Hd), 0.02)
        if i in opened:
            box(dark, (x, 0.05, Hd / 2), (W, 0.04, Hd), 0.0)
            text('X', (x, -0.01, Hd / 2), 0.7, glowm('xm', (0.6, 0.62, 0.68), 0.6))
            hx = x - W / 2; ang = math.radians(-70)
            box(b3d.mat(f'd{i}', DOORC[i], rough=0.3, coat=0.6), (hx + math.cos(ang) * W / 2, -0.02 + math.sin(ang) * W / 2, Hd / 2), (W, 0.06, Hd), 0.02, rz=ang)
        else:
            box(b3d.mat(f'd{i}', DOORC[i], rough=0.3, coat=0.6), (x, -0.02, Hd / 2), (W, 0.06, Hd), 0.02)
            box(b3d.mat(f'p{i}', tuple(c * 0.8 for c in DOORC[i]), rough=0.3, coat=0.6), (x, -0.06, Hd * 0.68), (W * 0.7, 0.02, Hd * 0.4), 0.01)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(x + W * 0.33, -0.1, Hd * 0.45)); bpy.context.object.data.materials.append(knob)
            text(str(i + 1), (x, -0.075, Hd * 0.3), 0.32, glowm('num', (1, 1, 1), 0.8))
    am = glowm('amber', (1.0, 0.72, 0.2), 1.6)
    bpy.ops.mesh.primitive_cone_add(radius1=0.18, radius2=0, depth=0.3, location=(xs[0], -0.05, Hd + 0.45), rotation=(math.pi, 0, 0))
    bpy.context.object.data.materials.append(am)
    b3d.stack_camera((0, 0, Hd / 2 + 0.15), span + 0.3, az=10.0, el=12.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((800, 560), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t, 1), flush=True)
