"""ROOM 041 cards in the 3D style (kit/style3d.py), from the seesaw sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 41, '2026.10.25'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
KEYS = dict(zip('ABCD', 'ctsr')); NAME = {'c': '공', 't': '피라미드', 's': '큐브', 'r': '별'}


def spr(fr, name, cx, cy, w=None, h=None):
    im = trim(Image.open(f'{B}/{name}.png').convert('RGBA'))
    if w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    else: im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))); return im


def scales(fr, y0, w, gap):
    for i in range(4):
        cy = y0 + i * gap; spr(fr, f'scale{i + 1}', 590, cy, w)
        put(fr, text_layer(f'저울 {i + 1}', 30, SOFT, 'Bold'), 105, cy + 20)


def legend(fr, y, marks=None, h=90):
    for n, k in enumerate('ABCD'):
        cx = 165 + n * 250; spr(fr, f'icon-{KEYS[k]}', cx, y, h=h)
        put(fr, pill(k, 32, INK, (244, 246, 250, 245), (18, 6)), cx - 70, y - 40)
        if marks: put(fr, badge(marks[n], 38), cx + 70, y - 40)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
# 1 hook
fr = card(ROOM, DATE, 1, 7, '저울 네 개가 알려주는 순서', 'A B C D는 무거운 순서로 몇 등?')
scales(fr, 385, 600, 190)
legend(fr, 1115, h=76)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules
fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '내려간 쪽이 더 무겁다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 같은 모양은 무게도 같다', '2. 수평이면 양쪽이 같고, 기울면 내려간 쪽이 무겁다',
                          ('3. 암호 = A B C D의 순위 (가장 무거우면 1등)', YEL)], 33)
legend(fr, 680, h=110)
for n, k in enumerate('ABCD'): put(fr, text_layer(NAME[KEYS[k]], 32, WHITE, 'Bold'), 165 + n * 250, 780)
spr(fr, 'scale2', 540, 950, 760)
cta(fr, CTA4); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D의 무게 순위')
legend(fr, 500, list('????'), h=110)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 무거운 순서가 큐브, 별, 공, 피라미드라면', ('A 3등, B 4등, C 1등, D 2등 → 암호 3412', YEL), '',
                          ('네 모양의 무게는 모두 다르다', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
scales(fr, 375, 580, 182)
fr.alpha_composite(panel(960, 110), (60, 1045))
text_lines(fr, 540, 1062, ['같은 모양 = 같은 무게 · 내려간 쪽이 무겁다', ('암호 = A공 B피라미드 C큐브 D별의 순위', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

# 5 hint
fr = card(ROOM, DATE, 5, 7, '힌트와 함정', f'가벼운 순서로 적으면 {PROOF["trap_lightest_first"]} (오답)', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('모든 모양을 "공 몇 개"로 바꿔 보세요.', WHITE), '저울 1에서 큐브가 공 몇 개인지,', '저울 2와 3에서 피라미드가 공 몇 개쯤인지,',
                          ('1등은 가장 무거운 것이에요', YEL)], 35)
legend(fr, 850, h=110)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '모두 공 몇 개로 바꾸면')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 318, ['저울 1  큐브 = 공 2개', '저울 2·3  공 3개 < 피라미드 < 큐브 2개(공 4개)', '저울 4  별 2개 = 피라미드 → 별은 공 1.5~2개',
                          ('피라미드 > 큐브 > 별 > 공', YEL)], 33)
legend(fr, 850, list(CODE), h=110)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 4등 · B 1등 · C 2등 · D 3등')
legend(fr, 560, list(CODE), h=130)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 820)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 970)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
