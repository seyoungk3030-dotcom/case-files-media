"""ROOM 200 3D sprites, seen from above at an angle: a river flowing to the right (white chevrons), grassy banks, a straw
hat floating, and the rowing boat at the moment it turns round (amber arrow = the way it now rows). Positions are the real
ones at that moment, scaled per board. a*: a mint path from the boat to where it picks the hat up, with a ghost hat there."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def box(m, loc, sc, bev=0.03, rz=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=(0, 0, rz)); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def cyl(m, r, depth, loc, verts=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, vertices=verts); o = bpy.context.object
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def chevron(m, x, y):
    for sgn in (1, -1): box(m, (x, y + sgn * 0.07, 0.01), (0.22, 0.035, 0.01), 0.005, rz=-sgn * 0.6)


def hat(x, m_straw, m_band, z=0.06):
    cyl(m_straw, 0.34, 0.04, (x, 0, z)); cyl(m_straw, 0.19, 0.16, (x, 0, z + 0.09)); cyl(m_band, 0.195, 0.05, (x, 0, z + 0.05))


def boat(x, facing):
    hull = b3d.mat('hull', (0.75, 0.28, 0.16), rough=0.4, coat=0.5); inner = b3d.mat('inner', (0.5, 0.34, 0.2), rough=0.6, coat=0)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(x, 0, 0.08)); o = bpy.context.object; o.scale = (0.62, 0.26, 0.16)
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(hull); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(x, 0, 0.13)); o = bpy.context.object; o.scale = (0.54, 0.2, 0.1)
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(inner); bpy.ops.object.shade_smooth()
    oar = b3d.mat('oar', (0.85, 0.7, 0.45), rough=0.5, coat=0)
    for s in (1, -1): box(oar, (x, s * 0.42, 0.18), (0.06, 0.6, 0.03), 0.01, rz=s * 0.35 * facing)
    box(b3d.mat('seat', (0.35, 0.22, 0.12), rough=0.6, coat=0), (x, 0, 0.2), (0.12, 0.38, 0.04), 0.01)


def scene(key, after):
    d, c, v, t1, v2 = BOARDS[key]; s = -1 if d == 'up' else 1
    hx, bx = c * t1, (s * v + c) * t1; tau = GOOD[key]; mx = hx + c * tau
    lo, hi = min(hx, bx, mx), max(hx, bx, mx); k = 2.9 / (hi - lo); cen = (lo + hi) / 2
    X = lambda p: (p - cen) * k
    water = b3d.mat('water', (0.06, 0.32, 0.55), rough=0.08, coat=0.8); grass = b3d.mat('grass', (0.25, 0.55, 0.22), rough=0.7, coat=0)
    box(water, (0, 0, -0.05), (4.4, 1.9, 0.1), 0.01)
    for y in (-1.25, 1.25): box(grass, (0, y, 0.0), (4.4, 0.6, 0.22), 0.06)
    wm = glowm('wave', (0.85, 0.95, 1.0), 0.5)
    for x in (-1.8, -0.6, 0.6, 1.8):
        for y in (-0.7, 0.7): chevron(wm, x, y)
    hat(X(hx), b3d.mat('straw', (0.95, 0.8, 0.4), rough=0.6, coat=0), b3d.mat('band', (0.85, 0.15, 0.15), rough=0.4, coat=0))
    boat(X(bx), s)
    am = glowm('amber', (1.0, 0.72, 0.2), 1.4); dirx = -s; ax = X(bx) + dirx * 0.75
    box(am, (ax + dirx * 0.2, 0, 0.32), (0.45, 0.06, 0.06), 0.02)
    bpy.ops.mesh.primitive_cone_add(radius1=0.12, radius2=0, depth=0.24, location=(ax + dirx * 0.52, 0, 0.32), rotation=(0, dirx * math.pi / 2, 0))
    bpy.context.object.data.materials.append(am)
    if after:
        mint = glowm('mint', (0.2, 0.95, 0.65), 1.6); a, b = sorted((X(bx), X(mx)))
        n = max(int((b - a) / 0.22), 1)
        for i in range(n + 1):
            box(mint, (a + (b - a) * i / n, -0.42, 0.03), (0.1, 0.06, 0.02), 0.01)
        ghost = glowm('ghost', (0.2, 0.95, 0.65), 0.8); hat(X(mx), ghost, ghost, z=0.04)
    b3d.stack_camera((0, 0, 0.1), 4.8, az=8.0, el=42.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((760, 560), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t, 1), flush=True)
