"""ROOM 156 3D sprites: a curling house (blue, white, red rings and the button) on ice with red-handled and yellow-handled
stones, seen from above at a slant. p*: the end of the round. a*: a thin white circle through the other team's nearest
stone and mint rings on the stones that score."""
import os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, HR, SR
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
EL = 62.0


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def matte(name, col):
    m = b3d.mat(name, col, rough=0.6, coat=0); m.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0.1; return m


def disc(r, z, m):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=0.004, location=(0, 0, z), vertices=96); bpy.context.object.data.materials.append(m)


def scene(k, after):
    win, sc, _, lim = RES[k]
    ice = matte('ice', (0.62, 0.68, 0.76)); blue = matte('blue', (0.1, 0.3, 0.75)); wht = matte('w', (0.95, 0.96, 0.98)); red = matte('r', (0.8, 0.12, 0.12))
    granite = b3d.mat('gran', (0.35, 0.36, 0.38), rough=0.5, coat=0.3)
    hc = {'R': b3d.mat('hr', (0.9, 0.12, 0.1), rough=0.3, coat=0.4), 'Y': b3d.mat('hy', (1.0, 0.8, 0.1), rough=0.3, coat=0.4)}
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.3, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.8)
    lm = b3d.mat('lim', (0.05, 0.05, 0.08), rough=0.6, coat=0)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.05)); o = bpy.context.object; o.scale = (4.3, 4.3, 0.1); o.data.materials.append(ice); b3d.bevel(o, 0.06)
    disc(HR, 0.002, blue); disc(1.22, 0.004, wht); disc(0.61, 0.006, red); disc(0.15, 0.008, wht)
    for i, (x, y, t) in enumerate(BOARDS[k]):
        bpy.ops.mesh.primitive_cylinder_add(radius=SR, depth=0.11, location=(x, y, 0.065), vertices=48); o = bpy.context.object; o.data.materials.append(granite); b3d.bevel(o, 0.03)
        bpy.ops.mesh.primitive_cylinder_add(radius=SR * 0.62, depth=0.03, location=(x, y, 0.13), vertices=40); bpy.context.object.data.materials.append(hc[t])
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.16)); o = bpy.context.object; o.scale = (SR * 1.2, 0.05, 0.04); o.data.materials.append(hc[t])
        if after and i in sc:
            bpy.ops.mesh.primitive_torus_add(location=(x, y, 0.1), major_radius=SR + 0.06, minor_radius=0.025, major_segments=48); bpy.context.object.data.materials.append(mint)
    if after:
        bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0.02), major_radius=lim, minor_radius=0.02, major_segments=128); bpy.context.object.data.materials.append(lm)
    b3d.stack_camera((0, 0.0, 0.0), 4.5, az=0.0, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((880, 820), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
