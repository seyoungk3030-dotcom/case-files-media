"""Share a room's reel as an Instagram story (the story disappears after 24 h; stickers can't be added via the API).
Usage: python3 -I kit/story.py <room number> <video_base_url>   (same base URL as publish.py; skipped if the ledger
already has a story_id for that room)."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from publish import call
KIT = os.path.dirname(os.path.abspath(__file__))
room, base = int(sys.argv[1]), sys.argv[2]
L = json.load(open(f'{KIT}/ledger.json')); ep = next(e for e in L['episodes'] if e['room'] == room)
if ep.get('story_id'): sys.exit(print('story already posted', ep['story_id']))
c = call('/me/media', {'media_type': 'STORIES', 'video_url': f'{base}/reel.mp4'})['id']
for _ in range(90):
    s = call(f'/{c}', {'fields': 'status_code'}, 'GET')['status_code']
    if s != 'IN_PROGRESS': break
    time.sleep(5)
assert s == 'FINISHED', s
ep['story_id'] = call('/me/media_publish', {'creation_id': c})['id']
with open(f'{KIT}/ledger.json', 'w') as f: json.dump(L, f, ensure_ascii=False, indent=1); f.write('\n')
print('story', ep['story_id'])
