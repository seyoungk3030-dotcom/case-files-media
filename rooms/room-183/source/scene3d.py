"""ROOM 183 3D sprites: a hallway wall with closed doors seen from your side, slightly from the left so the hinge
barrels stand out. Doors with gold hinge knuckles on your side swing toward you (pull). Handles are either a pull bar
or a flat push plate, which may not match. p*: question. a*: answer, the doors you must pull get a mint frame."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
DOORC = [(0.1, 0.3, 0.65), (0.65, 0.18, 0.12), (0.15, 0.45, 0.25), (0.75, 0.5, 0.08), (0.4, 0.2, 0.5)]
DW, DH, SP = 0.9, 2.0, 1.25


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def box(loc, sc, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = sc; o.data.materials.append(m)
    bpy.ops.object.modifier_add(type='BEVEL'); o.modifiers['Bevel'].width = min(0.015, min(sc) / 3); o.modifiers['Bevel'].segments = 2; return o


def cyl(loc, r, d, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, rotation=rot, vertices=32); o = bpy.context.object; o.data.materials.append(m)
    bpy.ops.object.shade_smooth(); return o


def scene(k, after):
    doors = BOARDS[k]; n = len(doors)
    wall = b3d.mat('wall', (0.5, 0.52, 0.55), rough=0.8, coat=0); trim = b3d.mat('trim', (0.25, 0.22, 0.2), rough=0.5, coat=0.2)
    gold = b3d.mat('gold', (0.95, 0.72, 0.3), rough=0.25, metal=1.0, coat=0); steel = b3d.mat('steel', (0.8, 0.8, 0.82), rough=0.25, metal=0.9, coat=0)
    floor = b3d.mat('floor', (0.5, 0.4, 0.3), rough=0.6, coat=0.2); mint = glowm('mint', (0.05, 0.8, 0.5), 0.8)
    W = n * SP + 0.5
    box((0, 0.1, DH / 2 + 0.08), (W, 0.2, DH + 0.36), wall)
    box((0, -0.6, -0.03), (W, 1.4, 0.06), floor)
    for i, (pull, handle, hs) in enumerate(doors):
        cx = (i - (n - 1) / 2) * SP; s = -1 if hs == 'L' else 1  # hinge edge x sign
        box((cx, -0.01, DH / 2 + 0.04), (DW + 0.16, 0.06, DH + 0.1), mint if after and pull else trim)       # frame
        box((cx, -0.05, DH / 2), (DW, 0.06, DH), b3d.mat(f'd{i}', DOORC[i % 5], rough=0.45, coat=0.2))   # door leaf
        hx = cx + s * DW / 2
        if pull:  # hinge knuckles stand out on this side
            for z in (0.25, DH / 2, DH - 0.25):
                cyl((hx, -0.13, z), 0.075, 0.3, gold)
                box((hx - s * 0.08, -0.085, z), (0.16, 0.012, 0.26), gold)
        ox = cx - s * (DW / 2 - 0.14)
        if handle == 'bar':
            cyl((ox, -0.2, 1.0), 0.028, 0.6, steel)
            for z in (0.76, 1.24): cyl((ox, -0.14, z), 0.02, 0.14, steel, rot=(math.pi / 2, 0, 0))
        else:
            box((ox, -0.085, 1.05), (0.12, 0.012, 0.36), steel)
    b3d.stack_camera((0, 0, DH / 2), W * 0.98, az=-14.0, el=6.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((1000, 560), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
