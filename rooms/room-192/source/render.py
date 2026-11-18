"""ROOM 192 cards (반 잘라 쌓기) in the 3D style (kit/style3d.py), from the object-and-paper-pile sprites made by scene3d.py, with each board's object height and the
pile after the needed cuts written under it. All sprites are cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 192, '2026.12.17'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_one_sheet_per_cut']; CUTS = PROOF['cuts']; PILE = PROOF['pile_mm']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    nm, h = BOARDS[n[1]]; k = n[1]; out = Image.new('RGBA', (c.width, c.height + 150), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'{nm} 높이 {h}mm', WHITE), ('종이 1장 0.1mm', YEL))
    else: lines = ((f'{CUTS[k]}번 → {2 ** CUTS[k]:,}장', MINT), (f'{PILE[k]}mm > {h}mm', SOFT))
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

fr = card(ROOM, DATE, 1, 7, '반 잘라 쌓기', '종이를 몇 번 잘라 쌓으면 탁구공보다 높을까요?')
four(fr, 'q', 360)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '쌓기 규칙', '종이 1장 0.1mm · 판마다 그림 비율은 달라요')
fr.alpha_composite(panel(960, 360), (60, 290))
text_lines(fr, 100, 322, ['1. 종이 1장을 반으로 잘라 두 장을 겹쳐요', '2. 겹친 묶음 전체를 또 반으로 잘라 겹쳐요', '3. 이걸 한 번 할 때마다 "1번"으로 세요',
                          '4. 쌓인 높이가 옆 물건보다 높아지면 끝', ('가장 적은 횟수는 몇 번?', YEL)], 33)
one(fr, 'qA', 540, 905, 360, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 자른 횟수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2번 · 3번 · 1번 · 4번이면', ('암호 2314', YEL), '', ('한 번에 한 장씩 늘어날까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '종이 0.1mm · 물건보다 높아지는 최소 횟수')
four(fr, 'q', 360)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '자를 때마다 몇 장이 될까요?', CORAL)
fr.alpha_composite(panel(960, 360), (60, 300))
text_lines(fr, 100, 330, [('1장 → 2장 → 4장 → 8장 → 16장 ...', WHITE), '묶음 전체를 자르니까 장수가 두 배씩!', '10번이면 1,024장, 약 10cm예요',
                          (f'한 번에 1장씩이라 보면 함정 {TRAP["A"]}번', YEL)], 35)
one(fr, 'qC', 540, 935, 340, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '자를 때마다 두 배, 몇 번이면 충분해요')
four(fr, 'r', 360, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '9번이면 탁구공도 넘어요')
one(fr, 'rC', 300, 560, 380, tag=False); one(fr, 'rD', 790, 560, 380, tag=False)
fr.alpha_composite(panel(960, 260), (60, 900))
text_lines(fr, 100, 925, ['C 탁구공 40mm: 8번은 25.6mm, 9번이면 51.2mm', '한 장씩 쌓았다면 400장이 필요했어요'], 31)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
