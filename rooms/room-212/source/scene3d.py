"""ROOM 212 3D sprites: a bus side window seen from inside (the bus drives to the right), with a 6 x 4 square grid on the
glass and rain outside. Every rain line has the board's slant (a squares back for b squares down). One guide line runs
grid point to grid point so the slant can be counted. p*: guide line white. a*: guide line mint with its across/down
steps marked. Same camera for every board."""
import math, os, random, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
GW, GH = 6, 4


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def box(m, loc, sc, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def seg(m, p, q, r):
    from mathutils import Vector
    d = Vector(q) - Vector(p); bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=r, depth=d.length, location=(Vector(p) + Vector(q)) / 2)
    o = bpy.context.object; o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d)
    o.data.materials.append(m); return o


def scene(key, after):
    u, a, b = BOARDS[key]; k = 2 if (a == 1 and b <= 2) else 1; A, Bd = a * k, b * k
    body = b3d.mat('body', (0.32, 0.36, 0.44), rough=0.7, coat=0); frame = b3d.mat('frame', (0.12, 0.12, 0.14), rough=0.5, coat=0)
    sky = glowm('sky', (0.12, 0.15, 0.24), 0.5, 0.9); bld = glowm('bld', (0.09, 0.11, 0.17), 0.4, 0.9)
    grid = glowm('grid', (0.95, 0.85, 0.5), 0.25, 0.5); rain = glowm('rain', (0.6, 0.85, 1.0), 1.4, 0.3)
    guide = glowm('guide', (0.2, 0.95, 0.65), 2.5) if after else glowm('guide', (1.0, 1.0, 1.0), 1.6)
    # bus wall with the window hole: four slabs around a GW x GH opening centred at the origin
    box(body, (0, 0.2, GH / 2 + 0.9), (GW + 2.4, 0.2, 1.6)); box(body, (0, 0.2, -GH / 2 - 0.9), (GW + 2.4, 0.2, 1.6))
    box(body, (-GW / 2 - 0.6, 0.2, 0), (1.2, 0.2, GH + 0.2)); box(body, (GW / 2 + 0.6, 0.2, 0), (1.2, 0.2, GH + 0.2))
    for z in (GH / 2, -GH / 2): box(frame, (0, 0.05, z), (GW + 0.3, 0.12, 0.16), 0.04)
    for x in (GW / 2, -GW / 2): box(frame, (x, 0.05, 0), (0.16, 0.12, GH + 0.3), 0.04)
    box(sky, (0, 3.0, 0), (GW + 6, 0.1, GH + 6))
    rnd = random.Random(5)
    x = -GW / 2 - 1
    while x < GW / 2 + 1:
        w = rnd.uniform(0.6, 1.4); h = rnd.uniform(0.8, 3.0); box(bld, (x + w / 2, 2.9, -GH / 2 + h / 2), (w, 0.1, h)); x += w + 0.1
    for i in range(1, GW): box(grid, (-GW / 2 + i, 0.0, 0), (0.016, 0.02, GH))
    for j in range(1, GH): box(grid, (0, 0.0, -GH / 2 + j), (GW, 0.02, 0.016))
    L = math.hypot(a, b); dx, dz = -a / L, -b / L; sl = 0.55
    for i in range(46):
        px = rnd.uniform(-GW / 2 + 0.3, GW / 2 + 0.3); pz = rnd.uniform(-GH / 2 + 0.6, GH / 2 - 0.1)
        q = (px + dx * sl, 1.2, pz + dz * sl)
        if abs(q[0]) < GW / 2 - 0.05 and abs(q[2]) < GH / 2 - 0.05: seg(rain, (px, 1.2, pz), q, 0.018)
    x0 = -GW / 2 + A + (GW - A) // 2; z0 = GH / 2 - (GH - Bd) // 2
    seg(guide, (x0, -0.05, z0), (x0 - A, -0.05, z0 - Bd), 0.06)
    for p in ((x0, z0), (x0 - A, z0 - Bd)):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, location=(p[0], -0.05, p[1])); bpy.context.object.data.materials.append(guide)
    if after:
        dash = glowm('dash', (1.0, 0.75, 0.2), 1.6)
        for i in range(A): seg(dash, (x0 - i - 0.06, -0.06, z0), (x0 - i - 0.94, -0.06, z0), 0.035)
        for j in range(Bd): seg(dash, (x0 - A, -0.06, z0 - j - 0.06), (x0 - A, -0.06, z0 - j - 0.94), 0.035)
    b3d.stack_camera((0, 0, 0), GW + 1.6, az=0.0, el=0.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((900, 680), 48); b3d.lights(6)
        t0 = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t0, 1), flush=True)
