"""ROOM 085 cards in the 3D style (kit/style3d.py). Each trap question is baked into q*.png (sprite + question text on
transparency) so the reel (short3d.py) shows the same questions."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 85, '2026.11.12'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
Q = {'A': '버스가 → 쪽으로 출발! 헬륨 풍선은?', 'B': '버스가 → 쪽으로 출발! 손잡이는?',
     'C': '아래 페달 끈을 ← 로 당기면 자전거는?', 'D': '배 위 돌을 물에 던지면 수면은?'}
CIR = '①②③④'
OPT = {k: '  '.join(f'{CIR[i]} {o}' for i, o in enumerate(v)) for k, v in PROOF['options'].items()}


def qsprite(k, ans=False):
    im = Image.open(f'{B}/{"a" if ans else "p"}{k}.png').convert('RGBA'); im = im.crop(im.getchannel('A').getbbox())
    sc = min(440 / im.width, 250 / im.height); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    out = Image.new('RGBA', (480, 400), (0, 0, 0, 0)); out.alpha_composite(im, ((480 - im.width) // 2, 255 - im.height))
    put(out, text_layer(Q[k], 25, WHITE, 'Bold'), 240, 292)
    if ans: put(out, text_layer(f'{CODE["ABCD".index(k)]} · {PROOF["true"][k]}', 36, MINT, 'Black', glow=MINT), 240, 350)
    else:
        o = PROOF['options'][k]; half = (len(o) + 1) // 2
        put(out, text_layer('  '.join(f'{i + 1}. {o[i]}' for i in range(half)), 23, YEL, 'Bold'), 240, 336)
        put(out, text_layer('  '.join(f'{i + 1}. {o[i]}' for i in range(half, len(o))), 23, YEL, 'Bold'), 240, 372)
    out.putpixel((0, 0), (255, 255, 255, 44)); out.putpixel((479, 399), (255, 255, 255, 44))
    out.save(f'{B}/{"a" if ans else "q"}{k}.png' if not ans else f'{B}/r{k}.png'); return out


for k in 'ABCD': qsprite(k); qsprite(k, True)


def grid(fr, pre, y0=330, vals=None):
    for i, k in enumerate('ABCD'):
        im = Image.open(f'{B}/{pre}{k}.png'); x, y = 60 + (i % 2) * 480, y0 + (i // 2) * 410
        fr.alpha_composite(im, (x, y)); put(fr, pill(k, 38, INK, (244, 246, 250, 245), (20, 6)), x + 40, y + 30)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '물리 직감 4문제', '바로 떠오른 답은 대부분 함정이에요')
grid(fr, 'q', 320)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '네 장면, 각각 보기 번호로 답해요')
fr.alpha_composite(panel(960, 290), (60, 290))
text_lines(fr, 100, 322, ['1. 그림의 → 쪽이 앞이에요', '2. 실제로 해 보면 일어나는 일을 골라요',
                          '3. 고른 보기의 번호가 그 칸의 숫자', ('A B C D 번호를 이으면 암호!', YEL)], 34)
im = Image.open(f'{B}/qA.png'); fr.alpha_composite(im, (300, 650))
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 고른 보기 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 260), (60, 700))
text_lines(fr, 540, 735, ['예: 3번 · 1번 · 2번 · 4번을 고르면', ('암호 3124', YEL)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '몸이 느끼는 방향과 다를 수 있어요')
grid(fr, 'q', 320)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '버스 안 공기도 뒤로 쏠려요', CORAL)
fr.alpha_composite(panel(960, 380), (60, 300))
text_lines(fr, 100, 330, [('풍선은 공기보다 가벼워 공기와 반대로 가요', WHITE), '페달은 자전거와 같은 쪽으로 움직여요.', '배 위 돌은 무게만큼 물을 밀어내요.',
                          '가라앉은 돌은 자기 부피만큼만 밀어내요.', ('돌은 물보다 훨씬 무거워요!', YEL)], 33)
im = Image.open(f'{B}/qD.png'); fr.alpha_composite(im, (300, 720))
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '풍선은 앞 · 손잡이는 뒤 · 자전거는 뒤 · 수면은 내려가요')
grid(fr, 'r', 320)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '앞 · 뒤 · 뒤 · 내려가요')
for i, k in enumerate('ABCD'):
    im = Image.open(f'{B}/p{k}.png').convert('RGBA'); im = im.crop(im.getchannel('A').getbbox()); sc = min(300 / im.width, 170 / im.height)
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS); cx, cy = 300 + (i % 2) * 480, 430 + (i // 2) * 230
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))); put(fr, badge(CODE[i], 44), cx - 190, cy)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 960)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
