"""ROOM 092 cards in the 3D style (kit/style3d.py), from the music-box sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 92, '2026.11.14'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 40, y0 + 36)
    if val: put(fr, badge(val, 40), x0 + im.width - 14, y0 + 34)


POS = [(292, 480), (788, 480), (292, 860), (788, 860)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '세 번째로 울리는 빗살 번호는?')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '오르골 규칙', '원통이 돌면 핀이 위의 빗살을 튕겨요')
fr.alpha_composite(panel(960, 330), (60, 290))
text_lines(fr, 100, 322, ['1. 빗살은 원통 맨 위에 있어요', '2. 노란 화살표 = 원통 앞면이 움직이는 방향', '3. 핀은 보이는 앞면에만 있어요',
                          '4. 핀이 맨 위에 닿는 순간 소리가 나요', ('세 번째 소리의 빗살 번호는?', YEL)], 33)
one(fr, 'qA', 540, 870, 640, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 세 번째 소리의 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 4번 · 1번 · 8번 · 2번이면', ('암호 4182', YEL), '', ('왼쪽부터 읽으면 틀려요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '화살표 방향을 꼭 보세요')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '아래로 도는 원통이 함정이에요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('앞면이 위로 돌면', WHITE), '→ 위쪽 핀부터 차례로 울려요.', '앞면이 아래로 돌면 핀은 뒤로 넘어가 올라와요',
                          ('→ 맨 아래 핀이 먼저 울려요!', YEL)], 35)
one(fr, 'qB', 540, 880, 620, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '1 2 3 = 울리는 순서 · 빨간 핀 = 세 번째')
four(fr, 'r', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '돌아가는 방향이 순서를 정해요')
one(fr, 'rC', 300, 520, 500, tag=False); one(fr, 'rD', 790, 520, 500, tag=False)
fr.alpha_composite(panel(960, 300), (60, 800))
text_lines(fr, 100, 830, ['C(위로): 3 → 6 → 1 순서, 세 번째는 1', 'D(아래로): 3 → 7 → 9 순서, 세 번째는 9'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1010)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
