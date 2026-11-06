"""ROOM 095 cards in the 3D style (kit/style3d.py), from the water-jug sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 95, '2026.11.15'
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
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 - 40, y0 + 40)
    if val: put(fr, badge(val, 44), x0 + im.width + 30, y0 + im.height / 2)


POS = [(292, 500), (788, 500), (292, 880), (788, 880)]


def four(fr, pre, w=330, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

def steps(k):
    p = PROOF['shortest_states'][k]; a, b, _ = PROOF['jugs_a_b_target'][k]; out = []
    for (x, y), (x2, y2) in zip(p, p[1:]):
        if (x2, y2) == (a, y): s = f'{a}L 채우기'
        elif (x2, y2) == (x, b): s = f'{b}L 채우기'
        elif (x2, y2) == (0, y): s = f'{a}L 비우기'
        elif (x2, y2) == (x, 0): s = f'{b}L 비우기'
        elif x2 < x: s = f'{a}L → {b}L 붓기'
        else: s = f'{b}L → {a}L 붓기'
        out.append(f'{s} ({x2}, {y2})')
    return out


fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '목표 양을 만들려면 최소 몇 번?')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '물통 계량 규칙', '눈금 없는 물통 두 개와 수도꼭지')
fr.alpha_composite(panel(960, 330), (60, 290))
text_lines(fr, 100, 322, ['1. 한 통을 가득 채우기 = 1번', '2. 한 통을 다 비우기 = 1번', '3. 한 통을 다른 통에 붓기 = 1번 (넘치기 직전까지)',
                          '4. 어느 한 통에 목표 양이 담기면 끝', ('최소 몇 번 만에 될까요?', YEL)], 31)
one(fr, 'qA', 540, 870, 420, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 최소 동작 횟수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2번 · 4번 · 6번 · 2번이면', ('암호 2462', YEL), '', ('목표 리터 수를 적으면 틀려요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '어느 통부터 채우느냐가 중요해요')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '붓고 남은 물이 열쇠예요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('5L를 채워 3L에 부으면', WHITE), '5L 통에 2L가 남아요.', '남은 양을 다시 옮기면 새로운 양이 생겨요.',
                          ('작은 통, 큰 통 양쪽에서 다 해 보세요!', YEL)], 35)
one(fr, 'qC', 540, 870, 420, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '마지막 모습 · 초록 숫자 = 목표 양')
four(fr, 'r', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A (3L·5L로 4L) 6번 풀이')
fr.alpha_composite(panel(960, 420), (60, 300))
text_lines(fr, 110, 335, [f'{i + 1}. {s}' for i, s in enumerate(steps('A'))], 34)
put(fr, text_layer(' '.join(CODE), 110, MINT, glow=MINT), 540, 900)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
