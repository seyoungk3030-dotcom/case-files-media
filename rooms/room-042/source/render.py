"""ROOM 042 cards in the 3D style (kit/style3d.py), from the rolling-dice sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 42, '2026.10.25'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']


def spr(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 60 else 0).getbbox()
    im = im.crop((l - 10, t - 10, r + 10, b + 10)); sc = w / 470; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag:
        put(fr, pill(name[1], 40, INK, (244, 246, 250, 245), (22, 6)), x0 + 30, y0 + 30)
        if val: put(fr, badge(val, 40), x0 + 100, y0 + 30)


def grid(fr, pre, y0, w=420, vals=None, gap=330):
    for i, k in enumerate('ABCD'):
        spr(fr, pre + k, 305 + (i % 2) * 480, y0 + (i // 2) * gap, w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
# 1 hook
fr = card(ROOM, DATE, 1, 7, '화살표대로 주사위를 굴리면', '초록 칸에 도착했을 때 윗면 숫자는?')
grid(fr, 'd', 470, 430, gap=360)
text_lines(fr, 540, 1090, [('주사위는 마주 보는 면의 합이 7', SOFT)], 34, center=True)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules
fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '미끄러지지 않고 넘어지듯 한 칸씩')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 마주 보는 두 면의 합은 항상 7', '2. 화살표 하나 = 그 방향으로 한 번 넘어뜨리기',
                          ('3. 초록 칸에서 위를 보는 숫자가 정답', YEL)], 34)
spr(fr, 'dA', 540, 760, 520, tag=False)
text_lines(fr, 540, 990, ['오른쪽으로 넘어지면 왼쪽 면이 위로 올라온다', ('보이지 않는 면은 7에서 빼서 구한다', YEL)], 34, center=True)
cta(fr, CTA4); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 주사위의 마지막 윗면')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 초록 칸에서 윗면이 A 6, B 1, C 2, D 5라면', ('암호 6125', YEL), '',
                          ('화살표가 두 개면 두 번 굴린다', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
grid(fr, 'd', 450, 410, gap=340)
fr.alpha_composite(panel(960, 110), (60, 1040))
text_lines(fr, 540, 1058, ['마주 보는 면의 합 7 · 화살표마다 한 번 넘어뜨리기', ('암호 = 초록 칸에서의 윗면 A B C D', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

# 5 trap
fr = card(ROOM, DATE, 5, 7, '함정 주의', f'반대 방향으로 굴리면 {PROOF["trap_wrong_direction"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('오른쪽으로 넘어지면 위에 있던 면은', WHITE), '오른쪽을 보게 되고, 왼쪽 면이 위로 와요.', '앞으로 넘어지면 뒷면이 위로 와요.',
                          ('D는 첫 번째 굴림이 함정이에요', YEL)], 35)
spr(fr, 'dD', 540, 880, 520)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '위로 올라오는 면을 7로 구하면')
fr.alpha_composite(panel(960, 260), (60, 280))
text_lines(fr, 100, 300, ['A →  왼쪽 면 = 7-2 = 5', 'B ↓  뒷면 = 7-3 = 4', 'C →→  바닥 = 7-4 = 3',
                          ('D ↓→  오른쪽 1은 그대로, 왼쪽 면 7-1 = 6', YEL)], 32)
grid(fr, 'e', 720, 360, list(CODE), gap=300)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', '초록 칸에 도착한 네 주사위')
grid(fr, 'e', 420, 360, list(CODE), gap=290)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 870)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1020)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
