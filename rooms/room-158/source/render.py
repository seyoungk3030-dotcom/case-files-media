"""ROOM 158 cards in the 3D style (kit/style3d.py), from the fuse sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png)."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 158, '2026.12.06'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_middle']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 20, y0 + 22)
    if val: put(fr, badge(val, 44), x0 + im.width / 2, y0 + 34)


POS = [(540, 420), (540, 625), (540, 830), (540, 1035)]


def four(fr, pre, w=980, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '두 불꽃은 몇 번 기둥에서 만날까?', '양쪽 끝에서 도화선에 불을 붙여요')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '도화선 규칙', '가는 줄 1초 · 굵은 줄 2초')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['불은 가는 줄 한 칸을 1초, 굵은 줄 한 칸을 2초에 타요', '왼쪽 끝은 0초에 바로 불을 붙여요',
                          '노란 시계가 있으면 오른쪽은 그 초만큼 늦게 붙여요', ('두 불꽃이 만나는 기둥 번호가 숫자예요', YEL)], 30)
one(fr, 'qC', 540, 850, 980, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 만나는 기둥 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 3 · 9 · 1 · 2번 기둥이면', ('암호 3912', YEL), '', ('모두 기둥 위에서 딱 만나요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '같은 시각에 같은 기둥에 닿는 곳을 찾아요')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '무조건 한가운데 5번일까요?', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('A: 오른쪽 불은 6초 늦게 출발해요', WHITE), '그동안 왼쪽 불은 혼자 6칸을 가요',
                          '남은 4칸을 둘이 반씩 나눠요', ('가운데 5번은 함정!', YEL)], 33)
one(fr, 'qA', 540, 850, 980, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 고리 = 두 불꽃이 만나는 기둥')
four(fr, 'r', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'qC', 540, 430, 980, tag=False); one(fr, 'rC', 540, 640, 980, tag=False)
fr.alpha_composite(panel(960, 230), (60, 830))
text_lines(fr, 100, 860, ['C: 왼쪽 불은 7번까지 10초', '오른쪽 불도 5초 + 5초 = 10초에 7번 도착!'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1135)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
