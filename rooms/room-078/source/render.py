"""ROOM 078 cards in the 3D style (kit/style3d.py), from the cube-cut sprites made by scene3d.py. q*/r*.png are the
sprites with two faint corner pixels so the reel (short3d.py) scales all four the same."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 78, '2026.11.10'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
for k in 'ABCD':
    for s, d in (('p', 'q'), ('a', 'r')):
        im = Image.open(f'{B}/{s}{k}.png').convert('RGBA'); im.putpixel((0, 0), (255, 255, 255, 44)); im.putpixel((799, 799), (255, 255, 255, 44))
        im.save(f'{B}/{d}{k}.png')


def grid(fr, pre, y0=300, size=420, vals=None, gap=430):
    for i, k in enumerate('ABCD'):
        im = Image.open(f'{B}/{pre}{k}.png').resize((size, size), Image.LANCZOS); x, y = 300 + (i % 2) * 480 - size // 2, y0 + (i // 2) * gap
        fr.alpha_composite(im, (x, y)); put(fr, pill(k, 38, INK, (244, 246, 250, 245), (20, 6)), x + 20, y + 30)
        if vals: put(fr, badge(vals[i], 44), x + size - 30, y + 30)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '빨간 점 세 개를 지나게 자르면 단면은 몇 각형?')
grid(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '유리 정육면체를 평평한 칼로 한 번 잘라요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 칼은 빨간 점 세 개를 모두 지나요', '2. 점은 모서리 위나 꼭짓점에 있어요',
                          '3. 자른 면(단면)의 변 개수를 세요', ('삼각형 3 · 사각형 4 · 오각형 5 · 육각형 6', YEL)], 33)
im = Image.open(f'{B}/pB.png').resize((480, 480), Image.LANCZOS); fr.alpha_composite(im, (300, 640))
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 단면의 변 개수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 260), (60, 700))
text_lines(fr, 540, 735, ['예: 사각형 · 삼각형 · 사각형 · 오각형이면', ('암호 4345', YEL)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '점이 세 개라고 삼각형은 아니에요')
grid(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '단면의 꼭짓점은 모두 모서리 위에 있어요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('칼은 빨간 점에서 멈추지 않아요', WHITE), '평면을 계속 늘려 보세요.', '평면이 지나는 모서리를 모두 세면',
                          ('그게 단면의 변 개수예요!', YEL)], 35)
im = Image.open(f'{B}/pA.png').resize((480, 480), Image.LANCZOS); fr.alpha_composite(im, (300, 650))
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '육각형 · 삼각형 · 오각형 · 사각형')
grid(fr, 'a', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '평면이 지나는 모서리를 모두 세요')
for i, k in enumerate('ABCD'):
    im = Image.open(f'{B}/a{k}.png').resize((230, 230), Image.LANCZOS); cx = 165 + i * 250
    fr.alpha_composite(im, (cx - 115, 380)); put(fr, badge(CODE[i], 46), cx, 650)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 860)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 990)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
