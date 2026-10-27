"""Pick and fetch a Mixkit stock clip (free licence, no credit needed) for a room's backgrounds.
Clips rotate by room number. Writes <ep>/.build-short/bg.mp4 (720p, for short3d.json "bg_video") and bg.jpg (a still
for the cards: run render.py with CARD_BG=<ep>/.build-short/bg.jpg). The clips are never committed (the repo is public).
Usage: python3 stock.py <absolute episode_dir>"""
import json, os, subprocess, sys, urllib.request
# vertical night/commute clips without faces, chosen 2026-10-27
CLIPS = [40654, 34562, 1594, 40746, 41865, 40671, 49878, 39854, 42048]


def fetch(ep):
    room = json.load(open(f'{ep}/short3d.json'))['room']
    cid = CLIPS[room % len(CLIPS)]
    out = f'{ep}/.build-short'; os.makedirs(out, exist_ok=True)
    if not os.path.exists(f'{out}/bg.mp4'):
        urllib.request.urlretrieve(f'https://assets.mixkit.co/videos/{cid}/{cid}-720.mp4', f'{out}/bg.mp4')
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-ss', '2', '-i', f'{out}/bg.mp4', '-frames:v', '1',
                    f'{out}/bg.jpg'], check=True)
    print('stock clip', cid)
    return cid


if __name__ == '__main__':
    fetch(sys.argv[1])
