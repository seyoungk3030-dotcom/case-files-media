"""ROOM 047 3D sprites: per net A-D the six faces lie flat as thick tiles ('nA'..'nD'): white tiles with dark
numbers, the star face mint with a white star. Answer sprites ('hA'..'hD') dim every tile except the star (mint glow)
and the face opposite it (amber glow). Same camera scale for all. Optional argv after '--': names to render."""
import math, os, sys, time
import bpy, bmesh
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import NETS, STAR, solve
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)


def glow(m, col, s):
    p = m.node_tree.nodes['Principled BSDF']; p.inputs['Emission Color'].default_value = (*col, 1)
    p.inputs['Emission Strength'].default_value = s; return m


def flat_star(m, x, y, z, r=0.3, depth=0.05):
    me = bpy.data.meshes.new('star'); bm = bmesh.new()
    vs = [bm.verts.new((math.sin(i * math.pi / 5) * (r if i % 2 == 0 else r * 0.45),
                        math.cos(i * math.pi / 5) * (r if i % 2 == 0 else r * 0.45), 0)) for i in range(10)]
    f = bm.faces.new(vs); ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    bmesh.ops.translate(bm, verts=[v for v in ext['geom'] if isinstance(v, bmesh.types.BMVert)], vec=(0, 0, depth))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('star', me); bpy.context.collection.objects.link(o); o.location = (x, y, z)
    o.data.materials.append(m); return o


def scene(k, answer):
    net = NETS[k]; s, opp, _, _ = solve(net)
    cx = (min(c[0] for c in net) + max(c[0] for c in net)) / 2; cy = (min(c[1] for c in net) + max(c[1] for c in net)) / 2
    b3d.reset((1000, 800), 40); b3d.lights(6)
    font = bpy.data.fonts.load(os.path.join(HERE, '../../../kit/fonts/P-Bold.otf'))
    b3d.stack_camera((0, 0, 0), 5.6, 0.0, 58.0)
    white = b3d.mat('white', (0.93, 0.92, 0.88), rough=0.35, coat=0.4)
    dim = b3d.mat('dim', (0.42, 0.46, 0.54), rough=0.5, coat=0.1)
    ink = b3d.mat('ink', (0.08, 0.10, 0.15), rough=0.4, coat=0.2)
    mint = b3d.mat('mint', b3d.PAL['mint'], rough=0.3, coat=0.5)
    if answer: glow(mint, (0.1, 0.9, 0.7), 0.6)
    gold = glow(b3d.mat('gold', (0.98, 0.70, 0.15), rough=0.3, coat=0.5), (1.0, 0.65, 0.1), 1.0)
    star_m = b3d.mat('starw', (0.98, 0.98, 0.95), rough=0.3, coat=0.4)
    for (c, r), v in net.items():
        x, y = c - cx, -(r - cy)
        m = mint if v == STAR else (gold if answer and (c, r) == opp else (dim if answer else white))
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.11))
        t = bpy.context.object; t.scale = (0.94, 0.94, 0.22); t.data.materials.append(m); b3d.bevel(t, 0.05, 3)
        if v == STAR: flat_star(star_m, x, y, 0.22)
        else:
            bpy.ops.object.text_add(location=(x, y, 0.22)); o = bpy.context.object
            o.data.font = font; o.data.body = str(v); o.data.size = 0.62; o.data.extrude = 0.02
            o.data.align_x = 'CENTER'; o.data.align_y = 'CENTER'; o.data.materials.append(ink)
    b3d.floor()


names = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [p + k for k in 'ABCD' for p in 'nh']
for name in names:
    t = time.time(); scene(name[1], name[0] == 'h'); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
