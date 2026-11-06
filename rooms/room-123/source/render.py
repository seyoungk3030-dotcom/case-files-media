"""ROOM 110 cards in the 3D style (kit/style3d.py), from the coloured-shadow sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 123, '2026.11.25'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_same_side']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    bd = PROOF['boards'][n[1]]; f = c.width / 470; col = {'R': (80, 230, 230, 255), 'G': (240, 110, 230, 255), 'B': (250, 230, 70, 255)}[bd['ask']]
    put(c, pill(f"{PROOF['asked_colour'][n[1]]} 그림자는 몇 번?", round(26 * f), INK, col, (round(14 * f), round(5 * f))), 0.5 * c.width, 0.06 * c.height)
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

fr = card(ROOM, DATE, 1, 7, '그림자는 무슨 색일까?', '빨강 · 초록 · 파랑 램프를 동시에 켜요')
four(fr, 'q', 490)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '그림자 규칙', '램프 셋, 기둥 하나, 하얀 벽')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['램프마다 기둥 그림자가 하나씩 생겨요', '그림자 속엔 나머지 두 램프 빛만 닿아요',
                          '판마다 물어보는 색 그림자의 벽 번호는?', ('빛은 섞으면 밝아져요 (물감과 반대)', YEL)], 33)
one(fr, 'qA', 540, 900, 600, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 그 색 그림자의 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2 · 6 · 9 · 4번 칸이면', ('암호 2694', YEL), '', ('과학관에 있는 컬러 그림자 실험', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '그림자는 램프의 어느 쪽에 생길까요?')
four(fr, 'q', 490)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '빛의 삼원색: 빨강 + 초록 + 파랑 = 흰색', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('빨강 램프 그림자 = 초록+파랑 = 청록', WHITE), '초록 그림자 = 자홍 · 파랑 그림자 = 노랑',
                          '그림자는 기둥 너머 램프 반대쪽에 생겨요', ('램프와 같은 쪽에 놓으면 함정!', YEL)], 32)
one(fr, 'qA', 540, 900, 600, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '램프를 모두 켜면 진짜 이렇게 보여요')
four(fr, 'r', 490, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'qA', 300, 520, 450, tag=False); one(fr, 'rA', 790, 520, 450, tag=False)
fr.alpha_composite(panel(960, 230), (60, 830))
text_lines(fr, 100, 860, ['A: 왼쪽 빨강 램프의 그림자는 오른쪽 8번', '그 안엔 초록+파랑만 닿아 청록이에요'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1135)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
