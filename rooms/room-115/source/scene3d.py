"""ROOM 115 3D sprites: front view of 2-3 clear tanks of width 1, 2 or 3 units standing on a base, joined at the bottom
by a pipe with red (closed) valves. A ruler 0-9 on the left and faint level lines on the back wall; amber tags under
each tank say its width. a*: the valves are mint (open) and every tank shows the same water level, with a mint line."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, LV
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U, WU, GAP, Z0 = 0.36, 0.62, 0.55, 0.55


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def box(m, c, s, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def scene(k, after):
    b = BOARDS[k]; L = float(LV[k])
    wall = b3d.mat('wall', (0.012, 0.016, 0.03), rough=0.8, coat=0); base = b3d.mat('base', (0.14, 0.16, 0.22), rough=0.5, coat=0.1)
    tick = b3d.mat('tick', (0.8, 0.83, 0.9), rough=0.5, coat=0); glow(tick, (0.8, 0.83, 0.9), 1.5)
    faint = b3d.mat('faint', (0.3, 0.33, 0.4), rough=0.6, coat=0); glow(faint, (0.3, 0.33, 0.4), 0.5)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.5)
    red = b3d.mat('red', (0.9, 0.2, 0.18), rough=0.4, coat=0.2); amber = b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0.1)
    ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0); pipe = b3d.mat('pipe', (0.5, 0.53, 0.6), rough=0.3, metal=0.7, coat=0)
    glass = b3d.mat('glass', (0.8, 0.9, 1.0), rough=0.3, coat=0); glass.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.16
    water = b3d.mat('water', (0.08, 0.35, 0.85), rough=0.3, coat=0); water.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.75
    ws = [w * WU for w in b['w']]; total = sum(ws) + GAP * (len(ws) - 1); x = -total / 2 + 0.45; xs = []
    for w in ws: xs.append(x + w / 2); x += w + GAP
    span = (-total / 2 - 0.6, total / 2 + 0.6)
    box(wall, (0.2, 0.75, 2.4), (total + 2.6, 0.1, 5.0), 0.0)
    box(base, (0.45, 0, Z0 / 2), (total + 0.6, 1.2, Z0), 0.04)
    for n in range(10):
        z = Z0 + n * U
        box(faint, ((span[0] + span[1]) / 2 + 0.45, 0.68, z), (span[1] - span[0], 0.01, 0.015), 0.0)
        box(tick, (span[0] + 0.25, -0.05, z), (0.14, 0.02, 0.025), 0.0); text(str(n), (span[0] - 0.12, -0.05, z), 0.34, tick)
    box(base, (span[0] + 0.1, 0.1, Z0 + 4.5 * U), (0.08, 0.3, 9.6 * U), 0.01)
    # pipe and valves between tanks
    bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=xs[-1] - xs[0], location=((xs[0] + xs[-1]) / 2, 0.15, Z0 + 0.12), rotation=(0, math.radians(90), 0), vertices=24)
    bpy.context.object.data.materials.append(pipe)
    for i in range(len(xs) - 1):
        vx = (xs[i] + ws[i] / 2 + xs[i + 1] - ws[i + 1] / 2) / 2
        box(mint if after else red, (vx, 0.15, Z0 + 0.32), (0.08, 0.08, 0.34), 0.02)
        box(mint if after else red, (vx, 0.15, Z0 + 0.5), (0.36 if not after else 0.08, 0.1, 0.08), 0.02)
    for xc, w, wn, h in zip(xs, ws, b['w'], b['h']):
        o = box(glass, (xc, 0.15, Z0 + 10.2 * U / 2), (w, 0.8, 10.2 * U), 0.02); o.visible_shadow = False; o.visible_glossy = False
        lv = L if after else h
        if lv > 0:
            o = box(water, (xc, 0.15, Z0 + lv * U / 2), (w - 0.06, 0.74, lv * U), 0.01); o.visible_shadow = False
        box(amber, (xc, -0.62, Z0 / 2), (min(1.1, max(0.6, w * 0.95)), 0.05, 0.46), 0.05); text(f'폭 {wn}', (xc, -0.66, Z0 / 2), 0.3, ink)
    if after: box(mint, ((span[0] + span[1]) / 2 + 0.45, -0.3, Z0 + L * U), (span[1] - span[0] + 0.2, 0.02, 0.03), 0.0)
    b3d.stack_camera((0.2, 0, 2.3), 5.6, az=0.0, el=5.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 1000), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
