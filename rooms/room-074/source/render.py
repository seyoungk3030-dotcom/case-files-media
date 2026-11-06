"""ROOM 074 cards in the 3D style (kit/style3d.py), from the desk sprite made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 74, '2026.11.08'
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






def one(fr, cx, cy, w):
    im = Image.open(f'{B}/pA.png').convert('RGBA'); im = im.crop(im.getchannel('A').getbbox())
    sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


Q = '9는 몇 개? 6은? 8은? 0은?'
fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '책상 위에 보이는 숫자를 세어 보세요')
one(fr, 540, 690, 960)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '보이는 숫자를 하나하나 세요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 숫자 한 글자마다 1개로 세요', '2. 한 화면에 두 번 나오면 2개',
                          '3. 쉼표, 쌍점(:), 글자는 숫자가 아니에요', ('A=9 · B=6 · C=8 · D=0 의 개수', YEL)], 34)
one(fr, 540, 860, 720)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A 9의 개수 · B 6의 개수 · C 8의 개수 · D 0의 개수')
for n, (k, d) in enumerate(zip('ABCD', '9680')):
    cx = 165 + n * 250; put(fr, pill(f'{k}  {d}', 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 9가 1개, 6이 5개, 8이 8개, 0이 2개면', ('암호 1582', YEL), '',
                          ('물건 개수를 세면 함정', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', Q)
one(fr, 540, 690, 960)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', f'물건 개수를 세면 {PROOF["trap_objects_with_digit"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('9696 계산기에는 9가 2개, 6도 2개', WHITE), '8,990원에는 9가 2개, 0이 1개.', '시계의 1도 놓치지 마세요.',
                          ('물건 말고 숫자를 세요!', YEL)], 35)
one(fr, 540, 900, 640)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '물건마다 숫자를 하나씩')
fr.alpha_composite(panel(960, 560), (60, 300))
text_lines(fr, 100, 330, ['11:59  →  9 하나', '9696  →  9 둘, 6 둘', '29  →  9 하나', '8,990원  →  9 둘, 8 하나, 0 하나',
                          '6610  →  6 둘, 0 하나', '88  →  8 둘'], 36)
text_lines(fr, 540, 920, [('9는 6개 · 6은 4개 · 8은 3개 · 0은 2개', YEL)], 38, center=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 6 · B 4 · C 3 · D 2')
one(fr, 540, 600, 640)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 960)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
