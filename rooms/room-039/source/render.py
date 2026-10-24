"""ROOM 039 cards in the 3D style (kit/style3d.py), from the tray and piece sprites made by scene3d.py."""
import json, os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 39, '2026.10.24'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
PC = {'1': (40, 200, 160), '2': (255, 160, 40), '3': (240, 100, 90), '4': (150, 130, 255)}


def spr(fr, name, cx, cy, w, tags=None):
    im = Image.open(f'{B}/{name}.png').convert('RGBA')
    l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 60 else 0).getbbox()
    pts = json.load(open(f'{B}/{name}.json')); t2 = t; b = max(b, max(p['y'] for p in pts) + 30)
    im = im.crop((l, t2, r, b)); sc = w / im.width; im = im.resize((w, round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - w / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    for p in pts:
        x, y = x0 + (p['x'] - l) * sc, y0 + (p['y'] - t2) * sc; k = p['key']
        if tags == 'holes': put(fr, pill(k, 34, INK, (244, 246, 250, 245), (20, 6)), x, y)
        elif tags == 'pieces': put(fr, badge(k, 30), x, y)
    return im.height


def mini(cells, cell=34, col=(150, 130, 255)):
    W = max(x for x, _ in cells) + 1; H = max(y for _, y in cells) + 1
    lay = Image.new('RGBA', (W * cell + 4, H * cell + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for x, y in cells:
        X, Y = x * cell + 2, (H - 1 - y) * cell + 2; d.rounded_rectangle((X, Y, X + cell - 3, Y + cell - 3), 6, fill=(*col, 255))
    return lay


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
# 1 hook
fr = card(ROOM, DATE, 1, 7, '구멍 네 개, 조각 네 개', '돌리기만 하고 뒤집지 않는다면?')
spr(fr, 'tray', 540, 470, 1000, 'holes')
spr(fr, 'pieces', 540, 820, 1000, 'pieces')
text_lines(fr, 540, 1050, [('A B C D에 들어갈 조각 번호가 암호', SOFT)], 34, center=True)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules
fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '조각 윗면에만 색이 칠해져 있다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 조각은 바닥에 댄 채로 돌릴 수만 있다', '2. 뒤집기는 안 된다 (색칠된 면이 위로)',
                          ('3. 구멍 하나에 조각 하나', YEL)], 34)
P = {(0, 0), (0, 1), (0, 2), (1, 1), (1, 2)}
for cx, cells, lab, col in ((210, P, '처음', WHITE), (540, {(y, 1 - x) for x, y in P}, '돌리기 O', MINT),
                            (870, {(1 - x, y) for x, y in P}, '뒤집기 X', CORAL)):
    mn = min(x for x, _ in cells), min(y for _, y in cells); cells = {(x - mn[0], y - mn[1]) for x, y in cells}
    put(fr, mini(cells, 46), cx, 700); put(fr, text_layer(lab, 38, col, 'Black'), cx, 860)
text_lines(fr, 540, 960, [('예시 조각은 이번 문제와 상관없어요', SOFT)], 32, center=True)
cta(fr, CTA4); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 구멍에 들어갈 조각 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A에 2번, B에 1번, C에 4번, D에 3번이면', ('암호 2143', YEL), '',
                          ('조각은 한 번씩만 쓴다', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
spr(fr, 'tray', 540, 450, 1000, 'holes')
spr(fr, 'pieces', 540, 790, 1000, 'pieces')
fr.alpha_composite(panel(960, 120), (60, 990))
text_lines(fr, 540, 1012, ['돌리기 O · 뒤집기 X · 구멍 하나에 조각 하나', ('암호 = A B C D에 들어갈 조각 번호', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

# 5 trap
fr = card(ROOM, DATE, 5, 7, '함정 주의', f'뒤집어도 된다면 {PROOF["trap"]}도 맞아 보인다', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('두 조각이 서로 거울에 비친 모양이에요.', WHITE), '뒤집을 수 있다면 어느 구멍에도 들어가지만',
                          '돌리기만 해서는 딱 한 구멍에만 맞아요.', ('머릿속으로 돌려보세요', YEL)], 35)
spr(fr, 'pieces', 540, 900, 960, 'pieces')
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '돌려서 끼우면 딱 맞는 자리')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 540, 318, ['A ㄴ자 → 3번을 반 바퀴 돌리면 ㄴ', 'B ㅗ자 → 4번 · D 번개 모양 → 2번', 'C 거울 ㄴ자 → 1번',
                          ('3번과 1번은 뒤집어야만 서로 바뀐다', YEL)], 34, center=True)
spr(fr, 'solved', 540, 830, 1000, 'holes')
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A는 3번, B는 4번, C는 1번, D는 2번')
spr(fr, 'solved', 540, 520, 1000, 'holes')
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 800)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 950)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
