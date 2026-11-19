"""ROOM 196 cards (기름 아끼기) in the 3D style (kit/style3d.py), from the car sprites made by scene3d.py, with each board's
fuel economy and the litres saved written under it. All sprites are cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 196, '2026.12.19'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; LIT = PROOF['litres']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 40, min(b[1] for b in bb) - 20, max(b[2] for b in bb) + 40, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    k = n[1]; a, b = BOARDS[k]; u0, u1 = LIT[k]; out = Image.new('RGBA', (c.width, c.height + 150), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'연비 {a} → {b} km/L', WHITE), ('60km에 몇 L 아낄까?', YEL))
    else: lines = ((f'{u0 - u1}L 절약', MINT), (f'60÷{a} − 60÷{b} = {u0} − {u1}', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 62 if j == 0 else 52, col), c.width / 2, c.height + 30 + j * 76)
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

fr = card(ROOM, DATE, 1, 7, '기름 아끼기', '연비가 가장 많이 오른 차가 제일 아낄까요?')
four(fr, 'q', 460)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '연비 = 기름 1L로 가는 거리(km)')
fr.alpha_composite(panel(960, 360), (60, 290))
text_lines(fr, 100, 322, ['1. 네 대 모두 똑같이 60km를 달려요', '2. 차를 고쳐서 연비가 왼쪽 → 오른쪽이 됐어요', '3. 쓰는 기름 = 60 ÷ 연비',
                          '4. 고치기 전보다 기름을 몇 L 덜 쓸까요?', ('아낀 기름(L)이 각 자리 숫자', YEL)], 33)
one(fr, 'qA', 540, 905, 360, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 아낀 기름(L)')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2L · 7L · 1L · 9L 아꼈다면', ('암호 2719', YEL), '', ('연비가 두 배면 제일 많이 아낄까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '60km 달릴 때 아낀 기름(L)')
four(fr, 'q', 460)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '연비 숫자 말고 기름 양을 보세요', CORAL)
fr.alpha_composite(panel(960, 360), (60, 300))
text_lines(fr, 100, 330, [('먼저 고치기 전에 쓴 기름을 구해요', WHITE), '60 ÷ 고치기 전 연비  −  60 ÷ 고친 뒤 연비', '연비가 낮은 차일수록 조금만 올라도 크게 줄어요',
                          ('연비가 오른 만큼(km/L)을 적으면 함정', YEL)], 35)
one(fr, 'qB', 540, 935, 340, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '두 배가 된 B가 제일 적게 아껴요')
four(fr, 'r', 460, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '연비 15 오른 차 < 2 오른 차')
one(fr, 'rB', 300, 560, 380, tag=False); one(fr, 'rA', 790, 560, 380, tag=False)
fr.alpha_composite(panel(960, 260), (60, 900))
text_lines(fr, 100, 925, ['B: 15 → 30 km/L, 4L → 2L로 2L 절약', 'A: 4 → 6 km/L, 15L → 10L로 5L 절약'], 31)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
