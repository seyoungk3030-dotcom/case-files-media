"""ROOM 043 cards in the 3D style (kit/style3d.py), from the coin sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 43, '2026.10.25'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; SIZES = PROOF['big_coin_radius_in_small_coins']


def spr(fr, name, cx, cy, sc):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox()
    im = im.crop((l, t, r, b)); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))); return im


def grid(fr, y0, sc, gap, vals=None, size_pill=True):
    for i, k in enumerate('ABCD'):
        cx, cy = 290 + (i % 2) * 500, y0 + (i // 2) * gap
        im = spr(fr, 'c' + k, cx, cy, sc)
        put(fr, pill(k, 38, INK, (244, 246, 250, 245), (22, 6)), cx - 190, cy - gap / 2 + 50)
        if vals: put(fr, badge(vals[i], 40), cx - 120, cy - gap / 2 + 50)
        if size_pill: put(fr, pill(f'큰 동전 = 작은 동전 {SIZES[k]}배', 24, WHITE, (255, 255, 255, 30), (14, 5)), cx, cy + gap / 2 - 40)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
# 1 hook
fr = card(ROOM, DATE, 1, 7, '동전을 한 바퀴 굴리면', '작은 동전은 몇 바퀴 돌까?')
grid(fr, 520, 0.78, 380)
text_lines(fr, 540, 1110, [('미끄러지지 않고 큰 동전 둘레를 한 바퀴', SOFT)], 32, center=True)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules
fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '큰 동전은 고정, 작은 동전만 굴러간다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 작은 동전이 큰 동전 바깥을 미끄러짐 없이 한 바퀴', '2. 출발한 자리로 돌아오면 멈춘다',
                          ('3. 위에서 볼 때 화살표가 몇 바퀴 도는지 센다', YEL)], 33)
spr(fr, 'cB', 540, 800, 0.95)
text_lines(fr, 540, 1060, [('크기는 반지름 기준 (2배 = 반지름이 2배)', SOFT)], 32, center=True)
cta(fr, CTA4); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D에서 작은 동전이 도는 횟수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 7바퀴, B 3바퀴, C 9바퀴, D 1바퀴라면', ('암호 7391', YEL), '',
                          ('화살표가 처음처럼 위를 볼 때마다 1바퀴', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
grid(fr, 510, 0.74, 360)
fr.alpha_composite(panel(960, 110), (60, 1050))
text_lines(fr, 540, 1068, ['큰 동전 고정 · 미끄러짐 없이 바깥을 한 바퀴', ('암호 = 작은 동전이 도는 횟수 A B C D', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

# 5 trap
fr = card(ROOM, DATE, 5, 7, '함정 주의', f'둘레만 나누면 {PROOF["trap_rolled_distance_only"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('"큰 동전 둘레 ÷ 작은 동전 둘레"는', WHITE), '바닥이 일자일 때만 맞는 계산이에요.', '동전 주위를 빙 돌면 그 자체로',
                          ('한 바퀴가 더 생겨요', YEL)], 35)
spr(fr, 'cA', 540, 860, 1.25)
put(fr, pill('A: 같은 크기 동전, 정말 1바퀴일까?', 30, WHITE, (255, 255, 255, 30), (18, 6)), 540, 1100)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '도는 횟수 = 둘레 비율 + 1')
fr.alpha_composite(panel(960, 260), (60, 280))
text_lines(fr, 540, 305, ['작은 동전의 중심은 더 큰 원(큰 반지름 + 작은 반지름)을 돈다',
                          'A 1+1=2 · B 3+1=4 · C 2+1=3 · D 4+1=5', ('같은 크기 동전도 2바퀴 돈다', YEL)], 32, center=True)
spr(fr, 'aA', 540, 840, 1.35)
put(fr, pill('A: 반 바퀴만 돌아도 화살표는 이미 한 바퀴', 28, WHITE, (255, 255, 255, 30), (18, 6)), 540, 1110)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 2바퀴 · B 4바퀴 · C 3바퀴 · D 5바퀴')
grid(fr, 420, 0.58, 290, list(CODE), size_pill=False)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 880)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1030)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
