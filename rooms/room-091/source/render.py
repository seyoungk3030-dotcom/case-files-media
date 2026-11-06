"""ROOM 091 cards in the 3D style (kit/style3d.py), from the warehouse push-box sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 91, '2026.11.14'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 40, y0 + 36)
    if val: put(fr, badge(val, 46), x0 + im.width - 44, y0 + 40)


POS = [(292, 505), (788, 505), (292, 940), (788, 940)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '상자를 초록 칸까지 최소 몇 번 밀까?')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '창고 규칙', '노란 직원이 나무 상자를 옮겨요')
fr.alpha_composite(panel(960, 330), (60, 290))
text_lines(fr, 100, 322, ['1. 직원은 위·아래·왼쪽·오른쪽으로 걸어요', '2. 상자는 밀기만 돼요 (당기기 금지)', '3. 검은 벽과 바깥으로는 못 가요',
                          '4. 걷는 건 공짜, 상자 한 칸 밀기 = 1번', ('최소 몇 번 밀어야 할까요?', YEL)], 33)
one(fr, 'qA', 540, 880, 560, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 최소 밀기 횟수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2번 · 6번 · 4번 · 7번이면', ('암호 2647', YEL), '', ('상자 칸 수만 세면 틀려요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '밀려면 상자 반대편에 서야 해요')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', 'A는 바로 옆인데 1번이 아니에요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('상자를 왼쪽으로 밀려면', WHITE), '직원이 상자 오른쪽에 서야 해요.', '그 자리가 벽이면 돌아서 밀어야 해요.',
                          ('벽에 붙은 상자는 그 방향으로 못 밀어요!', YEL)], 35)
one(fr, 'qA', 540, 880, 520, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '빨간 화살표 = 상자가 밀려 가는 길')
four(fr, 'r', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '돌아가는 길이 가장 빠를 때가 있어요')
one(fr, 'rA', 300, 560, 500, tag=False); one(fr, 'rC', 790, 560, 500, tag=False)
fr.alpha_composite(panel(960, 300), (60, 800))
text_lines(fr, 100, 830, ['A: 오른쪽이 벽 → 아래·왼쪽·위로 3번', 'C: 위로 올렸다가 오른쪽으로 쭉, 5번'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1010)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
