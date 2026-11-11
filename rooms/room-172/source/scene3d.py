"""ROOM 172 3D sprites: one glass per board, seen from the front and slightly above: a cocktail cone on a stem, a
V-shaped vase (triangular prism, edge down) or a straight tumbler. Thin dark rings split the height from the inside
bottom to the rim into N equal parts, and blue water reaches the first ring. p*: as above. a*: the glass filled to the
rim in pale water, the old water still blue inside, and the first ring glowing mint."""
import math, os, sys, time
import bpy, bmesh
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
H = 1.8; R = 0.95; L = 0.9; Z0 = 0.0  # inner bottom of every glass at z = Z0, rim at Z0 + H


def glowm(name, c, s):
    m = b3d.mat(name, c, rough=0.3, coat=0); q = m.node_tree.nodes['Principled BSDF']
    q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s; return m


def prism(h, m, top, shell=False):
    """triangular prism, edge down at z = Z0, half-width R * h / H at height h, length L along y"""
    w = R * h / H; me = bpy.data.meshes.new('v'); bm = bmesh.new()
    v = [bm.verts.new(p) for p in [(0, -L / 2, Z0), (-w, -L / 2, Z0 + h), (w, -L / 2, Z0 + h), (0, L / 2, Z0), (-w, L / 2, Z0 + h), (w, L / 2, Z0 + h)]]
    bm.faces.new((v[0], v[1], v[2])); bm.faces.new((v[3], v[5], v[4])); bm.faces.new((v[0], v[3], v[4], v[1])); bm.faces.new((v[0], v[2], v[5], v[3]))
    if top: bm.faces.new((v[1], v[4], v[5], v[2]))
    bm.normal_update(); bm.to_mesh(me); o = bpy.data.objects.new('v', me); bpy.context.collection.objects.link(o); o.data.materials.append(m)
    if shell: s = o.modifiers.new('s', 'SOLIDIFY'); s.thickness = 0.03; s.offset = 1
    return o


def body(shape, h, m, top, shell=False):
    if shape == 'vee': return prism(h, m, top, shell)
    if shape == 'cone':
        bpy.ops.mesh.primitive_cone_add(radius1=0.0, radius2=R * h / H, depth=h, location=(0, 0, Z0 + h / 2), vertices=64, end_fill_type='NGON' if top else 'NOTHING')
    else:
        bpy.ops.mesh.primitive_cylinder_add(radius=R * 0.72, depth=h, location=(0, 0, Z0 + h / 2), vertices=64, end_fill_type='NGON' if top else 'NOTHING')
    o = bpy.context.object; o.data.materials.append(m)
    if shell: s = o.modifiers.new('s', 'SOLIDIFY'); s.thickness = 0.03; s.offset = 1
    return o


def ring(shape, z, m, t=0.018):
    h = z - Z0
    if shape == 'vee':
        w = R * h / H
        for (a, b) in [((-w, -L / 2), (w, -L / 2)), ((-w, L / 2), (w, L / 2)), ((-w, -L / 2), (-w, L / 2)), ((w, -L / 2), (w, L / 2))]:
            ln = math.dist(a, b); bpy.ops.mesh.primitive_cylinder_add(radius=t, depth=ln + 2 * t, location=((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, z), vertices=12,
                                                                       rotation=(math.pi / 2, 0, 0) if a[0] == b[0] else (0, math.pi / 2, 0))
            bpy.context.object.data.materials.append(m)
        return
    r = R * h / H if shape == 'cone' else R * 0.72
    bpy.ops.mesh.primitive_torus_add(location=(0, 0, z), major_radius=r + 0.03, minor_radius=t, major_segments=64, minor_segments=8); bpy.context.object.data.materials.append(m)


def scene(k, after):
    shape, N = BOARDS[k]
    mg = b3d.mat('glass', (0.85, 0.92, 1.0), rough=0.05, coat=0.5); mg.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.28
    mw = b3d.mat('water', (0.12, 0.45, 0.95), rough=0.1, coat=0.4)
    mp = b3d.mat('pale', (0.6, 0.8, 1.0), rough=0.1, coat=0.2); mp.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.35
    ink = b3d.mat('ink', (0.1, 0.1, 0.13), rough=0.5, coat=0); mint = glowm('mint', (0.15, 0.85, 0.6), 2.2)
    wood = b3d.mat('wood', (0.75, 0.55, 0.35), rough=0.6, coat=0.2)
    body(shape, H, mg, False, shell=True)
    body(shape, H / N - 0.004, mw, True)
    if after: body(shape, H - 0.01, mp, True)
    for i in range(1, N): ring(shape, Z0 + H * i / N, mint if after and i == 1 else ink, 0.026 if after and i == 1 else 0.018)
    ring(shape, Z0 + H, ink, 0.022)
    if shape == 'cone':  # stem and foot below the point
        bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=1.0, location=(0, 0, Z0 - 0.5), vertices=24); bpy.context.object.data.materials.append(mg)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.6, depth=0.05, location=(0, 0, Z0 - 1.0), vertices=64); bpy.context.object.data.materials.append(mg)
        base = Z0 - 1.03
    elif shape == 'vee':  # two wooden cradles with a V notch hold the edge off the table
        zt = Z0 + 0.32; wt = R * (zt - Z0) / H; a = 0.5; zb = Z0 - 0.35
        for y in (-L / 2 + 0.1, L / 2 - 0.1):
            me = bpy.data.meshes.new('c'); bm = bmesh.new()
            pts = [(-a, zb), (a, zb), (a, zt), (wt + 0.02, zt), (0, Z0 - 0.02), (-wt - 0.02, zt), (-a, zt)]
            f = [bm.verts.new((x, y - 0.07, z)) for x, z in pts]; b = [bm.verts.new((x, y + 0.07, z)) for x, z in pts]
            bm.faces.new(f[::-1]); bm.faces.new(b)
            for i in range(len(pts)):
                j = (i + 1) % len(pts); bm.faces.new((f[i], f[j], b[j], b[i]))
            bm.normal_update(); bm.to_mesh(me); o = bpy.data.objects.new('c', me); bpy.context.collection.objects.link(o); o.data.materials.append(wood)
            b3d.bevel(o, 0.015, 2)
        base = zb
    else:
        bpy.ops.mesh.primitive_cylinder_add(radius=R * 0.72 + 0.03, depth=0.15, location=(0, 0, Z0 - 0.075), vertices=64); bpy.context.object.data.materials.append(mg)
        base = Z0 - 0.15
    b3d.stack_camera((0, 0, (base + Z0 + H) / 2), 3.6, az=18.0, el=14.0)


only = sys.argv[1:]
for key in 'ABCD':
    for after in (False, True):
        name = ('a' if after else 'p') + key
        if only and name not in only: continue
        b3d.reset((900, 1000), 48); b3d.lights(3)
        t = time.time(); scene(key, after); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
