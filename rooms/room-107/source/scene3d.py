"""ROOM 107 3D sprites. o*: top view of Earth with eight grey moons on a ring, numbered, lit only by a sun lamp from
the board's sun direction (a glowing sun sits at the frame edge). v*: the target moon as a person on Earth sees it
(camera at Earth looking at that moon, head to the north). a*: the orbit with the matching spot ringed in mint."""
import math, os, sys, time
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import BOARDS, RES, spot
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')
RO, RM = 1.65, 0.27


def glow(m, c, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = (*c, 1); q.inputs['Emission Strength'].default_value = s


def text(s, loc, size, m):
    bpy.ops.object.text_add(location=loc); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.02; t.data.materials.append(m)
    t.visible_shadow = False


def ball(loc, r, m):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=64, ring_count=32); o = bpy.context.object; o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = True
    return o


def sun(deg):
    bpy.ops.object.light_add(type='SUN'); L = bpy.context.object
    d = Vector((math.cos(math.radians(deg)), math.sin(math.radians(deg)), 0))
    L.rotation_mode = 'QUATERNION'; L.rotation_quaternion = Vector((0, 0, -1)).rotation_difference(-d); L.data.energy = 4.5; L.data.angle = math.radians(1)
    return d


def dim_world():
    bpy.context.scene.world.node_tree.nodes['Background'].inputs[1].default_value = 0.12


def orbit(k, after):
    b = BOARDS[k]; dim_world(); d = sun(b['sun'])
    moon = b3d.mat('moon', (0.75, 0.75, 0.72), rough=0.9, coat=0); earth = b3d.mat('earth', (0.10, 0.35, 0.85), rough=0.5, coat=0.2)
    white = b3d.mat('white', (0.92, 0.93, 0.96), rough=0.5, coat=0); glow(white, (0.9, 0.92, 0.96), 0.6)
    ring = b3d.mat('ring', (0.3, 0.34, 0.45), rough=0.6, coat=0); glow(ring, (0.3, 0.34, 0.45), 0.4)
    mint = b3d.mat('mint', (0.15, 0.85, 0.6), rough=0.4, coat=0); glow(mint, (0.15, 0.85, 0.6), 2.0)
    sunm = b3d.mat('sun', (1, 0.8, 0.3), rough=0.5, coat=0); glow(sunm, (1, 0.7, 0.2), 2.5)
    ball((0, 0, 0), 0.5, earth)
    bpy.ops.mesh.primitive_torus_add(major_radius=RO, minor_radius=0.012, major_segments=128); bpy.context.object.data.materials.append(ring)
    for i in range(1, 9):
        x, y = spot(i, b['start']); ball((x * RO, y * RO, 0), RM, moon)
        text(str(i), (x * (RO + 0.6), y * (RO + 0.6), 0), 0.52, white)
        if after and i == RES[k][0][0]:
            bpy.ops.mesh.primitive_torus_add(location=(x * RO, y * RO, 0), major_radius=RM + 0.1, minor_radius=0.03); bpy.context.object.data.materials.append(mint)
    s = ball(d * 3.05, 0.42, sunm); s.visible_shadow = False
    b3d.stack_camera((0, 0, 0), 6.6, az=0.0, el=89.0)


def view(k):
    b = BOARDS[k]; dim_world(); sun(b['sun']); x, y = spot(b['target'], b['start'])
    moon = b3d.mat('moon', (0.75, 0.75, 0.72), rough=0.9, coat=0); ball((x * RO, y * RO, 0), RM, moon)
    bpy.ops.object.camera_add(location=(0, 0, 0)); cam = bpy.context.object; cam.data.type = 'ORTHO'; cam.data.ortho_scale = RM * 2.4
    tgt = bpy.data.objects.new('t', None); bpy.context.collection.objects.link(tgt); tgt.location = (x * RO, y * RO, 0)
    c = cam.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'; bpy.context.scene.camera = cam


only = sys.argv[1:]
for k in 'ABCD':
    for kind in ('p', 'a', 'v'):
        name = kind + k
        if only and name not in only: continue
        b3d.reset((900, 900) if kind != 'v' else (400, 400), 48)
        t = time.time()
        if kind == 'v': view(k)
        else: orbit(k, kind == 'a')
        b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
