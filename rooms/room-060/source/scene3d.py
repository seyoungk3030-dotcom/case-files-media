"""ROOM 060 3D sprites: four domino boards seen from the front-top. 'pA'..'pD' = start (all standing, mint push arrow),
'aA'..'aD' = after: dominoes on reached runs lie toppled toward the chain, the ringing bell glows amber."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import NODES, BOARDS, runs, fall
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
EL = 66.0
SP, DH, DW, DT = 0.3, 0.42, 0.3, 0.09     # spacing, height, width, thickness


def label(s, x, y, z, size, m):
    bpy.ops.object.text_add(location=(x, y, z), rotation=(math.radians(90 - EL), 0, 0))
    t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.04; t.data.materials.append(m)


def domino(x, y, ang, m, tilt=0.0):
    """Standing domino at (x, y), facing along heading ang (radians, 0 = +y). tilt topples it forward along the heading."""
    bpy.ops.mesh.primitive_cube_add(size=1); o = bpy.context.object
    o.scale = (DW, DT, DH); o.data.materials.append(m); b3d.bevel(o, 0.015, 2)
    bpy.ops.object.transform_apply(scale=True)
    for v in o.data.vertices: v.co.z += DH / 2      # pivot at the bottom
    o.rotation_mode = 'XYZ'; o.rotation_euler = (-tilt, 0, -ang)
    hx, hy = math.sin(ang), math.cos(ang)
    o.location = (x + hx * (DT / 2) * (1 if tilt else 0), y + hy * (DT / 2) * (1 if tilt else 0), 0)


def bell(x, y, m, post):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.5, location=(x, y, 0.25)); bpy.context.object.data.materials.append(post)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.34, location=(x, y, 0.45), segments=32, ring_count=16); o = bpy.context.object
    o.scale = (1, 1, 1.05); o.data.materials.append(m)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=0.06, location=(x, y, 0.42)); bpy.context.object.data.materials.append(m)


def scene(k, after):
    b3d.reset((760, 900), 48); b3d.lights(7)
    b3d.stack_camera((0, 2.65, 0.2), 7.4, az=0.0, el=EL)
    board = b3d.mat('board', (0.10, 0.13, 0.20), rough=0.6, coat=0.1)
    ivory = b3d.mat('ivory', (0.93, 0.91, 0.85), rough=0.35, coat=0.5)
    down = b3d.mat('down', (0.45, 0.85, 0.74), rough=0.45, coat=0.3)
    gold = b3d.mat('gold', (0.85, 0.72, 0.35), rough=0.25, metal=0.8)
    grey = b3d.mat('grey', (0.45, 0.48, 0.55), rough=0.35, metal=0.5)
    post = b3d.mat('post', (0.25, 0.28, 0.34), rough=0.4)
    white = b3d.mat('white', (0.96, 0.97, 0.99), rough=0.4)
    mint = b3d.mat('mint', b3d.PAL['mint'], rough=0.35, coat=0.4); amber = b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3)
    for p in (mint, amber):
        q = p.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
        q.inputs['Emission Strength'].default_value = 0.8
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 2.65, -0.06)); o = bpy.context.object
    o.scale = (5.6, 6.6, 0.12); o.data.materials.append(board); b3d.bevel(o, 0.05, 3)
    order, rung = fall(k) if after else ([], [])
    fallen = {frozenset(e): e for e in order}
    reached = {'S'} | {o for _, o in order}
    into = {o: n for n, o in order}
    for u, v, gap in runs(k):
        (x0, y0), (x1, y1) = NODES[u], NODES[v]
        L = math.hypot(x1 - x0, y1 - y0); ang = math.atan2(x1 - x0, y1 - y0)
        end = L - (0.55 if v in 'LMR' else SP)
        ts = [SP + i * SP for i in range(int((end - SP) / SP + 1e-6) + 1)]
        if gap:
            mid = len(ts) // 2; ts = ts[:mid - 2] + ts[mid + 1:]
        e = fallen.get(frozenset((u, v)))
        for t in ts:
            px, py = x0 + (x1 - x0) * t / L, y0 + (y1 - y0) * t / L
            if e:
                a = ang if e[0] == u else ang + math.pi
                domino(px, py, a, down, math.radians(68))
            else:
                domino(px, py, ang, ivory)
    for n, (x, y) in NODES.items():
        if n in 'LMR': continue
        if n == 'S':
            ang = 0.0
        else:
            ang = 0.0 if n in ('F', 'Lm', 'Mm', 'Rm') else (-math.pi / 2 if n == 'Lf' else math.pi / 2)
        if after and n in reached:
            if n == 'S': a = 0.0
            else:
                (px, py) = NODES[into[n]]; a = math.atan2(x - px, y - py)
            domino(x, y, a, down, math.radians(68))
        else:
            domino(x, y, ang, ivory)
    bells = BOARDS[k]['bells']
    for b in 'LMR':
        x, y = NODES[b]; ring = b in rung
        bell(x, y, amber if ring else (gold if not after else grey), post)
        label(str(bells[b]), x, y + 0.75, 1.15, 0.9, amber if ring else white)
        if ring:
            bpy.ops.mesh.primitive_torus_add(major_radius=0.62, minor_radius=0.05, location=(x, y, 0.45), rotation=(math.radians(90 - EL), 0, 0))
            bpy.context.object.data.materials.append(amber)
    if not after:
        bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.2, radius2=0, depth=0.4, location=(0, -0.4, 0.25), rotation=(math.radians(-90), 0, 0))
        bpy.context.object.data.materials.append(mint)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.45, location=(0, -0.75, 0.25), rotation=(math.radians(90), 0, 0))
        bpy.context.object.data.materials.append(mint)
    b3d.floor().location.z = -0.5


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
