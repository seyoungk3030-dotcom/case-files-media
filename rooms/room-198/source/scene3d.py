"""ROOM 198 3D sprites: an open-front lift car with a kitchen scale on its floor and a 5 kg watermelon on the scale.
A glowing arrow above the car shows which way it moves. p*: scale display '?'; a*: display shows the reading in mint."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')


def glowm(name, c, s, rough=0.4):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    return m


def box(m, loc, sc, bev=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = sc
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m); b3d.bevel(o, bev, 4); return o


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.pi / 2, 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def melon():
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.62, location=(0, 0.1, 0.62 + 0.36), segments=64, ring_count=32); o = bpy.context.object
    o.scale = (1.0, 1.0, 0.92); bpy.ops.object.shade_smooth()
    m = bpy.data.materials.new('melon'); m.use_nodes = True; nt = m.node_tree; p = nt.nodes['Principled BSDF']
    p.inputs['Roughness'].default_value = 0.35
    tc = nt.nodes.new('ShaderNodeTexCoord'); wave = nt.nodes.new('ShaderNodeTexWave'); wave.wave_type = 'BANDS'; wave.bands_direction = 'X'
    wave.inputs['Scale'].default_value = 1.6; wave.inputs['Distortion'].default_value = 6.0; wave.inputs['Detail'].default_value = 3.0
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); ang = nt.nodes.new('ShaderNodeMath'); ang.operation = 'ARCTAN2'
    nt.links.new(tc.outputs['Object'], sep.inputs[0]); nt.links.new(sep.outputs['X'], ang.inputs[0]); nt.links.new(sep.outputs['Y'], ang.inputs[1])
    comb = nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(ang.outputs[0], comb.inputs['X']); nt.links.new(sep.outputs['Z'], comb.inputs['Y'])
    nt.links.new(comb.outputs[0], wave.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position = 0.45; ramp.color_ramp.elements[1].position = 0.6
    ramp.color_ramp.elements[0].color = (0.02, 0.12, 0.03, 1); ramp.color_ramp.elements[1].color = (0.12, 0.42, 0.1, 1)
    nt.links.new(wave.outputs['Fac'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], p.inputs['Base Color'])
    o.data.materials.append(m)


def scene(key, after):
    d, ch = BOARDS[key]
    wall = b3d.mat('wall', (0.62, 0.65, 0.7), rough=0.3, metal=0.7, coat=0); floor = b3d.mat('floor', (0.2, 0.21, 0.24), rough=0.6, coat=0)
    trim = b3d.mat('trim', (0.85, 0.7, 0.35), rough=0.25, metal=1.0, coat=0)
    W, H, D = 2.6, 3.0, 1.8
    box(floor, (0, 0.2, 0.06), (W, D, 0.12)); box(wall, (0, 0.2 + D / 2, H / 2), (W, 0.08, H))
    for x in (-W / 2, W / 2): box(wall, (x, 0.2, H / 2), (0.08, D, H))
    box(wall, (0, 0.2, H), (W + 0.08, D, 0.1)); box(trim, (0, 0.2 + D / 2 - 0.05, 1.1), (W - 0.1, 0.03, 0.06), 0.01)
    # cable on top and the direction sign
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.9, location=(0, 0.2, H + 0.5)); bpy.context.object.data.materials.append(b3d.mat('cab', (0.15, 0.15, 0.17), rough=0.5, coat=0))
    sign = b3d.mat('sign', (0.07, 0.09, 0.14), rough=0.4, coat=0); box(sign, (0, -0.65, H - 0.32), (0.9, 0.06, 0.42), 0.05)
    sg = 1 if d == 'up' else -1; zc = H - 0.32
    me = bpy.data.meshes.new('tri'); me.from_pydata([(-0.2, -0.7, zc - 0.13 * sg), (0.2, -0.7, zc - 0.13 * sg), (0, -0.7, zc + 0.17 * sg)], [], [(0, 1, 2)])
    o = bpy.data.objects.new('tri', me); bpy.context.collection.objects.link(o)
    o.modifiers.new('sol', 'SOLIDIFY').thickness = 0.04
    o.data.materials.append(glowm('arrow', (1.0, 0.8, 0.25), 2.0))
    # kitchen scale
    body = b3d.mat('scale', (0.93, 0.93, 0.95), rough=0.25, coat=0.6); box(body, (0, 0.1, 0.24), (1.5, 1.2, 0.24), 0.08)
    box(b3d.mat('lcd', (0.05, 0.08, 0.1), rough=0.2, coat=0), (0, -0.505, 0.24), (0.9, 0.02, 0.2), 0.02)
    if after: text(f'{int(GOOD[key])} kg', (0, -0.53, 0.235), 0.19, glowm('mint', (0.2, 0.95, 0.65), 1.6))
    else: text('? kg', (0, -0.53, 0.235), 0.19, glowm('wt', (0.9, 0.95, 1.0), 1.0))
    melon()
    b3d.stack_camera((0, 0, 1.6), 4.2, az=14.0, el=12.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((640, 700), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t, 1), flush=True)
