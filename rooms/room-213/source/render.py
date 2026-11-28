"""ROOM 213 cards (건전지 하나를 거꾸로) in the 3D style (kit/style3d.py), from the battery-holder sprites made by
scene3d.py, with each board's cell count written under it. All sprites are cropped to one shared box
(q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS, GOOD
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 213, '2026.12.24'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
f = lambda x: str(int(x)) if x.denominator == 1 else f'{float(x):g}'
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 8, min(b[1] for b in bb) - 8, max(b[2] for b in bb) + 8, max(b[3] for b in bb) + 8)
for n, im in ims.items():
    c = im.crop(BOX); k = n[1]; cs = BOARDS[k]; f, r = cs.count('+'), cs.count('-')
    TW = 270; out = Image.new('RGBA', (c.width + TW, c.height + 30), (0, 0, 0, 0)); out.alpha_composite(c, (0, 15))
    if n[0] == 'p': lines = ((f'{len(cs)}개', WHITE, 72), ('? V', YEL, 92))
    else: lines = ((f'{GOOD[k]} V', MINT, 92), (f'1.5×({f}−{r})', SOFT, 48))
    ys = (out.height / 2 - 52, out.height / 2 + 50)
    for (t, col, sz), y in zip(lines, ys): put(out, text_layer(t, sz, col), c.width + TW / 2, y)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 10, y0 + 30)
    if val: put(fr, badge(val, 40), x0 + im.width * 0.385, y0 + 46)


POS = [(545, 372), (545, 582), (545, 792), (545, 1002)]


def four(fr, pre, w=980, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '건전지 하나를 거꾸로', '빠진 셈 치면 될까요?')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '건전지를 한 줄로 이어 끝과 끝 전압을 재요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['1. 건전지 1개는 1.5 V예요', '2. 금색 쪽 볼록한 끝이 + 예요', '3. 몇 개는 거꾸로 들어가 있어요',
                          '4. 전압계(빨강 +, 검정 −)는 몇 V?', ('A~D 전압(V)이 각 자리 숫자', YEL)], 32)
one(fr, 'qA', 540, 830, 980, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 전압계 숫자(V)')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 3 V · 7 V · 5 V · 2 V라면', ('암호 3752', YEL), '', ('+ 방향을 하나씩 세어 보세요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '전압계는 몇 V를 가리킬까?')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '거꾸로 든 건전지는 반대로 밀어요', CORAL)
fr.alpha_composite(panel(960, 270), (60, 300))
text_lines(fr, 100, 330, [('바른 방향 1개 = +1.5 V', WHITE), '거꾸로 1개 = −1.5 V (0 V가 아니에요)', '전압 = 1.5 × (바른 개수 − 거꾸로 개수)',
                          ('거꾸로 든 건 빼고 센다? 함정', YEL)], 34)
one(fr, 'qC', 540, 830, 980, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 = 바른 방향 · 빨강 = 거꾸로')
four(fr, 'r', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '거꾸로 1개는 건전지 2개 몫을 잃어요')
one(fr, 'rC', 540, 440, 980, tag=False); one(fr, 'rD', 540, 680, 980, tag=False)
fr.alpha_composite(panel(960, 280), (60, 860))
text_lines(fr, 100, 885, ['A: 바른 3 − 거꾸로 1 = 2 → 3 V (4.5 V 아님)', 'C: 바른 2 − 거꾸로 2 = 0 → 0 V', 'D: 바른 7 − 거꾸로 1 = 6 → 9 V'], 30)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
