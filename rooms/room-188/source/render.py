"""ROOM 188 cards (휴지 남은 날) in the 3D style (kit/style3d.py), from the toilet-roll sprites made by scene3d.py, with each board's numbers written under the roll. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 188, '2026.12.16'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_diameter_linear']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    k, F, cc, N = BOARDS[n[1]]; out = Image.new('RGBA', (c.width, c.height + 210), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    for j, (t, col) in enumerate(((f'새 휴지 {F}cm', (150, 190, 255) if n[0] == 'p' else CORAL), (f'{N}일 쓰고 {cc}cm', WHITE), (f'심 {k}cm', SOFT))):
        put(out, text_layer(t, 50 if j < 2 else 42, col), c.width / 2, c.height + 30 + j * 64)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 40, y0 + 36)
    if val: put(fr, badge(val, 46), x0 + im.width - 44, y0 + 40)


POS = [(292, 525), (788, 525), (292, 950), (788, 950)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '휴지 남은 날', '며칠 더 쓸 수 있을까요?')
four(fr, 'q', 290)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '휴지 규칙', '그림은 실제 크기 비율 그대로예요')
fr.alpha_composite(panel(960, 330), (60, 290))
text_lines(fr, 100, 322, ['1. 점선 = 새 휴지였을 때의 크기(지름)', '2. 지금까지 쓴 날과 지금 지름이 적혀 있어요', '3. 매일 똑같은 길이만큼 써요',
                          '4. 가운데 심만 남으면 끝이에요', ('앞으로 며칠 더 쓸 수 있을까요?', YEL)], 33)
one(fr, 'qA', 540, 900, 400, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 남은 날 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2일 · 7일 · 1일 · 5일이면', ('암호 2715', YEL), '', ('지름이 줄어든 만큼만 보면 될까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '매일 같은 길이를 써요 · 심만 남으면 끝')
four(fr, 'q', 290)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '바깥쪽 한 바퀴가 훨씬 길어요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('휴지 길이는 지름이 아니라', WHITE), '휴지 단면(도넛 모양)의 넓이에 비례해요.', '넓이는 지름 x 지름에 비례해요.',
                          (f'지름만 빼서 나누면 함정 {TRAP}', YEL)], 35)
one(fr, 'qA', 540, 900, 380, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '남은 넓이 ÷ 쓴 넓이 × 쓴 날')
four(fr, 'r', 290, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '절반 지름이면 절반 남은 게 아니에요')
one(fr, 'rA', 300, 600, 400, tag=False); one(fr, 'rD', 790, 600, 400, tag=False)
fr.alpha_composite(panel(960, 260), (60, 880))
text_lines(fr, 100, 905, ['A: 쓴 넓이 144-64=80이 5일, 남은 64-16=48은 3일', 'D: 쓴 넓이 100-64=36이 3일, 남은 64-16=48은 4일'], 31)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
