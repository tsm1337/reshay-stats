#!/usr/bin/env python3
"""ПОТОП s01 — сведение звука: голос + фон (drone) + редкие эффекты.
python3 mix.py <out.wav>   → stem без нормализации (громкость доводится в сборке до -14 LUFS)
"""
import subprocess, sys, os
H = os.path.dirname(os.path.abspath(__file__))
SND = os.path.join(H, '..', 'sound')
DUR = 80.5
VOICE_GAIN = 13.0          # голос -27 → ~-14 LUFS
BED_GAIN = (-27.0 + VOICE_GAIN) - 19.0 - (-32.9)  # фон ≈ на 19 дБ тише голоса (drone2 = -32.9 LUFS)

# (файл, старт в файле, длительность, где в ролике, громкость дБ, доп. фильтры)
EV = [
    ('amb_rain_loop_1.ogg', 0, 13.4, 0.0, -8, 'afade=t=in:d=1,afade=t=out:st=12.9:d=0.5'),           # дождь за окном
    ('amb_rain_loop_1.ogg', 13.4, 43.0, 13.25, -12, 'lowpass=f=500,afade=t=in:d=0.4,afade=t=out:st=42.4:d=0.6'),  # дождь глухо, в доме
    ('amb_rain_loop_1.ogg', 60.0, 10.6, 60.8, -13, 'lowpass=f=500,afade=t=in:d=1.5,afade=t=out:st=10:d=0.6'),  # снова дождь за стенами
    ('amb_rain_loop_1.ogg', 0, 9.5, 71.3, -9, 'afade=t=in:d=0.5,afade=t=out:st=7:d=2.5'),              # дождь над городом
    ('rain-thunder.ogg', 21.0, 7.5, 3.55, -13, 'lowpass=f=1800,afade=t=out:st=5:d=2.5'),               # гром на «море»
    ('wind_woosh_loop.ogg', 0, 5.9, 0.3, -14, 'afade=t=in:d=1.5,afade=t=out:st=4.4:d=1.5'),           # ветер
    ('wind_woosh_loop.ogg', 0, 5.9, 72.0, -15, 'afade=t=in:d=1.5,afade=t=out:st=4.4:d=1.5'),
    ('wind_woosh_loop.ogg', 1.0, 1.2, 38.55, -16, 'afade=t=in:d=0.3,afade=t=out:st=0.6:d=0.6'),         # «вжух» на записке
    ('bfh1_rock_breaking_01.ogg', 0, 1.15, 31.95, -10, 'lowpass=f=2500,aecho=0.8:0.6:60:0.4'),         # треск дома
    ('tree_creak.ogg', 0.2, 2.6, 32.05, -6, 'asetrate=44100*0.8,aresample=44100,afade=t=out:st=2:d=0.6'),  # скрип
    ('tree_creak.ogg', 2.3, 1.6, 34.15, -8, 'asetrate=44100*0.7,aresample=44100,afade=t=out:st=1.0:d=0.6'),  # дом кренится
    ('bfh1_wood_breaking_01.ogg', 0, 0.3, 34.6, -10, 'lowpass=f=1500'),
    ('metal_steps.ogg', 0.0, 1.75, 41.42, -12, 'lowpass=f=1500,aecho=0.8:0.7:90|160:0.35|0.25'),     # шаги вниз по лестнице
    ('water_splashes.ogg', 2.6, 0.6, 43.0, -14, 'aecho=0.8:0.6:120:0.3'),                            # шаг в воду
    ('water_splashes.ogg', 4.05, 1.0, 49.3, -16, 'lowpass=f=2000,aecho=0.8:0.6:140:0.3'),            # плеск у лодки
    ('bfh1_metal_hit_01.ogg', 0, 1.0, 72.8, -20, 'lowpass=f=700,aecho=0.8:0.8:200:0.4'),             # город «включился»
]
# сердце: удары синхронно с пульсом кадра (период 0.9 с, старт 56.74)
for i in range(5):
    EV.append(('heartbeat_slow.ogg', 0, 0.9, 56.74 + i * 0.9, -3 if i < 4 else -7, 'lowpass=f=900'))

cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-i', os.path.join(H, 'voice.mp3'), '-i', os.path.join(SND, 'drone2.ogg')]
fc = [f'[0:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={VOICE_GAIN}dB,apad=whole_dur={DUR}[v]',
      # фон: тихий, ровный; в «тишине» (56.6–60.7) почти пропадает
      f"[1:a]aformat=sample_rates=44100:channel_layouts=stereo,atrim=0:{DUR},volume={BED_GAIN:.1f}dB,"
      f"volume='if(between(t,56.5,60.8),0.3,1)':eval=frame,afade=t=in:d=2,afade=t=out:st={DUR - 3}:d=3[bed]"]
labels = ['[v]', '[bed]']
for k, (f, ss, d, at, g, extra) in enumerate(EV):
    cmd += ['-ss', str(ss), '-t', str(d), '-i', os.path.join(SND, f)]
    n = k + 2; ms = int(at * 1000)
    fc.append(f'[{n}:a]aformat=sample_rates=44100:channel_layouts=stereo,{extra + "," if extra else ""}volume={g}dB,adelay={ms}|{ms}[e{k}]')
    labels.append(f'[e{k}]')
fc.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{DUR}[out]")
cmd += ['-filter_complex', ';'.join(fc), '-map', '[out]', '-c:a', 'pcm_s16le', sys.argv[1]]
subprocess.run(cmd, check=True)
print('ok', sys.argv[1])
