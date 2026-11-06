"""ROOM 137 3D sprites: front view of a bimetal strip (gold brass layer + grey iron layer) clamped upright between two
contact posts, each wired to a numbered bulb; a candle (heated) or an ice block (cooled) sits by the strip and small
labels name the two metals. p*: the strip straight, both bulbs off. a*: the strip curls over to touch one contact,
that bulb glows and its chip turns mint."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
Z0, LS, RB, CX = 0.55, 2.5, 5.7, 0.62


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def box(m, c, s, bev=0.02, ry=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c, rotation=(0, ry, 0)); o = bpy.context.object; o.scale = s; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev)
    return o


def rod(a, b, r, m, v=12):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=v); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y'); o.data.materials.append(m); return o


def strip(s, brass_side, mb, mi):
    n = 24; dl = LS / n
    for i in range(n):
        if s == 0: c = Vector((0, 0, Z0 + (i + 0.5) * dl)); phi = 0.0; nn = Vector((1, 0, 0))
        else:
            phi = (i + 0.5) * dl / RB; c = Vector((s * RB * (1 - math.cos(phi)), 0, Z0 + RB * math.sin(phi))); nn = Vector((math.cos(phi), 0, -s * math.sin(phi)))
        for side, m in (('L', mb if brass_side == 'L' else mi), ('R', mb if brass_side == 'R' else mi)):
            e = -0.06 if side == 'L' else 0.06
            box(m, c + nn * e, (0.12, 0.42, dl + 0.004), 0.0, s * phi)


def scene(k, after):
    b = BOARDS[k]; on = RES[k][2] if after else None; s = (1 if on == 'R' else -1) if after else 0
    brass = b3d.mat('brass', (0.85, 0.62, 0.2), rough=0.3, metal=0.9, coat=0); iron = b3d.mat('iron', (0.32, 0.34, 0.38), rough=0.4, metal=0.8, coat=0)
    base = b3d.mat('base', (0.08, 0.09, 0.13), rough=0.6, coat=0); clamp = b3d.mat('clamp', (0.2, 0.22, 0.28), rough=0.5, coat=0)
    copper = b3d.mat('copper', (0.8, 0.42, 0.25), rough=0.3, metal=0.9, coat=0); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    chip = b3d.mat('chip', (0.94, 0.95, 0.97), rough=0.5, coat=0); mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.6)
    glassoff = b3d.mat('bulboff', (0.75, 0.78, 0.85), rough=0.2, coat=0); glassoff.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.6
    glasson = b3d.mat('bulbon', (1.0, 0.9, 0.5), rough=0.2, coat=0); glow(glasson, (1.0, 0.8, 0.3), 3.0)
    white = b3d.mat('white', (0.92, 0.93, 0.96), rough=0.5, coat=0); glow(white, (0.92, 0.93, 0.96), 0.4)
    box(base, (0, 0, -0.1), (3.8, 1.6, 0.2), 0.05); box(clamp, (0, 0, 0.3), (0.5, 0.6, 0.6), 0.04)
    strip(s, b['brass'], brass, iron)
    zc = Z0 + LS - 0.02
    for sd, sx in (('L', -1), ('R', 1)):
        box(clamp, (sx * (CX + 0.15), 0, zc / 2), (0.12, 0.3, zc), 0.02)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.07, location=(sx * (CX + 0.07), 0, zc)); bpy.context.object.data.materials.append(copper)
        bc = Vector((sx * 1.35, 0, zc + 0.75)); rod((sx * (CX + 0.15), 0, zc), (sx * 1.35, 0, zc + 0.45), 0.02, copper)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.28, location=bc); o = bpy.context.object; o.data.materials.append(glasson if on == sd else glassoff)
        for p in o.data.polygons: p.use_smooth = True
        box(clamp, bc - Vector((0, 0, 0.32)), (0.22, 0.22, 0.16), 0.03)
        cp = bc + Vector((0, -0.3, 0.55))
        bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.05, location=cp, rotation=(math.radians(90), 0, 0), vertices=32); bpy.context.object.data.materials.append(mint if on == sd else chip)
        text(str(b['lamps'][sd]), cp + Vector((0, -0.03, 0)), 0.3, ink)
    for sd, sx in (('L', -1), ('R', 1)):
        text('놋쇠' if b['brass'] == sd else '철', (sx * 0.42, -0.35, 0.28), 0.17, white)
    if b['temp'] == 'hot':
        wax = b3d.mat('wax', (0.95, 0.92, 0.85), rough=0.6, coat=0); fl = b3d.mat('flame', (1.0, 0.6, 0.1), rough=0.5, coat=0); glow(fl, (1.0, 0.55, 0.1), 8.0)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=0.9, location=(0, -0.55, 0.45)); bpy.context.object.data.materials.append(wax)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(0, -0.55, 1.02)); o = bpy.context.object; o.scale = (1, 1, 1.8); o.data.materials.append(fl)
    else:
        ice = b3d.mat('ice', (0.7, 0.88, 1.0), rough=0.15, coat=0.5); ice.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.75; glow(ice, (0.6, 0.85, 1.0), 0.4)
        for dx, dz in ((-0.18, 0.75), (0.18, 0.78), (0.0, 1.05)): box(ice, (dx, -0.48, dz), (0.3, 0.3, 0.28), 0.05)
    b3d.stack_camera((0, 0, 2.15), 5.3, az=0.0, el=6.0)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((760, 900), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
