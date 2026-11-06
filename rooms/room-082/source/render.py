"""ROOM 082 cards in the 3D style (kit/style3d.py), from the pegboard sprites made by scene3d.py. q*/r*.png are the
sprites with two faint corner pixels so the reel (short3d.py) scales all four the same."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 82, '2026.11.11'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
for k in 'ABCD':
    for s, d in (('p', 'q'), ('a', 'r')):
        im = Image.open(f'{B}/{s}{k}.png').convert('RGBA'); im.putpixel((0, 0), (255, 255, 255, 44)); im.putpixel((799, 759), (255, 255, 255, 44))
        im.save(f'{B}/{d}{k}.png')


def grid(fr, pre, y0=300, size=420, vals=None, gap=430):
    for i, k in enumerate('ABCD'):
        im = Image.open(f'{B}/{pre}{k}.png').resize((size, size * 760 // 800), Image.LANCZOS); x, y = 300 + (i % 2) * 480 - size // 2, y0 + (i // 2) * gap
        fr.alpha_composite(im, (x, y)); put(fr, pill(k, 38, INK, (244, 246, 250, 245), (20, 6)), x + 20, y + 30)
        if vals: put(fr, badge(vals[i], 44), x + size - 30, y + 30)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '고무줄 안쪽 넓이는 작은 칸 몇 개?')
grid(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '못이 1칸 간격으로 박힌 판에 고무줄을 걸었어요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 못 4개가 만드는 작은 정사각형 = 1칸', '2. 반만 덮인 칸은 반 칸으로 쳐요',
                          '3. 답은 모두 딱 떨어지는 한 자리 수', ('고무줄 안쪽 넓이는 몇 칸?', YEL)], 33)
im = Image.open(f'{B}/pC.png').resize((480, 456), Image.LANCZOS); fr.alpha_composite(im, (300, 650))
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 넓이(칸 수)')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 넓이가 2 · 9 · 4 · 3칸이면', ('암호 2943', YEL), '', ('안쪽 못 개수가 아니라 넓이예요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '기울어진 변은 반 칸 조각을 만들어요')
grid(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '바깥 직사각형에서 빼 보세요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('도형을 감싸는 직사각형을 그려요', WHITE), '직각삼각형은 직사각형의 절반이에요.', '바깥 넓이 − 빈 삼각형들 = 고무줄 넓이',
                          ('B: 4×4 = 16에서 빈 곳을 빼요!', YEL)], 35)
im = Image.open(f'{B}/pB.png').resize((480, 456), Image.LANCZOS); fr.alpha_composite(im, (300, 650))
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '6칸 · 8칸 · 5칸 · 7칸')
grid(fr, 'a', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '직사각형에서 빈 삼각형을 빼요')
for i, k in enumerate('ABCD'):
    im = Image.open(f'{B}/a{k}.png').resize((230, 218), Image.LANCZOS); cx = 165 + i * 250
    fr.alpha_composite(im, (cx - 115, 380)); put(fr, badge(CODE[i], 46), cx, 650)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 860)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 990)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
