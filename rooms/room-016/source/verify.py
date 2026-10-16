"""ROOM 016 proof: CCTV shows a wall clock through a mirror (left-right flip). Shown hands: hour hand at the 4:10 position,
minute hand on 2 (10 min). Find every real time (each minute of 24h) whose mirror image matches, keep the evening ones."""
import json, os
SHOWN_H, SHOWN_M = (4 + 10 / 60) * 30, 10 * 6           # degrees clockwise from 12
mirror = lambda a: (360 - a) % 360
hits = []
for t in range(24 * 60):
    h, m = divmod(t, 60)
    ah, am = ((h % 12) + m / 60) * 30, m * 6
    if abs(mirror(ah) - SHOWN_H) < 1e-6 and abs(mirror(am) - SHOWN_M) < 1e-6:
        hits.append(f'{h:02d}{m:02d}')
evening = [x for x in hits if 18 <= int(x[:2]) <= 23]
print(hits, evening)
assert hits == ['0750', '1950'] and evening == ['1950']
json.dump({'unique_answer': evening[0], 'tested_times': 1440, 'mirror_matches_any_time': hits,
           'traps': {'read_without_mirror': '0410', 'forgot_evening': '0750'},
           'rules': 'mirror flips left-right; code = real time in 24h HHMM; incident is in the evening after work (18-23h)'},
          open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
