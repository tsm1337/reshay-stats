#!/usr/bin/env python3
"""ПОТОП s02 — сведение звука: голос (voice_short.wav) + фон + эффекты по словам.
python3 mix.py <out.wav>"""
import json, subprocess, sys, os
H = os.path.dirname(os.path.abspath(__file__)); S1 = os.path.join(H, '..', 'sound'); S2 = os.path.join(H, '..', 'sound2'); CR = os.path.join(S2, 'oga', 'creature')
W = {w['i']: w for w in json.load(open(os.path.join(H, 'words_short.json')))}
T = lambda i: W[i]['s']
VE = max(w['e'] for w in W.values()) + .35; DUR = VE + 4.5
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
a2, a_calm, a_end = T(6) - .1, T(110), T(127)

# --- город: дождь снаружи, гром, ветер (до спуска в подвал)
ev(rain, 0, a2 + .6, 0, -8, f'afade=t=in:d=0.4,afade=t=out:st={a2 - .2:.2f}:d=0.8')
ev(thunder, 21.0, 6.5, .1, -9, 'lowpass=f=1800,afade=t=out:st=4:d=2.5')
ev(wind, 0, 5.9, .2, -15, 'afade=t=in:d=1.2,afade=t=out:st=4.4:d=1.5')
# --- подвал: глухой дождь сверху, капли, вода
ev(rain, 14, a_calm - a2 + .5, a2 - .3, -19, 'lowpass=f=400,' + fd(a_calm - a2, .8, 1.2))
ev(os.path.join(S2, 'oga', 'water_drops.mp3'), 30, a_calm - T(12) + .3, T(12) - .2, -17, 'lowpass=f=3500,' + fd(a_calm - T(12), .8, .6))
ev(splash, 1.0, 4.0, T(15), -20, 'lowpass=f=1200,' + fd(4.0, .5, .8))
# удар сверху, лампочка
ev(rock, 0, 1.15, T(9) - .05, -9, 'lowpass=f=2200,aecho=0.8:0.6:70:0.4')
ev(creak, 0.2, 2.2, T(9) + .1, -11, 'asetrate=44100*0.75,aresample=44100,' + fd(2.2, .1, .8))
for k, dt in enumerate((.0, .12, .22)): ev(hit, 0, .24, T(11) + dt, -22 - k * 2, 'lowpass=f=1800')
# люди внизу: приглушённый шёпот толпы
ev(crowd, 3, T(22) - T(12) + .5, T(12) - .3, -33, 'lowpass=f=450,' + fd(T(22) - T(12), 1.0, 1.2))
ev(c('barking_01.ogg'), 0, .4, T(21) + .35, -14, 'lowpass=f=1800,aecho=0.8:0.5:90:0.35')
# лодка
ev(creak, 3, 3.2, T(23), -11, 'lowpass=f=1500,asetrate=44100*0.85,aresample=44100,' + fd(3.2, .3, .8))
ev(creak, 0, 2.0, T(32) - .3, -13, 'lowpass=f=1200,asetrate=44100*0.7,aresample=44100,' + fd(2.0, .2, .6))
ev(wood, 0, .3, T(31) + .05, -16, 'lowpass=f=900')
# вода поднимается
ev(splash, 0, 5.6, T(33) - .2, -14, 'lowpass=f=1800,' + fd(5.6, .4, 1.2))
ev(hit, 0, .24, T(39) - .3, -26, 'lowpass=f=500')
# напряжение: сердце
for i in range(8): ev(beat, 0, .9, T(47) + i * 1.0, -12 - (i > 4) * 2, 'lowpass=f=800')
# крик, давка, собака
ev(c('scream_01.ogg'), 0, .96, T(58) - .15, -14, 'lowpass=f=2500,aecho=0.8:0.5:100:0.35')
ev(crowd, 8, T(66) - T(57) + .8, T(57) - .3, -15, 'lowpass=f=2200,' + fd(T(66) - T(57), .5, 1.6))
for k, dt in enumerate((0, .9, 1.7, 2.8)): ev(splash, 1.0 + k, 1.0, T(62) + dt, -12, 'lowpass=f=2500')
ev(c('hurt_01.ogg'), 0, .5, T(62) + .5, -16, 'lowpass=f=2000')
ev(c('barking_01.ogg'), 0, .4, T(64) - .3, -9, 'aecho=0.8:0.5:110:0.35')
ev(c('barking_02.ogg'), 0, .46, T(64) + .3, -9, 'aecho=0.8:0.5:110:0.35')
for k in range(3): ev(c('howl.ogg'), 0, .72, T(65) + .1 + k * .75, -8, 'asetrate=44100*0.9,aresample=44100,aecho=0.8:0.6:150:0.45')
# Вера выходит в воду
ev(splash, 2, 1.4, T(66) + .15, -13, 'lowpass=f=1800,' + fd(1.4, .1, .5))
ev(steps, 0, 1.5, T(66) + .1, -17, 'lowpass=f=1200,aecho=0.8:0.7:90:0.3')
# тишина: вода шумит у ступеней
ev(splash, 0.5, 5.0, T(80) - .3, -19, 'lowpass=f=1000,' + fd(5.0, .6, 1.2))
# кашель
ev(c('cough_01.ogg'), 0, .43, T(86) + .05, -4, 'lowpass=f=3500')
ev(c('cough_02.ogg'), 0, .35, T(86) + .62, -5, 'lowpass=f=3500')
# «они знали, что я болен» — сердце
for i in range(4): ev(beat, 0, .9, T(91) + i * .85, -8, 'lowpass=f=900')
# свисток и тишина
ev(whistle, 0.0, 1.8, T(101) + .0, -9, 'highpass=f=500,aecho=0.8:0.7:170|330:0.5|0.3,' + fd(1.8, .02, .8))
ev(whistle, 0.1, 1.2, T(102) - .05, -19, 'highpass=f=800,aecho=0.8:0.8:260|500:0.5|0.35,' + fd(1.2, .1, .8))
# одеяло шевелится
ev(creak, 0.5, 2.0, T(118), -15, 'lowpass=f=1000,asetrate=44100*0.6,aresample=44100,' + fd(2.0, .3, .7))
ev(c('breath.ogg'), 0, .67, T(119) + .4, -14, 'lowpass=f=1500,aecho=0.8:0.6:120:0.35')
ev(c('breath.ogg'), 0, .67, T(120) + .5, -16, 'lowpass=f=1500,aecho=0.8:0.6:120:0.35')
# Аня
ev(hit, 0, .24, T(129) - .1, -17, 'lowpass=f=600,aecho=0.8:0.8:240:0.4')
ev(creak, 3, 2.5, T(129) - .1, -12, 'lowpass=f=900,asetrate=44100*0.6,aresample=44100,' + fd(2.5, .2, 1.5))
ev(beat, 0, .9, T(129) + .3, -6, 'lowpass=f=700'); ev(beat, 0, .9, T(129) + 1.2, -7, 'lowpass=f=700')

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
