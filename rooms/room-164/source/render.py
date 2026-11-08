"""ROOM 164 cards in the 3D style (kit/style3d.py), from the jigsaw sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png)."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 164, '2026.12.08'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_flipped']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 - 6, y0 + im.height / 2)
    if val: put(fr, badge(val, 44), x0 + im.width - 34, y0 + 34)


POS = [(292, 515), (788, 515), (292, 937), (788, 937)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '빈칸에 딱 맞는 조각은 몇 번?', '직소 퍼즐, 뒤집으면 반칙!')
four(fr, 'q', 405)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '퍼즐 규칙', '돌리기는 OK, 뒤집기는 NO')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['볼록 튀어나온 곳은 오목 들어간 곳에 끼워져요', '테두리 쪽은 평평한 변이어야 해요',
                          '조각은 돌릴 수 있지만 뒤집을 수는 없어요', ('빈칸에 맞는 조각의 숫자가 암호 한 자리', YEL)], 30)
one(fr, 'qA', 540, 870, 540, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 맞는 조각 숫자')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 3 · 9 · 1 · 2번 조각이면', ('암호 3912', YEL), '', ('조각마다 맞는 것은 딱 하나', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '돌려서 맞는 조각 · 뒤집기 금지')
four(fr, 'q', 405)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '모양이 같아 보이는 조각이 둘?', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('A: 5번과 8번이 비슷해 보여요', WHITE), '하지만 5번은 뒤집어야만 들어가요',
                          '돌리기만 해서 맞는 쪽을 고르세요', (f'뒤집은 조각을 고르면 함정 {TRAP}', YEL)], 33)
one(fr, 'qA', 540, 870, 540, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 조각 = 돌려서 딱 맞는 조각')
four(fr, 'r', 405, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'rB', 540, 560, 560, tag=False)
fr.alpha_composite(panel(960, 200), (60, 880))
text_lines(fr, 100, 905, ['B: 거울에 비친 모양인 조각은', '아무리 돌려도 들어가지 않아요'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1145)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
