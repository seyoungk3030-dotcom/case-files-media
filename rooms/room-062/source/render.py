"""ROOM 062 cards in the 3D style (kit/style3d.py), from the lock and key sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 62, '2026.11.04'
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


fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '자물쇠마다 열쇠 세 개, 맞는 열쇠는?')
row(fr, 'p', 730, 245)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '열쇠를 꽂으면 톱니가 핀을 밀어 올린다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 핀은 그 아래 톱니 높이만큼 올라간다', '2. 다섯 핀의 윗면이 모두 노란 선에 맞으면 열린다',
                          ('3. 맞는 열쇠는 판마다 딱 하나', YEL)], 34)
spr(fr, 'pA', 540, 850, 300, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 맞는 열쇠의 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 1번 · B 5번 · C 8번 · D 3번 열쇠라면', ('암호 1583', YEL), '',
                          ('열쇠 번호는 손잡이 고리 안에 있어요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
row(fr, 'p', 640, 245)
fr.alpha_composite(panel(960, 110), (60, 925))
text_lines(fr, 540, 943, ['핀 윗면이 모두 노란 선에 맞아야 열린다', ('암호 = 맞는 열쇠 번호 A B C D', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', f'핀 모양을 닮은 열쇠를 고르면 {PROOF["trap_teeth_copy_pins"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('긴 핀 밑에는 낮은 톱니가 와야 해요.', WHITE), '핀 길이 + 톱니 높이가', '다섯 칸 모두 똑같아야 해요.',
                          ('핀과 똑같이 생긴 열쇠는 반대예요', YEL)], 35)
spr(fr, 'pB', 540, 880, 250, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '맞는 열쇠를 꽂으면 핀이 노란 선에 딱')
fr.alpha_composite(panel(960, 160), (60, 280))
text_lines(fr, 540, 300, ['핀 길이 + 톱니 높이 = 5칸', ('A 7번 · B 2번 · C 9번 · D 4번', YEL)], 31, center=True)
grid(fr, 'a', 640, 380, 320, list(CODE), dx=480)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 7 · B 2 · C 9 · D 4')
grid(fr, 'a', 450, 300, 250, list(CODE), dx=400)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 975)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
