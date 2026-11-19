const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();const p=await b.newPage();
const [F,OUT]=process.argv.slice(2);await p.goto('file:///home/claude/anhtrong-jft-app/public/tailieu/'+F);await p.waitForTimeout(500);
const r=await p.evaluate(()=>{const T=e=>e?e.innerText.replace(/\s+\n/g,'\n').trim():'';const H=e=>e?e.innerHTML:'';
return [...document.querySelectorAll('.slide')].map((s,i)=>{const o={i:i+1,h2:T(s.querySelector('h2:not(.q)'))};
 if(s.classList.contains('dark')){o.t='cover';const c=s.querySelector('.cover');o.txt=[...c.querySelectorAll('.kk,h1,p')].map(x=>x.textContent.trim()).join('\n');return o}
 if(s.querySelector('.sec')){o.t='sec';o.txt=T(s.querySelector('.sec .t'));o.d=T(s.querySelector('.sec .d'));return o}
 if(s.querySelector('.spd')){o.t='speed';return o}
 if(s.querySelector('.clw')){o.t='cloud';o.w=[...s.querySelectorAll('.cw')].map(T);return o}
 if(s.querySelector('.ptc')){o.t='ptc';o.items=[...s.querySelectorAll('.ptc button')].map(b=>({q:b.cloneNode(true),}))&&[...s.querySelectorAll('.ptc button')].map(b=>{const c=b.cloneNode(true);c.querySelectorAll('rt').forEach(x=>x.remove());const a=c.querySelector('.bl span').textContent;c.querySelector('.bl').textContent='（　）';const vi=c.querySelector('small').textContent;c.querySelector('small').remove();return {q:c.textContent,a,vi}});return o}
 if(s.querySelector('.ord')){o.t='ord';const c=s.querySelector('.sol').cloneNode(true);c.querySelectorAll('rt').forEach(x=>x.remove());o.sol=c.textContent;o.vi=T(s.querySelector('.ord .vi'));o.ch=[...s.querySelectorAll('.chk')].sort((a,b)=>a.dataset.i-b.dataset.i).map(x=>{const y=x.cloneNode(true);y.querySelectorAll('rt').forEach(z=>z.remove());return y.textContent});return o}
 if(s.querySelector('.gx')){o.t='gx';o.no=T(s.querySelector('.gxp .no'));return o}
 if(s.querySelector('.plan')){o.t='plan';o.items=[...s.querySelectorAll('.plan>div')].map(d=>[...d.children].map(c=>c.textContent.trim()).join(' · '));return o}
 if(s.querySelector('.rk')){o.t='skill';o.items=[...s.querySelectorAll('.rk>div')].map(d=>{const c=d.cloneNode(true);c.querySelectorAll('rt').forEach(x=>x.remove());return c.innerText.replace(/\s+/g,' ').trim()});const pb=s.querySelector('.pb');if(pb){const c=pb.cloneNode(true);c.querySelectorAll('rt').forEach(x=>x.remove());o.pb=c.innerText}return o}
 if(s.querySelector('.rdq')&&!s.classList.contains('qz')){o.t='demo';o.items=[...s.querySelectorAll('.exl')].map(d=>{const c=d.cloneNode(true);c.querySelectorAll('rt').forEach(x=>x.remove());return c.innerText.replace(/\s+/g,' ').trim()});return o}
 if(s.classList.contains('qz')){o.t=s.classList.contains('rd')?'read':s.classList.contains('ls')?'listen':'quiz';o.src=T(s.querySelector('.kk2'));const q=s.querySelector('h2.q').cloneNode(true);q.querySelectorAll('rt').forEach(x=>x.remove());o.q=q.innerText.trim();
   o.opts=[...s.querySelectorAll('.o')].map(b=>{const y=b.querySelector('.ot').cloneNode(true);y.querySelectorAll('rt').forEach(z=>z.remove());return y.textContent.trim()});o.a=s.querySelector('.opts').dataset.a;
   const e=s.querySelector('.ex').cloneNode(true);o.exh=e.innerHTML;e.querySelectorAll('rt').forEach(x=>x.remove());o.ex=e.innerText.trim();o.big=T(s.querySelector('.qbig'));return o}
 if(s.querySelector('.vg')){o.t='vocab';o.w=[...s.querySelectorAll('.kv')].map(k=>{const w=k.querySelector('.w').cloneNode(true);w.querySelectorAll('rt').forEach(x=>x.remove());return w.textContent});return o}
 if(s.querySelector('.kd')){o.t='kanji';o.w=T(s.querySelector('.kdw'));return o}
 if(s.querySelector('.kg')){o.t='kgrid';o.w=[...s.querySelectorAll('.kc .k')].map(T);return o}
 if(s.querySelector('.gp')){o.t='gram';o.no=[...s.querySelectorAll('.gpi .no')].map(T);return o}
 if(s.querySelector('.tb2')){o.t='table';const t=s.querySelector('.tb2').cloneNode(true);t.querySelectorAll('rt').forEach(x=>x.remove());o.rows=[...t.querySelectorAll('tr')].map(r=>[...r.children].map(c=>c.innerText.trim()));const pb=s.querySelector('.pb');if(pb){const c=pb.cloneNode(true);c.querySelectorAll('rt').forEach(x=>x.remove());o.pb=c.innerText}return o}
 o.t='other';o.txt=T(s).slice(0,300);return o})});
fs.writeFileSync(OUT,JSON.stringify(r,null,0));const c={};r.forEach(x=>c[x.t]=(c[x.t]||0)+1);console.log(c);await b.close()})();
