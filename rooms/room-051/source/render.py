"""ROOM 051 cards in the 3D style (kit/style3d.py), from the equation rows made by eqs.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 51, '2026.10.28'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_left_to_right']


def rows(fr, pre, y0, gap, w=900, only=(1, 2, 3, 4)):
    for n, i in enumerate(only):
        im = Image.open(f'{B}/{pre}{i}.png').convert('RGBA'); sc = w / 1200
        im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
        fr.alpha_composite(im, (540 - im.width // 2, int(y0 + n * gap - im.height / 2)))


def icon(fr, k, cx, cy, h):
    im = Image.open(f'{B}/icon-{k}.png').convert('RGBA'); im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
fr = card(ROOM, DATE, 1, 7, '그림 수식 네 줄', '공 · 상자 · 피라미드 · 별은 각각 얼마?')
rows(fr, 'eq', 470, 175)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '같은 모양은 같은 숫자')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 같은 모양은 언제나 같은 값', '2. 값은 모두 자연수', ('3. 계산 순서는 수학 그대로 (곱셈 먼저)', YEL)], 33)
for n, k in enumerate('ABCD'): icon(fr, k, 165 + n * 250, 760, 190)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A 공 → B 상자 → C 피라미드 → D 별')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; icon(fr, k, cx, 470, 150)
    put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 600); put(fr, badge('?', 46), cx, 700)
fr.alpha_composite(panel(960, 150), (60, 800))
text_lines(fr, 540, 835, ['예: 공 3, 상자 5, 피라미드 1, 별 9라면', ('암호 3519', YEL)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '수식은 이것이 전부')
rows(fr, 'eq', 420, 165)
fr.alpha_composite(panel(960, 110), (60, 1050))
text_lines(fr, 540, 1068, ['같은 모양 = 같은 값 · 곱셈 먼저', ('암호 = 공 상자 피라미드 별의 값', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', f'왼쪽부터 계산하면 {TRAP}?', CORAL)
fr.alpha_composite(panel(960, 220), (60, 300))
text_lines(fr, 100, 330, ['마지막 줄을 왼쪽부터 계산하면 틀려요.', '더하기보다 곱하기가 먼저예요.',
                          ('피라미드 × 공을 먼저 계산하세요', YEL)], 35)
rows(fr, 'eq', 800, 0, 980, (4,))
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '위에서부터 하나씩 풀면 끝')
rows(fr, 'ax', 400, 170, 840)
fr.alpha_composite(panel(960, 120), (60, 1030))
text_lines(fr, 540, 1050, ['공 12÷3=4 · 상자 6−4=2 · 피라미드 (16−2)÷2=7', ('별 + 7×4 = 36 → 별 = 8', YEL)], 29, center=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '공 4 · 상자 2 · 피라미드 7 · 별 8')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; icon(fr, k, cx, 520, 170); put(fr, badge(CODE[n], 44), cx, 660)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 840)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 990)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
