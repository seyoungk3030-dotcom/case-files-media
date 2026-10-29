"""Post one promo carousel (promo/<key>/<key>-1..7.png + caption.txt) once. Skips it when a post with the same first
caption line is already on the account. Usage: python3 -I promo/post_pin.py <key> <raw base url of promo/<key>>"""
import glob, os, sys, time, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit'))
import publish as P

key, base = sys.argv[1], sys.argv[2].rstrip('/')
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), key)
cap = open(f'{d}/caption.txt').read().strip(); head = cap.splitlines()[0]


def on_account():
    return next((m for m in P.recent(30) if (m.get('caption') or '').startswith(head)), None)


if on_account(): sys.exit(f'already on account: {on_account()["permalink"]}')
files = sorted(glob.glob(f'{d}/{key}-*.png'))
for f in files:
    u = f'{base}/{os.path.basename(f)}'
    for _ in range(40):
        try:
            if urllib.request.urlopen(urllib.request.Request(u, method='HEAD'), timeout=60).status == 200: break
        except Exception: pass
        time.sleep(15)
kids = [P.call('/me/media', {'image_url': f'{base}/{os.path.basename(f)}', 'is_carousel_item': 'true'})['id'] for f in files]
for k in kids: P.wait(k)
cid = P.call('/me/media', {'media_type': 'CAROUSEL', 'children': ','.join(kids), 'caption': cap})['id']; P.wait(cid)
try: P.call('/me/media_publish', {'creation_id': cid})
except RuntimeError as e: print('publish said:', str(e)[:120])   # "action is blocked" can still publish: check below
for _ in range(10):
    m = on_account()
    if m: print('posted', m['permalink']); break
    time.sleep(10)
else: sys.exit('not visible on account')
