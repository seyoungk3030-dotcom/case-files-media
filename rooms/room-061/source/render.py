"""ROOM 061 cards in the 3D style (kit/style3d.py), from the transparent film sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 61, '2026.11.04'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']


def spr(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()
    im = im.crop((max(l - 10, 0), max(t - 10, 0), r + 10, b + 10)); sc = w / im.width
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag:
        put(fr, pill(name[1], 38, INK, (244, 246, 250, 245), (20, 6)), x0 + 12, y0 + im.height - 40)
        if val: put(fr, badge(val, 38), x0 + 82, y0 + im.height - 40)


def grid(fr, pre, y0, w=380, gap=380, vals=None, dx=480):
    for i, k in enumerate('ABCD'):
        spr(fr, pre + k, 540 - dx / 2 + (i % 2) * dx, y0 + (i // 2) * gap, w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '오른쪽 필름을 뒤집어 겹치면 어떤 숫자?')
grid(fr, 'p', 640, 440, 330, dx=500)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '투명 필름이라 겹치면 네모가 합쳐진다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 오른쪽 필름을 좌우로 뒤집는다', '2. 뒤집은 필름을 왼쪽 필름 위에 그대로 겹친다',
                          ('3. 민트 + 코랄 네모가 만드는 숫자는?', YEL)], 34)
spr(fr, 'pA', 540, 830, 760, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 겹쳐서 보이는 숫자')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 1 · B 7 · C 4 · D 0 이 보였다면', ('암호 1740', YEL), '',
                          ('뒤집지 않으면 다른 숫자가 보여요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
grid(fr, 'p', 520, 400, 300, dx=500)
fr.alpha_composite(panel(960, 110), (60, 985))
text_lines(fr, 540, 1003, ['오른쪽 필름 = 좌우로 뒤집어서 겹친다', ('암호 = 겹쳐서 보이는 숫자 A B C D', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', f'뒤집지 않고 겹치면 {PROOF["trap_no_flip"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('좌우로 뒤집으면 왼쪽 칸과 오른쪽 칸이', WHITE), '서로 자리를 바꿔요.', '가운데 줄은 그대로예요.',
                          ('맨 오른쪽 코랄 네모 → 맨 왼쪽으로', YEL)], 35)
spr(fr, 'pC', 540, 900, 700, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '뒤집어 겹친 필름에 보이는 숫자')
fr.alpha_composite(panel(960, 160), (60, 280))
text_lines(fr, 540, 300, ['민트 = 왼쪽 필름 · 코랄 = 뒤집은 오른쪽 필름', ('A 6 · B 8 · C 2 · D 9', YEL)], 31, center=True)
for i, k in enumerate('ABCD'):
    spr(fr, 'a' + k, 165 + i * 250, 780, 220, val=CODE[i])
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 6 · B 8 · C 2 · D 9')
for i, k in enumerate('ABCD'):
    spr(fr, 'a' + k, 165 + i * 250, 640, 220, val=CODE[i])
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 975)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
