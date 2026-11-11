"""ROOM 172 cards in the 3D style (kit/style3d.py), from the glass sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png)."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 172, '2026.12.11'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_volume_follows_height']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 - 4, y0 + im.height / 2 - 30)
    if val: put(fr, badge(val, 44), x0 + im.width - 20, y0 + 20)


POS = [(292, 505), (788, 505), (292, 950), (788, 950)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '반만 찼을까?', '물 높이가 반이면 양도 반? 대부분 틀려요')
four(fr, 'q', 345)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '잔 규칙', '눈금은 잔 높이를 똑같이 나눠요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['검은 고리가 잔 안쪽 바닥부터 테두리까지', '높이를 똑같은 간격으로 나눠요',
                          '물은 첫 번째 고리까지 있어요', ('잔을 가득 채우면 지금 물의 몇 배일까요?', YEL)], 30)
one(fr, 'qD', 540, 860, 470, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 몇 배인지')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 100 + 440, 735, ['예: 7 · 0 · 2 · 5배면', ('암호 7025', YEL), '', ('잔의 모양을 잘 보세요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '가득 채우면 지금 물의 몇 배?')
four(fr, 'q', 345)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '위로 갈수록 넓어지는 잔', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('곧은 컵: 높이 1/3이면 양도 1/3이라 3배', WHITE), 'V자 화병: 높이 2배면 폭도 2배라 양은 2×2배',
                          '원뿔 잔: 높이 2배면 폭 2배 · 깊이 2배 → 2×2×2배', (f'높이만 보면 함정 {TRAP}', YEL)], 31)
one(fr, 'qA', 540, 860, 470, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 고리 = 지금 물')
four(fr, 'r', 345, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'rA', 540, 560, 440, tag=False)
fr.alpha_composite(panel(960, 200), (60, 850))
text_lines(fr, 100, 880, ['A 칵테일 잔: 높이 절반까지 찬 물은', '가득 찬 잔의 1/8뿐이에요! 반이 아니라 8배'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1130)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
