"""ROOM 022 3D sprites: the three seesaws and one icon per shape, rendered to ../.build-3d/."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
import b3d
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
SCALES = [(['c', 'c', 'c'], ['t']), (['t', 'c'], ['s', 's']), (['r', 's'], ['t', 't', 'c'])]
only = sys.argv[1:]
for i, (L, R) in enumerate(SCALES, 1):
    if only and f'scale{i}' not in only: continue
    t = time.time(); b3d.reset((1000, 400)); M = b3d.mats()
    b3d.floor(); b3d.lights(); b3d.camera(); placed = b3d.seesaw(M, L, R)
    json.dump(b3d.project(placed), open(f'{OUT}/scale{i}.json', 'w'))
    b3d.render(f'{OUT}/scale{i}.png'); print('scale', i, round(time.time() - t, 1), 's')
for k in 'ctsr':
    if only and f'icon-{k}' not in only: continue
    b3d.reset((300, 300)); M = b3d.mats(); b3d.floor(); b3d.lights(2)
    fn, col = b3d.SHAPES[k]; fn(M[col], 0, 0)
    b3d.camera(target=(0, 0, 0.42), dist=6, height=2.0, lens=70)
    b3d.render(f'{OUT}/icon-{k}.png'); print('icon', k)
