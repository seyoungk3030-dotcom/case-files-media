"""ROOM 190 cards (왕복 평균 속도) in the 3D style (kit/style3d.py), from the road-and-car sprites made by scene3d.py, with each board's two speeds written under it. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 190, '2026.12.17'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_mean_of_speeds']; AVG = PROOF['average_kmh']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    a, b = BOARDS[n[1]]; out = Image.new('RGBA', (c.width, c.height + 150), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'갈 때 {a}km/h →', YEL), (f'← 올 때 {b}km/h', WHITE))
    else: lines = ((f'왕복 평균 {AVG[n[1]]}km/h', MINT), (f'갈 때 {a} · 올 때 {b}', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 60 if j == 0 else 54, col), c.width / 2, c.height + 30 + j * 74)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 40, y0 + 36)
    if val: put(fr, badge(val, 46), x0 + im.width - 44, y0 + 40)


POS = [(290, 500), (790, 500), (290, 920), (790, 920)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '왕복 평균 속도', '갈 때 60, 올 때 20이면 평균은 40일까요?')
four(fr, 'q', 470)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '드라이브 규칙', '같은 길을 갔다가 그대로 돌아와요')
fr.alpha_composite(panel(960, 360), (60, 290))
text_lines(fr, 100, 322, ['1. 집 → 회사, 회사 → 집, 똑같은 길이에요', '2. 갈 때와 올 때 속도는 노란 판에 적혀 있어요', '3. 중간에 쉬지 않고 그 속도로만 달려요',
                          '4. 평균 속도 = 전체 거리 ÷ 전체 시간', ('왕복 평균 속도의 앞자리(÷10)는?', YEL)], 33)
one(fr, 'qA', 540, 900, 620, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 평균 속도 ÷ 10')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 평균 20 · 70 · 10 · 90km/h면', ('암호 2719', YEL), '', ('거리는 안 나와요. 아무 거리나 넣어 보세요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '평균 = 전체 거리 ÷ 전체 시간')
four(fr, 'q', 470)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '두 속도를 더해서 반으로 나누면 될까요?', CORAL)
fr.alpha_composite(panel(960, 360), (60, 300))
text_lines(fr, 100, 330, [('집에서 회사까지 60km라고 해 볼게요', WHITE), 'A: 갈 때 60km/h면 1시간, 올 때 20km/h면 3시간', '느린 쪽에서 훨씬 오래 달려요.',
                          (f'두 속도의 가운데 값을 쓰면 함정 {TRAP}', YEL)], 35)
one(fr, 'qA', 540, 955, 600, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '느린 쪽에서 더 오래 달려서 평균이 내려가요')
four(fr, 'r', 470, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '평균 속도는 거리 ÷ 시간')
one(fr, 'rA', 540, 540, 700, tag=False)
fr.alpha_composite(panel(960, 300), (60, 830))
text_lines(fr, 100, 855, ['A: 60km를 1시간 + 3시간 = 4시간에 120km → 30', 'B: 120km를 3시간 + 1시간 = 4시간에 240km → 60', 'D: 120km를 1시간 + 2시간 = 3시간에 240km → 80'], 31)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
