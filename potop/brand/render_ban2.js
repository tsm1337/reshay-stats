const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();
for(let n=1;n<=6;n++){const p=await b.newPage({viewport:{width:2560,height:1440}});p.on('pageerror',e=>console.log('ERR',n,e.message));
 await p.goto('file://'+path.resolve(__dirname,'banners2.html')+`?n=${n}`);await p.waitForTimeout(400);await p.screenshot({path:path.resolve(__dirname,`banners2/banner_${n}.png`)});await p.close();}
await b.close();})();
