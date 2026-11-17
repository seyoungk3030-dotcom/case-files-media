"""ROOM 191 cards (지구 밧줄) in the 3D style (kit/style3d.py), from the ball-and-rope sprites made by scene3d.py, with each board's ball size and rope extension written under it. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 191, '2026.12.17'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_big_ball_barely_moves']; GAP = PROOF['gap_cm']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    nm, d, u, L = BOARDS[n[1]]; out = Image.new('RGBA', (c.width, c.height + 150), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'{nm} 지름 {d:,}{u}', WHITE), (f'밧줄 +{L}cm', YEL))
    else: lines = ((f'틈 약 {GAP[n[1]]:.1f}cm', MINT), (f'{L} ÷ 6.28', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 62 if j == 0 else 58, col), c.width / 2, c.height + 30 + j * 76)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 40, y0 + 36)
    if val: put(fr, badge(val, 46), x0 + im.width - 44, y0 + 40)


POS = [(290, 520), (790, 520), (290, 945), (790, 945)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '지구 밧줄', '지구에 감은 밧줄을 9cm 늘리면 뜰까요?')
four(fr, 'q', 360)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '밧줄 규칙', '그림은 실제 크기 비율과 달라요')
fr.alpha_composite(panel(960, 360), (60, 290))
text_lines(fr, 100, 322, ['1. 공의 적도에 밧줄을 팽팽하게 한 바퀴 감아요', '2. 밧줄을 적힌 만큼 더 길게 이어 붙여요', '3. 밧줄을 모든 곳에서 똑같은 높이로 띄워요',
                          '4. 원 둘레 = 지름 × 3.14', ('공과 밧줄 사이 틈은 몇 cm? (소수점 버림)', YEL)], 33)
one(fr, 'qC', 540, 905, 360, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 틈의 cm (소수점 버림)')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 틈 2.4 · 0.3 · 6.9 · 1.5cm면', ('암호 2061', YEL), '', ('지구는 너무 커서 거의 안 뜰까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '둘레 = 지름 × 3.14 · 틈은 소수점 버림')
four(fr, 'q', 360)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '공 크기가 정말 상관있을까요?', CORAL)
fr.alpha_composite(panel(960, 360), (60, 300))
text_lines(fr, 100, 330, [('틈을 h라고 하면 새 지름은 지름 + 2h', WHITE), '새 둘레 - 원래 둘레 = 2h × 3.14', '늘린 길이만 알면 h가 나와요. 지름은 지워져요!',
                          (f'지구·달은 거의 0이라고 보면 함정 {TRAP}', YEL)], 35)
one(fr, 'qC', 540, 935, 340, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '틈 = 늘린 길이 ÷ 6.28, 공 크기와 상관없어요')
four(fr, 'r', 360, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '지구도 귤도 똑같이 떠요')
one(fr, 'rA', 300, 560, 380, tag=False); one(fr, 'rC', 790, 560, 380, tag=False)
fr.alpha_composite(panel(960, 260), (60, 900))
text_lines(fr, 100, 925, ['A 귤: 22 ÷ 6.28 ≈ 3.5cm', 'C 지구: 9 ÷ 6.28 ≈ 1.4cm, 손가락 하나 들어갈 만큼 떠요'], 31)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
