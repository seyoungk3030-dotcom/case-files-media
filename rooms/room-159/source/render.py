"""ROOM 159 cards in the 3D style (kit/style3d.py), from the train sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png)."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 159, '2026.12.07'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_queue']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 30, y0 + im.height - 34)
    if val: put(fr, badge(val, 44), x0 + im.width / 2, y0 + 34)


POS = [(540, 420), (540, 625), (540, 830), (540, 1035)]


def four(fr, pre, w=980, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '세 번째로 나가는 칸은?', '별 칸은 막다른 옆 선로로 들어가요')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '기차 규칙', '앞 칸(왼쪽)부터 하나씩 출구로')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['기차는 왼쪽 출구로 가요. 맨 앞 칸부터 차례로', '별 없는 칸은 회전판을 지나 바로 출구로 나가요',
                          '별 칸은 회전판에서 돌아 위쪽 막다른 선로로 들어가요', ('다 지나가면 옆 선로 칸들이 나와 출구로 가요', YEL)], 29)
one(fr, 'qA', 540, 850, 980, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 세 번째로 나간 칸 숫자')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 세 번째 칸이 3 · 9 · 1 · 2면', ('암호 3912', YEL), '', ('출구를 지나간 순서로 세요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '세 번째로 출구를 지나는 칸의 숫자')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '별 칸은 들어간 순서대로 나올까요?', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('옆 선로는 막다른 길이에요', WHITE), '들어간 입구로 다시 나와야 해요',
                          '입구 쪽에 있는 칸, 즉 마지막에 들어간 칸이 먼저!', (f'들어간 순서대로 세면 함정 {TRAP}', YEL)], 33)
one(fr, 'qB', 540, 850, 980, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '출구로 나간 순서, 민트 = 세 번째 칸')
four(fr, 'r', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'qA', 540, 430, 980, tag=False); one(fr, 'rA', 540, 640, 980, tag=False)
fr.alpha_composite(panel(960, 230), (60, 830))
text_lines(fr, 100, 860, ['A: 2, 1이 먼저 나가고', '옆 선로에서는 9 → 4 → 7 순서로 나와요'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1135)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
