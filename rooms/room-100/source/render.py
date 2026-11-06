"""ROOM 100 cards in the 3D style (kit/style3d.py), from the rope-knot sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 100, '2026.11.17'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 22, y0 + 24)
    if val: put(fr, badge(val, 44), x0 + im.width - 40, y0 + 40)


POS = [(282, 500), (798, 500), (282, 820), (798, 820)]


def four(fr, pre, w=500, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '100번째 방 · 대부분 틀려요', '양 끝을 당기면 진짜 매듭은 몇 개?')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '매듭 규칙', '탁자 위에 밧줄을 위에서 내려다봤어요')
fr.alpha_composite(panel(960, 330), (60, 290))
text_lines(fr, 100, 322, ['1. 줄이 겹친 곳마다 위·아래가 있어요', '2. 두 끝을 잡고 양쪽으로 쭉 당겨요', '3. 끝까지 풀리면 매듭이 아니에요',
                          '4. 남아 있는 매듭만 세요', ('진짜 매듭은 몇 개일까요?', YEL)], 33)
one(fr, 'qA', 540, 860, 760, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 남는 매듭 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 1개 · 0개 · 2개 · 1개면', ('암호 1021', YEL), '', ('복잡해 보인다고 매듭은 아니에요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '겹친 곳의 위·아래를 하나씩 보세요')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '위·아래가 번갈아 엮여야 매듭', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('줄을 따라가며 겹친 곳을 지나 보세요', WHITE), '위 → 아래 → 위 → 아래로 번갈아 가면 매듭!', '위로만 두 번 연속 지나면 풀리는 곳이 있어요.',
                          ('한 번만 꼬인 고리는 그냥 풀려요', YEL)], 33)
one(fr, 'qB', 540, 870, 760, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '초록 원 = 진짜 매듭 · 회색 = 풀려요')
four(fr, 'r', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '100번째 방 탈출 성공', 'B 왼쪽 줄은 겹친 곳이 3개라도 풀려요')
one(fr, 'rB', 540, 540, 820, tag=False)
fr.alpha_composite(panel(960, 250), (60, 840))
text_lines(fr, 100, 865, ['함께해 주셔서 고마워요! 다음 100방도 기대해 주세요', ('(매듭은 존스 다항식으로 하나하나 확인했어요)', SOFT)], 31)
put(fr, text_layer(' '.join(CODE), 80, MINT, glow=MINT), 540, 1035)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
