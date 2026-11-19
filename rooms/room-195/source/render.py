"""ROOM 195 cards (물 섞기) in the 3D style (kit/style3d.py), from the measuring-jug sprites made by scene3d.py, with each board's two waters and the mixed
temperature written under it. All sprites are cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 195, '2026.12.18'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAPC = PROOF['trap_code']; FIN = PROOF['final_c']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 130, min(b[1] for b in bb) - 20, max(b[2] for b in bb) + 130, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    (v1, t1), (v2, t2) = BOARDS[n[1]]; k = n[1]; out = Image.new('RGBA', (c.width, c.height + 150), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'{v1}L {t1}°  +  {v2}L {t2}°', WHITE), ('섞으면 몇 도?', YEL))
    else: lines = ((f'{FIN[k]}°', MINT), (f'({v1}×{t1} + {v2}×{t2}) ÷ {v1 + v2}', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 62 if j == 0 else 52, col), c.width / 2, c.height + 30 + j * 76)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 34, y0 + im.height * 0.3)
    if val: put(fr, badge(val, 46), x0 + im.width - 40, y0 + im.height * 0.3)


POS = [(290, 520), (790, 520), (290, 945), (790, 945)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '물 섞기', '뜨거운 물과 찬물을 한 통에 부으면 몇 도?')
four(fr, 'q', 460)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '섞기 규칙', '눈금 한 칸 = 1L')
fr.alpha_composite(panel(960, 360), (60, 290))
text_lines(fr, 100, 322, ['1. 두 통의 물을 빈 통 하나에 모두 부어요', '2. 잘 저어서 온도가 고르게 돼요', '3. 열은 밖으로 빠져나가지 않아요',
                          '4. 숫자는 각 통의 물 온도(°C)예요', ('섞인 물의 온도, 십의 자리는?', YEL)], 33)
one(fr, 'qA', 540, 905, 360, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 섞인 온도의 십의 자리')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 20° · 60° · 10° · 80°면', ('암호 2618', YEL), '', ('두 온도의 중간이면 될까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '눈금 1칸 = 1L · 섞인 온도의 십의 자리')
four(fr, 'q', 460)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '물 양도 같이 보세요', CORAL)
fr.alpha_composite(panel(960, 360), (60, 300))
text_lines(fr, 100, 330, [('1L 1도마다 "열 1칸"이라고 생각해요', WHITE), '전체 열 칸 수 = 양×온도 + 양×온도', '그걸 전체 물 양으로 나누면 섞인 온도',
                          (f'그냥 두 온도의 중간이면 함정 {TRAPC}', YEL)], 35)
one(fr, 'qB', 540, 935, 340, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '물이 많은 쪽 온도로 끌려가요')
four(fr, 'r', 460, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '끓는 물을 부어도 40°예요')
one(fr, 'rB', 300, 560, 380, tag=False); one(fr, 'rD', 790, 560, 380, tag=False)
fr.alpha_composite(panel(960, 260), (60, 900))
text_lines(fr, 100, 925, ['B: 90°가 1L, 10°가 3L → 120 ÷ 4 = 30°', 'D: 100°가 1L, 25°가 4L → 200 ÷ 5 = 40°'], 31)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
