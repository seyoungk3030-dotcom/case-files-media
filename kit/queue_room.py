"""Queue a finished room for GitHub Actions: ledger entry (QUEUED at the next free slot, date = slot in KST), RUNBOOK
backlog tick, build-dir cleanup, commit 'ROOM NNN' and push. Usage: queue_room.py NNN '<title>' <mechanic> <answer> '<backlog name>'"""
import json, os, shutil, subprocess, sys
from datetime import datetime, timedelta
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); KIT = f'{ROOT}/kit'
room, title, mech, ans, tick = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
slot = subprocess.run([sys.executable, '-I', f'{KIT}/next_slot.py'], capture_output=True, text=True, check=True).stdout.strip()
assert slot != 'FULL', 'queue is full'
proof = json.load(open(f'{ROOT}/rooms/room-{room:03d}/notes/proof.json')); assert proof['unique_answer'] == ans
L = json.load(open(f'{KIT}/ledger.json')); assert all(e['room'] != room for e in L['episodes']), 'room already in ledger'
assert max(e['room'] for e in L['episodes']) == room - 1
kst = datetime.strptime(slot, '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=9)
L['episodes'].append({'room': room, 'title': title, 'mechanic': mech, 'answer': ans, 'date': kst.strftime('%Y.%m.%d'), 'status': 'QUEUED', 'post_at': slot})
json.dump(L, open(f'{KIT}/ledger.json', 'w'), ensure_ascii=False, indent=1)
rb = open(f'{KIT}/RUNBOOK.md').read(); i = rb.find(tick)
if i >= 0:
    j = rb.find(')', i) + 1; rb = rb[:j] + f' [{room:03d}]' + rb[j:]; open(f'{KIT}/RUNBOOK.md', 'w').write(rb)
for d in ('.build-3d', '.build-short', '.build', 'source/__pycache__'): shutil.rmtree(f'{ROOT}/rooms/room-{room:03d}/{d}', ignore_errors=True)
g = ['git', '-C', ROOT, '-c', 'user.name=Claude', '-c', 'user.email=noreply@anthropic.com']
subprocess.run(g + ['add', '-A'], check=True)
msg = f'ROOM {room:03d} (queued {slot})\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01US1BUi8V1ubC666r5Bk4fZ'
subprocess.run(g + ['commit', '-qm', msg], check=True)
for n in range(4):
    if subprocess.run(['git', '-C', ROOT, 'pull', '-q', '--rebase', 'origin', 'main']).returncode == 0 and \
       subprocess.run(['git', '-C', ROOT, 'push', '-q', 'origin', 'main']).returncode == 0: break
else: sys.exit('push failed')
print('queued', room, title, ans, slot, kst.strftime('%m/%d %H:%M KST'))
