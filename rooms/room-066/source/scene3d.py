"""ROOM 066 3D sprites: side view of a spool on a tiled plank (0.4 per tile). Wheel radius 1.4 tiles, axle half of it.
p*: thread leaves the axle from the bottom or the top, straight to a coral ring; '실 N칸' = how far the hand pulls.
a*: spool moved to the answer tick (amber), grey ghost at 0, amber 'N칸' label."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, res
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U, RW, RA = 0.4, 0.56, 0.28
X90 = (math.radians(90), 0, 0)


def label(s, x, z, size, m, y=-0.5):
    bpy.ops.object.text_add(location=(x, y, z), rotation=X90); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def cyl(r, depth, loc, m, rot=X90, v=64):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, vertices=v, location=loc, rotation=rot)
    o = bpy.context.object; o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = True
    return o


def spool(x, M, ghost=False):
    zc = RW
    if ghost:
        bpy.ops.mesh.primitive_torus_add(major_radius=RW - 0.03, minor_radius=0.025, location=(x, 0.32, zc), rotation=X90)
        bpy.context.object.data.materials.append(M['ghost'])
        bpy.ops.mesh.primitive_torus_add(major_radius=RA, minor_radius=0.02, location=(x, 0.32, zc), rotation=X90)
        bpy.context.object.data.materials.append(M['ghost']); return
    b3d.bevel(cyl(RW, 0.07, (x, 0.22, zc), M['flange']), 0.02, 2)
    bpy.ops.mesh.primitive_torus_add(major_radius=RW - 0.035, minor_radius=0.035, location=(x, -0.22, zc), rotation=X90)
    bpy.context.object.data.materials.append(M['flange'])
    cyl(RA, 0.42, (x, 0, zc), M['thread'])
    cyl(0.07, 0.02, (x, -0.22, zc), M['hub'])


def scene(k, after):
    side, L = BOARDS[k]
    M = {'flange': b3d.mat('flange', b3d.PAL['mint'], rough=0.3, coat=0.6), 'thread': b3d.mat('thread', (0.95, 0.90, 0.78), rough=0.7, coat=0.0),
         'hub': b3d.mat('hub', (0.20, 0.24, 0.32), rough=0.4), 'ghost': b3d.mat('ghost', (0.45, 0.50, 0.60), rough=0.5, coat=0.0)}
    wood = b3d.mat('wood', (0.45, 0.32, 0.22), rough=0.6, coat=0.1); tick = b3d.mat('tick', (0.85, 0.88, 0.94), rough=0.5)
    coral = b3d.mat('coral', (0.90, 0.30, 0.24), rough=0.35, coat=0.5); amber = b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3)
    white = b3d.mat('white', (0.96, 0.97, 0.99), rough=0.4); soft = b3d.mat('soft', (0.70, 0.75, 0.85), rough=0.5)
    q = amber.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
    q.inputs['Emission Strength'].default_value = 0.6
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.6, 0, -0.07)); o = bpy.context.object
    o.scale = (4.7, 0.7, 0.14); o.data.materials.append(wood); b3d.bevel(o, 0.02, 2)
    d = res[k]
    for i in range(10):
        hot = after and i == d
        bpy.ops.mesh.primitive_cube_add(size=1, location=(i * U, -0.36, 0.0)); t = bpy.context.object
        t.scale = (0.03 if not hot else 0.06, 0.02, 0.12); t.data.materials.append(amber if hot else tick)
        label(str(i), i * U, -0.32, 0.24, amber if hot else soft)
    if after:
        spool(0, M, ghost=True); spool(d * U, M)
        label(f'{d}칸', d * U + (0.95 if d < 8 else -0.95), RW, 0.36, amber)
    else:
        spool(0, M)
        zt = RW - RA if side == 'bottom' else RW + RA
        xh = 3.85
        cyl(0.018, xh - 0.0, (xh / 2, 0, zt), M['thread'], rot=(0, math.radians(90), 0), v=12)
        bpy.ops.mesh.primitive_torus_add(major_radius=0.11, minor_radius=0.035, location=(xh + 0.11, 0, zt), rotation=X90)
        bpy.context.object.data.materials.append(coral)
        label(f'실 {L}칸 →', 3.75, zt + 0.32, 0.28, white)
    b3d.stack_camera((1.75, 0, 0.45), 5.6, az=0.0, el=4.0)
    pass


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1100, 440), 40); b3d.lights(7)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
