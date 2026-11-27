"""ROOM 210 3D sprites, true scale in cm: each container is drawn as a cut-away (back half of its wall plus the full rim)
so the inside shows. Basin 40 cm wide, cup 6 cm, a 10 cm funnel on a 5 cm tube, a jar with a 6 cm neck on a 12 cm body.
p*: empty, with rain streaks above. a*: the collected water at the proven depth (mint top line). Each board is framed to
fit (sizes are written under it)."""
import math, os, sys, time
import bpy, bmesh
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
AZ = 20.0


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def shell(m, prof, a0, a1, n=48, thick=0.4):
    """Surface of revolution of profile [(r, z), ...] over angles a0..a1 (radians), solidified."""
    me = bpy.data.meshes.new('shell'); bm = bmesh.new(); rows = []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n; rows.append([bm.verts.new((r * math.cos(a), r * math.sin(a), z)) for r, z in prof])
    for i in range(n):
        for j in range(len(prof) - 1): bm.faces.new((rows[i][j], rows[i + 1][j], rows[i + 1][j + 1], rows[i][j + 1]))
    bm.to_mesh(me); bm.free(); o = bpy.data.objects.new('shell', me); bpy.context.collection.objects.link(o); o.data.materials.append(m)
    md = o.modifiers.new('s', 'SOLIDIFY'); md.thickness = thick
    for p in o.data.polygons: p.use_smooth = True
    return o


def cyl(m, r, z0, z1):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=r, depth=z1 - z0, location=(0, 0, (z0 + z1) / 2)); o = bpy.context.object
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def ring(m, r, z, t):
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=t, location=(0, 0, z), major_segments=64); o = bpy.context.object
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def scene(key, after):
    nm, kind, D0, D1, rain, h = BOARDS[key]; d = GOOD[key]
    wall = b3d.mat('wall', (0.55, 0.62, 0.72), rough=0.45, coat=0.2); dark = b3d.mat('in', (0.55, 0.6, 0.7), rough=0.4, coat=0)
    water = b3d.mat('water', (0.15, 0.45, 0.9), rough=0.1, coat=0.6); mint = glowm('mint', (0.2, 0.95, 0.65), 1.2)
    back = math.radians(AZ) + math.pi / 2     # half facing away from the camera
    a0, a1 = back - math.pi / 2 - 0.25, back + math.pi / 2 + 0.25
    R0, R1 = D0 / 2, D1 / 2; t = max(0.25, R0 * 0.02)
    if kind == 'straight': prof = [(R0, 0), (R0, h)]; top = h
    elif kind == 'funnel': prof = [(R1, 0), (R1, h), (R0, h + 6)]; top = h + 6
    else: prof = [(R1, 0), (R1, h), (R0, h + 3), (R0, h + 7)]; top = h + 7
    shell(wall, prof, a0, a1, thick=t)
    cyl(dark, max(r for r, _ in prof) if kind == 'straight' else R1, -t, 0)
    ring(wall, R0, top, t * 0.9)
    if kind != 'straight': ring(wall, R1, 0.2, t * 0.9)
    if after and d > 0:
        cyl(water, R1 - t * 0.6, 0.0, d); ring(mint, R1 - t * 0.6, d, t * 0.8)
    rainm = glowm('rain', (0.6, 0.8, 1.0), 1.2)
    import random; rnd = random.Random(7); W = max(R0 * 2.4, 10)
    for i in range(int(10 + W * 0.6)):
        x = rnd.uniform(-W / 2, W / 2); y = rnd.uniform(-W / 2, W / 2); z = top + rnd.uniform(1.5, 1.5 + W * 0.28)
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=W * 0.004 + 0.05, depth=W * 0.06 + 0.8, location=(x, y, z)); bpy.context.object.data.materials.append(rainm)
    H = top + 1.5 + W * 0.28
    b3d.stack_camera((0, 0, H / 2 - 1), max(W * 1.1, H * 1.15), az=AZ, el=24.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((760, 760), 48); b3d.lights(6)
        t0 = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t0, 1), flush=True)
