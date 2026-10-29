"""ROOM 053 3D sprites: two level reference seesaws ('ref1', 'ref2') and four seesaws A-D ('qA'..'qD') with a glowing
'?' on the right pan, plus one icon per shape. Optional argv after '--': names to render."""
import json, math, os, sys, time
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
import b3d
OUT = os.path.join(HERE, '..', '.build-3d'); os.makedirs(OUT, exist_ok=True)
P = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
SCALES = {'ref1': P['refs'][0], 'ref2': P['refs'][1]} | {'q' + k: (v, '?') for k, v in P['ask'].items()}


def qmark():
    m = b3d.mat('q', (1.0, 0.62, 0.08)); p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Emission Color'].default_value = (1.0, 0.62, 0.08, 1); p.inputs['Emission Strength'].default_value = 1.2
    bpy.ops.object.text_add(location=(2.05, 0, 1.33 + 0.68), rotation=(math.radians(90), 0, 0)); t = bpy.context.object
    t.data.body = '?'; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.size = 1.5; t.data.extrude = 0.12; t.data.bevel_depth = 0.05
    t.data.materials.append(m)


def scene(name):
    if name.startswith('icon-'):
        b3d.reset((300, 300)); M = b3d.mats(); b3d.floor(); b3d.lights(2)
        fn, col = b3d.SHAPES[name[5:]]; fn(M[col], 0, 0)
        b3d.camera(target=(0, 0, 0.42), dist=6, height=2.0, lens=70); return
    L, R = SCALES[name]
    b3d.reset((1000, 470)); M = b3d.mats(); b3d.floor(); b3d.lights(); b3d.camera(target=(0, 0, 1.4))
    b3d.seesaw(M, list(L), [] if R == '?' else list(R))
    if R == '?': qmark()


names = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else list(SCALES) + ['icon-c', 'icon-s', 'icon-r']
for name in names:
    t = time.time(); scene(name); b3d.render(f'{OUT}/{name}.png'); print(name, round(time.time() - t, 1), flush=True)
