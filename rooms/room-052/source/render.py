"""ROOM 052 cards in the 3D style (kit/style3d.py), from the block-pyramid sprites made by scene3d.py."""
import json, os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 52, '2026.10.28'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']


def spr(fr, name, cx, cy, sc):
    im = Image.open(f'{B}/{name}.png').convert('RGBA')
    l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()   # the blocks
    m = 50; im = im.crop((l - m, t - m, r + m, b + m))       # keep a little of the soft shadow, fade it out at the edges
    ys, xs = np.mgrid[0:im.height, 0:im.width]
    fade = np.clip(np.minimum.reduce([xs, ys, im.width - 1 - xs, im.height - 1 - ys]) / m, 0, 1)
    a = np.asarray(im.getchannel('A'), dtype=float) * fade; im.putalpha(Image.fromarray(a.astype('uint8')))
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))); return im


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
fr = card(ROOM, DATE, 1, 7, '숫자 블록 피라미드', '위 블록 = 아래 두 블록의 합, A B C D는?')
spr(fr, 'pyr', 540, 700, 1.6)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '블록 쌓기 덧셈')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 위 블록 = 바로 아래 두 블록의 합', '2. 빈 블록에도 숫자가 숨어 있다',
                          ('3. 노란 블록 A B C D의 숫자가 암호', YEL)], 33)
spr(fr, 'ex', 540, 800, 1.6)
put(fr, text_layer('3 + 4 = 7', 52, YEL), 540, 1060)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D의 숫자')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (255, 196, 92, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 150), (60, 700))
text_lines(fr, 540, 735, ['예: A 1, B 9, C 3, D 7이라면', ('암호 1937', YEL)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 숫자는 이것이 전부')
spr(fr, 'pyr', 540, 660, 1.45)
fr.alpha_composite(panel(960, 110), (60, 1050))
text_lines(fr, 540, 1068, ['위 블록 = 아래 두 블록의 합', ('암호 = A B C D', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '막히면 위에서 아래로 빼 보세요', CORAL)
fr.alpha_composite(panel(960, 220), (60, 300))
text_lines(fr, 100, 330, ['아래에서 더해 올라갈 수 없는 칸은', '위 블록에서 옆 블록을 빼면 나와요.',
                          ('C = 15 − 7부터 시작해 보세요', YEL)], 35)
spr(fr, 'pyr', 540, 820, 1.15)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '빈 블록은 28 − 15 = 13')
spr(fr, 'ans', 540, 650, 1.45)
fr.alpha_composite(panel(960, 120), (60, 1030))
text_lines(fr, 540, 1050, ['C = 15−7 = 8 · A = 7−2 = 5', ('D = 13−7 = 6 · B = 6−2 = 4', YEL)], 30, center=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 5 · B 4 · C 8 · D 6')
spr(fr, 'ans', 540, 560, 1.05)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 880)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1030)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
