"""ROOM 194 cards (편의점 행사) in the 3D style (kit/style3d.py), from the shelf sprites made by scene3d.py, with each board's deal and the real discount
written under it. All sprites are cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 194, '2026.12.18'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_half_price_read_as_50']; PCT = PROOF['percent']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    deal, take, pay, prod = BOARDS[n[1]]; k = n[1]; out = Image.new('RGBA', (c.width, c.height + 150), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'{prod} · {deal}', WHITE), (f'{take}개를 가져가요', YEL))
    else: lines = ((f'{PCT[k]:g}% 할인', MINT), (f'{take}개 값 중 {float(pay):g}개만 냄', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 62 if j == 0 else 52, col), c.width / 2, c.height + 30 + j * 76)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 40, y0 + 36)
    if val: put(fr, badge(val, 46), x0 + im.width - 44, y0 + 40)


POS = [(290, 520), (790, 520), (290, 945), (790, 945)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '편의점 행사', '두 번째 반값, 진짜 몇 % 할인일까요?')
four(fr, 'q', 360)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '행사 규칙', '모든 물건은 1개 정가가 같아요')
fr.alpha_composite(panel(960, 360), (60, 290))
text_lines(fr, 100, 322, ['1. 행사대로 딱 한 묶음만 사요', '2. 50% 딱지는 그 자리 물건 하나만 반값이에요', '3. 가져간 개수를 모두 정가로 샀을 때와 비교해요',
                          '4. 실제로 몇 % 덜 냈는지 계산해요', ('할인율의 십의 자리 숫자는?', YEL)], 33)
one(fr, 'qB', 540, 905, 360, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 할인율의 십의 자리')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 40% · 12% · 75% · 60%면', ('암호 4176', YEL), '', ('반값 딱지는 50% 할인일까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '가져간 전체 개수 기준 할인율 · 십의 자리')
four(fr, 'q', 360)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '공짜로 받은 몫을 세어 보세요', CORAL)
fr.alpha_composite(panel(960, 360), (60, 300))
text_lines(fr, 100, 330, [('1+1: 2개 중 1개가 공짜 → 1 ÷ 2 = 50%', WHITE), '반값 딱지: 그 1개 중 절반만 공짜예요', '할인율 = 공짜 몫 ÷ 가져간 개수',
                          (f'반값이니 50%라고 보면 함정 {TRAP}', YEL)], 35)
one(fr, 'qD', 540, 935, 340, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 = 공짜로 받은 몫')
four(fr, 'r', 360, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '두 번째 반값은 25% 할인이에요')
one(fr, 'rB', 300, 560, 380, tag=False); one(fr, 'rD', 790, 560, 380, tag=False)
fr.alpha_composite(panel(960, 260), (60, 900))
text_lines(fr, 100, 925, ['B: 2개 중 0.5개가 공짜 → 0.5 ÷ 2 = 25%', 'D: 3개 중 0.5개가 공짜 → 0.5 ÷ 3 ≈ 16.7%'], 31)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
