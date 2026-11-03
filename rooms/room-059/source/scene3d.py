"""ROOM 059 3D sprites: four pulley rigs, front view. 'pA'..'pD' = start, mint arrow '당김 N칸' beside the free rope end.
'aA'..'aD' = after the pull: box raised (ghost at start), amber arrow with its rise, rope end lowered."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import RIGS, rise
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U = 0.25                 # one tile
TOPZ, PZ, PRAD = 5.2, 4.75, 0.3
BOX0, BS = 0.6, 0.7      # box bottom at start, box size
END0 = 2.8               # free rope end height at start


def label(s, x, z, size, m, y=-0.6, al='CENTER'):
    bpy.ops.object.text_add(location=(x, y, z), rotation=(math.radians(90), 0, 0))
    t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = al; t.data.align_y = 'CENTER'; t.data.extrude = 0.03; t.data.materials.append(m)


def rope(x0, z0, x1, z1, m, r=0.035):
    L = math.hypot(x1 - x0, z1 - z0); ang = math.atan2(x1 - x0, z1 - z0)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, vertices=12, location=((x0 + x1) / 2, 0, (z0 + z1) / 2), rotation=(0, ang, 0))
    bpy.context.object.data.materials.append(m)


def pulley(x, z, wheel, hub):
    bpy.ops.mesh.primitive_cylinder_add(radius=PRAD + 0.03, depth=0.16, vertices=48, location=(x, 0, z), rotation=(math.radians(90), 0, 0))
    o = bpy.context.object; o.data.materials.append(wheel); b3d.bevel(o, 0.03, 3)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.2, vertices=24, location=(x, -0.02, z), rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.materials.append(hub)


def arrow(x, z0, z1, m, t=0.07):   # vertical arrow from z0 to z1
    d = 1 if z1 > z0 else -1
    rope(x, z0, x, z1 - d * 0.18, m, t)
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.17, radius2=0, depth=0.3, location=(x, 0, z1 - d * 0.12),
                                    rotation=(0 if d > 0 else math.pi, 0, 0))
    bpy.context.object.data.materials.append(m)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, z0)); o = bpy.context.object; o.scale = (0.32, 0.05, 0.05); o.data.materials.append(m)


def box(x, z, m, size=BS, wide=1.4):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, z + size / 2)); o = bpy.context.object
    o.scale = (size * wide, size, size); o.data.materials.append(m); b3d.bevel(o, 0.05, 3)


def scene(k, after):
    kind, n, pull = RIGS[k]
    b3d.reset((700, 900), 48); b3d.lights(6)
    b3d.stack_camera((0.15, 0, 2.95), 6.0, az=0.0, el=6.0)
    wood = b3d.mat('wood', (0.45, 0.32, 0.22), rough=0.6, coat=0.1)
    wheel = b3d.mat('wheel', (0.62, 0.68, 0.78), rough=0.3, metal=0.6); hub = b3d.mat('hub', (0.25, 0.28, 0.34), rough=0.4)
    rp = b3d.mat('rope', (0.93, 0.86, 0.66), rough=0.7, coat=0.0)
    crate = b3d.mat('crate', (0.85, 0.30, 0.22), rough=0.45, coat=0.4)
    ghost = b3d.mat('ghost', (0.85, 0.30, 0.22), rough=0.5, coat=0.0); ghost.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.22
    mint = b3d.mat('mint', b3d.PAL['mint'], rough=0.35, coat=0.4); amber = b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3)
    for p in (mint, amber):
        q = p.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
        q.inputs['Emission Strength'].default_value = 0.7
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.15, 0, TOPZ + 0.12)); o = bpy.context.object
    o.scale = (3.4, 0.5, 0.24); o.data.materials.append(wood); b3d.bevel(o, 0.04, 3)
    up = rise(n, pull) * U if after else 0.0
    bz = BOX0 + up; btop = bz + BS; end = END0 - (pull * U if after else 0.0)

    def hang(x0, x1):   # pulley axle strap from the beam
        rope(x0, TOPZ, x1, PZ, hub, 0.04)
    if kind == 'fixed':
        bx = -PRAD; ex = PRAD; pulley(0, PZ, wheel, hub); hang(0, 0)
        rope(bx, btop, bx, PZ, rp); rope(ex, PZ, ex, end, rp)
    elif kind == 'double_fixed':
        bx, ex = -0.9, 0.9; pulley(-0.6, PZ, wheel, hub); pulley(0.6, PZ, wheel, hub); hang(-0.6, -0.6); hang(0.6, 0.6)
        rope(bx, btop, bx, PZ, rp); rope(-0.6, PZ + PRAD, 0.6, PZ + PRAD, rp); rope(ex, PZ, ex, end, rp)
    elif kind == 'movable':
        bx = -0.3; mz = btop + 0.38; pulley(bx, mz, wheel, hub); rope(bx, btop, bx, mz, hub, 0.05)
        pulley(0.3, PZ, wheel, hub); hang(0.3, 0.3)
        rope(-0.6, TOPZ, -0.6, mz, rp); rope(0.0, mz, 0.0, PZ, rp); ex = 0.6; rope(ex, PZ, ex, end, rp)
    else:   # triple: anchor on the box, fixed, movable on the box, fixed
        bx = 0.15; mz = btop + 0.38; pulley(-0.15, PZ, wheel, hub); pulley(0.45, mz, wheel, hub); pulley(1.05, PZ, wheel, hub)
        hang(-0.15, -0.15); hang(1.05, 1.05); rope(0.45, btop, 0.45, mz, hub, 0.05)
        rope(-0.45, btop, -0.45, PZ, rp); rope(0.15, PZ, 0.15, mz, rp); rope(0.75, mz, 0.75, PZ, rp); ex = 1.35; rope(ex, PZ, ex, end, rp)
    W = 1.9 if kind == 'triple' else 1.4
    box(bx, bz, crate, wide=W)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.13, minor_radius=0.04, location=(ex, 0, end - 0.12), rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.materials.append(hub)
    if after:
        box(bx, BOX0, ghost, wide=W)
        arrow(bx - BS * W / 2 - 0.28, BOX0 + BS, btop, amber)
        label(f'{int(round(up / U))}칸', bx, BOX0 + BS / 2, 0.55, amber, -0.62)
    else:
        arrow(ex + 0.35, END0, END0 - pull * U, mint)
        label(f'당김 {pull}칸', ex + 0.1, END0 - pull * U - 0.45, 0.5, mint)
    b3d.floor().location.z = -0.5


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
