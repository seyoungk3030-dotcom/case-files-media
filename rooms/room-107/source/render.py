"""ROOM 107 cards in the 3D style (kit/style3d.py), from the moon-orbit sprites. Each board sprite is the top-view
orbit (p*/a*) with the "seen from Earth" moon (v*) beside it, composed here before the shared crop. made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 107, '2026.11.19'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
for s in 'pa':
    for k in 'ABCD':
        o = Image.open(f'{B}/{s}{k}.png').convert('RGBA'); v = Image.open(f'{B}/v{k}.png').convert('RGBA').resize((230, 230), Image.LANCZOS)
        c = Image.new('RGBA', (1140, 900), (0, 0, 0, 0)); c.alpha_composite(o, (0, 0))
        c.alpha_composite(panel(250, 340), (885, 280)); c.alpha_composite(v, (895, 370))
        lab = text_layer('지구에서 본 달', 34, YEL); c.alpha_composite(lab, (1010 - lab.width // 2, 300))
        c.save(f'{B}/c{s}{k}.png')
ims = {f'{s}{k}': Image.open(f'{B}/c{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 22, y0 + 24)
    if val: put(fr, badge(val, 44), x0 + im.width - 14, y0 + im.height - 60)


POS = [(282, 470), (798, 470), (282, 860), (798, 860)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '이 달은 어디에 있을까?', '지구에서 본 달 모양과 같은 위치 번호는?')
four(fr, 'q', 520)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '달의 위상 규칙', '위에서 내려다본 지구와 달 8자리')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['달은 늘 해를 향한 절반이 밝아요', '오른쪽 패널 = 우리나라에서 올려다본 달 모양',
                          '같은 모양으로 보이는 자리를 찾아요', ('밝은 쪽이 왼쪽인지 오른쪽인지가 열쇠', YEL)], 33)
one(fr, 'qA', 540, 880, 960, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 달의 자리 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 8번 · 3번 · 3번 · 1번 자리면', ('암호 8331', YEL), '', ('해의 방향이 판마다 달라요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '지구에 서서 달을 바라본다고 상상하세요')
four(fr, 'q', 520)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '얼마나 차 있나 + 어느 쪽이 밝나', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('가는 초승달 = 해 가까운 쪽 자리', WHITE), '거의 보름달 = 해 반대쪽 자리',
                          '달을 바라볼 때 해가 오른쪽이면 오른쪽이 밝아요', ('모양만 같은 반대편 자리 = 함정!', YEL)], 33)
one(fr, 'qB', 540, 880, 960, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 고리가 그 달의 자리')
four(fr, 'r', 520, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {PROOF['trap_mirror_spot']}")
one(fr, 'rA', 540, 560, 900, tag=False)
fr.alpha_composite(panel(960, 230), (60, 860))
text_lines(fr, 100, 890, ['A의 2번과 4번은 둘 다 초승달 모양', '해가 왼쪽에 있으니 4번에서 보면 오른쪽이 밝아요'], 31)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1145)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
