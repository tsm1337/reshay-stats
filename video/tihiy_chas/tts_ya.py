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
def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
words=[];lst=[];t0=0.0;parts=[]
for i,s in enumerate(S):
    sd=t0
    for j,p in enumerate([x.strip() for x in re.split(r'(?<=[.?!])\s+',s) if x.strip()]):
        mp=f"p{i}_{j}.mp3";wv=f"p{i}_{j}.wav"
        if not os.path.exists(mp): syn(p,mp)
        subprocess.run(["ffmpeg","-y","-v","error","-i",mp,"-ar","44100","-ac","1","-af","silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=1:stop_duration=0.05:stop_threshold=-45dB",wv],check=True)
        d=dur(wv);ws=p.split();wt=[len(re.sub(r'\W','',w))+0.6 for w in ws];tot=sum(wt);c=t0
        for w,x in zip(ws,wt):
            dd=d*x/tot;words.append({"t":c,"d":dd,"w":w,"s":i});c+=dd
        parts.append((wv,t0));t0+=d+0.22
    lst.append((i,sd,t0-sd-0.22));t0+=(0.45 if i not in (4,) else 0.25)
fl=[];f=""
for k,(wv,st) in enumerate(parts):
    fl+=["-i",wv];f+=f"[{k}]adelay={int(st*1000)}[a{k}];"
f+="".join(f"[a{k}]" for k in range(len(parts)))+f"amix=inputs={len(parts)}:normalize=0[o]"
subprocess.run(["ffmpeg","-y","-v","error",*fl,"-filter_complex",f,"-map","[o]","voice.wav"],check=True)
json.dump({"words":words,"sent":lst,"total":t0},open("words.json","w"),ensure_ascii=False)
print("total",t0,"parts",len(parts))
