"""ROOM 072 cards in the 3D style (kit/style3d.py), from the block-well sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 72, '2026.11.08'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']


def spr(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()
    im = im.crop((max(l - 10, 0), max(t - 10, 0), r + 10, b + 10)); sc = w / im.width
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag:
        put(fr, pill(name[1], 38, INK, (244, 246, 250, 245), (20, 6)), x0 + 12, y0 + 20)
        if val: put(fr, badge(val, 38), x0 + 82, y0 + 20)


def grid(fr, pre, y0, w=380, gap=380, vals=None, dx=480):
    for i, k in enumerate('ABCD'):
        spr(fr, pre + k, 540 - dx / 2 + (i % 2) * dx, y0 + (i // 2) * gap, w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'


def row(fr, pre, y, w, vals=None):
    for i, k in enumerate('ABCD'):
        spr(fr, pre + k, 165 + i * 250, y, w, val=vals[i] if vals else None)




BOX = (60, 45, 640, 990)


def normalise():
    for k in 'ABCD':
        for pre in 'pa':
            p = f'{B}/{pre}{k}.png'; im = Image.open(p).convert('RGBA')
            if im.size != (700, 1000): continue
            im = im.crop(BOX)
            for xy in ((0, 0), (im.width - 1, im.height - 1)): im.putpixel(xy, (20, 30, 50, 44))
            im.save(p)


normalise()


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); sc = w / im.width
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag:
        put(fr, pill(name[1], 38, INK, (244, 246, 250, 245), (20, 6)), cx - w * 0.22, y0 - 26)
        if val: put(fr, badge(val, 34), cx + w * 0.22, y0 - 26)


def row(fr, pre, cy, w, vals=None, gap=262):
    for i, k in enumerate('ABCD'):
        one(fr, pre + k, 540 + (i - 1.5) * gap, cy, w, val=vals[i] if vals else None)


fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '조각을 떨어뜨리면 블록은 몇 개 남을까?')
row(fr, 'p', 740, 250)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '조각은 돌리지 않고 그대로 떨어져요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 주황 조각이 화살표대로 곧장 떨어져요', '2. 처음 닿는 곳에 멈춰요',
                          '3. 가로줄이 꽉 차면 그 줄은 사라지고', ('남은 블록은 몇 개?', YEL)], 34)
one(fr, 'pB', 540, 880, 300, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 남은 블록 개수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 1개 · B 5개 · C 8개 · D 2개면', ('암호 1582', YEL), '',
                          ('줄 지우기를 잊으면 함정', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '꽉 찬 줄은 사라져요 · 암호 = 남은 블록 수')
row(fr, 'p', 740, 250)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', '조각이 걸리는 곳을 잘 보세요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('조각은 어느 한 칸이라도 닿으면 멈춰요', WHITE), '빈 구멍이 있어도 위가 막히면 못 들어가요.', '꽉 찬 줄은 5개씩 사라져요.',
                          ('남은 블록만 세면 끝!', YEL)], 35)
one(fr, 'pD', 540, 915, 290, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '떨어진 뒤 꽉 찬 줄을 지운 모습')
fr.alpha_composite(panel(960, 160), (60, 280))
text_lines(fr, 540, 300, ['A 12-5=7 · B 12-10=2', ('C 14-10=4 · D 13-5=8', YEL)], 31, center=True)
row(fr, 'a', 810, 230, list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 7 · B 2 · C 4 · D 8')
row(fr, 'a', 600, 170, list(CODE), gap=200)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 960)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
