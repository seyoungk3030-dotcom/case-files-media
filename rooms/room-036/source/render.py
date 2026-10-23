"""ROOM 036 cards in the 3D style (kit/style3d.py), from sprites made by scene3d.py plus a drawn swap chart."""
import json, os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import SWAPS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 36, '2026.10.23'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
CCOL = {'A': (40, 200, 160), 'B': (255, 160, 40), 'C': (240, 100, 90), 'D': (150, 130, 255)}
GOLD = (255, 200, 90, 255)


def chart(w=900, row=96, title=True):
    """4 swap steps: spot dots 1-4 and an arc joining the two swapped spots."""
    h = row * len(SWAPS) + 10; lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    x0 = 400; dx = (w - x0 - 50) / 3
    for r, (a, b) in enumerate(SWAPS):
        cy = r * row + row * 0.62
        lay.alpha_composite(text_layer(f'{r + 1}단계', 34, SOFT, 'Bold'), (10, int(cy - 26)))
        lay.alpha_composite(text_layer(f'자리 {a} ↔ {b}', 34, WHITE, 'Bold'), (120, int(cy - 26)))
        xa, xb = x0 + (a - 1) * dx, x0 + (b - 1) * dx
        d.arc((xa, cy - 52, xb, cy + 8), 190, 350, fill=GOLD, width=6)
        for k in range(4):
            x = x0 + k * dx; on = k + 1 in (a, b)
            d.ellipse((x - 22, cy - 22, x + 22, cy + 22), fill=GOLD if on else (60, 74, 96, 255))
            t = text_layer(str(k + 1), 26, INK if on else SOFT, 'Black', shadow=False)
            lay.alpha_composite(t, (int(x - t.width / 2), int(cy - t.height / 2)))
    return lay


def cups(fr, name, cx, cy, w, labels=True, show=None):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); sc = w / im.width
    im = im.resize((w, round(im.height * sc)), Image.LANCZOS); x0, y0 = cx - w / 2, cy - im.height / 2
    fr.alpha_composite(im, (int(x0), int(y0)))
    for p in json.load(open(f'{B}/{name}.json')):
        x, y = x0 + p['x'] * sc, y0 + p['y'] * sc
        if p['key'].isdigit(): put(fr, pill(f"자리 {p['key']}", round(w / 34), INK, (244, 246, 250, 240), (12, 4)), x, y)
        elif labels: put(fr, text_layer(p['key'], round(w / 14), WHITE, 'Black'), x, y)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


chart().save(f'{B}/swaps.png')
CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
# 1 hook
fr = card(ROOM, DATE, 1, 7, '컵 4개, 자리 바꾸기 4번', 'A B C D는 마지막에 몇 번 자리에?')
cups(fr, 'start', 540, 470, 900)
fr.alpha_composite(panel(960, 420), (60, 690)); fr.alpha_composite(chart(), (90, 700))
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules
fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '바꾸는 기준은 글자가 아니라 자리')
fr.alpha_composite(panel(960, 220), (60, 290))
text_lines(fr, 100, 322, ['1. "자리 1 ↔ 2"는 그 두 자리에 있는 컵끼리 바꾼다', '2. 1단계부터 4단계까지 순서대로',
                          ('3. 암호 = A B C D가 마지막에 선 자리 번호', YEL)], 34)
cups(fr, 'start', 540, 680, 760)
put(fr, text_layer('자리 1 ↔ 2를 하면', 38, WHITE, 'Bold'), 540, 890)
put(fr, text_layer('A B C D  →  B A C D', 56, YEL, 'Black'), 540, 980)
text_lines(fr, 540, 1060, [('지금 1번 자리에 있는 컵이 2번 자리로', SOFT)], 32, center=True)
cta(fr, CTA4); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D의 마지막 자리 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (*CCOL[k], 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 330), (60, 700))
text_lines(fr, 540, 735, ['예: 마지막에 C A D B 순서로 서 있다면', ('A는 2, B는 4, C는 1, D는 3 → 암호 2413', YEL), '',
                          ('자리 번호는 왼쪽부터 1, 2, 3, 4', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
cups(fr, 'start', 540, 450, 860)
fr.alpha_composite(panel(960, 420), (60, 640)); fr.alpha_composite(chart(), (90, 650))
text_lines(fr, 540, 1085, [('자리 기준으로 바꾸기 · 암호 = A B C D의 마지막 자리', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

# 5 trap
fr = card(ROOM, DATE, 5, 7, '함정 주의', f'글자끼리 바꾸면 {PROOF["trap_swap_letters"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('"자리 1 ↔ 3"은 A와 C를 바꾸라는 뜻이 아니에요.', WHITE), '그 순간 1번과 3번 자리에 서 있는',
                          '컵끼리 바꿔요. 컵이 움직일수록', ('자리에 선 글자가 달라져요', YEL)], 35)
cups(fr, 'start', 540, 860, 820)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer steps
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '자리마다 서 있는 컵을 따라가면')
rows = [('처음', 'A B C D')] + [(f'{i + 1}단계  자리 {a}↔{b}', ' '.join(s)) for i, ((a, b), s) in enumerate(zip(SWAPS, PROOF['steps']))]
fr.alpha_composite(panel(960, 420), (60, 300))
for i, (l, s) in enumerate(rows):
    y = 345 + i * 78
    lay = text_layer(l, 34, SOFT, 'Bold'); fr.alpha_composite(lay, (110, int(y - lay.height / 2)))
    put(fr, text_layer(s, 46, YEL if i == len(rows) - 1 else WHITE, 'Black'), 760, y)
cups(fr, 'final', 540, 900, 860)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A는 2, B는 4, C는 3, D는 1번 자리')
cups(fr, 'final', 540, 560, 900)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 870)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1010)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
