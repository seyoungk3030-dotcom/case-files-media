"""ROOM 031 cards in the 3D style (kit/style3d.py), from sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 31, '2026.10.21'
CODE = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))['unique_answer']
TURNS = dict(zip('ABCD', CODE))
TAGS = {'S': 'S · 36', 'A': 'A · 12', 'B': 'B · 18', 'B2': '작은 기어 · 9', 'C': 'C · 6', 'D': 'D · 18'}
PTS = json.load(open(f'{B}/train.json'))
COLS = {'A': (109, 218, 197), 'B': (255, 180, 70), 'C': (160, 150, 255), 'D': (240, 120, 110)}


def letter(k): return pill(k, 34, INK, (*COLS[k], 245), (24, 8))


def train(fr, cx, cy, w, show=None, tag_size=28):
    im = Image.open(f'{B}/train.png').convert('RGBA')
    bx = im.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox(); im = im.crop(bx); sc = w / im.width
    im = im.resize((w, round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    for p in PTS:
        put(fr, pill(TAGS[p['key']], tag_size, INK, (244, 246, 250, 245)), x0 + (p['x'] - bx[0]) * sc, y0 + (p['y'] - bx[1]) * sc)
    if show:
        for p in PTS:
            if p['key'] in TURNS:
                dx, dy = (-60, -55) if p['key'] == 'C' else (70, -50)
                put(fr, badge(TURNS[p['key']] if show == 'num' else '?', 40), x0 + (p['x'] - bx[0] + dx) * sc, y0 + (p['y'] - bx[1] + dy) * sc)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


# 1 hook
fr = card(ROOM, DATE, 1, 7, 'S가 딱 한 바퀴 돌면?', 'A B C D는 각각 몇 바퀴 돌까')
train(fr, 540, 720, 900, '?')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules + example
fr = card(ROOM, DATE, 2, 7, '규칙은 두 가지', '톱니 수를 보면 바퀴 수가 보인다')
fr.alpha_composite(panel(960, 220), (60, 290))
text_lines(fr, 100, 322, ['1. 맞물린 기어: 톱니 수 × 바퀴 수가 같다', '2. 같은 축에 꽂힌 기어는 함께 돈다',
                          ('3. 암호 = A B C D가 도는 바퀴 수', YEL)], 36)
ex = sprite(f'{B}/ex.png', width=560); put(fr, ex, 540, 720)
put(fr, pill('톱니 12', 30, INK, (244, 246, 250, 245)), 455, 715); put(fr, pill('톱니 6', 30, INK, (244, 246, 250, 245)), 735, 715)
text_lines(fr, 540, 990, ['톱니 12개 기어가 1바퀴 돌면', ('톱니 6개 기어는 2바퀴 (12 × 1 = 6 × 2)', YEL)], 36, center=True)
cta(fr, '4장까지 풀고 댓글에 암호를 남겨주세요'); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'S가 1바퀴 돌 때 A → B → C → D의 바퀴 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, letter(k), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 330), (60, 700))
text_lines(fr, 540, 735, ['예: A 4바퀴, B 1바퀴, C 6바퀴, D 2바퀴라면', ('암호는 4162', YEL), '',
                          ('반 바퀴 같은 분수는 나오지 않아요', SOFT)], 38, center=True)
cta(fr, '4장까지 풀고 댓글에 암호를 남겨주세요'); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
train(fr, 540, 625, 760)
fr.alpha_composite(panel(960, 180), (60, 990))
text_lines(fr, 100, 1012, ['S가 딱 1바퀴 · 맞물리면 톱니 수 × 바퀴 수가 같다', '같은 축의 기어는 함께 돈다',
                           ('암호 = A B C D 바퀴 수', YEL)], 33, gap=1.5)
cta(fr, '4장까지 풀고 댓글에 암호를 남겨주세요'); save(fr, 4)

# 5 trap
fr = card(ROOM, DATE, 5, 7, '함정 주의', '전부 S와 바로 비교하면 3262', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('C와 D는 S와 맞물려 있지 않아요.', WHITE), 'C는 B 위에 꽂힌 작은 기어와 맞물리고,',
                          '작은 기어는 B와 같은 축이에요.', ('같은 축 = 같은 바퀴 수', YEL)], 36)
train(fr, 540, 905, 600, None, 22)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer reasoning
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '작은 기어가 B와 함께 2바퀴')
train(fr, 540, 625, 760, 'num')
fr.alpha_composite(panel(960, 170), (60, 990))
text_lines(fr, 540, 1012, ['A = 36 ÷ 12 = 3  ·  B = 36 ÷ 18 = 2', ('C = 2 × 9 ÷ 6 = 3  ·  D = 2 × 9 ÷ 18 = 1', YEL)], 34, center=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', '같은 축을 찾은 사람만 정답')
train(fr, 540, 580, 680, 'num', 24)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 935)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1060)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
