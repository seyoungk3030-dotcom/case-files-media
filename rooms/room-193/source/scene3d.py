"""ROOM 193 3D sprites: produce (watermelon, cucumbers, tomatoes, napa cabbage) on a platform scale, with a glass water
gauge beside it. p*: fresh, the display shows the weight and the gauge the water share. a*: after drying, the produce is
smaller and darker (volume follows weight), the gauge sits only a little lower and the display glows mint with the new
weight."""
import math, os, random, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, GOOD
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')


def glowm(name, c, s, rough=0.4, alpha=1.0):
    m = b3d.mat(name, c, rough=rough, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s
    if alpha < 1: q.inputs['Alpha'].default_value = alpha
    return m


def box(m, loc, scale, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev, 3)
    return o


def sph(m, r, loc, sc=(1, 1, 1), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=48, ring_count=24); o = bpy.context.object
    o.scale = sc; o.rotation_euler = rot; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.pi / 2, 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def dark(c, after): return tuple(x * (0.62 if after else 1.0) for x in c)


def produce(name, s, after, top):
    random.seed(3)
    if name == '수박':
        m = bpy.data.materials.new('wm'); m.use_nodes = True; nt = m.node_tree; N = nt.nodes; Lk = nt.links
        bs = N['Principled BSDF']; bs.inputs['Roughness'].default_value = 0.35; bs.inputs['Coat Weight'].default_value = 0.4
        tc = N.new('ShaderNodeTexCoord'); gr = N.new('ShaderNodeTexGradient'); gr.gradient_type = 'RADIAL'
        mu = N.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = 2 * math.pi * 11
        sn = N.new('ShaderNodeMath'); sn.operation = 'SINE'
        n2 = N.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 6
        ad = N.new('ShaderNodeMath'); ad.operation = 'ADD'
        cr = N.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.45; cr.color_ramp.elements[1].position = 0.6
        cr.color_ramp.elements[0].color = (*dark((0.02, 0.12, 0.03), after), 1); cr.color_ramp.elements[1].color = (*dark((0.2, 0.55, 0.15), after), 1)
        Lk.new(tc.outputs['Object'], gr.inputs['Vector']); Lk.new(gr.outputs['Fac'], mu.inputs[0]); Lk.new(mu.outputs[0], sn.inputs[0])
        Lk.new(sn.outputs[0], ad.inputs[0]); Lk.new(n2.outputs['Fac'], ad.inputs[1]); Lk.new(ad.outputs[0], cr.inputs['Fac']); Lk.new(cr.outputs['Color'], bs.inputs['Base Color'])
        r = 0.62 * s; sph(m, r, (0, 0, top + r * 0.85), (0.85, 1, 1.15), (0, math.pi / 2, 0))
    elif name == '오이':
        g = b3d.mat('cu', dark((0.12, 0.42, 0.12), after), rough=0.45, coat=0.3)
        for i, (x, y, z, a) in enumerate([(-0.3, -0.25, 0, 0.1), (0.05, -0.28, 0, -0.08), (0.38, -0.22, 0, 0.12), (-0.15, 0.08, 0, -0.05), (0.22, 0.1, 0, 0.06),
                                          (-0.1, -0.1, 1, 0.3), (0.25, -0.08, 1, -0.2), (0.05, 0.05, 2, 0.05)]):
            sph(g, 0.15 * s, (x * 0.6 * s, y * 1.6 * s, top + 0.13 * s + z * 0.22 * s), (4.2, 1, 1), (0, 0, a))
    elif name == '토마토':
        g = b3d.mat('to', dark((0.85, 0.1, 0.06), after), rough=0.25, coat=0.5); lf = b3d.mat('tl', dark((0.15, 0.45, 0.12), after), rough=0.6, coat=0)
        pts = [(x, y, 0) for x in (-0.42, 0, 0.42) for y in (-0.3, 0.12)] + [(-0.21, -0.1, 1), (0.21, -0.1, 1), (0, 0.15, 1)]
        for x, y, z in pts:
            c = (x * s, y * s, top + 0.2 * s + z * 0.3 * s); sph(g, 0.22 * s, c, (1, 1, 0.82)); sph(lf, 0.06 * s, (c[0], c[1], c[2] + 0.17 * s), (1.6, 1.6, 0.35))
    else:
        g = b3d.mat('cb', dark((0.86, 0.92, 0.62), after), rough=0.5, coat=0.2); lf = b3d.mat('cbl', dark((0.35, 0.65, 0.2), after), rough=0.5, coat=0.2)
        for x, y, z in [(0, -0.42, 0), (0, 0.0, 0), (0, 0.42, 0), (0, -0.21, 1), (0, 0.21, 1)]:
            c = (x * s - 0.12 * s, y * s, top + 0.2 * s + z * 0.32 * s); sph(g, 0.2 * s, c, (2.4, 1, 1)); sph(lf, 0.2 * s, (c[0] + 0.42 * s, c[1], c[2] + 0.02 * s), (1.3, 1.1, 1.1))

def scene(key, after):
    name, w, p0, p1 = BOARDS[key]; kg = GOOD[key] if after else w; pct = p1 if after else p0
    metal = b3d.mat('scale', (0.72, 0.74, 0.78), rough=0.3, metal=0.8, coat=0.2); dk = b3d.mat('panel', (0.05, 0.06, 0.08), rough=0.4, coat=0.3)
    box(metal, (0, 0, 0.09), (1.9, 1.3, 0.18), 0.04); box(metal, (0, 0, 0.21), (1.75, 1.15, 0.06), 0.02)
    box(dk, (0, -0.66, 0.11), (1.2, 0.02, 0.17), 0.01)
    disp = glowm('disp', (0.25, 0.95, 0.7) if after else (1.0, 0.82, 0.3), 2.2)
    text(f'{kg} kg', (0, -0.68, 0.105), 0.2, disp)
    s = (kg / w) ** (1 / 3) if after else 1.0
    produce(name, s, after, 0.24)
    glass = glowm('glass', (0.85, 0.92, 1.0), 0.15, rough=0.05, alpha=0.25); water = glowm('water', (0.2, 0.55, 1.0), 0.5, rough=0.2)
    gx, H = 1.35, 1.4
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=H, location=(gx, 0, H / 2), vertices=48); bpy.context.object.data.materials.append(glass)
    hw = H * pct / 100
    bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=hw, location=(gx, 0, hw / 2), vertices=48); bpy.context.object.data.materials.append(water)
    lab = glowm('lab', (0.95, 0.97, 1.0), 1.2); text(f'{pct}%', (gx, -0.2, H + 0.18), 0.17, lab)
    b3d.stack_camera((0.3, 0, 0.75), 3.0, az=0.0, el=16.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        nm = ('a' if after else 'p') + key
        if only and nm not in only: continue
        b3d.reset((700, 640), 40); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{nm}.png'); print(nm, round(time.time() - t, 1), flush=True)
