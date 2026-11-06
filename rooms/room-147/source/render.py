"""ROOM 147 cards in the 3D style (kit/style3d.py), from the raft sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png); the raft-weight pill is baked into each sprite."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 147, '2026.12.03'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_raft_fixed']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    f = c.width / 470; M = PROOF['boards'][n[1]]['M']
    put(c, pill(f'뗏목 무게 = 사람 {M}명', round(24 * f), INK, (250, 200, 70, 255), (round(12 * f), round(4 * f))), 0.5 * c.width, 0.9 * c.height)
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

fr = card(ROOM, DATE, 1, 7, '끝까지 걸어가면 몇 번 앞?', '물에 뜬 뗏목 위를 걸어가요')
four(fr, 'q', 470)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '뗏목 규칙', '뗏목은 묶여 있지 않고 물에 떠 있어요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['사람이 뗏목 왼쪽 끝에서 오른쪽 끝까지 걸어요', '물의 저항은 무시해요 (뗏목이 미끄러져요)',
                          '뗏목 무게는 사람 몇 명분인지 적혀 있어요', ('도착한 곳의 부두 번호가 숫자예요', YEL)], 31)
one(fr, 'qA', 540, 900, 600, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 도착한 부두 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2 · 6 · 0 · 9번 앞이면', ('암호 2609', YEL), '', ('보트에서 내릴 때 배가 밀려나는 그 현상', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '사람이 앞으로 가면 뗏목은?')
four(fr, 'q', 470)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '사람과 뗏목의 무게중심은 제자리', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('A: 뗏목 6칸, 무게 사람 2명', WHITE), '사람 2칸 : 뗏목 1칸 비율로 나눠 움직여요',
                          '사람 +4, 뗏목 -2 → 1에서 5로', ('뗏목이 가만히 있다고 보면 함정!', YEL)], 33)
one(fr, 'qC', 540, 900, 600, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '빨간 테두리 = 뗏목이 있던 자리')
four(fr, 'r', 470, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'qC', 300, 520, 450, tag=False); one(fr, 'rC', 790, 520, 450, tag=False)
fr.alpha_composite(panel(960, 230), (60, 830))
text_lines(fr, 100, 860, ['C: 뗏목 무게 = 사람 1명이면 반반!', '4칸 중 사람 2칸, 뗏목 2칸 → 2에서 4로'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1135)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
