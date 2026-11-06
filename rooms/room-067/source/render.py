"""ROOM 067 cards in the 3D style (kit/style3d.py), from the spring sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 67, '2026.11.06'
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




BOX = (95, 35, 490, 975)   # fixed crop, saved back so kit/short3d.py's trim keeps one scale for every sprite


def normalise():
    for k in 'ABCDX':
        for pre in 'pa':
            p = f'{B}/{pre}{k}.png'; im = Image.open(p).convert('RGBA')
            if im.size != (640, 1000): continue
            im = im.crop(BOX)
            for xy in ((0, 0), (im.width - 1, im.height - 1)): im.putpixel(xy, (20, 30, 50, 44))
            im.save(p)


normalise()


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); sc = w / im.width
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag:
        put(fr, pill(name[1], 38, INK, (244, 246, 250, 245), (20, 6)), cx - w * 0.28, y0 - 20)
        if val: put(fr, badge(val, 34), cx + w * 0.22, y0 - 20)


def row(fr, pre, cy, w, vals=None, gap=262):
    for i, k in enumerate('ABCD'):
        one(fr, pre + k, 540 + (i - 1.5) * gap, cy, w, val=vals[i] if vals else None)


fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '추를 걸면 몇 칸 내려갈까?')
row(fr, 'p', 740, 262)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '스프링은 모두 똑같아요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 스프링 하나에 추 1개가 걸리면 1칸 늘어나요', '2. 추 2개면 2칸, 3개면 3칸',
                          '3. 손을 놓으면 추 아래쪽은', ('눈금 몇 칸까지 내려갈까?', YEL)], 34)
one(fr, 'pX', 390, 870, 230, tag=False); one(fr, 'aX', 690, 870, 230, tag=False)
put(fr, text_layer('→', 60, YEL), 540, 650)
put(fr, text_layer('예: 스프링 1개 + 추 2개 = 2칸', 30, SOFT, 'Bold'), 540, 1140)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 추가 내려간 칸 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 1칸 · B 5칸 · C 8칸 · D 2칸이면', ('암호 1582', YEL), '',
                          ('추 개수만 세면 함정', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '추 1개 = 스프링 하나 1칸 · 암호 = 내려간 칸 수')
row(fr, 'p', 740, 262)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', f'추 개수만 세면 {PROOF["trap_count_weights"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('위아래로 이은 스프링은', WHITE), '각자 추 전부를 받아서 늘어난 만큼 더해요.', '나란히 매단 두 스프링은',
                          ('무게를 반씩 나눠 받아요!', YEL)], 35)
one(fr, 'pD', 540, 910, 230, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '위아래는 더하기 · 나란히는 반씩')
fr.alpha_composite(panel(960, 160), (60, 280))
text_lines(fr, 540, 300, ['A 3+3=6 · B 4÷2=2', ('C 3+3+3=9 · D 2÷2+2=3', YEL)], 31, center=True)
row(fr, 'a', 790, 225, list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 6 · B 2 · C 9 · D 3')
row(fr, 'a', 600, 170, list(CODE), gap=200)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 960)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
