#!/usr/bin/env python3
"""ПОТОП s01 — сведение звука для сокращённой версии: голос (voice_short.wav) + фон + эффекты по словам.
python3 mix.py <out.wav>   → stem без нормализации (громкость доводится в build.sh до -14 LUFS)"""
import json, subprocess, sys, os
H = os.path.dirname(os.path.abspath(__file__)); SND = os.path.join(H, '..', 'sound')
W = {w['i']: w for w in json.load(open(os.path.join(H, 'words_short.json')))}
T = lambda i: W[i]['s']
VE = max(w['e'] for w in W.values()) + .25; DUR = VE + 2.2
VOICE_GAIN = 13.0
BED_GAIN = (-27.0 + VOICE_GAIN) - 19.0 - (-32.9)   # фон на ~19 дБ тише голоса (drone2 = -32.9 LUFS)
a2, a12, a17, a18, a21 = T(23) - .2, T(76) - .15, T(98) - .2, T(106) - .15, T(127) - .15
tb = T(98)
F = lambda a, b: f'afade=t=in:d=0.5,afade=t=out:st={max(.1, b - a - .6):.2f}:d=0.6'
EV = [
    ('amb_rain_loop_1.ogg', 0, a2 + .5, 0, -8, f'afade=t=in:d=0.4,afade=t=out:st={a2 - .1:.2f}:d=0.6'),            # дождь за окном
    ('amb_rain_loop_1.ogg', 13.4, a12 - a2 + .8, a2 - .3, -12, 'lowpass=f=500,' + F(a2, a12 + .5)),               # глухой дождь в доме
    ('amb_rain_loop_1.ogg', 40, a21 - a18 + .8, a18 - .3, -13, 'lowpass=f=500,' + F(a18, a21 + .5)),              # снова дождь за стенами
    ('amb_rain_loop_1.ogg', 0, DUR - a21 + .3, a21 - .2, -9, f'afade=t=in:d=0.6,afade=t=out:st={DUR - a21 - 2.2:.2f}:d=2.4'),  # дождь над городом
    ('rain-thunder.ogg', 21.0, 7.5, .1, -9, 'lowpass=f=1800,afade=t=out:st=5:d=2.5'),                              # гром в первую секунду
    ('wind_woosh_loop.ogg', 0, 5.9, .3, -14, 'afade=t=in:d=1.5,afade=t=out:st=4.4:d=1.5'),
    ('wind_woosh_loop.ogg', 0, 5.9, T(132) - .5, -15, 'afade=t=in:d=1.5,afade=t=out:st=4.4:d=1.5'),
    ('wind_woosh_loop.ogg', 1.0, 1.2, T(72) - .1, -16, 'afade=t=in:d=0.3,afade=t=out:st=0.6:d=0.6'),             # вжух на большой записке
    ('bfh1_rock_breaking_01.ogg', 0, 1.15, T(61), -10, 'lowpass=f=2500,aecho=0.8:0.6:60:0.4'),                    # треск дома
    ('tree_creak.ogg', 0.2, 2.6, T(61) + .1, -6, 'asetrate=44100*0.8,aresample=44100,afade=t=out:st=2:d=0.6'),
    ('tree_creak.ogg', 2.3, 1.6, T(63) + .2, -8, 'asetrate=44100*0.7,aresample=44100,afade=t=out:st=1.0:d=0.6'),   # дом кренится
    ('bfh1_wood_breaking_01.ogg', 0, 0.3, T(65) + .4, -10, 'lowpass=f=1500'),
    ('metal_steps.ogg', 0.0, 1.75, T(76), -12, 'lowpass=f=1500,aecho=0.8:0.7:90|160:0.35|0.25'),                  # шаги вниз
    ('water_splashes.ogg', 2.6, 0.6, T(76) + .9, -14, 'aecho=0.8:0.6:120:0.3'),
    ('water_splashes.ogg', 4.05, 1.0, T(87) + .5, -16, 'lowpass=f=2000,aecho=0.8:0.6:140:0.3'),                   # плеск у лодки
    ('bfh1_metal_hit_01.ogg', 0, 1.0, T(132) - .05, -20, 'lowpass=f=700,aecho=0.8:0.8:200:0.4'),                   # город включился
]
for i in range(4): EV.append(('heartbeat_slow.ogg', 0, 0.9, tb + i * 0.9, -3 if i < 3 else -7, 'lowpass=f=900'))  # пульс в такт кадру

cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-i', os.path.join(H, 'voice_short.wav'), '-i', os.path.join(SND, 'drone2.ogg')]
fc = [f'[0:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={VOICE_GAIN}dB,apad=whole_dur={DUR:.2f}[v]',
      f"[1:a]aformat=sample_rates=44100:channel_layouts=stereo,atrim=0:{DUR:.2f},volume={BED_GAIN:.1f}dB,"
      f"volume='if(between(t,{tb - .1:.2f},{a18 + .1:.2f}),0.3,1)':eval=frame,afade=t=in:d=2,afade=t=out:st={DUR - 3:.2f}:d=3[bed]"]
labels = ['[v]', '[bed]']
for k, (f, ss, d, at, g, extra) in enumerate(EV):
    cmd += ['-ss', str(ss), '-t', f'{d:.2f}', '-i', os.path.join(SND, f)]
    n = k + 2; ms = int(max(0, at) * 1000)
    fc.append(f'[{n}:a]aformat=sample_rates=44100:channel_layouts=stereo,{extra + "," if extra else ""}volume={g}dB,adelay={ms}|{ms}[e{k}]')
    labels.append(f'[e{k}]')
fc.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{DUR:.2f}[out]")
cmd += ['-filter_complex', ';'.join(fc), '-map', '[out]', '-c:a', 'pcm_s16le', sys.argv[1]]
subprocess.run(cmd, check=True); print('ok', sys.argv[1], f'{DUR:.1f} c')
