"""ROOM 211 cards (호스 끝을 손가락으로 막으면) in the 3D style (kit/style3d.py), from the hose sprites with an end-on inset made by
scene3d.py, with each board's flow and opening written under it. All sprites are cropped to one shared box
(q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS, GOOD
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 211, '2026.12.24'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
f = lambda x: str(int(x)) if x.denominator == 1 else f'{float(x):g}'
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 16, min(b[1] for b in bb) - 16, max(b[2] for b in bb) + 16, max(b[3] for b in bb) + 6)
BOX = (BOX[0], BOX[1] - 250, BOX[2], BOX[3])
for n, im in ims.items():
    c = im.crop(BOX).copy(); k = n[1]; lb, q, a, th = BOARDS[k]
    e = Image.open(f'{B}/e{k}.png').convert('RGBA'); e = e.crop(e.getchannel('A').getbbox()); e = e.resize((int(e.width * 250 / e.height), 250), Image.LANCZOS)
    c.alpha_composite(e, (int(c.width * 0.42), 4)); out = Image.new('RGBA', (c.width, c.height + 170), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    A = f'{float(a):g}'
    if n[0] == 'p': lines = ((f'1분에 {q} L · 구멍 {A} cm²', WHITE), (f'{lb} → 물줄기 속도는?', YEL))
    else: lines = ((f'초속 {GOOD[k]} m', MINT), (f'{q * 1000 // 60} ÷ {A} = {GOOD[k] * 100} cm/s', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 70 if j == 0 else 62, col), c.width / 2, c.height + 50 + j * 86)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 30, y0 + 30)
    if val: put(fr, badge(val, 46), x0 + im.width - 50, y0 + 50)


POS = [(285, 500), (795, 500), (285, 900), (795, 900)]


def four(fr, pre, w=500, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '호스 끝을 손가락으로 막으면?', '물이 덜 나오니 느려질까요?')
four(fr, 'q', 500)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '마당 호스를 1 m 높이에서 수평으로 들어요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['1. 1분에 나오는 물의 양(L)은 수도꼭지가 정해요', '2. 위의 동그란 그림 = 호스 끝을 정면에서 본 모습', '3. 손가락으로 막으면 구멍 넓이만 줄어요',
                          '4. 물줄기는 초속 몇 m로 나갈까요?', ('A~D 초속(m)이 각 자리 숫자', YEL)], 32)
one(fr, 'qB', 540, 860, 700, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 물줄기 초속')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 초속 5 · 1 · 6 · 2 m라면', ('암호 5162', YEL), '', ('막으면 느려질까, 빨라질까?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '물줄기는 초속 몇 m?')
four(fr, 'q', 500)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '들어온 물은 다 나가야 해요', CORAL)
fr.alpha_composite(panel(960, 270), (60, 300))
text_lines(fr, 100, 330, [('1분에 12 L = 1초에 200 cm³', WHITE), '속도 = 1초에 나가는 양 ÷ 구멍 넓이', '구멍이 4분의 1이면 4배 빨라야 다 나가요',
                          ('막으면 물이 약해진다? 함정', YEL)], 34)
one(fr, 'qD', 540, 860, 700, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '빠를수록 멀리 날아가요 (민트 = 떨어진 곳)')
four(fr, 'r', 500, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '속도 = 물의 양 ÷ 구멍 넓이')
one(fr, 'rA', 285, 560, 500, tag=False); one(fr, 'rD', 795, 560, 500, tag=False)
fr.alpha_composite(panel(960, 280), (60, 860))
text_lines(fr, 100, 885, ['A: 200 cm³/s ÷ 2 cm² = 100 cm/s = 초속 1 m', 'B: 구멍 0.5 cm² → 400 cm/s = 초속 4 m', 'D: 구멍 0.25 cm² → 800 cm/s = 초속 8 m'], 30)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
