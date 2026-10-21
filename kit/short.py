"""Build short.mp4 (1080x1920, ~25s) — a fast-hook reel. The puzzle and the question are on screen from frame one,
then a one-line rule, a countdown, the answer and a comment prompt.

Episode folder needs cards/card-NN.png and short.json:
{"hook": ["line 1", "line 2"], "puzzle": {"card": 4, "crop": [x0, y0, x1, y1]}, "rule": "one line",
 "answer": "1325", "answer_img": {"card": 7, "crop": [...]}, "count": 10, "cta": "one line",
 "narration": {"hook": "...", "rule": "...", "answer": "...", "cta": "..."}}   (numbers in narration as Korean words)
Usage: python3 short.py <absolute episode_dir>
"""
import asyncio, json, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import style as S
import reel as R
import edge_tts


def crop(ep_dir, spec, width=1000):
    im = Image.open(f'{ep_dir}/cards/card-{spec["card"]:02d}.png').convert('RGB').crop(tuple(spec['crop']))
    return im.resize((width, round(im.height * width / im.width)))


def frame(ep_dir, sh, room, phase, n=None):
    im = Image.new('RGB', (1080, 1920), S.BG); d = ImageDraw.Draw(im)
    d.text((70, 70), f'퇴근 후 사건파일  ·  ROOM {room:03d}', font=S.F('SemiBold', 34), fill=S.GRAY)
    f = S.F('Black', 76)
    for i, l in enumerate(sh['hook']):
        S.ctext(d, 160 + i * 100, l, col=S.YEL if i == len(sh['hook']) - 1 else S.WHITE, font=f)
    top = 190 + len(sh['hook']) * 100
    if phase in ('answer', 'cta'): top += 180
    img = crop(ep_dir, sh['answer_img'] if phase in ('answer', 'cta') else sh['puzzle'])
    im.paste(img, (40, top)); y = top + img.height + 50
    if phase in ('hook', 'rule'):
        f = S.F('Bold', 50); ls = R.wrap(d, sh['rule'], f, 940) if sh['rule'] else []
        for i, l in enumerate(ls): S.ctext(d, y + i * 72, l, col=S.WHITE, font=f)
    elif phase == 'count':
        total = sh['count']
        S.ctext(d, y, str(n), col=S.MINT, font=S.F('Black', 180))
        bw = 900 * n / total
        d.rounded_rectangle([90, y + 240, 990, y + 268], radius=14, fill=S.PANEL)
        d.rounded_rectangle([90, y + 240, 90 + bw, y + 268], radius=14, fill=S.MINT)
        S.ctext(d, y + 300, '댓글에 암호를 먼저 남겨보세요', col=S.GRAY, font=S.F('Bold', 42))
    elif phase == 'answer':
        S.ctext(d, y + 40, '정답', col=S.GRAY, font=S.F('Bold', 48))
        S.ctext(d, y + 110, ' '.join(sh['answer']), col=S.MINT, font=S.F('Black', 170))
    elif phase == 'cta':
        S.ctext(d, y + 40, '정답', col=S.GRAY, font=S.F('Bold', 48))
        S.ctext(d, y + 110, ' '.join(sh['answer']), col=S.MINT, font=S.F('Black', 150))
        f = S.F('Bold', 52); ls = R.wrap(d, sh['cta'], f, 900)
        for i, l in enumerate(ls): S.ctext(d, y + 340 + i * 76, l, col=S.YEL if i == 0 else S.WHITE, font=f)
    return im


def build(ep_dir):
    ep = json.load(open(f'{ep_dir}/episode.json')); sh = json.load(open(f'{ep_dir}/short.json'))
    room, COUNT = ep['room'], sh.get('count', 10)
    T = f'{ep_dir}/.build-short'; os.makedirs(T, exist_ok=True)
    keys = ['hook', 'rule', 'answer', 'cta']

    async def tts():
        for k in keys:
            await edge_tts.Communicate(sh['narration'][k], R.VOICE, rate='+12%').save(f'{T}/{k}.mp3')
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{T}/{k}.mp3', '-ar', str(R.SR), '-ac', '1', f'{T}/{k}.wav'], check=True)
    asyncio.run(tts())

    segs, t0 = [], 0.0
    for k in keys:
        dd = R.dur(f'{T}/{k}.wav') + 0.4
        segs.append((k, t0, dd)); t0 += dd
        if k == 'rule': segs.append(('count', t0, COUNT)); t0 += COUNT
    total = t0
    lst = []
    for k, st, dd in segs:
        if k == 'count':
            for n in range(COUNT, 0, -1):
                p = f'{T}/count-{n:02d}.png'; frame(ep_dir, sh, room, 'count', n).save(p); lst.append((p, 1.0))
        else:
            p = f'{T}/{k}.png'; frame(ep_dir, sh, room, k).save(p); lst.append((p, dd))
    with open(f'{T}/list.txt', 'w') as f:
        for p, du in lst: f.write(f"file '{p}'\nduration {du:.3f}\n")
        f.write(f"file '{lst[-1][0]}'\n")

    voice = np.zeros(int(total * R.SR) + R.SR)
    for k, st, dd in segs:
        if k == 'count': continue
        with wave.open(f'{T}/{k}.wav') as w:
            a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16) / 32768
        s0 = int((st + 0.05) * R.SR); voice[s0:s0 + len(a)] += a
    music = R.bgm(len(voice) / R.SR, room)
    music = np.pad(music, (0, max(0, len(voice) - len(music))))[:len(voice)]
    duck = np.full_like(voice, 0.45)
    tick = np.zeros_like(voice)
    L = int(0.04 * R.SR); env = np.exp(-np.arange(L) / (0.008 * R.SR)); tone = 0.25 * np.sin(2 * np.pi * 1800 * np.arange(L) / R.SR) * env
    for k, st, dd in segs:
        if k == 'count':
            duck[int(st * R.SR):int((st + dd) * R.SR)] = 1.0
            for n in range(COUNT): s0 = int((st + n) * R.SR); tick[s0:s0 + L] += tone
    mix = (voice + music * 0.16 * duck + tick)[:int(total * R.SR)]
    fade = int(1.0 * R.SR); mix[-fade:] *= np.linspace(1, 0, fade)
    mix = np.clip(mix / max(1, np.abs(mix).max() / 0.9), -1, 1)
    with wave.open(f'{T}/mix.wav', 'w') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(R.SR)
        w.writeframes((np.repeat(mix[:, None], 2, axis=1) * 32767).astype(np.int16).tobytes())
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{T}/list.txt', '-i', f'{T}/mix.wav',
                    '-vf', f'fps={R.FPS},format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-profile:v', 'high',
                    '-c:a', 'aac', '-b:a', '160k', '-ar', str(R.SR), '-t', f'{total:.3f}', '-movflags', '+faststart', f'{ep_dir}/short.mp4'], check=True)
    for k, st, dd in segs:
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{st + dd / 2:.2f}', '-i', f'{ep_dir}/short.mp4',
                        '-frames:v', '1', f'{T}/qa-{k}.png'], check=True)
    print(f'short ok {total:.1f}s')


if __name__ == '__main__':
    build(sys.argv[1])
