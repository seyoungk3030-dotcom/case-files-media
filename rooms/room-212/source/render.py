"""ROOM 212 cards (버스 창밖 빗줄기) in the 3D style (kit/style3d.py), from the bus-window sprites made by
scene3d.py, with each board's rain speed and slant written under it. All sprites are cropped to one shared box around the window frame
(q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS, GOOD
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 212, '2026.12.24'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
f = lambda x: str(int(x)) if x.denominator == 1 else f'{float(x):g}'
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
BOX = (62, 84, 846, 622)  # the window frame plus a thin strip of bus wall (sprites are opaque wall)
for n, im in ims.items():
    c = im.crop(BOX); k = n[1]; u, a, b = BOARDS[k]; out = Image.new('RGBA', (c.width, c.height + 200), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'옆 {a}칸 · 아래 {b}칸', WHITE), ('버스는 초속 몇 m?', YEL))
    else: lines = ((f'초속 {GOOD[k]} m (시속 {round(GOOD[k] * 3.6)} km)', MINT), (f'{u} × {a}/{b} = {GOOD[k]}', SOFT))
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

fr = card(ROOM, DATE, 1, 7, '버스 창밖 빗줄기', '빗줄기가 누울수록 버스는…?')
four(fr, 'q', 460)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '바람 없는 날, 비는 똑바로 떨어져요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['1. 버스는 오른쪽(→)으로 달려요', '2. 창밖 빗줄기가 비스듬히 보여요', '3. 빗방울은 모두 초속 6 m로 떨어져요',
                          '4. 버스는 초속 몇 m로 달릴까요?', ('A~D 버스 초속(m)이 각 자리 숫자', YEL)], 32)
one(fr, 'qA', 540, 880, 620, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 버스 초속(m)')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 초속 3 · 7 · 5 · 2 m라면', ('암호 3752', YEL), '', ('창의 격자 칸을 세어 보세요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '버스는 초속 몇 m?')
four(fr, 'q', 460)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '버스에서 보면 비가 뒤로 밀려 보여요', CORAL)
fr.alpha_composite(panel(960, 270), (60, 300))
text_lines(fr, 100, 330, [('옆으로 간 칸 ÷ 아래로 간 칸', WHITE), '= 버스 속도 ÷ 빗방울 속도', '빗줄기가 많이 누울수록 빠른 버스',
                          ('가파를수록 빠르다? 함정', YEL)], 34)
one(fr, 'qB', 540, 880, 620, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '노란 점선 = 옆 칸과 아래 칸')
four(fr, 'r', 460, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '기울기 = 버스 속도 ÷ 빗방울 속도')
one(fr, 'rB', 285, 560, 470, tag=False); one(fr, 'rD', 795, 560, 470, tag=False)
fr.alpha_composite(panel(960, 280), (60, 860))
text_lines(fr, 100, 885, ['A: 옆 1 / 아래 2 → 6 × 1/2 = 3', 'B: 옆 4 / 아래 3 → 6 × 4/3 = 8', 'D: 옆 3 / 아래 2 → 6 × 3/2 = 9'], 30)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
