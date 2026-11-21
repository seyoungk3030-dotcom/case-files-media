"""ROOM 202 cards (몇 초 만에 땅에?) in the 3D style (kit/style3d.py), from the side-view sprites made by scene3d.py, with each
board's speed and the sticker's ground speed written under it. All sprites are cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 202, '2026.12.21'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; T = PROOF['seconds']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 20, min(b[1] for b in bb) - 20, max(b[2] for b in bb) + 20, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); k = n[1]; h, u, ball = BOARDS[k]; out = Image.new('RGBA', (c.width, c.height + 150), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'{h}m · {ball}', WHITE), (f'옆으로 초속 {u}m 던짐' if u else '손을 놓기만 함', YEL))
    else: lines = ((f'{T[k]}초 만에 땅에', MINT), (f'5 × {T[k]} × {T[k]} = {h}m', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 62 if j == 0 else 54, col), c.width / 2, c.height + 30 + j * 76)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 30, y0 + 30)
    if val: put(fr, badge(val, 46), x0 + im.width - 40, y0 + im.height * 0.42)


POS = [(290, 520), (790, 520), (290, 945), (790, 945)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '몇 초 만에 땅에?', '옆으로 던진 공이 더 오래 날까요?')
four(fr, 'q', 400)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '옥상 끝에서 공이 출발해요')
fr.alpha_composite(panel(960, 400), (60, 290))
text_lines(fr, 100, 322, ['1. 화살표 방향으로 공이 출발해요 (아래 = 그냥 놓기)', '2. 공기 저항은 없다고 해요', '3. 떨어진 거리 = 5 × 초 × 초 (m)',
                          '4. 공의 종류와 옆으로 던진 속도도 적혀 있어요', ('땅에 닿기까지 걸린 초가 각 자리 숫자', YEL)], 33)
one(fr, 'qA', 540, 930, 360, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 걸린 초')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2초 · 6초 · 1초 · 5초라면', ('암호 2615', YEL), '', ('무거운 볼링공이 더 빨리 떨어질까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '몇 초 만에 땅에 닿을까?')
four(fr, 'q', 400)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '옆으로 가는 것과 아래로 떨어지는 건 따로', CORAL)
fr.alpha_composite(panel(960, 400), (60, 300))
text_lines(fr, 100, 330, [('아래로 떨어지는 빠르기는 모든 공이 같아요', WHITE), '옆으로 던지면 멀리 갈 뿐, 떨어지는 시간은 같아요', '5 × 초 × 초 = 높이가 되는 초를 찾아요',
                          ('높이 4배 = 시간 4배? 함정', YEL)], 35)
one(fr, 'qD', 540, 950, 340, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '높이만 보면 돼요')
four(fr, 'r', 400, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '높이 4배면 시간은 2배')
one(fr, 'rB', 300, 560, 360, tag=False); one(fr, 'rC', 790, 560, 360, tag=False)
fr.alpha_composite(panel(960, 260), (60, 900))
text_lines(fr, 100, 925, ['B: 5m → 1초 (5 × 1 × 1)', 'C: 80m는 16배 높지만 → 4초 (5 × 4 × 4)'], 31)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
