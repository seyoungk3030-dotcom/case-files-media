"""ROOM 182 cards in the 3D style (kit/style3d.py), from the shoe sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png)."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 182, '2026.12.14'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_half_of_each_colour']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
for key in 'ABCD':
    bb = [ims[f'{s}{key}'].getchannel('A').getbbox() for s in 'pa']
    BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
    for s in 'pa':
        c = ims[f'{s}{key}'].crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
        c.save(f'{B}/{"q" if s == "p" else "r"}{key}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 - 4, y0 + im.height / 2 - 30)
    if val: put(fr, badge(val, 44), x0 + im.width - 20, y0 + 20)


POS = [(282, 520), (798, 520), (282, 930), (798, 930)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '현관 신발', '같은 색 두 짝이면 한 켤레? 대부분 틀려요')
four(fr, 'q', 505)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '켤레 규칙', '위에서 내려다본 현관 매트')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['한 켤레 = 같은 색의 왼쪽 한 짝 + 오른쪽 한 짝', '신발은 이리저리 돌아가 있어요',
                          '엄지발가락 쪽이 볼록 튀어나와요', ('매트마다 온전한 켤레는 몇 개?', YEL)], 30)
one(fr, 'qA', 540, 900, 800, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 켤레 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 1켤레 · 4켤레 · 0켤레 · 2켤레면', ('암호 1402', YEL), '', ('빨강 두 짝이 둘 다 왼쪽이면?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '같은 색 왼쪽 + 오른쪽 = 1켤레')
four(fr, 'q', 505)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '신발 코가 위로 가게 머릿속으로 돌려 보세요', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('코가 위를 볼 때 오른쪽이 볼록하면 왼발', WHITE), '왼쪽이 볼록하면 오른발 신발이에요',
                          '색마다 왼발 수와 오른발 수 중 작은 쪽이 켤레 수', (f'색마다 반으로 나누면 함정 {TRAP}', YEL)], 31)
one(fr, 'qA', 540, 900, 800, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 = 짝이 맞는 신발 · 어두운 신발 = 짝 없음')
four(fr, 'r', 505, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'rD', 540, 560, 800, tag=False)
fr.alpha_composite(panel(960, 200), (60, 850))
text_lines(fr, 100, 880, ['D: 빨강은 전부 왼발, 파랑은 전부 오른발', '신발이 7짝이나 있어도 켤레는 0개!'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1130)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
