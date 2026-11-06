const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const b=await chromium.launch();fs.mkdirSync(path.resolve(__dirname,'colors'),{recursive:true});
for(const pal of [2,3])for(const v of 'ABCD'){const p=await b.newPage({viewport:{width:2560,height:1440}});p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto('file://'+path.resolve(__dirname,'brand6.html')+`?v=${v}&p=${pal}`);await p.waitForTimeout(300);await p.screenshot({path:path.resolve(__dirname,`colors/p${pal}_banner_${v}.png`)});await p.close();}
await b.close();})();
