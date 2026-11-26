"""ROOM 208 cards (김밥 자르는 시간) in the 3D style (kit/style3d.py), from the kimbap sprites made by
scene3d.py, with each board's known pieces and time written under it. All sprites are cropped to one shared box
(q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS, GOOD, PER
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 208, '2026.12.23'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
f = lambda x: str(int(x)) if x.denominator == 1 else f'{float(x):g}'
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 16, min(b[1] for b in bb) - 16, max(b[2] for b in bb) + 16, max(b[3] for b in bb) + 6)
for n, im in ims.items():
    c = im.crop(BOX); k = n[1]; N, T, M = BOARDS[k]; out = Image.new('RGBA', (c.width, c.height + 170), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'{N}조각 → {T}초', WHITE), (f'{M}조각은 몇 초?', YEL))
    else: lines = ((f'{M}조각 = 칼질 {M - 1}번', MINT), (f'{M - 1}번 × {PER[k]}초 = {GOOD[k]}초', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 70 if j == 0 else 62, col), c.width / 2, c.height + 50 + j * 86)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 30, y0 + 30)
    if val: put(fr, badge(val, 46), x0 + im.width * 0.5, y0 + 40)


POS = [(285, 500), (795, 500), (285, 900), (795, 900)]


def four(fr, pre, w=500, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '김밥 자르는 시간', '3조각에 2초면 6조각은 4초?')
four(fr, 'q', 500)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '김밥 한 줄을 칼로 썰어요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['1. 김밥 길이는 모두 같고, 똑바로 가로로 썰어요', '2. 한 번에 칼질 한 번, 겹쳐 썰기 없음', '3. 칼질 한 번 걸리는 시간은 늘 같아요',
                          '4. 아래 조각 수로 썰면 몇 초 걸릴까요?', ('A~D 걸리는 초가 각 자리 숫자', YEL)], 32)
one(fr, 'qA', 540, 880, 640, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 걸리는 초')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 3초 · 1초 · 6초 · 2초라면', ('암호 3162', YEL), '', ('조각 수를 두 배로 하면 시간도 두 배?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '몇 초 걸릴까?')
four(fr, 'q', 500)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '조각 말고 칼질을 세어 보세요', CORAL)
fr.alpha_composite(panel(960, 270), (60, 300))
text_lines(fr, 100, 330, [('3조각은 칼질 2번이에요', WHITE), '칼질 한 번 시간 = 걸린 시간 ÷ 칼질 수', '6조각이면 칼질은 몇 번일까요?',
                          ('3조각 2초 → 6조각 4초? 함정', YEL)], 34)
one(fr, 'qA', 540, 870, 640, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트색 = 칼질한 자리')
four(fr, 'r', 500, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'n조각은 칼질 n − 1번')
one(fr, 'rA', 285, 560, 500, tag=False); one(fr, 'rD', 795, 560, 500, tag=False)
fr.alpha_composite(panel(960, 280), (60, 860))
text_lines(fr, 100, 885, ['A: 3조각 2초 = 칼질 2번 → 1번에 1초 → 5번 = 5초', 'C: 5조각 8초 = 칼질 4번 → 1번에 2초 → 2번 = 4초', 'D: 2조각 3초 = 칼질 1번 → 3번 = 9초'], 30)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
