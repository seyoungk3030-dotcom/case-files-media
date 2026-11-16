"""ROOM 188 3D sprites: a toilet roll seen end-on, drawn to scale (1 cm = 0.05). A dashed ring shows how big the roll
was when new; the cardboard core is in the middle. p*: question. a*: answer, the paper still left glows mint and the
ring of paper already used is shown as a coral ghost."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
S = 0.05; LEN = 0.5


def glowm(name, c, s, rough=0.4, alpha=1.0):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    if alpha < 1: q.inputs['Alpha'].default_value = alpha; m.blend_method = 'BLEND' if hasattr(m, 'blend_method') else None
    return m


def disc(m, r, depth, y):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=(0, y, 0), rotation=(math.pi / 2, 0, 0), vertices=96)
    o = bpy.context.object; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def ring(m, r, minor, y):
    bpy.ops.mesh.primitive_torus_add(location=(0, y, 0), rotation=(math.pi / 2, 0, 0), major_radius=r, minor_radius=minor, major_segments=96, minor_segments=8)
    bpy.context.object.data.materials.append(m)


def scene(key, after):
    k, F, c, N = BOARDS[key]
    paper = b3d.mat('paper', (0.82, 0.82, 0.8), rough=0.8, coat=0); line = b3d.mat('line', (0.78, 0.78, 0.76), rough=0.8, coat=0)
    core = b3d.mat('core', (0.62, 0.45, 0.28), rough=0.7, coat=0); hole = b3d.mat('hole', (0.05, 0.04, 0.03), rough=0.9, coat=0)
    mint = glowm('mint', (0.2, 0.85, 0.6), 0.25); ghost = glowm('ghost', (0.6, 0.75, 1.0), 0.8); coral = glowm('coral', (1.0, 0.3, 0.25), 0.5)
    disc(mint if after else paper, c * S / 2, LEN, 0)
    yf = -LEN / 2 - 0.002
    for i in range(1, 40):
        r = k * S / 2 + i * 0.012
        if r < c * S / 2 - 0.004: ring(line, r, 0.0018, yf)
    disc(core, k * S / 2, LEN + 0.02, 0); disc(hole, k * S / 2 - 0.008, LEN + 0.03, 0)
    R = F * S / 2; n = 48
    for i in range(n):
        if i % 2: continue
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        p, q = (R * math.cos(a0), R * math.sin(a0)), (R * math.cos(a1), R * math.sin(a1))
        L = math.dist(p, q); bpy.ops.mesh.primitive_cylinder_add(radius=0.006, depth=L, location=((p[0] + q[0]) / 2, yf, (p[1] + q[1]) / 2), vertices=12)
        o = bpy.context.object; o.rotation_euler = (0, math.atan2(q[0] - p[0], q[1] - p[1]), 0); o.data.materials.append(coral if after else ghost)
    b3d.stack_camera((0, 0, 0), 0.75, az=0.0, el=5.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((600, 600), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
