import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *
from PIL import ImageFilter

ROOM, DATE, N = 20, '2026.10.18', 7
OUT = os.path.join(HERE, '..', 'cards')
ANS = '9856'
KEYS = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['*', '0', '#']]
HOT, MID, COLD = (255, 84, 64), (255, 168, 56), (150, 112, 92)
HEAT = {'6': HOT, '5': MID, '8': MID, '9': COLD}
GLOW = {'6': 230, '5': 150, '8': 150, '9': 105}


def keypad(im, top, size=140, gap=20, hl=None, path=None, order=None):
    """hl: {key: outline color}; path: list of keys to connect with arrows; order: {key: label} small badges."""
    d = ImageDraw.Draw(im)
    x0 = (W - (3 * size + 2 * gap)) // 2
    pos = {}
    glow = Image.new('RGBA', im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    for r, row in enumerate(KEYS):
        for c, k in enumerate(row):
            x, y = x0 + c * (size + gap), top + r * (size + gap)
            pos[k] = (x + size / 2, y + size / 2)
            if k in HEAT:
                g.ellipse([x - 18, y - 18, x + size + 18, y + size + 18], fill=HEAT[k] + (GLOW[k],))
    glow = glow.filter(ImageFilter.GaussianBlur(26))
    im.paste(glow, (0, 0), glow)
    d = ImageDraw.Draw(im)
    for r, row in enumerate(KEYS):
        for c, k in enumerate(row):
            x, y = x0 + c * (size + gap), top + r * (size + gap)
            out = (hl or {}).get(k)
            d.rounded_rectangle([x, y, x + size, y + size], radius=22, fill=CELL, outline=out or CELL_LINE, width=6 if out else 2)
            col = HEAT.get(k, DIM if k in '*#' else GRAY)
            f = F('Bold', int(size * 0.46))
            d.text((x + size / 2 - d.textlength(k, font=f) / 2, y + size / 2 - size * 0.32), k, font=f, fill=col)
            if order and k in order:
                d.ellipse([x + size - 32, y - 10, x + size + 10, y + 32], fill=MINT, outline=BG, width=3)
                f2 = F('Black', 26); s = order[k]
                d.text((x + size - 11 - d.textlength(s, font=f2) / 2, y - 6), s, font=f2, fill=BG)
    if path:
        for a, b in zip(path, path[1:]):
            (ax, ay), (bx, by) = pos[a], pos[b]
            dx, dy = bx - ax, by - ay; L = (dx * dx + dy * dy) ** .5; ux, uy = dx / L, dy / L
            sx, sy, ex, ey = ax + ux * size * 0.3, ay + uy * size * 0.36, bx - ux * size * 0.36, by - uy * size * 0.42
            d.line([sx, sy, ex, ey], fill=MINT, width=8)
            px, py = -uy, ux
            d.polygon([(ex + ux * 6, ey + uy * 6), (ex - ux * 22 + px * 14, ey - uy * 22 + py * 14),
                       (ex - ux * 22 - px * 14, ey - uy * 22 - py * 14)], fill=MINT)
    return top + 4 * size + 3 * gap


def legend(d, y):
    items = [(HOT, '가장 뜨거움'), (MID, '중간 (둘이 같음)'), (COLD, '가장 차가움')]
    x = 90
    for col, s in items:
        d.ellipse([x, y + 6, x + 30, y + 36], fill=col)
        f = F('SemiBold', 28)
        d.text((x + 42, y + 2), s, font=f, fill=WHITE)
        x += 42 + d.textlength(s, font=f) + 46


def card1():
    im, d = base(ROOM, DATE, 1, N, '열화상에 찍힌 도어록', '키패드에 남은 네 개의 온기.')
    bottom = keypad(im, 290, size=132, gap=18)
    d = ImageDraw.Draw(im)
    lines(d, 80, bottom + 34, ['누군가 방금 문을 열고 들어갔다.', '열화상 카메라에 네 개의 키만 따뜻하게 남았다.'], size=34, w='Bold')
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '온기의 규칙', '손가락의 열은 시간이 지나면 식습니다.')
    d.rounded_rectangle([66, 290, 1014, 545], radius=24, fill=PANEL)
    lines(d, 110, 325, ['① 마지막에 누른 키가 가장 뜨겁다', '② 처음 누른 키가 가장 차갑다', '③ 네 키를 한 번씩, 총 네 번 눌렀다'],
          size=36, w='Bold', gap=1.75)
    d.text((100, 610), '예시', font=F('Bold', 34), fill=YEL)
    lines(d, 100, 670, ['1 → 2 → 3 순서로 눌렀다면', '3이 가장 뜨겁고, 1이 가장 차갑다.', '',
                        ('그런데 온도가 같은 키가 둘이라면?', MINT)], size=34)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '암호 = 누른 순서', '첫 번째 → 두 번째 → 세 번째 → 네 번째.')
    keypad(im, 300, size=110, gap=16, order={'9': '?', '5': '?', '8': '?', '6': '?'})
    d = ImageDraw.Draw(im)
    lines(d, 80, 840, ['따뜻한 키 네 개를 누른 순서대로 이으면', '네 자리 암호가 됩니다.', ('같은 키를 두 번 누르지는 않았어요.', MINT)],
          size=34, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '규칙과 단서는 이것이 전부.')
    bottom = keypad(im, 280, size=112, gap=16)
    d = ImageDraw.Draw(im)
    legend(d, bottom + 24)
    d.rounded_rectangle([66, bottom + 84, 1014, bottom + 340], radius=22, fill=PANEL)
    lines(d, 96, bottom + 104, ['가장 뜨거운 키 = 마지막, 가장 차가운 키 = 처음', '네 키를 한 번씩, 총 네 번 눌렀다', '5와 8은 온도가 똑같아 구분이 안 된다',
                                ('민재: "손가락은 매번 상하좌우 바로 옆 키로', YEL), ('       갔어요. 대각선은 한 번도 없었어요."', YEL)],
          size=29, w='SemiBold', gap=1.45)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 함정 9586', '온도만 보면 답이 두 개.', subcol=CORAL)
    bottom = keypad(im, 290, size=118, gap=16, hl={'9': CORAL, '5': CORAL})
    d = ImageDraw.Draw(im)
    lines(d, 80, bottom + 30, ['처음은 9, 마지막은 6. 가운데는 5와 8.', '그런데 9에서 5로 가려면 대각선이다.',
                               ('9 바로 다음에 누를 수 있는 키는?', CORAL)], size=33, w='Bold')
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', '9 → 8 → 5 → 6.')
    bottom = keypad(im, 280, size=112, gap=16, path=list(ANS), order={'9': '1', '8': '2', '5': '3', '6': '4'})
    d = ImageDraw.Draw(im)
    lines(d, 76, bottom + 30, ['가장 차가운 9가 처음, 가장 뜨거운 6이 마지막.', '9의 상하좌우 이웃 중 따뜻한 키는 8뿐 → 두 번째는 8.',
                               '남은 5를 누르고 바로 옆 6으로. 암호는 9856.'], size=31)
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '식어가던 온기가 알려준 순서', '대각선 한 칸이 함정을 갈랐습니다.')
    bottom = keypad(im, 280, size=100, gap=14, path=list(ANS), order={'9': '1', '8': '2', '5': '3', '6': '4'})
    d = ImageDraw.Draw(im)
    big_answer(d, bottom + 20, ANS)
    lines(d, 80, bottom + 200, ['맞혔다면 좋아요 · 다음 방은 팔로우!', '9586에 속았다면 댓글로 고백해 주세요.'], size=32, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
