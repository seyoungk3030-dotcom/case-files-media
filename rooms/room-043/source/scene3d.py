"""ROOM 043 3D sprites: for each setup A-D a fixed gold coin and a small silver coin with an arrow, ready to roll
around it along a dotted path ('cA'..'cD'); answer variants ('aA'..'aD') add ghost copies of the small coin at
eight points (only for A) of the lap with the arrow turned the way it really is there. Same camera scale for all."""
import json, math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import SIZES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
S, TH = 0.42, 0.16


def coin(x, y, rad, m, rim):
    bpy.ops.mesh.primitive_cylinder_add(radius=rad, depth=TH, vertices=96, location=(x, y, TH / 2))
    o = bpy.context.object; o.data.materials.append(m); b3d.bevel(o, 0.03, 3)
    bpy.ops.mesh.primitive_torus_add(major_radius=rad * 0.86, minor_radius=0.025, location=(x, y, TH), major_segments=96)
    bpy.context.object.data.materials.append(rim)


def arrow(x, y, ang, m, z=TH + 0.01):
    ux, uy = math.cos(ang), math.sin(ang)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x - ux * 0.08, y - uy * 0.08, z + 0.02))
    b = bpy.context.object; b.scale = (0.38, 0.09, 0.04); b.rotation_euler = (0, 0, ang); b.data.materials.append(m)
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.17, radius2=0.17, depth=0.04, location=(x + ux * 0.17, y + uy * 0.17, z + 0.02))
    c = bpy.context.object; c.rotation_euler = (0, 0, ang - math.pi / 2); c.data.materials.append(m)


def scene(k, answer):
    R = SIZES[k] * S; P = R + S
    res = (800, 800); b3d.reset(res, 40); b3d.lights(5)
    for o in bpy.data.objects:
        if o.type == 'LIGHT': o.location.z += 3
    b3d.stack_camera((0, 0, 0), 6.0, 0.0, 62.0)
    gold = b3d.mat('gold', (0.95, 0.68, 0.20), rough=0.3, metal=0.9, coat=0.3)
    silver = b3d.mat('silver', (0.86, 0.89, 0.93), rough=0.3, metal=0.35, coat=0.4)
    rim = b3d.mat('rim', (0.40, 0.30, 0.10), rough=0.4, metal=0.8)
    red = b3d.mat('red', b3d.PAL['coral'], rough=0.3, coat=0.5)
    dot = b3d.mat('dot', (0.55, 0.62, 0.75), rough=0.5)
    ghost = b3d.mat('ghost', (0.86, 0.89, 0.93), rough=0.3, coat=0.0)
    ghost.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.35
    coin(0, 0, R, gold, rim)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.12, location=(0, 0, TH + 0.06)); bpy.context.object.data.materials.append(rim)
    for i in range(48):   # dotted path of the small coin's centre
        a = 2 * math.pi * i / 48
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=(P * math.cos(a), P * math.sin(a), 0.02)); bpy.context.object.data.materials.append(dot)
    start = math.pi / 2                                    # small coin starts at 12 o'clock, arrow pointing up (outward)
    coin(0, P, S, silver, rim); arrow(0, P, math.pi / 2, red, TH)
    if answer:
        for j in range(1, 8):
            phi = 2 * math.pi * j / 8; c = start + phi       # anticlockwise lap
            x, y = P * math.cos(c), P * math.sin(c)
            spin = phi * (R + S) / S
            bpy.ops.mesh.primitive_cylinder_add(radius=S, depth=TH * 0.6, vertices=64, location=(x, y, TH * 0.3))
            bpy.context.object.data.materials.append(ghost)
            arrow(x, y, math.pi / 2 + spin, red, TH * 0.6)
    else:   # travel direction: curved arrow beside the start
        for i in range(10):
            a = start + 0.18 + i * 0.05
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=((P + S + 0.25) * math.cos(a), (P + S + 0.25) * math.sin(a), 0.05))
            bpy.context.object.data.materials.append(b3d.mat('trav', (0.95, 0.62, 0.10)))
        a = start + 0.18 + 10 * 0.05
        bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.16, radius2=0.16, depth=0.05,
                                        location=((P + S + 0.25) * math.cos(a), (P + S + 0.25) * math.sin(a), 0.05))
        c = bpy.context.object; c.rotation_euler = (0, 0, a + math.pi / 2 - math.pi / 2 + math.pi / 2); c.data.materials.append(b3d.mat('trav2', (0.95, 0.62, 0.10)))
    b3d.floor()


for k in 'ABCD':
    for answer in ((False, True) if k == 'A' else (False,)):
        name = ('a' if answer else 'c') + k
        t = time.time(); scene(k, answer); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
