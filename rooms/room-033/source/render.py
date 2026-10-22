"""ROOM 033 cards in the 3D style (kit/style3d.py), from sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 33, '2026.10.22'
CODE = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))['unique_answer']
W8 = dict(zip('ABCD', CODE))
ARM = (255, 214, 120, 245)


def tag(p, size):
    k = p['key']
    if k in W8: return pill(k, size, INK, (244, 246, 250, 245), (22, 8))
    if k == 'K': return pill('무게 9', size, INK, (190, 200, 214, 245), (18, 8))
    return pill(p['text'], round(size * 0.85), INK, ARM, (14, 4))


def scene(fr, name, cx, cy, w, show=None, size=30):
    im = Image.open(f'{B}/{name}.png').convert('RGBA')
    bx = im.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox(); im = im.crop(bx); sc = w / im.width
    im = im.resize((w, round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    for p in json.load(open(f'{B}/{name}.json')):
        x, y = x0 + (p['x'] - bx[0]) * sc, y0 + (p['y'] - bx[1]) * sc
        if name == 'ex': put(fr, pill(p['text'] if p['key'].startswith('d') else f"무게 {p['text']}", size, INK, ARM if p['key'].startswith('d') else (244, 246, 250, 245), (16, 6)), x, y); continue
        put(fr, tag(p, size), x, y)
        if show and p['key'] in W8: put(fr, badge(W8[p['key']] if show == 'num' else '?', round(size * 1.3)), x + size * 1.6, y - size * 0.2)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
# 1 hook
fr = card(ROOM, DATE, 1, 7, '모빌이 수평이다', 'A B C D의 무게는 각각 얼마?')
scene(fr, 'mobile', 540, 735, 960, '?')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules + example
fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '노란 숫자 = 가운데 고리에서 떨어진 칸 수')
fr.alpha_composite(panel(960, 220), (60, 290))
text_lines(fr, 100, 322, ['1. 막대마다 무게 × 칸 수가 왼쪽 = 오른쪽', '2. 막대와 줄의 무게는 0',
                          ('3. 아래 막대는 매달린 무게를 전부 더해서', YEL)], 36)
scene(fr, 'ex', 540, 735, 520, size=30)
text_lines(fr, 540, 1060, ['왼쪽 2 × 3칸 = 오른쪽 6 × 1칸', ('그래서 수평', YEL)], 36, center=True)
cta(fr, CTA4); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D의 무게')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 245), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 330), (60, 700))
text_lines(fr, 540, 735, ['예: A 5, B 1, C 7, D 2라면', ('암호는 5172', YEL), '',
                          ('무게는 모두 1~9의 자연수예요', SOFT)], 38, center=True)
cta(fr, CTA4); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
scene(fr, 'mobile', 540, 625, 860, size=28)
fr.alpha_composite(panel(960, 180), (60, 990))
text_lines(fr, 100, 1012, ['막대마다 무게 × 칸 수가 왼쪽 = 오른쪽', '아래 막대는 매달린 무게를 전부 더한다',
                           ('추의 무게는 9 · 암호 = A B C D 무게', YEL)], 33, gap=1.5)
cta(fr, CTA4); save(fr, 4)

# 5 hint
fr = card(ROOM, DATE, 5, 7, '힌트', '맨 아래 막대부터 위로 올라가자', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('추 9가 걸린 막대부터 보면 D가 바로 나와요.', WHITE), 'D × 3칸 = 9 × 1칸',
                          '그다음 C의 막대에서는 D와 추를', ('합친 무게 12로 계산해요', YEL)], 36)
scene(fr, 'mobile', 540, 905, 620, size=22)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer reasoning
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '아래에서 위로 차례로')
scene(fr, 'mobile', 540, 610, 860, 'num', 28)
fr.alpha_composite(panel(960, 210), (60, 960))
text_lines(fr, 540, 985, ['D × 3 = 9 → D = 3  ·  C × 3 = 12 → C = 4', '(A + B) × 2 = 16 → A + B = 8',
                          ('B × 3 = A × 1 → A = 6, B = 2', YEL)], 33, center=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', '아래 막대부터 푼 사람만 정답')
scene(fr, 'mobile', 540, 600, 780, 'num', 26)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 935)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1060)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
