"""ROOM 060 cards in the 3D style (kit/style3d.py), from the domino sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 60, '2026.11.04'
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
fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '맨 아래 도미노를 밀면 어느 종이 울릴까?')
grid(fr, 'p', 590, 305, 370, dx=460)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '도미노는 바로 옆 도미노만 넘어뜨린다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 맨 아래 민트 화살표 도미노를 민다', '2. 도미노가 빠진 빈틈에서는 멈춘다',
                          ('3. 갈림길·옆길로는 모든 방향으로 이어진다', YEL)], 34)
spr(fr, 'pA', 540, 860, 520, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 울리는 종의 숫자')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 2 · B 6 · C 1 · D 3 종이 울렸다면', ('암호 2613', YEL), '',
                          ('판마다 울리는 종은 딱 하나예요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
grid(fr, 'p', 470, 265, 315, dx=440)
fr.alpha_composite(panel(960, 110), (60, 975))
text_lines(fr, 540, 993, ['빈틈 = 멈춤 · 옆길 = 이어짐', ('암호 = 울리는 종의 숫자 A B C D', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', f'정면 종을 고르면 {PROOF["trap_straight_ahead"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('가운데 길에 빈틈이 있는지 먼저 보세요.', WHITE), '막히면 넘어진 도미노가', '옆길을 타고 돌아가요.',
                          ('C는 옆길을 두 번 건너요', YEL)], 35)
spr(fr, 'pC', 540, 920, 380, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '넘어진 도미노를 따라가면 울리는 종')
fr.alpha_composite(panel(960, 160), (60, 280))
text_lines(fr, 540, 300, ['A 왼쪽 4 · B 가운데 막힘 → 오른쪽 9', ('C 옆길 두 번 → 5 · D 옆길 → 왼쪽 7', YEL)], 31, center=True)
grid(fr, 'a', 600, 260, 310, list(CODE), dx=440)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 4 · B 9 · C 5 · D 7')
grid(fr, 'a', 480, 260, 300, list(CODE), dx=360)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 975)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
