"""ROOM 166 3D sprites: a patch of grass with a road (open path), a triangular flower bed or a round pond (closed
loops), and a paper tag naming the length and the spacing. p*: only the first tree stands at the start. a*: every tree
in place, the first one with a mint ring."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, trees
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
EL = 52.0
TAG = {'line': '길 {L}m · {d}m마다 · 양 끝까지', 'tri': '꽃밭 둘레 {L}m · {d}m마다', 'circle': '연못 둘레 {L}m · {d}m마다'}


def box(loc, scale, m, bev=0.0, rz=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=(0, 0, rz)); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 4)
    return o


def cyl(loc, r, d, m, v=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d, location=loc); o = bpy.context.object; o.data.materials.append(m); return o


def tree(x, y, M, ring=None):
    cyl((x, y, 0.2), 0.05, 0.3, M['trunk'], 16)
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.2, radius2=0, depth=0.5, location=(x, y, 0.55)); bpy.context.object.data.materials.append(M['leaf'])
    if ring:
        bpy.ops.mesh.primitive_torus_add(location=(x, y, 0.07), major_radius=0.25, minor_radius=0.025, major_segments=40); bpy.context.object.data.materials.append(ring)


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(70), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def path_point(b, s):  # point at distance s along the path, path scaled to fit
    L = b['L']; u = s / L
    if b['shape'] == 'line': return (-1.8 + 3.6 * u, -0.1)
    if b['shape'] == 'circle': a = math.pi / 2 + 2 * math.pi * u; return (1.25 * math.cos(a), -0.05 + 1.0 * math.sin(a))
    V = [(0, 1.0), (1.35, -1.0), (-1.35, -1.0)]; t = u * 3; i = min(int(t), 2); f = t - i
    a, c = V[i], V[(i + 1) % 3]; return (a[0] + (c[0] - a[0]) * f, -0.05 + a[1] + (c[1] - a[1]) * f)


def scene(key, after):
    b = BOARDS[key]
    M = {'trunk': b3d.mat('trunk', (0.35, 0.2, 0.1), rough=0.8, coat=0), 'leaf': b3d.mat('leaf', (0.15, 0.55, 0.22), rough=0.6, coat=0)}
    grass = b3d.mat('grass', (0.42, 0.68, 0.32), rough=0.9, coat=0); road = b3d.mat('road', (0.35, 0.36, 0.4), rough=0.8, coat=0)
    soil = b3d.mat('soil', (0.45, 0.28, 0.15), rough=0.9, coat=0); water = b3d.mat('water', (0.2, 0.5, 0.9), rough=0.1, coat=0.6)
    stone = b3d.mat('stone', (0.75, 0.75, 0.72), rough=0.7, coat=0); paper = b3d.mat('paper', (0.98, 0.93, 0.78), rough=0.7, coat=0)
    ink = b3d.mat('ink', (0.1, 0.08, 0.06), rough=0.8, coat=0); mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0)
    q = mint.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (0.15, 0.85, 0.6, 1); q.inputs['Emission Strength'].default_value = 1.4
    box((0, -0.05, -0.05), (4.4, 2.9, 0.1), grass, 0.05)
    if b['shape'] == 'line':
        box((0, -0.1, 0.01), (3.9, 0.45, 0.03), road)
        for i in range(9): box((-1.6 + i * 0.4, -0.1, 0.03), (0.18, 0.04, 0.01), stone)
    elif b['shape'] == 'circle':
        cyl((0, -0.05, 0.0), 1.0, 0.04, water, 64); o = bpy.context.object; o.scale = (1.25 / 1.0 * 0.85, 0.85, 1)
        bpy.ops.mesh.primitive_torus_add(location=(0, -0.05, 0.02), major_radius=1.0, minor_radius=0.06, major_segments=64); t = bpy.context.object; t.scale = (1.25, 1.0, 1); t.data.materials.append(stone)
    else:
        V = [(0, 0.95), (1.35, -1.0), (-1.35, -1.0)]
        me = bpy.data.meshes.new('bed'); me.from_pydata([(x, y - 0.05, 0.02) for x, y in V], [], [(0, 2, 1)]); me.materials.append(soil)
        bpy.context.collection.objects.link(bpy.data.objects.new('bed', me))
        for i in range(3):
            a, c = V[i], V[(i + 1) % 3]; mx, my = (a[0] + c[0]) / 2, (a[1] + c[1]) / 2 - 0.05
            box((mx, my, 0.03), (math.hypot(c[0] - a[0], c[1] - a[1]), 0.08, 0.06), stone, 0, math.atan2(c[1] - a[1], c[0] - a[0]))
    pts = trees(b) if after else [0]
    for i, s in enumerate(pts):
        x, y = path_point(b, s); tree(x, y + (0.32 if b['shape'] == 'line' else 0), M, mint if (after and i == 0) else (mint if not after else None))
    o = box((0, 1.75, 0.5), (3.9, 0.05, 0.62), paper, 0.03); o.rotation_euler = (math.radians(-20), 0, 0)
    text(TAG[b['shape']].format(**b), (0, 1.71, 0.52), 0.36, ink)
    b3d.stack_camera((0, 0.2, 0.3), 5.6, az=0.0, el=EL)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((1000, 900), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
