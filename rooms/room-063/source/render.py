"""ROOM 063 cards in the 3D style (kit/style3d.py), from the hole disc sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 63, '2026.11.05'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']


def spr(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()
    im = im.crop((max(l - 10, 0), max(t - 10, 0), r + 10, b + 10)); sc = w / im.width
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag:
        put(fr, pill(name[1], 38, INK, (244, 246, 250, 245), (20, 6)), x0 + 12, y0 + im.height - 40)
        if val: put(fr, badge(val, 38), x0 + 82, y0 + im.height - 40)


def grid(fr, pre, y0, w=380, gap=380, vals=None, dx=480):
    for i, k in enumerate('ABCD'):
        spr(fr, pre + k, 540 - dx / 2 + (i % 2) * dx, y0 + (i // 2) * gap, w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '위 판을 돌려 겹치면 빛은 몇 번 구멍으로?')
grid(fr, 'p', 640, 440, 330, dx=500)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '두 판 모두 구멍이 있어야 빛이 지나간다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 위 판을 화살표 칸 수만큼 시계방향으로 돌린다', '2. 돌린 위 판을 아래 판 위에 겹친다',
                          ('3. 구멍이 겹치는 번호는 딱 하나', YEL)], 34)
spr(fr, 'pA', 540, 830, 860, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 구멍이 겹치는 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 5 · B 1 · C 7 · D 2 번에서 겹친다면', ('암호 5172', YEL), '',
                          ('8번 다음은 다시 1번이에요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
grid(fr, 'p', 520, 400, 300, dx=500)
fr.alpha_composite(panel(960, 110), (60, 985))
text_lines(fr, 540, 1003, ['위 판 = 시계방향으로 화살표 칸 수만큼', ('암호 = 구멍이 겹치는 번호 A B C D', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', f'반대로 돌리면 {PROOF["trap_counter_clockwise"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('시계방향은 1 → 2 → 3 쪽이에요.', WHITE), '위 판 구멍 번호에', '돌린 칸 수를 더해 보세요.',
                          ('8을 넘으면 8을 빼요 (7 + 2 = 9 → 1)', YEL)], 35)
spr(fr, 'pD', 540, 900, 820, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '돌린 위 판 구멍(링)과 아래 판 구멍이 겹치는 곳')
fr.alpha_composite(panel(960, 160), (60, 280))
text_lines(fr, 540, 300, ['위 판 구멍 번호 + 돌린 칸 수', ('A 3 · B 8 · C 4 · D 2', YEL)], 31, center=True)
grid(fr, 'a', 640, 330, 360, list(CODE), dx=470)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 3 · B 8 · C 4 · D 2')
for i, k in enumerate('ABCD'):
    spr(fr, 'a' + k, 165 + i * 250, 640, 230, val=CODE[i])
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 975)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
