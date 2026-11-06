const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();
for(let n=1;n<=10;n++){const p=await b.newPage({viewport:{width:800,height:800}});p.on('pageerror',e=>console.log('ERR',n,e.message));
 await p.goto('file://'+path.resolve(__dirname,'avatars.html')+`?n=${n}`);await p.waitForTimeout(150);await p.screenshot({path:path.resolve(__dirname,`avatars/avatar_${n}.png`)});await p.close();}
await b.close();})();
