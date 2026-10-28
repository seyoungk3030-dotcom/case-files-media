"""ROOM 052 3D sprites: the number-block pyramid ('pyr', letters A-D on amber blocks, one blank block) and the answer
('ans', every block numbered, the A-D blocks in mint) and a 3 + 4 = 7 example for the rules card ('ex'). Optional argv after '--': names to render."""
import json, math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
import b3d
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
P = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
GRID = {tuple(map(int, k.split(','))): v for k, v in P['grid'].items()}
SHOWN = {tuple(map(int, k.split(','))) for k in P['shown']}
LET = {(0, 1): 'A', (0, 3): 'B', (1, 0): 'C', (1, 2): 'D'}


def label(s, x, z, m, size):
    bpy.ops.object.text_add(location=(x, -0.47, z), rotation=(math.radians(90), 0, 0)); t = bpy.context.object
    t.data.body = s; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.size = size; t.data.extrude = 0.03
    t.data.materials.append(m)


def example():
    b3d.reset((1000, 900), 64); b3d.lights(5)
    b3d.camera((0, 0, 1.9), 15, 4.6, 62)
    M = b3d.mats(); ink = b3d.mat('ink', (0.03, 0.05, 0.09), rough=0.5, coat=0.0)
    for x, z, v in ((-0.52, 0.47, 3), (0.52, 0.47, 4), (0, 1.47, 7)):
        bpy.ops.mesh.primitive_cube_add(size=0.94, location=(x, 0, z)); o = bpy.context.object
        o.data.materials.append(M['pearl']); b3d.bevel(o, 0.06); label(str(v), x, z, ink, 0.5)
    b3d.floor()


def scene(name):
    if name == 'ex': return example()
    ans = name == 'ans'
    b3d.reset((1000, 900), 64); b3d.lights(5)
    b3d.camera((0, 0, 1.9), 15, 4.6, 62)
    M = b3d.mats(); ink = b3d.mat('ink', (0.03, 0.05, 0.09), rough=0.5, coat=0.0)
    for (r, i), v in GRID.items():
        x = (i - (3 - r) / 2) * 1.04; z = r * 1.0 + 0.47
        let = LET.get((r, i))
        col = ('mint' if ans else 'amber') if let else 'pearl'
        bpy.ops.mesh.primitive_cube_add(size=0.94, location=(x, 0, z)); o = bpy.context.object
        o.data.materials.append(M[col]); b3d.bevel(o, 0.06)
        if ans or (r, i) in SHOWN: label(str(v), x, z, ink, 0.5)
        elif let: label(let, x, z, ink, 0.55)
    b3d.floor()


names = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['pyr', 'ans']
for name in names:
    t = time.time(); scene(name); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
