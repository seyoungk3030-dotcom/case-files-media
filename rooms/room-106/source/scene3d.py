"""ROOM 106 3D sprites: side view of a clear water bottle standing on a block, four plugged holes on its right side
with numbered amber tags, a long dark floor running to the right with distance ticks. a*: the plugs are out and four
blue water jets arc to the floor (Torricelli parabolas); the farthest one is mint."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
RB, HB = 0.5, 3.0


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)


def box(m, c, s, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def jet(S, H, h, m, r=0.06):
    v = math.sqrt(2 * 9.8 * (H - h)); y0 = S + h; T = math.sqrt(2 * y0 / 9.8)
    pts = [Vector((RB + v * t, 0, y0 - 4.9 * t * t)) for t in [T * i / 40 for i in range(41)]]
    cu = bpy.data.curves.new('j', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = r
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for i, q in enumerate(pts): sp.points[i].co = (*q, 1)
    o = bpy.data.objects.new('j', cu); bpy.context.collection.objects.link(o); o.data.materials.append(m)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.03, location=(pts[-1].x, 0, 0.015), vertices=32); bpy.context.object.data.materials.append(m)


def scene(k, after):
    S, H, holes = BOARDS[k]; win = RES[k][0]
    floor = b3d.mat('floor', (0.07, 0.09, 0.15), rough=0.7, coat=0); block = b3d.mat('block', (0.10, 0.12, 0.18), rough=0.6, coat=0)
    glass = b3d.mat('glass', (0.85, 0.95, 1.0), rough=0.05, coat=0.4)
    gq = glass.node_tree.nodes['Principled BSDF']; gq.inputs['Transmission Weight'].default_value = 1.0
    water = b3d.mat('water', (0.05, 0.25, 0.70), rough=0.15, coat=0.3); blue = b3d.mat('blue', (0.08, 0.28, 0.80), rough=0.2, coat=0.3)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.0)
    amber = b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0.1); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    tick = b3d.mat('tick', (0.45, 0.5, 0.6), rough=0.6, coat=0); cap = b3d.mat('cap', (0.85, 0.25, 0.2), rough=0.4, coat=0.2)
    box(floor, (2.9, 0, -0.06), (8.2, 1.6, 0.12))
    for x in range(1, 7): box(tick, (RB + x, -0.5, 0.005), (0.05, 0.5, 0.012), 0.005)
    if S > 0: box(block, (0, 0, S / 2), (1.5, 1.4, S))
    bpy.ops.mesh.primitive_cylinder_add(radius=RB, depth=HB, location=(0, 0, S + HB / 2), vertices=64); o = bpy.context.object
    o.modifiers.new('s', 'SOLIDIFY').thickness = 0.03; o.data.materials.append(glass)
    for p in o.data.polygons: p.use_smooth = True
    bpy.ops.mesh.primitive_cylinder_add(radius=RB * 0.55, depth=0.25, location=(0, 0, S + HB + 0.12), vertices=48); bpy.context.object.data.materials.append(cap)
    bpy.ops.mesh.primitive_cylinder_add(radius=RB - 0.035, depth=H, location=(0, 0, S + H / 2 + 0.01), vertices=64); o = bpy.context.object; o.data.materials.append(water)
    for p in o.data.polygons: p.use_smooth = True
    for n, h in holes.items():
        z = S + h
        if not after:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.2, location=(RB + 0.05, 0, z), rotation=(0, math.radians(90), 0), vertices=24)
            bpy.context.object.data.materials.append(amber)
        tx = -RB - 0.38 - (0.62 if sorted(holes.values()).index(h) % 2 else 0)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.05, location=(tx, -0.2, z), rotation=(math.radians(90), 0, 0), vertices=40)
        bpy.context.object.data.materials.append(amber); text(str(n), (tx, -0.24, z), 0.44, ink)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=abs(tx) - RB, location=((tx - RB) / 2, -0.15, z), rotation=(0, math.radians(90), 0), vertices=8)
        bpy.context.object.data.materials.append(amber)
        if after: jet(S, H, h, mint if n == win else blue, 0.09 if n == win else 0.05)
    b3d.stack_camera((2.4, 0, 2.9), 8.6, az=0.0, el=6.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 860), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
