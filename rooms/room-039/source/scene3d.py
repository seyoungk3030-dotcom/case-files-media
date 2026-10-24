"""ROOM 039 3D sprites: the tray with holes A-D, the four loose pieces 1-4, and the solved tray.
Label points (in front of each hole / piece) go to .build-3d/<name>.json."""
import json, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import HOLES, PIECES, sols
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
PCOL = {1: b3d.PAL['mint'], 2: b3d.PAL['amber'], 3: b3d.PAL['coral'], 4: (0.38, 0.30, 0.95)}
X0 = {k: 1 + i * 5 for i, k in enumerate('ABCD')}; W, D, TH = 21, 5, 0.55


def block(x, y, z, h, m, s=0.97):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x + 0.5, y + 0.5, z + h / 2))
    o = bpy.context.object; o.scale = (s, s, h); o.data.materials.append(m); b3d.bevel(o, 0.06, 3)


def setup(res, center, scale):
    b3d.reset(res, 48); b3d.lights(9)
    for o in bpy.data.objects:
        if o.type == 'LIGHT': o.location.x += center[0]; o.location.z += 3
    bpy.ops.object.light_add(type='AREA', location=(center[0], 2, 12)); L = bpy.context.object.data; L.energy = 700; L.size = 14
    b3d.stack_camera(center, scale, 0.0, 52.0)


def labels(keys, res):
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    sc = bpy.context.scene; bpy.context.view_layer.update(); out = []
    for k, (x, y, z) in keys.items():
        v = world_to_camera_view(sc, sc.camera, Vector((x, y, z)))
        out.append({'key': str(k), 'x': round(v.x * res[0], 1), 'y': round((1 - v.y) * res[1], 1)})
    return out


def tray(fill):
    res = (1300, 560); setup(res, (W / 2, D / 2, 0), 22.5)
    top = b3d.mat('tray', (0.42, 0.48, 0.58), rough=0.85, coat=0.0)
    pit = b3d.mat('pit', (0.03, 0.04, 0.07), rough=0.6, coat=0.0)
    holes = {(X0[h] + x, 1 + y): h for h, c in HOLES.items() for x, y in c}
    for x in range(W):
        for y in range(D):
            if (x, y) in holes: block(x, y, 0, 0.12, pit, 1.0)
            else: block(x, y, 0, TH, top, 1.0)
    if fill:
        for h, n in zip('ABCD', sols[0]):
            m = b3d.mat(f'p{n}', PCOL[int(n)], rough=0.25, coat=0.7)
            for x, y in HOLES[h]: block(X0[h] + x, 1 + y, 0.12, TH, m)
    return labels({h: (X0[h] + 1.5, -0.9, 0) for h in 'ABCD'}, res)


def pieces():
    res = (1300, 480); setup(res, (W / 2, 1.5, 0), 22.5)
    for i, (n, c) in enumerate(PIECES.items()):
        m = b3d.mat(f'p{n}', PCOL[n], rough=0.25, coat=0.7); w = max(x for x, _ in c) + 1
        ox = 1 + i * 5 + (4 - w) / 2
        for x, y in c: block(ox + x, y, 0, TH, m)
    return labels({n: (1 + i * 5 + 2, -1.0, 0) for i, n in enumerate(PIECES)}, res)


for name, fn in (('tray', lambda: tray(False)), ('pieces', pieces), ('solved', lambda: tray(True))):
    t = time.time(); pts = fn(); json.dump(pts, open(f'{OUT}/{name}.json', 'w'))
    b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
