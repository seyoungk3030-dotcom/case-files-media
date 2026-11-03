"""ROOM 057 3D sprites: a plank on two rollers on a 12-tile track, seen almost side-on.
'pA'..'pD' = start, with a mint ground arrow 'k칸' for how far the rollers roll.
'aA'..'aD' = after: rollers moved k, plank moved 2k (amber arrow '2k칸' over the plank), ghost of the start plank."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import ROLL, R, plank_shift
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
N, PL = 12, 3.0           # track tiles, plank length (tiles)
ROLLERS = (0.6, 2.4)      # roller centres under the plank at start


def box(x0, x1, y0, y1, z0, z1, m, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    o = bpy.context.object; o.scale = (x1 - x0, y1 - y0, z1 - z0); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def label(s, x, y, z, size, m):
    bpy.ops.object.text_add(location=(x, y, z), rotation=(math.radians(90), 0, 0))
    t = bpy.context.object; t.data.body = s; t.data.font = bpy.data.fonts.load(FONT) if 'P-Black' not in bpy.data.fonts else bpy.data.fonts['P-Black']
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)
    return t


def arrow(x0, x1, y, z, m, thick=0.07):
    box(x0, x1 - 0.22, y - thick / 2, y + thick / 2, z - thick / 2, z + thick / 2, m)
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.26, radius2=0, depth=0.42, location=(x1 - 0.2, y, z),
                                    rotation=(0, math.radians(90), 0))
    bpy.context.object.data.materials.append(m)
    for x in (x0,):
        box(x - 0.025, x + 0.025, y - 0.03, y + 0.03, z - 0.18, z + 0.18, m)


def roller(x, theta, wood, stripe):
    bpy.ops.mesh.primitive_cylinder_add(radius=R, depth=1.0, vertices=48, location=(x, 0, R), rotation=(math.radians(90), 0, 0))
    o = bpy.context.object; o.data.materials.append(wood); b3d.bevel(o, 0.03, 3)
    # a red stripe along the roller shows how far it has turned
    sx, sz = x + (R + 0.004) * math.sin(theta), R + (R + 0.004) * math.cos(theta)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(sx, 0, sz), rotation=(0, theta, 0))
    s = bpy.context.object; s.scale = (0.07, 1.02, 0.03); s.data.materials.append(stripe)


def scene(k, after):
    b3d.reset((1500, 420), 48); b3d.lights(10)
    b3d.stack_camera((N / 2, 0, 0.75), N + 0.4, az=0.0, el=24.0)
    t1 = b3d.mat('t1', (0.55, 0.62, 0.74), rough=0.6, coat=0.0); t2 = b3d.mat('t2', (0.36, 0.43, 0.56), rough=0.6, coat=0.0)
    wood = b3d.mat('wood', (0.80, 0.58, 0.34), rough=0.5, coat=0.2); plank = b3d.mat('plank', (0.93, 0.80, 0.55), rough=0.45, coat=0.3)
    stripe = b3d.mat('stripe', (0.85, 0.15, 0.12), rough=0.4)
    mint = b3d.mat('mint', b3d.PAL['mint'], rough=0.35, coat=0.4)
    amber = b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3, coat=0.4)
    for p in (mint, amber):
        q = p.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
        q.inputs['Emission Strength'].default_value = 0.6
    white = b3d.mat('white', (0.92, 0.94, 0.97), rough=0.5, coat=0.0)
    for i in range(N):
        box(i + 0.02, i + 0.98, -0.6, 0.6, -0.06, 0.0, t1 if i % 2 == 0 else t2)
    shift_p, shift_r = plank_shift(ROLL[k]) if after else (0.0, 0.0)
    theta = shift_r / R
    for x in ROLLERS: roller(x + shift_r, theta, wood, stripe)
    box(shift_p, shift_p + PL, -0.55, 0.55, 2 * R, 2 * R + 0.2, plank, 0.04)
    if after:
        g = b3d.mat('ghost', (0.93, 0.80, 0.55), rough=0.5, coat=0.0); g.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.22
        g.blend_method = 'BLEND' if hasattr(g, 'blend_method') else None
        box(0, PL, -0.55, 0.55, 2 * R, 2 * R + 0.2, g)
        arrow(PL, PL + shift_p, -0.6, 2 * R + 0.5, amber, 0.12)
        label(f'판자 {int(round(shift_p))}칸', PL + shift_p / 2, -0.62, 2 * R + 0.72, 0.75, amber)
    else:
        arrow(ROLLERS[1], ROLLERS[1] + ROLL[k], -0.75, 0.14, mint, 0.12)
        label(f'롤러 {ROLL[k]}칸', max(ROLLERS[1] + ROLL[k] / 2, 4.8), -0.8, 0.62, 0.75, mint)
    b3d.floor().location.z = -0.08


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
