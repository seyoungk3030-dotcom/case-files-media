"""ROOM 195 3D sprites: two measuring jugs (litre rings) of hot and cold water and an empty third jug. Water colour
runs from blue (cold) to red (hot); each jug carries its temperature. a*: the two jugs are empty and the third holds
all the water at the mixed colour, its label glowing mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, mix
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
L = 0.26; R = 0.34


def glowm(name, c, s, rough=0.4, alpha=1.0):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    if alpha < 1: q.inputs['Alpha'].default_value = alpha
    return m


def cyl(m, r, d, loc, v=64):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, vertices=v); o = bpy.context.object
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.pi / 2, 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def tcol(t):
    stops = [(0, (0.1, 0.35, 1.0)), (35, (0.2, 0.75, 0.95)), (60, (1.0, 0.7, 0.15)), (100, (1.0, 0.12, 0.06))]
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if t <= b:
            f = (t - a) / (b - a); return tuple(ca[i] + (cb[i] - ca[i]) * f for i in range(3))
    return stops[-1][1]


def jug(x, litres, temp, label, lab_m, n):
    glass = glowm(f'g{n}', (0.85, 0.92, 1.0), 0.08, rough=0.05, alpha=0.18)
    cyl(glass, R, 5 * L + 0.1, (x, 0, (5 * L + 0.1) / 2))
    ring = b3d.mat('ring', (0.4, 0.43, 0.5), rough=0.5, coat=0)
    for i in range(1, 6):
        bpy.ops.mesh.primitive_torus_add(major_radius=R + 0.004, minor_radius=0.005, location=(x, 0, i * L)); bpy.context.object.data.materials.append(ring)
    if litres:
        w = glowm(f'w{n}', tcol(temp), 0.12, rough=0.15, alpha=0.9); cyl(w, R - 0.02, litres * L, (x, 0, litres * L / 2))
    text(label, (x, -R - 0.05, 5 * L + 0.32), 0.24, lab_m)


def scene(key, after):
    (v1, t1), (v2, t2) = BOARDS[key]; tm = int(mix(*BOARDS[key]))
    b3d.mat('floor', (0.2, 0.22, 0.28), rough=0.6, coat=0)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.04)); f = bpy.context.object; f.scale = (3.4, 1.2, 0.08); f.data.materials.append(bpy.data.materials['floor'])
    wt = b3d.mat('lab', (0.97, 0.97, 1.0), rough=0.4, coat=0); qm = b3d.mat('q', (1.0, 0.82, 0.3), rough=0.4, coat=0)
    hot, cold = glowm('hot', tcol(t1), 0.3), glowm('cold', tcol(t2), 0.3)
    jug(-1.05, 0 if after else v1, t1, f'{t1}°', hot, 1)
    jug(0.0, 0 if after else v2, t2, f'{t2}°', cold, 2)
    if after: jug(1.05, v1 + v2, tm, f'{tm}°', glowm('mint', (0.2, 0.95, 0.65), 0.5), 3)
    else: jug(1.05, 0, 0, '?', qm, 3)
    b3d.stack_camera((0, 0, 0.85), 3.3, az=0.0, el=12.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((700, 640), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t, 1), flush=True)
