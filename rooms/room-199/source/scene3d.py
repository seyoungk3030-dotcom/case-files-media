"""ROOM 199 3D sprites, side view: a wall and floor, a faint ghost of the ladder standing upright, and the ladder after its
foot was pulled out d m (amber arrow on the floor). Every board is drawn to its own scale (ladder always the same size on
screen); lengths are on the card text. a*: a mint bar on the wall marks how far the top came down."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, top
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
S = 3.2


def glowm(name, c, s, rough=0.4, alpha=1.0):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    if alpha < 1: q.inputs['Alpha'].default_value = alpha
    return m


def box(m, loc, sc, bev=0.03):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def rod(m, p, q, r, verts=16):
    dx, dy, dz = (q[i] - p[i] for i in range(3)); L = math.sqrt(dx * dx + dy * dy + dz * dz)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=tuple((p[i] + q[i]) / 2 for i in range(3)), vertices=verts)
    o = bpy.context.object; o.rotation_euler = (0, math.atan2(dx, dz), 0) if abs(dy) < 1e-9 else (-math.pi / 2, 0, 0)
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def ladder(m, foot, head, rung_m, n=11):
    for y in (-0.24, 0.24): rod(m, (foot[0], y, foot[1]), (head[0], y, head[1]), 0.045)
    for i in range(1, n):
        t = i / n; x = foot[0] + (head[0] - foot[0]) * t; z = foot[1] + (head[1] - foot[1]) * t
        rod(rung_m, (x, -0.24, z), (x, 0.24, z), 0.03)


def scene(key, after):
    L, d = BOARDS[key]; s = S / L; h = top(L, d)
    wall = b3d.mat('wall', (0.82, 0.76, 0.66), rough=0.7, coat=0); floor = b3d.mat('floor', (0.45, 0.3, 0.18), rough=0.5, coat=0.3)
    box(wall, (-0.15, 0.2, 1.9), (0.3, 1.6, 3.8)); box(floor, (1.35, 0.2, -0.06), (3.3, 1.6, 0.12))
    rail = b3d.mat('rail', (0.95, 0.62, 0.12), rough=0.3, metal=0.6, coat=0.4); rung = b3d.mat('rung', (0.75, 0.77, 0.8), rough=0.25, metal=1.0, coat=0)
    ghost = glowm('ghost', (0.75, 0.85, 1.0), 0.25, alpha=0.25)
    ghost.blend_method = 'BLEND' if hasattr(ghost, 'blend_method') else None
    ladder(ghost, (0.07, 0.0), (0.07, S), ghost)
    ladder(rail, (d * s, 0.0), (0.07, h * s), rung)
    am = glowm('amber', (1.0, 0.72, 0.2), 1.2)
    a0, a1 = 0.1, d * s - 0.05
    rod(am, (a0, -0.55, 0.04), (a1 - 0.18, -0.55, 0.04), 0.035)
    bpy.ops.mesh.primitive_cone_add(radius1=0.09, radius2=0, depth=0.2, location=(a1 - 0.1, -0.55, 0.04), rotation=(0, math.pi / 2, 0))
    bpy.context.object.data.materials.append(am)
    if after:
        mint = glowm('mint', (0.2, 0.95, 0.65), 1.6)
        box(mint, (0.04, -0.5, (h * s + S) / 2), (0.08, 0.08, S - h * s), 0.02)
        for z in (h * s, S): box(mint, (0.1, -0.5, z), (0.22, 0.08, 0.04), 0.01)
    b3d.stack_camera((1.0, 0, 1.75), 4.3, az=14.0, el=8.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((640, 700), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t, 1), flush=True)
