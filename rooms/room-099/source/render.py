"""ROOM 099 cards in the 3D style (kit/style3d.py), from the paper-loop sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 99, '2026.11.17'
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
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 22, y0 + 24)
    if val: put(fr, badge(val, 44), x0 + im.width - 40, y0 + 40)


POS = [(290, 500), (790, 500), (290, 880), (790, 880)]


def four(fr, pre, w=480, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '점선대로 자르면 고리가 몇 개?')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '종이 고리 자르기', '종이 띠 끝을 붙여 고리를 만들었어요')
fr.alpha_composite(panel(960, 330), (60, 290))
text_lines(fr, 100, 322, ['1. 붙이기 전에 띠를 반 바퀴씩 꼰 것도 있어요', '2. 점선은 고리를 한 바퀴 빙 둘러요', '3. 점선을 따라 끝까지 가위로 잘라요',
                          '4. 잘린 뒤 따로 떨어진 고리 수를 세요', ('고리는 모두 몇 개가 될까요?', YEL)], 31)
one(fr, 'qB', 540, 870, 520, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 잘린 뒤 고리 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2개 · 3개 · 1개 · 2개면', ('암호 2312', YEL), '', ('줄 수만 세면 틀려요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '꼬임이 몇 번인지 먼저 세어 보세요')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '반 바퀴 꼬인 고리 = 뫼비우스의 띠', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('반 바퀴 꼬인 띠는 한 바퀴 돌면 뒤집혀요', WHITE), '그래서 위쪽 줄과 아래쪽 줄이 이어져 버려요.', '꼬임이 짝수면 뒤집히지 않아요.',
                          ('가운데를 자른 뫼비우스 띠는... 직접 해 보세요!', YEL)], 33)
one(fr, 'qA', 540, 880, 520, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '같은 색 = 하나로 이어진 고리')
four(fr, 'r', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'C: 위·아래 줄은 한 고리, 가운데 줄은 따로')
one(fr, 'rC', 540, 560, 640, tag=False)
fr.alpha_composite(panel(960, 250), (60, 850))
text_lines(fr, 100, 885, ['A는 자르면 두 배 길이의 고리 하나!', 'D는 서로 걸린 고리 세 개가 돼요'], 31)
put(fr, text_layer(' '.join(CODE), 80, MINT, glow=MINT), 540, 1050)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
