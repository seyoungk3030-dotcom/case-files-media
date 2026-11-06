"""ROOM 076 cards in the 3D style (kit/style3d.py). Each trap question is baked into q*.png (sprite + question text on
transparency) so the reel (short3d.py) shows the same questions."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 76, '2026.11.09'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
Q = {'A': ['셔츠 3장 말리는 데 1시간', '6장은 몇 시간?'], 'B': ['기계 5대가 5분에 부품 5개', '100대가 100개는 몇 분?'],
     'C': ['달걀 1개 삶는 데 6분', '한 냄비에 3개는 몇 분?'], 'D': ['2등을 따라잡아 추월했어요', '나는 지금 몇 등?']}
U = {'A': '시간', 'B': '분', 'C': '분', 'D': '등'}


def qsprite(k, ans=False):
    im = Image.open(f'{B}/p{k}.png').convert('RGBA'); im = im.crop(im.getchannel('A').getbbox())
    sc = min(420 / im.width, 250 / im.height); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    out = Image.new('RGBA', (480, 400), (0, 0, 0, 0)); out.alpha_composite(im, ((480 - im.width) // 2, 260 - im.height))
    l1 = text_layer(Q[k][0], 30, WHITE, 'Bold'); l2 = text_layer(Q[k][1], 34, YEL, 'Black')
    if ans: l2 = text_layer(f'{CODE["ABCD".index(k)]}{U[k]}', 44, MINT, 'Black', glow=MINT)
    put(out, l1, 240, 300); put(out, l2, 240, 352 if not ans else 356)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((479, 399), (255, 255, 255, 44))
    out.save(f'{B}/{"a" if ans else "q"}{k}.png'); return out


for k in 'ABCD': qsprite(k); qsprite(k, True)


def grid(fr, pre, y0=330, vals=None):
    for i, k in enumerate('ABCD'):
        im = Image.open(f'{B}/{pre}{k}.png'); x, y = 60 + (i % 2) * 480, y0 + (i // 2) * 410
        fr.alpha_composite(im, (x, y)); put(fr, pill(k, 38, INK, (244, 246, 250, 245), (20, 6)), x + 40, y + 30)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '직감이 틀리는 문제 4개', '바로 떠오른 답은 대부분 함정이에요')
grid(fr, 'q', 320)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '네 문제, 답은 모두 한 자리 숫자')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 말 그대로 일어나는 상황을 떠올려요', '2. 빨래 줄, 냄비 자리는 충분해요',
                          '3. 단위(시간, 분, 등)는 빼고 숫자만', ('A B C D 답을 이으면 암호!', YEL)], 34)
im = Image.open(f'{B}/qA.png'); fr.alpha_composite(im, (300, 650))
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 답의 숫자를 차례로')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 260), (60, 700))
text_lines(fr, 540, 735, ['예: 2시간 · 7분 · 3분 · 4등이면', ('암호 2734', YEL)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '직감 말고 상황을 그려 보세요')
grid(fr, 'q', 320)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '숫자를 곱하지 마세요', CORAL)
fr.alpha_composite(panel(960, 380), (60, 300))
text_lines(fr, 100, 330, [('빨래와 달걀은 하나씩 차례로 할까요?', WHITE), '아니면 동시에 될까요?', '기계 1대는 부품 1개에 몇 분 걸릴까요?',
                          '2등을 추월하면 1등은 아직 앞에 있어요.', ('함정 답: 2 · 100 · 18 · 1', YEL)], 34)
im = Image.open(f'{B}/qD.png'); fr.alpha_composite(im, (300, 720))
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '빨래·달걀은 동시에 · 기계 1대는 5분에 1개 · 1등은 그대로')
grid(fr, 'a', 320)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '1시간 · 5분 · 6분 · 2등')
for i, k in enumerate('ABCD'):
    im = Image.open(f'{B}/p{k}.png').convert('RGBA'); im = im.crop(im.getchannel('A').getbbox()); sc = min(300 / im.width, 170 / im.height)
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS); cx, cy = 300 + (i % 2) * 480, 430 + (i // 2) * 230
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))); put(fr, badge(CODE[i], 44), cx - 190, cy)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 960)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
