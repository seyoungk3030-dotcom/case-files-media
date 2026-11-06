"""ROOM 083 cards in the 3D style (kit/style3d.py), from the water-tank sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 83, '2026.11.11'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
BOXES = {}
for s0 in 'pa':
    bb = [ims[s0 + k].getchannel('A').getbbox() for k in 'ABCD']
    BOXES[s0] = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOXES[n[0]]); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag:
        put(fr, pill(name[1], 38, INK, (244, 246, 250, 245), (20, 6)), x0 + 20, y0 + 20)
        if val: put(fr, badge(val, 42), x0 + 20, y0 + 90)


YS = [420, 625, 830, 1035]


def four(fr, pre, w=490, vals=None, ys=None):
    if pre == 'q':
        for i, k in enumerate('ABCD'): one(fr, pre + k, 570, 425 + i * 212, 800)
        return
    for i, k in enumerate('ABCD'): one(fr, pre + k, 295 + (i % 2) * 490, 530 + (i // 2) * 360, w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '물에 넣으면 뜨는 블록은 몇 개?')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '작은 정육면체(1cm)로 만든 블록과 무게표')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 작은 정육면체 1개 = 1cm³', '2. 물 1cm³의 무게는 1g이에요',
                          '3. 무게표는 블록 전체의 무게예요', ('물에 뜨는 블록은 몇 개?', YEL)], 34)
one(fr, 'qA', 540, 800, 1000, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 뜨는 블록 개수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 1개 · 3개 · 2개 · 4개가 뜨면', ('암호 1324', YEL), '', ('하나도 안 뜨면 0이에요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '가볍다고 뜨는 게 아니에요')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '무게와 크기를 같이 보세요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('2×2×2 블록은 8cm³ = 물 8g만큼', WHITE), '3×3×3 블록은 27cm³ = 물 27g만큼', '블록이 그 물보다 가벼우면 떠요.',
                          ('30g짜리 큰 블록도 뜰 수 있을까요?', YEL)], 35)
one(fr, 'qD', 540, 830, 1000, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '노란 블록만 떠요 (무게 < 칸 수)')
four(fr, 'r', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '무게가 칸 수보다 작으면 떠요')
for i, k in enumerate('ABCD'): one(fr, 'r' + k, 295 + (i % 2) * 490, 420 + (i // 2) * 230, 400, tag=False)
for i, k in enumerate('ABCD'): put(fr, badge(CODE[i], 42), 80 + (i % 2) * 490, 420 + (i // 2) * 230)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 920)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1030)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
