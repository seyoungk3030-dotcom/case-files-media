"""ROOM 168 3D sprites: books on a wooden shelf, spines facing us with the volume number, thickness in cm on a label
under each book, a green bookworm on top of the start book's right edge (its first page) and a red pin on the end
book's left edge (its last page), and a paper tag naming the trip. p*: before. a*: the worm's tunnel as a glowing mint
bar from start to end."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, edges
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
EL = 14.0; U = 0.34; H = 1.45; D = 0.9
COLS = [(0.5, 0.06, 0.05), (0.05, 0.16, 0.45), (0.7, 0.42, 0.03), (0.06, 0.32, 0.12), (0.3, 0.1, 0.4)]


def box(loc, scale, m, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 4)
    return o


def text(s, loc, size, m, rot=(90, 0, 0)):
    bpy.ops.object.text_add(location=loc, rotation=tuple(math.radians(r) for r in rot)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def scene(key, after):
    b = BOARDS[key]; E = edges(b['t']); W = sum(b['t']) * U; x0 = -W / 2
    wood = b3d.mat('wood', (0.45, 0.28, 0.15), rough=0.7, coat=0); paper = b3d.mat('paper', (0.98, 0.93, 0.78), rough=0.7, coat=0)
    ink = b3d.mat('ink', (0.1, 0.08, 0.06), rough=0.8, coat=0); white = b3d.mat('white', (0.97, 0.97, 0.95), rough=0.6, coat=0)
    pages = b3d.mat('pages', (0.95, 0.92, 0.82), rough=0.8, coat=0)
    worm = b3d.mat('worm', (0.4, 0.8, 0.25), rough=0.4, coat=0); pin = b3d.mat('pin', (0.9, 0.15, 0.12), rough=0.4, coat=0)
    mint = glowm('mint', (0.15, 0.85, 0.6), 2.0)
    SW = max(3.2, W + 0.4)
    box((0, 0, -0.06), (SW, D + 0.2, 0.12), wood, 0.02)
    box((0, D / 2 + 0.12, H / 2), (SW, 0.06, H + 0.3), wood)
    for i, (l, r) in enumerate(E):
        w = (r - l) * U - 0.02; cx = x0 + (l + r) / 2 * U
        m = b3d.mat(f'c{i}', COLS[i % 5], rough=0.5, coat=0.2)
        box((cx, 0, H / 2), (w, D, H), m, 0.015)
        box((cx, 0.02, H / 2), (w - 0.06, D - 0.02, H - 0.08), pages)
        text(str(i + 1), (cx, -D / 2 - 0.012, H * 0.62), min(0.3, w * 0.75), white)
        text(f'{r - l}cm' if w > 0.5 else f'{r - l}\ncm', (cx, -D / 2 - 0.012, H * 0.2), 0.2 if w > 0.5 else 0.17, white)
    a, c = b['a'], b['b']
    sx = x0 + E[a - 1][1] * U; ex = x0 + E[c - 1][0] * U
    for j in range(5):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11 - j * 0.01, location=(sx - 0.02, -0.3 + j * 0.15, H + 0.1))
        bpy.context.object.data.materials.append(worm)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.4, location=(ex + 0.05, -0.2, H + 0.2)); bpy.context.object.data.materials.append(pin)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.07, location=(ex + 0.05, -0.2, H + 0.42)); bpy.context.object.data.materials.append(pin)
    if after:
        lo, hi = sorted((sx, ex)); box(((lo + hi) / 2, -D / 2 - 0.06, H * 0.42), (max(hi - lo, 0.04), 0.05, 0.1), mint)
        for xx in (lo, hi): box((xx, -D / 2 - 0.06, H * 0.42), (0.05, 0.05, 0.35), mint)
    o = box((0, D / 2 + 0.2, H + 0.65), (SW, 0.05, 0.5), paper, 0.03)
    text(f'{a}권 첫 쪽 → {c}권 마지막 쪽', (0, D / 2 + 0.16, H + 0.65), 0.27, ink)
    b3d.stack_camera((0, 0, H / 2 + 0.25), 4.0, az=0.0, el=EL)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((1000, 900), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
