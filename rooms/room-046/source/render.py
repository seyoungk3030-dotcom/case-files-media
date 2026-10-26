"""ROOM 046 cards in the 3D style (kit/style3d.py), from the block sprites made by scene3d.py."""
import json, os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BLOCKS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 46, '2026.10.26'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_bottom_forgotten']
SIZE = {k: f'{w}×{d}×{h}' for k, (w, d, h) in BLOCKS.items()}


def spr(fr, name, cx, cy, sc):
    im = Image.open(f'{B}/{name}.png').convert('RGBA')
    l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()   # the block itself
    m = 50; im = im.crop((l - m, t - m, r + m, b + m))       # keep a little of the soft shadow, fade it out at the edges
    ys, xs = np.mgrid[0:im.height, 0:im.width]
    fade = np.clip(np.minimum.reduce([xs, ys, im.width - 1 - xs, im.height - 1 - ys]) / m, 0, 1)
    a = np.asarray(im.getchannel('A'), dtype=float) * fade; im.putalpha(Image.fromarray(a.astype('uint8')))
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))); return im


def grid(fr, pre, y0, sc, gap, vals=None, foot=True):
    for i, k in enumerate('ABCD'):
        cx, cy = 290 + (i % 2) * 500, y0 + (i // 2) * gap
        im = spr(fr, pre + k, cx, cy, sc)
        put(fr, pill(k, 38, INK, (244, 246, 250, 245), (22, 6)), cx - 200, cy - gap / 2 + 40)
        if vals: put(fr, badge(vals[i], 40), cx - 130, cy - gap / 2 + 40)
        if foot: put(fr, pill(SIZE[k], 26, WHITE, (255, 255, 255, 30), (14, 5)), cx, cy + im.height / 2 + 26)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
fr = card(ROOM, DATE, 1, 7, '페인트에 담근 블록', '칠이 안 묻은 작은 큐브는 몇 개?')
grid(fr, 'b', 500, 0.62, 430)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '블록을 통째로 페인트 통에 담갔다 뺀다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 바닥까지 겉면이 전부 칠해진다', '2. 마른 뒤 작은 큐브로 하나하나 자른다',
                          ('3. 칠이 하나도 안 묻은 작은 큐브를 센다', YEL)], 33)
spr(fr, 'bC', 540, 800, 0.95)
text_lines(fr, 540, 1080, [('크기 = 가로 × 세로 × 높이 (작은 큐브 개수)', SOFT)], 32, center=True)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D의 칠 안 된 큐브 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 7개, B 3개, C 9개, D 1개라면', ('암호 7391', YEL), '',
                          ('칠이 한 면이라도 묻으면 세지 않아요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
grid(fr, 'b', 455, 0.5, 370)
fr.alpha_composite(panel(960, 110), (60, 1050))
text_lines(fr, 540, 1068, ['통째로 담가 바닥까지 칠함 · 작은 큐브로 자름', ('암호 = 칠 안 된 큐브 수 A B C D', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', '바닥을 빼먹으면 A가 6개?', CORAL)
fr.alpha_composite(panel(960, 290), (60, 300))
text_lines(fr, 100, 330, ['보이는 세 면만 생각하면 틀려요.', '바닥과 뒷면도 칠해졌으니', ('모든 방향에서 겉 한 겹을 벗겨야 해요', YEL)], 35)
spr(fr, 'bA', 540, 840, 0.85)
put(fr, pill(f'A: {SIZE["A"]} 블록', 30, WHITE, (255, 255, 255, 30), (18, 6)), 540, 1110)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '(가로-2) × (세로-2) × (높이-2)')
grid(fr, 'x', 480, 0.56, 400, list(CODE), foot=False)
text_lines(fr, 540, 1060, ['A 3×1×1=3 · B 2×2×1=4 · C 1×1×1=1 · D 2×2×2=8'], 30, center=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 3개 · B 4개 · C 1개 · D 8개')
grid(fr, 'x', 420, 0.4, 290, list(CODE), foot=False)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 880)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1030)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
