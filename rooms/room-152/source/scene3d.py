"""ROOM 152 3D sprites: a wooden mancala board seen from above at a slant: two rows of six cups, a long store at each
end (yours on the right, mint rim), glass seeds in the cups and a count beside every cup. A yellow ring marks the cup
you lift. p*: the start. a*: the board after the move; the store count glows mint and a captured cup pair gets coral
rings."""
import math, os, random, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
SP = 0.78; EL = 55.0; YR = 0.48


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - EL), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def cup(x, y, m, rx=0.3, ry=0.3):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(x, y, 0.1), segments=32, ring_count=16); o = bpy.context.object; o.scale = (rx, ry, 0.12); o.data.materials.append(m)


def seeds(x, y, n, mats, rng, rx=0.2, ry=0.2):
    for s in range(n):
        a = rng.random() * 2 * math.pi; r = math.sqrt(rng.random())
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(x + r * rx * math.cos(a), y + r * ry * math.sin(a), 0.2 + 0.05 * (s // 6)), segments=12, ring_count=6)
        bpy.context.object.data.materials.append(mats[s % len(mats)])


def ring(x, y, m, r=0.33, z=0.24):
    bpy.ops.mesh.primitive_torus_add(location=(x, y, z), major_radius=r, minor_radius=0.03, major_segments=40); bpy.context.object.data.materials.append(m)


def scene(k, after):
    b = BOARDS[k]; store, me, op, capd, last = RES[k]
    if not after: me, op, store = b['me'], b['op'], 0
    rng = random.Random(7)
    wood = b3d.mat('wood', (0.24, 0.12, 0.05), rough=0.6, coat=0.1); hole = b3d.mat('hole', (0.12, 0.06, 0.02), rough=0.9, coat=0)
    mats = [b3d.mat(f's{i}', c, rough=0.15, coat=0.6) for i, c in enumerate([(0.2, 0.55, 0.95), (0.95, 0.35, 0.3), (0.95, 0.8, 0.25), (0.3, 0.8, 0.5)])]
    ink = b3d.mat('ink', (0.97, 0.97, 1.0), rough=0.6, coat=0); glow(ink, (0.97, 0.97, 1.0), 0.6)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.5)
    yel = b3d.mat('yel', (1.0, 0.8, 0.2), rough=0.4, coat=0); glow(yel, (1.0, 0.8, 0.2), 1.5)
    cor = b3d.mat('cor', (0.95, 0.42, 0.35), rough=0.5, coat=0); glow(cor, (0.95, 0.42, 0.35), 1.2)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.02)); o = bpy.context.object; o.scale = (8 * SP + 0.4, 2.1, 0.16); o.data.materials.append(wood); b3d.bevel(o, 0.3, 6)
    X = lambda j: (j - 2.5) * SP
    for j in range(6):
        for row, cnt, y in (('m', me[j], -YR), ('o', op[j], YR)):
            cup(X(j), y, hole); seeds(X(j), y, cnt, mats, rng)
            text(str(cnt), (X(j), y + (-0.5 if row == 'm' else 0.5), 0.12), 0.24, ink)
    sx = 3.5 * SP + 0.05
    cup(sx, 0, hole, 0.3, 0.8); cup(-sx, 0, hole, 0.3, 0.8)
    seeds(sx, 0, store, mats, rng, 0.18, 0.6)
    bpy.ops.mesh.primitive_torus_add(location=(sx, 0, 0.17), major_radius=1, minor_radius=0.03, major_segments=48); o = bpy.context.object; o.scale = (0.32, 0.84, 1); o.data.materials.append(mint)
    text(str(store), (sx + 0.55, 0, 0.12), 0.34 if after else 0.26, mint if after else ink)
    text('내 창고', (sx, -1.05, 0.12), 0.18, ink); text('상대 창고', (-sx, 1.05, 0.12), 0.18, ink)
    if not after: ring(X(b['pick']), -YR, yel)
    elif capd is not None:
        ring(X(capd), -YR, cor); ring(X(capd), YR, cor)
    b3d.stack_camera((0, -0.05, 0.1), 7.2, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 560), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
