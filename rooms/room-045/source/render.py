"""ROOM 045 cards in the 3D style (kit/style3d.py), from the gear sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import SETUPS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 45, '2026.10.26'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_ignore_direction']


def spr(fr, name, cx, cy, sc):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); im = im.crop(im.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox())
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)   # same scale for all: sizes compare
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))); return im


def grid(fr, pre, y0, sc, gap, vals=None):
    for i, k in enumerate('ABCD'):
        cx, cy = 290 + (i % 2) * 500, y0 + (i // 2) * gap
        im = spr(fr, pre + k, cx, cy, sc)
        put(fr, pill(k, 38, INK, (244, 246, 250, 245), (22, 6)), cx - 215, cy - gap / 2 + 40)
        if vals: put(fr, badge(vals[i], 40), cx - 145, cy - gap / 2 + 40)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
# 1 hook
fr = card(ROOM, DATE, 1, 7, '노란 기어를 ¼바퀴', '빨간 화살표는 몇 번을 가리킬까?')
grid(fr, 'g', 530, 0.57, 440)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules
fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '노란 기어만 손으로 돌린다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 노란 기어를 시계 방향으로 ¼바퀴 돌린다', '2. 기어 가운데 숫자 = 톱니 개수',
                          ('3. 민트 기어의 빨간 화살표가 가리키는 숫자를 본다', YEL)], 32)
spr(fr, 'gA', 540, 800, 1.0)
text_lines(fr, 540, 1090, [('화살표는 처음에 모두 1을 가리켜요', SOFT)], 32, center=True)
cta(fr, CTA4); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D에서 화살표가 멈춘 숫자')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 1, B 1, C 3, D 2를 가리키면', ('암호 1132', YEL), '',
                          ('1 위 · 2 오른쪽 · 3 아래 · 4 왼쪽', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
grid(fr, 'g', 470, 0.5, 385)
fr.alpha_composite(panel(960, 110), (60, 1050))
text_lines(fr, 540, 1068, ['노란 기어 시계 방향 ¼바퀴 · 가운데 숫자 = 톱니 수', ('암호 = 빨간 화살표가 가리키는 숫자 A B C D', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

# 5 trap
fr = card(ROOM, DATE, 5, 7, '함정 주의', f'방향을 안 보면 {TRAP}', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, ['맞물린 기어는 서로 반대로 돌아요.', '기어 수가 짝수면 마지막 기어는 반대 방향,', ('작은 기어는 큰 기어보다 더 많이 돌아요', YEL)], 35)
spr(fr, 'gC', 540, 830, 1.3)
put(fr, pill('C: 노란 기어가 시계 방향이면 민트 기어는?', 30, WHITE, (255, 255, 255, 30), (18, 6)), 540, 1125)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '회전량 = 첫 톱니 ÷ 마지막 톱니')
grid(fr, 'h', 470, 0.46, 380, list(CODE))
text_lines(fr, 540, 1075, ['A 16÷8=2칸 시계 → 3 · B 24÷8=3칸 반시계 → 2', 'C 1칸 반시계 → 4 · D 32÷8=4칸 = 한 바퀴 → 1'], 29, center=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 3 · B 2 · C 4 · D 1')
grid(fr, 'h', 420, 0.36, 290, list(CODE))
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 880)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1030)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
