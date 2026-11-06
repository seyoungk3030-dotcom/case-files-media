"""ROOM 146 3D sprites: a battery, bulbs and knife switches wired as a ladder on a dark board, seen from above at a
slant. Closed switch = blade down on both posts; open switch = blade raised. p*: all bulbs dark. a*: lit bulbs glow
warm yellow with a mint ring."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, LIT
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
EL = 58.0; XS = [-2.0, -0.6, 0.8, 2.2]; YT, YB = 1.1, -1.1; Z = 0.08


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - EL), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def wire(p, q, m):
    (x1, y1), (x2, y2) = p, q; L = math.hypot(x2 - x1, y2 - y1)
    if L < 1e-6: return
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=L, location=((x1 + x2) / 2, (y1 + y2) / 2, Z), vertices=16,
                                        rotation=(0, math.radians(90), math.atan2(y2 - y1, x2 - x1))); bpy.context.object.data.materials.append(m)


def post(x, y, m):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.12, location=(x, y, 0.06), vertices=24); bpy.context.object.data.materials.append(m)


def piece(e, p, q, M, lit):
    """element between points p and q (piece occupies the middle 0.5 of the span)."""
    (x1, y1), (x2, y2) = p, q; mx, my = (x1 + x2) / 2, (y1 + y2) / 2; ux, uy = (x2 - x1), (y2 - y1); L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
    h = 0.24
    a, b = (mx - ux * h, my - uy * h), (mx + ux * h, my + uy * h)
    if e == 'W': wire(p, q, M['cu']); return
    wire(p, a, M['cu']); wire(b, q, M['cu'])
    if e == 'L':
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.14, location=(mx, my, 0.07), vertices=32); bpy.context.object.data.materials.append(M['base'])
        wire(a, (mx, my), M['cu']); wire((mx, my), b, M['cu'])
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=(mx, my, 0.3), segments=32, ring_count=16); bpy.context.object.data.materials.append(M['on'] if lit else M['glass'])
        if lit:
            bpy.ops.mesh.primitive_torus_add(location=(mx, my, 0.02), major_radius=0.3, minor_radius=0.03, major_segments=48); bpy.context.object.data.materials.append(M['mint'])
    else:
        post(*a, M['steel']); post(*b, M['steel'])
        bl = 2 * h
        if e == 'S':
            loc = (mx, my, 0.13); rot = (0, math.radians(90), math.atan2(uy, ux))
            bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = (0.06, 0.2, bl + 0.06); o.rotation_euler = rot
        else:
            th = math.atan2(uy, ux) + math.radians(42); dx, dy = math.cos(th), math.sin(th)
            bpy.ops.mesh.primitive_cube_add(size=1, location=(a[0] + dx * bl / 2, a[1] + dy * bl / 2, 0.15)); o = bpy.context.object; o.scale = (0.06, 0.2, bl + 0.06)
            o.rotation_euler = (0, math.radians(90), th)
        o.data.materials.append(M['red'])
        if e == 'O':
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(a[0] + dx * bl, a[1] + dy * bl, 0.2), segments=16, ring_count=8); bpy.context.object.data.materials.append(M['red'])


def scene(k, after):
    b = BOARDS[k]; lit = LIT[k] if after else {}
    M = {'cu': b3d.mat('cu', (0.8, 0.45, 0.22), rough=0.35, metal=0.8, coat=0), 'base': b3d.mat('base', (0.6, 0.6, 0.62), rough=0.4, metal=0.7, coat=0),
         'glass': b3d.mat('glass', (0.16, 0.18, 0.22), rough=0.2, coat=0.3), 'on': b3d.mat('on', (1.0, 0.75, 0.2), rough=0.3, coat=0),
         'steel': b3d.mat('steel', (0.7, 0.72, 0.75), rough=0.3, metal=0.9, coat=0), 'red': b3d.mat('red', (0.85, 0.12, 0.1), rough=0.4, coat=0),
         'mint': b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0)}
    glow(M['on'], (1.0, 0.72, 0.18), 2.5); glow(M['mint'], (0.15, 0.85, 0.6), 1.5)
    board = b3d.mat('board', (0.05, 0.07, 0.1), rough=1.0, coat=0); board.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0
    ink = b3d.mat('ink', (0.97, 0.97, 1.0), rough=0.6, coat=0); glow(ink, (0.97, 0.97, 1.0), 0.6)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.05)); o = bpy.context.object; o.scale = (5.6, 3.2, 0.1); o.data.materials.append(board); b3d.bevel(o, 0.08)
    # battery at column 0: + at top
    x0 = XS[0]
    bpy.ops.mesh.primitive_cylinder_add(radius=0.26, depth=1.0, location=(x0, 0, 0.27), rotation=(math.radians(90), 0, 0), vertices=40); bpy.context.object.data.materials.append(M['base'])
    bpy.ops.mesh.primitive_cylinder_add(radius=0.27, depth=0.45, location=(x0, 0.25, 0.27), rotation=(math.radians(90), 0, 0), vertices=40); bpy.context.object.data.materials.append(M['red'])
    text('+', (x0 + 0.48, 0.55, 0.1), 0.4, ink); text('−', (x0 + 0.48, -0.55, 0.1), 0.4, ink)
    wire((x0, YT), (x0, 0.5), M['cu']); wire((x0, -0.5), (x0, YB), M['cu'])
    for i, e in enumerate(b['top']): piece(e, (XS[i], YT), (XS[i + 1], YT), M, lit.get(('top', i)))
    wire((XS[0], YB), (XS[3], YB), M['cu'])
    for j, r in enumerate(b['rungs'], 1):
        n = len(r); ys = [YT + (YB - YT) * t / n for t in range(n + 1)]
        for t, e in enumerate(r): piece(e, (XS[j], ys[t]), (XS[j], ys[t + 1]), M, lit.get(('rung', j, t)))
    for x in XS:
        for y in (YT, YB):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(x, y, Z), segments=16, ring_count=8); bpy.context.object.data.materials.append(M['cu'])
    b3d.stack_camera((0.1, 0, 0.1), 6.0, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
