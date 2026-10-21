"""Reply to answer comments on recent posts (user choice 2026-10-21: "정답만 확인").

Only comments that contain a 4-digit guess get a reply: a congratulation when it matches the
room's answer, otherwise a short hint (how many digits sit in the right place). The answer
itself is never written. Comments without a guess, our own comments, and comments we already
replied to are left alone, so re-running is safe.

Usage: python3 -I kit/comments.py [--dry-run]
"""
import json, os, random, re, sys

KIT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KIT)
import publish as p

ROOMS = os.path.join(os.path.dirname(KIT), 'rooms')
MAX_REPLIES = 30

RIGHT = ['🎉 정답! 사건 해결이에요. 다음 방도 기다릴게요 🔓',
         '🎉 정확해요! 탐정 실력 인정 👏',
         '🎉 정답입니다! 이 방은 탈출 성공 🗝️']
CLOSE = ['아깝다! 4자리 중 {n}자리가 제자리에 있어요. 다시 도전해 보세요 🔍',
         '거의 왔어요! {n}자리는 맞았어요. 나머지를 다시 볼까요? 🔍']
FAR = '아쉬워요! 아직 제자리에 있는 숫자가 없어요. 카드 속 규칙을 다시 볼까요? 🔍'


def answer(room):
    try:
        return str(json.load(open(f'{ROOMS}/room-{room:03d}/notes/proof.json'))['unique_answer'])
    except (OSError, KeyError):
        return None


def guess(text):
    m = re.findall(r'(?<!\d)\d{4}(?!\d)', text)
    if len(m) == 1:
        return m[0]
    digits = re.sub(r'\D', '', text)
    return digits if not m and len(digits) == 4 else None


def message(g, ans):
    if g == ans:
        return random.choice(RIGHT)
    n = sum(a == b for a, b in zip(g, ans))
    return random.choice(CLOSE).format(n=n) if n else FAR


def main(dry):
    me = p.call('/me', {'fields': 'username'}, 'GET')['username']
    sent = 0
    for m in p.recent(25):
        r = re.match(r'\[ROOM (\d+)', m.get('caption') or '')
        ans = r and answer(int(r.group(1)))
        if not ans:
            continue
        cs = p.call(f"/{m['id']}/comments", {'fields': 'id,text,username,replies{username}', 'limit': 50}, 'GET')['data']
        for c in cs:
            if c.get('username') == me or any(x.get('username') == me for x in c.get('replies', {}).get('data', [])):
                continue
            g = guess(c.get('text') or '')
            if not g:
                continue
            msg = message(g, ans)
            print(f"ROOM {int(r.group(1)):03d} {'OK ' if g == ans else 'try'} -> {msg}")
            if not dry:
                p.call(f"/{c['id']}/replies", {'message': msg})
            sent += 1
            if sent >= MAX_REPLIES:
                return print('reply cap reached')
    print(f'replies: {sent}')


if __name__ == '__main__':
    main('--dry-run' in sys.argv)
