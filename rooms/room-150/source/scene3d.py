"""ROOM 150 3D sprites, seen from the front: on the left the glass standing upright with water at its starting mark; on
the right the same glass tilted (left side down) with numbered marks up its LEFT wall. p*: the tilted glass is empty
(the question). a*: the tilted glass holds the same water with a level, horizontal surface, and the mark where it meets
the left wall glows mint."""
import math, os, sys, time
import bpy, bmesh
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, low, high
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
U = 0.3; EL = 4.0; DEP = 0.7; T = 0.05


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90 - EL), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


class G:
    def __init__(s, x0, z0, t): s.x0, s.z0, s.t = x0, z0, t
    def P(s, u, v): c, n = math.cos(s.t), math.sin(s.t); return (s.x0 + (u * c - v * n) * U, s.z0 + (u * n + v * c) * U)
    def box(s, u, v, du, dv, m, y=0.0, dy=DEP):
        x, z = s.P(u, v); bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z)); o = bpy.context.object
        o.scale = (du * U, dy, dv * U); o.rotation_euler = (0, -s.t, 0); o.data.materials.append(m); return o
    def prism(s, pts, m, dy=DEP - 0.08):
        me = bpy.data.meshes.new('w'); bm = bmesh.new()
        front = [bm.verts.new((*(lambda p: (p[0], -dy / 2, p[1]))(s.P(u, v)),)) for u, v in pts]
        back = [bm.verts.new((*(lambda p: (p[0], dy / 2, p[1]))(s.P(u, v)),)) for u, v in pts]
        bm.faces.new(front); bm.faces.new(back[::-1]); n = len(pts)
        for i in range(n): bm.faces.new((front[i], front[(i + 1) % n], back[(i + 1) % n], back[i]))
        bm.normal_update(); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new('w', me); bpy.context.collection.objects.link(o); o.data.materials.append(m); return o


def glass(g, w, M):
    g.box(w / 2, -T / U / 2, w + 2 * T / U, T / U, M['glass'])
    for u in (-T / U / 2, w + T / U / 2): g.box(u, 5, T / U, 10, M['glass'])


def scene(k, after):
    b = BOARDS[k]; w = b['w']; t = math.atan(float(b['s']))
    M = {'glass': b3d.mat('glass', (0.7, 0.8, 0.9), rough=0.2, coat=0)}
    M['glass'].node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.35; M['glass'].blend_method = 'BLEND' if hasattr(M['glass'], 'blend_method') else None
    water = b3d.mat('water', (0.08, 0.32, 0.7), rough=0.2, coat=0); glow(water, (0.08, 0.3, 0.7), 0.15)
    ink = b3d.mat('ink', (0.98, 0.85, 0.35), rough=0.6, coat=0); glow(ink, (0.98, 0.85, 0.35), 0.6)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.5)
    table = b3d.mat('table', (0.12, 0.1, 0.09), rough=0.8, coat=0)
    # upright glass on the left
    ga = G(-3.6, 0.0, 0.0); glass(ga, w, M); ga.prism([(0, 0), (w, 0), (w, b['h0']), (0, b['h0'])], water)
    for v in range(10):
        ga.box(-0.35, v, 0.4, 0.06, ink, y=-DEP / 2 - 0.02, dy=0.02)
        if v == b['h0']: x, z = ga.P(-1.1, v); text(str(v), (x, -0.5, z), 0.26, ink)
    # tilted glass on the right, pivot on its low (left) bottom corner
    gb = G(0.7, 0.0, t); glass(gb, w, M)
    for v in range(10):
        gb.box(-0.35, v, 0.4, 0.06, ink, y=-DEP / 2 - 0.02, dy=0.02); x, z = gb.P(-1.15, v); text(str(v), (x, -0.5, z), 0.24, ink)
    if after:
        lo, hi = float(low(b)), float(high(b))
        gb.prism([(0, 0), (w, 0), (w, hi), (0, lo)], water)
        x, z = gb.P(-0.35, lo); bpy.ops.mesh.primitive_torus_add(location=(x, -DEP / 2 - 0.06, z), rotation=(math.radians(90), 0, 0), major_radius=0.14, minor_radius=0.025, major_segments=40)
        bpy.context.object.data.materials.append(mint)
    xs = [ga.P(-1.2, 0)[0], gb.P(w, 0)[0] + 0.3]
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.5, 0, -0.06)); o = bpy.context.object; o.scale = (7.8, 1.6, 0.12); o.data.materials.append(table)
    zt = gb.P(w, 10)[1]
    b3d.stack_camera((-0.5, 0, 1.75), 7.4, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((960, 720), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
