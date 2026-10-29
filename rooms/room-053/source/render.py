"""ROOM 053 cards in the 3D style (kit/style3d.py), from the seesaw sprites made by scene3d.py."""
import json, os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 53, '2026.10.29'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_object_count']


def spr(fr, name, cx, cy, sc):
    im = Image.open(f'{B}/{name}.png').convert('RGBA')
    l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()   # the seesaw without its soft shadow
    m = 40; im = im.crop((max(0, l - m), max(0, t - m), min(im.width, r + m), min(im.height, b + m)))
    ys, xs = np.mgrid[0:im.height, 0:im.width]
    fade = np.clip(np.minimum.reduce([xs, ys, im.width - 1 - xs, im.height - 1 - ys]) / m, 0, 1)
    a = np.asarray(im.getchannel('A'), dtype=float) * fade; im.putalpha(Image.fromarray(a.astype('uint8')))
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))); return im


def icon(fr, k, cx, cy, h):
    im = trim(Image.open(f'{B}/icon-{k}.png').convert('RGBA')); im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def board(fr, y0, sc, gap, vals=None):
    for i, n in enumerate(('ref1', 'ref2')):
        spr(fr, n, 290 + i * 500, y0, sc)
    put(fr, pill('힌트', 30, INK, (109, 218, 197, 245), (22, 6)), 540, y0 - 95 * sc / 0.5)
    for i, k in enumerate('ABCD'):
        cx, cy = 290 + (i % 2) * 500, y0 + gap * (1 + i // 2)
        spr(fr, 'q' + k, cx, cy, sc)
        put(fr, pill(k, 36, INK, (244, 246, 250, 245), (22, 6)), cx - 190, cy - 70 * sc / 0.5)
        if vals: put(fr, badge(vals[i], 40), cx + 205, cy - 70 * sc / 0.5)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
fr = card(ROOM, DATE, 1, 7, '저울 퍼즐', '물음표 자리엔 공이 몇 개 있어야 평평할까?')
board(fr, 430, 0.55, 250)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '평평한 저울 = 양쪽 무게가 같다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 같은 모양은 무게가 같다', '2. 위 두 저울(힌트)은 평평하게 맞춰져 있다',
                          ('3. 물음표 자리에 공 몇 개면 평평해질까?', YEL)], 33)
spr(fr, 'ref1', 540, 760, 0.95)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 저울의 공 개수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
icon(fr, 'c', 540, 760, 120)
fr.alpha_composite(panel(960, 150), (60, 880))
text_lines(fr, 540, 915, ['예: A 공 2개, B 6개, C 3개, D 8개라면', ('암호 2638', YEL)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '힌트와 저울은 이것이 전부')
board(fr, 400, 0.55, 250)
fr.alpha_composite(panel(960, 110), (60, 1050))
text_lines(fr, 540, 1068, ['같은 모양 = 같은 무게 · 위 두 저울이 힌트', ('암호 = 물음표에 들어갈 공 개수 A B C D', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', f'물건 개수만 세면 {TRAP}?', CORAL)
fr.alpha_composite(panel(960, 220), (60, 300))
text_lines(fr, 100, 330, ['물건이 몇 개인지가 아니라 무게예요.', '모든 모양을 공 몇 개인지로 바꿔 보세요.',
                          ('상자는 공 몇 개? 별은 공 몇 개?', YEL)], 35)
spr(fr, 'ref2', 540, 820, 0.95)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '상자 = 공 3 · 별 = 상자 + 공 2 = 공 5')
board(fr, 400, 0.55, 250, list(CODE))
fr.alpha_composite(panel(960, 110), (60, 1050))
text_lines(fr, 540, 1068, ['A 별 5 · B 3+3+1 = 7', ('C 3+1 = 4 · D 5+3+1 = 9', YEL)], 30, center=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '공 1 · 상자 3 · 별 5')
for n, (k, v) in enumerate((('c', 1), ('s', 3), ('r', 5))):
    cx = 270 + n * 270; icon(fr, k, cx, 520, 150); put(fr, badge(v, 40), cx, 650)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 840)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 990)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
