"""Print the next free GitHub posting slot (UTC ISO) after the last QUEUED room, or FULL."""
import json, os
from datetime import datetime, timedelta, timezone
KIT = os.path.dirname(os.path.abspath(__file__))
SLOTS = ((2, 30), (8, 30), (11, 30))  # 11:30, 17:30, 20:30 KST
END = datetime(2026, 12, 31, 15, 0, tzinfo=timezone.utc)  # end of 2026-12-31 KST
now = datetime.now(timezone.utc)
L = json.load(open(f'{KIT}/ledger.json'))
q = [datetime.fromisoformat(e['post_at'].replace('Z', '+00:00')) for e in L['episodes'] if e.get('status') == 'QUEUED']
after = max(q + [now])
d = after.replace(hour=0, minute=0, second=0, microsecond=0)
while True:
    cand = [d.replace(hour=h, minute=m) for h, m in SLOTS if d.replace(hour=h, minute=m) > after]
    if cand: slot = cand[0]; break
    d += timedelta(days=1)
print('FULL' if slot > END or slot > now + timedelta(days=30) else slot.strftime('%Y-%m-%dT%H:%M:%SZ'))
