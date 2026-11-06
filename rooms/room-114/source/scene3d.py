"""ROOM 114 3D sprites: a white card on a dark wall with 2 x 4 black arrows, a tall clear glass on a table in front
of two neighbouring columns, and a mint ring on the glass marking how high the water will go. a*: the water is in
(clear blue) and the arrows seen through the water are drawn as they appear - flipped left to right - in mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, S
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
CX = [-1.35, -0.45, 0.45, 1.35]; RZ = [2.35, 1.3]; ZT = 0.3


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def box(m, c, s, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = s; o.data.materials.append(m); b3d.bevel(o, bev); return o


def tri(pts, y, m):
    v = [(x, y - 0.03, z) for x, z in pts] + [(x, y + 0.03, z) for x, z in pts]
    me = bpy.data.meshes.new('t'); me.from_pydata(v, [], [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]); me.update()
    o = bpy.data.objects.new('t', me); bpy.context.collection.objects.link(o); o.data.materials.append(m)


def arrow(d, x, z, m, y=0.92):
    if d == 'U':
        box(m, (x, y, z - 0.1), (0.1, 0.06, 0.42), 0.01); tri([(x - 0.2, z + 0.08), (x + 0.2, z + 0.08), (x, z + 0.36)], y, m)
    else:
        sx = 1 if d == 'R' else -1
        box(m, (x - sx * 0.1, y, z), (0.42, 0.06, 0.1), 0.01); tri([(x + sx * 0.08, z - 0.2), (x + sx * 0.08, z + 0.2), (x + sx * 0.36, z)], y, m)


def scene(k, after):
    b = BOARDS[k]; g = b['glass']; wet = {r for r in range(2) if r >= 2 - b['water']}
    wall = b3d.mat('wall', (0.015, 0.02, 0.035), rough=0.8, coat=0); paper = b3d.mat('paper', (0.5, 0.52, 0.5), rough=0.7, coat=0)
    ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0); table = b3d.mat('table', (0.30, 0.20, 0.12), rough=0.6, coat=0.1)
    mint = b3d.mat('mint', (0.1, 0.75, 0.5), rough=0.4, coat=0); glow(mint, (0.12, 0.8, 0.55), 2.0)
    ring = b3d.mat('ring', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(ring, (0.15, 0.85, 0.6), 3.0)
    glass = b3d.mat('glass', (0.8, 0.9, 1.0), rough=0.3, coat=0); gn = glass.node_tree.nodes['Principled BSDF']; gn.inputs['Alpha'].default_value = 0.08
    water = b3d.mat('water', (0.25, 0.55, 0.95), rough=0.3, coat=0); water.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.2
    box(wall, (0, 1.05, 1.9), (5.2, 0.1, 3.6), 0.0)
    box(paper, (0, 0.97, 1.83), (3.9, 0.04, 2.2), 0.03)
    for r in range(2):
        for c in range(4):
            if after and r in wet and g[0] <= c <= g[1]: arrow(S[k][r][c], CX[c], RZ[r] + 2.87 * math.tan(math.radians(6.0)), mint, -1.95)
            else: arrow(b['rows'][r][c], CX[c], RZ[r], ink)
    box(table, (0, -0.6, ZT / 2), (5.0, 2.6, ZT), 0.03)
    gx = (CX[g[0]] + CX[g[1]]) / 2; R = 0.92; Hg = 2.75
    bpy.ops.mesh.primitive_cylinder_add(radius=R, depth=Hg, location=(gx, -0.9, ZT + Hg / 2), vertices=64); o = bpy.context.object
    o.data.materials.append(glass); o.modifiers.new('s', 'SOLIDIFY').thickness = 0.04; o.visible_shadow = False; o.visible_glossy = False
    for p in o.data.polygons: p.use_smooth = True
    zw = (RZ[0] + RZ[1]) / 2 if b['water'] == 1 else ZT + Hg - 0.2
    if after:
        bpy.ops.mesh.primitive_cylinder_add(radius=R - 0.05, depth=zw - ZT - 0.04, location=(gx, -0.9, (zw + ZT + 0.04) / 2), vertices=64)
        o = bpy.context.object; o.data.materials.append(water); o.visible_shadow = False; o.visible_glossy = False
        for p in o.data.polygons: p.use_smooth = True
    bpy.ops.mesh.primitive_torus_add(location=(gx, -0.9, zw), major_radius=R + 0.01, minor_radius=0.025, major_segments=64)
    bpy.context.object.data.materials.append(ring)
    b3d.stack_camera((0, 0, 1.75), 5.6, az=0.0, el=6.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((1000, 860), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
