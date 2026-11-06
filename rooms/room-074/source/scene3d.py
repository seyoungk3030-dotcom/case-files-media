"""ROOM 074 3D sprite: a desk seen from above with things that show numbers (digital clock, calculator, calendar,
price tag, toy bus, sticky note). The strings come from verify.ITEMS."""
import math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
import b3d
from verify import ITEMS as T
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '../../../kit/fonts/P-Black.otf')


def text(s, loc, size, m, rz=0.0):
    bpy.ops.object.text_add(location=loc, rotation=(0, 0, rz)); t = bpy.context.object; t.data.body = s
    t.data.font = bpy.data.fonts['P-Black'] if 'P-Black' in bpy.data.fonts else bpy.data.fonts.load(FONT)
    t.data.size = size; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.extrude = 0.008; t.data.materials.append(m)


def box(loc, scale, m, bev=0.03, rz=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=(0, 0, rz)); o = bpy.context.object; o.scale = scale
    o.data.materials.append(m); b3d.bevel(o, bev, 3); return o


def glow(m, s):
    q = m.node_tree.nodes['Principled BSDF']; q.inputs['Emission Color'].default_value = q.inputs['Base Color'].default_value
    q.inputs['Emission Strength'].default_value = s; return m


def scene():
    m = lambda n, c, **kw: b3d.mat(n, c, **kw)
    wood = m('wood', (0.50, 0.36, 0.25), rough=0.55, coat=0.2); dark = m('dark', (0.08, 0.09, 0.12), rough=0.3, coat=0.6)
    red = glow(m('red', (1.0, 0.25, 0.20), rough=0.3), 3.0); lcd = m('lcd', (0.70, 0.78, 0.66), rough=0.5, coat=0)
    ink = m('ink', (0.10, 0.12, 0.16), rough=0.5, coat=0); grey = m('grey', (0.55, 0.58, 0.64), rough=0.35, coat=0.5)
    btn = m('btn', (0.85, 0.87, 0.90), rough=0.4); white = m('white', (0.97, 0.97, 0.98), rough=0.5, coat=0)
    rhead = m('rhead', (0.88, 0.22, 0.22), rough=0.4); yel = m('yel', (0.99, 0.82, 0.25), rough=0.45, coat=0.2)
    bus = m('bus', (0.20, 0.55, 0.90), rough=0.3, coat=0.7); note = m('note', (0.70, 0.95, 0.55), rough=0.6, coat=0)
    glass = m('glass', (0.12, 0.16, 0.22), rough=0.1, coat=0.8); amber = glow(m('amber', (1.0, 0.75, 0.2), rough=0.3), 2.0)
    box((0, 0, -0.06), (6.4, 4.6, 0.12), wood, 0.05)
    # digital clock
    box((-1.9, 1.15, 0.2), (1.9, 0.9, 0.4), dark, 0.08); text(T['clock'], (-1.9, 1.15, 0.405), 0.55, red)
    # calculator
    box((0.55, 1.0, 0.07), (1.3, 1.9, 0.14), grey, 0.08); box((0.55, 1.6, 0.145), (1.05, 0.4, 0.02), lcd, 0.01)
    text(T['calc'], (0.55, 1.6, 0.16), 0.3, ink)
    for i in range(4):
        for j in range(4): box((0.55 + (i - 1.5) * 0.24, 1.1 - j * 0.24, 0.16), (0.18, 0.17, 0.04), btn, 0.02)
    # calendar
    box((2.2, 1.0, 0.05), (1.3, 1.5, 0.1), white, 0.03); box((2.2, 1.6, 0.11), (1.3, 0.32, 0.03), rhead, 0.01)
    text(T['calendar'], (2.2, 0.85, 0.11), 0.75, ink)
    # price tag
    box((-2.0, -0.6, 0.02), (1.5, 0.75, 0.04), yel, 0.02, rz=math.radians(-8)); text(T['tag'], (-2.0, -0.6, 0.045), 0.32, ink, rz=math.radians(-8))
    # toy bus (top view, route number on the roof)
    box((0.2, -0.85, 0.22), (2.0, 0.9, 0.44), bus, 0.12)
    for i in range(4): box((-0.55 + i * 0.5, -0.85, 0.45), (0.36, 0.7, 0.02), glass, 0.02)
    box((0.2, -0.85, 0.47), (0.9, 0.42, 0.03), dark, 0.02); text(T['bus'], (0.2, -0.85, 0.49), 0.32, amber)
    # sticky note
    box((2.15, -0.9, 0.01), (1.0, 1.0, 0.02), note, 0.005, rz=math.radians(6)); text(T['note'], (2.15, -0.9, 0.025), 0.55, ink, rz=math.radians(6))
    b3d.stack_camera((0, 0.05, 0), 6.7, az=0.0, el=72.0)


b3d.reset((1100, 860), 48); b3d.lights(7)
t = time.time(); scene(); b3d.render(f'{OUT}/pA.png'); print('pA', round(time.time() - t, 1), flush=True)
