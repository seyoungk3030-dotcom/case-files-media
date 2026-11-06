"""ROOM 084 cards in the 3D style (kit/style3d.py). Each hourglass and its steps are baked into q*.png (sprite above,
step list below, fixed canvas) so the reel (short3d.py) shows the same steps; r*.png carry the answer instead."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 84, '2026.11.12'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; G = PROOF['glasses_minutes_steps']


def col(k, ans=False):
    im = Image.open(f'{B}/{"a" if ans else "p"}{k}.png').convert('RGBA'); im = im.crop(im.getchannel('A').getbbox())
    im = im.resize((150, round(im.height * 150 / im.width)), Image.LANCZOS)
    out = Image.new('RGBA', (250, 720), (0, 0, 0, 0)); put(out, text_layer(f'{G[k][0]}분짜리', 34, YEL, 'Black'), 125, 26)
    out.alpha_composite(im, (50, 56)); y = im.height + 56 + 34
    if ans:
        put(out, text_layer('윗칸', 30, SOFT, 'Bold'), 125, y + 10); put(out, text_layer(f'{CODE["ABCD".index(k)]}분', 52, MINT, 'Black', glow=MINT), 125, y + 70)
    else:
        for s in G[k][1]:
            lay = text_layer('↻ 뒤집기', 30, CORAL, 'Black') if s == 'flip' else text_layer(f'{s}분 흐름', 30, WHITE, 'Bold')
            put(out, lay, 125, y); y += 42
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((249, 719), (255, 255, 255, 44))
    out.save(f'{B}/{"r" if ans else "q"}{k}.png')


for k in 'ABCD': col(k); col(k, True)


def row(fr, pre, y0=330, vals=None):
    for i, k in enumerate('ABCD'):
        im = Image.open(f'{B}/{pre}{k}.png'); x = 60 + i * 240
        fr.alpha_composite(im.resize((236, 680), Image.LANCZOS), (x, y0)); put(fr, pill(k, 36, INK, (244, 246, 250, 245), (18, 6)), x + 24, y0 + 80)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '순서대로 하고 나면 윗칸 모래는 몇 분어치?')
row(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '처음엔 모래가 전부 윗칸에 있어요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 모래시계 위 숫자 = 모래가 다 떨어지는 시간', '2. 적힌 순서대로 흘리고 뒤집어요',
                          '3. 눈금 1칸 = 모래 1분어치', ('끝났을 때 윗칸 모래는 몇 분어치?', YEL)], 33)
im = Image.open(f'{B}/qA.png'); fr.alpha_composite(im.resize((200, 576)), (440, 600))
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 윗칸에 남은 분')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 윗칸이 4 · 1 · 0 · 5분어치면', ('암호 4105', YEL), '', ('윗칸이 비었으면 0이에요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '뒤집으면 위와 아래가 바뀌어요')
row(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '윗칸·아랫칸 숫자를 같이 적어 가요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('A: 처음 위 8 · 아래 0', WHITE), '5분 흐름 → 위 3 · 아래 5', '뒤집기 → 위 5 · 아래 3',
                          ('2분 흐름 → 위는 몇 분?', YEL)], 35)
im = Image.open(f'{B}/qC.png'); fr.alpha_composite(im.resize((200, 576)), (440, 640))
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '빛나는 모래가 윗칸에 남은 모래')
row(fr, 'r')
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '비어 있는 윗칸은 더 흐르지 않아요')
for i, k in enumerate('ABCD'):
    im = Image.open(f'{B}/a{k}.png').convert('RGBA'); im = im.crop(im.getchannel('A').getbbox()); im = im.resize((130, round(im.height * 130 / im.width)), Image.LANCZOS)
    cx = 165 + i * 250; fr.alpha_composite(im, (cx - 65, 330)); put(fr, badge(CODE[i], 46), cx, 330 + im.height + 50)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 900)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1030)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
