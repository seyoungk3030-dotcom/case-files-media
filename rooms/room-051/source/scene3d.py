"""ROOM 051 3D sprites: the four objects of the picture equations, each alone ('oA'..'oD'), same camera and scale.
Optional argv after '--': names to render."""
import os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
import b3d
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
SHAPE = {'A': (b3d.sphere, 'mint'), 'B': (b3d.cube, 'coral'), 'C': (b3d.pyramid, 'amber'), 'D': (b3d.star, 'pearl')}


def scene(k):
    b3d.reset((600, 600), 48); b3d.lights(3)
    b3d.camera((0, 0, 0.45), 9, 3.2, 70)
    M = b3d.mats(); f, c = SHAPE[k]; f(M[c], 0, 0); b3d.floor()


names = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['o' + k for k in 'ABCD']
for name in names:
    t = time.time(); scene(name[1]); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
