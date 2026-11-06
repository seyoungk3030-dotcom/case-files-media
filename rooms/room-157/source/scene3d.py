"""ROOM 157 3D sprites: a paper strip of numbered squares lying flat, seen from the front at a slant, with dashed creases
and curved arrows labelled 1, 2, 3 that show which side flips over at each fold. p*: the flat strip. a*: the folded pile
standing where it ends up (faint outline of the strip behind it), its top number in mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U = 0.7; EL = 48.0; NMAX = 8; YA = 0.55


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def flat_text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.004; t.data.materials.append(m)


def up_text(s, loc, size, m):
    flat_text(s, loc, size, m); bpy.context.object.rotation_euler = (math.radians(90 - EL), 0, 0)


def X(p): return (p - NMAX / 2) * U  # left edge of square p+1


def arc(xc, d, h, m):
    """curved arrow from xc + d*U*0.5 over the crease at xc to xc - d*U*0.5 (d=+1: right part flips left)."""
    cu = bpy.data.curves.new('arc', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.03; sp = cu.splines.new('POLY')
    pts = [(xc + d * 0.4 * U * math.cos(t), YA, 0.05 + h * math.sin(t)) for t in [i * math.pi / 24 for i in range(21)]]
    sp.points.add(len(pts) - 1)
    for p, q in zip(sp.points, pts): p.co = (*q, 1)
    o = bpy.data.objects.new('arc', cu); bpy.context.collection.objects.link(o); o.data.materials.append(m)
    t = math.pi * 22 / 24; tip = (xc - d * 0.4 * U, YA, 0.12)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(xc + d * 0.4 * U, YA, 0.05)); bpy.context.object.data.materials.append(m)
    bpy.ops.mesh.primitive_cone_add(radius1=0.11, depth=0.2, location=tip, vertices=20, rotation=(0, math.pi, 0)); bpy.context.object.data.materials.append(m)


def scene(k, after):
    b = BOARDS[k]; n = b['n']; pile, creases, lo = RES[k]
    paper = b3d.mat('paper', (0.8, 0.78, 0.72), rough=0.8, coat=0); paper.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0.1
    ghost = b3d.mat('ghost', (0.5, 0.52, 0.58), rough=0.8, coat=0)
    ink = b3d.mat('ink', (0.12, 0.13, 0.2), rough=0.9, coat=0); dash = b3d.mat('dash', (0.85, 0.3, 0.25), rough=0.9, coat=0)
    yel = b3d.mat('yel', (1.0, 0.65, 0.1), rough=0.4, coat=0); glow(yel, (1.0, 0.6, 0.1), 0.8)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.6)
    for p in range(n):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(X(p) + U / 2, 0, 0.005)); o = bpy.context.object
        o.scale = (U - 0.03, U - 0.03, 0.01); o.data.materials.append(ghost if after else paper)
        if not after: flat_text(str(p + 1), (X(p) + U / 2, 0, 0.012), 0.42, ink)
    if not after:
        for i, (c, side) in enumerate(creases):
            for j in range(5):
                bpy.ops.mesh.primitive_cube_add(size=1, location=(X(c), -U * 0.4 + j * U * 0.2, 0.012)); o = bpy.context.object; o.scale = (0.025, U * 0.11, 0.004); o.data.materials.append(dash)
            h = 0.32 + 0.0 * i; arc(X(c), 1 if side == 'R' else -1, h, yel)
            bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.02, location=(X(c), YA, h + 0.28), rotation=(math.radians(90 - EL), 0, 0), vertices=32); bpy.context.object.data.materials.append(yel)
            up_text(str(i + 1), (X(c), YA - 0.03, h + 0.28), 0.22, ink)
    else:
        x = X(lo) + U / 2
        for j in range(n):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 0.02 + j * 0.05)); o = bpy.context.object; o.scale = (U - 0.05, U - 0.05, 0.03); o.data.materials.append(paper)
        flat_text(str(pile[-1]), (x, 0, 0.02 + (n - 1) * 0.05 + 0.017), 0.42, mint)
        bpy.ops.mesh.primitive_torus_add(location=(x, 0, 0.02 + (n - 1) * 0.05), major_radius=U * 0.62, minor_radius=0.03, major_segments=48); bpy.context.object.data.materials.append(mint)
    b3d.stack_camera((0, 0.25, 0.3), NMAX * U + 0.4, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1200, 330), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
