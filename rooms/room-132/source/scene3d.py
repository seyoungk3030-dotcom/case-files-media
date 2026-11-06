"""ROOM 132 3D sprites: a dark compass rose with eight numbered direction badges (N at the back), a wind sign (flag,
chimney smoke, windsock, or a car driving east) and a weather vane on a pole. p*: the vane head is hidden under an
amber '?' box. a*: the vane is shown, its mint arrow pointing into the wind, and the badge it points at glows."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, DIRS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
AZ, EL, RR = 20.0, 38.0, 2.25


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def facing(): return (math.radians(90 - EL), 0, math.radians(AZ))


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc, rotation=facing()); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.01; t.data.materials.append(m)


def cam_dir(): return Vector((math.sin(math.radians(AZ)) * math.cos(math.radians(EL)), -math.cos(math.radians(AZ)) * math.cos(math.radians(EL)), math.sin(math.radians(EL))))


def vec(i): a = math.radians(45 * i); return Vector((math.sin(a), math.cos(a), 0))


def rod(a, b, r, m, v=12):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=v); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y'); o.data.materials.append(m); return o


def box(m, c, s, bev=0.02, rz=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c, rotation=(0, 0, rz)); o = bpy.context.object; o.scale = s; o.data.materials.append(m)
    if bev: b3d.bevel(o, bev)
    return o


def vane(c, ang, m, fin):
    d = vec(ang); top = Vector(c)
    rod(top - d * 0.7, top + d * 0.55, 0.035, m)
    bpy.ops.mesh.primitive_cone_add(radius1=0.13, depth=0.32, location=top + d * 0.7); o = bpy.context.object; o.data.materials.append(m)
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y')
    bpy.ops.mesh.primitive_cube_add(size=1, location=top - d * 0.72); o = bpy.context.object; o.scale = (0.03, 0.42, 0.34)
    o.rotation_euler = (0, 0, -math.radians(45 * ang)); o.data.materials.append(fin)


def scene(k, after):
    b = BOARDS[k]; dw = DIRS.index(b['downwind']); up = (dw + 4) % 8; sign = b['sign']
    base = b3d.mat('base', (0.06, 0.07, 0.1), rough=0.7, coat=0); rose = b3d.mat('rose', (0.12, 0.14, 0.2), rough=0.6, coat=0)
    line = b3d.mat('line', (0.45, 0.5, 0.6), rough=0.6, coat=0); ink = b3d.mat('ink', (0.04, 0.05, 0.08), rough=0.6, coat=0)
    chip = b3d.mat('chip', (0.94, 0.95, 0.97), rough=0.5, coat=0); pole = b3d.mat('pole', (0.3, 0.32, 0.36), rough=0.4, metal=0.6, coat=0)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 1.5)
    amber = b3d.mat('amber', (0.92, 0.5, 0.06), rough=0.5, coat=0.1); fin = b3d.mat('fin', (0.1, 0.55, 0.4), rough=0.5, coat=0)
    red = b3d.mat('red', (0.85, 0.15, 0.12), rough=0.5, coat=0); white = b3d.mat('white', (0.92, 0.92, 0.9), rough=0.6, coat=0)
    bpy.ops.mesh.primitive_cylinder_add(radius=RR + 0.55, depth=0.12, location=(0, 0, -0.06), vertices=96); bpy.context.object.data.materials.append(base)
    bpy.ops.mesh.primitive_cylinder_add(radius=RR - 0.25, depth=0.03, location=(0, 0, 0.015), vertices=96); bpy.context.object.data.materials.append(rose)
    for i in range(8):
        v = vec(i); rod(v * 0.25 + Vector((0, 0, 0.04)), v * (RR - 0.45) + Vector((0, 0, 0.04)), 0.02 if i % 2 else 0.035, line)
        c = v * RR + Vector((0, 0, 0.32)); hit = after and i == up
        bpy.ops.mesh.primitive_cylinder_add(radius=0.27, depth=0.05, location=c, rotation=facing(), vertices=32); bpy.context.object.data.materials.append(mint if hit else chip)
        text(str(b['labels'][i]), c + cam_dir() * 0.03, 0.32, ink)
    text('N', vec(0) * (RR - 0.62) + Vector((0, 0, 0.2)), 0.22, line)
    H = 1.5; top = (0, 0, H)
    if sign == 'car':
        box(red, (0, 0, 0.35), (1.5, 0.75, 0.4), 0.08); box(red, (-0.1, 0, 0.7), (0.8, 0.65, 0.35), 0.08)
        for sx in (-0.5, 0.5):
            for sy in (-0.4, 0.4):
                bpy.ops.mesh.primitive_cylinder_add(radius=0.17, depth=0.12, location=(sx, sy, 0.17), rotation=(math.radians(90), 0, 0)); bpy.context.object.data.materials.append(ink)
        for j, dy in enumerate((-0.25, 0.05, 0.35)): rod((-1.05 - 0.15 * j, dy, 0.45), (-1.7 - 0.15 * j, dy, 0.45), 0.025, white)
        bpy.ops.mesh.primitive_cone_add(radius1=0.12, depth=0.3, location=(1.0, -0.55, 0.12), rotation=(0, math.radians(90), 0)); bpy.context.object.data.materials.append(amber)
        rod((0.55, -0.55, 0.12), (0.85, -0.55, 0.12), 0.04, amber)
        rod((-0.1, 0, 0.87), (-0.1, 0, H), 0.03, pole); top = (-0.1, 0, H)
    else:
        rod((0, 0, 0), top, 0.04, pole)
        dv = vec(dw)
        if sign == 'flag':
            p = Vector((-1.0, -0.75, 0)); rod(p, p + Vector((0, 0, 1.7)), 0.03, pole)
            for j in range(6):
                q = p + Vector((0, 0, 1.45)) + dv * (0.13 * j + 0.08) + Vector((0, 0, 0.02 * math.sin(j * 1.3)))
                box(red, q, (0.15, 0.02, 0.42), 0.0, math.atan2(dv.y, dv.x))
        elif sign == 'smoke':
            hpos = Vector((1.25, -0.55, 0)); box(white, hpos + Vector((0, 0, 0.3)), (0.7, 0.6, 0.6), 0.03)
            bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.6, depth=0.4, location=hpos + Vector((0, 0, 0.8)), rotation=(0, 0, math.radians(45))); bpy.context.object.data.materials.append(red)
            ch = hpos + Vector((0.15, 0.1, 1.0)); box(ink, ch, (0.14, 0.14, 0.4), 0.01)
            sm = b3d.mat('smoke', (0.8, 0.82, 0.86), rough=0.8, coat=0); sm.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.7
            for j in range(6):
                bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1 + 0.035 * j, location=ch + Vector((0, 0, 0.32 + 0.015 * j)) + dv * (0.3 * j)); o = bpy.context.object; o.data.materials.append(sm)
                for p_ in o.data.polygons: p_.use_smooth = True
        elif sign == 'sock':
            p = Vector((-1.2, -0.7, 0)); rod(p, p + Vector((0, 0, 1.5)), 0.03, pole)
            for j in range(4):
                a = p + Vector((0, 0, 1.4)) + dv * (0.12 + 0.22 * j); bb = a + dv * 0.22
                bpy.ops.mesh.primitive_cone_add(radius1=0.2 - 0.03 * j, radius2=0.17 - 0.03 * j, depth=0.22, location=(a + bb) / 2); o = bpy.context.object
                o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = dv.to_track_quat('Z', 'Y'); o.data.materials.append(amber if j % 2 == 0 else white)
    if after:
        vane(top, up, mint, fin)
    else:
        box(amber, Vector(top) + Vector((0, 0, 0.05)), (0.5, 0.5, 0.5), 0.06)
        text('?', Vector(top) + Vector((0, 0, 0.05)) + cam_dir() * 0.36, 0.42, ink)
    b3d.stack_camera((0, 0, 0.6), 6.6, az=AZ, el=EL)


only = sys.argv[1:]
for k in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + k
        if only and name not in only: continue
        b3d.reset((900, 800), 48); b3d.lights(3)
        t = time.time(); scene(k, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
