"""ROOM 029 3D sprites: each stack (solid and x-ray with hidden cubes lit up) and the rules example."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d, view
from verify import STACKS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
COLS = {'A': b3d.PAL['mint'], 'B': b3d.PAL['amber'], 'C': (0.42, 0.40, 0.95), 'D': b3d.PAL['coral']}
HID = (1.0, 0.80, 0.10)


def hidden(hs):
    return set(c for c, f in zip(view.CELLS, view.filled(hs)) if f) - view.visible(hs)


def shot(name, hm, col, ghost=()):
    t = time.time(); b3d.reset((560, 600), 48); b3d.lights(3)
    b3d.cubestack(hm, col, ghost, HID); b3d.stack_camera((1.5, 1.5, 1.0), 6.0, view.AZ, view.EL)
    b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), 's')


only = sys.argv[1:]
for k, h in STACKS.items():
    hm = [h[r * 3:(r + 1) * 3] for r in range(3)]
    if not only or k in only: shot(f'stack-{k}', hm, COLS[k])
    if not only or f'x{k}' in only: shot(f'xray-{k}', hm, COLS[k], hidden(h))
EX = (1, 0, 0, 2, 1, 0, 0, 0, 0)
if not only or 'ex' in only:
    hm = [EX[r * 3:(r + 1) * 3] for r in range(3)]
    shot('ex', hm, b3d.PAL['pearl']); shot('xray-ex', hm, b3d.PAL['pearl'], hidden(EX))
