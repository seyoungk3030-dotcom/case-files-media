"""ROOM 108 3D sprites: Shepard-Metzler block shapes made of unit cubes, each rendered alone with the same
front-right-top camera. s<k>0: the reference shape (amber). s<k>1-4: the numbered shapes (ivory). m<k>: the turned
copy again in mint for the answer cards. render.py lays each board out as one row."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import B, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)


def shape(cells, col):
    m = b3d.mat('c', col, rough=0.45, coat=0.2); cx = [sum(p[i] for p in cells) / len(cells) for i in range(3)]
    for p in cells:
        bpy.ops.mesh.primitive_cube_add(size=0.96, location=tuple(p[i] - cx[i] for i in range(3))); o = bpy.context.object
        o.data.materials.append(m); b3d.bevel(o, 0.06)
    b3d.stack_camera((0, 0, 0), 7.2, az=35.0, el=28.0)


AMB, IVO, MINT = (0.88, 0.45, 0.06), (0.80, 0.80, 0.78), (0.15, 0.78, 0.55)
only = sys.argv[1:]
jobs = []
for k in 'ABCD':
    ref, cands = B[k]; jobs.append((f's{k}0', ref, AMB))
    for i, s in enumerate(cands): jobs.append((f's{k}{i + 1}', s, IVO))
    jobs.append((f'm{k}', cands[RES[k][0][0] - 1], MINT))
for name, cells, col in jobs:
    if only and name not in only: continue
    b3d.reset((520, 520), 32); b3d.lights(3)
    t = time.time(); shape(cells, col); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
