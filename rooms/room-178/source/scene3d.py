"""ROOM 178 3D sprites: a round restaurant table with a lazy susan carrying 8 numbered dishes, seen from your seat
(front, above). Your place mat and spoon sit at the front edge. A glowing arrow on the FAR rim shows which way the
lazy susan turns and how many dish places. p*: before the turn. a*: after the turn, the dish now in front ringed mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
RT, RS, RD = 2.0, 1.45, 1.05  # table, lazy susan, dish ring radius
FOOD = [(0.9, 0.35, 0.2), (0.35, 0.7, 0.3), (0.95, 0.75, 0.2), (0.6, 0.3, 0.15), (0.95, 0.5, 0.55), (0.3, 0.55, 0.85), (0.85, 0.6, 0.35), (0.55, 0.75, 0.6)]


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def cyl(loc, r, d, m, v=64):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, vertices=v); o = bpy.context.object; o.data.materials.append(m); return o


def text(s, loc, size, m, rotz=0.0):
    bpy.ops.object.text_add(location=loc, rotation=(0, 0, rotz)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def pos(p, r):  # p = 0 in front of you, increasing clockwise seen from above
    a = math.radians(-90 - 45 * p); return r * math.cos(a), r * math.sin(a)


def scene(k, after):
    dishes, d, steps = BOARDS[k]
    if after:
        t = list(dishes)
        for _ in range(steps): t = [t[(p - d) % 8] for p in range(8)]
        dishes = ''.join(t)
    cloth = b3d.mat('cloth', (0.5, 0.08, 0.08), rough=0.8, coat=0); wood = b3d.mat('wood', (0.45, 0.25, 0.14), rough=0.4, coat=0.5)
    glass = b3d.mat('glass', (0.8, 0.88, 0.9), rough=0.08, coat=0.6); glass.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.5
    plate = b3d.mat('plate', (0.97, 0.97, 0.96), rough=0.3, coat=0.5); ink = b3d.mat('ink', (0.06, 0.06, 0.08), rough=0.5, coat=0)
    tag = b3d.mat('tag', (1, 1, 1), rough=0.5, coat=0); yel = glowm('yel', (1.0, 0.75, 0.15), 2.2); mint = glowm('mint', (0.15, 0.85, 0.6), 2.2)
    mat_ = b3d.mat('mat', (0.25, 0.35, 0.55), rough=0.7, coat=0); steel = b3d.mat('steel', (0.8, 0.8, 0.82), rough=0.25, metal=0.9)
    cyl((0, 0, -0.06), RT, 0.12, cloth, 96)
    cyl((0, 0, 0.03), RS, 0.06, glass, 96)
    for p in range(8):
        x, y = pos(p, RD); fm = b3d.mat(f'f{p}', FOOD[int(dishes[p]) % 8], rough=0.6, coat=0.1)
        cyl((x, y, 0.09), 0.3, 0.05, plate, 48)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=(x + 0.04, y + 0.08, 0.12)); o = bpy.context.object; o.scale = (1, 1, 0.45); o.data.materials.append(fm)
        cyl((x - 0.02, y - 0.1, 0.16), 0.17, 0.03, tag, 32)
        text(dishes[p], (x - 0.02, y - 0.1, 0.18), 0.27, ink)
        if after and p == 0:
            bpy.ops.mesh.primitive_torus_add(location=(x, y, 0.1), major_radius=0.36, minor_radius=0.03); bpy.context.object.data.materials.append(mint)
    # your place at the front edge of the table
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -RT + 0.25, 0.005)); o = bpy.context.object; o.scale = (0.9, 0.42, 0.01); o.data.materials.append(mat_)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.28, -RT + 0.25, 0.02)); o = bpy.context.object; o.scale = (0.05, 0.36, 0.015); o.data.materials.append(steel)
    cyl((-0.15, -RT + 0.25, 0.03), 0.12, 0.04, plate, 32)
    # turning arrow on the far rim: clockwise seen from above moves the far side to the right
    a0, a1 = (120, 60) if d == 1 else (60, 120); n = 14
    for i in range(n):
        a = math.radians(a0 + (a1 - a0) * (i + 0.5) / (n + 2)); x, y = RS * 1.12 * math.cos(a), RS * 1.12 * math.sin(a)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.08), rotation=(0, 0, a)); o = bpy.context.object; o.scale = (0.08, 0.1, 0.03); o.data.materials.append(yel)
    ah = math.radians(a1); x, y = RS * 1.12 * math.cos(ah), RS * 1.12 * math.sin(ah)
    tang = ah - math.pi / 2 * d  # direction of travel at the head
    bpy.ops.mesh.primitive_cone_add(radius1=0.15, depth=0.3, location=(x, y, 0.08), rotation=(0, math.pi / 2, tang)); bpy.context.object.data.materials.append(yel)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, RT + 0.32, 0.05)); o = bpy.context.object; o.scale = (1.0, 0.5, 0.06); o.data.materials.append(b3d.mat('sign', (0.04, 0.045, 0.06), rough=0.4, coat=0.3))
    text(f'{steps}칸', (0, RT + 0.32, 0.09), 0.36, glowm('yt', (1.0, 0.8, 0.2), 0.9))
    b3d.stack_camera((0, 0.05, 0), 4.6, az=0.0, el=52.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
