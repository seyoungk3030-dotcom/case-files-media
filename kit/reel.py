"""Build reel.mp4 (1080x1920, h264/aac 48k) from an episode folder.

Episode folder must contain cards/card-NN.png and episode.json:
{"room": 12, "title": "...", "date": "2026.10.15",
 "solve_after": 4, "solve_seconds": 20,
 "scenes": [{"card": 1, "narration": "...(numbers spelled in Korean words)", "subtitle": "..."}, ...]}
Usage: python3 reel.py <episode_dir>
"""
import asyncio, json, os, ssl, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw
import edge_tts
import edge_tts.communicate as _ec
if os.path.exists('/root/.ccr/ca-bundle.crt'):
    _ec._SSL_CTX = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import style as S

VOICE, RATE, FPS, SR = 'ko-KR-SunHiNeural', '+8%', 30, 48000


def wrap(d, s, font, width):
    out, cur = [], ''
    for word in s.split(' '):
        t = (cur + ' ' + word).strip()
        if d.textlength(t, font=font) <= width: cur = t
        else: out.append(cur); cur = word
    out.append(cur); return out


def frame(ep_dir, room, card, sub=None, count=None):
    im = Image.new('RGB', (1080, 1920), S.BG); d = ImageDraw.Draw(im)
    d.text((80, 84), f'ROOM {room:03d}  ·  퇴근 후 사건파일', font=S.F('SemiBold', 34), fill=S.GRAY)
    d.rectangle([80, 172, 1000, 182], fill=S.MINT)
    c = Image.open(f'{ep_dir}/cards/card-{card:02d}.png').convert('RGB').crop((0, 12, 1080, 1350)).resize((920, 1140))
    im.paste(c, (80, 190))
    d.rounded_rectangle([60, 1360, 1020, 1760], radius=24, fill=S.PANEL)
    if count is not None:
        S.ctext(d, 1400, '당신의 암호는?', col=S.WHITE, font=S.F('Bold', 52))
        S.ctext(d, 1480, str(count), col=S.MINT, font=S.F('Black', 130))
        S.ctext(d, 1670, '다음 장면부터 힌트 → 정답', col=S.GRAY, font=S.F('SemiBold', 36))
    else:
        f = S.F('Bold', 48); ls = wrap(d, sub, f, 880)
        assert len(ls) <= 4, f'subtitle too long for card {card}: {sub}'
        for i, l in enumerate(ls): d.text((100, 1400 + i * 76), l, font=f, fill=S.WHITE)
    S.ctext(d, 1800, '더 생각하고 싶으면 잠깐 멈춰도 좋아요', col=S.GRAY, font=S.F('SemiBold', 34))
    return im


def bgm(total, seed):
    rng = np.random.default_rng(seed)
    t = np.arange(int(total * SR)) / SR
    roots = [[220, 261.6, 329.6], [174.6, 220, 261.6], [261.6, 329.6, 392], [196, 246.9, 293.7],
             [146.8, 174.6, 220], [164.8, 196, 246.9]]
    prog = [roots[i] for i in rng.permutation(len(roots))[:4]]
    out = np.zeros_like(t); seg = 4.0
    for k in range(int(total / seg) + 1):
        a, b = int(k * seg * SR), min(int((k + 1) * seg * SR), len(t))
        if a >= len(t): break
        tt = t[a:b] - k * seg
        env = np.minimum(1, tt / 0.8) * np.minimum(1, (seg - tt) / 0.8)
        for f in prog[k % 4]:
            out[a:b] += env * (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.003 * tt)) / 6
        out[a:b] += env * 0.35 * np.sin(2 * np.pi * prog[k % 4][0] / 2 * tt)
    return out


def dur(p):
    with wave.open(p) as w: return w.getnframes() / w.getframerate()


def build(ep_dir):
    ep = json.load(open(f'{ep_dir}/episode.json'))
    room, scenes = ep['room'], ep['scenes']
    solve_after, SOLVE = ep.get('solve_after', 4), ep.get('solve_seconds', 20)
    T = f'{ep_dir}/.build'; os.makedirs(T, exist_ok=True)

    async def tts():
        for i, s in enumerate(scenes):
            await edge_tts.Communicate(s['narration'], VOICE, rate=RATE).save(f'{T}/n{i}.mp3')
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{T}/n{i}.mp3', '-ar', str(SR), '-ac', '1', f'{T}/n{i}.wav'], check=True)
    asyncio.run(tts())

    segs, t0 = [], 0.0
    for i, s in enumerate(scenes):
        dd = dur(f'{T}/n{i}.wav') + 1.0
        segs.append({'scene': i + 1, 'card': s['card'], 'start': round(t0, 3), 'end': round(t0 + dd, 3), 'narration': s['narration']}); t0 += dd
        if s['card'] == solve_after:
            segs.append({'scene': 'solve', 'card': solve_after, 'start': round(t0, 3), 'end': round(t0 + SOLVE, 3)}); t0 += SOLVE
    total = t0
    lst = []
    for s in segs:
        if s['scene'] == 'solve':
            for n in range(SOLVE, 0, -1):
                p = f'{T}/count-{n:02d}.png'; frame(ep_dir, room, s['card'], count=n).save(p); lst.append((p, 1.0))
        else:
            p = f'{T}/scene-{s["scene"]:02d}.png'
            frame(ep_dir, room, s['card'], scenes[s['scene'] - 1]['subtitle']).save(p); lst.append((p, s['end'] - s['start']))
    with open(f'{T}/list.txt', 'w') as f:
        for p, du in lst: f.write(f"file '{p}'\nduration {du:.3f}\n")
        f.write(f"file '{lst[-1][0]}'\n")

    voice = np.zeros(int(total * SR) + SR)
    for s in segs:
        if s['scene'] == 'solve': continue
        with wave.open(f'{T}/n{s["scene"] - 1}.wav') as w:
            a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16) / 32768
        st = int((s['start'] + 0.35) * SR); voice[st:st + len(a)] += a
    music = bgm(len(voice) / SR, room)
    duck = np.ones_like(voice)
    for s in segs:
        if s['scene'] != 'solve': duck[int(s['start'] * SR):int(s['end'] * SR)] = 0.45
    tick = np.zeros_like(voice)
    sv = [s for s in segs if s['scene'] == 'solve'][0]
    L = int(0.04 * SR); env = np.exp(-np.arange(L) / (0.008 * SR)); tone = 0.25 * np.sin(2 * np.pi * 1800 * np.arange(L) / SR) * env
    for n in range(SOLVE):
        st = int((sv['start'] + n) * SR); tick[st:st + L] += tone
    mix = (voice + music * 0.16 * duck + tick)[:int(total * SR)]
    fade = int(1.5 * SR); mix[-fade:] *= np.linspace(1, 0, fade)
    mix = np.clip(mix / max(1, np.abs(mix).max() / 0.9), -1, 1)
    with wave.open(f'{T}/mix.wav', 'w') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.repeat(mix[:, None], 2, axis=1) * 32767).astype(np.int16).tobytes())
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{T}/list.txt', '-i', f'{T}/mix.wav',
                    '-vf', f'fps={FPS},format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-profile:v', 'high',
                    '-c:a', 'aac', '-b:a', '160k', '-ar', str(SR), '-t', f'{total:.3f}', '-movflags', '+faststart', f'{ep_dir}/reel.mp4'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{ep_dir}/reel.mp4', '-f', 'null', '-'], check=True)
    json.dump({'duration_seconds': total, 'fps': FPS, 'voice': VOICE, 'segments': segs},
              open(f'{ep_dir}/notes/timeline.json', 'w'), ensure_ascii=False, indent=1)
    # QA stills for visual review
    for s in segs:
        if s['scene'] in (1, 'solve') or s['scene'] == len(scenes):
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{(s["start"] + s["end"]) / 2:.2f}', '-i', f'{ep_dir}/reel.mp4',
                            '-frames:v', '1', f'{T}/qa-{s["scene"]}.png'], check=True)
    print(f'reel ok {total:.1f}s')


if __name__ == '__main__':
    build(sys.argv[1])
