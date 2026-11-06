"""ROOM 096 cards in the 3D style (kit/style3d.py), from the ball-race track sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 96, '2026.11.16'
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


YS = [415, 622, 829, 1036]


def four(fr, pre, w=680, vals=None, ys=YS):
    for i, k in enumerate('ABCD'): one(fr, pre + k, 565 if not vals else 520, ys[i], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '어느 길의 공이 가장 먼저 도착할까?')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '공 굴리기 경주', '세 공을 동시에 놓아요')
fr.alpha_composite(panel(960, 330), (60, 290))
text_lines(fr, 100, 322, ['1. 출발 높이와 도착 지점은 모두 같아요', '2. 길 모양만 달라요', '3. 마찰과 공기 저항은 없어요',
                          '4. 깃발에 먼저 닿는 공이 1등', ('1등 길의 번호는?', YEL)], 33)
one(fr, 'qA', 540, 860, 960, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 1등 길의 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 3번 · 1번 · 1번 · 2번이면', ('암호 3112', YEL), '', ('짧은 길이 빠른 길은 아니에요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '처음에 얼마나 빨리 떨어지느냐가 열쇠')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '직선이 가장 빠르지 않아요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('처음에 가파르게 떨어지면', WHITE), '속도를 일찍 얻어서 길이 길어도 빨라요.', '하지만 너무 깊이 파이면 다시 올라오느라 느려요.',
                          ('혹(언덕)이 있는 길은 가장 느려요!', YEL)], 33)
one(fr, 'qC', 540, 860, 960, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '1등이 도착한 순간 다른 공의 위치')
four(fr, 'r', w=660, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

T = PROOF['times_s']
fr = card(ROOM, DATE, 7, 7, '탈출 성공', '가장 빠른 길 = 적당히 파인 곡선')
fr.alpha_composite(panel(960, 420), (60, 300))
text_lines(fr, 110, 335, [f'{k}: ' + ' · '.join(f'{i + 1}번 {t:.2f}초' for i, t in enumerate(T[k])) for k in 'ABCD'] + [('(높이 1.2m · 거리 2m 모형으로 계산)', SOFT)], 32)
put(fr, text_layer(' '.join(CODE), 110, MINT, glow=MINT), 540, 900)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
