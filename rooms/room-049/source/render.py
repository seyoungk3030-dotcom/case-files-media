"""ROOM 049 cards in the 3D style (kit/style3d.py), from the pipe sprites made by scene3d.py."""
import json, os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 49, '2026.10.27'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_straight_down']


def spr(fr, name, cx, cy, sc):
    im = Image.open(f'{B}/{name}.png').convert('RGBA')
    l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()   # the board itself
    m = 50; im = im.crop((l - m, t - m, r + m, b + m))       # keep a little of the soft shadow, fade it out at the edges
    ys, xs = np.mgrid[0:im.height, 0:im.width]
    fade = np.clip(np.minimum.reduce([xs, ys, im.width - 1 - xs, im.height - 1 - ys]) / m, 0, 1)
    a = np.asarray(im.getchannel('A'), dtype=float) * fade; im.putalpha(Image.fromarray(a.astype('uint8')))
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))); return im


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
fr = card(ROOM, DATE, 1, 7, '엉킨 파이프', '물을 틀면 A B C D는 어느 컵을 채울까?')
spr(fr, 'pipes', 540, 690, 0.98)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '수도꼭지 네 개, 컵 여섯 개')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 수도꼭지 A~D를 하나씩 튼다', '2. 물은 이어진 파이프를 따라 흐른다',
                          ('3. 물이 도착한 컵 번호를 적는다', YEL)], 33)
spr(fr, 'pipes', 540, 830, 0.62)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D가 채우는 컵 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 2, B 5, C 6, D 1이라면', ('암호 2561', YEL), '',
                          ('물을 못 받는 빈 컵도 있어요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
spr(fr, 'pipes', 540, 650, 0.9)
fr.alpha_composite(panel(960, 110), (60, 1050))
text_lines(fr, 540, 1068, ['파이프를 따라 물이 흐른다', ('암호 = A B C D가 채우는 컵 번호', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', '바로 아래 컵이 정답?', CORAL)
fr.alpha_composite(panel(960, 220), (60, 300))
text_lines(fr, 100, 330, ['파이프는 서로 위아래로 엇갈려 지나가요.', '겹치는 곳에서 옆 파이프로 갈아타지 말고',
                          ('한 줄만 손가락으로 끝까지 따라가 보세요', YEL)], 35)
spr(fr, 'pipes', 540, 830, 0.6)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', 'A→4 · B→6 · C→1 · D→3')
spr(fr, 'answer', 540, 650, 0.9)
text_lines(fr, 540, 1075, [(f'바로 아래 컵 {TRAP}을 고르면 함정이에요', SOFT)], 32, center=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 4 · B 6 · C 1 · D 3')
spr(fr, 'answer', 540, 560, 0.6)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 880)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1030)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
