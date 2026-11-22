"""ROOM 203 cards (바꿀까 말까) in the 3D style (kit/style3d.py), from the side-view sprites made by scene3d.py, with each
board's speed and the sticker's ground speed written under it. All sprites are cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 203, '2026.12.21'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; WIN = PROOF['wins']; PW = PROOF['p_win']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 20, min(b[1] for b in bb) - 20, max(b[2] for b in bb) + 20, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); k = n[1]; nd, ko, st, g = BOARDS[k]; out = Image.new('RGBA', (c.width, c.height + 150), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'문 {nd}개 · 사회자가 {ko}개 열어 줌', WHITE), (f'{"그대로" if st == "stay" else "다른 문으로 바꿈"} · {g}판이면?', YEL))
    else: lines = ((f'평균 {WIN[k]}번 당첨', MINT), (f'당첨 확률 {PW[k]} × {g}판', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 62 if j == 0 else 54, col), c.width / 2, c.height + 30 + j * 76)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 30, y0 + 30)
    if val: put(fr, badge(val, 46), x0 + im.width - 40, y0 + im.height * 0.42)


POS = [(290, 520), (790, 520), (290, 945), (790, 945)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '바꿀까 말까', '문이 열렸으면 반반 아닌가요?')
four(fr, 'q', 460)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '문 하나 뒤에만 상품이 있어요')
fr.alpha_composite(panel(960, 420), (60, 290))
text_lines(fr, 100, 322, ['1. 나는 1번 문을 골라요 (노란 표시)', '2. 답을 아는 사회자가 꽝인 문을 열어 보여줘요 (X)', '3. 그다음 그대로 두거나, 닫힌 다른 문으로 바꿔요',
                          '   (바꿀 문이 여럿이면 아무거나 하나)', '4. 같은 게임을 여러 판 해요', ('평균 당첨 횟수가 각 자리 숫자', YEL)], 32)
one(fr, 'qB', 540, 950, 420, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 평균 당첨 횟수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2번 · 5번 · 1번 · 4번이라면', ('암호 2514', YEL), '', ('바꾸든 안 바꾸든 똑같을까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '평균 몇 번 당첨될까?')
four(fr, 'q', 460)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '사회자는 상품 문을 절대 안 열어요', CORAL)
fr.alpha_composite(panel(960, 400), (60, 300))
text_lines(fr, 100, 330, [('처음 고른 문이 맞을 확률은 문이 열려도 그대로', WHITE), '문 3개면 1/3, 틀렸을 확률 2/3', '틀렸다면 바꾸는 순간 무조건 당첨!',
                          ('열렸으니 반반? 함정', YEL)], 35)
one(fr, 'qA', 540, 950, 400, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '바꾸면 2배로 잘 맞아요')
four(fr, 'r', 460, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '처음 고른 문은 1/3 그대로')
one(fr, 'rA', 300, 560, 400, tag=False); one(fr, 'rB', 790, 560, 400, tag=False)
fr.alpha_composite(panel(960, 280), (60, 890))
text_lines(fr, 100, 915, ['A: 그대로 = 처음 맞혀야 당첨 → 9판 중 3번', 'B: 바꿈 = 처음 틀렸으면 당첨 → 9판 중 6번', 'D: 문 4개, 1개만 열림 → 3/4 × 1/2 = 3/8'], 30)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1110)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
