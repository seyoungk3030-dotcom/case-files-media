"""Build reel.mp4 (1080x1920, ~30-40s): an animated fast-hook reel over 3D sprites rendered by kit/b3d.py.

Episode folder needs sprites in .build-3d/ and short3d.json. The puzzle area (y 330..1380) is either
 "layout": [{"sprite": "stack-A", "answer_sprite": "xray-A", "x": 290, "y": 600, "w": 440, "label": "A", "key": "A"}, ...]
   (free placement; "key" puts that legend value's badge on the sprite's top centre during the answer; or
   "marks": "<json name>" with "tags": {key: "text"} to pin text pills and answer badges to points in one big sprite), or
 "stack": ["scale1", ...], "stack_labels": ["저울 1", ...]  (full-width rows; <name>.json from b3d.project places badges).
Other fields: {"hook": ["line 1", "line 2"], "rule": ["line", "line"], "legend": ["c", "t", "s", "r"]
 (icon-<k>.png if present, else a letter pill coloured by optional "legend_colors"), "values": {"c": 1, ...},
 "answer": "1325", "count": 10, "cta": "one line",
 "narration": {"hook": "...", "rule": "...", "answer": "...", "cta": "..."}}   (numbers in narration as Korean words)
The answer narration should name the legend items in order; their reveals are spaced across its first 70%.
Usage: python3 short3d.py <absolute episode_dir>
"""
import asyncio, json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import style as S
import reel as R
from style3d import ease_out_back, ease, background, text_layer, pill, badge, put, trim
import edge_tts

W, H, FPS = 1080, 1920, 30
SLOT0, SLOT, SPR = 330, 318, 1.08          # first sprite top, sprite spacing, sprite scale
PANEL_Y = 1395


class Scene:
    def __init__(self, ep_dir, sh, room, segs):
        B = f'{ep_dir}/.build-3d'; self.sh, self.segs = sh, segs
        self.bg, self.bok = background(room)
        self.items = []                      # sprite, answer sprite, centre, label, badge marks relative to the sprite's top-left
        if 'layout' in sh:
            for it in sh['layout']:
                im = Image.open(f'{B}/{it["sprite"]}.png').convert('RGBA')
                if not it.get('marks'): im = trim(im)
                sc = it['w'] / im.width
                im = im.resize((it['w'], round(im.height * sc)), Image.LANCZOS)
                ans = im
                if it.get('answer_sprite'):
                    ans = Image.open(f'{B}/{it["answer_sprite"]}.png').convert('RGBA')
                    if not it.get('marks'): ans = trim(ans)
                    k = min(im.width / ans.width, im.height / ans.height); ans = ans.resize((round(ans.width * k), round(ans.height * k)), Image.LANCZOS)
                marks, tags = ([(it['key'], im.width / 2, 0, 1.35)] if it.get('key') else []), []
                if it.get('marks'):   # positions from b3d-style json [{key, x, y}] in the untrimmed sprite's pixels
                    pts = json.load(open(f'{B}/{it["marks"]}.json'))
                    off = it.get('badge_offset', {})
                    marks = [(p['key'], p['x'] * sc + off.get(p['key'], [70, -50])[0], p['y'] * sc + off.get(p['key'], [70, -50])[1], 1.0)
                             for p in pts if p['key'] in sh['legend']]
                    tags = [(pill(it['tags'][p['key']], 30, (16, 28, 44), (244, 246, 250, 245)),
                             p['x'] * sc, p['y'] * sc) for p in pts if p['key'] in it.get('tags', {})]
                self.items.append({'im': im, 'ans': ans, 'cx': it['x'], 'cy': it['y'], 'label': it.get('label'),
                                   'lpos': (14, 22), 'marks': marks, 'tags': tags})
        else:
            for i, (name, lab) in enumerate(zip(sh['stack'], sh['stack_labels'])):
                im = Image.open(f'{B}/{name}.png').convert('RGBA')
                im = im.resize((int(im.width * SPR), int(im.height * SPR)), Image.LANCZOS)
                marks = [(p['shape'], p['x'] * SPR, p['y'] * SPR - 52, 0.8) for p in json.load(open(f'{B}/{name}.json'))]
                self.items.append({'im': im, 'ans': im, 'cx': W / 2, 'cy': SLOT0 + i * SLOT + im.height / 2, 'label': lab,
                                   'lpos': (120 - (W - im.width) / 2, 330), 'marks': marks})
        self.icons = {}
        for k in sh['legend']:
            if os.path.exists(f'{B}/icon-{k}.png'):
                v = trim(Image.open(f'{B}/icon-{k}.png').convert('RGBA')); self.icons[k] = v.resize((int(v.width * 150 / v.height), 150), Image.LANCZOS)
            else:
                self.icons[k] = pill(k, 64, (16, 28, 44), (*sh.get('legend_colors', {}).get(k, S.MINT), 245), (34, 10))
        self.brand = pill(f'퇴근 후 사건파일  ·  ROOM {room:03d}', 30, (200, 212, 226), (255, 255, 255, 26))
        n = len(sh['hook'])
        self.hook = [text_layer(l, 70, S.YEL if i == n - 1 else S.WHITE) for i, l in enumerate(sh['hook'])]
        self.head_ans = text_layer('정답 공개', 84, S.MINT, glow=S.MINT)
        for it in self.items:
            col = sh.get('legend_colors', {}).get(it['label'], S.MINT)
            it['lab'] = pill(it['label'], 28 if 'stack' in sh else 40, (16, 28, 44), (*col, 240)) if it['label'] else None
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
        for i, it in enumerate(self.items):
            st = 0.25 + 0.22 * i; k = ease_out_back((t - st) / 0.55)
            spr = it['ans'] if answer else it['im']
            top = it['cy'] - spr.height / 2 - 150 * (1 - k) + 4 * math.sin(2 * math.pi * (t * 0.3 + i * 0.33))
            left = it['cx'] - spr.width / 2
            put(fr, spr, it['cx'], top + spr.height / 2, 1, min(1, max(0, (t - st) * 3)))
            if it['lab']: put(fr, it['lab'], left + it['lpos'][0], top + it['lpos'][1], 1, min(1, max(0, (t - st - 0.3) * 3)))
            for lay, tx, ty in it.get('tags', []): put(fr, lay, left + tx, top + ty, 1, min(1, max(0, (t - st - 0.4) * 3)))
            if answer:
                for key, dx, dy, sc in it['marks']:
                    j = self.sh['legend'].index(key)
                    if t >= self.reveal[j]:
                        put(fr, self.badges[key], left + dx, top + dy, sc * ease_out_back((t - self.reveal[j]) / 0.35))
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
    sh = json.load(open(f'{ep_dir}/short3d.json'))
    room = sh['room'] if 'room' in sh else json.load(open(f'{ep_dir}/episode.json'))['room']
    COUNT = sh.get('count', 10)
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
    for i in range(len(sc.items)): add(sfx(0.3, 'thud'), 0.25 + 0.22 * i + 0.3)
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
                           '-movflags', '+faststart', f'{ep_dir}/reel.mp4'], stdin=subprocess.PIPE)
    qa = {k: st + dd * (0.95 if k in ('answer', 'cta') else 0.5) for k, st, dd in segs}
    for i in range(int(total * FPS) + 1):
        t = i / FPS; k, st, dd = next((s for s in segs if s[1] <= t < s[1] + s[2]), segs[-1])
        fr = sc.draw(t, k, t - st); ff.stdin.write(fr.tobytes())
        if abs(t - qa[k]) < 0.5 / FPS: fr.save(f'{T}/qa-{k}.png')
    ff.stdin.close(); assert ff.wait() == 0
    print(f'short ok {total:.1f}s')


if __name__ == '__main__':
    build(sys.argv[1])
