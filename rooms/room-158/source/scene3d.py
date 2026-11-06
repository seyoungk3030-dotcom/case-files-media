"""ROOM 158 3D sprites: a fuse stretched over 11 numbered posts (0-10) on a dark board, thin and thick sections, a flame
at the left end and at the right end a flame or a clock tag with the seconds before it is lit. p*: the start. a*: the
two flames meeting at the post where they meet (mint ring), the burnt fuse dark."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U = 0.56; EL = 30.0; N = 10


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - EL), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def X(i): return (i - N / 2) * U


def flame(x, z, mf, mc):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, location=(x, 0, z + 0.06), segments=24, ring_count=12); o = bpy.context.object; o.scale = (1, 1, 1.7); o.data.materials.append(mf)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(x, -0.03, z + 0.03), segments=16, ring_count=8); o = bpy.context.object; o.scale = (1, 1, 1.5); o.data.materials.append(mc)


def scene(k, after):
    b = BOARDS[k]; seg = b['seg']; m, _ = RES[k]
    board = b3d.mat('board', (0.16, 0.12, 0.09), rough=0.8, coat=0); post = b3d.mat('post', (0.55, 0.4, 0.22), rough=0.6, coat=0)
    rope = b3d.mat('rope', (0.85, 0.2, 0.12), rough=0.7, coat=0); burnt = b3d.mat('burnt', (0.05, 0.05, 0.05), rough=0.9, coat=0)
    wht = b3d.mat('wht', (0.95, 0.95, 0.95), rough=0.5, coat=0); glow(wht, (1, 1, 1), 0.6)
    mf = b3d.mat('fl', (1.0, 0.55, 0.1), rough=0.5, coat=0); glow(mf, (1.0, 0.45, 0.05), 3.0)
    mc = b3d.mat('flc', (1.0, 0.95, 0.6), rough=0.5, coat=0); glow(mc, (1.0, 0.9, 0.5), 4.0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.6)
    tagm = b3d.mat('tag', (0.98, 0.85, 0.3), rough=0.4, coat=0); ink = b3d.mat('ink', (0.1, 0.08, 0.06), rough=0.9, coat=0)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.05)); o = bpy.context.object; o.scale = (N * U + 0.8, 0.8, 0.1); o.data.materials.append(board); b3d.bevel(o, 0.03)
    H = 0.32
    for i in range(N + 1):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=H, location=(X(i), 0, H / 2), vertices=16); bpy.context.object.data.materials.append(post)
        text(str(i), (X(i), -0.33, 0.13), 0.2, wht)
    for i, s in enumerate(seg):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.028 if s == 1 else 0.065, depth=U - 0.02, location=(X(i) + U / 2, 0, H), vertices=20)
        o = bpy.context.object; o.rotation_euler = (0, math.pi / 2, 0); o.data.materials.append(burnt if after else rope)
    if not after:
        flame(X(0) - 0.05, H + 0.05, mf, mc)
        if b['delay'] == 0: flame(X(N) + 0.05, H + 0.05, mf, mc)
        else:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.27, depth=0.03, location=(X(N) + 0.05, 0.05, H + 0.36), rotation=(math.radians(90 - EL), 0, 0), vertices=32); bpy.context.object.data.materials.append(tagm)
            text(f"{b['delay']}초 뒤", (X(N) + 0.05, 0.02, H + 0.36), 0.17, ink)
    else:
        flame(X(m) - 0.08, H + 0.05, mf, mc); flame(X(m) + 0.08, H + 0.05, mf, mc)
        bpy.ops.mesh.primitive_torus_add(location=(X(m), 0, H + 0.12), major_radius=0.25, minor_radius=0.03, major_segments=48, rotation=(math.radians(90 - EL), 0, 0))
        bpy.context.object.data.materials.append(mint)
    b3d.stack_camera((0, 0.0, 0.3), N * U + 1.1, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1200, 330), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
