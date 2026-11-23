// node pdf.js in.html out.pdf [thư mục ảnh trang] [danh sách trang, vd 1,5,9-12]
const {chromium}=require('playwright');
(async()=>{const [i,o,png,sel]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:794,height:1123}});
await p.goto('file://'+i,{timeout:0});await p.evaluate(()=>document.fonts.ready);
if(await p.$('script'))await p.waitForSelector('body[data-ok]',{timeout:600000}).catch(()=>{});
await p.waitForTimeout(800);
const over=await p.evaluate(()=>window.__over||[]);const n=await p.$$eval('section.pg',a=>a.length);
console.log('trang:',n,'tràn:',over.join(',')||'không');
if(o!=='-')await p.pdf({path:o,format:'A4',printBackground:true,preferCSSPageSize:true,timeout:0});
if(png){let ks=[...Array(n).keys()].map(k=>k+1);
 if(sel){ks=[];for(const t of sel.split(',')){const [a,z]=t.split('-').map(Number);for(let k=a;k<=(z||a);k++)ks.push(k)}}
 const els=await p.$$('section.pg');for(const k of ks){if(els[k-1])await els[k-1].screenshot({path:`${png}/p${String(k).padStart(3,'0')}.png`})}}
await b.close()})();
