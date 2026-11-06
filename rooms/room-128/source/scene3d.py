"""ROOM 128 3D sprites: chain pieces (steel links, alternate links standing up) laid in rows on a dark tray, seen from
above at a slant. p*: the pieces as they are. a*: the links the jeweller opens glow mint (whole short pieces taken
apart, plus one end link of a piece when more joiners are needed); the count of mint links is the answer."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
P, RM, RN = 0.3, 0.2, 0.05


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def link(x, y, up, m):
    bpy.ops.mesh.primitive_torus_add(location=(x, y, RM if up else RN), rotation=(math.radians(90) if up else 0, 0, 0),
                                     major_radius=RM, minor_radius=RN, major_segments=40, minor_segments=12)
    o = bpy.context.object; o.scale = (1.35, 1, 1) if not up else (1.35, 1, 1); o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = True


def layout(L):
    """Rows of pieces, two columns when there are more than four pieces."""
    cols = 2 if len(L) > 4 else 1; rows = math.ceil(len(L) / cols); out = []
    for i, n in enumerate(L):
        c, r = (i % cols, i // cols) if cols == 2 else (0, i)
        cx = (c - (cols - 1) / 2) * 2.3; cy = ((rows - 1) / 2 - r) * 1.4
        out.append((cx - (n - 1) * P * 1.35 / 2, cy))
    return out


def scene(k, after):
    L = BOARDS[k]; cost, S = RES[k]; extra = cost - sum(L[i] for i in S); ends = [i for i in range(len(L)) if i not in S][:extra]
    steel = b3d.mat('steel', (0.75, 0.77, 0.8), rough=0.25, metal=0.95, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.35, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.2)
    tray = b3d.mat('tray', (0.06, 0.07, 0.1), rough=0.7, coat=0); felt = b3d.mat('felt', (0.02, 0.08, 0.07), rough=0.9, coat=0)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.08)); o = bpy.context.object; o.scale = (5.6, 5.8, 0.16); o.data.materials.append(tray); b3d.bevel(o, 0.08)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.0)); o = bpy.context.object; o.scale = (5.2, 5.4, 0.02); o.data.materials.append(felt)
    for i, ((x0, y0), n) in enumerate(zip(layout(L), L)):
        for j in range(n):
            open_ = after and (i in S or (i in ends and j == 0))
            link(x0 + j * P * 1.35, y0, j % 2 == 1, mint if open_ else steel)
    b3d.stack_camera((0, 0, 0), 6.6, az=0.0, el=38.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 760), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
