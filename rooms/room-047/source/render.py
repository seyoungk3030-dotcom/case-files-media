"""ROOM 047 cards in the 3D style (kit/style3d.py), from the net sprites made by scene3d.py."""
import json, os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 47, '2026.10.27'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_farthest_face']


def spr(fr, name, cx, cy, sc):
    im = Image.open(f'{B}/{name}.png').convert('RGBA')
    l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()   # the tiles themselves
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
fr = card(ROOM, DATE, 1, 7, '별의 반대편', '접어서 주사위를 만들면 별과 마주 보는 숫자는?')
grid(fr, 'n', 520, 0.53, 440)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '정육면체 전개도 네 장이 펼쳐져 있다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 전개도를 접으면 주사위 한 개가 된다', '2. 숫자 면은 바깥쪽을 향한다',
                          ('3. 별과 마주 보는 면의 숫자를 찾는다', YEL)], 33)
spr(fr, 'nB', 540, 800, 0.75)
text_lines(fr, 540, 1080, [('주사위에서 마주 보는 면 = 서로 닿지 않는 면', SOFT)], 32, center=True)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D의 별 반대편 숫자')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 6, B 3, C 8, D 1이라면', ('암호 6381', YEL), '',
                          ('별 면은 숫자가 아니라서 세지 않아요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
grid(fr, 'n', 480, 0.47, 390)
fr.alpha_composite(panel(960, 110), (60, 1050))
text_lines(fr, 540, 1068, ['전개도를 접어 주사위로 만든다', ('암호 = 별 반대편 숫자 A B C D', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', '가장 멀리 있는 면이 반대편?', CORAL)
fr.alpha_composite(panel(960, 220), (60, 300))
text_lines(fr, 100, 330, ['펼친 그림에서 멀다고 반대편이 아니에요.', '한 줄로 이어진 세 칸에서는',
                          ('양 끝 두 면이 서로 마주 봐요', YEL)], 35)
spr(fr, 'nC', 540, 850, 0.8)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '별(초록)과 마주 보는 면(노랑)')
grid(fr, 'h', 500, 0.45, 410, list(CODE))
text_lines(fr, 540, 1060, [f'가장 먼 면을 고르면 {TRAP} · 함정이에요'], 30, center=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 7 · B 2 · C 5 · D 9')
grid(fr, 'h', 440, 0.34, 290, list(CODE))
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 880)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1030)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
