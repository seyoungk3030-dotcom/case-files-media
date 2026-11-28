"""ROOM 215 cards (뚜껑 닫은 물통) in the 3D style (kit/style3d.py), from the water-jug sprites made by
scene3d.py, with each board's holes and cap written under it. All sprites are cropped to one shared box around the window frame
(q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS, GOOD
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 215, '2026.12.25'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
f = lambda x: str(int(x)) if x.denominator == 1 else f'{float(x):g}'
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 6, min(b[1] for b in bb) - 6, max(b[2] for b in bb) + 6, max(b[3] for b in bb) + 6)
for n, im in ims.items():
    c = im.crop(BOX); k = n[1]; nh, cap, air = BOARDS[k]; out = Image.new('RGBA', (c.width, c.height + 170), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'아래 구멍 {nh}개 · 뚜껑 {"닫힘" if cap else "열림"}', WHITE), ('물줄기는 몇 개?', YEL))
    else: lines = ((f'물줄기 {GOOD[k]}개', MINT), ('위 구멍으로 공기 들어옴' if air else ('뚜껑으로 공기 들어옴' if not cap else '공기가 못 들어옴'), SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 66 if j == 0 else 60, col), c.width / 2, c.height + 46 + j * 80)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 30, y0 + 30)
    if val: put(fr, badge(val, 46), x0 + im.width - 50, y0 + 44)


POS = [(285, 505), (795, 505), (285, 945), (795, 945)]


def four(fr, pre, w=500, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '뚜껑 닫은 물통', '구멍마다 물이 샐까요?')
four(fr, 'q', 440)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '물이 가득 든 물통 아래에 작은 구멍을 뚫었어요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['1. 아래 구멍은 모두 같은 높이예요', '2. 뚜껑은 닫혀 있거나 옆에 빠져 있어요', '3. 어떤 물통은 물 위쪽에도 작은 구멍이 있어요',
                          '4. 물줄기는 몇 개 나올까요?', ('A~D 물줄기 개수가 각 자리 숫자', YEL)], 32)
one(fr, 'qC', 540, 880, 600, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 물줄기 개수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 3 · 7 · 5 · 2개라면', ('암호 3752', YEL), '', ('물이 빠진 자리는 무엇이 채울까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '물줄기는 몇 개 나올까?')
four(fr, 'q', 440)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '물이 나간 만큼 공기가 들어와야 해요', CORAL)
fr.alpha_composite(panel(960, 270), (60, 300))
text_lines(fr, 100, 330, [('공기는 열린 입구나 물 위 구멍으로만 들어와요', WHITE), '작은 구멍으로는 공기 방울이 못 들어가요', '공기가 못 들어오면 물줄기가 멈춰요',
                          ('구멍 수 = 물줄기 수? 함정', YEL)], 33)
one(fr, 'qB', 540, 880, 600, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 = 물이 나오는 구멍 · 빨강 = 막힌 구멍')
four(fr, 'r', 440, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '공기가 들어와야 물이 나가요')
one(fr, 'rB', 285, 560, 470, tag=False); one(fr, 'rC', 795, 560, 470, tag=False)
fr.alpha_composite(panel(960, 280), (60, 860))
text_lines(fr, 100, 885, ['A, D: 뚜껑이 열려 있어 구멍마다 물줄기', 'B: 뚜껑 닫힘, 공기 길이 없어 0개', 'C: 뚜껑은 닫혔지만 위 구멍으로 공기 → 5개'], 30)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
