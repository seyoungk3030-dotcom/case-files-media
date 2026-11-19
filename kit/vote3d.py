"""Build a short vote reel (1080x1920, ~15 s): challenge hook + ONE question + three options A/B/C + countdown, and a
call to comment one letter. No answer in the reel: the answer goes out as replies to letter comments.
Episode dir needs vote.json:
 {"room": 193, "sprite": "<abs png>", "hook": "대부분 틀려요", "question": ["line 1", "line 2"], "caption": ["under sprite", ...],
  "options": {"A": "9.2kg", "B": "8kg", "C": "5kg"}, "answer": "C", "count": 5,
  "narration": {"hook": "..."}, optional "bg_video": "<abs mp4>"}
Narration: Qwen3-TTS <ep>/.build-vote/hook.wav (+hook.txt) if it matches, else edge-tts.
Usage: python3 vote3d.py <abs episode_dir>"""
import asyncio, json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import style as S
import reel as R
from style3d import ease_out_back, ease, background, text_layer, pill, put, trim, panel
from short3d import sfx
import edge_tts

W, H, FPS = 1080, 1920, 30
OPT_COL = {'A': (255, 120, 120), 'B': (120, 190, 255), 'C': (255, 206, 92)}


def build(ep):
    v = json.load(open(f'{ep}/vote.json')); T = f'{ep}/.build-vote'; os.makedirs(T, exist_ok=True)
    q = f'{T}/hook.txt'
    if os.path.exists(q) and open(q).read() == v['narration']['hook'] and os.path.exists(f'{T}/hook.wav'):
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{T}/hook.wav', '-af', 'atempo=1.1', '-ar', str(R.SR), '-ac', '1', f'{T}/hook-v.wav'], check=True)
    else:
        print('edge-tts for hook')
        asyncio.run(edge_tts.Communicate(v['narration']['hook'], R.VOICE, rate='+14%').save(f'{T}/hook.mp3'))
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{T}/hook.mp3', '-ar', str(R.SR), '-ac', '1', f'{T}/hook-v.wav'], check=True)
    nd = R.dur(f'{T}/hook-v.wav'); COUNT = v.get('count', 5)
    t_count = nd + 0.3; t_end = t_count + COUNT; total = t_end + 2.6

    bg, bok = background(v['room'])
    vid = None
    if v.get('bg_video'):
        vid = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-stream_loop', '-1', '-i', v['bg_video'], '-vf',
            f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=10,eq=brightness=-0.1:saturation=0.85,fps={FPS}',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    spr = trim(Image.open(v['sprite']).convert('RGBA')); sw = v.get('sprite_w', 900)
    spr = spr.resize((sw, round(spr.height * sw / spr.width)), Image.LANCZOS)
    hook = text_layer(v['hook'], 104, S.YEL, glow=S.YEL)
    ques = [text_layer(s, 62, S.WHITE) for s in v['question']]
    caps = [text_layer(s, 48, (215, 225, 238), 'Bold') for s in v.get('caption', [])]
    opts = []
    for k, s in v['options'].items():
        lay = Image.new('RGBA', (300, 170), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle([4, 8, 296, 166], 34, fill=(0, 0, 0, 90)); d.rounded_rectangle([0, 0, 292, 158], 34, fill=(22, 34, 54, 235), outline=(*OPT_COL[k], 255), width=6)
        lay.alpha_composite(text_layer(k, 64, OPT_COL[k], shadow=False), (14, -14))
        t2 = text_layer(s, 54, S.WHITE, shadow=False); lay.alpha_composite(t2, (int(176 - t2.width / 2 + 10), 20))
        opts.append(lay)
    cta1 = text_layer('댓글에 A · B · C 하나만!', 70, S.MINT, glow=S.MINT)
    end = [text_layer('정답은 댓글로 알려드려요', 66, S.YEL, glow=S.YEL), text_layer('팔로우하면 매일 새 문제', 52, S.WHITE, 'Bold')]
    nums = {n: text_layer(str(n), 120, S.WHITE) for n in range(COUNT + 1)}
    brand = pill(v.get('brand') or f'퇴근 후 사건파일 · ROOM {v["room"]:03d}', 30, (200, 212, 226), (16, 28, 44, 200))
    SY = 560 + spr.height / 2 * 0  # sprite centre
    SY = 330 + 60 + spr.height / 2 + 120

    voice = np.zeros(int(total * R.SR) + R.SR)
    with wave.open(f'{T}/hook-v.wav') as w: sig = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16) / 32768
    voice[int(0.15 * R.SR):int(0.15 * R.SR) + len(sig)] += sig
    def add(s, at): s0 = int(at * R.SR); voice[s0:s0 + len(s)] += s[:max(0, len(voice) - s0)]
    add(sfx(0.3, 'thud'), 0.35)
    for i in range(3): add(sfx(0.25, 'pop'), 1.2 + 0.25 * i)
    L = int(0.04 * R.SR); tone = 0.25 * np.sin(2 * np.pi * 1800 * np.arange(L) / R.SR) * np.exp(-np.arange(L) / (0.008 * R.SR))
    for n in range(COUNT): add(tone * (1.6 if COUNT - n <= 3 else 1), t_count + n)
    add(sfx(1.6, 'chime'), t_end)
    music = R.bgm(len(voice) / R.SR, v['room']); music = np.pad(music, (0, max(0, len(voice) - len(music))))[:len(voice)]
    duck = np.full_like(voice, 0.45); duck[int(t_count * R.SR):] = 1.0
    mix = (voice + music * 0.16 * duck)[:int(total * R.SR)]
    f = int(0.8 * R.SR); mix[-f:] *= np.linspace(1, 0, f); mix = np.clip(mix / max(1, np.abs(mix).max() / 0.9), -1, 1)
    with wave.open(f'{T}/mix.wav', 'w') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(R.SR); w.writeframes((np.repeat(mix[:, None], 2, axis=1) * 32767).astype(np.int16).tobytes())

    ff = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-i', f'{T}/mix.wav', '-vf', 'format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-profile:v', 'high',
                           '-c:a', 'aac', '-b:a', '160k', '-ar', str(R.SR), '-t', f'{total:.3f}', '-movflags', '+faststart', f'{ep}/vote.mp4'], stdin=subprocess.PIPE)
    vf, vi = None, -1; qa = {'hook': 1.0, 'question': nd * 0.8, 'count': t_count + 2.5, 'end': total - 0.5}
    for i in range(int(total * FPS) + 1):
        t = i / FPS; fr = bg.copy()
        if vid:
            while vi < i or vf is None:
                raw = vid.stdout.read(W * H * 3)
                if len(raw) < W * H * 3: break
                vf = Image.frombuffer('RGB', (W, H), raw).convert('RGBA'); vi += 1
            if vf: fr = Image.blend(bg, vf, 0.5)
        off = int(t * 22) % H; fr.alpha_composite(bok.crop((0, off, W, off + H)))
        put(fr, brand, W / 2, 80)
        k = ease_out_back(t / 0.4); shake = 6 * math.sin(t * 40) * max(0, 1 - t / 0.6)
        put(fr, hook, W / 2 + shake, 200, k)
        for j, lay in enumerate(ques): put(fr, lay, W / 2, 320 + j * 80, ease_out_back((t - 0.3 - j * 0.15) / 0.4), min(1, max(0, (t - 0.3) * 4)))
        ks = ease_out_back((t - 0.35) / 0.55)
        put(fr, spr, W / 2, SY - 120 * (1 - ks) + 5 * math.sin(t * 1.8), 1, min(1, max(0, (t - 0.35) * 3)))
        cy = SY + spr.height / 2 + 40
        for j, lay in enumerate(caps): put(fr, lay, W / 2, cy + j * 64, 1, min(1, max(0, (t - 0.8) * 3)))
        oy = 1540
        for j, lay in enumerate(opts):
            st = 1.2 + 0.25 * j; pulse = 1 + (0.05 * math.sin((t - t_count) * 6 + j) if t_count <= t < t_end else 0)
            put(fr, lay, W / 2 + (j - 1) * 330, oy, ease_out_back((t - st) / 0.4) * pulse)
        if t < t_end:
            put(fr, cta1, W / 2, 1725, 1, min(1, max(0, (t - 1.9) * 3)))
            if t >= t_count:
                pt = t - t_count; left = COUNT - pt; r = 62; cx, cyy = W - 120, 205
                d = ImageDraw.Draw(fr); d.ellipse([cx - r, cyy - r, cx + r, cyy + r], fill=(16, 28, 44, 200), outline=(255, 255, 255, 50), width=10)
                d.arc([cx - r, cyy - r, cx + r, cyy + r], -90, -90 + 360 * max(0, left / COUNT), fill=S.MINT if left > 2 else S.CORAL, width=10)
                put(fr, nums[max(0, math.ceil(left - 1e-6))], cx, cyy, 0.62 * (1 + 0.18 * (1 - ease((pt % 1) / 0.25))))
        else:
            ke = ease_out_back((t - t_end) / 0.45)
            put(fr, end[0], W / 2, 1715, ke); put(fr, end[1], W / 2, 1810, ke)
        out = fr.convert('RGB'); ff.stdin.write(out.tobytes())
        for nm, at in qa.items():
            if abs(t - at) < 0.5 / FPS: out.save(f'{T}/qa-{nm}.png')
    ff.stdin.close(); assert ff.wait() == 0
    if vid: vid.stdout.close(); vid.kill()
    print(f'vote ok {total:.1f}s')


if __name__ == '__main__':
    build(sys.argv[1])
