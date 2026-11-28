"""ROOM 214 cards (주사위 두 개) in the 3D style (kit/style3d.py), from the dice sprites made by
scene3d.py, with each board's target sum written under it. All sprites are cropped to one shared box around the window frame
(q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS, GOOD, SHOW
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 214, '2026.12.25'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
f = lambda x: str(int(x)) if x.denominator == 1 else f'{float(x):g}'
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 6, min(b[1] for b in bb) - 6, max(b[2] for b in bb) + 6, max(b[3] for b in bb) + 6)
for n, im in ims.items():
    c = im.crop(BOX); k = n[1]; S = BOARDS[k]; r0, b0 = SHOW[k]; out = Image.new('RGBA', (c.width, c.height + 200), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'합이 {S}', WHITE), ('몇 가지일까?', YEL))
    else: lines = ((f'{GOOD[k]}가지', MINT), ('빨강·파랑 순서까지', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 78 if j == 0 else 70, col), c.width / 2, c.height + 56 + j * 96)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 30, y0 + 30)
    if val: put(fr, badge(val, 46), x0 + im.width - 50, y0 + 44)


POS = [(285, 518), (795, 518), (285, 952), (795, 952)]


def four(fr, pre, w=500, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '주사위 두 개', '4+5와 5+4는 같은 경우일까요?')
four(fr, 'q', 460)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '빨강 주사위와 파랑 주사위를 함께 던져요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['1. 두 주사위 윗면 숫자를 더해요', '2. 그림은 그 합이 나온 한 가지 예예요', '3. 그 합이 나오는 경우는 모두 몇 가지?',
                          '4. 주사위 색이 달라요 (빨강 · 파랑)', ('A~D 경우의 수가 각 자리 숫자', YEL)], 32)
one(fr, 'qA', 540, 880, 640, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 경우의 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 3 · 7 · 5 · 2가지라면', ('암호 3752', YEL), '', ('빨강 몇, 파랑 몇으로 적어 보세요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '그 합이 나오는 경우는 몇 가지?')
four(fr, 'q', 460)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '빨강 4 · 파랑 5 ≠ 빨강 5 · 파랑 4', CORAL)
fr.alpha_composite(panel(960, 270), (60, 300))
text_lines(fr, 100, 330, [('두 주사위는 서로 다른 주사위예요', WHITE), '빨강을 1부터 6까지 바꿔 가며', '파랑이 맞는 숫자인지 세어 보세요',
                          ('4+5와 5+4를 하나로 센다? 함정', YEL)], 34)
one(fr, 'qC', 540, 880, 640, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '그 합이 나오는 모든 경우')
four(fr, 'r', 460, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '합 7이 6가지로 가장 자주 나와요')
one(fr, 'rC', 285, 560, 470, tag=False); one(fr, 'rA', 795, 560, 470, tag=False)
fr.alpha_composite(panel(960, 280), (60, 860))
text_lines(fr, 100, 885, ['A 합 9: 3+6 6+3 4+5 5+4 → 4가지', 'B 합 3: 1+2 2+1 → 2가지', 'D 합 10: 4+6 6+4 5+5 → 3가지'], 30)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
