"""ROOM 088 cards in the 3D style (kit/style3d.py), from the belt-wheel sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 88, '2026.11.13'
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
    if tag:
        put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 - 34, y0 + im.height / 2)
        if val: put(fr, badge(val, 42), x0 + im.width + 34, y0 + im.height / 2)


YS = [420, 625, 830, 1035]


def four(fr, pre, w=880, vals=None, ys=YS):
    for i, k in enumerate('ABCD'): one(fr, pre + k, 565 if not vals else 530, ys[i], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '시계 방향으로 도는 바퀴는 모두 몇 개?')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '바퀴들이 고무 벨트로 이어져 있어요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 맨 왼쪽 바퀴가 화살표대로 시계 방향', '2. 벨트는 미끄러지지 않아요',
                          '3. 바퀴 크기는 빠르기만 바꿔요', ('시계 방향 바퀴는 몇 개? (1번 포함)', YEL)], 33)
one(fr, 'qC', 540, 820, 980, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 시계 방향 바퀴 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2개 · 5개 · 1개 · 3개면', ('암호 2513', YEL), '', ('맨 왼쪽 바퀴도 개수에 넣어요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '벨트 모양을 잘 보세요')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '벨트가 X로 꼬였는지 보세요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('나란히 걸린 벨트 = 같은 방향', WHITE), 'X로 꼬인 벨트 = 반대 방향', '큰 바퀴, 작은 바퀴는 상관없어요.',
                          ('X를 지날 때마다 방향이 바뀌어요!', YEL)], 35)
one(fr, 'qB', 540, 850, 980, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '노란 화살표 = 시계 방향 · 파란 화살표 = 반대')
four(fr, 'r', w=840, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'X 벨트마다 방향이 뒤집혀요')
for i, k in enumerate('ABCD'): one(fr, 'r' + k, 580, 360 + i * 120, 700, tag=False)
for i, k in enumerate('ABCD'): put(fr, badge(CODE[i], 40), 150, 360 + i * 120)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 900)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1030)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
