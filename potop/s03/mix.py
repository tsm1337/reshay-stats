#!/usr/bin/env python3
"""ПОТОП s03 — сведение звука: голос (voice_short.wav) + фон + эффекты по словам.
python3 mix.py <out.wav>"""
import json, subprocess, sys, os
H = os.path.dirname(os.path.abspath(__file__)); S1 = os.path.join(H, '..', 'sound'); S2 = os.path.join(H, '..', 'sound2'); CR = os.path.join(S2, 'oga', 'creature')
W = {w['i']: w for w in json.load(open(os.path.join(H, 'words_short.json')))}
T = lambda i: W[i]['s']
VE = max(w['e'] for w in W.values()) + .35; DUR = VE + 3.0
VOICE_GAIN = 13.0
BED_GAIN = (-27.0 + VOICE_GAIN) - 19.0 - (-32.9)
EV = []
def ev(f, ss, d, at, g, extra=''): EV.append((f, ss, d, at, g, extra))
fd = lambda d, i=.3, o=.4: f'afade=t=in:d={i},afade=t=out:st={max(.05, d - o):.2f}:d={o}'
rain, thunder, wind = os.path.join(S1, 'amb_rain_loop_1.ogg'), os.path.join(S1, 'rain-thunder.ogg'), os.path.join(S1, 'wind_woosh_loop.ogg')
creak, splash, steps = os.path.join(S1, 'tree_creak.ogg'), os.path.join(S1, 'water_splashes.ogg'), os.path.join(S1, 'metal_steps.ogg')
hit, wood, rock, beat = os.path.join(S1, 'bfh1_metal_hit_01.ogg'), os.path.join(S1, 'bfh1_wood_breaking_01.ogg'), os.path.join(S1, 'bfh1_rock_breaking_01.ogg'), os.path.join(S1, 'heartbeat_slow.ogg')
whistle, crowd = os.path.join(S2, 'whistle.wav'), os.path.join(S2, 'oga', 'crowd_shouting.ogg')
c = lambda n: os.path.join(CR, n)
a_calm = T(133)
# --- фон: тишина, подвал, вода стоит; капли весь ролик
ev(os.path.join(S2, 'oga', 'water_drops.mp3'), 60, T(133) - .2, 0, -19, 'lowpass=f=3500,' + fd(T(133), 1.5, .5))
ev(splash, 0.5, 4.0, T(0) + .2, -27, 'lowpass=f=900,' + fd(4.0, .6, 1.0))
# Аня поднимает голову
ev(creak, 0.5, 2.6, T(7) - .1, -13, 'lowpass=f=1100,asetrate=44100*0.7,aresample=44100,' + fd(2.6, .3, .8))
ev(c('breath.ogg'), 0, .67, T(9) + .1, -12, 'lowpass=f=1500,aecho=0.8:0.6:120:0.3')
ev(c('breath.ogg'), 0, .67, T(17) - .1, -15, 'lowpass=f=1500,aecho=0.8:0.6:120:0.3')
# записки на двери
ev(wood, 0, .3, T(19) + .1, -15, 'lowpass=f=900')
# бабушка ахнула
ev(c('breath.ogg'), 0, .67, T(28) - .05, -6, 'asetrate=44100*1.25,aresample=44100,aecho=0.8:0.5:90:0.3')
# мужчина с собакой, скулёж
ev(splash, 2, 1.4, T(45), -14, 'lowpass=f=1800,' + fd(1.4, .1, .5))
ev(steps, 0, 1.2, T(45) - .1, -18, 'lowpass=f=1200,aecho=0.8:0.7:90:0.3')
ev(c('cute_02.ogg'), 0, .46, T(44) + .3, -9, 'lowpass=f=2500,asetrate=44100*0.8,aresample=44100,aecho=0.8:0.5:120:0.35')
ev(c('cute_05.ogg'), 0, .5, T(73) + .2, -8, 'lowpass=f=2500,asetrate=44100*0.75,aresample=44100,aecho=0.8:0.5:130:0.4')
ev(c('cute_02.ogg'), 0, .46, T(74) + .6, -10, 'lowpass=f=2500,asetrate=44100*0.7,aresample=44100,aecho=0.8:0.5:130:0.4')
# лодка ждёт, вода поднимается
ev(creak, 3, 3.0, T(58), -14, 'lowpass=f=1200,asetrate=44100*0.8,aresample=44100,' + fd(3.0, .3, .8))
ev(hit, 0, .24, T(64) + .2, -18, 'lowpass=f=500,aecho=0.8:0.8:240:0.4')
ev(splash, 0, 5.6, T(66) - .1, -13, 'lowpass=f=1800,' + fd(5.6, .4, 1.2))
# часы, пульс
for k, tt in enumerate((T(80), T(82), T(83) + .25)): ev(hit, 0, .24, tt, -23, 'highpass=f=1200,lowpass=f=4000')
for i in range(4): ev(beat, 0, .9, T(84) + i * 1.0, -11, 'lowpass=f=800')
# Вера, Аня
ev(c('breath.ogg'), 0, .67, T(90) - .2, -17, 'lowpass=f=1500')
ev(creak, 0.5, 2.0, T(100), -17, 'lowpass=f=900,asetrate=44100*0.6,aresample=44100,' + fd(2.0, .3, .8))
# свисток: звякнуло, цифры
ev(hit, 0, .24, T(115) - .1, -12, 'highpass=f=1500,aecho=0.8:0.7:100:0.35')
for k, i in enumerate((122, 123, 124, 125)): ev(hit, 0, .24, T(i) + .05, -9 + k, 'asetrate=44100*' + str(1.0 + k * .08) + ',aresample=44100,aecho=0.8:0.8:180:0.4')
ev(hit, 0, .24, T(128), -12, 'lowpass=f=700,aecho=0.8:0.8:260:0.45')
for i in range(4): ev(beat, 0, .9, T(113) + i * .95, -9, 'lowpass=f=900')
# вода дрогнула и идёт вверх
ev(thunder, 21.0, 6.0, T(133) - .1, -12, 'lowpass=f=900,afade=t=out:st=3:d=2.5')
ev(splash, 0, 5.6, T(134), -9, 'lowpass=f=2200,' + fd(5.6, .2, 1.6))
ev(rock, 0, 1.15, T(134), -14, 'lowpass=f=1800,aecho=0.8:0.6:90:0.4')
ev(creak, 2.3, 2.5, T(135), -11, 'lowpass=f=1000,asetrate=44100*0.65,aresample=44100,' + fd(2.5, .2, 1.0))
# Вера достала свисток
ev(hit, 0, .24, T(140) + .3, -13, 'highpass=f=1200,aecho=0.8:0.8:200:0.4')
ev(hit, 0, .24, T(145) - .05, -9, 'lowpass=f=900,aecho=0.8:0.9:320:0.5')
ev(beat, 0, .9, T(145) + .35, -6, 'lowpass=f=700'); ev(beat, 0, .9, T(145) + 1.3, -7, 'lowpass=f=700')

cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-i', os.path.join(H, 'voice_short.wav'), '-i', os.path.join(S1, 'drone2.ogg')]
fc = [f'[0:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={VOICE_GAIN}dB,apad=whole_dur={DUR:.2f}[v]',
      # фон: тише на тишине «вода замерла» и усиливается к финалу
      f"[1:a]aformat=sample_rates=44100:channel_layouts=stereo,atrim=0:{DUR:.2f},volume={BED_GAIN:.1f}dB,"
      f"volume='if(between(t,{a_calm - .05:.2f},{T(115) - .2:.2f}),0.25,1)':eval=frame,afade=t=in:d=2,afade=t=out:st={DUR - 3:.2f}:d=3[bed]"]
labels = ['[v]', '[bed]']
for k, (f, ss, d, at, g, extra) in enumerate(EV):
    cmd += ['-ss', str(ss), '-t', f'{d:.2f}', '-i', f]
    n = k + 2; ms = int(max(0, at) * 1000)
    fc.append(f'[{n}:a]aformat=sample_rates=44100:channel_layouts=stereo,{extra + "," if extra else ""}volume={g}dB,adelay={ms}|{ms}[e{k}]')
    labels.append(f'[e{k}]')
fc.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{DUR:.2f}[out]")
cmd += ['-filter_complex', ';'.join(fc), '-map', '[out]', '-c:a', 'pcm_s16le', sys.argv[1]]
subprocess.run(cmd, check=True); print('ok', sys.argv[1], f'{DUR:.1f} c', len(EV), 'эффектов')
