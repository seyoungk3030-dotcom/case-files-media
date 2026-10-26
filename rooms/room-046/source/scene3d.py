"""ROOM 046 3D sprites: blocks A-D built from small cubes, painted coral all over ('bA'..'bD'); answer versions
('xA'..'xD') make every painted cube see-through and light up the unpainted inside cubes. Same camera scale for all.
Optional argv after '--': names to render."""
import os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BLOCKS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)


def scene(k, answer):
    w, d, h = BLOCKS[k]
    b3d.reset((800, 800), 40); b3d.lights(6)
    b3d.stack_camera((0, 0, 1.9), 8.6, 33.0, 30.0)
    paint = b3d.mat('paint', b3d.PAL['coral'], rough=0.35, coat=0.5)
    glass = b3d.mat('glass', b3d.PAL['coral'], rough=0.2, coat=0.0)
    glass.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.12
    core = b3d.mat('core', (0.95, 0.93, 0.85), rough=0.4, coat=0.2)
    p = core.node_tree.nodes['Principled BSDF']; p.inputs['Emission Color'].default_value = (1.0, 0.85, 0.45, 1); p.inputs['Emission Strength'].default_value = 0.8
    for x in range(w):
        for y in range(d):
            for z in range(h):
                inside = 0 < x < w - 1 and 0 < y < d - 1 and 0 < z < h - 1
                bpy.ops.mesh.primitive_cube_add(size=0.96, location=(x - (w - 1) / 2, y - (d - 1) / 2, z + 0.5))
                c = bpy.context.object
                c.data.materials.append(core if inside else (glass if answer else paint)); b3d.bevel(c, 0.06, 2)
    b3d.floor()


names = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [p + k for k in 'ABCD' for p in 'bx']
for name in names:
    t = time.time(); scene(name[1], name[0] == 'x'); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
