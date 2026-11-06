const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();
for(const [m,w,h,out] of [['avatar',800,800,'avatar.png'],['banner',2560,1440,'banner_youtube.png']]){
 const p=await b.newPage({viewport:{width:w,height:h}});p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto('file://'+path.resolve(__dirname,'brand.html')+'?m='+m);await p.waitForTimeout(300);
 await p.screenshot({path:path.resolve(__dirname,out)});}
await b.close();})();
