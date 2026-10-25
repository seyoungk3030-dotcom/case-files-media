"""ROOM 041 3D sprites: four seesaws (level or tipped toward the heavier side) and one icon per shape, in ../.build-3d/."""
import json, math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import SCALES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
TILT = math.radians(7)
only = sys.argv[1:]
for i, (L, R, res) in enumerate(SCALES, 1):
    if only and f'scale{i}' not in only: continue
    t = time.time(); b3d.reset((1000, 470)); M = b3d.mats()
    b3d.floor(); b3d.lights(); b3d.camera(target=(0, 0, 1.4))
    before = set(bpy.data.objects); placed = b3d.seesaw(M, L, R)
    if res != '=':   # tip everything above the fulcrum around the pivot; right side down = +angle about y
        bpy.context.view_layer.update()
        piv = bpy.data.objects.new('piv', None); bpy.context.collection.objects.link(piv); piv.location = (0, 0, 1.15 + 0.09)
        bpy.context.view_layer.update()
        for o in set(bpy.data.objects) - before:
            if o.type == 'MESH' and o.location.z > 0.9:
                mw = o.matrix_world.copy(); o.parent = piv; o.matrix_world = mw
        piv.rotation_euler = (0, TILT if res == 'R' else -TILT, 0)
    json.dump(b3d.project(placed), open(f'{OUT}/scale{i}.json', 'w'))
    b3d.render(f'{OUT}/scale{i}.png'); print('scale', i, round(time.time() - t, 1), 's', flush=True)
for k in 'ctsr':
    if only and f'icon-{k}' not in only: continue
    b3d.reset((300, 300)); M = b3d.mats(); b3d.floor(); b3d.lights(2)
    fn, col = b3d.SHAPES[k]; fn(M[col], 0, 0)
    b3d.camera(target=(0, 0, 0.42), dist=6, height=2.0, lens=70)
    b3d.render(f'{OUT}/icon-{k}.png'); print('icon', k, flush=True)
