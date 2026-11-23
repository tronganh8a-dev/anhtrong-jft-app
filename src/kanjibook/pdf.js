// node pdf.js in.html out.pdf [thư mục ảnh trang]
const {chromium}=require('playwright');
(async()=>{const [i,o,png]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:794,height:1123}});
await p.goto('file://'+i);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
await p.pdf({path:o,format:'A4',printBackground:true,preferCSSPageSize:true});
if(png){const n=await p.$$eval('section.pg',a=>a.length);for(let k=0;k<n;k++){const el=(await p.$$('section.pg'))[k];await el.screenshot({path:`${png}/p${String(k+1).padStart(2,'0')}.png`})}}
await b.close()})();
