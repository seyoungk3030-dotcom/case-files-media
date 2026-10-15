"""퇴근 후 사건파일 card style helpers. Cards are 1080x1350 PNG."""
import os
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
def F(w, s): return ImageFont.truetype(f'{KIT}/fonts/P-{w}.otf', s)

BG = (16, 28, 44); MINT = (109, 218, 197); YEL = (255, 196, 92); WHITE = (244, 244, 240)
GRAY = (160, 172, 188); DASH = (78, 94, 116); CORAL = (240, 128, 120); PANEL = (24, 40, 60)
CELL = (22, 37, 56); CELL_LINE = (70, 88, 112); DIM = (90, 104, 124)
W, H = 1080, 1350


def base(room, date, n, total, title, sub, subcol=MINT):
    """Blank card with header/title/subtitle/footer. Content area roughly y=280..1130; CTA at y=1160."""
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 12], fill=MINT)
    f = F('SemiBold', 28)
    d.text((66, 52), '퇴근 후 사건파일', font=f, fill=GRAY)
    d.text((66 + d.textlength('퇴근 후 사건파일', font=f) + 14, 52), f'/  ROOM {room:03d}', font=f, fill=GRAY)
    d.text((66, 122), title, font=F('Bold', 56), fill=WHITE)
    d.text((66, 204), sub, font=F('Bold', 30), fill=subcol)
    d.line([66, 1253, 1014, 1253], fill=(52, 66, 86), width=2)
    f = F('SemiBold', 24)
    d.text((66, 1284), f'{date}   ·   직접 풀어보는 방탈출', font=f, fill=GRAY)
    pg = f'{n:02d} / {total:02d}'
    d.text((1014 - d.textlength(pg, font=f), 1284), pg, font=f, fill=GRAY)
    return im, d


def ctext(d, y, s, col=MINT, font=None):
    font = font or F('Bold', 32)
    d.text(((W - d.textlength(s, font=font)) / 2, y), s, font=font, fill=col)


def lines(d, x, y, arr, size=32, col=WHITE, gap=1.55, w='SemiBold'):
    """arr items: str or (str, color). Keep each line under ~900px."""
    for i, s in enumerate(arr):
        c = col
        if isinstance(s, tuple): s, c = s
        d.text((x, y + i * size * gap), s, font=F(w, size), fill=c)


def cell(d, x0, y0, size, value=None, col=WHITE, fs=64):
    d.rounded_rectangle([x0 + 8, y0 + 8, x0 + size - 8, y0 + size - 8], radius=14, fill=CELL, outline=CELL_LINE, width=2)
    if value is not None:
        f = F('Bold', fs); s = str(value)
        d.text((x0 + size / 2 - d.textlength(s, font=f) / 2, y0 + size / 2 - fs * 0.62), s, font=f, fill=col)


def big_answer(d, y, code, col=MINT):
    ctext(d, y, ' '.join(code), col=col, font=F('Black', 120))


CTA_START = '도전 → 4장까지 / 정답 → {a}장'
CTA_SOLVE = '4장까지 풀고 댓글에 암호를 남겨주세요'
CTA_HINT = '다음 장부터 정답 · 먼저 멈춰서 풀어보세요'
