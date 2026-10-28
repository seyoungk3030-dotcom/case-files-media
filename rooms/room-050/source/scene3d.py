"""ROOM 050 3D sprites: four matchstick figures A-D on felt ('fA'..'fD'). Answer sprites ('xA'..'xD') add a faint
mint tile in every small square that counts and a glowing amber/coral frame for every bigger square. Same camera scale
for all. Optional argv after '--': names to render."""
import os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import FIGS, squares
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)


def mat_glow(name, col, s):
    m = b3d.mat(name, col, rough=0.4, coat=0.3); p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Emission Color'].default_value = (*col, 1); p.inputs['Emission Strength'].default_value = s; return m


def match(e, M, cx, cy):
    d, x, y = e; L = 0.86
    mx, my = (x + 0.5, y) if d == 'h' else (x, y + 0.5)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(mx - cx, my - cy, 0.06)); o = bpy.context.object
    o.scale = (L, 0.09, 0.09) if d == 'h' else (0.09, L, 0.09); o.data.materials.append(M['wood']); b3d.bevel(o, 0.02, 2)
    hx, hy = (mx + L / 2 - cx, my - cy) if d == 'h' else (mx - cx, my + L / 2 - cy)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.085, location=(hx, hy, 0.07)); o = bpy.context.object
    o.scale = (1.35, 1, 1) if d == 'h' else (1, 1.35, 1); o.data.materials.append(M['head'])


def frame(x, y, k, m, cx, cy, inset):
    a, b = x + inset - cx, x + k - inset - cx; c, d = y + inset - cy, y + k - inset - cy
    for (px, py, sx, sy) in (((a + b) / 2, c, b - a, 0.05), ((a + b) / 2, d, b - a, 0.05), (a, (c + d) / 2, 0.05, d - c), (b, (c + d) / 2, 0.05, d - c)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(px, py, 0.13)); o = bpy.context.object; o.scale = (sx + 0.05, sy + 0.05, 0.04)
        o.data.materials.append(m)


def scene(name):
    S = FIGS[name[1]]; ans = name[0] == 'x'
    w = max(x for _, x, _ in S) + 1; h = max(y for _, _, y in S) + 1
    w = max(x + (1 if d == 'h' else 0) for d, x, _ in S); h = max(y + (1 if d == 'v' else 0) for d, _, y in S)
    cx, cy = w / 2, h / 2
    b3d.reset((900, 900), 40); b3d.lights(5)
    b3d.stack_camera((0, 0, 0), 4.6, 0.0, 62.0)
    M = {'wood': b3d.mat('wood', (0.93, 0.72, 0.42), rough=0.55, coat=0.2), 'head': b3d.mat('head', (0.85, 0.10, 0.08), rough=0.4, coat=0.5),
         'felt': b3d.mat('felt', (0.08, 0.20, 0.17), rough=0.9, coat=0.0)}
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.08)); o = bpy.context.object
    o.scale = (w + 0.7, h + 0.7, 0.12); o.data.materials.append(M['felt']); b3d.bevel(o, 0.08, 4)
    for e in S: match(e, M, cx, cy)
    if ans:
        tile = mat_glow('tile', (0.15, 0.85, 0.65), 0.25)
        cols = {2: mat_glow('k2', (1.0, 0.70, 0.12), 1.2), 3: mat_glow('k3', (1.0, 0.30, 0.25), 0.5)}
        for x, y, k in squares(S):
            if k == 1:
                bpy.ops.mesh.primitive_cube_add(size=1, location=(x + 0.5 - cx, y + 0.5 - cy, 0.0)); o = bpy.context.object
                o.scale = (0.72, 0.72, 0.03); o.data.materials.append(tile)
            else: frame(x, y, k, cols[k], cx, cy, 0.17 if k == 2 else 0.1)
    b3d.floor()


names = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [p + k for k in 'ABCD' for p in 'fx']
for name in names:
    t = time.time(); scene(name); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
