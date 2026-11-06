"""ROOM 087 cards in the 3D style (kit/style3d.py), from the cup-row sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 87, '2026.11.13'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; K = {k: v[1] for k, v in PROOF['boards_cups_flip_k'].items()}
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'p' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag:
        put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 - 30, y0 + 30)
        put(fr, pill(f'{K[name[1]]}개씩', 28, INK, (250, 200, 90, 245), (14, 5)), x0 - 30, y0 + 95)
        if val: put(fr, badge(val, 42), x0 + im.width + 30, y0 + im.height / 2)


YS = [420, 625, 830, 1035]


def four(fr, pre, w=820, vals=None, ys=YS):
    for i, k in enumerate('ABCD'): one(fr, pre + k, 560 if not vals else 520, ys[i], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '컵을 전부 바로 세우려면 최소 몇 번?')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '엎어진 컵을 모두 바로 세워요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 한 번에 정해진 개수만큼 꼭 뒤집어요', '2. 어느 컵이든 고를 수 있어요 (바로 선 컵도)',
                          '3. 절대 불가능하면 0이에요', ('전부 바로 서려면 최소 몇 번?', YEL)], 33)
one(fr, 'qA', 560, 800, 860)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 최소 횟수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 1번 · 4번 · 불가능 · 2번이면', ('암호 1402', YEL), '', ('바로 선 컵을 다시 엎어도 돼요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '엎어진 컵 수의 홀짝을 보세요')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '2개씩 뒤집으면 엎어진 수는 ±2 또는 그대로', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('엎어진 컵이 홀수면 2개씩으론 영원히 홀수', WHITE), '3개씩이면 홀짝이 매번 바뀌어요.', '컵 1개만 엎어져 있어도 한 번에 안 돼요.',
                          ('바로 선 컵도 같이 뒤집어야 해요!', YEL)], 33)
one(fr, 'qD', 560, 850, 860)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', 'A 2번 · B 불가능(0) · C 3번 · D 3번')
four(fr, 'q', w=760, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'D는 1개만 엎어졌는데 3번!')
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 325, ['D 1번: 엎어진 1 + 바로 선 2 → 엎어진 2개', 'D 2번: 엎어진 1 + 바로 선 2 → 엎어진 3개', 'D 3번: 엎어진 3개를 뒤집으면 모두 바로!', ('B: 엎어진 3개(홀수)는 2개씩으로 불가능', YEL)], 31)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 860)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 990)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
