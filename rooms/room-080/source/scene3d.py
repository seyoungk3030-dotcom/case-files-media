"""ROOM 080 3D sprites: a row of seesaws on posts, each end overlapping the next one above or below; a big amber
arrow presses the left end of seesaw 1. Each seesaw has its number on a tag. a*: the seesaws that move are tilted and
glow amber; the rest stay grey and level."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, moving
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
X90 = (math.radians(90), 0, 0)
LEN, STEP, DZ = 2.0, 1.7, 0.42


def box(loc, scale, m, bev=0.03, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def label(s, x, z, size, m, y=-0.2):
    bpy.ops.object.text_add(location=(x, y, z), rotation=X90); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def scene(k, after):
    c = BOARDS[k]; n = len(c) + 1; mv = moving(c)
    zs = [1.0]
    for ch in c: zs.append(zs[-1] + (DZ if ch == 'U' else -DZ))
    base = min(zs) - 0.2
    beam = b3d.mat('beam', (0.55, 0.62, 0.78), rough=0.35, coat=0.5); hot = b3d.mat('hot', (0.98, 0.66, 0.12), rough=0.3, coat=0.5)
    post = b3d.mat('post', (0.35, 0.38, 0.46), rough=0.4); tag = b3d.mat('tag', (0.97, 0.98, 1.0), rough=0.4)
    ink = b3d.mat('ink', (0.06, 0.09, 0.18), rough=0.4); amb = b3d.mat('amb', (0.98, 0.5, 0.25), rough=0.3)
    x0 = -(n - 1) * STEP / 2
    d = +1
    for i in range(n):
        x, z = x0 + i * STEP, zs[i]
        moves = after and i < mv
        ang = math.radians(9) * (d if i % 2 == 0 else -d) if moves else 0.0   # seesaw 1: right end up
        box((x, 0, (z - 0.12 + base) / 2 - 0.05), (0.12, 0.12, z - 0.12 - base + 0.1), post, 0.02)
        bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.2, depth=0.3, location=(x, 0, z - 0.12), rotation=(math.radians(90), 0, 0))
        bpy.context.object.data.materials.append(post)
        box((x, 0.06 if i % 2 else -0.06, z), (LEN, 0.26, 0.16), hot if moves else beam, 0.03, rot=(0, -ang, 0))
        box((x, -0.2, z + 0.32), (0.36, 0.03, 0.36), tag, 0.04); label(str(i + 1), x, z + 0.32, 0.3, ink, -0.22)
    box((0, 0, base - 0.05), ((n - 1) * STEP + 2.4, 0.9, 0.1), post, 0.02)
    xa = x0 - LEN / 2 + 0.2
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.6, location=(xa, -0.1, zs[0] + 0.75)); bpy.context.object.data.materials.append(amb)
    bpy.ops.mesh.primitive_cone_add(radius1=0.18, depth=0.3, location=(xa, -0.1, zs[0] + 0.3), rotation=(math.pi, 0, 0)); bpy.context.object.data.materials.append(amb)
    b3d.stack_camera((0, 0, (max(zs) + base) / 2 + 0.3), 12.6, az=0.0, el=6.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1400, 520), 40); b3d.lights(10)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
