"""ROOM 066 cards in the 3D style (kit/style3d.py), from the spool sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 66, '2026.11.06'
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




BOX = (55, 65, 1015, 392)   # same crop for every sprite so all rows share one scale


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png').convert('RGBA').crop(BOX); sc = w / im.width
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag:
        put(fr, pill(name[1], 38, INK, (244, 246, 250, 245), (20, 6)), x0 - 34, cy - (28 if val else 0))
        if val: put(fr, badge(val, 34), x0 - 34, cy + 50)


def rows(fr, pre, y0, w, gap, vals=None):
    for i, k in enumerate('ABCD'):
        one(fr, pre + k, 565, y0 + i * gap, w, val=vals[i] if vals else None)


fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '실을 당기면 실패는 몇 칸 굴러갈까?')
rows(fr, 'p', 395, 620, 214)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '실패는 미끄러지지 않고 굴러요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 축(크림색)은 바퀴 크기의 절반', '2. 실은 축 아래 또는 위에서 나와요',
                          '3. 고리를 적힌 칸만큼 오른쪽으로 당기면', ('실패 중심은 몇 칸 굴러갈까?', YEL)], 34)
one(fr, 'pC', 540, 800, 940, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 실패가 굴러간 칸 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A 1칸 · B 5칸 · C 8칸 · D 2칸이면', ('암호 1582', YEL), '',
                          ('당긴 만큼 간다고 생각하면 함정', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '축은 바퀴의 절반 · 암호 = 굴러간 칸 수 A B C D')
rows(fr, 'p', 395, 620, 214)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', f'당긴 만큼 굴러간다고 하면 {PROOF["trap_same_as_pulled"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('바닥에 닿은 점은 멈춰 있어요', WHITE), '축 아래쪽은 실패 속도의 절반,', '축 위쪽은 1.5배로 움직여요.',
                          ('실이 어디서 나오는지가 핵심!', YEL)], 35)
one(fr, 'pB', 540, 860, 940, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '아래 실은 당긴 칸 × 2 · 위 실은 × 2/3')
fr.alpha_composite(panel(960, 160), (60, 280))
text_lines(fr, 540, 300, ['A 3×2=6 · B 6×2/3=4', ('C 4×2=8 · D 3×2/3=2', YEL)], 31, center=True)
rows(fr, 'a', 545, 480, 166, list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 6 · B 4 · C 8 · D 2')
rows(fr, 'a', 360, 430, 148, list(CODE))
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 960)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
