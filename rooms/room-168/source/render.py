"""ROOM 168 cards in the 3D style (kit/style3d.py), from the bookshelf sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png)."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 168, '2026.12.10'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_whole_books']
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


POS = [(292, 535), (788, 535), (292, 935), (788, 935)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '책벌레는 몇 cm를 갉아 먹을까?', '책꽂이 책벌레, 대부분 다 더해요')
four(fr, 'q', 450)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '책벌레 규칙', '책은 책등이 보이게 순서대로 꽂혀 있어요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['책벌레가 꼬리표의 첫 쪽에서 출발해', '마지막 쪽(빨간 핀)까지 옆으로 똑바로 뚫고 가요',
                          '책 두께는 책등에 적혀 있고 표지는 무시해요', ('책벌레가 뚫는 길이는 몇 cm일까요?', YEL)], 30)
one(fr, 'qA', 540, 850, 640, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 뚫은 길이(cm)')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 5 · 1 · 8 · 2cm면', ('암호 5182', YEL), '', ('첫 쪽은 책의 어느 쪽 끝에 있을까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '책벌레가 뚫는 길이는 몇 cm?')
four(fr, 'q', 450)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '책을 직접 꽂아 보세요', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('책등이 보이게 꽂으면 앞표지는 오른쪽!', WHITE), '그래서 1쪽은 책의 오른쪽 끝, 마지막 쪽은 왼쪽 끝',
                          'A: 1권 오른쪽 끝 → 3권 왼쪽 끝 = 2권만 뚫어요', (f'책을 다 더하면 함정 {TRAP}', YEL)], 31)
one(fr, 'qA', 540, 860, 640, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 선이 책벌레가 뚫은 길')
four(fr, 'r', 450, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'rD', 540, 560, 640, tag=False)
fr.alpha_composite(panel(960, 230), (60, 860))
text_lines(fr, 100, 890, ['D: 4권 첫 쪽(오른쪽 끝)에서 2권 마지막 쪽(왼쪽 끝)', '4권, 3권, 2권을 모두 뚫어서 2 + 3 + 2 = 7cm!'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1145)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
