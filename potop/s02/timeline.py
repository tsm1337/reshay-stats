#!/usr/bin/env python3
"""ПОТОП s02 — сокращённая версия: вырезает проходные фразы из готовой озвучки (без новой генерации),
сжимает паузы, пишет voice_short.wav и words_short.json (новые тайминги слов; поле i — номер слова в words.json)."""
import json, subprocess, os, sys
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
SR = 44100
words = json.load(open(os.path.join(H, 'words.json')))
# вырезаем: «Мимо плыли машины.», «Никто в общаге не знал зачем.», «Неделю назад мы ехали в одном купе.», «Её искали с самого утра.»
CUT = set()
if os.environ.get('CUT_EXTRA'):
    CUT |= set(map(int, os.environ['CUT_EXTRA'].split(',')))
KEEP = [i for i in range(len(words)) if i not in CUT]
SPECIAL = {3: .55, 22: .5, 27: .5, 31: .35, 80: .5, 87: .45, 99: .45, 100: .4, 102: .4, 110: .85, 112: .5, 115: .95, 121: .5, 124: .5, 127: .95, 72: .45}  # драматические паузы перед словом i
DEF_SENT, DEF_IN = .36, .28
PAD_IN, PAD_OUT = .05, .09

x = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(H, 'voice.mp3'), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
end_punct = ('.', '…', '!', '?', ':', '»')

# сегменты подряд идущих слов без разрыва
segs = []; cur = [KEEP[0]]
for a, b in zip(KEEP, KEEP[1:]):
    gap = words[b]['s'] - words[a]['e']
    sent = words[a]['w'].endswith(end_punct)
    target = SPECIAL.get(b, DEF_SENT if sent else DEF_IN)
    if b == a + 1 and gap <= target + .12:
        cur.append(b)
    else:
        segs.append((cur, target)); cur = [b]
segs.append((cur, 0))

out = np.zeros(int((words[KEEP[-1]]['e'] + 40) * SR), np.float32); t_new = 0.12; new_words = {}
for k, (idx, target_after) in enumerate(segs):
    s0 = max(words[idx[0]]['s'] - PAD_IN, (words[idx[0] - 1]['e'] + .02) if idx[0] > 0 else 0)
    e0 = min(words[idx[-1]]['e'] + PAD_OUT, (words[idx[-1] + 1]['s'] - .02) if idx[-1] + 1 < len(words) else 1e9)
    a, b = int(s0 * SR), int(e0 * SR); seg = x[a:b].copy(); f = int(.012 * SR)
    seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    p = int(t_new * SR); out[p:p + len(seg)] += seg
    for i in idx: new_words[i] = (words[i]['s'] - s0 + t_new, words[i]['e'] - s0 + t_new)
    seg_len = (b - a) / SR
    realized = (words[idx[-1]]['e'] + PAD_OUT) - words[idx[-1]]['e']  # хвост уже включён
    t_new += seg_len + max(.04, target_after - PAD_OUT - PAD_IN)
last_end = max(e for s, e in new_words.values())
voice_end = last_end + .25
out = out[:int(voice_end * SR)]
wav = os.path.join(H, 'voice_short.wav')
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', wav], input=out.tobytes(), check=True)
json.dump([{'i': i, 'w': words[i]['w'], 's': round(new_words[i][0], 3), 'e': round(new_words[i][1], 3)} for i in KEEP], open(os.path.join(H, 'words_short.json'), 'w'), ensure_ascii=False)
OUTRO = 3.0
print(f'речь до {last_end:.1f} с, ролик {voice_end + OUTRO:.1f} с (с титром {OUTRO} с)')
line = ''
for i in KEEP:
    line += f"{i}:{words[i]['w']}@{new_words[i][0]:.1f} "
    if words[i]['w'].endswith(end_punct): print(line); line = ''
print(line)
