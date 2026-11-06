"""ROOM 081 cards in the 3D style (kit/style3d.py). Each wheel's turn is baked into q*/r*.png (sprite + turn text on
transparency, fixed canvas) so the reel (short3d.py) shows the same instructions."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 81, '2026.11.11'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
TT = {'A': '윗층을 ← 방향으로 한 번', 'B': '앞면을 ↻ 시계 방향 한 번', 'C': '오른쪽 층을 ↓ 방향 한 번', 'D': '앞면을 ↺ 반시계 한 번'}


def qsprite(k, ans=False):
    im = Image.open(f'{B}/{"a" if ans else "p"}{k}.png').convert('RGBA'); im = im.crop((70, 128, 656, 714))
    im = im.resize((420, 420), Image.LANCZOS)
    out = Image.new('RGBA', (480, 500), (0, 0, 0, 0)); out.alpha_composite(im, (30, 0))
    lay = text_layer(f'별 칸 = {CODE["ABCD".index(k)]}', 40, MINT, 'Black', glow=MINT) if ans else text_layer(TT[k], 32, YEL, 'Black')
    put(out, lay, 240, 460)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((479, 499), (255, 255, 255, 44))
    out.save(f'{B}/{"r" if ans else "q"}{k}.png')


for k in 'ABCD': qsprite(k); qsprite(k, True)


def grid(fr, pre, y0=310):
    for i, k in enumerate('ABCD'):
        im = Image.open(f'{B}/{pre}{k}.png'); x, y = 60 + (i % 2) * 480, y0 + (i // 2) * 410
        im = im.resize((384, 400), Image.LANCZOS); fr.alpha_composite(im, (x + 48, y))
        put(fr, pill(k, 38, INK, (244, 246, 250, 245), (20, 6)), x + 40, y + 30)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '한 번 돌리면 별 칸(분홍 테두리)에 오는 숫자는?')
grid(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '숫자가 적힌 큐브 퍼즐을 딱 한 번 돌려요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 화살표가 있는 층만 90도 (한 칸) 돌아요', '2. 별 칸은 앞면의 분홍 테두리 자리예요',
                          '3. 누운 숫자도 같은 숫자로 읽어요', ('돌린 뒤 별 칸에 오는 숫자는?', YEL)], 33)
im = Image.open(f'{B}/qA.png'); fr.alpha_composite(im.resize((384, 400)), (348, 630))
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 별 칸 숫자')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 260), (60, 700))
text_lines(fr, 540, 735, ['예: 별 칸이 1 · 2 · 3 · 4가 되면', ('암호 1234', YEL)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '지금 별 칸 숫자가 아니라 돌린 뒤 숫자!')
grid(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '별 칸으로 들어오는 스티커를 거꾸로 따라가요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('윗층이 ← 로 돌면 오른쪽 면이 앞으로 와요', WHITE), '오른쪽 층이 ↓ 로 돌면 윗면이 앞으로 와요.', '앞면이 돌면 앞면 숫자끼리 자리를 바꿔요.',
                          ('보이는 면에서 답이 와요!', YEL)], 33)
im = Image.open(f'{B}/qC.png'); fr.alpha_composite(im.resize((384, 400)), (348, 680))
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '돌린 뒤의 큐브 · 노란 칸이 별 칸')
grid(fr, 'r')
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '들어오는 스티커를 거꾸로 따라가요')
for i, k in enumerate('ABCD'):
    im = Image.open(f'{B}/a{k}.png').convert('RGBA').crop((70, 128, 656, 714)).resize((220, 220), Image.LANCZOS); cx = 165 + i * 250
    fr.alpha_composite(im, (cx - 110, 360)); put(fr, badge(CODE[i], 46), cx, 640)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 860)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 990)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
