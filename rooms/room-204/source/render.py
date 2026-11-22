"""ROOM 204 cards (천둥까지 몇 km?) in the 3D style (kit/style3d.py), from the side-view sprites made by scene3d.py, with each
board's speed and the sticker's ground speed written under it. All sprites are cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 204, '2026.12.21'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; KM = PROOF['km']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 20, min(b[1] for b in bb) - 20, max(b[2] for b in bb) + 20, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); k = n[1]; t = BOARDS[k]; out = Image.new('RGBA', (c.width, c.height + 150), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'번개 번쩍, {t}초 뒤 우르릉', WHITE), ('번개는 몇 km 떨어져 있나?', YEL))
    else: lines = ((f'약 {round(KM[k])} km', MINT), (f'340 m × {t}초 = {round(KM[k] * 1000):,} m', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 62 if j == 0 else 54, col), c.width / 2, c.height + 48 + j * 76)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 30, y0 + 30)
    if val: put(fr, badge(val, 46), x0 + im.width - 40, y0 + im.height * 0.42)


POS = [(285, 520), (795, 520), (285, 945), (795, 945)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '천둥까지 몇 km?', '1초에 1 km 아닌가요?')
four(fr, 'q', 500)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '번개를 보고 천둥까지 초를 세요')
fr.alpha_composite(panel(960, 420), (60, 290))
text_lines(fr, 100, 322, ['1. 번개가 번쩍하는 순간 초를 세기 시작해요', '2. 우르릉 천둥이 들리면 멈춰요', '3. 소리는 1초에 약 340 m 가요',
                          '4. 번개가 친 곳까지 몇 km인지 반올림해요', ('A~D의 km가 각 자리 숫자', YEL)], 32)
one(fr, 'qB', 540, 950, 520, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 거리(km)')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2 km · 5 km · 1 km · 4 km라면', ('암호 2514', YEL), '', ('센 초가 그대로 km일까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '번개까지 몇 km?')
four(fr, 'q', 500)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '빛은 거의 바로 도착해요', CORAL)
fr.alpha_composite(panel(960, 400), (60, 300))
text_lines(fr, 100, 330, [('빛은 3 km를 0.00001초 만에 와요', WHITE), '그러니 센 시간은 거의 다 소리가 온 시간', '소리 340 m/s → 3초면 약 1 km',
                          ('1초 = 1 km? 함정', YEL)], 35)
one(fr, 'qC', 540, 950, 520, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '센 초를 3으로 나누면 km')
four(fr, 'r', 500, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '3초에 약 1 km')
one(fr, 'rA', 300, 560, 440, tag=False); one(fr, 'rD', 790, 560, 440, tag=False)
fr.alpha_composite(panel(960, 280), (60, 890))
text_lines(fr, 100, 915, ['A: 9초 × 340 m = 3,060 m → 약 3 km', 'D: 12초 × 340 m = 4,080 m → 약 4 km', '1초 = 1 km라면 소리가 음속의 3배!'], 30)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1110)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
