"""Build short.mp4 (1080x1920, ~30s): an animated fast-hook reel over 3D sprites rendered by kit/b3d.py.

Episode folder needs .build-3d/<name>.png (+ <name>.json shape positions from b3d.project), icon-<k>.png, and short3d.json:
{"hook": ["line 1", "line 2"], "rule": ["line", "line"], "stack": ["scale1", ...], "stack_labels": ["저울 1", ...],
 "legend": ["c", "t", "s", "r"], "values": {"c": 1, ...}, "answer": "1325", "count": 10, "cta": "one line",
 "narration": {"hook": "...", "rule": "...", "answer": "...", "cta": "..."}}   (numbers in narration as Korean words)
The answer narration should name the legend items in order; their reveals are spaced across its first 70%.
Usage: python3 short3d.py <absolute episode_dir>
"""
import asyncio, json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import style as S
import reel as R
import edge_tts

W, H, FPS = 1080, 1920, 30
SLOT0, SLOT, SPR = 330, 318, 1.08          # first sprite top, sprite spacing, sprite scale
PANEL_Y = 1395


def ease_out_back(x):
    x = min(max(x, 0), 1); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def ease(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


def background(seed):
    y = np.linspace(0, 1, H)[:, None]; x = np.linspace(-1, 1, W)[None, :]
    top, bot = np.array([10, 18, 34]), np.array([20, 38, 62])
    img = top + (bot - top) * y[..., None]
    glow = np.exp(-((x * 0.9) ** 2 + ((y - 0.38) * 2.2) ** 2) * 2.2)[..., None] * np.array([26, 46, 60])
    vig = 1 - 0.45 * np.clip((x ** 2 + ((y - 0.5) * 1.6) ** 2) - 0.35, 0, 1)[..., None]
    bg = Image.fromarray(np.clip((img + glow) * vig, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    rng = np.random.default_rng(seed)
    bok = Image.new('RGBA', (W, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(bok)
    for _ in range(46):
        r = rng.uniform(6, 34); cx, cy = rng.uniform(0, W), rng.uniform(0, H * 2)
        col = [(109, 218, 197), (255, 196, 92), (140, 170, 255)][rng.integers(3)]
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*col, int(rng.uniform(18, 55))))
    bok = bok.filter(ImageFilter.GaussianBlur(7))
    return bg, bok


def text_layer(s, size, col, weight='Black', glow=None, shadow=True):
    f = S.F(weight, size); tmp = ImageDraw.Draw(Image.new('L', (1, 1)))
    w = int(tmp.textlength(s, font=f)) + 80; h = int(size * 1.5) + 60
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if shadow:
        sh = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((40, 36), s, font=f, fill=(0, 0, 0, 170))
        lay = Image.alpha_composite(lay, sh.filter(ImageFilter.GaussianBlur(6)))
    if glow:
        g = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(g).text((40, 30), s, font=f, fill=(*glow, 200))
        lay = Image.alpha_composite(lay, g.filter(ImageFilter.GaussianBlur(14)))
    ImageDraw.Draw(lay).text((40, 30), s, font=f, fill=col)
    return lay


def pill(s, size, fg, bg, pad=(26, 12)):
    f = S.F('Bold', size); tmp = ImageDraw.Draw(Image.new('L', (1, 1)))
    w = int(tmp.textlength(s, font=f)) + pad[0] * 2; h = int(size * 1.25) + pad[1] * 2
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=bg)
    d.text((pad[0], pad[1] - size * 0.08), s, font=f, fill=fg)
    return lay


def badge(n, r=40, col=(255, 196, 92)):
    lay = Image.new('RGBA', (r * 2 + 20, r * 2 + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse([12, 14, r * 2 + 12, r * 2 + 14], fill=(0, 0, 0, 110))
    d.ellipse([10, 10, r * 2 + 10, r * 2 + 10], fill=(*col, 255), outline=(255, 255, 255, 230), width=4)
    f = S.F('Black', int(r * 1.2)); s = str(n)
    d.text((r + 10 - d.textlength(s, font=f) / 2, r + 10 - r * 0.86), s, font=f, fill=(16, 28, 44))
    return lay


def put(fr, lay, cx, cy, scale=1.0, alpha=1.0):
    """Composite lay centred on (cx, cy) with scale and opacity."""
    if scale <= 0.01 or alpha <= 0.01: return
    if abs(scale - 1) > 0.01:
        lay = lay.resize((max(1, int(lay.width * scale)), max(1, int(lay.height * scale))), Image.BILINEAR)
    if alpha < 0.99:
        lay = lay.copy(); a = lay.getchannel('A').point(lambda v: int(v * alpha)); lay.putalpha(a)
    x, y = int(cx - lay.width / 2), int(cy - lay.height / 2)
    x0, y0 = max(0, -x), max(0, -y)
    if x0 or y0: lay = lay.crop((x0, y0, lay.width, lay.height)); x, y = x + x0, y + y0
    fr.alpha_composite(lay, (x, y))


def trim(im):
    return im.crop(im.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox())


class Scene:
    def __init__(self, ep_dir, sh, room, segs):
        B = f'{ep_dir}/.build-3d'; self.sh, self.segs = sh, segs
        self.bg, self.bok = background(room)
        self.sprites = []
        for name in sh['stack']:
            im = Image.open(f'{B}/{name}.png').convert('RGBA')
            self.sprites.append((im.resize((int(im.width * SPR), int(im.height * SPR)), Image.LANCZOS),
                                 json.load(open(f'{B}/{name}.json'))))
        self.icons = {k: trim(Image.open(f'{B}/icon-{k}.png').convert('RGBA')) for k in sh['legend']}
        self.icons = {k: v.resize((int(v.width * 150 / v.height), 150), Image.LANCZOS) for k, v in self.icons.items()}
        self.brand = pill(f'퇴근 후 사건파일  ·  ROOM {room:03d}', 30, (200, 212, 226), (255, 255, 255, 26))
        n = len(sh['hook'])
        self.hook = [text_layer(l, 70, S.YEL if i == n - 1 else S.WHITE) for i, l in enumerate(sh['hook'])]
        self.head_ans = text_layer('정답 공개', 84, S.MINT, glow=S.MINT)
        self.labels = [pill(l, 28, (16, 28, 44), (*S.MINT, 235)) for l in sh['stack_labels']]
        self.rule = [text_layer(l, 44, S.WHITE, 'Bold') for l in sh['rule']]
        self.code_lbl = text_layer('암호 =', 44, S.YEL, 'Bold')
        self.qmark = badge('?', 34, (160, 172, 188))
        self.badges = {k: badge(v) for k, v in sh['values'].items()}
        self.code = text_layer(' '.join(sh['answer']), 150, S.MINT, glow=S.MINT)
        self.cta = [text_layer(l, 50, S.YEL if i == 0 else S.WHITE, 'Bold') for i, l in enumerate(R.wrap(ImageDraw.Draw(self.bg), sh['cta'], S.F('Bold', 50), 940))]
        self.count_hint = text_layer('댓글에 먼저 남겨보세요', 44, (200, 212, 226), 'Bold')
        self.count_nums = {i: text_layer(str(i), 150, S.WHITE, glow=S.MINT) for i in range(sh['count'] + 1)}
        self.panel = Image.new('RGBA', (W - 80, 470), (0, 0, 0, 0))
        ImageDraw.Draw(self.panel).rounded_rectangle([0, 0, W - 81, 469], radius=36, fill=(255, 255, 255, 16), outline=(255, 255, 255, 40), width=2)
        rng = np.random.default_rng(room + 7)
        self.conf = [(rng.uniform(-14, 14), rng.uniform(-30, -12), rng.uniform(0, 6.28), rng.uniform(-0.3, 0.3),
                      [S.MINT, S.YEL, S.CORAL, (140, 170, 255), S.WHITE][rng.integers(5)]) for _ in range(90)]
        a = next(s for s in segs if s[0] == 'answer')
        self.reveal = [a[1] + a[2] * (0.12 + 0.15 * i) for i in range(len(sh['legend']))]
        self.code_t = a[1] + a[2] * 0.78

    def legend_row(self, fr, t, y, show_vals):
        keys = self.sh['legend']; n = len(keys); gap = 195; x0 = W / 2 - gap * (n - 1) / 2 + 70
        put(fr, self.code_lbl, x0 - 165, y + 4)
        for i, k in enumerate(keys):
            x = x0 + i * gap; put(fr, self.icons[k], x, y)
            if show_vals and t >= self.reveal[i]:
                put(fr, self.badges[k], x + 60, y - 58, ease_out_back((t - self.reveal[i]) / 0.35))
            elif not show_vals or t < self.reveal[i]:
                put(fr, self.qmark, x + 60, y - 58)

    def draw(self, t, phase, pt):
        fr = self.bg.copy()
        off = int(t * 22) % H; fr.alpha_composite(self.bok.crop((0, off, W, off + H)))
        put(fr, self.brand, W / 2, 86)
        answer = phase in ('answer', 'cta')
        if answer:
            a = next(s for s in self.segs if s[0] == 'answer')[1]
            put(fr, self.head_ans, W / 2, 230, ease_out_back((t - a) / 0.4))
        else:
            for i, lay in enumerate(self.hook):
                put(fr, lay, W / 2, 190 + i * 96, ease_out_back((t - 0.05 - i * 0.25) / 0.4), min(1, (t - i * 0.25) * 4))
        for i, (spr, pos) in enumerate(self.sprites):
            st = 0.25 + 0.22 * i; k = ease_out_back((t - st) / 0.55)
            top = SLOT0 + i * SLOT - 150 * (1 - k) + 4 * math.sin(2 * math.pi * (t * 0.3 + i * 0.33))
            put(fr, spr, W / 2, top + spr.height / 2, 1, min(1, max(0, (t - st) * 3)))
            put(fr, self.labels[i], 120, top + 330, 1, min(1, max(0, (t - st - 0.3) * 3)))
            if answer:
                for p in pos:
                    j = self.sh['legend'].index(p['shape'])
                    if t >= self.reveal[j]:
                        put(fr, self.badges[p['shape']], p['x'] * SPR, top + p['y'] * SPR - 52, 0.8 * ease_out_back((t - self.reveal[j]) / 0.35))
        fr.alpha_composite(self.panel, (40, PANEL_Y))
        cy = PANEL_Y + 235
        if phase in ('hook', 'rule'):
            k = ease((t - 0.9) / 0.5)
            for i, lay in enumerate(self.rule): put(fr, lay, W / 2, PANEL_Y + 70 + i * 66, 1, k)
            self.legend_row(fr, t, PANEL_Y + 330, False)
        elif phase == 'count':
            n = self.sh['count']; left = n - pt; r = 128; cx = W / 2
            d = ImageDraw.Draw(fr)
            d.ellipse([cx - r, cy - r - 20, cx + r, cy + r - 20], outline=(255, 255, 255, 40), width=16)
            frac = max(0, left / n); col = S.MINT if left > 3 else S.CORAL
            d.arc([cx - r, cy - r - 20, cx + r, cy + r - 20], -90, -90 + 360 * frac, fill=col, width=16)
            sec = math.ceil(left - 1e-6); beat = pt - math.floor(pt)
            put(fr, self.count_nums[max(sec, 0)], cx, cy - 20, 1 + 0.18 * (1 - ease(beat / 0.25)))
            put(fr, self.count_hint, W / 2, PANEL_Y + 425)
        else:
            self.legend_row(fr, t, PANEL_Y + 120, True)
            if t >= self.code_t:
                k = ease_out_back((t - self.code_t) / 0.45)
                put(fr, self.code, W / 2, PANEL_Y + 320 if phase == 'answer' else PANEL_Y + 290, k)
                dt = t - self.code_t
                if dt < 2.2:
                    d = ImageDraw.Draw(fr)
                    for vx, vy, a0, va, col in self.conf:
                        x = W / 2 + vx * dt * 40; y = PANEL_Y + 300 + vy * dt * 40 + 0.5 * 900 * dt * dt
                        ang = a0 + va * dt * 30; s1, c1 = math.sin(ang) * 11, math.cos(ang) * 11
                        d.polygon([(x - c1, y - s1), (x + s1 * 0.5, y - c1 * 0.5), (x + c1, y + s1), (x - s1 * 0.5, y + c1 * 0.5)],
                                  fill=(*col, int(255 * min(1, (2.2 - dt) * 2))))
            if phase == 'cta':
                a = next(s for s in self.segs if s[0] == 'cta')[1]
                for i, lay in enumerate(self.cta):
                    put(fr, lay, W / 2, PANEL_Y + 420 + i * 66 + 40 * (1 - ease((t - a) / 0.4)), 1, ease((t - a) / 0.4))
        return fr.convert('RGB')


def sfx(n, kind):
    t = np.arange(int(n * R.SR)) / R.SR
    if kind == 'pop':
        f = 520 + 900 * np.exp(-t * 40); return 0.35 * np.sin(2 * np.pi * np.cumsum(f) / R.SR) * np.exp(-t * 18)
    if kind == 'thud':
        return 0.45 * np.sin(2 * np.pi * (90 + 60 * np.exp(-t * 30)) * t) * np.exp(-t * 14)
    if kind == 'chime':
        return sum(0.18 * np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2) for f in (784, 988, 1175, 1568))


def build(ep_dir):
    ep = json.load(open(f'{ep_dir}/episode.json')); sh = json.load(open(f'{ep_dir}/short3d.json'))
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
        dd = R.dur(f'{T}/{k}.wav') + (0.9 if k == 'answer' else 0.4)
        segs.append((k, t0, dd)); t0 += dd
        if k == 'rule': segs.append(('count', t0, COUNT)); t0 += COUNT
    total = t0
    sc = Scene(ep_dir, sh, room, segs)

    voice = np.zeros(int(total * R.SR) + R.SR)
    def add(sig, at):
        s0 = int(at * R.SR); voice[s0:s0 + len(sig)] += sig[:max(0, len(voice) - s0)]
    for k, st, dd in segs:
        if k == 'count': continue
        with wave.open(f'{T}/{k}.wav') as w:
            add(np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16) / 32768, st + 0.05)
    for i in range(len(sh['stack'])): add(sfx(0.3, 'thud'), 0.25 + 0.22 * i + 0.3)
    for r in sc.reveal: add(sfx(0.25, 'pop'), r)
    add(sfx(1.6, 'chime'), sc.code_t)
    music = R.bgm(len(voice) / R.SR, room)
    music = np.pad(music, (0, max(0, len(voice) - len(music))))[:len(voice)]
    duck = np.full_like(voice, 0.45); tick = np.zeros_like(voice)
    L = int(0.04 * R.SR); env = np.exp(-np.arange(L) / (0.008 * R.SR)); tone = 0.25 * np.sin(2 * np.pi * 1800 * np.arange(L) / R.SR) * env
    for k, st, dd in segs:
        if k == 'count':
            duck[int(st * R.SR):int((st + dd) * R.SR)] = 1.0
            for n in range(COUNT): s0 = int((st + n) * R.SR); tick[s0:s0 + L] += tone * (1.6 if COUNT - n <= 3 else 1)
    mix = (voice + music * 0.16 * duck + tick)[:int(total * R.SR)]
    fade = int(1.0 * R.SR); mix[-fade:] *= np.linspace(1, 0, fade)
    mix = np.clip(mix / max(1, np.abs(mix).max() / 0.9), -1, 1)
    with wave.open(f'{T}/mix.wav', 'w') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(R.SR)
        w.writeframes((np.repeat(mix[:, None], 2, axis=1) * 32767).astype(np.int16).tobytes())

    ff = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                           '-i', '-', '-i', f'{T}/mix.wav', '-vf', 'format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19',
                           '-profile:v', 'high', '-c:a', 'aac', '-b:a', '160k', '-ar', str(R.SR), '-t', f'{total:.3f}',
                           '-movflags', '+faststart', f'{ep_dir}/short.mp4'], stdin=subprocess.PIPE)
    qa = {k: st + dd * (0.95 if k in ('answer', 'cta') else 0.5) for k, st, dd in segs}
    for i in range(int(total * FPS) + 1):
        t = i / FPS; k, st, dd = next((s for s in segs if s[1] <= t < s[1] + s[2]), segs[-1])
        fr = sc.draw(t, k, t - st); ff.stdin.write(fr.tobytes())
        if abs(t - qa[k]) < 0.5 / FPS: fr.save(f'{T}/qa-{k}.png')
    ff.stdin.close(); assert ff.wait() == 0
    print(f'short ok {total:.1f}s')


if __name__ == '__main__':
    build(sys.argv[1])
