const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();
for(const v of ['A','B','C','D'])for(const [m,w,h] of [['avatar',800,800],['banner',2560,1440]]){
 const p=await b.newPage({viewport:{width:w,height:h}});p.on('pageerror',e=>console.log('ERR',v,m,e.message));
 await p.goto('file://'+path.resolve(__dirname,'brand4.html')+`?v=${v}&m=${m}`);await p.waitForTimeout(300);
 await p.screenshot({path:path.resolve(__dirname,`neon/n${v}_${m}.png`)});await p.close();}
await b.close();})();
