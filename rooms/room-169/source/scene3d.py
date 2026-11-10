"""ROOM 169 3D sprites: a train on a track with its front at the entrance of a tunnel (or a bridge over water), lengths
drawn to scale, and a paper tag with the lengths, the speed and the question. p*: before. a*: a glowing mint bar under
the track showing how far the train's front travels while the question is true."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
EL = 24.0; U = 0.042
NAME = {'tunnel': '터널', 'bridge': '다리'}
ASK = {'pass': '다 지나가는 데 몇 초?', 'hidden': '통째로 숨는 시간은?'}


def box(loc, scale, m, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 4)
    return o


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def scene(key, after):
    b = BOARDS[key]; L, T = b['L'] * U, b['T'] * U
    xe = -(L + 2 * T) / 2 + T  # tunnel entrance; train spans [xe - T, xe]; room for the tail to come out
    grass = b3d.mat('grass', (0.25, 0.5, 0.2), rough=0.9, coat=0); rail = b3d.mat('rail', (0.3, 0.3, 0.33), rough=0.4, metal=0.5, coat=0)
    rock = b3d.mat('rock', (0.22, 0.17, 0.13), rough=0.8, coat=0); dark = b3d.mat('dark', (0.03, 0.03, 0.04), rough=0.9, coat=0)
    water = b3d.mat('water', (0.12, 0.35, 0.75), rough=0.1, coat=0.6); deck = b3d.mat('deck', (0.6, 0.35, 0.18), rough=0.6, coat=0)
    red = b3d.mat('red', (0.75, 0.1, 0.08), rough=0.35, coat=0.4); win = b3d.mat('win', (0.75, 0.9, 1.0), rough=0.1, coat=0.5)
    paper = b3d.mat('paper', (0.98, 0.93, 0.78), rough=0.7, coat=0); ink = b3d.mat('ink', (0.1, 0.08, 0.06), rough=0.8, coat=0)
    mint = glowm('mint', (0.15, 0.85, 0.6), 2.0)
    span = L + 2 * T + 0.8
    if b['kind'] == 'tunnel':
        box((0, 0, -0.08), (span, 1.4, 0.16), grass, 0.03)
        box((xe + L / 2, 0.05, 0.42), (L, 1.0, 0.84), rock, 0.06)
        box((xe + 0.02, -0.3, 0.27), (0.06, 0.32, 0.46), dark); box((xe + L - 0.02, -0.3, 0.27), (0.06, 0.32, 0.46), dark)
    else:
        for sx in (-1, 1):
            w = T + 0.4; box(((xe - w / 2) if sx < 0 else (xe + L + w / 2), 0, -0.08), (w, 1.4, 0.16), grass, 0.03)
        box((xe + L / 2, 0, -0.3), (L, 1.4, 0.1), water)
        box((xe + L / 2, -0.3, 0.02), (L, 0.5, 0.06), deck, 0.01)
        for i in range(4): box((xe + L * (i + 0.5) / 4, -0.3, -0.15), (0.08, 0.08, 0.3), deck)
    box((0, -0.38, 0.03), (span, 0.03, 0.03), rail); box((0, -0.22, 0.03), (span, 0.03, 0.03), rail)
    n = 2; cl = T / n
    for i in range(n):
        cx = xe - T + cl * (i + 0.5)
        box((cx, -0.3, 0.2), (cl - 0.04, 0.3, 0.28), red, 0.04)
        for j in range(max(1, int(cl / 0.2))): box((cx - cl / 2 + 0.12 + j * 0.2, -0.455, 0.24), (0.1, 0.01, 0.1), win)
    if after:
        a, c = (xe, xe + L + T) if b['ask'] == 'pass' else (xe + T, xe + L)
        box(((a + c) / 2, -0.62, 0.02), (c - a, 0.04, 0.06), mint)
        for xx in (a, c): box((xx, -0.62, 0.08), (0.04, 0.04, 0.2), mint)
    tw = 3.9
    box((0, 0.9, 1.55), (tw, 0.05, 1.3), paper, 0.03)
    text(f"{NAME[b['kind']]} {b['L']}m · 기차 {b['T']}m", (0, 0.86, 1.95), 0.36, ink)
    text(f"1초에 {b['v']}m", (0, 0.86, 1.55), 0.36, ink)
    text(ASK[b['ask']], (0, 0.86, 1.15), 0.36, ink)
    b3d.stack_camera((0, 0, 0.8), max(4.4, span + 0.2), az=0.0, el=EL)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((1000, 860), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
