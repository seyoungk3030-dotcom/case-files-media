"""ROOM 061 3D sprites: transparent films seen from the front-top. 'pA'..'pD' = left film (mint squares) and right film
(coral squares) side by side, with a '뒤집기' sign over the right film. 'aA'..'aD' = right film turned over and laid on the left."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import FILMS, mirror
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
EL, C = 68.0, 0.52        # camera elevation, cell size


def label(s, x, y, z, size, m):
    bpy.ops.object.text_add(location=(x, y, z), rotation=(math.radians(90 - EL), 0, 0))
    t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.03; t.data.materials.append(m)


def cube(loc, sc, m, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = sc; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 2)
    return o


def film(cx, cells, cols, M, z=0.0):
    glass, frame, cellm = M['glass'], M['frame'], M['cell']
    cube((cx, 0, z), (3 * C + 0.25, 5 * C + 0.25, 0.04), glass)
    for sx, sy, w, h in ((0, 1, 3 * C + 0.3, 0.06), (0, -1, 3 * C + 0.3, 0.06), (1, 0, 0.06, 5 * C + 0.3), (-1, 0, 0.06, 5 * C + 0.3)):
        cube((cx + sx * (3 * C + 0.25) / 2, sy * (5 * C + 0.25) / 2, z + 0.02), (w, h, 0.06), frame)
    for i in range(15):
        x, y = cx + (i % 3 - 1) * C, (2 - i // 3) * C
        cube((x, y, z + 0.025), (C * 0.86, C * 0.86, 0.005), cellm)
    for group, m in zip(cells, cols):
        for i in group:
            x, y = cx + (i % 3 - 1) * C, (2 - i // 3) * C
            cube((x, y, z + 0.05), (C * 0.8, C * 0.8, 0.05), m, 0.015)


def scene(k, after):
    b3d.reset((900, 640) if not after else (520, 640), 48); b3d.lights(6)
    mint = b3d.mat('mint', b3d.PAL['mint'], rough=0.3, coat=0.5); coral = b3d.mat('coral', (0.95, 0.38, 0.30), rough=0.3, coat=0.5)
    amber = b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3)
    q = amber.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
    q.inputs['Emission Strength'].default_value = 0.8
    glass = b3d.mat('glass', (0.75, 0.85, 0.95), rough=0.1, coat=0.8); glass.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.28
    cellm = b3d.mat('cellm', (0.95, 0.97, 1.0), rough=0.4); cellm.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.10
    frame = b3d.mat('frame', (0.80, 0.84, 0.90), rough=0.3, metal=0.5)
    M = {'glass': glass, 'frame': frame, 'cell': cellm}
    L, R = FILMS[k]
    if after:
        b3d.stack_camera((0, 0.05, 0), 3.9, az=0.0, el=EL)
        film(0, [L, sorted(mirror(R))], [mint, coral], M)
    else:
        b3d.stack_camera((0, 0.25, 0), 4.4 * 900 / 640 * 0.95, az=0.0, el=EL)
        film(-1.25, [L], [mint], M); film(1.25, [R], [coral], M)
        label('뒤집기', 1.25, 5 * C / 2 + 0.55, 0.3, 0.42, amber)
        for d in (-1, 1):
            bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.12, radius2=0, depth=0.25,
                                            location=(1.25 + d * 0.85, 5 * C / 2 + 0.55, 0.3), rotation=(0, d * math.pi / 2, 0))
            bpy.context.object.data.materials.append(amber)
    b3d.floor().location.z = -0.5


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
