"""ROOM 205 cards (페달 한 바퀴) in the 3D style (kit/style3d.py), from the side-view sprites made by scene3d.py, with each
board's speed and the sticker's ground speed written under it. All sprites are cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 205, '2026.12.22'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TURN = PROOF['turns']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 20, min(b[1] for b in bb) - 20, max(b[2] for b in bb) + 20, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); k = n[1]; F, R, P = BOARDS[k]; out = Image.new('RGBA', (c.width, c.height + 150), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'앞 톱니 {F} · 뒤 톱니 {R}', WHITE), (f'페달 {P}바퀴 → 뒷바퀴는?', YEL))
    else: lines = ((f'뒷바퀴 {TURN[k]}바퀴', MINT), (f'{F} ÷ {R} × 페달 {P}바퀴', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 62 if j == 0 else 54, col), c.width / 2, c.height + 48 + j * 76)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 30, y0 + 30)
    if val: put(fr, badge(val, 46), x0 + im.width - 40, y0 + im.height * 0.42)


POS = [(300, 515), (780, 515), (300, 940), (780, 940)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '페달 한 바퀴', '바퀴도 한 바퀴 아닌가요?')
four(fr, 'q', 330)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '자전거 체인이 앞뒤 톱니를 이어요')
fr.alpha_composite(panel(960, 420), (60, 290))
text_lines(fr, 100, 322, ['1. 페달은 앞 톱니(큰 은색)를 돌려요', '2. 체인이 뒤 톱니(작은 금색)를 돌려요', '3. 뒤 톱니는 뒷바퀴에 붙어 함께 돌아요',
                          '4. 페달을 적힌 만큼 돌리면 뒷바퀴는 몇 바퀴?', ('A~D 뒷바퀴 바퀴 수가 각 자리 숫자', YEL)], 32)
one(fr, 'qB', 540, 980, 340, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 뒷바퀴 바퀴 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2바퀴 · 5바퀴 · 1바퀴 · 4바퀴라면', ('암호 2514', YEL), '', ('페달 한 바퀴 = 바퀴 한 바퀴일까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '뒷바퀴는 몇 바퀴 돌까?')
four(fr, 'q', 330)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '체인은 톱니 한 칸씩 지나가요', CORAL)
fr.alpha_composite(panel(960, 400), (60, 300))
text_lines(fr, 100, 330, [('페달 한 바퀴 = 앞 톱니 수만큼 체인이 움직여요', WHITE), '뒤 톱니는 그 칸 수만큼 돌아요', '예: 앞 40, 뒤 20 → 뒤 톱니 2바퀴',
                          ('페달 한 바퀴 = 바퀴 한 바퀴? 함정', YEL)], 34)
one(fr, 'qC', 540, 980, 340, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '앞 톱니 ÷ 뒤 톱니 × 페달')
four(fr, 'r', 330, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '그래서 고단 기어가 빨라요')
one(fr, 'rA', 300, 560, 340, tag=False); one(fr, 'rD', 780, 560, 340, tag=False)
fr.alpha_composite(panel(960, 280), (60, 890))
text_lines(fr, 100, 915, ['A: 48 ÷ 12 = 페달 1바퀴에 4바퀴', 'C: 30 ÷ 30 = 1바퀴, 오르막용 가벼운 기어', 'D: 30 ÷ 18 × 3바퀴 = 5바퀴'], 30)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1110)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
