"""ROOM 051: lays the four picture equations out as transparent PNG rows ('eq1'..'eq4', 'ax1'..'ax4' with each object's
value under it) and the legend icons ('icon-A'..'icon-D') in .build-3d, from the object sprites made by scene3d.py."""
import os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import text_layer, badge, trim, WHITE, YEL
import json
B = os.path.join(HERE, '..', '.build-3d')
LINES = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))['lines']   # written by verify.py
VAL = {'A': 4, 'B': 2, 'C': 7, 'D': 8}


def obj(k, h=135):
    im = trim(Image.open(f'{B}/o{k}.png').convert('RGBA'))
    a = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()   # the object without its long soft shadow
    im = im.crop((max(0, a[0] - 12), max(0, a[1] - 12), min(im.width, a[2] + 8), min(im.height, a[3] + 14)))
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def row(expr, n, values=False):
    parts = []
    for tok in expr.split() + ['=', str(n)]:
        if tok in VAL:
            im = obj(tok)
            if values:
                b = badge(VAL[tok], 34); c = Image.new('RGBA', (max(im.width, b.width), im.height + b.height + 4))
                c.alpha_composite(im, ((c.width - im.width) // 2, 0)); c.alpha_composite(b, ((c.width - b.width) // 2, im.height + 4)); im = c
            parts.append(im)
        else: parts.append(text_layer(tok, 84, YEL if tok == '×' else WHITE))
    H = max(p.height for p in parts) + 20; W = sum(p.width for p in parts) + 14 * (len(parts) - 1)
    out = Image.new('RGBA', (1200, H)); x = (1200 - W) // 2   # same canvas for every row, so they scale alike
    for p in parts:
        y = 10 if (values and p.height > 160) else (H - p.height) // 2
        out.alpha_composite(p, (x, y)); x += p.width + 14
    return out


if __name__ == '__main__':
    for i, (e, n) in enumerate(LINES, 1):
        row(e, n).save(f'{B}/eq{i}.png'); row(e, n, True).save(f'{B}/ax{i}.png')
    for k in VAL: obj(k, 300).save(f'{B}/icon-{k}.png')
    print('eqs ok')
