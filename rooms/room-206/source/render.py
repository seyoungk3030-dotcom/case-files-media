"""ROOM 206 cards (배에서 돌을 던지면?) in the 3D style (kit/style3d.py), from the side-view sprites made by scene3d.py, with each
board's speed and the sticker's ground speed written under it. All sprites are cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 206, '2026.12.22'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; DROP = PROOF['drop_mm']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 20, min(b[1] for b in bb) - 20, max(b[2] for b in bb) + 20, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); k = n[1]; nm, V, rho = BOARDS[k]; g = int(V * rho); out = Image.new('RGBA', (c.width, c.height + 150), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'{nm} {V} cm³ · {g} g', WHITE), ('물에 던지면 물 높이는?', YEL))
    else: lines = ((f'{DROP[k]} mm 내려감' if DROP[k] else '그대로 (뜨니까)', MINT), (f'{g} cm³ → {V if rho > 1 else g} cm³', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 62 if j == 0 else 54, col), c.width / 2, c.height + 48 + j * 76)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 30, y0 + 30)
    if val: put(fr, badge(val, 46), x0 + im.width - 40, y0 + im.height * 0.42)


POS = [(300, 505), (780, 505), (300, 945), (780, 945)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '배에서 돌을 던지면?', '첨벙! 물이 올라갈까요?')
four(fr, 'q', 360)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '수조 안에 장난감 배가 떠 있어요')
fr.alpha_composite(panel(960, 420), (60, 290))
text_lines(fr, 100, 322, ['1. 수조 바닥은 가로 20 cm × 세로 20 cm', '2. 배 위의 물건을 물속으로 던져요', '3. 물은 1 cm³에 1 g, 배는 계속 떠 있어요',
                          '4. 수조 물 높이는 몇 mm 내려갈까요?', ('A~D 내려간 mm가 각 자리 숫자 (그대로면 0)', YEL)], 32)
one(fr, 'qA', 540, 930, 360, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 내려간 mm')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2 mm · 5 mm · 0 · 4 mm라면', ('암호 2504', YEL), '', ('던지면 물이 올라갈까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '물 높이는 몇 mm 내려갈까?')
four(fr, 'q', 360)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '떠 있는 배는 무게만큼 물을 밀어내요', CORAL)
fr.alpha_composite(panel(960, 400), (60, 300))
text_lines(fr, 100, 330, [('배 위의 200 g 돌 → 물 200 cm³를 밀어내요', WHITE), '가라앉은 돌 → 자기 부피 80 cm³만 밀어내요', '물에 뜨는 나무는 어디서든 무게만큼',
                          ('첨벙 했으니 올라간다? 함정', YEL)], 34)
one(fr, 'qC', 540, 930, 360, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '빨간 선 = 처음 높이 · 민트 = 던진 뒤')
four(fr, 'r', 360, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '무거운 것일수록 많이 내려가요')
one(fr, 'rA', 300, 560, 400, tag=False); one(fr, 'rD', 780, 560, 400, tag=False)
fr.alpha_composite(panel(960, 280), (60, 890))
text_lines(fr, 100, 915, ['A: 200 − 80 = 120 cm³ ÷ 400 cm² = 0.3 cm → 3 mm', 'B: 나무는 떠서 24 g 그대로 → 0', 'D: 360 − 40 = 320 cm³ ÷ 400 = 8 mm'], 30)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1110)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
