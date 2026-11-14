"""ROOM 181 cards in the 3D style (kit/style3d.py), from the jar-and-bottle sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png)."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 181, '2026.12.14'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_arrows_ccw_from_above']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
for key in 'ABCD':
    bb = [ims[f'{s}{key}'].getchannel('A').getbbox() for s in 'pa']
    BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
    for s in 'pa':
        c = ims[f'{s}{key}'].crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
        c.save(f'{B}/{"q" if s == "p" else "r"}{key}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 - 4, y0 + im.height / 2 - 30)
    if val: put(fr, badge(val, 44), x0 + im.width - 20, y0 + 20)


POS = [(282, 520), (798, 520), (282, 930), (798, 930)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '돌아가는 원탁', '내 앞에 올 접시는? 대부분 반대로 돌려요')
four(fr, 'q', 505)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '원탁 규칙', '파란 매트가 내 자리')
fr = card(ROOM, DATE, 1, 7, '뚜껑 돌리기', '화살표대로 돌리면 몇 개가 열릴까요?')
four(fr, 'q', 505)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '뚜껑 규칙', '노란 화살표 = 내가 위에서 본 돌리는 방향')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['뚜껑은 뚜껑 윗면에서 볼 때 반시계로 돌리면 열려요', '잼 병은 똑바로, 소스 통은 뚜껑을 바닥에 대고 거꾸로',
                          '화살표는 모두 위에서 내려다본 방향이에요', ('선반마다 열리는 뚜껑은 몇 개?', YEL)], 30)
one(fr, 'qA', 540, 880, 860, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 열리는 뚜껑 개수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2개 · 0개 · 5개 · 1개면', ('암호 2051', YEL), '', ('거꾸로 선 통은 어느 쪽이 위일까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '뚜껑 윗면 기준 반시계 = 열림')
four(fr, 'q', 505)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '거꾸로 선 통은 방향이 뒤집혀요', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('소스 통 뚜껑의 윗면은 선반 쪽을 보고 있어요', WHITE), '위에서 시계 방향으로 보이면',
                          '뚜껑 윗면에서는 반시계, 그래서 열려요', (f'위에서 본 반시계만 세면 함정 {TRAP}', YEL)], 31)
one(fr, 'qA', 540, 880, 860, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 = 열림 · 빨강 = 더 잠김')
four(fr, 'r', 505, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'rC', 540, 560, 860, tag=False)
fr.alpha_composite(panel(960, 200), (60, 850))
text_lines(fr, 100, 880, ['C: 잼 병은 시계 방향, 소스 통은 위에서 반시계', '네 개 모두 더 잠겨요. 열리는 뚜껑 0개!'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1130)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
