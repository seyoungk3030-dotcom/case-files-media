"""ROOM 189 cards (달군 고리) in the 3D style (kit/style3d.py), from the ring-and-balls sprites made by scene3d.py, with each board's hole size and heating/cooling step written under it. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 189, '2026.12.16'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_hole_shrinks_when_heated']; AFTER = PROOF['hole_after_mm']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    hole, sg, balls = BOARDS[n[1]]; out = Image.new('RGBA', (c.width, c.height + 190), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'구멍 {hole}mm', WHITE), ('→ 빨갛게 달굼' if sg > 0 else '→ 상온으로 식힘', (255, 140, 60) if sg > 0 else (150, 190, 255)))
    else: a = float(AFTER[n[1]]); lines = ((f'구멍 {a:g}mm' if abs(a * 10 - round(a * 10)) < 1e-9 else f'구멍 약 {round(a)}mm', MINT), (f'{"달군 뒤" if sg > 0 else "식힌 뒤"}', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 60 if j == 0 else 50, col), c.width / 2, c.height + 62 + j * 72)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 40, y0 + 36)
    if val: put(fr, badge(val, 46), x0 + im.width - 44, y0 + 40)


POS = [(290, 510), (790, 510), (290, 945), (790, 945)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '달군 고리', '빨갛게 달구면 구멍은 어떻게 될까요?')
four(fr, 'q', 420)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '고리 규칙', '쇠고리와 쇠구슬, 전부 같은 쇠예요')
fr.alpha_composite(panel(960, 360), (60, 290))
text_lines(fr, 100, 322, ['1. 빨갛게 달군 쇠는 모든 길이가 1% 커져요', '2. 다시 식으면 원래 크기로 돌아와요', '3. 구슬은 계속 상온, 숫자는 지름(mm)이에요',
                          '4. 구슬 지름이 구멍보다 작아야 통과해요', ('달군(식힌) 뒤 통과하는 구슬은 몇 개?', YEL)], 33)
one(fr, 'qA', 540, 960, 430, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 통과하는 구슬 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2개 · 0개 · 4개 · 1개면', ('암호 2041', YEL), '', ('구멍은 빈 공간인데, 같이 변할까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '달구면 길이 +1% · 식히면 원래대로')
four(fr, 'q', 420)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '쇠가 늘어나면 구멍 쪽으로 밀려들까요?', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('고리는 사진을 확대하듯 통째로 커져요', WHITE), '바깥 둘레도, 안쪽 둘레도 똑같이 1% 길어져요.', '안쪽 둘레가 길어지면 구멍도 커져요.',
                          (f'구멍이 줄어든다고 보면 함정 {TRAP}', YEL)], 35)
one(fr, 'qA', 540, 930, 400, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '달구면 구멍도 커지고, 식히면 작아져요')
four(fr, 'r', 420, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '구멍도 고리와 같이 커져요')
one(fr, 'rA', 300, 600, 430, tag=False); one(fr, 'rB', 790, 600, 430, tag=False)
fr.alpha_composite(panel(960, 260), (60, 900))
text_lines(fr, 100, 925, ['A: 구멍 100 → 101mm, 98.5 · 99.5 · 100.5 통과', 'B: 100 ÷ 1.01 ≈ 99mm, 98.5만 통과'], 31)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
