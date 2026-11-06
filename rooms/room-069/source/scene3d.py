"""ROOM 069 3D sprites: three nested cup stacks on a shelf in front of a tile wall (lines every 0.25, numbered 0..9).
Two stacks show their height ('4칸'), the third '?'. Under each stack: number of cups. a*: the third stack's height amber."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, res
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U = 0.25
X90 = (math.radians(90), 0, 0)
COLS = [(0.90, 0.30, 0.24), (0.98, 0.62, 0.08), (0.24, 0.56, 0.92)]


def label(s, x, z, size, m, y=-0.6):
    bpy.ops.object.text_add(location=(x, y, z), rotation=X90); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def box(loc, scale, m, bev=0.02):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 2); return o


def stack(x, n, H, h, m, rim):
    for i in range(n):
        z0 = i * h * U; d = H * U
        bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=0.2, radius2=0.29, depth=d - 0.03, location=(x, 0, z0 + (d - 0.03) / 2))
        o = bpy.context.object; o.data.materials.append(m)
        for p in o.data.polygons: p.use_smooth = True
        bpy.ops.mesh.primitive_torus_add(major_radius=0.29, minor_radius=0.03, location=(x, 0, z0 + d - 0.03), major_segments=48)
        bpy.context.object.data.materials.append(rim)
    return (H + (n - 1) * h) * U


def scene(k, after):
    (n1, t1), (n2, t2), q = BOARDS[k]
    H = next(H for H in range(1, 10) for h in range(1, 10) if H > h and H + (n1 - 1) * h == t1 and H + (n2 - 1) * h == t2)
    h = (t1 - H) // (n1 - 1) if n1 > 1 else (t2 - H) // (n2 - 1)
    cup = b3d.mat('cup', COLS['ABCD'.index(k) % 3], rough=0.3, coat=0.6); rim = b3d.mat('rim', (0.97, 0.97, 0.99), rough=0.3)
    wall = b3d.mat('wall', (0.20, 0.25, 0.36), rough=0.6, coat=0); line = b3d.mat('line', (0.55, 0.62, 0.75), rough=0.6, coat=0)
    wood = b3d.mat('wood', (0.45, 0.32, 0.22), rough=0.6, coat=0.1); white = b3d.mat('white', (0.96, 0.97, 0.99), rough=0.4)
    soft = b3d.mat('soft', (0.75, 0.80, 0.90), rough=0.5); amber = b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3)
    q_ = amber.node_tree.nodes['Principled BSDF']; q_.inputs['Emission Color'].default_value = q_.inputs['Base Color'].default_value
    q_.inputs['Emission Strength'].default_value = 0.7
    box((0, 0.45, 1.2), (2.9, 0.05, 2.6), wall, 0.01)
    for i in range(1, 10):
        box((0.05, 0.41, i * U), (2.7, 0.02, 0.012), line, 0.002); label(str(i), -1.28, i * U, 0.17, soft, y=0.38)
    box((0, 0, -0.06), (3.0, 0.9, 0.12), wood, 0.03)
    xs = (-0.8, 0.05, 0.9)
    for x, n, t, ask in ((xs[0], n1, t1, False), (xs[1], n2, t2, False), (xs[2], q, res[k], True)):
        if ask and not after:   # hidden behind a cover box so the wall lines cannot give the height away
            box((x, 0, 1.17), (0.72, 0.72, 2.34), b3d.mat('cover', (0.93, 0.86, 0.72), rough=0.7, coat=0), 0.03)
            label('?', x, 1.2, 0.6, b3d.mat('qm', (0.35, 0.28, 0.20), rough=0.6), y=-0.37)
            label(f'{n}개', x, -0.2, 0.28, white, y=-0.48); continue
        top = stack(x, n, H, h, cup, rim)
        label(f'{n}개', x, -0.2, 0.28, white, y=-0.48)
        if ask:
            label(f'{t}칸', x, top + 0.26, 0.32, amber); box((x, 0.4, top), (0.75, 0.03, 0.025), amber, 0.004)
        else:
            label(f'{t}칸', x, top + 0.26, 0.3, white)
    b3d.stack_camera((0.05, 0, 1.02), 3.3, az=0.0, el=8.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((820, 900), 40); b3d.lights(5)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
