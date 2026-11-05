"""ROOM 064 cards in the 3D style (kit/style3d.py), from the bar magnet sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 64, '2026.11.06'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']


def spr(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()
    im = im.crop((max(l - 10, 0), max(t - 10, 0), r + 10, b + 10)); sc = w / im.width
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag:
        put(fr, pill(name[1], 38, INK, (244, 246, 250, 245), (20, 6)), x0 + 12, y0 + im.height - 40)
        if val: put(fr, badge(val, 38), x0 + 82, y0 + im.height - 40)


def grid(fr, pre, y0, w=380, gap=380, vals=None, dx=480):
    for i, k in enumerate('ABCD'):
        spr(fr, pre + k, 540 - dx / 2 + (i % 2) * dx, y0 + (i // 2) * gap, w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'


def rows(fr, pre, y0, w, gap, vals=None):
    for i, k in enumerate('ABCD'):
        spr(fr, pre + k, 540, y0 + i * gap, w, val=vals[i] if vals else None)


fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '다 붙고 나면 자석은 몇 조각?')
rows(fr, 'p', 470, 940, 190)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '막대자석은 한쪽이 N, 반대쪽이 S')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 맞닿은 끝이 N-S면 딱 붙는다', '2. N-N, S-S면 서로 밀어내 떨어진다',
                          ('3. 다 끝나고 남는 조각은 몇 개?', YEL)], 34)
spr(fr, 'pA', 540, 700, 960, tag=False)
spr(fr, 'aA', 540, 900, 960, tag=False)
put(fr, text_layer('↓ 이렇게 6조각', 34, SOFT, 'Bold'), 540, 805)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 남는 조각 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 2조각 · B 5조각 · C 1조각 · D 8조각이면', ('암호 2518', YEL), '',
                          ('A는 2장에서 보여드렸어요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
rows(fr, 'p', 400, 940, 170)
fr.alpha_composite(panel(960, 110), (60, 960))
text_lines(fr, 540, 978, ['N-S = 붙음 · N-N, S-S = 밀어냄', ('암호 = 남는 조각 수 A B C D', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', f'같은 극끼리 붙는다고 하면 {PROOF["trap_rule_swapped"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('맞닿은 두 끝만 보세요.', WHITE), '빨강-파랑이 만나면 붙고,', '같은 색이 만나면 떨어져요.',
                          ('떨어지는 곳 수 + 1 = 조각 수', YEL)], 35)
spr(fr, 'pC', 540, 880, 960, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '붙을 곳은 붙고, 같은 극은 떨어진 모습')
fr.alpha_composite(panel(960, 160), (60, 280))
text_lines(fr, 540, 300, ['떨어지는 곳 수 + 1', ('A 6 · B 4 · C 7 · D 3', YEL)], 31, center=True)
rows(fr, 'a', 560, 940, 170, list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 6 · B 4 · C 7 · D 3')
rows(fr, 'a', 360, 900, 150, list(CODE))
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 975)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
