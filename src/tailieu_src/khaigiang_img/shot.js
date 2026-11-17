const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:900,height:830},deviceScaleFactor:2});
await p.goto('http://localhost:8812/index.html');await p.waitForTimeout(1500);
await p.evaluate(()=>{window.newxWill=()=>false;window.newxShow=()=>{};try{unlock()}catch(e){};document.querySelectorAll('#nmodal,.newx,#newx').forEach(x=>x.remove())});
await p.waitForFunction(()=>window.EXAMS&&EXAMS.length>0,{timeout:20000}).catch(()=>{});
const picks=process.argv.slice(2);
for(const pk of picks){const [id,qi]=pk.split(':');
 await p.evaluate(([id,qi])=>{const i=EXAMS.findIndex(e=>e.id==id);startExam(i,'exam');clearInterval(tick);
  const q=+qi;S.sec=S.secs.findIndex(s=>s.idx.includes(q));S.i=q;render();document.querySelectorAll('audio').forEach(a=>a.pause());[...document.querySelectorAll('#cbt *')].filter(x=>/^\s*Nguồn: Đề/.test(x.textContent)&&x.textContent.length<40).forEach(x=>x.style.display='none');var tm=document.getElementById('timer');if(tm)tm.textContent='00:15:00'},[id,qi]);
 await p.waitForTimeout(900);
 await p.addStyleTag({content:'#aiFab,#penFab,.vi-q{display:none!important}'});
 await p.screenshot({path:`/tmp/kgs/${id}_${qi}.jpg`,type:'jpeg',quality:90});}
await b.close()})();
