"""3D-look design helpers shared by carousel cards (1080x1350) and kit/short3d.py reels (1080x1920):
gradient background with glow and bokeh, shadowed text layers, pills, number badges, glass panels."""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from style import F, MINT, YEL, WHITE, GRAY, CORAL, BG

INK = (16, 28, 44); SOFT = (200, 212, 226)


def ease_out_back(x):
    x = min(max(x, 0), 1); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def ease(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


def background(seed, W=1080, H=1920, glow_y=0.38):
    y = np.linspace(0, 1, H)[:, None]; x = np.linspace(-1, 1, W)[None, :]
    top, bot = np.array([10, 18, 34]), np.array([20, 38, 62])
    img = top + (bot - top) * y[..., None]
    glow = np.exp(-((x * 0.9) ** 2 + ((y - glow_y) * 2.2) ** 2) * 2.2)[..., None] * np.array([26, 46, 60])
    vig = 1 - 0.45 * np.clip((x ** 2 + ((y - 0.5) * 1.6) ** 2) - 0.35, 0, 1)[..., None]
    bg = Image.fromarray(np.clip((img + glow) * vig, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    rng = np.random.default_rng(seed)
    bok = Image.new('RGBA', (W, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(bok)
    for _ in range(46):
        r = rng.uniform(6, 34); cx, cy = rng.uniform(0, W), rng.uniform(0, H * 2)
        col = [(109, 218, 197), (255, 196, 92), (140, 170, 255)][rng.integers(3)]
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*col, int(rng.uniform(18, 55))))
    bok = bok.filter(ImageFilter.GaussianBlur(7))
    return bg, bok


def text_layer(s, size, col, weight='Black', glow=None, shadow=True):
    f = F(weight, size); tmp = ImageDraw.Draw(Image.new('L', (1, 1)))
    w = int(tmp.textlength(s, font=f)) + 80; h = int(size * 1.5) + 60
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if shadow:
        sh = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((40, 36), s, font=f, fill=(0, 0, 0, 170))
        lay = Image.alpha_composite(lay, sh.filter(ImageFilter.GaussianBlur(6)))
    if glow:
        g = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(g).text((40, 30), s, font=f, fill=(*glow, 200))
        lay = Image.alpha_composite(lay, g.filter(ImageFilter.GaussianBlur(14)))
    ImageDraw.Draw(lay).text((40, 30), s, font=f, fill=col)
    return lay


def pill(s, size, fg, bg, pad=(26, 12)):
    f = F('Bold', size); tmp = ImageDraw.Draw(Image.new('L', (1, 1)))
    w = int(tmp.textlength(s, font=f)) + pad[0] * 2; h = int(size * 1.25) + pad[1] * 2
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=bg)
    d.text((pad[0], pad[1] - size * 0.08), s, font=f, fill=fg)
    return lay


def badge(n, r=40, col=(255, 196, 92)):
    lay = Image.new('RGBA', (r * 2 + 20, r * 2 + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse([12, 14, r * 2 + 12, r * 2 + 14], fill=(0, 0, 0, 110))
    d.ellipse([10, 10, r * 2 + 10, r * 2 + 10], fill=(*col, 255), outline=(255, 255, 255, 230), width=4)
    f = F('Black', int(r * 1.2)); s = str(n)
    d.text((r + 10 - d.textlength(s, font=f) / 2, r + 10 - r * 0.86), s, font=f, fill=(16, 28, 44))
    return lay


def put(fr, lay, cx, cy, scale=1.0, alpha=1.0):
    """Composite lay centred on (cx, cy) with scale and opacity."""
    if scale <= 0.01 or alpha <= 0.01: return
    if abs(scale - 1) > 0.01:
        lay = lay.resize((max(1, int(lay.width * scale)), max(1, int(lay.height * scale))), Image.BILINEAR)
    if alpha < 0.99:
        lay = lay.copy(); a = lay.getchannel('A').point(lambda v: int(v * alpha)); lay.putalpha(a)
    x, y = int(cx - lay.width / 2), int(cy - lay.height / 2)
    x0, y0 = max(0, -x), max(0, -y)
    if x0 or y0: lay = lay.crop((x0, y0, lay.width, lay.height)); x, y = x + x0, y + y0
    fr.alpha_composite(lay, (x, y))


def trim(im):
    return im.crop(im.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox())




def panel(w, h, r=36):
    p = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(p).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=(255, 255, 255, 16), outline=(255, 255, 255, 40), width=2)
    return p


def text_lines(fr, x, y, arr, size=38, col=WHITE, gap=1.55, weight='Bold', center=False):
    """arr items: str or (str, colour). Draws shadowed lines; x is the left edge, or the centre when center=True."""
    for i, s in enumerate(arr):
        c = col
        if isinstance(s, tuple): s, c = s
        lay = text_layer(s, size, c, weight)
        yy = y + i * size * gap
        if center: put(fr, lay, x, yy + lay.height / 2 - 30)
        else: fr.alpha_composite(lay, (int(x - 40), int(yy - 30)))


def sprite(path, width=None, height=None):
    im = trim(Image.open(path).convert('RGBA'))
    if width: im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    elif height: im = im.resize((round(im.width * height / im.height), height), Image.LANCZOS)
    return im


def card(room, date, n, total, title, sub, subcol=MINT, seed=None):
    """Blank 1080x1350 card. Content area about y=300..1150; cta() sits at y=1190."""
    W, H = 1080, 1350
    bg, bok = background(seed if seed is not None else room * 10 + n, W, H, 0.45)
    if os.environ.get('CARD_BG'):    # stock still (kit/stock.py), blurred and dimmed under the navy background
        ph = Image.open(os.environ['CARD_BG']).convert('RGB'); k = max(W / ph.width, H / ph.height)
        ph = ph.resize((round(ph.width * k), round(ph.height * k)), Image.LANCZOS)
        ph = ph.crop(((ph.width - W) // 2, (ph.height - H) // 2, (ph.width + W) // 2, (ph.height + H) // 2))
        ph = ImageEnhance.Color(ph.filter(ImageFilter.GaussianBlur(14))).enhance(0.85)
        bg = Image.blend(bg, ImageEnhance.Brightness(ph).enhance(0.92).convert('RGBA'), 0.55)
    fr = bg.copy(); fr.alpha_composite(bok.crop((0, (n * 377) % H, W, (n * 377) % H + H)))
    put(fr, pill(f'퇴근 후 사건파일  ·  ROOM {room:03d}', 26, SOFT, (255, 255, 255, 26)), 250, 70)
    pg = pill(f'{n:02d} / {total:02d}', 26, SOFT, (255, 255, 255, 26)); put(fr, pg, W - 66 - pg.width / 2, 70)
    fr.alpha_composite(text_layer(title, 62, WHITE), (26, 112))
    fr.alpha_composite(text_layer(sub, 34, subcol, 'Bold'), (26, 200))
    d = ImageDraw.Draw(fr); f = F('SemiBold', 24)
    s = f'{date}   ·   직접 풀어보는 방탈출'; d.text(((W - d.textlength(s, font=f)) / 2, 1298), s, font=f, fill=GRAY)
    return fr


def cta(fr, s, col=None):
    put(fr, pill(s, 34, INK, (*(col or MINT), 240), (34, 16)), 540, 1222)
