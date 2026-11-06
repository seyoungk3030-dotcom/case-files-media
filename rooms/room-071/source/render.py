"""ROOM 071 cards in the 3D style (kit/style3d.py), from the candle sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 71, '2026.11.07'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']


def spr(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()
    im = im.crop((max(l - 10, 0), max(t - 10, 0), r + 10, b + 10)); sc = w / im.width
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag:
        put(fr, pill(name[1], 38, INK, (244, 246, 250, 245), (20, 6)), x0 + 12, y0 + 20)
        if val: put(fr, badge(val, 38), x0 + 82, y0 + 20)


def grid(fr, pre, y0, w=380, gap=380, vals=None, dx=480):
    for i, k in enumerate('ABCD'):
        spr(fr, pre + k, 540 - dx / 2 + (i % 2) * dx, y0 + (i // 2) * gap, w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'


def row(fr, pre, y, w, vals=None):
    for i, k in enumerate('ABCD'):
        spr(fr, pre + k, 165 + i * 250, y, w, val=vals[i] if vals else None)


fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '먼저 꺼질 때 남은 초는 몇 칸?')
grid(fr, 'p', 507, 350, 420, dx=400)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '두 초에 동시에 불을 붙여요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 얇은 초는 1시간에 2칸 타요', '2. 굵은 초는 1시간에 1칸 타요',
                          '3. 하나가 먼저 다 타서 꺼지는 순간', ('다른 초는 몇 칸 남았을까?', YEL)], 34)
spr(fr, 'pA', 540, 872, 440, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 남은 초의 칸 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 1칸 · B 5칸 · C 8칸 · D 2칸이면', ('암호 1582', YEL), '',
                          ('짧은 초가 먼저 꺼진다? 함정', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '얇은 초 1시간 2칸 · 굵은 초 1시간 1칸')
grid(fr, 'p', 507, 350, 420, dx=400)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', f'똑같이 탄다고 하면 {PROOF["trap_same_speed"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('짧다고 먼저 꺼지는 게 아니에요', WHITE), '얇은 초 9칸은 4시간 반,', '굵은 초 3칸은 3시간 만에 꺼져요.',
                          ('먼저 꺼지는 시간을 비교!', YEL)], 35)
spr(fr, 'pB', 540, 902, 420, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '먼저 꺼지는 시간 → 그동안 다른 초가 탄 만큼 빼기')
fr.alpha_composite(panel(960, 160), (60, 280))
text_lines(fr, 540, 300, ['A 3시간 7-3=4 · B 3시간 9-6=3', ('C 1시간 9-1=8 · D 4시간 9-8=1', YEL)], 31, center=True)
grid(fr, 'a', 640, 290, 345, list(CODE), dx=360)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 4 · B 3 · C 8 · D 1')
grid(fr, 'a', 480, 230, 280, list(CODE), dx=300)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 975)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
