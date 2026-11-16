"""ROOM 187 cards (전신 거울) in the 3D style (kit/style3d.py), from the mirror sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 187, '2026.12.16'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_full_height']
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

fr = card(ROOM, DATE, 1, 7, '전신 거울', '머리부터 발끝까지, 거울은 최소 몇 칸?')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '거울 규칙', '벽에 붙이는 평평한 거울이에요')
fr.alpha_composite(panel(960, 330), (60, 290))
text_lines(fr, 100, 322, ['1. 거울 1칸 = 세로 20cm', '2. 거울은 벽 어느 높이에나 붙일 수 있어요', '3. 서 있는 자리에서 그대로 거울을 봐요',
                          '4. 머리끝부터 발끝까지 전부 보여야 해요', ('필요한 최소 칸 수를 세요', YEL)], 33)
one(fr, 'qB', 540, 870, 560, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 필요한 거울 칸 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 3칸 · 5칸 · 1칸 · 6칸이면', ('암호 3516', YEL), '', ('멀리 서면 거울이 작아도 될까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '거울 1칸 = 20cm · 키와 거리를 보세요')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '빛이 거울 어디에서 꺾이는지 보세요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('머리끝에서 온 빛은 눈과 머리끝의', WHITE), '딱 중간 높이에서 반사돼 눈에 들어와요.', '발끝 빛도 눈과 발 사이 중간에서 반사돼요.',
                          (f'키만큼 거울이 필요하다고 하면 함정 {TRAP}', YEL)], 33)
one(fr, 'qD', 540, 880, 520, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '거울은 키의 절반, 거리는 상관없어요')
four(fr, 'r', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '멀리 서도 거울은 작아지지 않아요')
one(fr, 'rB', 300, 560, 500, tag=False); one(fr, 'rD', 790, 560, 500, tag=False)
fr.alpha_composite(panel(960, 300), (60, 800))
text_lines(fr, 100, 830, ['B와 D: 키 160cm면 2m에서도 0.5m에서도', '거울 80cm, 딱 4칸이면 전신이 다 보여요'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1010)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
