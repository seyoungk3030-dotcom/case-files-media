"""ROOM 192 3D sprites: an everyday small object (sugar cube, bean, ping-pong ball, pill) on a table, and next to it a
paper pile drawn to the same scale. p*: question, a single sheet lies there. a*: answer, the pile after the needed cuts
(2^n sheets, 0.1 mm each) glows mint and is just taller than the object; a faint ghost shows the pile one cut earlier."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD, SHEET
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)


def glowm(name, c, s, rough=0.4, alpha=1.0):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    if alpha < 1: q.inputs['Alpha'].default_value = alpha
    return m


def box(m, loc, scale, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def obj(name, u, x):
    h = BOARDS_H[name] * u
    if name == '각설탕':
        box(b3d.mat('sugar', (0.96, 0.95, 0.92), rough=0.9, coat=0), (x, 0, h / 2), (h, h, h), h * 0.06)
    elif name == '콩':
        bpy.ops.mesh.primitive_uv_sphere_add(radius=h / 2, location=(x, 0, h / 2), segments=48, ring_count=24); o = bpy.context.object
        o.scale = (1.3, 1.0, 1.0); o.data.materials.append(b3d.mat('bean', (0.85, 0.7, 0.4), rough=0.4, coat=0.3)); bpy.ops.object.shade_smooth()
    elif name == '탁구공':
        bpy.ops.mesh.primitive_uv_sphere_add(radius=h / 2, location=(x, 0, h / 2), segments=64, ring_count=32); o = bpy.context.object
        o.data.materials.append(b3d.mat('pp', (1.0, 0.55, 0.12), rough=0.5, coat=0)); bpy.ops.object.shade_smooth()
    else:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=h, location=(x, 0, h / 2), segments=48, ring_count=24); o = bpy.context.object
        o.scale = (0.65, 0.6, 0.5); o.data.materials.append(b3d.mat('pill', (0.95, 0.95, 0.97), rough=0.3, coat=0.4)); bpy.ops.object.shade_smooth()


BOARDS_H = {v[0]: v[1] for v in BOARDS.values()}


def pile(m, line, x, w, hmm, u, layers):
    h = max(hmm * u, 0.006); box(m, (x, 0, h / 2), (w, w * 0.8, h))
    if hmm * u > 0.05:
        n = min(layers, 24)
        for i in range(1, n): box(line, (x, -w * 0.4 - 0.002, h * i / n), (w * 1.002, 0.004, 0.006))


def scene(key, after):
    name, H = BOARDS[key]; n = GOOD[key]; top = SHEET * 2 ** n
    u = 1.3 / top
    table = b3d.mat('table', (0.42, 0.28, 0.18), rough=0.55, coat=0.2)
    paper = b3d.mat('paper', (0.94, 0.94, 0.92), rough=0.8, coat=0); line = b3d.mat('pline', (0.7, 0.7, 0.68), rough=0.8, coat=0)
    mint = glowm('mint', (0.25, 0.95, 0.7), 0.35, rough=0.6); ghost = glowm('ghost', (0.6, 0.75, 1.0), 0.6)
    box(table, (0, 0, -0.04), (3.2, 1.6, 0.08))
    w = max(H * u * 1.0, 0.45); xo = -0.6 if name != '알약' else -0.5
    obj(name, u, xo)
    if after:
        pile(mint, line, 0.65, 0.55, top, u, 2 ** n)
        hp = SHEET * 2 ** (n - 1) * u
        box(ghost, (0.65, 0.3, hp), (0.62, 0.01, 0.012))
        box(ghost, (0.0, 0, H * u), (2.2, 0.01, 0.01))
    else:
        pile(paper, line, 0.65, 0.55, SHEET, u, 1)
    b3d.stack_camera((0, 0, 0.6), 2.5, az=0.0, el=12.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((700, 640), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t, 1), flush=True)
