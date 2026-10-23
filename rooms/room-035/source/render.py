"""ROOM 035 cards in the 3D style (kit/style3d.py), from sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import SIL
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 35, '2026.10.23'
CODE = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))['unique_answer']
ANS = dict(zip('ABCD', CODE))
TCOL = {1: (40, 200, 160), 2: (255, 160, 40), 3: (240, 100, 90), 4: (150, 130, 255)}
DIR = {'front': '앞에서', 'right': '오른쪽에서', 'top': '위에서'}
WHITE_BG = (244, 246, 250, 245)


def tower(fr, n, cx, cy, w, tags=True, size=24):
    im = Image.open(f'{B}/t{n}.png').convert('RGBA')
    bx = im.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox(); im = im.crop(bx); sc = w / im.width
    im = im.resize((w, round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - w / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tags:
        for p in json.load(open(f'{B}/t{n}.json')):
            put(fr, pill('앞' if p['key'] == 'front' else '오른쪽', size, INK, (190, 200, 214, 235), (10, 3)), x0 + (p['x'] - bx[0]) * sc, y0 + (p['y'] - bx[1]) * sc)
    put(fr, pill(str(n), round(size * 1.5), INK, (*TCOL[n], 250), (20, 6)), cx, y0 - 30)


def sil(fr, k, cx, cy, w, show=None, size=30):
    put(fr, sprite(f'{B}/sil-{k}.png', width=w), cx, cy)
    put(fr, pill(k, size, INK, WHITE_BG, (20, 6)), cx - w * 0.38, cy - w * 0.6)
    put(fr, pill(DIR[SIL[k][0]], round(size * 0.8), INK, (255, 214, 120, 245), (12, 4)), cx + w * 0.12, cy - w * 0.6)
    if show: put(fr, badge(ANS[k] if show == 'num' else '?', round(size * 1.3)), cx + w * 0.5, cy + w * 0.45)


def towers(fr, y, w=235, tags=False):
    for n in range(1, 5): tower(fr, n, 165 + (n - 1) * 250, y, w, tags)


def sils(fr, y, w=170, show=None):
    for i, k in enumerate('ABCD'): sil(fr, k, 165 + i * 250, y, w, show)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
# 1 hook
fr = card(ROOM, DATE, 1, 7, '이 모습은 몇 번 탑?', '보는 방향이 적힌 그림자 4개')
towers(fr, 480); sils(fr, 870, show='?')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules
fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '그림자 = 그 방향에서 본 모양')
fr.alpha_composite(panel(960, 220), (60, 290))
text_lines(fr, 100, 322, ['1. A~D는 적힌 방향에서 본 탑의 모양', '2. 모든 탑의 앞과 오른쪽은 아래 그림과 같다',
                          ('3. 암호 = A B C D에 맞는 탑 번호', YEL)], 36)
tower(fr, 1, 330, 760, 380, tags=True, size=30)
put(fr, sprite(f'{B}/sil-exF.png', width=220), 800, 780)
put(fr, pill('1번을 앞에서 본 모양', 28, INK, (255, 214, 120, 245), (14, 5)), 800, 635)
text_lines(fr, 540, 1020, ['앞에서 보면 줄마다 가장 높은 블록까지 보여요', ('위에서 보면 앞줄이 그림의 아래쪽이에요', YEL)], 34, center=True)
cta(fr, CTA4); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D에 맞는 탑 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, WHITE_BG, (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 330), (60, 700))
text_lines(fr, 540, 735, ['예: A는 3번, B는 1번, C는 4번, D는 2번 탑이라면', ('암호는 3142', YEL), '',
                          ('그림자마다 맞는 탑은 딱 하나예요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
towers(fr, 470); sils(fr, 840)
fr.alpha_composite(panel(960, 120), (60, 1045))
text_lines(fr, 540, 1068, ['왼쪽 아래 면이 앞, 오른쪽 아래 면이 오른쪽', ('암호 = A B C D에 맞는 탑 번호', YEL)], 32, center=True, gap=1.45)
cta(fr, CTA4); save(fr, 4)

# 5 trap
fr = card(ROOM, DATE, 5, 7, '함정 주의', '오른쪽에서 보면 앞줄이 왼쪽에 온다', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('오른쪽에서 볼 때는 탑의 오른쪽 면 앞에 서요.', WHITE), '그러면 앞줄은 왼쪽, 뒷줄은 오른쪽에 보여요.',
                          '좌우를 뒤집어 읽으면', ('맞는 탑이 없어져요', YEL)], 35)
tower(fr, 1, 360, 900, 300, tags=True)
put(fr, sprite(f'{B}/sil-exR.png', width=210), 790, 900)
put(fr, pill('1번을 오른쪽에서', 28, INK, (255, 214, 120, 245), (14, 5)), 790, 760)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '그림자와 탑을 짝지으면')
for i, k in enumerate('ABCD'):
    cx = 165 + i * 250; n = int(ANS[k])
    sil(fr, k, cx, 470, 160)
    put(fr, text_layer('↓', 50, MINT), cx, 590)
    tower(fr, n, cx, 815, 225, tags=False)
fr.alpha_composite(panel(960, 130), (60, 1000))
text_lines(fr, 540, 1022, ['A(앞) 2번 · B(오른쪽) 4번', ('C(위) 1번 · D(앞) 3번', YEL)], 34, center=True, gap=1.45)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', '방향까지 따진 사람만 정답')
for i, k in enumerate('ABCD'): tower(fr, int(ANS[k]), 165 + i * 250, 600, 235, tags=False)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 870)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1010)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
