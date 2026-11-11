"""ROOM 171 cards in the 3D style (kit/style3d.py), from the tic-tac-toe sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png)."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 171, '2026.12.11'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_obvious']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 - 4, y0 + im.height / 2 - 30)
    if val: put(fr, badge(val, 44), x0 + im.width - 20, y0 + 20)


POS = [(292, 520), (788, 520), (292, 945), (788, 945)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, 'O는 어디에 둬야 할까?', '틱택토 한 수, 대부분 막기부터 해요')
four(fr, 'q', 380)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '틱택토 규칙', '가로, 세로, 대각선 한 줄 3개면 승리')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['지금은 O 차례예요', '상대 X도 가장 잘 둔다고 생각해요',
                          '이길 수 있으면 이기고, 못 이기면 지지 않는', ('최고의 한 칸은 어디일까요? (딱 한 칸)', YEL)], 30)
one(fr, 'qA', 540, 870, 520, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 칸 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2 · 8 · 4 · 6번 칸이면', ('암호 2846', YEL), '', ('가운데가 늘 정답은 아니에요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', 'O의 최고의 한 칸은?')
four(fr, 'q', 380)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '막기보다 먼저 볼 게 있어요', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('A: X가 4, 5에 있어 6을 막고 싶지만', WHITE), '내가 바로 이기는 칸이 있으면 그게 먼저!',
                          'B, D: 상대를 막게 만든 뒤 두 줄을 동시에 노려요', (f'막기와 가운데만 보면 함정 {TRAP}', YEL)], 31)
one(fr, 'qA', 540, 870, 520, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 고리가 최고의 한 칸')
four(fr, 'r', 380, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'rB', 540, 560, 500, tag=False)
fr.alpha_composite(panel(960, 200), (60, 850))
text_lines(fr, 100, 872, ['B: 7에 두면 X는 4를 막아야 해요', '이어서 O가 5에 두면 3-5-7, 1-5-9 두 줄이 동시에!', '가운데부터 두면 비겨요'], 29)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1130)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
