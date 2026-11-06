const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();
for(let v=4;v<=13;v++)for(const [m,w,h] of [['avatar',800,800],['banner',2560,1440]]){
 const p=await b.newPage({viewport:{width:w,height:h}});p.on('pageerror',e=>console.log('ERR',v,e.message));
 await p.goto('file://'+path.resolve(__dirname,'brand3.html')+`?v=${v}&m=${m}`);await p.waitForTimeout(150);
 await p.screenshot({path:path.resolve(__dirname,`variants/v${v}_${m}.png`)});await p.close();}
await b.close();})();
