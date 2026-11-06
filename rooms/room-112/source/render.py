"""ROOM 110 cards in the 3D style (kit/style3d.py), from the water-cup scale sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 112, '2026.11.21'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_always_weight']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    bd = PROOF['boards'][n[1]]; f = c.width / 470
    put(c, pill(f"{bd['m']} g", round(30 * f), INK, (246, 200, 70, 255), (round(14 * f), round(4 * f))), 0.13 * c.width, 0.36 * c.height - 22 * f)
    put(c, pill(f"{bd['V']} cm³", round(26 * f), INK, (246, 200, 70, 255), (round(12 * f), round(4 * f))), 0.13 * c.width, 0.36 * c.height + 22 * f)
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 22, y0 + 34)
    if val: put(fr, badge(val, 44), x0 + im.width / 2 - 40, y0 + im.height - 40)


POS = [(292, 510), (788, 510), (292, 950), (788, 950)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '저울은 몇 g을 가리킬까?', '물컵을 올리고 0에 맞춘 저울이에요')
four(fr, 'q', 450)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '저울 규칙', '물체를 물에 넣으면 저울 숫자가 바뀌어요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['노란 표: 물체의 무게와 부피', '줄에 매단 물체는 받침대가 잡고 있어요',
                          '줄 없는 물체는 그냥 놓아 버려요', ('민트 그림자 = 물체가 멈추는 자리', YEL)], 33)
one(fr, 'qA', 540, 900, 560, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 저울 숫자 ÷ 100')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 저울이 500 g이면 5', ('네 저울의 숫자를 이으면 암호', YEL), '', ('물 1 cm³ = 1 g 이에요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '매단 것과 놓은 것, 무엇이 다를까요?')
four(fr, 'q', 450)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '물이 물체를 밀어 올리는 만큼 물도 눌려요', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('매단 물체: 잠긴 부피만큼만 늘어요 (1 cm³ = 1 g)', WHITE), '떠 있는 물체: 자기 무게가 전부 늘어요',
                          '가라앉은 물체: 바닥에 얹혀 무게가 전부 늘어요', ('매단 것도 무게가 다 늘면 함정!', YEL)], 31)
one(fr, 'qD', 540, 900, 560, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '물에 넣은 뒤 저울이 가리키는 무게')
four(fr, 'r', 450, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'qA', 300, 520, 450, tag=False); one(fr, 'rA', 790, 520, 450, tag=False)
fr.alpha_composite(panel(960, 230), (60, 830))
text_lines(fr, 100, 860, ['700 g 돌이라도 줄이 잡고 있으면', '밀어낸 물 300 cm³ = 300 g만 늘어요'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1135)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
