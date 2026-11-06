"""ROOM 110 cards in the 3D style (kit/style3d.py), from the Newton's-cradle sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 124, '2026.11.25'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_same_counts']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 22, y0 + 34)
    if val: put(fr, badge(val, 44), x0 + im.width - 40, y0 + 40)


POS = [(292, 530), (788, 530), (292, 930), (788, 930)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '뉴턴의 요람', '양쪽 공을 동시에 놓으면?')
four(fr, 'q', 490)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '요람 규칙', '똑같은 쇠공들이 나란히 매달려 있어요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['들린 공들을 모두 동시에 놓아요', '부딪친 뒤 오른쪽으로 튀어나가는 공들 중',
                          '가장 안쪽 공의 번호는?', ('든 공이 없는 쪽도 있어요', YEL)], 33)
one(fr, 'qA', 540, 900, 600, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 오른쪽 가장 안쪽 공 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 5 · 2 · 8 · 1번 공이면', ('암호 5281', YEL), '', ('책상 위 그 딱딱 소리 나는 장난감', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '오른쪽으로 튀어나가는 공은 몇 개일까요?')
four(fr, 'q', 490)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '왼쪽에서 든 개수만큼 오른쪽에서 튀어나가요', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('양쪽에서 동시에 놓으면 개수가 서로 바뀌어요', WHITE), '왼쪽 3개, 오른쪽 1개 → 왼쪽 1개, 오른쪽 3개',
                          '오른쪽 끝에서 그 개수번째 공이 정답', ('오른쪽에서 든 개수를 쓰면 함정!', YEL)], 32)
one(fr, 'qB', 540, 900, 600, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '부딪친 뒤 모습 · 민트 = 오른쪽 가장 안쪽')
four(fr, 'r', 490, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'qB', 300, 520, 450, tag=False); one(fr, 'rB', 790, 520, 450, tag=False)
fr.alpha_composite(panel(960, 230), (60, 830))
text_lines(fr, 100, 860, ['B: 왼쪽 3개, 오른쪽 1개를 동시에 놓으면', '오른쪽으로 3개가 튀어나가요 → 안쪽 공 6번'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1135)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
