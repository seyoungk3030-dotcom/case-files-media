"""ROOM 032 cards in the 3D style (kit/style3d.py), from sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 32, '2026.10.22'
CODE = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))['unique_answer']
HIT = dict(zip('ABCD', CODE))
PTS = json.load(open(f'{B}/board.json'))
LCOL = {'1': (40, 200, 160), '2': (255, 160, 40), '3': (150, 130, 255), '4': (255, 90, 110)}


def lamp_pill(n, size=34): return pill(n, size, INK, (*LCOL[n], 250), (22, 8))


def board(fr, cx, cy, w, beams=False, show=None, tag=30):
    im = Image.open(f'{B}/{"beams" if beams else "board"}.png').convert('RGBA')
    bx = Image.open(f'{B}/board.png').getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox()
    im = im.crop(bx); sc = w / im.width
    im = im.resize((w, round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    for p in PTS:
        x, y = x0 + (p['x'] - bx[0]) * sc, y0 + (p['y'] - bx[1]) * sc
        if p['key'] in LCOL: put(fr, lamp_pill(p['key'], tag), x, y)
        else:
            put(fr, pill(p['key'], tag, INK, (244, 246, 250, 245), (22, 8)), x, y)
            if show: put(fr, badge(HIT[p['key']] if show == 'num' else '?', round(tag * 1.3)), x + 52 * w / 900, y - 40 * w / 900)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
# 1 hook
fr = card(ROOM, DATE, 1, 7, 'A B C D에 닿는 빛은?', '램프 네 개, 거울 여섯 개')
board(fr, 540, 745, 920, show='?')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules + example
fr = card(ROOM, DATE, 2, 7, '규칙은 두 가지', '빛은 곧게 가다가 거울에서 꺾인다')
fr.alpha_composite(panel(960, 220), (60, 290))
text_lines(fr, 100, 322, ['1. 거울을 만나면 빛은 90도 꺾인다 (앞뒤 모두)', '2. 빛끼리는 서로 막지 않고 지나간다',
                          ('3. 암호 = A B C D에 닿는 램프 번호', YEL)], 36)
ex = sprite(f'{B}/ex.png', width=560); put(fr, ex, 540, 745)
text_lines(fr, 540, 1000, ['오른쪽으로 가던 빛이 / 거울을 만나면', ('위로 꺾여요', YEL)], 36, center=True)
cta(fr, CTA4); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D에 닿는 빛의 램프 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 245), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 330), (60, 700))
text_lines(fr, 540, 735, ['예: A에 4번, B에 2번, C에 1번, D에 3번 빛이', ('닿는다면 암호는 4213', YEL), '',
                          ('램프마다 빛은 정확히 한 곳에 닿아요', SOFT)], 38, center=True)
cta(fr, CTA4); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
board(fr, 540, 640, 760)
fr.alpha_composite(panel(960, 180), (60, 990))
text_lines(fr, 100, 1012, ['램프는 모두 오른쪽으로 빛을 쏜다', '거울에서 90도 꺾이고, 빛끼리는 지나간다',
                           ('암호 = A B C D에 닿는 램프 번호', YEL)], 33, gap=1.5)
cta(fr, CTA4); save(fr, 4)

# 5 hint
fr = card(ROOM, DATE, 5, 7, '힌트', '한 번 꺾이고 끝나지 않는 빛이 있다', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('2번과 4번 빛은 거울을 여러 번 만나요.', WHITE), '4번 빛은 위로 꺾인 다음에도',
                          '거울 세 개를 더 지나요.', ('끝까지 따라가야 C가 보여요', YEL)], 36)
board(fr, 540, 905, 560, tag=24)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer reasoning
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '빛을 끝까지 따라가면')
board(fr, 540, 665, 700, beams=True, show='num')
fr.alpha_composite(panel(960, 170), (60, 990))
text_lines(fr, 540, 1012, ['1번 → B  ·  3번 → A  (거울 한 번)', ('2번 → D (세 번)  ·  4번 → C (네 번)', YEL)], 34, center=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', '마지막 거울까지 따라간 사람만 정답')
board(fr, 540, 610, 590, beams=True, show='num', tag=26)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 935)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1060)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
