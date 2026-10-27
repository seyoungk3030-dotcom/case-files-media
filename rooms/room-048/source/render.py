"""ROOM 048 cards in the 3D style (kit/style3d.py), from the clock sprites made by scene3d.py."""
import json, os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 48, '2026.10.27'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_read_as_is']


def spr(fr, name, cx, cy, sc):
    im = Image.open(f'{B}/{name}.png').convert('RGBA')
    l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()   # the clock or mirror itself
    m = 50; im = im.crop((l - m, t - m, r + m, b + m))       # keep a little of the soft shadow, fade it out at the edges
    ys, xs = np.mgrid[0:im.height, 0:im.width]
    fade = np.clip(np.minimum.reduce([xs, ys, im.width - 1 - xs, im.height - 1 - ys]) / m, 0, 1)
    a = np.asarray(im.getchannel('A'), dtype=float) * fade; im.putalpha(Image.fromarray(a.astype('uint8')))
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))); return im


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
fr = card(ROOM, DATE, 1, 7, '거울 속 시계', '진짜 시각은 몇 시 몇 분?')
spr(fr, 'mirror', 540, 700, 0.88)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '벽시계가 거울에 비쳐 보인다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 시계는 거울로만 볼 수 있다', '2. 거울 속은 좌우가 뒤집혀 있다',
                          ('3. 진짜 시각을 시·분 네 자리로 쓴다', YEL)], 33)
spr(fr, 'mirror', 540, 820, 0.55)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', '진짜 시각의 시 두 자리 + 분 두 자리')
for n, k in enumerate(['시', '시', '분', '분']):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 진짜 시각이 9시 41분이라면', ('암호 0941', YEL), '',
                          ('오전·오후는 따지지 않아요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
spr(fr, 'mirror', 540, 640, 0.72)
fr.alpha_composite(panel(960, 110), (60, 1050))
text_lines(fr, 540, 1068, ['거울에 비친 벽시계 · 좌우가 뒤집힘', ('암호 = 진짜 시각 시·분 네 자리', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', '보이는 대로 읽으면 1시 23분?', CORAL)
fr.alpha_composite(panel(960, 220), (60, 300))
text_lines(fr, 100, 330, ['거울 속 바늘은 좌우가 바뀐 모습이에요.', '12시와 6시를 잇는 선을 기준으로',
                          ('바늘을 반대쪽으로 넘겨 보세요', YEL)], 35)
spr(fr, 'mirror', 540, 830, 0.5)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '거울 속 1시 23분 = 진짜 10시 37분')
spr(fr, 'mirror', 290, 640, 0.44); spr(fr, 'real', 790, 640, 0.48)
put(fr, pill('거울', 30, INK, (244, 246, 250, 245), (18, 6)), 290, 900); put(fr, pill('진짜', 30, INK, (*MINT, 245), (18, 6)), 790, 900)
text_lines(fr, 540, 990, ['12:00 − 1:23 = 10:37', (f'보이는 대로 {TRAP}을 쓰면 함정이에요', SOFT)], 32, center=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '진짜 시각 10시 37분')
spr(fr, 'real', 540, 560, 0.5)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 880)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1030)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
