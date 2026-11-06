"""ROOM 149 cards in the 3D style (kit/style3d.py), from the street-lamp sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png); the height pill is baked into each sprite."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 149, '2026.12.03'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_shadow_equals_height']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    f = c.width / 470; b = PROOF['boards'][n[1]]
    put(c, pill(f"가로등 높이 {b['H']} · 막대 높이 {b['h']}", round(24 * f), INK, (250, 200, 70, 255), (round(12 * f), round(4 * f))), 0.6 * c.width, 0.08 * c.height)
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 22, y0 + 34)
    if val: put(fr, badge(val, 44), x0 + im.width - 40, y0 + 115)


POS = [(292, 530), (788, 530), (292, 930), (788, 930)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '가로등을 켜면 그림자 끝은?', '막대 그림자가 몇 번까지 뻗을까요?')
four(fr, 'q', 470)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '가로등 규칙', '높이도 땅 눈금과 같은 단위예요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['전구는 0번 위, 노란 칸에 높이가 적혀 있어요', '빛은 전구에서 직선으로 퍼져요',
                          '전구 → 막대 꼭대기 → 땅에 닿는 곳이 그림자 끝', ('그림자 끝의 땅 번호가 숫자예요', YEL)], 31)
one(fr, 'qA', 540, 900, 600, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 그림자 끝 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2 · 6 · 0 · 9번이면', ('암호 2609', YEL), '', ('밤길에 가로등 지나면 그림자가 늘어나는 이유', SOFT)], 34, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '막대가 가로등 높이에 가까우면?')
four(fr, 'q', 470)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '닮은 삼각형 두 개를 찾아요', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('A: 가로등 6, 막대 2 → 막대는 3분의 1 높이', WHITE), '그림자 끝까지의 3분의 2 지점에 막대가 있어요',
                          '막대가 2번이면 그림자 끝은 3번', ('그림자 = 막대 길이라고 보면 함정!', YEL)], 31)
one(fr, 'qA', 540, 900, 600, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 선 = 전구에서 막대 꼭대기를 지나는 빛')
four(fr, 'r', 470, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'qB', 300, 520, 450, tag=False); one(fr, 'rB', 790, 520, 450, tag=False)
fr.alpha_composite(panel(960, 230), (60, 830))
text_lines(fr, 100, 860, ['B: 막대가 가로등의 딱 절반 높이', '그림자도 막대까지 거리만큼 → 4에서 8로!'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1135)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
