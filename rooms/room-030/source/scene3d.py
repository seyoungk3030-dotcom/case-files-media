"""ROOM 030 3D sprites: each die as seen (top, front, right) and the same die seen from below with the bottom
face lit, plus the rules example."""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d, dice
from verify import DICE
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
GLOW = (1.0, 0.75, 0.1)


def shot(name, R, below=False):
    t = time.time(); b3d.reset((520, 520), 64); b3d.lights(2)
    if not below: b3d.floor()
    b3d.die(R, (0, 0, 0.5), glow=(dice.DOWN, GLOW) if below else None)
    b3d.stack_camera((0.25, 0.15, 0.4), 2.3 if below else 3.1, 33.0, -32.0 if below else 30.0)
    b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), 's')


only = sys.argv[1:]
for k, tfr in list(DICE.items()) + [('ex', (2, 1, 4))]:
    R = dice.find(*tfr)
    if not only or k in only: shot(f'die-{k}', R)
    if not only or f'b{k}' in only: shot(f'bottom-{k}', R, below=True)
