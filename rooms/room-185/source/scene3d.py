"""ROOM 185 3D sprites: brushed-steel elevator button panels seen from the front. The red ring marks the floor you
are on, the yellow-lit button is where you are going. p*: question. a*: answer, every button you really pass on the
way up (after the start, up to the destination) glows mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, lab
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
DX, DZ, R = 0.36, 0.62, 0.24


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.pi / 2, 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.005; t.data.materials.append(m)


def scene(k, after):
    btn, s, d = BOARDS[k]; n = len(btn); rows = (n + 1) // 2
    steel = b3d.mat('steel', (0.3, 0.31, 0.34), rough=0.4, metal=0.8, coat=0); bm = b3d.mat('btn', (0.85, 0.86, 0.88), rough=0.3, metal=0.6, coat=0.2)
    ink = b3d.mat('ink', (0.06, 0.06, 0.08), rough=0.5, coat=0); blue = glowm('ring', (1.0, 0.2, 0.15), 1.5)
    yel = glowm('yel', (1.0, 0.75, 0.1), 1.2); mint = glowm('mint', (0.15, 0.85, 0.55), 1.0)
    H = rows * DZ + 0.5
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.06, H / 2 - 0.25)); o = bpy.context.object; o.scale = (2 * DX + 0.75, 0.08, H); o.data.materials.append(steel)
    bpy.ops.object.modifier_add(type='BEVEL'); o.modifiers['Bevel'].width = 0.04; o.modifiers['Bevel'].segments = 3
    i0, i1 = btn.index(s), btn.index(d)
    for i, v in enumerate(btn):
        x = (-DX if i % 2 == 0 else DX); z = (i // 2) * DZ
        m = bm
        if v == d: m = yel
        if after and i0 < i <= i1: m = mint
        bpy.ops.mesh.primitive_cylinder_add(radius=R, depth=0.08, location=(x, -0.02, z), rotation=(math.pi / 2, 0, 0), vertices=48)
        o = bpy.context.object; o.data.materials.append(m); bpy.ops.object.shade_smooth()
        if v == s:
            bpy.ops.mesh.primitive_torus_add(location=(x, -0.05, z), rotation=(math.pi / 2, 0, 0), major_radius=R + 0.05, minor_radius=0.035)
            bpy.context.object.data.materials.append(blue)
        text(lab(v), (x, -0.07, z), 0.24 if len(lab(v)) < 2 else 0.2, ink)
    b3d.stack_camera((0, 0, H / 2 - 0.25), max(H + 0.4, 3.2), az=0.0, el=4.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((420, 1000), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
