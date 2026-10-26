"""ROOM 044 cards in the 3D style (kit/style3d.py), from the paper sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import SETUPS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 44, '2026.10.26'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_layers_times_holes']
FOLD = {k: f'{len(SETUPS[k][0])}번 접기 · {2 ** len(SETUPS[k][0])}겹' for k in 'ABCD'}


def spr(fr, name, cx, cy, sc):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox()
    im = im.crop((l, t, r, b)); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))); return im


def grid(fr, pre, y0, sc, gap, vals=None, foot=True):
    for i, k in enumerate('ABCD'):
        cx, cy = 290 + (i % 2) * 500, y0 + (i // 2) * gap
        im = spr(fr, pre + k, cx, cy, sc)
        put(fr, pill(k, 38, INK, (244, 246, 250, 245), (22, 6)), cx - im.width / 2 - 10, cy - im.height / 2 - 6)
        if vals: put(fr, badge(vals[i], 40), cx + im.width / 2 + 4, cy - im.height / 2 - 6)
        if foot: put(fr, pill(FOLD[k], 24, WHITE, (255, 255, 255, 30), (14, 5)), cx, cy + im.height / 2 + 30)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
# 1 hook
fr = card(ROOM, DATE, 1, 7, '접어서 뚫은 구멍', '종이를 펼치면 구멍은 몇 개?')
grid(fr, 'f', 510, 0.64, 420)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules
fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '정사각형 종이를 접고 구멍을 뚫는다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 오른쪽 반을 왼쪽으로 접기 (B·D는 위를 아래로 한 번 더)', '2. 접힌 채로 그림처럼 구멍을 뚫는다',
                          ('3. 민트 = 접힌 선, 점선 = 원래 종이', YEL)], 32)
spr(fr, 'fB', 540, 800, 0.95)
text_lines(fr, 540, 1080, [('B: 두 번 접어 4겹, 구멍 2개를 뚫었다', SOFT)], 32, center=True)
cta(fr, CTA4); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', '종이를 다 펼쳤을 때 구멍 수 A → B → C → D')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 구멍 7개, B 3개, C 9개, D 1개라면', ('암호 7391', YEL), '',
                          ('다 펼친 종이에 보이는 구멍을 센다', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
grid(fr, 'f', 480, 0.6, 380)
fr.alpha_composite(panel(960, 110), (60, 1050))
text_lines(fr, 540, 1068, ['민트 = 접힌 선 · 점선 = 원래 종이 크기', ('암호 = 펼쳤을 때 구멍 수 A B C D', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

# 5 trap
fr = card(ROOM, DATE, 5, 7, '함정 주의', f'구멍 × 겹 수로 세면 {TRAP}', CORAL)
fr.alpha_composite(panel(960, 290), (60, 300))
text_lines(fr, 100, 330, ['"2겹이니까 구멍도 2배"는 보통 구멍만 맞아요.', '접힌 선 위에 뚫은 반달 구멍은', ('펼치면 두 개가 아니라 하나로 이어져요', YEL)], 35)
spr(fr, 'fC', 540, 840, 0.9)
put(fr, pill('C: 접힌 선 위의 반달 구멍', 30, WHITE, (255, 255, 255, 30), (18, 6)), 540, 1100)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '접힌 선 위 구멍은 펼쳐도 1개')
grid(fr, 'u', 500, 0.5, 400, list(CODE), foot=False)
text_lines(fr, 540, 1050, ['A 1×2=2 · B 2×4=8 · C 1+2=3 · D 1+4=5', ('노란 원 = 접힌 선에서 하나로 이어진 구멍', SOFT)], 30, center=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 2개 · B 8개 · C 3개 · D 5개')
grid(fr, 'u', 420, 0.36, 290, list(CODE), foot=False)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 880)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1030)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
