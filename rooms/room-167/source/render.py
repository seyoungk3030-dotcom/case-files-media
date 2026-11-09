"""ROOM 167 cards in the 3D style (kit/style3d.py), from the pizza-tray sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png)."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 167, '2026.12.09'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_diameters']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 34, y0 + im.height - 44)
    if val: put(fr, badge(val, 44), x0 + im.width - 44, y0 + im.height - 44)


POS = [(292, 545), (788, 545), (292, 930), (788, 930)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '피자가 더 많은 쪽은?', '큰 피자 한 판 vs 작은 피자 여러 판')
four(fr, 'q', 470)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '피자 규칙', '두께는 모두 같아요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['쟁반마다 번호와 피자 지름, 판 수가 적혀 있어요', '피자 두께는 모두 같아요',
                          '먹을 수 있는 피자 양이 더 많은 쪽은?', ('그쪽 쟁반의 번호가 암호 한 자리예요', YEL)], 30)
one(fr, 'qA', 540, 830, 760, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 더 많은 쪽 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 1 · 8 · 4 · 6번 쪽이 많으면', ('암호 1846', YEL), '', ('판 수에 속지 마세요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '피자 양이 더 많은 쪽 번호')
four(fr, 'q', 470)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '지름을 더하면 함정', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('피자 양은 지름이 아니라 넓이예요', WHITE), '넓이는 지름 × 지름에 비례해요',
                          'A: 30×30 = 900  vs  20×20 × 2 = 800', (f'지름만 더하면 함정 {TRAP}', YEL)], 33)
one(fr, 'qA', 540, 850, 760, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '지름 × 지름 × 판 수가 큰 쪽')
four(fr, 'r', 470, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'rB', 540, 560, 760, tag=False)
fr.alpha_composite(panel(960, 230), (60, 840))
text_lines(fr, 100, 870, ['B: 36×36 = 1296  vs  20×20 × 3 = 1200', '한 판짜리 36cm가 세 판보다 많아요!'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1135)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
