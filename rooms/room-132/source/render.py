"""ROOM 132 cards in the 3D style (kit/style3d.py), from the weather-vane sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png); the wind-sign pill is baked into each sprite."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 132, '2026.11.28'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_downwind']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    f = c.width / 470; lab = {'A': '깃발', 'B': '굴뚝 연기', 'C': '바람자루', 'D': '바람 없는 날 · 달리는 차'}[n[1]]
    put(c, pill(lab, round(24 * f), INK, (250, 200, 70, 255), (round(12 * f), round(4 * f))), 0.5 * c.width, 0.05 * c.height)
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

fr = card(ROOM, DATE, 1, 7, '풍향계 화살은 어디를 가리킬까?', '상자 속에 풍향계가 숨어 있어요')
four(fr, 'q', 470)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '풍향계 규칙', '깃발 · 연기 · 바람자루로 바람을 읽어요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['풍향계는 화살촉과 넓은 꼬리가 있어요', 'D는 바람이 없고 차가 화살표 쪽으로 달려요',
                          '풍향계 화살촉이 가리키는 숫자는?', ('화살은 바람 따라 날아가는 쪽일까요?', YEL)], 33)
one(fr, 'qA', 540, 900, 560, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 화살촉 쪽 숫자')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2 · 6 · 0 · 9쪽을 가리키면', ('암호 2609', YEL), '', ('지붕 위 수탉 풍향계도 같은 원리', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '바람은 어느 쪽에서 불어오고 있나요?')
four(fr, 'q', 470)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '넓은 꼬리가 바람에 밀려 나가요', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('꼬리가 바람 따라가면 화살촉은 반대쪽', WHITE), '화살촉 = 바람이 불어오는 쪽',
                          '달리는 차에는 앞에서 바람이 와요', ('깃발 방향 그대로 고르면 함정!', YEL)], 33)
one(fr, 'qD', 540, 900, 560, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 화살 = 바람이 불어오는 쪽')
four(fr, 'r', 470, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'qD', 300, 520, 450, tag=False); one(fr, 'rD', 790, 520, 450, tag=False)
fr.alpha_composite(panel(960, 230), (60, 830))
text_lines(fr, 100, 860, ['D: 바람이 없어도 차가 달리면', '앞에서 바람이 와서 화살은 앞을 가리켜요'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1135)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
