"""ROOM 042 3D sprites: each die on its tile path with arrows ('dA'..'dD'), and after rolling with the top glowing
('eA'..'eD'). Same camera scale everywhere so the sprites match. Label point (in front of the start tile) -> json."""
import json, math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d, dice
from verify import DICE, START, END
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
STEP = {'R': (1.15, 0), 'F': (0, -1.15)}
GLOW = (1.0, 0.45, 0.02)


def arrow(x, y, d, m):
    dx, dy = STEP[d]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; ang = math.atan2(uy, ux)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x - ux * 0.12, y - uy * 0.12, 0.1))
    b = bpy.context.object; b.scale = (0.5, 0.14, 0.05); b.rotation_euler = (0, 0, ang); b.data.materials.append(m)
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.28, radius2=0.28, depth=0.06, location=(x + ux * 0.18, y + uy * 0.18, 0.1))
    c = bpy.context.object; c.rotation_euler = (0, 0, ang - math.pi / 2); c.data.materials.append(m)


def scene(k, after):
    res = (620, 620); b3d.reset(res, 64); b3d.lights(4)
    seq = DICE[k][1]; pts = [(0.0, 0.0)]
    for s in seq: pts.append((pts[-1][0] + STEP[s][0], pts[-1][1] + STEP[s][1]))
    cx = (min(p[0] for p in pts) + max(p[0] for p in pts)) / 2; cy = (min(p[1] for p in pts) + max(p[1] for p in pts)) / 2
    b3d.stack_camera((cx, cy, 0.45), 3.9, 33.0, 36.0)
    tile = b3d.mat('tile', (0.30, 0.37, 0.50), rough=0.6, coat=0.0); goal = b3d.mat('goal', (0.20, 0.55, 0.48), rough=0.6, coat=0.0)
    am = b3d.mat('arrow', (0.95, 0.62, 0.10), rough=0.35, coat=0.3)
    for i, (x, y) in enumerate(pts):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.03)); t = bpy.context.object
        t.scale = (1.08, 1.08, 0.06); t.data.materials.append(goal if i == len(pts) - 1 else tile); b3d.bevel(t, 0.03, 2)
        if i and not after: arrow(x, y, seq[i - 1], am)
    p = pts[-1] if after else pts[0]
    b3d.die(END[k] if after else START[k], (p[0], p[1], 0.565), glow=(dice.UP, GLOW) if after else None)
    b3d.floor(); bpy.context.view_layer.update()
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; v = world_to_camera_view(sc, sc.camera, Vector((pts[0][0] - 0.2, pts[0][1] - 0.85, 0)))
    return [{'key': k, 'x': round(v.x * res[0], 1), 'y': round((1 - v.y) * res[1], 1)}]


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('e' if after else 'd') + k
        if only and name not in only: continue
        t = time.time(); pts = scene(k, after); json.dump(pts, open(f'{OUT}/{name}.json', 'w'))
        b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
