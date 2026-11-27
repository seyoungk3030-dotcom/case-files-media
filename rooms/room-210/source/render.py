"""ROOM 210 cards (빗물은 몇 cm?) in the 3D style (kit/style3d.py), from the container sprites made by
scene3d.py, with each board's container and rain written under it. All sprites are cropped to one shared box
(q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS, GOOD
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 210, '2026.12.23'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
f = lambda x: str(int(x)) if x.denominator == 1 else f'{float(x):g}'
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
crops = {}
for n, im in ims.items():
    b = im.getchannel('A').getbbox(); crops[n] = im.crop((b[0] - 16, b[1] - 16, b[2] + 16, b[3] + 6))
CW, CH = max(c.width for c in crops.values()), max(c.height for c in crops.values())
for n, c0 in crops.items():
    c = Image.new('RGBA', (CW, CH)); c.alpha_composite(c0, ((CW - c0.width) // 2, CH - c0.height))
    k = n[1]; nm, kind, D0, D1, rain, h = BOARDS[k]; out = Image.new('RGBA', (c.width, c.height + 200), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    sz = {'A': '대야 지름 40 cm', 'B': '컵 지름 6 cm', 'C': '깔때기 10 → 관 5 cm', 'D': '병 입구 6 · 몸통 12 cm'}[k]
    if n[0] == 'p': lines = ((sz, WHITE), (f'비 {rain} cm → 물은 몇 cm?', YEL))
    else: lines = ((f'물 {GOOD[k]} cm', MINT), (f'{rain} × ({D0}/{D1})² = {GOOD[k]}' if kind != 'straight' else f'곧은 벽 = 비 {rain} cm', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 62 if j == 0 else 58, col), c.width / 2, c.height + 50 + j * 84)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 30, y0 + 30)
    if val: put(fr, badge(val, 46), x0 + im.width * 0.5, y0 + 40)


POS = [(290, 490), (790, 490), (290, 930), (790, 930)]


def four(fr, pre, w=500, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
W4 = 320

fr = card(ROOM, DATE, 1, 7, '빗물은 몇 cm?', '넓은 대야에 더 깊이 고일까요?')
four(fr, 'q', W4)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '마당에 그릇을 두고 비를 받아요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['1. 비 3 cm = 땅 어디에나 물이 3 cm 쌓일 만큼', '2. 빗물은 입구로만 들어가요 (넘치지 않아요)', '3. 깔때기 물은 아래 관으로 다 흘러내려요',
                          '4. 그릇에 고인 물 높이는 몇 cm?', ('A~D 물 높이(cm)가 각 자리 숫자', YEL)], 32)
one(fr, 'qC', 540, 870, 430, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 물 높이')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 5 cm · 1 cm · 6 cm · 2 cm라면', ('암호 5162', YEL), '', ('넓은 대야가 빗물을 더 많이 받으니 더 깊을까요?', SOFT)], 34, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '고인 물은 몇 cm?')
four(fr, 'q', W4)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '받는 넓이 ÷ 고이는 넓이', CORAL)
fr.alpha_composite(panel(960, 270), (60, 300))
text_lines(fr, 100, 330, [('넓게 받으면 넓게 퍼져요 → 곧은 벽은 비 온 만큼', WHITE), '입구 지름이 2배면 넓이는 4배', '좁은 곳으로 모이면 그만큼 깊어져요',
                          ('대야가 더 깊다? 함정', YEL)], 34)
one(fr, 'qA', 540, 870, 430, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 선 = 고인 물 높이')
four(fr, 'r', W4, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '대야도 컵도 비 온 만큼만 차요')
one(fr, 'rA', 290, 560, 380, tag=False); one(fr, 'rB', 790, 560, 380, tag=False)
fr.alpha_composite(panel(960, 280), (60, 860))
text_lines(fr, 100, 885, ['A, B: 곧은 벽이면 넓든 좁든 3 cm', 'C: 지름 10 → 5, 넓이 4배로 모여 2 × 4 = 8 cm', 'D: 입구 6, 몸통 12 → 4 ÷ 4 = 1 cm'], 30)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
