"""ROOM 123 3D sprites: a white wall with nine numbered strips (amber floor tags), a thin dark post in front of it, and
three lamps (red, green, blue bulbs on short stands) in a row in front of the post. p*: ordinary room light, lamps
off. a*: the room light is off and only the three coloured lamps shine, so the wall shows the real coloured shadows;
the asked strip's tag turns mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, XS, W, X0
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
COL = {'R': (1.0, 0.08, 0.05), 'G': (0.05, 1.0, 0.1), 'B': (0.1, 0.25, 1.0)}
YL, YW, ZL = -1.6, 1.6, 1.0


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m, rot=(math.radians(60), 0, 0)):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def box(m, c, s, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def scene(k, after):
    b = BOARDS[k]; ans = RES[k][0]; sc = bpy.context.scene
    wall = b3d.mat('wall', (0.92, 0.92, 0.92), rough=0.9, coat=0); floor = b3d.mat('floor', (0.08, 0.09, 0.12), rough=0.8, coat=0)
    post = b3d.mat('post', (0.08, 0.08, 0.1), rough=0.5, coat=0); stand = b3d.mat('stand', (0.2, 0.21, 0.25), rough=0.4, metal=0.5, coat=0)
    amber = b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0.1); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.0)
    line = b3d.mat('line', (0.55, 0.57, 0.62), rough=0.8, coat=0)
    box(floor, (0, 0, -0.05), (8.4, 4.6, 0.1), 0.02)
    box(wall, (0, YW + 0.05, 1.5), (9 * W + 0.4, 0.1, 3.0), 0.0)
    for i in range(10): box(line, (X0 + i * W, YW - 0.005, 1.5), (0.015, 0.01, 3.0), 0.0)
    for n in range(1, 10):
        cx = X0 + (n - 0.5) * W
        box(mint if (after and n == ans) else amber, (cx, YW - 0.3, 0.03), (0.5, 0.4, 0.06), 0.05)
        text(str(n), (cx, YW - 0.32, 0.12), 0.3, ink, (math.radians(35), 0, 0))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=2.4, location=(b['xo'], 0, 1.2), vertices=24); bpy.context.object.data.materials.append(post)
    for c, x in zip(b['order'], XS):
        box(stand, (x, YL, (ZL - 0.12) / 2), (0.06, 0.06, ZL - 0.12), 0.01)
        bm = b3d.mat('bulb' + c, COL[c], rough=0.3, coat=0); glow(bm, COL[c], 2.5 if after else 0.6)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.13, location=(x, YL, ZL)); o = bpy.context.object; o.data.materials.append(bm)
        o.visible_shadow = False
        if after:
            bpy.ops.object.light_add(type='POINT', location=(x, YL, ZL)); L = bpy.context.object.data; L.energy = 260; L.color = COL[c]; L.shadow_soft_size = 0.02
    if after:
        sc.world.node_tree.nodes['Background'].inputs[1].default_value = 0.04
    b3d.stack_camera((0, 0.3, 1.0), 7.6, az=0.0, el=28.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 860), 64)
        if not after: b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
