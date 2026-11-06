const {chromium}=require('playwright');const fs=require('fs');
const data=JSON.parse(fs.readFileSync('words.json','utf8'));
const html=fs.readFileSync('scene.html','utf8').replace('__DATA__',JSON.stringify(data));
fs.writeFileSync('_scene.html',html);
const FPS=30,mode=process.argv[2];
(async()=>{
 const b=await chromium.launch();
 if(mode==='stills'){
  const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+process.cwd()+'/_scene.html');
  fs.mkdirSync('stills',{recursive:true});
  const S=data.sent.map(a=>a[1]);
  const ts=[1.0,S[1]+1.2,S[3]+1.6,S[4]+1.4,S[5]+1.0,S[7]+1.2,S[9]+1.0];
  for(const [i,t] of ts.entries()){await p.evaluate(t=>draw(t),t);await p.screenshot({path:`stills/f${i}.png`});}
 }else{
  const N=Math.ceil((data.total+0.8)*FPS),W=4;fs.mkdirSync('frames',{recursive:true});
  await Promise.all([...Array(W).keys()].map(async w=>{
   const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+process.cwd()+'/_scene.html');
   for(let f=w;f<N;f+=W){await p.evaluate(t=>draw(t),f/FPS);await p.screenshot({path:`frames/${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:92});}
  }));console.log('frames',N);
 }
 await b.close();})();
