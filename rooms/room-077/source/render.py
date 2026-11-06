"""ROOM 077 cards in the 3D style (kit/style3d.py). Each wheel's turn is baked into q*/r*.png (sprite + turn text on
transparency, fixed canvas) so the reel (short3d.py) shows the same instructions."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 77, '2026.11.09'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
T = {k: v[1] for k, v in PROOF['wheels_clockwise_from_top_and_turn'].items()}


def turn_text(t): return f'시계 방향 ↻ {t}칸' if t > 0 else f'반시계 방향 ↺ {-t}칸'


def qsprite(k, ans=False):
    im = Image.open(f'{B}/{"a" if ans else "p"}{k}.png').convert('RGBA'); im = im.crop((60, 40, 840, 860))
    im = im.resize((400, 420), Image.LANCZOS)
    out = Image.new('RGBA', (480, 500), (0, 0, 0, 0)); out.alpha_composite(im, (40, 0))
    lay = text_layer(f'꼭대기 = {CODE["ABCD".index(k)]}', 40, MINT, 'Black', glow=MINT) if ans else text_layer(turn_text(T[k]), 36, YEL, 'Black')
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

fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '돌린 뒤 꼭대기에 오는 칸 번호는?')
grid(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '관람차를 칸 수만큼 돌려요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 관람차는 적힌 방향으로 적힌 칸 수만큼 돌아요', '2. 칸은 매달려 있어서 숫자는 늘 똑바로예요',
                          '3. 1칸 = 옆 칸 자리까지', ('돌린 뒤 꼭대기 칸의 숫자는?', YEL)], 33)
im = Image.open(f'{B}/qA.png'); fr.alpha_composite(im.resize((384, 400)), (348, 630))
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 꼭대기 칸 숫자')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 260), (60, 700))
text_lines(fr, 540, 735, ['예: 꼭대기가 1 · 2 · 3 · 4이면', ('암호 1234', YEL)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '방향을 잘 보세요 · 시계 ↻ / 반시계 ↺')
grid(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '꼭대기 칸이 어디로 가는지 말고', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('어느 칸이 꼭대기로 올라오는지 보세요', WHITE), '시계 방향으로 돌면 바퀴 왼쪽이 올라가요.', '반시계 방향이면 오른쪽이 올라가요.',
                          ('꼭대기에서 반대 방향으로 칸을 세요!', YEL)], 34)
im = Image.open(f'{B}/qD.png'); fr.alpha_composite(im.resize((384, 400)), (348, 680))
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '돌린 뒤의 관람차 · 빛나는 칸이 꼭대기')
grid(fr, 'r')
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '시계 방향이면 왼쪽 칸이 올라와요')
for i, k in enumerate('ABCD'):
    im = Image.open(f'{B}/a{k}.png').convert('RGBA').crop((60, 40, 840, 860)).resize((220, 231), Image.LANCZOS); cx = 165 + i * 250
    fr.alpha_composite(im, (cx - 110, 360)); put(fr, badge(CODE[i], 46), cx, 640)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 860)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 990)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
