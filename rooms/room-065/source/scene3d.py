"""ROOM 065 3D sprites: two pendulums from one wooden beam, front view, string lengths to scale (0.3 per tile).
Left: small mint bob, '8번' = swings it makes. Right: big coral bob, '?번'. 'aX' shows the right count in amber."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, res
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
S, TOP = 0.3, 5.0


def label(s, x, z, size, m):
    bpy.ops.object.text_add(location=(x, -0.5, z), rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.03; t.data.materials.append(m)


def pend(x, L, r, m, txt, tm, M, tilt):
    z1 = TOP - L * S; a = math.radians(tilt); bx = x + math.sin(a) * L * S; bz = TOP - math.cos(a) * L * S
    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=L * S, vertices=12, location=((x + bx) / 2, 0, (TOP + bz) / 2), rotation=(0, -a, 0))
    bpy.context.object.data.materials.append(M['string'])
    for i in range(1, L):   # bead every tile so the length can be counted
        f = i / L; bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(x + (bx - x) * f, 0, TOP + (bz - TOP) * f))
        bpy.context.object.data.materials.append(M['bead'])
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(bx, 0, bz - r * 0.9), segments=48, ring_count=24)
    bpy.context.object.data.materials.append(m)
    label(txt, bx, bz - 2 * r - 0.35, 0.42, tm)
    label(f'줄 {L}칸', x + (0.62 if x > 0 else -0.62), TOP - 0.35, 0.24, M['soft'])


def scene(k, after):
    a, n, b = BOARDS[k]
    M = {'string': b3d.mat('string', (0.92, 0.88, 0.78), rough=0.6), 'bead': b3d.mat('bead', (0.55, 0.60, 0.70), rough=0.4),
         'soft': b3d.mat('soft', (0.80, 0.84, 0.92), rough=0.5)}
    wood = b3d.mat('wood', (0.45, 0.32, 0.22), rough=0.6, coat=0.1)
    mint = b3d.mat('mint', b3d.PAL['mint'], rough=0.3, coat=0.5); coral = b3d.mat('coral', (0.90, 0.30, 0.24), rough=0.35, metal=0.3, coat=0.5)
    amber = b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3); white = b3d.mat('white', (0.96, 0.97, 0.99), rough=0.4)
    for p in (mint, amber):
        q = p.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
        q.inputs['Emission Strength'].default_value = 0.6
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, TOP + 0.12)); o = bpy.context.object
    o.scale = (2.9, 0.4, 0.24); o.data.materials.append(wood); b3d.bevel(o, 0.04, 3)
    pend(-0.75, a, 0.17, mint, f'{n}번', mint, M, 10)
    pend(0.75, b, 0.32, coral, f'{res[k]}번' if after else '?번', amber if after else white, M, -10)
    b3d.stack_camera((0, 0, 2.2), 6.6, az=0.0, el=4.0)
    b3d.floor().location.z = -3.0


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((560, 1000), 40); b3d.lights(7)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
