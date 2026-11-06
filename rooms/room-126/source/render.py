"""ROOM 126 cards in the 3D style (kit/style3d.py), from the nut-on-a-threaded-rod sprites made by scene3d.py. All
sprites are cropped to one shared box (q*/r*.png); the turn count pill is baked into each sprite."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 126, '2026.11.26'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_one_turn_one_step']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    bd = PROOF['boards'][n[1]]; f = c.width / 250
    put(c, pill(f"{'↓' if bd['dir'] < 0 else '↑'} {bd['turns']}바퀴", round(26 * f), INK, (250, 200, 70, 255), (round(10 * f), round(4 * f))), 0.5 * c.width, 0.035 * c.height)
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 22, y0 + 34)
    if val: put(fr, badge(val, 44), x0 + im.width - 40, y0 + 40)


POS = [(150 + 260 * i, 760) for i in range(4)]


def four(fr, pre, w=250, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '너트는 어디까지 갈까?', '바퀴 수만큼 돌린 뒤 화살표 눈금은?')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '나사 규칙', '너트를 노란 칸의 바퀴 수만큼 돌려요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['너트는 한 바퀴에 나사산 한 칸 움직여요', '↓는 내려가고 ↑는 올라가요',
                          '다 돌린 뒤 화살표가 가리키는 눈금은?', ('눈금 사이 나사산을 세어 보세요', YEL)], 33)
one(fr, 'qA', 540, 860, 160, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 마지막 눈금')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2 · 6 · 0 · 9 눈금이면', ('암호 2609', YEL), '', ('공구함 볼트로 직접 해볼 수 있어요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '한 바퀴 = 눈금 한 칸일까요?')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '눈금 한 칸 사이에 나사산이 몇 개?', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('나사산 2개 = 두 바퀴에 눈금 한 칸', WHITE), '나사산 3개 = 세 바퀴에 눈금 한 칸',
                          '그래서 촘촘한 나사는 천천히 움직여요', ('바퀴 수만큼 눈금을 세면 함정!', YEL)], 33)
one(fr, 'qB', 540, 880, 160, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '흐린 너트 = 처음 · 민트 화살표 = 끝')
four(fr, 'r', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'qA', 400, 600, 200, tag=False); one(fr, 'rA', 680, 600, 200, tag=False)
fr.alpha_composite(panel(960, 180), (60, 895))
text_lines(fr, 100, 922, ['A: 나사산 2개짜리, 6바퀴 → 눈금 3칸', '9에서 3칸 내려가 6이에요'], 31)
put(fr, text_layer(' '.join(CODE), 72, MINT, glow=MINT), 540, 1128)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
