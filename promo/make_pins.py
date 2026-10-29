"""Two extra pinned carousels next to promo/intro: 'duel' (three puzzles to race a friend on) and 'levels'
(an easy-medium-hard test). Each is a cover, three puzzles, then three answers, reusing the rooms' own cards."""
import os, sys
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'kit'))
from style3d import *
R = os.path.join(HERE, '..', 'rooms')
W, H = 1080, 1350
SETS = {
 'duel': {'title': '친구랑 대결', 'sub': '같은 3문제, 누가 먼저 다 풀까?',
          'rooms': [(38, '1라운드'), (46, '2라운드'), (49, '3라운드')], 'foot': '대결할 친구를 태그하세요 · 정답은 5~7장',
          'line': '친구에게 보내고 시간 재기!', 'last': '이긴 사람 댓글로 · 친구 태그하고 재대결!'},
 'levels': {'title': '두뇌 레벨 테스트', 'sub': '쉬움 → 보통 → 어려움, 어디까지 가나요?',
            'rooms': [(51, '쉬움'), (48, '보통'), (44, '어려움')], 'foot': '몇 단계까지 풀었는지 댓글로 · 정답은 5~7장',
            'line': '저장해 두고 하나씩 도전!', 'last': '몇 개 맞혔는지 댓글로 · 새 문제는 팔로우!'},
}


def header(fr, n, label):
    put(fr, pill(label, 26, SOFT, (255, 255, 255, 26)), 250, 70)
    pg = pill(f'{n:02d} / 07', 26, SOFT, (255, 255, 255, 26)); put(fr, pg, W - 66 - pg.width / 2, 70)


def rounded(im, r=34):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=255)
    out = im.convert('RGBA'); out.putalpha(m); return out


def reuse(room, card, n, label):
    """The room's card with its header pills and its own call to action painted over by a blurred stretch of the
    background next to them (keeps a stock-photo background seamless), then this carousel's header."""
    im = Image.open(f'{R}/room-{room:03d}/cards/card-{card:02d}.png').convert('RGBA')
    for a, b, src in ((30, 108, (108, 116)), (1166, 1282, (1158, 1166))):
        band = im.crop((0, src[0], W, src[1])).resize((W, b - a), Image.BILINEAR).filter(ImageFilter.GaussianBlur(10))
        im.paste(band, (0, a))
    header(im, n, label); return im


def make(key):
    S = SETS[key]; out = os.path.join(HERE, key); os.makedirs(out, exist_ok=True)
    bg, bok = background(900 + len(key), W, H, 0.45); fr = bg.copy(); fr.alpha_composite(bok.crop((0, 377, W, 377 + H)))
    header(fr, 1, '퇴근 후 사건파일')
    put(fr, text_layer(S['title'], 92, WHITE), 540, 220); put(fr, text_layer(S['sub'], 40, MINT, 'Bold'), 540, 330)
    for i, (room, tag) in enumerate(S['rooms']):
        th = rounded(Image.open(f'{R}/room-{room:03d}/cards/card-01.png').resize((300, 375), Image.LANCZOS), 26)
        cx = 190 + i * 350; cy = 700
        sh = Image.new('RGBA', (th.width + 60, th.height + 60), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([30, 36, th.width + 30, th.height + 36], 26, fill=(0, 0, 0, 150))
        fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)), (int(cx - sh.width / 2), int(cy - sh.height / 2)))
        fr.alpha_composite(th, (int(cx - th.width / 2), int(cy - th.height / 2)))
        put(fr, pill(tag, 34, INK, (255, 196, 92, 250), (28, 10)), cx, cy - th.height / 2 - 10)
    put(fr, text_layer(S['line'], 46, WHITE, 'Bold'), 540, 1000)
    cta(fr, S['foot']); fr.convert('RGB').save(f'{out}/{key}-1.png')
    for i, (room, tag) in enumerate(S['rooms']):
        fr = reuse(room, 4, 2 + i, f'{tag}  ·  ROOM {room:03d}')
        cta(fr, '먼저 풀고 → 정답은 5장부터' if i < 2 else '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', None if i < 2 else CORAL)
        fr.convert('RGB').save(f'{out}/{key}-{2 + i}.png')
    for i, (room, tag) in enumerate(S['rooms']):
        fr = reuse(room, 7, 5 + i, f'{tag} 정답  ·  ROOM {room:03d}')
        cta(fr, S['last'] if i == 2 else '맞혔다면 다음 장으로')
        fr.convert('RGB').save(f'{out}/{key}-{5 + i}.png')
    print(key, 'ok')


for k in SETS: make(k)
