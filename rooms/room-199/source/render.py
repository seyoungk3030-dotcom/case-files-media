"""ROOM 199 cards (미끄러지는 사다리) in the 3D style (kit/style3d.py), from the side-view sprites made by scene3d.py, with each
board's motion and the scale reading written under it. All sprites are cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 199, '2026.12.20'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; DROP = PROOF['drop']; TOP = PROOF['top_after']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 20, min(b[1] for b in bb) - 20, max(b[2] for b in bb) + 20, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); k = n[1]; L, d = BOARDS[k]; out = Image.new('RGBA', (c.width, c.height + 150), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'{L}m 사다리', WHITE), (f'아래를 {d}m 빼면?', YEL))
    else: lines = ((f'{DROP[k]}m 내려옴', MINT), (f'높이 {L} → {TOP[k]}m', SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 62 if j == 0 else 54, col), c.width / 2, c.height + 30 + j * 76)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 30, y0 + 30)
    if val: put(fr, badge(val, 46), x0 + im.width - 40, y0 + im.height * 0.42)


POS = [(300, 512), (780, 512), (300, 937), (780, 937)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '미끄러지는 사다리', '아래를 뺀 만큼 위도 내려올까요?')
four(fr, 'q', 300)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '벽에 똑바로 세운 곧은 사다리')
fr.alpha_composite(panel(960, 400), (60, 290))
text_lines(fr, 100, 322, ['1. 사다리는 처음에 벽에 딱 붙어 서 있어요 (흐린 그림)', '2. 아래쪽을 벽에서 노란 화살표만큼 빼요', '3. 꼭대기는 벽을 따라 미끄러져 내려와요',
                          '4. 사다리 길이는 변하지 않아요', ('꼭대기가 내려온 거리(m)가 각 자리 숫자', YEL)], 33)
one(fr, 'qA', 540, 960, 300, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 내려온 거리(m)')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2m · 9m · 3m · 7m 내려왔다면', ('암호 2937', YEL), '', ('아래를 3m 빼면 위도 3m 내려올까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '꼭대기는 몇 m 내려왔을까?')
four(fr, 'q', 300)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '벽, 바닥, 사다리가 직각삼각형을 만들어요', CORAL)
fr.alpha_composite(panel(960, 400), (60, 300))
text_lines(fr, 100, 330, [('꼭대기 높이² + 뺀 거리² = 사다리 길이²', WHITE), '예) 5m 사다리를 4m 빼면 높이 3m', '처음 높이(= 사다리 길이)에서 빼면 끝',
                          ('뺀 거리만큼 내려온다고 적으면 함정', YEL)], 35)
one(fr, 'qC', 540, 980, 280, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '아래를 많이 빼도 위는 조금만 내려와요')
four(fr, 'r', 300, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '높이 = √(사다리² − 뺀 거리²)')
one(fr, 'rA', 300, 560, 330, tag=False); one(fr, 'rD', 790, 560, 330, tag=False)
fr.alpha_composite(panel(960, 260), (60, 900))
text_lines(fr, 100, 925, ['A: √(5² − 3²) = 4 → 5에서 4로, 1m', 'D: √(10² − 8²) = 6 → 10에서 6으로, 4m'], 31)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
