"""ROOM 129 cards in the 3D style (kit/style3d.py), from the spirit-level sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 129, '2026.11.27'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_rolls_down']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 22, y0 + 34)
    if val: put(fr, badge(val, 44), x0 + im.width - 40, y0 + 40)


POS = [(292, 530), (788, 530), (292, 930), (788, 930)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '수평계 거품은 어디에?', '기울어진 선반 위 수평계의 공기 방울')
four(fr, 'q', 470)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '수평계 규칙', '선반 양 끝은 같은 블록 위에 놓여 있어요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['평평하면 거품은 가운데 5에 있어요', '블록 1개 차이마다 눈금 1칸 움직여요',
                          '거품이 멈추는 눈금 숫자는?', ('거품은 어느 쪽으로 갈까요?', YEL)], 33)
one(fr, 'qA', 540, 880, 640, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 거품 아래 숫자')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2 · 6 · 1 · 9 눈금이면', ('암호 2619', YEL), '', ('목수 아저씨 공구함에 꼭 있는 그것', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '구슬이라면 낮은 쪽으로 굴러가겠죠?')
four(fr, 'q', 470)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '거품은 물보다 훨씬 가벼워요', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('무거운 물이 낮은 쪽으로 내려가면', WHITE), '가벼운 공기는 밀려서 높은 쪽으로 가요',
                          '높은 쪽 = 블록이 더 많이 쌓인 쪽', ('구슬처럼 내려간다고 하면 함정!', YEL)], 33)
one(fr, 'qB', 540, 880, 640, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 동그라미 = 거품 자리')
four(fr, 'r', 470, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'qA', 540, 450, 640, tag=False); one(fr, 'rA', 540, 720, 640, tag=False)
fr.alpha_composite(panel(960, 200), (60, 880))
text_lines(fr, 100, 910, ['A: 오른쪽이 블록 3개 더 높아요', '거품은 높은 쪽으로 3칸 → 8'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1135)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
