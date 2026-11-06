"""ROOM 108 cards in the 3D style (kit/style3d.py), from the Shepard-Metzler block sprites. Each board is one row:
the amber reference, a divider, then the four numbered shapes; built here from the single-shape renders. All sprites are cropped to one
shared box (q*/r*.png) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 108, '2026.11.20'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
from verify import RES
shots = {n[:-4]: Image.open(f'{B}/{n}').convert('RGBA') for n in os.listdir(B) if n[0] in 'sm' and n.endswith('.png')}
bb = [im.getchannel('A').getbbox() for im in shots.values()]
SB = (min(b[0] for b in bb) - 8, min(b[1] for b in bb) - 8, max(b[2] for b in bb) + 8, max(b[3] for b in bb) + 8)
CW = SB[2] - SB[0]; CH = SB[3] - SB[1]
for k in 'ABCD':
    for ans in (False, True):
        row = Image.new('RGBA', (CW * 5 + 90, CH + 70), (0, 0, 0, 0))
        row.alpha_composite(panel(CW + 30, CH + 60), (0, 5)); row.alpha_composite(shots[f's{k}0'].crop(SB), (15, 50))
        lab = text_layer('기준', 58, YEL); row.alpha_composite(lab, (15 + CW // 2 - lab.width // 2, 10))
        for i in range(4):
            x = CW + 90 + i * CW; nm = f'm{k}' if ans and i + 1 == RES[k][0][0] else f's{k}{i + 1}'
            row.alpha_composite(shots[nm].crop(SB), (x, 50))
            p = pill(str(i + 1), 62, INK, (244, 246, 250, 245), (24, 6)); row.alpha_composite(p, (x + CW // 2 - p.width // 2, 6))
        row.save(f'{B}/{"a" if ans else "p"}{k}.png')
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 34, INK, (244, 246, 250, 245), (16, 5)), x0 - 4, y0 + im.height / 2)
    if val: put(fr, badge(val, 40), x0 + im.width + 26, y0 + im.height / 2)


YS = [405, 620, 835, 1050]


def four(fr, pre, w=930, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, 560 if not vals else 512, YS[i], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '돌린 걸까, 뒤집힌 걸까?', '기준 모양을 돌리기만 해서 만든 건 몇 번?')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '돌리기 규칙', '같은 정육면체를 이어 붙인 블록')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['기준 모양을 공중에서 어느 방향으로든 돌려요', '거울에 비친 모양은 돌려서 만들 수 없어요',
                          '블록 하나가 옮겨진 가짜도 섞여 있어요', ('판마다 정답은 딱 하나', YEL)], 33)
one(fr, 'qA', 540, 820, 980, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 돌리기만 한 모양의 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 4번 · 1번 · 1번 · 3번이면', ('암호 4113', YEL), '', ('IQ 테스트 단골 문제예요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '팔이 꺾이는 방향을 따라가 보세요')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '끝에서부터 꺾임을 세어 보세요', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('한쪽 끝에서 출발해 몇 칸 가고 어디로 꺾는지', WHITE), '팔 길이가 다르면 블록이 옮겨진 가짜',
                          '꺾임이 왼쪽·오른쪽 반대면 거울 모양', ('거울 모양 = 함정!', YEL)], 33)
one(fr, 'qB', 540, 830, 980, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 블록이 기준을 돌린 모양')
four(fr, 'r', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {PROOF['trap_mirror']}")
one(fr, 'rA', 540, 470, 980, tag=False)
fr.alpha_composite(panel(960, 230), (60, 700))
text_lines(fr, 100, 730, ['A의 1번은 기준의 거울 모양이에요', '아무리 돌려도 겹치지 않아요 · 3번만 딱 겹쳐요'], 31)
put(fr, text_layer(' '.join(CODE), 100, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
