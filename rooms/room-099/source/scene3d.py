"""ROOM 099 3D sprites: a paper loop with n half twists, standing on a desk, with dark dashed cut lines running all the
way round it, and a pair of scissors at one cut. a*: the cut lanes are pulled slightly apart, and lanes that become
the same loop share a colour."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
RR, WD, NU = 1.55, 0.95, 360
PAL = [(0.98, 0.45, 0.40), (0.30, 0.62, 1.0), (0.98, 0.75, 0.20), (0.35, 0.85, 0.55)]


def pt(u, w, n):
    t = math.pi / 2 + n * u / 2; r = (math.cos(u), math.sin(u), 0.0); s = (w - 0.5) * WD
    return (RR * r[0] + s * math.cos(t) * r[0], RR * r[1] + s * math.cos(t) * r[1], 1.2 + s * math.sin(t))


def strip(w0, w1, n, m, nw=4):
    verts, faces = [], []
    for i in range(NU + 1):
        u = 2 * math.pi * i / NU
        for j in range(nw + 1): verts.append(pt(u, w0 + (w1 - w0) * j / nw, n))
    for i in range(NU):
        for j in range(nw):
            a = i * (nw + 1) + j; faces.append((a, a + 1, a + nw + 2, a + nw + 1))
    me = bpy.data.meshes.new('s'); me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new('s', me); bpy.context.collection.objects.link(o); o.data.materials.append(m)
    sol = o.modifiers.new('t', 'SOLIDIFY'); sol.thickness = 0.025; sol.offset = 0
    for p in me.polygons: p.use_smooth = True


def dashes(w, n, m):
    for i in range(0, NU, 6):
        u0, u1 = 2 * math.pi * i / NU, 2 * math.pi * (i + 3) / NU
        verts = []
        for u in (u0, u1):
            for dw in (-0.012, 0.012): verts.append(pt(u, w + dw, n))
        me = bpy.data.meshes.new('d'); me.from_pydata(verts, [], [(0, 1, 3, 2)]); me.update()
        o = bpy.data.objects.new('d', me); bpy.context.collection.objects.link(o); o.data.materials.append(m)
        sol = o.modifiers.new('t', 'SOLIDIFY'); sol.thickness = 0.04; sol.offset = 0


def scene(k, after):
    n, kc = BOARDS[k]
    desk = b3d.mat('desk', (0.04, 0.05, 0.09), rough=0.85, coat=0); paper = b3d.mat('paper', (0.80, 0.80, 0.76), rough=0.7, coat=0)
    ink = b3d.mat('ink', (0.05, 0.05, 0.08), rough=0.6, coat=0)
    pass
    cuts = [(i + 1) / (kc + 1) for i in range(kc)]
    if not after:
        strip(0, 1, n, paper, nw=12)
        for c in cuts: dashes(c, n, ink)
    else:
        orb = {j: oi for oi, o in enumerate(RES[k]) for j in o}; edges = [0] + cuts + [1]
        for j in range(kc + 1):
            m = b3d.mat(f'l{j}', PAL[orb[j] % len(PAL)], rough=0.5, coat=0)
            strip(edges[j] + 0.018, edges[j + 1] - 0.018, n, m)
    b3d.stack_camera((0, 0, 1.1), 4.4, az=0.0, el=30.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((760, 620), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
