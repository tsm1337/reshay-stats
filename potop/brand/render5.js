const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const b=await chromium.launch();fs.mkdirSync(path.resolve(__dirname,'neon2'),{recursive:true});
const jobs=[...'ABCD'].map(v=>[`v=${v}`,2560,1440,`banner_${v}.png`]).concat([1,2,3].map(a=>[`a=${a}`,800,800,`avatar_${a}.png`]));
for(const [qs,w,h,out] of jobs){const p=await b.newPage({viewport:{width:w,height:h}});p.on('pageerror',e=>console.log('ERR',qs,e.message));
 await p.goto('file://'+path.resolve(__dirname,'brand5.html')+'?'+qs);await p.waitForTimeout(300);await p.screenshot({path:path.resolve(__dirname,'neon2/'+out)});await p.close();}
await b.close();})();
