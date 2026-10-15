"""Publish one episode (carousel + reel) to @case_files_after_work via the Instagram API.

Usage: python3 publish.py <episode_dir> <public_base_url>
  public_base_url must serve <base>/cards/card-NN.png and <base>/reel.mp4 publicly.
Needs env IG_ACCESS_TOKEN. Never prints the token.
Safe to re-run: anything already on the account (matched by caption prefix "[ROOM NNN") is skipped.
Reels go to the Reels tab only (share_to_feed=false).
"""
import glob, json, os, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone

B = 'https://graph.instagram.com/v21.0'
T = os.environ['IG_ACCESS_TOKEN']
KIT = os.path.dirname(os.path.abspath(__file__))


def call(path, params=None, method='POST'):
    p = dict(params or {}); p['access_token'] = T
    q = urllib.parse.urlencode(p)
    req = urllib.request.Request(B + path + ('' if method == 'POST' else '?' + q),
                                 data=q.encode() if method == 'POST' else None, method=method)
    try:
        return json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        raise RuntimeError(e.read().decode()) from None


def recent(limit=25):
    return call('/me/media', {'fields': 'id,caption,media_type,media_product_type,permalink,timestamp', 'limit': limit}, 'GET')['data']


def find(room, kind):
    tag = f'[ROOM {room:03d}'
    for m in recent():
        if (m.get('caption') or '').startswith(tag):
            if kind == 'carousel' and m['media_type'] == 'CAROUSEL_ALBUM': return m
            if kind == 'reel' and m['media_type'] == 'VIDEO': return m
    return None


def wait(cid, tries=90):
    for _ in range(tries):
        s = call('/' + cid, {'fields': 'status_code,status'}, 'GET')
        if s.get('status_code') == 'FINISHED': return
        if s.get('status_code') in ('ERROR', 'EXPIRED'): raise RuntimeError(f'container {cid}: {s}')
        time.sleep(5)
    raise RuntimeError(f'container {cid} timeout')


def publish(room, kind, cid):
    try:
        call('/me/media_publish', {'creation_id': cid})
    except RuntimeError as e:
        # Instagram sometimes returns 2207051 "action is blocked" yet publishes anyway.
        time.sleep(10)
        m = find(room, kind)
        if m: return m
        raise
    for _ in range(6):
        m = find(room, kind)
        if m: return m
        time.sleep(5)
    raise RuntimeError(f'{kind} published but not visible yet')


def main(ep_dir, base):
    ep = json.load(open(f'{ep_dir}/episode.json')); room = ep['room']
    cards = sorted(glob.glob(f'{ep_dir}/cards/card-*.png'))
    cap_c = open(f'{ep_dir}/notes/caption-carousel.txt').read().strip()
    cap_r = open(f'{ep_dir}/notes/caption-reel.txt').read().strip()
    assert cap_c.startswith(f'[ROOM {room:03d}') and cap_r.startswith(f'[ROOM {room:03d}')
    rec = {}
    m = find(room, 'carousel')
    if not m:
        kids = [call('/me/media', {'image_url': f'{base}/cards/{os.path.basename(c)}', 'is_carousel_item': 'true'})['id'] for c in cards]
        for k in kids: wait(k)
        cid = call('/me/media', {'media_type': 'CAROUSEL', 'children': ','.join(kids), 'caption': cap_c})['id']
        wait(cid); m = publish(room, 'carousel', cid)
    else:
        print('carousel already on account, skipped')
    rec['carousel'] = m
    m = find(room, 'reel')
    if not m:
        # Instagram's video fetch from the CDN sometimes fails transiently (HTTP 500); retry a fresh container.
        for attempt in range(3):
            cid = call('/me/media', {'media_type': 'REELS', 'video_url': f'{base}/reel.mp4', 'caption': cap_r, 'share_to_feed': 'false'})['id']
            try:
                wait(cid); break
            except RuntimeError as e:
                print('reel container failed, retrying:', call('/' + cid, {'fields': 'error_message'}, 'GET').get('error_message'))
                if attempt == 2: raise
                time.sleep(60)
        m = publish(room, 'reel', cid)
    else:
        print('reel already on account, skipped')
    rec['reel'] = m
    rec['verified_at'] = datetime.now(timezone.utc).isoformat()
    json.dump(rec, open(f'{ep_dir}/notes/publication-record.json', 'w'), ensure_ascii=False, indent=1)
    lp = f'{KIT}/ledger.json'; L = json.load(open(lp))
    for e in L['episodes']:
        if e['room'] == room:
            e.update(status='PUBLISHED', carousel_url=rec['carousel']['permalink'], reel_url=rec['reel']['permalink'], published_at=rec['verified_at'])
    json.dump(L, open(lp, 'w'), ensure_ascii=False, indent=1)
    print('carousel', rec['carousel']['permalink']); print('reel', rec['reel']['permalink'])


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2].rstrip('/'))
