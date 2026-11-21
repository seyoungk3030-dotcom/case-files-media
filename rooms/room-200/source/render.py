"""ROOM 200 cards (강물에 떨어진 모자) in the 3D style (kit/style3d.py), from the side-view sprites made by scene3d.py, with each
board's speed and the sticker's ground speed written under it. All sprites are cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
from verify import BOARDS
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 200, '2026.12.20'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; MIN = PROOF['minutes']
DIR = {'up': '거슬러', 'down': '따라'}
POW = lambda v, v2: '같은 속도로' if v == v2 else ('2배 빠르게' if v2 == 2 * v else '절반 속도로')
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 20, min(b[1] for b in bb) - 20, max(b[2] for b in bb) + 20, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); k = n[1]; d, cur, v, t1, v2 = BOARDS[k]; out = Image.new('RGBA', (c.width, c.height + 150), (0, 0, 0, 0)); out.alpha_composite(c, (0, 0))
    if n[0] == 'p': lines = ((f'물살 {cur} · {DIR[d]} {t1}분 저음', WHITE), (f'돌아올 땐 {POW(v, v2)}', YEL))
    else: lines = ((f'{MIN[k]}분 만에 주움', MINT), (f'{t1}분' + (' 그대로' if v == v2 else (' ÷ 2' if v2 == 2 * v else ' × 2')), SOFT))
    for j, (t, col) in enumerate(lines): put(out, text_layer(t, 62 if j == 0 else 54, col), c.width / 2, c.height + 30 + j * 76)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((out.width - 1, out.height - 1), (255, 255, 255, 44))
    out.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 30, y0 + 30)
    if val: put(fr, badge(val, 46), x0 + im.width - 40, y0 + im.height * 0.42)


POS = [(290, 520), (790, 520), (290, 945), (790, 945)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '강물에 떨어진 모자', '돌아가서 모자를 줍기까지 몇 분?')
four(fr, 'q', 460)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '강물은 오른쪽으로 흘러요 (분당 m)')
fr.alpha_composite(panel(960, 400), (60, 290))
text_lines(fr, 100, 322, ['1. 배에서 모자가 떨어져 물에 둥둥 떠내려가요', '2. 모르고 물살을 거슬러/따라 몇 분 더 저었어요', '3. 알아채자마자 바로 돌아서 모자로 가요',
                          '4. 노 젓는 속도는 물 위에서 잰 속도예요', ('돌아선 뒤 모자를 줍기까지 걸린 분이 각 자리 숫자', YEL)], 32)
one(fr, 'qA', 540, 930, 420, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 걸린 시간(분)')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2분 · 9분 · 5분 · 1분이라면', ('암호 2951', YEL), '', ('물살을 거슬러 돌아가면 더 오래 걸릴까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '돌아선 뒤 몇 분 만에 모자를 주울까?')
four(fr, 'q', 460)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '강가 말고 물 위에서 보세요', CORAL)
fr.alpha_composite(panel(960, 400), (60, 300))
text_lines(fr, 100, 330, [('물살은 배도 모자도 똑같이 밀어요', WHITE), '물 위에 뜬 뗏목에서 보면 모자는 가만히 있어요', '그럼 물살은 없는 것과 같아요',
                          ('물살 숫자로 계산하면 함정', YEL)], 35)
one(fr, 'qC', 540, 950, 400, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '물살은 아무 상관이 없어요')
four(fr, 'r', 460, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '멀어진 시간만큼 돌아오면 끝')
one(fr, 'rA', 300, 560, 400, tag=False); one(fr, 'rD', 790, 560, 400, tag=False)
fr.alpha_composite(panel(960, 260), (60, 900))
text_lines(fr, 100, 925, ['A: 4분 멀어지고 같은 속도로 돌아옴 → 4분', 'D: 2분 멀어지고 절반 속도로 돌아옴 → 4분'], 31)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1100)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
