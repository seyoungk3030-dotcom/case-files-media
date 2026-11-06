"""ROOM 073 cards in the 3D style (kit/style3d.py), from the parking-lot sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 73, '2026.11.08'
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
        put(fr, pill(name[1], 38, INK, (244, 246, 250, 245), (20, 6)), x0 + 4, y0 + 4)
        if val: put(fr, badge(val, 40), x0 + 80, y0 + 4)


fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '자동차가 가린 주차 칸 번호는?')
one(fr, 'pA', 540, 560, 860); one(fr, 'pB', 540, 985, 860)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '주차장 바닥에 번호가 칠해져 있어요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 칸 번호는 하나씩 차례로 늘어나요', '2. 빨간 차가 한 칸을 가렸어요',
                          '3. 수식이나 패턴 계산은 필요 없어요', ('가린 칸의 번호는?', YEL)], 34)
one(fr, 'pA', 540, 860, 900, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A 칸 번호 두 자리 + B 칸 번호 두 자리')
for n, k in enumerate(['A', 'A', 'B', 'B']):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A가 15번, B가 82번이면', ('암호 1582', YEL), '',
                          ('한 자리 번호는 앞에 0을 붙여요 (예: 05)', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '번호는 하나씩 늘어나요 · 암호 = A 두 자리 + B 두 자리')
one(fr, 'pA', 540, 560, 860); one(fr, 'pB', 540, 985, 860)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '숫자를 계산하지 말고 보는 방향을 바꿔요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('이 번호는 누구를 위해 칠해졌을까요?', WHITE), '차는 반대편에서 들어와요.', '운전석에서 보면 어떻게 보일까요?',
                          ('휴대폰을 거꾸로 돌려 보세요!', YEL)], 35)
one(fr, 'pB', 540, 900, 900, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '운전석에서 보면 (화면을 180도 돌린 모습)')
fr.alpha_composite(panel(960, 160), (60, 280))
text_lines(fr, 540, 300, ['A 66 · 67 · 68 · 69', ('B 06 · 07 · 08 · 09 · 10 · 11', YEL)], 31, center=True)
one(fr, 'aA', 540, 645, 640, val='67', flip=True); one(fr, 'aB', 540, 1005, 680, val='07', flip=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 67번 · B 07번')
one(fr, 'aA', 540, 470, 600, val='67', flip=True); one(fr, 'aB', 540, 760, 600, val='07', flip=True)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 960)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
