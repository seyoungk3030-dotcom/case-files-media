"""ROOM 050 cards in the 3D style (kit/style3d.py), from the matchstick sprites made by scene3d.py."""
import json, os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 50, '2026.10.28'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_small_only']


def spr(fr, name, cx, cy, sc):
    im = Image.open(f'{B}/{name}.png').convert('RGBA')
    l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()   # the felt and matches
    m = 50; im = im.crop((l - m, t - m, r + m, b + m))       # keep a little of the soft shadow, fade it out at the edges
    ys, xs = np.mgrid[0:im.height, 0:im.width]
    fade = np.clip(np.minimum.reduce([xs, ys, im.width - 1 - xs, im.height - 1 - ys]) / m, 0, 1)
    a = np.asarray(im.getchannel('A'), dtype=float) * fade; im.putalpha(Image.fromarray(a.astype('uint8')))
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))); return im


def grid(fr, pre, y0, sc, gap, vals=None):
    for i, k in enumerate('ABCD'):
        cx, cy = 290 + (i % 2) * 500, y0 + (i // 2) * gap
        im = spr(fr, pre + k, cx, cy, sc)
        put(fr, pill(k, 38, INK, (244, 246, 250, 245), (22, 6)), cx - 200, cy - gap / 2 + 40)
        if vals: put(fr, badge(vals[i], 40), cx - 130, cy - gap / 2 + 40)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
fr = card(ROOM, DATE, 1, 7, '정사각형 세기', '성냥 그림 속 정사각형은 모두 몇 개?')
grid(fr, 'f', 530, 0.56, 440)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '성냥개비 그림 네 개')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 성냥 네 변이 다 있으면 정사각형', '2. 작은 것, 큰 것 크기 상관없이 센다',
                          ('3. 겹쳐 있는 정사각형도 따로 센다', YEL)], 33)
spr(fr, 'fB', 540, 820, 0.8)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D의 정사각형 개수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 2개, B 7개, C 4개, D 6개라면', ('암호 2746', YEL), '',
                          ('네 변 중 하나라도 빠지면 세지 않아요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
grid(fr, 'f', 470, 0.5, 400)
fr.alpha_composite(panel(960, 110), (60, 1050))
text_lines(fr, 540, 1068, ['네 변이 모두 있는 정사각형만 · 크기 상관없음', ('암호 = 정사각형 개수 A B C D', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', f'작은 칸만 세면 {TRAP}?', CORAL)
fr.alpha_composite(panel(960, 220), (60, 300))
text_lines(fr, 100, 330, ['한 칸짜리만 세면 틀려요.', '2×2, 3×3처럼 여러 칸을 묶은 큰 정사각형도',
                          ('네 변이 다 있으면 하나로 세요', YEL)], 35)
spr(fr, 'fD', 540, 840, 0.75)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '초록 = 작은 칸 · 노랑 = 2×2 · 빨강 = 3×3')
grid(fr, 'x', 490, 0.52, 420, list(CODE))
text_lines(fr, 540, 1075, ['A 2+1 · B 6+2 · C 4+1 · D 6+2+1'], 30, center=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 3 · B 8 · C 5 · D 9')
grid(fr, 'x', 430, 0.38, 300, list(CODE))
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 880)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1030)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
