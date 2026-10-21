"""ROOM 029 cards in the 3D style (kit/style3d.py), from sprites made by scene3d.py."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE, T = 29, '2026.10.21', '보이지 않는 큐브까지'
CODE = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))['unique_answer']
COUNTS = dict(zip('ABCD', CODE))
COLS = {'A': (109, 218, 197), 'B': (255, 180, 70), 'C': (160, 150, 255), 'D': (240, 120, 110)}


def letter(k): return pill(k, 34, INK, (*COLS[k], 245), (24, 8))


def grid(fr, kind, y0, w, gap_y, show=None):
    for n, k in enumerate('ABCD'):
        sp = sprite(f'{B}/{kind}-{k}.png', width=w)
        cx = 290 + (n % 2) * 500; cy = y0 + (n // 2) * gap_y
        put(fr, sp, cx, cy)
        put(fr, letter(k), cx - w / 2 + 10, cy - sp.height / 2 + 20)
        if show: put(fr, badge(COUNTS[k] if show == 'num' else '?', 44), cx + w / 2 - 20, cy - sp.height / 2 + 30)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


# 1 hook
fr = card(ROOM, DATE, 1, 7, '큐브는 모두 몇 개?', '보이는 것만 세면 틀린다')
grid(fr, 'stack', 520, 420, 470, '?')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules + example
fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '바닥 3×3 칸 위에만 쌓았다')
fr.alpha_composite(panel(960, 220), (60, 290))
text_lines(fr, 100, 322, ['1. 큐브는 모두 같은 크기, 바닥 3×3 칸 위에만', '2. 공중에 뜬 큐브는 없다 (바닥이나 큐브 위)',
                          '3. 안 보이는 곳엔 꼭 필요한 받침만 있다'], 36)
put(fr, sprite(f'{B}/ex.png', width=360), 290, 820); put(fr, sprite(f'{B}/xray-ex.png', width=360), 790, 820)
put(fr, text_layer('→', 80, YEL), 540, 820)
put(fr, text_layer('보이는 큐브 3개', 36, WHITE, 'Bold'), 290, 1050)
put(fr, text_layer('실제로는 4개', 36, YEL, 'Bold'), 790, 1050)
put(fr, text_layer('뒤에 받침이 숨어 있다', 30, SOFT, 'Bold'), 790, 1100)
cta(fr, '4장까지 풀고 댓글에 암호를 남겨주세요'); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 순서로 큐브 개수')
for n, k in enumerate('ABCD'):
    sp = sprite(f'{B}/stack-{k}.png', width=220); cx = 165 + n * 250
    put(fr, sp, cx, 560); put(fr, letter(k), cx, 760); put(fr, badge('?', 40), cx, 860)
fr.alpha_composite(panel(960, 220), (60, 960))
text_lines(fr, 540, 990, ['예: A 3개, B 4개, C 2개, D 6개라면', ('암호는 3426', YEL)], 38, center=True)
cta(fr, '4장까지 풀고 댓글에 암호를 남겨주세요'); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
grid(fr, 'stack', 445, 320, 360)
fr.alpha_composite(panel(960, 180), (60, 990))
text_lines(fr, 100, 1012, ['바닥 3×3 칸 · 공중에 뜬 큐브 없음', '안 보이는 곳엔 꼭 필요한 받침만', ('암호 = A B C D 큐브 개수', YEL)], 34, gap=1.5)
cta(fr, '4장까지 풀고 댓글에 암호를 남겨주세요'); save(fr, 4)

# 5 trap
fr = card(ROOM, DATE, 5, 7, '함정 주의', '보이는 큐브만 세면 6485', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('높이 떠 보이는 큐브를 찾으세요.', WHITE), '그 아래 칸이 다른 큐브에 가려져 있다면',
                          '보이지 않아도 받침 큐브가 꼭 있어요.', ('더미마다 숨은 받침이 하나씩 있다', YEL)], 36)
put(fr, sprite(f'{B}/stack-B.png', width=420), 540, 900)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer reasoning
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '노란 큐브가 숨은 받침')
grid(fr, 'xray', 450, 330, 370, 'num')
fr.alpha_composite(panel(960, 150), (60, 1010))
text_lines(fr, 540, 1030, ['보이는 큐브 6·4·8·5개에', ('숨은 받침 1개씩 더하면 7·5·9·6개', YEL)], 36, center=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', '숨은 받침까지 센 사람만 정답')
for n, k in enumerate('ABCD'):
    sp = sprite(f'{B}/xray-{k}.png', width=220); cx = 165 + n * 250
    put(fr, sp, cx, 520); put(fr, badge(COUNTS[k], 44), cx, 700)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 830)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 960)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
