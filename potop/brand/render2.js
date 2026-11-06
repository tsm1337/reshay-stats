const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const b=await chromium.launch();fs.mkdirSync(path.resolve(__dirname,'variants'),{recursive:true});
for(const v of [1,2,3])for(const [m,w,h] of [['avatar',800,800],['banner',2560,1440]]){
 const p=await b.newPage({viewport:{width:w,height:h}});p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto('file://'+path.resolve(__dirname,'brand2.html')+`?v=${v}&m=${m}`);await p.waitForTimeout(200);
 await p.screenshot({path:path.resolve(__dirname,`variants/v${v}_${m==='avatar'?'avatar':'banner'}.png`)});}
await b.close();})();
