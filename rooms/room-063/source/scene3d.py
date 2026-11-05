"""ROOM 063 3D sprites, top view. 'pA'..'pD' = top disc (mint holes, amber clockwise arrow 'N칸') and bottom disc
(coral holes) side by side, positions 1-8 printed around each. 'aA'..'aD' = top disc turned and laid on the bottom one:
holes of the top disc as mint rings, the one spot where light passes glows amber."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, turn, through
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
R, HR = 1.0, 0.68


def pos(cx, p, r): a = math.radians(90 - (p - 1) * 45); return cx + r * math.cos(a), r * math.sin(a)


def label(s, x, y, z, size, m):
    bpy.ops.object.text_add(location=(x, y, z)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def cyl(x, y, z, r, d, m, v=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, vertices=v, location=(x, y, z)); o = bpy.context.object
    o.data.materials.append(m); return o


def disc(cx, holes, body, hole, M, nums=True):
    cyl(cx, 0, 0.0, R + 0.32, 0.04, M['ring'], 64)
    o = cyl(cx, 0, 0.08, R, 0.12, body, 64); b3d.bevel(o, 0.02, 2)
    cyl(cx, 0, 0.15, 0.1, 0.04, M['hub'], 24)
    for p in range(1, 9):
        x, y = pos(cx, p, HR)
        cyl(x, y, 0.145, 0.17, 0.02, hole if p in holes else M['dent'], 32)
        if nums:
            x, y = pos(cx, p, R + 0.17); label(str(p), x, y, 0.03, 0.22, M['num'])


def arrow(cx, n, m):
    a0 = 90.0; a1 = 90.0 - n * 45 + 8
    steps = 24
    for i in range(steps):
        a = math.radians(a0 + (a1 - a0) * (i + 0.5) / steps); x, y = cx + 1.47 * math.cos(a), 1.47 * math.sin(a)
        cyl(x, y, 0.06, 0.045, 0.05, m, 12)
    a = math.radians(a1); x, y = cx + 1.47 * math.cos(a), 1.47 * math.sin(a)
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.12, radius2=0, depth=0.26, location=(x, y, 0.06),
                                    rotation=(0, math.radians(90), a - math.radians(90) + math.pi))
    bpy.context.object.rotation_euler = (math.radians(-90), 0, a - math.pi)
    bpy.context.object.data.materials.append(m)


def scene(k, after):
    T, B, n = BOARDS[k]
    M = {'ring': b3d.mat('ring', (0.16, 0.19, 0.27), rough=0.6, coat=0.1), 'hub': b3d.mat('hub', (0.6, 0.62, 0.66), rough=0.3, metal=0.7),
         'dent': b3d.mat('dent', (0.70, 0.74, 0.80), rough=0.5), 'num': b3d.mat('num', (0.94, 0.95, 0.98), rough=0.4)}
    lid = b3d.mat('lid', (0.86, 0.88, 0.92), rough=0.35, coat=0.4); base = b3d.mat('base', (0.86, 0.88, 0.92), rough=0.35, coat=0.4)
    mint = b3d.mat('mint', b3d.PAL['mint'], rough=0.3, coat=0.5); coral = b3d.mat('coral', (0.95, 0.38, 0.30), rough=0.3, coat=0.5)
    amber = b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3)
    q = amber.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
    q.inputs['Emission Strength'].default_value = 1.0
    if after:
        b3d.stack_camera((0, 0, 0), 3.2, az=0.0, el=89.0)
        disc(0, B, base, coral, M)
        (hit,) = through(k)
        for p in turn(T, n):
            x, y = pos(0, p, HR)
            bpy.ops.mesh.primitive_torus_add(major_radius=0.2, minor_radius=0.045, location=(x, y, 0.17))
            bpy.context.object.data.materials.append(amber if p == hit else mint)
        x, y = pos(0, hit, HR); cyl(x, y, 0.16, 0.17, 0.03, amber, 32)
    else:
        b3d.stack_camera((0, 0.12, 0), 6.6, az=0.0, el=89.0)
        disc(-1.75, T, lid, mint, M); disc(1.75, B, base, coral, M)
        arrow(-1.75, n, amber)
        label(f'{n}칸', -1.75 + 1.25, 1.55, 0.05, 0.36, amber)
        label('위 판', -1.75, -1.62, 0.03, 0.3, M['num']); label('아래 판', 1.75, -1.62, 0.03, 0.3, M['num'])
    b3d.floor().location.z = -0.5


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 620) if not after else (600, 600), 40); b3d.lights(6)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
