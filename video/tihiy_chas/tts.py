import ssl,asyncio,json,subprocess,edge_tts,edge_tts.communicate as ec
ec._SSL_CTX=ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
VOICE="ru-RU-DmitryNeural";RATE="+28%";PITCH="-4Hz"
S=["Ты на мели. До зарплаты три дня.","Незнакомец даёт тебе пять тысяч рублей.",
"Условие простое. Час не трогай телефон.","Экран заблокирован.",
"Таймер пошёл.","Сообщения летят. Лена. Банк. Работа. Курьер.",
"Тебе нужны эти деньги.","И вдруг. Мама. Позвони срочно.",
"Она никогда так не писала.","Осталось сорок минут.",
"Первое. Забрать пять тысяч.","Второе. Позвонить маме.",
"Что бы ты сделал?","Один или два?"]
async def one(s):
    for a in range(60):
        try:
            au=b"";w=[]
            async for x in edge_tts.Communicate(s,VOICE,rate=RATE,pitch=PITCH,boundary="WordBoundary").stream():
                if x["type"]=="audio": au+=x["data"]
                elif x["type"]=="WordBoundary": w.append((x["offset"]/1e7,x["duration"]/1e7,x["text"]))
            if au: return au,w
        except Exception: pass
        await asyncio.sleep(0.5)
    raise SystemExit("fail: "+s)
async def m():
    words=[];t0=0.0;lst=[]
    for i,s in enumerate(S):
        import os
        if os.path.exists(f"s{i}.json"):
            w=[tuple(x) for x in json.load(open(f"s{i}.json"))]
        else:
            au,w=await one(s)
            open(f"s{i}.mp3","wb").write(au); json.dump(w,open(f"s{i}.json","w"))
        subprocess.run(["ffmpeg","-y","-v","error","-i",f"s{i}.mp3","-ar","44100","-ac","1",f"s{i}.wav"],check=True)
        d=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"s{i}.wav"]))
        for o,du,tx in w: words.append({"t":t0+o,"d":du,"w":tx,"s":i})
        lst.append((i,t0,d)); t0+=d+(0.18 if i not in (4,) else 0.1)
    # concat with gaps
    fl=[];cx=[]
    for i,st,d in lst:
        fl+=["-i",f"s{i}.wav"]
    f="".join(f"[{i}]adelay={int(st*1000)}[a{i}];" for i,st,d in lst)+"".join(f"[a{i}]" for i,_,_ in lst)+f"amix=inputs={len(lst)}:normalize=0[o]"
    subprocess.run(["ffmpeg","-y","-v","error",*fl,"-filter_complex",f,"-map","[o]","voice.wav"],check=True)
    json.dump({"words":words,"sent":lst,"total":t0},open("words.json","w"),ensure_ascii=False)
    for i,x in enumerate(words): print(i,round(x["t"],2),x["w"],x["s"])
    print("total",t0)
asyncio.run(m())
