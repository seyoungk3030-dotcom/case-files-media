"""ROOM 211 3D sprites, metres: a garden hose held level 1 m above the lawn, nozzle at x = 0, a 4 m lawn ruler (big tick
every 1 m). The hose is drawn thicker than life so the end shows; a thumb covers part of the end on B-D. p*: the hose
before the tap opens. a*: the jet, a parabola from 1 m height at the proven speed, landing where v*sqrt(2h/g) says, with a
mint splash ring. Same camera for every board."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD, H
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
G = 9.81


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def box(m, loc, sc, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def rod(m, p, q, r, v=24):
    from mathutils import Vector
    d = Vector(q) - Vector(p); bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d.length, location=(Vector(p) + Vector(q)) / 2)
    o = bpy.context.object; o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d)
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def ball(m, loc, r):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=16, ring_count=8); o = bpy.context.object
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def scene(key, after):
    lb, q, a, thumb = BOARDS[key]; v = GOOD[key]
    grass = b3d.mat('grass', (0.3, 0.6, 0.3), rough=0.9, coat=0); hose = b3d.mat('hose', (0.15, 0.7, 0.35), rough=0.4, coat=0.3)
    skin = glowm('skin', (0.95, 0.72, 0.58), 0.25, 0.6); white = glowm('white', (1, 1, 1), 0.6, 0.5)
    water = glowm('water', (0.35, 0.7, 1.0), 1.0, 0.1); mint = glowm('mint', (0.2, 0.95, 0.65), 2.0)
    box(grass, (1.4, 0, -0.03), (6.4, 1.6, 0.06), 0.02)
    for i in range(0, 9):
        x = i * 0.5; box(white, (x, -0.55, 0.005), (0.025, 0.3 if i % 2 == 0 else 0.15, 0.01))
    R = 0.07
    pts = [(-1.8, 0, 0.02), (-1.2, 0, 0.05), (-0.75, 0, 0.45), (-0.45, 0, 0.9), (-0.2, 0, 1.0), (0.0, 0, 1.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(hose, p0, p1, R)
        if p1[0] < 0: ball(hose, p1, R)
    rod(b3d.mat('rim', (0.1, 0.4, 0.2), rough=0.4, coat=0), (-0.01, 0, 1.0), (0.01, 0, 1.0), R * 1.02)
    box(skin, (-0.3, 0, 1.0), (0.2, 0.2, 0.2), 0.08)                   # hand
    rod(b3d.mat('hole', (0.02, 0.03, 0.05), rough=0.9, coat=0), (0.0, 0, 1.0), (0.012, 0, 1.0), R * 0.82, 48)
    if thumb:   # thumb pad slides down from the top and leaves the proven open area below it
        frac = float(a) / 2                       # open fraction of the full 2 cm^2 end
        rr = R * 0.82; lo, hi = 0.0, 2 * rr          # open segment height h with segment area = frac * pi r^2
        for _ in range(60):
            h = (lo + hi) / 2; seg = rr * rr * math.acos((rr - h) / rr) - (rr - h) * math.sqrt(2 * rr * h - h * h)
            lo, hi = (h, hi) if seg < frac * math.pi * rr * rr else (lo, h)
        hcov = 2 * rr - h
        box(skin, (0.03, 0, 1.0 + rr - hcov / 2 + 0.01), (0.03, 2 * R * 1.05, hcov + 0.02), 0.006)
        rod(skin, (-0.14, 0, 1.08), (0.03, 0, 1.0 + R), 0.04)
    if after:
        T = math.sqrt(2 * H / G); n = 26
        for i in range(1, n + 1):
            t = T * i / n; ball(water, (v * t, 0, H - G * t * t / 2), 0.022 + 0.006 * (i % 3))
        xr = v * T; bpy.ops.mesh.primitive_torus_add(major_radius=0.1, minor_radius=0.018, location=(xr, 0, 0.02)); bpy.context.object.data.materials.append(mint)
        box(mint, (xr, -0.55, 0.012), (0.035, 0.45, 0.015))
    b3d.stack_camera((1.45, 0, 0.55), 6.0, az=0.0, el=14.0)


only = sys.argv[1:]
for key in 'ABCD':
    for kind in 'pae':
        nm = kind + key
        if only and nm not in only: continue
        b3d.reset((900, 420) if kind != 'e' else (360, 360), 48); b3d.lights(6)
        t0 = time.time(); scene(key, kind == 'a')
        if kind == 'e': b3d.stack_camera((0.0, 0, 1.0), 0.32, az=90.0, el=4.0)     # close-up of the hose end
        b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t0, 1), flush=True)
