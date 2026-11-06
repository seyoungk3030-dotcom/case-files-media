"""ROOM 069 cards in the 3D style (kit/style3d.py), from the cup-stack sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 69, '2026.11.07'
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


fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '가려진 컵 더미는 몇 칸 높이?')
grid(fr, 'p', 507, 400, 420, dx=430)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '컵은 모두 똑같아요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 똑같은 컵을 포개어 쌓았어요', '2. 두 더미는 높이가 적혀 있어요',
                          '3. 상자 속에 적힌 개수만큼 쌓으면', ('높이는 몇 칸일까?', YEL)], 34)
spr(fr, 'pA', 540, 870, 520, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 가려진 더미의 높이')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 1칸 · B 5칸 · C 8칸 · D 2칸이면', ('암호 1582', YEL), '',
                          ('컵 개수에 비례한다고 생각하면 함정', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '똑같은 컵 · 암호 = 가려진 더미의 높이')
grid(fr, 'p', 507, 400, 420, dx=430)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', '2개가 4칸이니 1개는 2칸? 아니에요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('컵은 포개지니까 겹쳐요', WHITE), '한 개 더 쌓을 때마다 늘어나는 건', '컵 테두리 높이뿐이에요.',
                          ('두 더미의 차이로 테두리를 구해요!', YEL)], 35)
spr(fr, 'pB', 540, 900, 500, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '높이 = 컵 1개 + 테두리 × (개수 - 1)')
fr.alpha_composite(panel(960, 160), (60, 280))
text_lines(fr, 540, 300, ['A 3+1×4=7 · B 4+2×1=6', ('C 5+1×3=8 · D 2+1×1=3', YEL)], 31, center=True)
grid(fr, 'a', 660, 330, 345, list(CODE), dx=400)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 7 · B 6 · C 8 · D 3')
grid(fr, 'a', 490, 260, 290, list(CODE), dx=320)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 975)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
