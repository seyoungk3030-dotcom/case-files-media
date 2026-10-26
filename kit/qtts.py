"""Narration with Qwen3-TTS (1.7B CustomVoice, Korean speaker Sohee), run with the venv at /home/user/qtts:
  /home/user/qtts/bin/python kit/qtts.py <absolute episode_dir>
Reads short3d.json "narration" and writes .build-short/<key>.wav (+ <key>.txt with the text it was made from), which
kit/short3d.py then reuses instead of edge-tts. Lines whose .txt already matches are skipped.
Setup once per container (~3 GB): python3 -m venv /home/user/qtts &&
  /home/user/qtts/bin/pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu && /home/user/qtts/bin/pip install qwen-tts"""
import json, os, sys, time
import soundfile as sf, torch
from qwen_tts import Qwen3TTSModel

MODEL, SPEAKER = 'Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice', 'Sohee'
STYLE = '밝고 자연스러운 20대 여성 퀴즈 진행자처럼, 또박또박하지만 경쾌하게 말해 주세요.'

ep = sys.argv[1]; T = f'{ep}/.build-short'; os.makedirs(T, exist_ok=True)
nar = json.load(open(f'{ep}/short3d.json'))['narration']
todo = {k: v for k, v in nar.items() if not (os.path.exists(f'{T}/{k}.wav') and os.path.exists(f'{T}/{k}.txt')
                                              and open(f'{T}/{k}.txt').read() == v)}
if todo:
    torch.set_num_threads(os.cpu_count() or 4); t = time.time()
    m = Qwen3TTSModel.from_pretrained(MODEL, device_map='cpu', dtype=torch.float32)
    for k, text in todo.items():
        w, sr = m.generate_custom_voice(text=text, speaker=SPEAKER, language='Korean', instruct=STYLE)
        sf.write(f'{T}/{k}.wav', w[0], sr); open(f'{T}/{k}.txt', 'w').write(text)
        print(k, round(len(w[0]) / sr, 1), 's', flush=True)
    print('qtts', round(time.time() - t), 's')
print('qtts ok')
