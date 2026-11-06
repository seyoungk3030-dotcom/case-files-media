"""ROOM 075 cards in the 3D style (kit/style3d.py), from the bus sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 75, '2026.11.09'
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


def one(fr, name, cx, cy, w, tag=True, val=None, flip=False):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); im = im.crop(im.getchannel('A').getbbox())
    if flip: im = im.rotate(180)
    sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag:
        cy2 = y0 + im.height / 2
        put(fr, pill(name[1], 38, INK, (244, 246, 250, 245), (20, 6)), x0 - 45, cy2 - (38 if val else 0))
        if val: put(fr, badge(val, 40), x0 - 45, cy2 + 38)



YS = [420, 625, 830, 1035]


def four(fr, pre, w=660, vals=None, ys=YS):
    for i, k in enumerate('ABCD'): one(fr, pre + k, 580, ys[i], w, val=vals[i] if vals else None)


fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '버스는 어느 정류장으로 갈까요?')
four(fr, 'p')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '버스 옆모습만 보고 방향을 맞혀요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 버스는 앞뒤 모양이 똑같아요', '2. 한국 도로를 달리는 한국 버스예요',
                          '3. 버스는 양쪽 정류장 중 한 곳으로 가요', ('가는 쪽 정류장 번호는?', YEL)], 34)
one(fr, 'pB', 540, 850, 900, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 버스가 가는 정류장 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 260), (60, 700))
text_lines(fr, 540, 735, ['예: 1 · 2 · 3 · 4번 정류장으로 가면', ('암호 1234', YEL)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '버스 앞뒤는 똑같아요 · 한국 버스예요')
four(fr, 'p')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '버스 모양 말고 버스 문을 보세요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('한국 버스는 어느 쪽에 문이 있을까요?', WHITE), '승객은 인도 쪽에서 타요.', '한국은 오른쪽 차선으로 달려요.',
                          ('문이 안 보이면 반대쪽 옆면이에요!', YEL)], 35)
one(fr, 'pD', 540, 880, 900, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '문은 버스의 오른쪽 옆면에 있어요')
fr.alpha_composite(panel(960, 150), (60, 280))
text_lines(fr, 540, 298, ['문이 보이면 → 오른쪽으로', ('문이 안 보이면 → 왼쪽으로', YEL)], 32, center=True)
four(fr, 'a', w=580, vals=list(CODE), ys=[535, 715, 895, 1070])
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '문 쪽이 버스의 오른쪽!')
for i, k in enumerate('ABCD'): one(fr, 'a' + k, 320 + (i % 2) * 490, 450 + (i // 2) * 230, 370, val=CODE[i])
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 960)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
