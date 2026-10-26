"""ROOM 044 3D sprites: for each setup A-D the folded, punched paper ('fA'..'fD') sitting where it lies on the
original sheet (dotted outline), creases in mint; and the unfolded sheet with every hole ('uA'..'uD'), holes cut on a
crease ringed in amber. Same camera for all, so sizes match. Optional argv: sprite names to render."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import SETUPS, unfold
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
T, HR = 0.035, 0.13      # thickness of one paper layer, hole radius


CUT = None


def cutters(pts):
    """Hidden cylinders; every paper box gets a boolean difference with all of them (real holes)."""
    global CUT
    CUT = bpy.data.collections.new('cut'); bpy.context.scene.collection.children.link(CUT)
    for x, y in pts:
        bpy.ops.mesh.primitive_cylinder_add(radius=HR, depth=2, vertices=64, location=(x, y, 0))
        o = bpy.context.object
        for c in o.users_collection: c.objects.unlink(o)
        CUT.objects.link(o); o.hide_render = True; o.hide_viewport = True


def box(x0, x1, y0, y1, z0, z1, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    o = bpy.context.object; o.scale = (x1 - x0, y1 - y0, z1 - z0); o.data.materials.append(m)
    if CUT and m.name.startswith(('paper', 'edge')):
        md = o.modifiers.new('cut', 'BOOLEAN'); md.operation = 'DIFFERENCE'; md.operand_type = 'COLLECTION'; md.collection = CUT
    return o


def disk(x, y, z, m, r=HR):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=0.006, vertices=64, location=(x, y, z)); bpy.context.object.data.materials.append(m)


def crease(axis, a0, a1, z, m, holes, rad=0.035):
    """Rounded fold edge along x=0 (axis 'x', running in y from a0 to a1) or y=0, skipping hole gaps."""
    cuts = sorted((h[1] if axis == 'x' else h[0]) for h in holes if abs(h[0 if axis == 'x' else 1]) < 1e-9)
    segs, s = [], a0
    for c in cuts: segs.append((s, c - HR)); s = c + HR
    segs.append((s, a1))
    for s0, s1 in segs:
        if s1 - s0 < 0.02: continue
        mid, L = (s0 + s1) / 2, s1 - s0
        loc = (0, mid, z) if axis == 'x' else (mid, 0, z)
        bpy.ops.mesh.primitive_cylinder_add(radius=rad, depth=L, vertices=24, location=loc,
                                            rotation=(math.pi / 2, 0, 0) if axis == 'x' else (0, math.pi / 2, 0))
        bpy.context.object.data.materials.append(m)


def scene(k, unfolded):
    creases, holes = SETUPS[k]
    b3d.reset((800, 800), 40); b3d.lights(5)
    b3d.stack_camera((0, 0, 0.05), 3.0, 0.0, 55.0)
    global CUT; CUT = None
    cutters(unfold(creases, holes) if unfolded else holes)
    paper = b3d.mat('paper', (0.95, 0.93, 0.88), rough=0.65, coat=0.0)
    edge = b3d.mat('edge', (0.80, 0.78, 0.72), rough=0.7, coat=0.0)
    hole = b3d.mat('hole', (0.03, 0.05, 0.10), rough=0.9, coat=0.0)
    mint = b3d.mat('mint', b3d.PAL['mint'], rough=0.35, coat=0.4)
    amber = b3d.mat('amber', (0.95, 0.62, 0.10), rough=0.3, coat=0.4)
    dot = b3d.mat('dot', (0.55, 0.62, 0.75), rough=0.5)
    if unfolded:
        box(-1, 1, -1, 1, 0, T, paper)
        for c in creases:    # faint crease lines
            if c == 'x': box(-0.006, 0.006, -1, 1, T, T + 0.002, edge)
            else: box(-1, 1, -0.006, 0.006, T, T + 0.002, edge)
        for x, y in unfold(creases, holes):
            if (('x' in creases and abs(x) < 1e-9) or ('y' in creases and abs(y) < 1e-9)):
                bpy.ops.mesh.primitive_torus_add(major_radius=HR + 0.05, minor_radius=0.022, location=(x, y, T + 0.01))
                bpy.context.object.data.materials.append(amber)
    else:
        n = 2 ** len(creases); h = n * T
        x1, y1 = 0.0, (0.0 if 'y' in creases else 1.0)
        for i in range(n):   # layers, visible as stripes on the open edges
            box(-1, x1, -1, y1, i * T, (i + 1) * T - 0.004, paper if i == n - 1 else edge if i % 2 else paper)
        for c in creases:
            crease(c, -0.995, y1 if c == 'x' else x1, h / 2, mint, holes, rad=h / 2 + 0.01)
        steps = 40   # dotted outline of the unfolded sheet
        for i in range(4 * steps):
            t = (i % steps) / steps * 2 - 1; side = i // steps
            x, y = [(t, -1), (1, t), (-t, 1), (-1, -t)][side]
            if x < x1 - 0.02 and y < y1 - 0.02 and side in (0, 3): continue
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.014, location=(x, y, 0.01)); bpy.context.object.data.materials.append(dot)
    b3d.floor()


names = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [p + k for k in 'ABCD' for p in 'fu']
for name in names:
    t = time.time(); scene(name[1], name[0] == 'u'); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
