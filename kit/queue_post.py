"""Post queued rooms without Claude (run by .github/workflows/queued-post.yml, also safe to run by hand).

A room is queued when its ledger entry has "status": "QUEUED" and "post_at" (UTC ISO time, e.g. 2026-11-07T02:30:00Z),
and its cards, reel and captions are already committed. Each run posts at most ONE queued room whose post_at has
passed (the earliest), then shares the reel as a story. publish.py skips anything already on the account, so a room
is never posted twice. Needs env IG_ACCESS_TOKEN (never printed) and GITHUB_SHA (or a SHA as argv[1]) for media URLs."""
import json, os, subprocess, sys
from datetime import datetime, timezone
KIT = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(KIT)
sys.path.insert(0, KIT)
import publish

L = json.load(open(f'{KIT}/ledger.json'))
now = datetime.now(timezone.utc)
due = sorted((e for e in L['episodes'] if e.get('status') == 'QUEUED'
              and datetime.fromisoformat(e['post_at'].replace('Z', '+00:00')) <= now), key=lambda e: e['post_at'])
if not due:
    sys.exit(print('nothing due'))
e = due[0]; room = e['room']
sha = sys.argv[1] if len(sys.argv) > 1 else os.environ['GITHUB_SHA']
base = f'https://raw.githubusercontent.com/seyoungk3030-dotcom/case-files-media/{sha}/rooms/room-{room:03d}'
print('posting ROOM', room)
publish.main(f'{ROOT}/rooms/room-{room:03d}', base, base)
subprocess.run([sys.executable, '-I', f'{KIT}/story.py', str(room), base], check=False)
