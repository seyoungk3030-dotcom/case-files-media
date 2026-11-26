"""ROOM 208 cards (그네 한 번 왕복) in the 3D style (kit/style3d.py), from the swing sprites made by
scene3d.py, with each board's rider, chain and push written under it. All sprites are cropped to one shared box
(q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS, GOOD, EXACT
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 208, '2026.12.23'
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
    k = n[1]; who, kg, L, deg = BOARDS[k]; out = Image.new('RGBA', (c.width, c.height + 200), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'줄 {L:g} m · {who} {kg} kg', WHITE), ('살짝 밀기' if deg < 20 else '세게 밀기', YEL))
    else: lines = ((f'왕복 약 {GOOD[k]}초', MINT), (f'2초 × √{L:g} = {2 * L ** 0.5:g}초', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 76 if j == 0 else 66, col), c.width / 2, c.height + 56 + j * 96)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 30, y0 + 30)
    if val: put(fr, badge(val, 46), x0 + im.width * 0.5, y0 + 40)


POS = [(290, 505), (790, 505), (290, 935), (790, 935)]


def four(fr, pre, w=500, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
W4 = 380

fr = card(ROOM, DATE, 1, 7, '그네 한 번 왕복', '무거우면 느릴까? 세게 밀면 빠를까?')
four(fr, 'q', W4)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '놀이터 그네를 한 번 밀고 손을 놔요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['1. 줄 길이, 타는 사람, 미는 세기가 달라요', '2. 미는 세기: 살짝 15°, 세게 30~35°', '3. 한 번 갔다가 돌아오는 데 몇 초?',
                          '4. 소수점은 반올림해요', ('A~D 왕복 초가 각 자리 숫자', YEL)], 32)
one(fr, 'qD', 540, 860, 470, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 왕복 초')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 5초 · 1초 · 6초 · 2초라면', ('암호 5162', YEL), '', ('어른이 타면 더 천천히 흔들릴까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '한 번 왕복에 몇 초?')
four(fr, 'q', W4)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '시계추와 같은 원리예요', CORAL)
fr.alpha_composite(panel(960, 270), (60, 300))
text_lines(fr, 100, 330, [('줄 1 m 그네 → 왕복 약 2초', WHITE), '줄이 4배 길면 시간은 2배 (√ 길이)', '몸무게는 시간에 영향이 없어요',
                          ('어른이니 느리다? 세게 미니 빠르다? 함정', YEL)], 34)
one(fr, 'qB', 540, 860, 470, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '줄 길이만 시간을 바꿔요')
four(fr, 'r', W4, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '왕복 시간 ≈ 2초 × √(줄 길이 m)')
one(fr, 'rA', 290, 560, 400, tag=False); one(fr, 'rB', 790, 560, 400, tag=False)
fr.alpha_composite(panel(960, 280), (60, 860))
text_lines(fr, 100, 885, ['A와 B: 줄 2.25 m로 같으니 둘 다 약 3초', '어린이 25 kg이든 어른 75 kg이든 같아요', 'D: 줄 4 m → 2 × 2 = 4초'], 30)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
