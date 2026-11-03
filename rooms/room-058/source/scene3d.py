"""ROOM 058 3D sprites: seven glasses joined by pipes, tap over glass 1. 'start' = empty glasses, stream from the tap.
'end' = water when the 4th glass is full (verify.simulate(stop=4)) with amber '1번째'..'4번째' under the full glasses."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import PIPES, simulate
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
POS = {1: (0, 5.2), 2: (-2.4, 2.6), 3: (2.4, 2.6), 4: (-3.6, 0), 5: (-1.2, 0), 6: (1.2, 0), 7: (3.6, 0)}
GH, GR, PR = 1.5, 0.5, 0.075


def label(s, x, z, size, m, y=-0.7):
    bpy.ops.object.text_add(location=(x, y, z), rotation=(math.radians(90), 0, 0))
    t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.03; t.data.materials.append(m)


def cyl(r, d, loc, m, rot=(0, 0, 0), v=40):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, vertices=v, location=loc, rotation=rot)
    o = bpy.context.object; o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = True
    return o


def bar(x0, z0, x1, z1, m, r=PR):
    L = math.hypot(x1 - x0, z1 - z0); ang = math.atan2(x1 - x0, z1 - z0)
    cyl(r, L, ((x0 + x1) / 2, 0, (z0 + z1) / 2), m, (0, ang, 0), 20)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(x1, 0, z1)); bpy.context.object.data.materials.append(m)


def glass_mats():
    g = b3d.mat('glass', (0.80, 0.90, 1.0), rough=0.05, coat=0.0); g.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.22
    w = b3d.mat('water', (0.10, 0.48, 0.95), rough=0.1, coat=0.3); q = w.node_tree.nodes['Principled BSDF']
    q.inputs['Alpha'].default_value = 0.85; q.inputs['Emission Color'].default_value = (0.10, 0.45, 0.95, 1); q.inputs['Emission Strength'].default_value = 0.35
    return g, w


def scene(end):
    b3d.reset((1000, 1000), 48); b3d.lights(8)
    b3d.stack_camera((0, 0, 3.1), 9.9, az=0.0, el=8.0)
    glass, water = glass_mats()
    rim = b3d.mat('rim', (0.85, 0.92, 1.0), rough=0.2, coat=0.3)
    pipe = b3d.mat('pipe', (0.62, 0.68, 0.78), rough=0.3, metal=0.6)
    red = b3d.mat('red', (0.92, 0.14, 0.12), rough=0.35)
    white = b3d.mat('white', (0.95, 0.96, 0.98), rough=0.4, coat=0.0)
    amber = b3d.mat('amber', (0.98, 0.62, 0.08), rough=0.3); qa = amber.node_tree.nodes['Principled BSDF']
    qa.inputs['Emission Color'].default_value = (0.98, 0.62, 0.08, 1); qa.inputs['Emission Strength'].default_value = 0.8
    full, level = simulate(stop=4) if end else ([], {g: 0.0 for g in POS})
    for g, (x, z) in POS.items():
        cyl(GR, GH, (x, 0, z + GH / 2), glass)
        bpy.ops.mesh.primitive_torus_add(major_radius=GR, minor_radius=0.035, location=(x, 0, z + GH)); bpy.context.object.data.materials.append(rim)
        cyl(GR, 0.06, (x, 0, z + 0.03), rim)
        if level[g] > 0: cyl(GR - 0.05, level[g] * GH - 0.06, (x, 0, z + 0.06 + (level[g] * GH - 0.06) / 2), water)
        label(str(g), x, z - 0.38, 0.55, white)
        if g in full: label(f'{full.index(g) + 1}번째', x, z + GH + 0.42 if g in (4, 5, 6, 7) and False else z - 0.95, 0.42, amber)
    for g, outs in PIPES.items():
        px, pz = POS[g]
        for h, c, blocked in outs:
            cx, cz = POS[c]; side = -1 if cx < px else 1
            x0, zz = px + side * GR, pz + h * GH
            bar(x0, zz, cx, zz, pipe); bar(cx, zz, cx, cz + GH + 0.2, pipe)
            if blocked:
                mx = (x0 + cx) / 2
                for a in (45, -45):
                    bpy.ops.mesh.primitive_cube_add(size=1, location=(mx, -0.12, zz), rotation=(0, math.radians(a), 0))
                    o = bpy.context.object; o.scale = (0.1, 0.1, 0.7); o.data.materials.append(red)
    # tap over glass 1
    tx, tz = POS[1][0], POS[1][1] + GH + 0.9
    bpy.ops.mesh.primitive_cube_add(size=1, location=(tx - 0.45, 0, tz + 0.12)); o = bpy.context.object; o.scale = (1.0, 0.24, 0.24); o.data.materials.append(pipe)
    cyl(0.16, 0.3, (tx, 0, tz - 0.05), pipe)
    cyl(0.06, tz - 0.2 - (POS[1][1] + (level[1] * GH if end else 0.06)), (tx, 0, (tz - 0.2 + POS[1][1] + (level[1] * GH if end else 0.06)) / 2), water, v=16)
    b3d.floor().location.z = -1.7


for name, end in (('start', False), ('end', True)):
    if sys.argv[1:] and name not in sys.argv[1:]: continue
    t = time.time(); scene(end); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
