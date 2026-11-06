# Yandex SpeechKit v3, voice anton. Ключ подставляет прокси (в коде его нет).
import json,base64,subprocess,os,re,time,urllib.request
VOICE="anton";SPEED=0.95
S=["Ты на мели. До зарплаты три дня. Холодильник пуст.","Незнакомец даёт тебе пять тысяч рублей. Прямо сейчас, наличными.",
"Условие простое. Час не трогай телефон.","Экран заблокирован. Открыть нельзя.",
"Таймер пошёл.","Сообщения летят. Лена. Банк. Работа. Курьер.",
"Тебе нужны эти деньги. Очень нужны.","И вдруг. Мама. Позвони срочно.",
"Она никогда так не писала. Что-то случилось?","Осталось сорок минут. Ты ещё держишься.",
"Первое. Забрать пять тысяч.","Второе. Позвонить маме.",
"Что бы ты сделал?","Один или два?"]
def syn(text,out):
    body=json.dumps({"text":text,"hints":[{"voice":VOICE},{"speed":SPEED}],"outputAudioSpec":{"containerAudio":{"containerAudioType":"MP3"}}}).encode()
    for a in range(8):
        try:
            r=urllib.request.Request("https://tts.api.cloud.yandex.net/tts/v3/utteranceSynthesis",body,{"Content-Type":"application/json"})
            au=b""
            for l in urllib.request.urlopen(r,timeout=60).read().decode().splitlines():
                if l.strip(): au+=base64.b64decode(json.loads(l).get("result",{}).get("audioChunk",{}).get("data",""))
            if au: open(out,"wb").write(au);return
        except Exception as e: err=e
        time.sleep(1)
    raise SystemExit(f"fail {text}: {err}")
import difflib
from faster_whisper import WhisperModel
WM=WhisperModel('small',device='cpu',compute_type='int8')
norm=lambda w:re.sub(r'[^а-яёa-z0-9]','',w.lower().replace('ё','е'))
def align(wv,ws,d):
    import numpy as np
    raw=subprocess.check_output(["ffmpeg","-v","error","-i",wv,"-ar","16000","-ac","1","-f","f32le","-"])
    segs,_=WM.transcribe(np.frombuffer(raw,dtype=np.float32),language='ru',word_timestamps=True,beam_size=5)
    ww=[(norm(w.word),w.start,w.end) for sg in segs for w in sg.words]
    sw=[norm(w) for w in ws]
    sm=difflib.SequenceMatcher(None,sw,[x[0] for x in ww],autojunk=False)
    res=[None]*len(ws)
    for i,j,n in sm.get_matching_blocks():
        for k in range(n): res[i+k]=(ww[j+k][1],ww[j+k][2])
    # fill gaps: interpolate between known neighbours
    i=0
    while i<len(res):
        if res[i] is None:
            j=i
            while j<len(res) and res[j] is None: j+=1
            a=res[i-1][1] if i>0 else 0.0
            b=res[j][0] if j<len(res) else d
            n=j-i
            for k in range(n): res[i+k]=(a+(b-a)*k/n,a+(b-a)*(k+1)/n)
            i=j
        else: i+=1
    return res,sum(r is not None for r in res)
def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
words=[];lst=[];t0=0.0;parts=[]
for i,s in enumerate(S):
    sd=t0
    for j,p in enumerate([x.strip() for x in re.split(r'(?<=[.?!])\s+',s) if x.strip()]):
        mp=f"p{i}_{j}.mp3";wv=f"p{i}_{j}.wav"
        if not os.path.exists(mp): syn(p,mp)
        subprocess.run(["ffmpeg","-y","-v","error","-i",mp,"-ar","44100","-ac","1","-af","silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",wv],check=True)
        d=dur(wv);ws=p.split()
        al,_=align(wv,ws,d)
        for w,(a,b) in zip(ws,al):
            words.append({"t":t0+a,"d":max(0.08,b-a),"w":w,"s":i})
        parts.append((wv,t0));t0+=d+0.15
    lst.append((i,sd,t0-sd-0.15));t0+=(0.3 if i not in (4,) else 0.15)
fl=[];f=""
for k,(wv,st) in enumerate(parts):
    fl+=["-i",wv];f+=f"[{k}]adelay={int(st*1000)}[a{k}];"
f+="".join(f"[a{k}]" for k in range(len(parts)))+f"amix=inputs={len(parts)}:normalize=0[o]"
subprocess.run(["ffmpeg","-y","-v","error",*fl,"-filter_complex",f,"-map","[o]","voice.wav"],check=True)
json.dump({"words":words,"sent":lst,"total":t0},open("words.json","w"),ensure_ascii=False)
print("total",t0,"parts",len(parts))
