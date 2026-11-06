"""ROOM 070 cards in the 3D style (kit/style3d.py), from the sliding-tile sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 70, '2026.11.07'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']


def spr(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()
    im = im.crop((max(l - 10, 0), max(t - 10, 0), r + 10, b + 10)); sc = w / im.width
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag:
        put(fr, pill(name[1], 38, INK, (244, 246, 250, 245), (20, 6)), x0 - 4, y0 + 8)
        if val: put(fr, badge(val, 38), x0 + im.width + 4, y0 + 8)


def grid(fr, pre, y0, w=380, gap=380, vals=None, dx=480):
    for i, k in enumerate('ABCD'):
        spr(fr, pre + k, 540 - dx / 2 + (i % 2) * dx, y0 + (i // 2) * gap, w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'


def row(fr, pre, y, w, vals=None):
    for i, k in enumerate('ABCD'):
        spr(fr, pre + k, 165 + i * 250, y, w, val=vals[i] if vals else None)


fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '순서대로 밀면 민트 칸에는 몇 번?')
grid(fr, 'p', 507, 340, 420, dx=400)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '빈칸 옆 타일만 밀 수 있어요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 아래 동그라미 번호 순서대로', '2. 그 번호 타일을 옆 빈칸으로 밀어요',
                          '3. 다 밀고 나면 민트 테두리 칸에는', ('몇 번 타일이 있을까?', YEL)], 34)
spr(fr, 'pA', 540, 870, 440, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 민트 칸의 마지막 숫자')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 1 · B 5 · C 8 · D 2 타일이면', ('암호 1582', YEL), '',
                          ('지금 민트 칸 숫자를 읽으면 함정', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '번호 순서대로 밀기 · 암호 = 민트 칸 숫자')
grid(fr, 'p', 507, 340, 420, dx=400)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', f'지금 민트 칸을 읽으면 {PROOF["trap_star_before"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('밀 때마다 빈칸이 옮겨 가요', WHITE), '방금 민 타일이 있던 자리가', '새 빈칸이 돼요.',
                          ('빈칸을 따라가면 쉬워요!', YEL)], 35)
spr(fr, 'pC', 540, 902, 410, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '다 민 뒤의 모습 · 노란 타일이 민트 칸')
grid(fr, 'a', 507, 340, 420, list(CODE), dx=400)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 3 · B 1 · C 7 · D 6')
grid(fr, 'a', 490, 230, 300, list(CODE), dx=300)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 975)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
