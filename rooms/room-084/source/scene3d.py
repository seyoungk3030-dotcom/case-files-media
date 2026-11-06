"""ROOM 084 3D sprites: a wooden-framed hourglass with N minute marks on each glass bulb (bulbs are cylinders so
sand height is proportional to minutes). p*: all sand on top. a*: the sand after the steps, top sand glowing amber."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import GLASSES, END
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
X90 = (math.radians(90), 0, 0)
FR = {'A': (0.62, 0.42, 0.26), 'B': (0.35, 0.55, 0.85), 'C': (0.4, 0.7, 0.5), 'D': (0.75, 0.45, 0.65)}


def cyl(loc, r, d, m):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, vertices=64); o = bpy.context.object; o.data.materials.append(m)
    bpy.ops.object.shade_smooth(); return o


def label(s, x, z, size, m, y=-0.6):
    bpy.ops.object.text_add(location=(x, y, z), rotation=X90); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def glassy(name, col, a):
    m = b3d.mat(name, col, rough=0.05, coat=1.0); p = m.node_tree.nodes['Principled BSDF']; p.inputs['Alpha'].default_value = a
    try: m.surface_render_method = 'BLENDED'
    except Exception: m.blend_method = 'BLEND'
    return m


def scene(k, after):
    cap, steps = GLASSES[k]; top, bot = END[k] if after else (cap, 0)
    wood = b3d.mat('wood', FR[k], rough=0.45, coat=0.4); glass = glassy('glass', (0.85, 0.93, 1.0), 0.18)
    sand = b3d.mat('sand', (0.78, 0.52, 0.24), rough=0.8, coat=0); hot = b3d.mat('hot', (0.98, 0.62, 0.12), rough=0.6, coat=0)
    q = hot.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (0.98, 0.62, 0.12, 1); q.inputs['Emission Strength'].default_value = 0.5
    tick = b3d.mat('tick', (0.95, 0.96, 1.0), rough=0.4); ink = b3d.mat('ink', (0.95, 0.96, 1.0), rough=0.4)
    R, Hb, gap = 0.55, 1.8, 0.16
    zt0, zb0 = gap / 2, -gap / 2 - Hb
    cyl((0, 0, zt0 + Hb / 2), R, Hb, glass); cyl((0, 0, zb0 + Hb / 2), R, Hb, glass); cyl((0, 0, 0), 0.08, gap + 0.1, glass)
    if top: cyl((0, 0, zt0 + Hb * top / cap / 2), R - 0.03, Hb * top / cap, hot if after else sand)
    if bot: cyl((0, 0, zb0 + Hb * bot / cap / 2), R - 0.03, Hb * bot / cap, sand)
    for z0 in (zt0, zb0):
        for i in range(1, cap):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(-R - 0.02, -0.3, z0 + Hb * i / cap)); o = bpy.context.object
            o.scale = (0.18, 0.04, 0.025); o.data.materials.append(tick)
    for z in (zt0 + Hb + 0.12, zb0 - 0.12): cyl((0, 0, z), 0.85, 0.24, wood)
    for x in (-0.78, 0.78): cyl((x, 0, 0), 0.06, 2 * Hb + gap + 0.2, wood)
    label(f'{cap}분', 0, zt0 + Hb + 0.12, 0.3, ink, -0.86)
    b3d.stack_camera((0, 0, 0), 4.9, az=0.0, el=8.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((560, 900), 40); b3d.lights(5)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
