"""Slide 2 buổi tổng ôn いろどり 入門 (17/11/2026) — mỗi buổi 90 phút: Từ vựng · Chữ Hán · Ngữ pháp · Luyện tập.
Buổi 1 = 入門 Bài 1–9 (cơ bản), Buổi 2 = 入門 Bài 10–18.
Dữ liệu: DOCS (từ vựng + chữ Hán, tài liệu tổng hợp lớp cô Quỳnh, nguồn いろどり 入門) và GRAMMAR (文法ノート いろどり 入門:
mẫu câu, câu ví dụ, câu luyện tập). Bảng tổng hợp + lưu ý ngắn là tự soạn.
Chạy: python3 src/tailieu_src/tongon_nhapmon_build.py → public/tailieu/Buoi01_TongOn_NhapMon_1.html, Buoi02_TongOn_NhapMon_2.html"""
import re, html, sys, json, io, base64, subprocess
sys.path.insert(0, '/home/claude/anhtrong-jft-app/src/jft')
from furi import furi
from PIL import Image
R = '/home/claude/anhtrong-jft-app/'
exec(open(R + 'src/tailieu_src/_head_snip.py').read())  # HEAD, LOGO
_kg = open(R + 'src/tailieu_src/khaigiang_build.py').read()
KGCSS = _kg[_kg.index("HEAD = HEAD.replace('</style></head>', '''") + 41:_kg.index("</style></head>''', 1)")]
CSS = KGCSS + '''
.slide h2:not(.q){display:flex;align-items:baseline;gap:16px}
.bt{display:inline-block;background:#0d5a8c;color:#fff;border-radius:12px;padding:2px 14px;font-size:24px;font-weight:800;margin-right:4px;vertical-align:middle}
.jpt{font-family:"Klee One",serif;font-weight:600}
/* từ vựng */
.vg{display:grid;grid-template-columns:repeat(5,1fr);gap:18px;margin-top:4px}
.kc.kv{padding:12px 12px 10px;border-top-width:6px;border-color:#0d5a8c}.kc.kv:nth-child(5n+2){border-color:#c42f66}.kc.kv:nth-child(5n+3){border-color:#f2a93b}.kc.kv:nth-child(5n+4){border-color:#5a9e2f}.kc.kv:nth-child(5n+5){border-color:#7a4fb5}
.kv img{width:100%;height:150px;object-fit:contain;display:block;margin:0 auto 6px}
.kv .w{font-family:"Klee One",serif;font-weight:600;font-size:34px;line-height:1.5;color:#0d2b40;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.kv .w rt{font-size:.5em}
.kv .w.sm{font-size:26px}
.kv.noimg{display:flex;flex-direction:column;justify-content:center;min-height:220px}.kv.noimg .w{font-size:40px;white-space:normal}.kv.noimg .w.sm{font-size:32px}
.kv .m{font-size:22px;color:#c42f66;font-weight:700;line-height:1.3;min-height:29px}
/* chữ Hán */
.kg{margin-top:6px}.kc .k{font-size:var(--ks,120px)}
.kc .hv{font-size:34px!important}.kc .rd{font-size:32px!important}.kc .mn{font-size:27px!important}
.kc .ex2{font-size:25px;margin-top:8px;background:#f6f8fb;border-radius:12px;padding:8px;line-height:1.7;text-align:left}.kc .ex2 rt{font-size:.5em}.kc .ex2 small{font-family:Quicksand,sans-serif;font-weight:600;display:block;color:#47647a;font-size:22px;line-height:1.35}
.kc .cs{font-size:21px;color:#47647a;margin-top:6px;line-height:1.4}.kc .cs b{color:#0d5a8c;font-family:"Klee One",serif;font-size:26px}
/* ngữ pháp */
.gp{display:grid;gap:18px}
.gpi{background:#fff;border-radius:20px;box-shadow:0 8px 24px #0d2b4012;padding:20px 28px;display:grid;grid-template-columns:600px 1fr;gap:26px;align-items:center;border-left:10px solid #0d5a8c}
.gpi:nth-child(2){border-color:#c42f66}.gpi:nth-child(3){border-color:#f2a93b}.gpi:nth-child(4){border-color:#5a9e2f}
.gpi .pt{font-family:"Klee One",serif;font-weight:600;font-size:46px;line-height:1.55;color:#0d2b40}.gpi .pt rt{font-size:.45em}
.gpi .pt .no{color:#c42f66;margin-right:6px}
.gpi .mv{font-size:29px;color:#0d5a8c;font-weight:700;margin-top:4px;line-height:1.35}
.gpi .eg{font-size:40px;line-height:1.65}.gpi .eg .jpt rt{font-size:.45em}.gpi .eg .vi{font-size:28px;color:#47647a;line-height:1.35;margin-bottom:6px}
.gpi .nt{font-size:25px;color:#8a5a00;background:#fff8e6;border-radius:10px;padding:6px 12px;margin-top:6px;line-height:1.4}
.gp{margin-top:6px;min-height:640px;grid-auto-rows:1fr}.gp.n2{gap:28px}.gp.n2 .gpi{padding:34px 34px}.gp.n2 .gpi .pt{font-size:44px}.gp.n2 .gpi .eg{font-size:36px}
/* bảng */
.tb2{width:100%;border-collapse:separate;border-spacing:0;font-size:32px;background:#fff;border-radius:20px;overflow:hidden;box-shadow:0 8px 24px #0d2b4012}
.tb2 th{background:#0d5a8c;color:#fff;padding:16px 22px;font-size:28px;text-align:left}
.tb2 td{padding:14px 22px;border-bottom:2px solid #eef3f8;line-height:1.5}.tb2 td.h{font-weight:800;color:#0d5a8c;background:#f4f9fe}
.tb2 .jpt{font-size:33px}.tb2 rt{font-size:.45em}.tb2 em{font-style:normal;color:#c42f66;font-weight:800}
/* chia phần */
.sec{display:flex;flex-direction:column;justify-content:center;height:100%;padding-left:40px}
.sec .n{font-size:60px;font-weight:800;line-height:1;color:#fff;background:#0d5a8c;border-radius:20px;padding:10px 22px;align-self:flex-start}
.sec .t{font-size:110px;font-weight:800;color:#0d2b40;margin-top:20px}
.sec .j{font-family:"Klee One",serif;font-weight:600;font-size:52px;color:#c42f66;margin-top:8px}
.sec .d{font-size:32px;color:#2f5674;margin-top:22px}
.sec .tm{display:inline-block;margin-top:26px;background:#fff;border-radius:99px;padding:10px 26px;font-size:28px;font-weight:800;color:#0d5a8c;box-shadow:0 6px 18px #0d5a8c22}
.plan{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin-top:10px}
.plan>div{background:#fff;border-radius:22px;padding:26px;box-shadow:0 8px 24px #0d2b4012;border-top:10px solid #0d5a8c}
.plan>div:nth-child(2){border-color:#c42f66}.plan>div:nth-child(3){border-color:#f2a93b}.plan>div:nth-child(4){border-color:#5a9e2f}
.plan b{font-size:50px;color:#0d5a8c}.plan>div:nth-child(2) b{color:#c42f66}.plan>div:nth-child(3) b{color:#d98a17}.plan>div:nth-child(4) b{color:#4f8a25}
.plan h3{font-size:34px;margin:8px 0}.plan p{font-size:25px;color:#47647a;line-height:1.5}
/* quiz có ảnh */
.qi{display:grid;grid-template-columns:420px 1fr;gap:40px;align-items:center}.qi img{width:100%;max-height:420px;object-fit:contain;background:#fff;border-radius:22px;padding:16px;box-shadow:0 8px 24px #0d2b4012}
.qbig{font-family:"Klee One",serif;font-weight:600;font-size:96px;text-align:center;background:#fff;border-radius:22px;padding:40px 10px;box-shadow:0 8px 24px #0d2b4012}
.q,.ot{font-family:Quicksand,"Klee One","M PLUS Rounded 1c",sans-serif!important;font-weight:700}
.kg.c7{grid-template-columns:repeat(7,1fr);gap:16px}.kg.c7 .kc{padding:18px 8px}.kg.c7 .kc .k{font-size:64px!important;writing-mode:vertical-rl;margin:0 auto;height:230px}
.lsn{margin:-6px 0 18px}.lsn audio{width:640px;height:54px}
.ls .q .vi-q{display:block;font-size:24px;color:#47647a;font-weight:600;line-height:1.4}
.opts.oimg{grid-template-columns:repeat(3,1fr);gap:22px}.opts.oimg .o{height:auto;flex-direction:column;padding:14px;gap:8px}.opts.oimg .o img{width:100%;height:200px;object-fit:contain;position:relative;z-index:1}
.opts.oimg .o b{position:absolute;left:14px;top:10px;z-index:2}
.lpic{width:100%;max-height:430px;object-fit:contain;background:#fff;border-radius:18px;padding:10px;box-shadow:0 8px 24px #0d2b4012}
.lex.on{display:none}.lex.on.open{display:block}
.lsb{position:absolute;right:60px;top:40px;border:0;border-radius:99px;background:#0d5a8c;color:#fff;font:700 24px Quicksand,sans-serif;padding:10px 24px;cursor:pointer;z-index:6;display:none}.ls .ex.on~.lsb{display:block}
.ls .qi{grid-template-columns:720px 1fr}.ls .lpic{max-height:520px}
.lex{position:absolute;right:60px;top:120px;width:640px;max-height:640px;overflow:auto;font-size:24px!important;line-height:1.55!important;z-index:5;box-shadow:0 16px 40px #0d2b4030}
.lex .ans{font-weight:800;color:#2f9e5b;margin-bottom:8px}.lex .lb{display:block;font-size:18px;font-weight:800;color:#c42f66;margin:10px 0 4px;letter-spacing:1px}.lex p{margin:0}.lex .v,.lex .vi{color:#47647a;font-size:20px;margin-bottom:6px}.lex rt{font-size:.5em}
.kd{display:grid;grid-template-columns:640px 1fr;gap:44px;align-items:start;margin-top:4px}
.kdl{display:flex;flex-direction:column;align-items:center;gap:12px}.kdl .kvr{border:0;border-radius:99px;background:#fff;color:#0d5a8c;font:700 22px Quicksand,sans-serif;padding:8px 22px;cursor:pointer;box-shadow:0 4px 12px #0d5a8c22;margin:0 4px}
.kdl .kvr+.kvr{margin-top:-4px}
.kvi{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}.kvi .cell{width:var(--cw,250px);height:var(--cw,250px);background:#fff;border-radius:22px;position:relative;box-shadow:0 10px 30px #0d2b4018}
.kvi .cell:before,.kvi .cell:after{content:'';position:absolute;border:0 dashed #e8b4c6}.kvi .cell:before{left:50%;top:6%;bottom:6%;border-left-width:2px}.kvi .cell:after{top:50%;left:6%;right:6%;border-top-width:2px}
.kvi svg{position:absolute;inset:0;width:100%;height:100%}.kvi .g path{stroke:#e3ebf2}.kvi .d path{stroke:#0d2b40}.kvi .d path.cur{stroke:#c42f66}.kvi text{font:700 7px Quicksand,sans-serif;fill:#c42f66}
.kdh{display:flex;align-items:baseline;gap:24px}.kdw{font-family:"Klee One",serif;font-weight:600;font-size:110px;line-height:1.1;color:#0d2b40}.kdv{font-size:40px;font-weight:800;color:#c42f66;letter-spacing:1px}
.kdm{font-size:42px;font-weight:700;margin:6px 0 18px}.kdm .jp{color:#0d5a8c;font-family:"Klee One",serif}
.kdt{border-collapse:separate;border-spacing:0;width:100%;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 6px 18px #0d2b4010;font-size:30px}
.kdt th{background:#0d5a8c;color:#fff;font-size:22px;padding:10px 16px;text-align:left}.kdt td{padding:14px 16px;border-bottom:2px solid #eef3f8;font-family:Quicksand,"Klee One",sans-serif;font-weight:600}
.kdt .kk{font-family:"Klee One",serif;font-size:54px;line-height:1;color:#0d2b40}.kdt .hh{color:#c42f66;font-weight:800}.kdt .mm{color:#47647a}
.kdn{margin-top:14px;background:#fff8e6;border-left:8px solid #f2a93b;border-radius:12px;padding:14px 20px;font-size:29px;line-height:1.5}.kdn b{color:#c47a00;margin-right:8px}
.kde{margin-top:14px;background:#fff;border-radius:14px;padding:14px 20px;font-size:36px;line-height:1.8;box-shadow:0 6px 18px #0d2b4010}.kde rt{font-size:.5em}.kde small{display:block;font-size:26px;color:#47647a;line-height:1.4}
.kdt{font-size:25px!important}.kdt td{padding:8px 12px!important}.kdt .kk{font-size:44px!important}.kdw{font-size:84px!important}.kdv{font-size:32px!important}.kdm{font-size:32px!important;margin:2px 0 10px!important}.kdh{margin-top:-8px}
.kdn{font-size:23px!important;padding:8px 14px!important;margin-top:8px!important}.kde{font-size:28px!important;padding:6px 14px!important;margin-top:8px!important;line-height:1.55!important}.kde small{font-size:21px!important}
.krel{margin-top:10px;background:#fff;border-radius:16px;padding:8px 12px;box-shadow:0 6px 18px #0d2b4010;width:100%;display:grid;grid-template-columns:1fr 1fr;gap:2px 12px}.krel b{grid-column:1/-1;color:#c42f66;font-size:19px}
.krel div{line-height:1.25;padding:3px 0;border-top:1px dashed #e3ebf2}.krel .jp{font-family:"Klee One",serif;font-weight:600;font-size:28px;margin-right:6px}.krel i{font-style:normal;color:#0d5a8c;font-weight:700;font-size:18px}.krel small{display:block;color:#47647a;font-size:17px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ck{font-size:28px!important;line-height:1.6!important}
.ck{list-style:none;font-size:31px;line-height:1.8}.ck li:before{content:"✓";color:#5a9e2f;font-weight:800;margin-right:14px}
'''
TAIL = open(R + 'src/tailieu_src/buoi15_tail.html').read()
# Nét viết chữ Hán: KanjiVG (CC BY-SA 3.0, http://kanjivg.tagaini.net) — dữ liệu nét đã rút gọn ở src/tailieu_src/kanjivg_strokes.json
KVG = json.load(open(R + 'src/tailieu_src/kanjivg_strokes.json'))
KVGCSS = '''
.kw{position:absolute;right:10px;top:10px;border:0;background:#eef5fc;color:#0d5a8c;border-radius:12px;font:700 20px Quicksand,sans-serif;padding:6px 12px;cursor:pointer;z-index:2}.kw:hover{background:#0d5a8c;color:#fff}.kc{position:relative}
#kvo{position:fixed;inset:0;z-index:60;background:#0d2b40cc;display:none;align-items:center;justify-content:center;flex-direction:column;gap:24px}#kvo.on{display:flex}
#kvo .bx{display:flex;gap:28px}#kvo .cell{width:min(40vh,40vw);height:min(40vh,40vw);background:#fff;border-radius:24px;position:relative;box-shadow:0 20px 50px #0008}
#kvo .cell:before,#kvo .cell:after{content:'';position:absolute;border:0 dashed #e8b4c6}#kvo .cell:before{left:50%;top:6%;bottom:6%;border-left-width:2px}#kvo .cell:after{top:50%;left:6%;right:6%;border-top-width:2px}
#kvo svg{position:absolute;inset:0;width:100%;height:100%}#kvo .g path{stroke:#e3ebf2}#kvo .d path{stroke:#0d2b40}#kvo .d path.cur{stroke:#c42f66}#kvo text{font:600 6px Quicksand,sans-serif;fill:#c42f66}
#kvo .ct{display:flex;gap:14px}#kvo .ct button{border:0;border-radius:99px;padding:12px 26px;font:700 24px Quicksand,sans-serif;cursor:pointer;background:#fff;color:#0d2b40}#kvo .ct button.p{background:#c42f66;color:#fff}
#kvo .cap{color:#fff;font:700 28px Quicksand,sans-serif}#kvo .src2{color:#9fb6c8;font:500 16px Quicksand,sans-serif}
'''
VSTEP = '''<script>(()=>{const _st=step;step=function(){const s=S[cur];if(s&&s.querySelector('.vg')){for(const k of ['g1','g2']){const xs=s.querySelectorAll('.st.'+k+':not(.sh)');if(xs.length){xs.forEach(x=>x.classList.add('sh'));return}}}_st()};
document.querySelectorAll('.kv').forEach(c=>c.onclick=e=>{e.stopPropagation();const x=c.querySelector('.st:not(.sh)');x&&x.classList.add('sh')});})();</script>'''
KVGJS = '''<div id="kvo"><div class="cap"></div><div class="bx"></div><div class="ct"><button class="p" data-a="re">▶ Viết lại</button><button data-a="sl">Chậm</button><button data-a="fa">Nhanh</button><button data-a="x">✕ Đóng</button></div><div class="src2">Nét viết: KanjiVG (CC BY-SA 3.0)</div></div>
<script>window.kvDrawIn=(BX,W,sp,tm)=>{const NS='http://www.w3.org/2000/svg';tm.forEach(clearTimeout);tm.length=0;BX.innerHTML='';let t=250;const cs=[...W].filter(c=>KVG[c]);BX.style.setProperty('--cw',(cs.length>2?190:cs.length>1?255:330)+'px');
 cs.forEach(c=>{const d=KVG[c],cell=document.createElement('div');cell.className='cell';const sv=document.createElementNS(NS,'svg');sv.setAttribute('viewBox','0 0 109 109');
  const g=document.createElementNS(NS,'g'),dd=document.createElementNS(NS,'g'),tx=document.createElementNS(NS,'g');g.setAttribute('class','g');dd.setAttribute('class','d');
  [g,dd].forEach(x=>{x.setAttribute('fill','none');x.setAttribute('stroke-width','4');x.setAttribute('stroke-linecap','round');x.setAttribute('stroke-linejoin','round')});
  sv.append(g,dd,tx);cell.append(sv);BX.append(cell);
  d.p.forEach((pd,i)=>{const a=document.createElementNS(NS,'path');a.setAttribute('d',pd);g.append(a);const b=document.createElementNS(NS,'path');b.setAttribute('d',pd);dd.append(b);
   const L=b.getTotalLength();b.style.strokeDasharray=L;b.style.strokeDashoffset=L;const dur=(250+L*9)/sp;
   tm.push(setTimeout(()=>{dd.querySelectorAll('.cur').forEach(x=>x.classList.remove('cur'));b.classList.add('cur');b.style.transition='stroke-dashoffset '+dur+'ms linear';b.style.strokeDashoffset=0;
     const n=d.n[i];if(n){const e=document.createElementNS(NS,'text');e.setAttribute('x',n[0]);e.setAttribute('y',n[1]);e.textContent=i+1;tx.append(e)}},t));t+=dur+180/sp});
  tm.push(setTimeout(()=>dd.querySelectorAll('.cur').forEach(x=>x.classList.remove('cur')),t));t+=350/sp});};
window.kvPlay=(el,sp)=>{el._tm=el._tm||[];kvDrawIn(el,el.dataset.w,sp||1,el._tm)};
new MutationObserver(ms=>ms.forEach(m=>{const s=m.target;if(s.classList&&s.classList.contains('on')&&!m.oldValue?.includes(' on')){s.querySelectorAll('.kvi').forEach(e=>kvPlay(e,1))}})).observe(document.getElementById('stage'),{subtree:true,attributes:true,attributeFilter:['class'],attributeOldValue:true});
(()=>{const O=document.getElementById('kvo'),BX=O.querySelector('.bx'),NS='http://www.w3.org/2000/svg';let W='',sp=1,tm=[];
function draw(){tm.forEach(clearTimeout);tm=[];BX.innerHTML='';let t=200;
 [...W].filter(c=>KVG[c]).forEach(c=>{const d=KVG[c],cell=document.createElement('div');cell.className='cell';const sv=document.createElementNS(NS,'svg');sv.setAttribute('viewBox','0 0 109 109');
  const g=document.createElementNS(NS,'g'),dd=document.createElementNS(NS,'g'),tx=document.createElementNS(NS,'g');g.setAttribute('class','g');dd.setAttribute('class','d');
  [g,dd].forEach(x=>{x.setAttribute('fill','none');x.setAttribute('stroke-width','4');x.setAttribute('stroke-linecap','round');x.setAttribute('stroke-linejoin','round')});
  sv.append(g,dd,tx);cell.append(sv);BX.append(cell);
  d.p.forEach((pd,i)=>{const a=document.createElementNS(NS,'path');a.setAttribute('d',pd);g.append(a);const b=document.createElementNS(NS,'path');b.setAttribute('d',pd);dd.append(b);
   const L=b.getTotalLength();b.style.strokeDasharray=L;b.style.strokeDashoffset=L;const dur=(250+L*9)/sp;
   tm.push(setTimeout(()=>{dd.querySelectorAll('.cur').forEach(x=>x.classList.remove('cur'));b.classList.add('cur');b.style.transition='stroke-dashoffset '+dur+'ms linear';b.style.strokeDashoffset=0;
     const n=d.n[i];if(n){const e=document.createElementNS(NS,'text');e.setAttribute('x',n[0]);e.setAttribute('y',n[1]);e.textContent=i+1;tx.append(e)}},t));t+=dur+180/sp});
  tm.push(setTimeout(()=>dd.querySelectorAll('.cur').forEach(x=>x.classList.remove('cur')),t));t+=350/sp});}
window.kvOpen=(w,cap)=>{W=w;O.querySelector('.cap').textContent=cap||'';O.classList.add('on');draw()};
O.querySelector('.ct').onclick=e=>{const a=e.target.dataset.a;if(!a)return;if(a=='x'){O.classList.remove('on');tm.forEach(clearTimeout)}else{if(a=='sl')sp=.5;if(a=='fa')sp=2;if(a=='re')sp=1;draw()}};
O.onclick=e=>{if(e.target===O){O.classList.remove('on');tm.forEach(clearTimeout)}};
addEventListener('keydown',e=>{if(O.classList.contains('on')){e.stopImmediatePropagation();if(e.key=='Escape'){O.classList.remove('on');tm.forEach(clearTimeout)}if(e.key==' '||e.key=='Enter'){e.preventDefault();draw()}}},true);
document.querySelectorAll('.kw').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();kvOpen(b.dataset.w,b.dataset.c)},true));})();</script>'''

HEAD = HEAD.replace('</style></head>', CSS + KVGCSS + '</style></head>', 1)

def js(f, var):
    s = open(R + 'public/app/data/' + f, encoding='utf-8').read()
    return json.JSONDecoder().raw_decode(s[s.index('=') + 1:])[0]
DOCS = js('docs.js', 'DOCS'); GRAM = js('grammar.js', 'GRAMMAR')
EXAMS = {e['id']: e for e in js('exams.js', 'EXAMS')}
_VW = js('vocab.js', 'VOCAB')['words']
_LVO = {'入門': 0, '初級1': 1, '初級2': 2, '初中級': 3}
def rel(word, n=4):
    # Từ liên quan: từ trong いろどり có chung chữ Hán (ưu tiên cấp thấp, từ ngắn)
    ks = [c for c in word if '\u4e00' <= c <= '\u9fff']; out = []; seen = {word}
    for c in ks:
        cand = [w for w in _VW if c in w['h'] and w['h'] not in seen and len(w['h']) <= 4 and w.get('y')]
        cand.sort(key=lambda w: (min((_LVO.get(l[0], 9) for l in w.get('l') or []), default=9), len(w['h'])))
        for w in cand[:2 if len(ks) > 1 else 4]:
            seen.add(w['h']); out.append(w)
    out = out[:n]
    if not out: return ''
    return '<div class="krel st"><b>Từ liên quan</b>' + ''.join(f'<div><span class="jp">{html.escape(w["h"])}</span><i>{html.escape(w["y"])}</i><small>{html.escape(w["v"].split(",")[0][:24])}</small></div>' for w in out) + '</div>'

VOC = DOCS['vocab']['入門']; KAN = DOCS['kanji']['入門']
GB = {g['bai']: g for g in GRAM if g['lv'] == '入門'}

RB0 = lambda s: re.sub(r'\{([^|{}]+)\|([^{}]+)\}', r'<ruby>\1<rt>\2</rt></ruby>', html.escape(s)).replace('\n', '<br>')
J = lambda s: furi(html.escape(s))
def RB(s):
    s = re.sub(r'【[A-Za-z][A-Za-z ]*\s*', '【', s)
    s = re.sub(r'（[A-Za-zマス\-]*-form\s*', '（', s)
    s = re.sub(r'＜[A-Za-z]+\s*', '＜', s)
    return RB0(s)
_AU = {}
def aud(path):
    if path not in _AU:
        b = subprocess.run(['ffmpeg', '-v', 'error', '-i', R + 'public/' + path, '-ac', '1', '-b:a', '64k', '-f', 'mp3', '-'], capture_output=True, check=True).stdout
        _AU[path] = 'data:audio/mpeg;base64,' + base64.b64encode(b).decode()
    return _AU[path]
def pimg(path, w=520):
    im = Image.open(R + 'public/' + path).convert('RGB')
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=80, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
_IMG = {}
def img(name, w=360):
    if name not in _IMG:
        im = Image.open(R + 'public/app/media/doc/' + name).convert('RGB')
        if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, 'JPEG', quality=78, optimize=True)
        _IMG[name] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    return _IMG[name]

G1CSS = (".gx{display:grid;grid-template-columns:660px 1fr;gap:32px;margin-top:0;align-items:start}"
 ".gxl{display:flex;flex-direction:column;gap:12px}.gxp{background:#0d5a8c;color:#fff;border-radius:20px;padding:16px 26px;font-family:'Klee One',serif;font-weight:600;font-size:40px;line-height:1.45}"
 ".gxp.lo{font-size:33px}.gxp rt{font-size:.42em}.gxp .no{color:#ffd166;margin-right:10px}.gxm{font-size:27px;font-weight:800;color:#c42f66;line-height:1.3}"
 ".gxh{font-size:19px;font-weight:800;letter-spacing:.06em;color:#6b8296;text-transform:uppercase}"
 ".gxx{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:8px}.gxx li{background:#fff;border-radius:14px;padding:9px 16px;font-size:21px;line-height:1.45;box-shadow:0 6px 18px #0d2b4010;border-left:8px solid #f2a93b}"
 ".gxx li rt{font-size:.5em}.gxn{background:#fff8e6;border-radius:14px;padding:8px 16px;font-size:21px;color:#8a5a00;line-height:1.4}"
 ".gxr{display:flex;flex-direction:column;gap:12px}.gxe{background:#fff;border-radius:16px;padding:10px 20px;box-shadow:0 6px 18px #0d2b4012;border-left:8px solid #0d5a8c}"
 ".gxe:nth-child(3){border-color:#c42f66}.gxe:nth-child(4){border-color:#5a9e2f}"
 ".gxe .jpt{font-size:29px;line-height:1.7}.gxe .jpt rt{font-size:.45em}.gxe .vi{font-size:20px;color:#47647a;line-height:1.4}"
 ".gx.sm .gxe .jpt{font-size:25px;line-height:1.65}.gx.sm .gxx li{font-size:19.5px}")
def g1slide(p, note=None):
    """Slide dạy 1 mẫu ngữ pháp: mẫu + nghĩa + cách dùng (文法ノート) bên trái, tối đa 3 câu ví dụ bên phải (câu sách + câu luyện thêm của 文法ノート)."""
    plain = lambda t: re.sub(r'\{([^|]+)\|[^}]+\}', r'\1', t)
    xs = [x for x in p.get('explain_vi', []) if x.strip() and not x.rstrip().endswith((':', '：'))][:3]
    exs = (p.get('examples') or []) + (p.get('more_examples') or [])
    pick, tot = [], 0
    for e in exs:
        L = len(plain(e['jp'])) + 14 * e['jp'].count('\n')
        if pick and (tot + L > 100 or len(pick) >= 3): continue
        pick.append(e); tot += L
    xl = sum(len(x) for x in xs)
    sm = tot > 75 or xl > 300
    lo = len(plain(p['pattern'])) > 22
    li = ''.join(f'<li class="st">{RB(x)}</li>' for x in xs)
    eg = ''.join(f'<div class="gxe"><div class="jpt">{RB(e["jp"])}</div><div class="vi st">{html.escape(e["vi"]).replace(chr(10), "<br>")}</div></div>' for e in pick)
    return (f'<div class="gx{" sm" if sm else ""}"><div class="gxl"><div class="gxp{" lo" if lo else ""}"><span class="no">{p["no"]}</span>{RB(p["pattern"])}</div><div class="gxm">{html.escape(p["meaning_vi"])}</div>'
            f'<div class="gxh">Cách dùng</div><ul class="gxx">{li}</ul>' + (f'<div class="gxn st">{note}</div>' if note else '') +
            f'</div><div class="gxr"><div class="gxh">Ví dụ</div>{eg}</div></div>')
def build(no, bais, title, sub, kanji, gsel, tables, quizzes_g, plan, ends, fname, basic, listen, hooks=None, extra_js='', label=None, coverp=None, bare=False, gone=False):
    hooks = hooks or {}; label = label or f'Buổi {no}'
    S = []
    CR = f'<div class="cr">Tổng ôn いろどり 入門 · {label} · Anh Trọng Dạy JFT · 出典：いろどり 生活の日本語 入門 (Quỹ Giao lưu Quốc tế Nhật Bản), 文法ノート いろどり · nét viết: KanjiVG (CC BY-SA 3.0) · bảng tổng hợp và lưu ý là tự soạn</div>'
    def sl(t, body, cls=''):
        S.append(f'<section class="slide{(" " + cls) if cls else ""}">{("<h2>" + t + "</h2>") if t else ""}{body}{CR}</section>')
    NQ = [0]
    def quiz(qhtml, opts, a, expl, src, pic=None, big=None):
        NQ[0] += 1; ks = 'abcd'
        ob = ''.join(f'<button class="o" data-k="{ks[i]}"><b>{ks[i]}</b><span class="jp ot">{o}</span><i></i><em></em></button>' for i, o in enumerate(opts))
        op = f'<div class="opts list" data-a="{ks[a]}">{ob}</div>'
        if pic: body = f'<div class="qi"><img src="{pic}">{op}</div>'
        elif big: body = f'<div class="qi"><div class="qbig">{big}</div>{op}</div>'
        else: body = op
        S.append(f'<section class="slide qz"><div class="kk2">Luyện tập {NQ[0]} <span class="src">{src}</span></div><h2 class="jp q">{qhtml}</h2>{body}<div class="ex"><b>Đáp án: {ks[a]}</b> — {expl}</div>{CR}</section>')
    def shuf(right, wrong, seed):
        opts = [right] + wrong[:3]; k = seed % len(opts)
        opts = opts[k:] + opts[:k]; return opts, opts.index(right)

    # 1. Bìa + kế hoạch
    if not bare: S.append(f'''<section class="slide dark"><div class="cover"><img class="lg" src="{LOGO}"><div class="kk">{label.upper()} · TỔNG ÔN いろどり 入門</div>
<h1>{title}<br><span>{sub}</span></h1><p>{coverp or 'Từ vựng · Chữ Hán · Ngữ pháp · 90 phút'}</p></div>{CR}</section>''')
    if not bare: sl(f'Nội dung {label.lower()} <small>{"90 phút" if not coverp else ""}</small>', '<div class="plan">' + ''.join(f'<div><b>{m if isinstance(m, str) else str(m) + "′"}</b><h3>{h}</h3><p>{p}</p></div>' for m, h, p in plan) + '</div>')

    # 2. Từ vựng
    sl('', f'<div class="sec"><div class="n">01</div><div class="t">Từ vựng</div><div class="j">ことば</div><div class="d">Nhìn tranh – đọc từ – bấm thẻ để xem nghĩa</div>{f"<div class=tm>{plan[0][0]} phút</div>" if isinstance(plan[0][0], int) else ""}</div>')
    vq = []
    for b in bais:
        ws = ([w for w in VOC if w['b'] == b and w.get('img')] + [w for w in VOC if w['b'] == b and not w.get('img')])[:10]
        if not ws: continue
        def vcard(w):
            wc = f'<div class="w{" sm" if len(w["r"]) > 7 else ""}">{w["wr"]}</div>'
            vi = f'<div class="st g2"><div class="m">{html.escape(w["vi"])}</div></div>'
            if w.get('img'): return f'<div class="kc kv"><img src="{img(w["img"])}"><div class="st g1">{wc}</div>{vi}</div>'
            return f'<div class="kc kv noimg"><div class="nw">{wc}</div>{vi}</div>'
        cards = ''.join(vcard(w) for w in ws)
        g = GB.get(b)
        sl(f'<span class="bt">Bài {b}</span> <span class="jpt">{RB(g["title"]) if g else ""}</span> <small>{html.escape(g["title_vi"]) if g else ""}</small>', f'<div class="vg">{cards}</div>')
        vq += [w for w in ws if w.get('rd')][2:3] + [w for w in ws if w.get('rd')][6:7]
    for i, w in enumerate(vq[:2] if basic else vq[:3]):
        opts, a = shuf(w['r'], w['rd'], i + 1)
        quiz('Nhìn tranh, chọn cách đọc đúng.', [html.escape(o) for o in opts], a, f'<span class="jp">{w["wr"]}</span> ({html.escape(w["r"])}) – {html.escape(w["vi"])}', 'Từ vựng いろどり 入門 Bài ' + str(w['b']), pic=img(w['img']))

    if 'vocab' in hooks: hooks['vocab'](S, sl, quiz, CR)
    # 3. Chữ Hán
    sl('', f'<div class="sec"><div class="n">02</div><div class="t">Chữ Hán</div><div class="j">かんじ</div><div class="d">Âm Hán Việt · cách đọc · nghĩa · câu ví dụ</div>{f"<div class=tm>{plan[1][0]} phút</div>" if isinstance(plan[1][0], int) else ""}</div>')
    for grp, gt in kanji:
        ks = [k for k in KAN if k['w'] in grp]
        ks.sort(key=lambda k: grp.index(k['w']))
        n = len(ks)
        def kcard(k):
            L = len(k['w'].replace('、', ''))
            ksz = {1: 120, 2: 96, 3: 74, 4: 58, 5: 48}.get(L, 30)
            if n >= 6: ksz = int(ksz * .78)
            cs = '　'.join(f'<b>{c["k"]}</b> {c["hv"]}' for c in k['chars'][:3]) if len(k['chars']) > 1 and n <= 5 else ''
            ex = f'<div class="ex2 jp">{k["ex"]["jp"]}<small>{html.escape(k["ex"]["vi"])}</small></div>' if k.get('ex') and n <= 5 else ''
            kj = ''.join(c for c in k['w'] if c in KVG)
            kb = f'<button class="kw" data-w="{kj}" data-c="{html.escape(k["w"])} · {html.escape(k["hv"])}">✍ Nét</button>' if kj else ''
            if '、' in k['w']:
                return f'<div class="kc" style="--ks:64px">{kb}<div class="k">一〜十</div><div class="st"><div class="hv">NHẤT … THẬP</div><div class="rd jp">いち … じゅう</div><div class="mn">{html.escape(k["vi"])}</div></div></div>'
            return f'<div class="kc" style="--ks:{ksz}px">{kb}<div class="k"{" style=white-space:nowrap" if L <= 5 else ""}>{html.escape(k["w"])}</div><div class="st"><div class="hv">{html.escape(k["hv"])}</div><div class="rd jp">{html.escape(k["r"])}</div><div class="mn">{html.escape(k["vi"])}</div>{f"<div class=cs>{cs}</div>" if cs else ""}{ex}</div></div>'
        if n == 7 or any('、' in k['w'] for k in ks):
            sl(f'Chữ Hán <small>{gt}</small>', f'<div class="kg c{min(n, 5) if n != 7 else 7}">' + ''.join(kcard(k) for k in ks) + '</div>')
            continue
        for ii, k in enumerate(ks):
            kj = ''.join(c for c in k['w'] if c in KVG)
            rows = ''.join(f'<tr><td class="kk">{html.escape(c["k"])}</td><td class="hh">{html.escape(c["hv"])}</td><td>{html.escape(c.get("on") or "–")}</td><td>{html.escape(c.get("kun") or "–")}</td><td class="mm">{html.escape(c.get("vi") or "")}</td></tr>' for c in k['chars'])
            tip = re.sub(r'^\s*(Mẹo nhớ|Mẹo|Ghi nhớ)\s*:\s*', '', k.get('tip') or '')
            ex = k.get('ex') or {}
            body = (f'<div class="kd"><div class="kdl"><div class="kvi" data-w="{kj}"></div><button class="kvr" onclick="kvPlay(this.previousElementSibling,1)">▶ Viết lại</button><button class="kvr" onclick="kvPlay(this.parentNode.querySelector(&quot;.kvi&quot;),.45)">Chậm</button>{rel(k["w"])}</div>'
                    f'<div class="kdr"><div class="kdh"><span class="kdw">{html.escape(k["w"])}</span><span class="kdv">{html.escape(k["hv"])}</span></div>'
                    f'<div class="st kdm"><span class="jp">{html.escape(k["r"])}</span> · {html.escape(k["vi"])}</div>'
                    f'<table class="kdt st"><tr><th>Chữ</th><th>Hán Việt</th><th>Âm On</th><th>Âm Kun</th><th>Nghĩa</th></tr>{rows}</table>'
                    + (f'<div class="kdn st"><b>Cách nhớ</b> {html.escape(tip)}</div>' if tip else '')
                    + (f'<div class="kde st"><div class="jp">{ex["jp"]}</div><small>{html.escape(ex.get("vi", ""))}</small></div>' if ex.get('jp') else '')
                    + '</div></div>')
            sl(f'Chữ Hán <small>{gt} · {ii + 1}/{n}</small>', body)
    allk = [k for grp, _ in kanji for k in KAN if k['w'] in grp and k.get('rd')]
    pick = [allk[3], allk[len(allk) // 2], allk[-4]]
    for i, k in enumerate(pick[:2] if basic else pick):
        opts, a = shuf(k['r'], k['rd'], i + 2)
        quiz('Chữ Hán này đọc thế nào?', [html.escape(o) for o in opts], a, f'{html.escape(k["w"])} đọc là <b>{html.escape(k["r"])}</b> ({html.escape(k["hv"])}) – {html.escape(k["vi"])}', 'Chữ Hán いろどり 入門', big=html.escape(k['w']))
    kw = [k for k in allk if k.get('wk')]
    for i, k in enumerate([kw[1], kw[-2]] if not basic else [kw[5]]):
        opts, a = shuf(k['w'], k['wk'], i + 3)
        quiz('Chọn chữ Hán đúng.', [html.escape(o) for o in opts], a, f'<b>{html.escape(k["w"])}</b> ({html.escape(k["hv"])}) – {html.escape(k["vi"])}', 'Chữ Hán いろどり 入門', big=html.escape(k['r']))

    if 'kanji' in hooks: hooks['kanji'](S, sl, quiz, CR)
    # 4. Ngữ pháp
    sl('', f'<div class="sec"><div class="n">03</div><div class="t">Ngữ pháp</div><div class="j">ぶんぽう</div><div class="d">Mẫu câu – nghĩa – câu ví dụ trong sách</div>{f"<div class=tm>{plan[2][0]} phút</div>" if isinstance(plan[2][0], int) else ""}</div>')
    if gone:   # 19/11 anh dặn: mỗi mẫu ngữ pháp 1 slide riêng, giảng kỹ + nhiều ví dụ, rồi 1 câu luyện ngay sau
        S.append('<style>' + G1CSS + '</style>')
        for b, nos, notes in gsel:
            g = GB[b]
            for k, pno in enumerate(nos):
                p = next(x for x in g['points'] if x['no'] == pno)
                sl(f'<span class="bt">Bài {b}</span> <span class="jpt">{RB(g["title"])}</span> <small>{html.escape(g["title_vi"])} · mẫu {k + 1}/{len(nos)}</small>', g1slide(p, notes.get(pno)))
                qs = p.get('quiz') or []
                if qs:
                    q = qs[0]
                    quiz(RB(q['q']).replace('（　）', '<u>（　　）</u>'), [RB(o) for o in q['o']], q['a'], html.escape(q.get('ex_vi', '')), f'文法ノート いろどり 入門 Bài {b} · mẫu {pno}')
            if b in tables: sl(*tables[b])
        gsel = []
    for b, nos, notes in gsel:
        g = GB[b]; pts = [p for p in g['points'] if p['no'] in nos]
        mx = 3 if all(len(re.sub(r'\{([^|]+)\|[^}]+\}', r'\1', p['pattern'])) <= 16 and len(re.sub(r'\{([^|]+)\|[^}]+\}', r'\1', p['examples'][0]['jp'] if p['examples'] else '')) <= 26 for p in pts) else 2
        nc = -(-len(pts) // mx); sz = [len(pts) // nc + (1 if i < len(pts) % nc else 0) for i in range(nc)]
        st = [sum(sz[:i]) for i in range(nc)]
        for c, z in zip(st, sz):
            ch = pts[c:c + z]
            items = ''
            for p in ch:
                eg = ''.join(f'<div class="jpt">{RB(e["jp"])}</div><div class="vi st">{html.escape(e["vi"])}</div>' for e in p['examples'][:1 if len(ch) == 3 or sum(len(x['jp']) for x in p['examples'][:2]) > 50 else 2])
                nt = notes.get(p['no'])
                items += f'<div class="gpi"><div><div class="pt"><span class="no">{p["no"]}</span>{RB(p["pattern"])}</div><div class="mv">{html.escape(p["meaning_vi"])}</div></div><div class="eg">{eg}{f"<div class=nt>{nt}</div>" if nt else ""}</div></div>'
            sl(f'<span class="bt">Bài {b}</span> <span class="jpt">{RB(g["title"])}</span> <small>{html.escape(g["title_vi"])}</small>', f'<div class="gp{" n2" if len(ch) <= 2 else ""}">{items}</div>')
        if b in tables: sl(*tables[b])
    for i, (b, pno, qi) in enumerate(quizzes_g):
        q = next(p for p in GB[b]['points'] if p['no'] == pno)['quiz'][qi]
        quiz(RB(q['q']).replace('（　）', '<u>（　　）</u>'), [RB(o) for o in q['o']], q['a'], html.escape(q.get('ex_vi', '')), f'文法ノート いろどり 入門 Bài {b}')

    if 'gram' in hooks: hooks['gram'](S, sl, quiz, CR)
    # 5. Nghe hiểu (câu lấy từ ngân hàng đề trong app)
    sl('', f'<div class="sec"><div class="n">04</div><div class="t">Nghe hiểu</div><div class="j">ちょうかい</div><div class="d">Đọc câu hỏi trước → nghe → chọn đáp án</div>{f"<div class=tm>{plan[3][0]} phút</div>" if isinstance(plan[3][0], int) else ""}</div>')
    for j, (eid, qi) in enumerate(listen):
        e = EXAMS[eid]; q = e['qs'][qi]; ks = 'abcd'; a = q['a'][0]
        hasimg = any(o.get('img') for o in q['o'])
        ob = ''.join(f'<button class="o{" oi" if hasimg else ""}" data-k="{ks[i]}">{f"<img src={chr(34)}{pimg(o[chr(105)+chr(109)+chr(103)], 360)}{chr(34)}>" if o.get("img") else ""}<b>{ks[i]}</b><span class="jp ot">{o["t"]}</span><i></i><em></em></button>' for i, o in enumerate(q['o']))
        op = f'<div class="opts {"oimg" if hasimg else "list"}" data-a="{ks[a]}">{ob}</div>'
        pic = ''.join(f'<img class="lpic" src="{pimg(x)}">' for x in (q.get('imgs') or []))
        body = f'<div class="lsn"><audio controls preload="none" src="{aud(q["au"])}"></audio></div>' + (f'<div class="qi">{pic}{op}</div>' if pic else op)
        S.append(f'<section class="slide qz ls"><div class="kk2">Nghe hiểu {j + 1} <span class="src">Nguồn: {html.escape(e["title"])} · câu {qi + 1} (app luyện thi)</span></div><h2 class="jp q">{q["t"]}</h2>{body}<div class="ex lex">{q.get("ex", "")}</div><button class="lsb" onclick="this.previousElementSibling.classList.toggle(&quot;open&quot;)">📄 Script</button>{CR}</section>')

    if 'listen' in hooks: hooks['listen'](S, sl, quiz, CR)
    # 6. Kết
    if bare: return S
    sl(f'Tổng kết {label.lower()}', ends)
    S.append(f'''<section class="slide dark"><div class="cover"><img class="lg" src="{LOGO}"><div class="kk">おつかれさまでした！</div>
<h1>Hết {label.lower()}<br><span>{f"Hẹn gặp lại ở buổi {no + 1}" if no < 5 else "Tiếp theo: いろどり 初級1"}</span></h1>
<p>Ôn lại trên app: Tài liệu → Từ vựng · Chữ Hán · Ngữ pháp (入門)</p></div>{CR}</section>''')
    out = HEAD.replace('<title>Kính ngữ trong JFT-Basic</title>', f'<title>{label} · Tổng ôn いろどり 入門</title>') + ''.join(S) + '<script>window.KVG=' + json.dumps({c: KVG[c] for c in set(''.join(k['w'] for g_, _ in kanji for k in KAN if k['w'] in g_)) if c in KVG}, ensure_ascii=False, separators=(',', ':')) + '</script>' + KVGJS + TAIL + VSTEP + extra_js
    open(R + 'public/tailieu/' + fname, 'w').write(out)
    print(fname, len(S), 'slides', len(out) // 1024, 'KB')

T = lambda head, rows: '<table class="tb2"><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr>' + ''.join('<tr>' + ''.join(f'<td class="{"h" if i == 0 else ""}">{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows) + '</table>'
jp = lambda s: f'<span class="jpt">{J(s)}</span>'

# ---------------- BUỔI 1 ----------------
tab1 = {
 3: ('Bảng tổng hợp <small>Câu danh từ</small>', T(['', 'Khẳng định', 'Phủ định', 'Câu hỏi'], [
     ['Danh từ', jp('学生です'), jp('学生じゃないです'), jp('学生ですか？')],
     ['Ví dụ', jp('私はベトナム人です'), jp('日本人じゃないです'), jp('マイさんは？')]]) +
     '<div class="pb st">は = chủ đề · も = cũng · か ở cuối = câu hỏi (lên giọng)</div>'),
 5: ('Bảng tổng hợp <small>Động từ thể ます</small>', T(['', 'Khẳng định', 'Phủ định (lịch sự)', 'Phủ định (thường)'], [
     ['飲みます', jp('コーヒーを飲みます'), jp('飲みません'), jp('飲まないです')],
     ['食べます', jp('パンを食べます'), jp('食べません'), jp('食べないです')],
     ['Tần suất', jp('いつも・よく') + ' + <em>V-ます</em>', jp('あまり') + ' + <em>V-ません</em>', '']]) +
     '<div class="pb st">Tân ngữ đi với <b>を</b>: ' + jp('ごはんを食べます') + ' · Thích đi với <b>が</b>: ' + jp('うどんが好きです') + '</div>'),
 7: ('Bảng tổng hợp <small>Tính từ な / い</small>', T(['', 'Khẳng định', 'Phủ định'], [
     ['な-A', jp('静かです') + ' · ' + jp('きれいです'), jp('静かじゃないです')],
     ['い-A', jp('広いです') + ' · ' + jp('新しいです'), jp('広くないです')],
     ['いい', jp('いいです'), '<em>' + jp('よくないです') + '</em>']]) +
     '<div class="pb st">' + jp('きれい') + ' là <b>な-A</b> dù kết thúc bằng い → ' + jp('きれいじゃないです') + '</div>'),
 8: ('Bảng tổng hợp <small>あります・います</small>', T(['', 'Dùng cho', 'Ví dụ'], [
     [jp('あります'), 'Đồ vật, cây cối, sự kiện', jp('机の上に本があります')],
     [jp('います'), 'Người, con vật', jp('山田さんは会議室にいます')],
     ['Vị trí', jp('上・下・中・前・後ろ・横'), jp('かばんの中にあります')]]) +
     '<div class="pb st">Nơi có / ở đi với <b>に</b> · Nơi làm hành động đi với <b>で</b>: ' + jp('食堂で食べます') + '</div>'),
}
build(1, range(1, 10), 'Tổng ôn 入門', 'Bài 1 – 9', [
    (['名前', '国', '私', '日本', '家'], 'Bản thân · nhà'),
    (['父', '母', '子ども', '水', '好き'], 'Gia đình · sở thích'),
    (['食べます', '飲みます', '魚', '肉'], 'Ăn uống'),
    (['新しい', '広い', '古い'], 'Tính từ'),
    (['上', '下', '中'], 'Vị trí'),
    (['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日'], 'Thứ trong tuần'),
    (['朝', '昼', '夜', '時', '分'], 'Thời gian'),
  ], [
    (3, ['❶', '❷', '❸', '❹', '❺', '❻'], {'❺': 'も thay cho は', '❻': 'Cũng nói: ではありません'}),
    (4, ['❶', '❸', '❹'], {}),
    (5, ['❶', '❷', '❸', '❹', '❺', '❻'], {'❷': 'Từ chối nhẹ nhàng, không nói hết câu'}),
    (6, ['❶', '❷', '❸', '❹'], {}),
    (7, ['❷', '❸', '❹', '❺'], {}),
    (8, ['❶', '❷', '❸', '❺'], {}),
    (9, ['❶', '❷', '❸'], {'❶': 'Giờ chính xác + に · khoảng giờ + ごろ (không cần に)'}),
  ], tab1, [(3, '❺', 0), (5, '❹', 0), (7, '❺', 0), (8, '❷', 0), (9, '❷', 0)],
  [(15, 'Từ vựng', 'Bài 4–9: gia đình, món ăn, nhà ở, giờ giấc'), (20, 'Chữ Hán', 'Từng chữ: nét viết, Hán Việt, On/Kun, ví dụ'),
   (40, 'Ngữ pháp', 'Câu danh từ, động từ ます, tính từ, あります・います'), (15, 'Nghe hiểu', '3 câu ngắn: vị trí, giờ hẹn, sở thích')],
  '<div class="kgr g2"><div class="kcd kb"><h3>Đã ôn</h3><ul class="ck"><li>Câu danh từ: です / じゃないです</li><li>Động từ: ます / ません</li><li>Tính từ な・い</li><li>あります・います, vị trí</li><li>Giờ: に・ごろ・から〜まで</li></ul></div>'
  '<div class="kcd kp"><h3>Bài tập về nhà</h3><ul class="ck"><li>App → Tài liệu → Từ vựng 入門 Bài 4–9</li><li>Chữ Hán: luyện cách đọc</li><li>Ngữ pháp: làm worksheet Bài 3–9</li></ul></div></div>',
  'Buoi01_TongOn_NhapMon_1.html', True, [('jft-f10', 31), ('jft-y1', 27), ('jft-ln1', 7)])

# ---------------- BUỔI 2 ----------------
tab2 = {
 13: ('Bảng tổng hợp <small>Trợ từ chỉ nơi chốn, phương tiện</small>', T(['Trợ từ', 'Nghĩa', 'Ví dụ'], [
     [jp('に'), 'Nơi đến · nơi có · lên xe', jp('空港に行きます') + ' · ' + jp('バスに乗ります')],
     [jp('で'), 'Nơi làm hành động · phương tiện', jp('駅で降ります') + ' · ' + jp('電車で来ます')],
     [jp('へ'), 'Hướng đi (= に)', jp('京都へ行きます')],
     [jp('を'), 'Rời khỏi', jp('バスを降ります')],
     [jp('から・まで'), 'Từ … đến …', jp('駅から会社まで')]])),
 16: ('Bảng tổng hợp <small>こ・そ・あ・ど</small>', T(['', 'こ (gần mình)', 'そ (gần bạn)', 'あ (xa cả hai)', 'ど (hỏi)'], [
     ['Vật', jp('これ'), jp('それ'), jp('あれ'), jp('どれ')],
     ['+ N', jp('この'), jp('その'), jp('あの'), jp('どの')],
     ['Nơi', jp('ここ'), jp('そこ'), jp('あそこ'), jp('どこ')]])),
 17: ('Bảng tổng hợp <small>Quá khứ</small>', T(['', 'Khẳng định', 'Phủ định'], [
     ['Động từ', jp('見ました'), jp('見ませんでした')],
     ['Danh từ', jp('雨でした'), jp('雨じゃなかったです')],
     ['な-A', jp('静かでした'), jp('静かじゃなかったです')],
     ['い-A', jp('楽しかったです'), jp('楽しくなかったです')],
     ['いい', '<em>' + jp('よかったです') + '</em>', '<em>' + jp('よくなかったです') + '</em>']])),
 18: ('Bảng tổng hợp <small>Từ nối câu · どこか / 何か</small>', T(['', 'Nghĩa', 'Ví dụ'], [
     [jp('あと'), 'Ngoài ra còn', jp('温泉に入りたいです。あと、すしも食べたいです。')],
     [jp('それから'), 'Sau đó', jp('お寺を見ます。それから、買い物します。')],
     [jp('それに'), 'Hơn nữa', jp('安いです。それに、おいしいです。')],
     [jp('でも'), 'Nhưng', jp('楽しかったです。でも、疲れました。')],
     [jp('どこにも・何も'), '+ phủ định: không … gì / đâu cả', jp('どこにも行きませんでした。')]])),
}
# 19/11: Buổi 2 cũ (Bài 10–18, 113 slide) dài quá → anh bảo chia đôi: Buổi 2 = Bài 10–13, Buổi 3 = Bài 14–18.
# Mỗi buổi: từ vựng + "từ khó hay gặp trong đề", chữ Hán, ngữ pháp, luyện nghe (câu trong ngân hàng đề nghe của app – audio いろどり 入門, script đã kiểm)
# và phần Đọc hiểu (cách làm bài đọc – tự soạn + bài đọc dễ trong ngân hàng đề của app, đã có đáp án, dịch, giải thích).
HARD = {
 'bien': ('Biển báo · thông báo <small>Bài 14–16</small>', [('営業中', 'えいぎょうちゅう', 'DOANH NGHIỆP TRUNG', 'đang mở cửa'), ('準備中', 'じゅんびちゅう', 'CHUẨN BỊ TRUNG', 'đang chuẩn bị (chưa mở)'),
            ('定休日', 'ていきゅうび', 'ĐỊNH HƯU NHẬT', 'ngày nghỉ định kỳ'), ('年中無休', 'ねんじゅうむきゅう', 'NIÊN TRUNG VÔ HƯU', 'mở cửa quanh năm'), ('工事中', 'こうじちゅう', 'CÔNG SỰ TRUNG', 'đang thi công'),
            ('通行止', 'つうこうどめ', 'THÔNG HÀNH CHỈ', 'cấm đường'), ('非常口', 'ひじょうぐち', 'PHI THƯỜNG KHẨU', 'lối thoát hiểm'), ('化粧室', 'けしょうしつ', 'HOÁ TRANG THẤT', 'nhà vệ sinh'),
            ('税込', 'ぜいこみ', 'THUẾ + 込', 'đã gồm thuế'), ('半額', 'はんがく', 'BÁN NGẠCH', 'nửa giá')],
          [('定休日', 'ていきゅうび', ['ていきゅうひ', 'じょうきゅうび', 'ていやすみび'], 'ngày nghỉ định kỳ'), ('非常口', 'ひじょうぐち', ['ひじょうこう', 'ひしょうぐち', 'ひじょうくち'], 'lối thoát hiểm'),
           ('半額', 'はんがく', ['はんかく', 'はんがっく', 'ばんがく'], 'nửa giá')]),
 'tau': ('Tàu xe · ngày tháng · sự kiện <small>Bài 12–13</small>', [('改札', 'かいさつ', 'CẢI TRÁT', 'cửa soát vé'), ('快速', 'かいそく', 'KHOÁI TỐC', 'tàu nhanh'),
            ('各駅停車', 'かくえきていしゃ', 'CÁC DỊCH ĐÌNH XA', 'tàu dừng mọi ga'), ('終点', 'しゅうてん', 'CHUNG ĐIỂM', 'ga cuối'), ('乗り換え', 'のりかえ', 'THỪA HOÁN', 'chuyển tàu'),
            ('反対側', 'はんたいがわ', 'PHẢN ĐỐI TRẮC', 'phía đối diện'), ('1日', 'ついたち', 'cách đọc đặc biệt', 'ngày mùng 1'), ('20日', 'はつか', 'cách đọc đặc biệt', 'ngày 20'),
            ('入場無料', 'にゅうじょうむりょう', 'NHẬP TRƯỜNG VÔ LIỆU', 'vào cửa miễn phí'), ('問い合わせ先', 'といあわせさき', 'VẤN HỢP TIÊN', 'nơi liên hệ')],
          [('改札', 'かいさつ', ['かいさく', 'かいざつ', 'がいさつ'], 'cửa soát vé'), ('終点', 'しゅうてん', ['しゅってん', 'しゅうでん', 'じゅうてん'], 'ga cuối'),
           ('20日', 'はつか', ['にじゅうにち', 'はっか', 'はつび'], 'ngày 20 (cách đọc đặc biệt)')])}
def hook_vocab(key):
    t, ws, qs = HARD[key]
    def f(S, sl, quiz, CR):
        cards = ''.join(f'<div class="kc kv noimg"><div class="nw"><div class="w{" sm" if len(w) > 3 else ""}" style="font-size:{46 if len(w) <= 3 else 36}px">{html.escape(w)}</div></div>'
                        f'<div class="st g1"><div class="m" style="color:#0d5a8c;font-size:24px">{html.escape(r)}<br><small style="color:#6b8296;font-size:16px">{html.escape(h)}</small></div></div>'
                        f'<div class="st g2"><div class="m">{html.escape(v)}</div></div></div>' for w, r, h, v in ws)
        sl(f'Từ khó hay gặp trong đề · {t}', f'<div class="vg">{cards}</div>')
        for i, (w, r, wr, v) in enumerate(qs):
            opts = [r] + wr; k = (i + 1) % 4; opts = opts[k:] + opts[:k]
            quiz('Đọc thế nào?', opts, opts.index(r), f'{w} đọc là <b>{r}</b> – {v} (câu tự soạn)', 'Từ khó いろどり 入門 · câu tự soạn', big=w)
    return f
def exq(S, CR, eid, qi, lab, src, listen):
    e = EXAMS[eid]; q = e['qs'][qi]; ks = 'abcd'; a = q['a'][0]
    hasimg = any(o.get('img') for o in q['o'])
    ot = lambda t: re.sub(r'^\s*[a-dA-D]\s*[\.．]\s*', '', t)     # bỏ "a. " có sẵn trong phương án
    ob = ''.join(f'<button class="o{" oi" if hasimg else ""}" data-k="{ks[i]}">{f"<img src={chr(34)}{pimg(o[chr(105)+chr(109)+chr(103)], 360)}{chr(34)}>" if o.get("img") else ""}<b>{ks[i]}</b><span class="jp ot">{ot(o["t"])}</span><i></i><em></em></button>' for i, o in enumerate(q['o']))
    op = f'<div class="opts {"oimg" if hasimg else "list"}" data-a="{ks[a]}">{ob}</div>'
    if listen:
        body = f'<div class="lsn"><audio controls preload="none" src="{aud(q["au"])}"></audio></div>' + op
    else:
        ims = (q.get('imgs') or []) + ([q['img']] if q.get('img') else [])
        body = f'<div class="qi rdq"><img src="{pimg(ims[0], 900)}">{op}</div>'
    S.append(f'<section class="slide qz ls{" rd" if not listen else ""}"><div class="kk2">{lab} <span class="src">{src} · {html.escape(e["title"])} câu {qi + 1} trong app</span></div><h2 class="jp q">{q["t"]}</h2>{body}<div class="ex lex">{q.get("ex", "")}</div><button class="lsb" onclick="this.previousElementSibling.classList.toggle(&quot;open&quot;)">📄 {"Script" if listen else "Dịch · giải thích"}</button>{CR}</section>')
RDCSS = '<style>.rdq{grid-template-columns:1.5fr 1fr!important;align-items:start}.rdq>img{max-height:500px;width:100%;object-fit:contain;border-radius:14px;box-shadow:0 6px 18px #0d2b4018;background:#fff}.rk{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:8px}.rk>div{background:#fff;border-radius:18px;padding:16px 22px;box-shadow:0 6px 18px #0d2b4010;font-size:26px;line-height:1.45}.rk b.n{display:inline-block;background:#0d5a8c;color:#fff;border-radius:10px;padding:0 12px;margin-right:8px}.rk .jpt{font-size:28px}</style>'
RDSKILL = {
 3: ('Đọc thông báo, lịch, tờ rơi', [
   ('1', 'Đọc câu hỏi trước', 'Gạch chân từ để hỏi: ' + jp('いつ・何時・何曜日・何回・いくら・どこ・だれ')),
   ('2', 'Nhìn tiêu đề, biết đây là gì', jp('お知らせ') + ' thông báo · ' + jp('予定') + ' lịch · ' + jp('教室') + ' lớp học · ' + jp('営業時間') + ' giờ mở cửa'),
   ('3', 'Tìm đúng dòng có câu trả lời', jp('日時') + ' ngày giờ · ' + jp('場所') + ' địa điểm · ' + jp('費用') + ' chi phí · ' + jp('問い合わせ') + ' liên hệ'),
   ('4', 'Đọc kỹ dòng ※ và chữ trong ngoặc', 'Đáp án hay nằm ở đây: ' + jp('※15分前に来てください') + ' · ' + jp('（コピー代がかかります）'))]),
 4: ('Đọc biển, bảng giá, thực đơn', [
   ('1', 'Giá tiền: xem có thuế chưa', jp('税込') + ' đã gồm thuế · ' + jp('税別・税抜') + ' chưa gồm thuế (＋税)'),
   ('2', 'Giảm giá: tính lại', jp('50円引') + ' trừ 50 yên · ' + jp('半額') + ' nửa giá · ' + jp('今週限り') + ' chỉ tuần này'),
   ('3', 'Giờ mở cửa: chú ý ngoại lệ', jp('月〜土 7:00〜17:00（土 16:30）') + ' · ' + jp('定休日は日曜日')),
   ('4', 'Thực đơn: món lẻ hay set', jp('単品') + ' món lẻ · ' + jp('セット') + ' suất có kèm đồ uống, khoai')]),
 5: ('Đọc tin nhắn, email, bài kể chuyện', [
   ('1', 'Xem ai viết cho ai', 'Dòng đầu: ' + jp('〜さん、') + ' là người nhận · cuối thư là tên người viết'),
   ('2', 'Tìm thời gian', jp('昨日・先週・週末・去年') + ' → chuyện đã qua, động từ đuôi ' + jp('〜ました')),
   ('3', 'Tìm cảm xúc, lý do', jp('うれしかったです・楽しかったです') + ' · lý do thường đứng trước ' + jp('から・ので')),
   ('4', 'Câu cuối thường là lời nhờ, lời rủ', jp('〜てください・〜ませんか・また〜ましょう') + ' — câu hỏi "người viết muốn gì" nằm ở đây')])}
def hook_listen(no, parts, reads, rd_fn=None):
    def f(S, sl, quiz, CR):
        n = 0
        for ph, t, src, items in parts:
            sl('', f'<div class="sec"><div class="n">{ph}</div><div class="t" style="font-size:80px">{t}</div><div class="j">{src}</div><div class="d">{len(items)} câu · đọc câu hỏi trước → nghe → chọn</div></div>')
            for eid, qi in items:
                n += 1; exq(S, CR, eid, qi, f'Nghe hiểu {n}', f'{ph} · {src}', True)
        if rd_fn: return rd_fn(S, sl, quiz, CR)
        t, steps = RDSKILL[no]
        sl('', f'<div class="sec"><div class="n">05</div><div class="t">Đọc hiểu</div><div class="j">どっかい</div><div class="d">{t} · {len(reads)} câu</div><div class="tm">15 phút</div></div>')
        sl(f'Cách làm bài đọc <small>{t} · tự soạn</small>', RDCSS + '<div class="rk">' + ''.join(f'<div class="st"><b class="n">{a}</b><b>{b}</b><br>{c}</div>' for a, b, c in steps) + '</div>'
           '<div class="pb st">Không cần hiểu hết bài. Chỉ cần tìm đúng chỗ có câu trả lời.</div>')
        for i, (eid, qi) in enumerate(reads):
            exq(S, CR, eid, qi, f'Đọc hiểu {i + 1}', 'Bài đọc dễ', False)
    return f
def rd_bang(S, sl, quiz, CR):
    """Buổi 2 (19/11, anh dặn): dạy kỹ năng đọc bảng thông tin (情報検索). Cách làm, bảng ký hiệu, câu làm mẫu, câu tự soạn: tự soạn.
    Bài đọc + câu hỏi gốc: ngân hàng đề trong app (đã có đáp án, dịch, giải thích)."""
    sl('', f'<div class="sec"><div class="n">05</div><div class="t">Đọc bảng thông tin</div><div class="j">じょうほうけんさく</div><div class="d">Lịch · giờ mở cửa · thông báo · lịch đổ rác — tìm đúng 1 thông tin</div><div class="tm">20 phút</div></div>')
    sl('Bảng thông tin trong đề JFT <small>tự soạn</small>', RDCSS + '<div class="rk">'
       + ''.join(f'<div class="st"><b>{a}</b><br>{b}</div>' for a, b in [
           (jp('予定表・時間表'), 'Lịch làm việc, lịch học, giờ bắt đầu – kết thúc'), (jp('営業時間・診察時間'), 'Giờ mở cửa cửa hàng, phòng khám, ngày nghỉ'),
           (jp('お知らせ・案内'), 'Thông báo sự kiện, lớp học: ngày giờ, địa điểm, chi phí'), (jp('ゴミの出し方'), 'Lịch đổ rác: loại rác nào, thứ mấy')]) + '</div>'
       '<div class="pb st">Câu hỏi chỉ hỏi <b>1 thông tin</b> (mấy giờ, thứ mấy, bao nhiêu) kèm <b>điều kiện</b> (của ai, ngày nào, nhóm nào). Không cần đọc hết bảng.</div>')
    sl('4 bước đọc bảng <small>tự soạn</small>', RDCSS + '<div class="rk">' + ''.join(f'<div class="st"><b class="n">{a}</b><b>{b}</b><br>{c}</div>' for a, b, c in [
        ('1', 'Đọc câu hỏi, gạch 2 thứ', 'Từ để hỏi: ' + jp('何時・何曜日・いつ・いくら') + '<br>Điều kiện: ' + jp('金曜日・Bグループ・アナさん')),
        ('2', 'Nhìn tiêu đề, tên hàng và tên cột', 'Bảng này nói về gì? Hàng là gì, cột là gì?'),
        ('3', 'Dò hàng rồi dò cột', 'Lấy ngón tay dò: hàng có điều kiện → cột có thông tin cần tìm'),
        ('4', 'Đọc dòng ※ và chữ trong ngoặc', 'Có đến sớm không? Có ngày nghỉ, ngoại lệ không? Tính lại nếu cần')]) + '</div>')
    KH = [('● ／ ○', '', 'có, mở'), ('ー ／ ×', '', 'không có, nghỉ'), ('〜', '', 'từ … đến … (から〜まで)'), ('※', '', 'lưu ý (hay chứa đáp án)'),
          (jp('毎週'), 'まいしゅう', 'mỗi tuần'), (jp('午前・午後'), 'ごぜん・ごご', 'sáng · chiều'), (jp('休業・休診'), 'きゅうぎょう・きゅうしん', 'cửa hàng nghỉ · phòng khám nghỉ'),
          (jp('通常営業'), 'つうじょうえいぎょう', 'mở cửa bình thường'), (jp('受付'), 'うけつけ', 'quầy tiếp đón'), (jp('〜分前に'), '〜ふんまえに', 'trước ~ phút')]
    tb = lambda rows: '<table class="tb2"><tr><th>Trong bảng</th><th>Nghĩa</th></tr>' + ''.join(
        f'<tr><td class="h" style="padding:10px 14px;font-size:30px">{a}</td><td class="st" style="padding:10px 14px;font-size:24px">{c}</td></tr>' for a, b, c in rows) + '</table>'
    sl('Ký hiệu và từ hay gặp trong bảng <small>bấm để xem nghĩa · tự soạn</small>', f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start">{tb(KH[:5])}{tb(KH[5:])}</div>')
    E = EXAMS['jft-g14']; q = E['qs'][22]; im = pimg((q.get('imgs') or [q.get('img')])[0], 900)
    steps = [('1', 'Câu hỏi', f'{jp("金曜日は何時までですか。")}<br>Từ hỏi: <b>{jp("何時まで")}</b> · điều kiện: <b>{jp("金曜日")}</b>'),
             ('2', 'Bảng', f'{jp("診察時間")} = giờ khám. Hàng: 2 khung giờ. Cột: thứ trong tuần.'),
             ('3', 'Dò cột 金', f'Hàng {jp("9:00〜12:00")} có ● · hàng {jp("15:00〜19:00")} có ● → khám đến 19:00'),
             ('4', 'Đọc dòng dưới', f'{jp("休診日：木曜・土曜午後・日曜")} → thứ Sáu không nghỉ. <b>Đáp án: 19:00</b>')]
    sl('Làm mẫu <small>4 bước với bảng giờ khám · ' + html.escape(E['title']) + ' câu 23 trong app</small>', RDCSS + f'<div class="qi rdq"><img src="{im}"><div>' + ''.join(
        f'<div class="exl st" style="font-size:24px;margin-top:10px"><b style="color:#c42f66">Bước {a} · {b}</b><br>{c}</div>' for a, b, c in steps) + '</div></div>')
    ob = ''.join(f'<button class="o" data-k="{k}"><b>{k}</b><span class="jp ot">{t}</span><i></i><em></em></button>' for k, t in zip('abc', ['12:00', '15:00', '19:00']))
    S.append(f'<section class="slide qz"><div class="kk2">Tự làm <span class="src">Câu tự soạn · cùng bảng giờ khám</span></div><h2 class="jp q">{jp("土曜日は何時までですか。")}</h2>'
             f'<div class="qi rdq"><img src="{im}"><div class="opts list" data-a="a">{ob}</div></div>'
             '<div class="ex"><b>Đáp án: a</b> — Cột 土: hàng 9:00〜12:00 có ●, hàng 15:00〜19:00 là ー; dòng dưới ghi 休診日：土曜午後 → thứ Bảy chỉ khám buổi sáng, đến 12:00.</div>' + CR + '</section>')
    for i, (eid, qi) in enumerate(RD_B2):
        exq(S, CR, eid, qi, f'Đọc bảng {i + 1}', 'Luyện tập', False)
LSN_B2 = [('Phần 1', 'Giờ giấc, lịch hẹn', 'いろどり 入門 第9・10課', [('jft-ln3', 0), ('jft-ln1', 2), ('jft-ln2', 0), ('jft-ln1', 3)])]
LSN_B3 = [('Phần 1', 'Sự kiện, thông báo', 'Đề nghe trong app · audio いろどり', [('jft-ln2', 13), ('jft-ln2', 14)]),
          ('Phần 2', 'Đi tàu, tìm sân ga', 'Đề nghe trong app · audio いろどり', [('jft-ln2', 8), ('jft-ln3', 4)])]
LSN_B4 = [('Phần 1', 'Nơi đó thế nào?', 'Đề nghe trong app · audio いろどり', [('jft-ln1', 13), ('jft-ln3', 3)]),
          ('Phần 2', 'Đồ vật, mua sắm', 'Đề nghe trong app · audio いろどり', [('jft-ln2', 19), ('jft-ln1', 15)])]
LSN_B5 = [('Phần 1', 'Ngày nghỉ thế nào?', 'いろどり 入門 第17・18課', [('jft-ln1', 6), ('jft-ln1', 5)]),
          ('Phần 2', 'Muốn làm gì ở Nhật?', 'いろどり 入門 第18課', [('jft-ln1', 4), ('jft-ln2', 1)])]
RD_B2 = [('jft-f8', 38), ('jft-f8', 39), ('jft-f5', 44), ('jft-y3', 40), ('jft-y3', 41), ('jft-g18', 41), ('jft-f8', 41)]
RD_B3 = [('jft-f10', 39), ('jft-g21', 30), ('jft-g21', 31), ('jft-g18', 40), ('jft-f6', 46)]
RD_B4 = [('jft-f13', 49), ('jft-f6', 40), ('jft-g21', 28), ('jft-g21', 29), ('jft-f8', 47)]
RD_B5 = [('jft-f6', 42), ('jft-f4', 44), ('jft-f9', 36), ('jft-g18', 36), ('jft-f2', 36)]
# 19/11 (lần 2): anh thấy chữ Hán và ngữ pháp vẫn nhiều → chia Bài 10–18 thành 4 buổi (anh chọn):
# Buổi 2 = Bài 10–11 · Buổi 3 = Bài 12–13 · Buổi 4 = Bài 14–16 · Buổi 5 = Bài 17–18.
# Mỗi buổi ~10–11 chữ Hán; mỗi mẫu ngữ pháp 1 slide riêng (cách dùng theo 文法ノート + 3–4 câu ví dụ) và 1 câu luyện ngay sau (gone=True).
END = lambda done, hw: ('<div class="kgr g2"><div class="kcd kb"><h3>Đã ôn</h3><ul class="ck">' + ''.join(f'<li>{x}</li>' for x in done) + '</ul></div>'
                        '<div class="kcd kp"><h3>Bài tập về nhà</h3><ul class="ck">' + ''.join(f'<li>{x}</li>' for x in hw) + '</ul></div></div>')
build(2, range(10, 12), 'Tổng ôn 入門', 'Bài 10 – 11', [
    (['読みます', '聞きます', '見ます', '本', '友だち'], 'Hoạt động'),
    (['何', '年', '月', '日', '今日'], 'Ngày tháng'),
  ], [
    (10, ['❶', '❷', '❸'], {'❶': 'Thể て sẽ học kỹ ở 初級1 — buổi này chỉ cần nhớ cả cụm 〜てください.'}),
    (11, ['❷', '❸', '❹', '❺'], {}),
  ], {}, [],
  [(15, 'Từ vựng', 'Bài 10–11: đồ dùng văn phòng, sở thích, hoạt động thường ngày'), (15, 'Chữ Hán', '10 chữ: nét viết, Hán Việt, On/Kun, ví dụ'),
   (25, 'Ngữ pháp', '7 mẫu, mỗi mẫu 1 slide + 1 câu luyện: てください, mượn đồ, どんな, あまり, tần suất, と・で'), (15, 'Nghe hiểu', '4 câu từ いろどり 入門: giờ hẹn, lịch làm việc'),
   (20, 'Đọc bảng thông tin', '4 bước đọc bảng, làm mẫu + 8 câu: lịch, giờ mở cửa, thông báo, lịch đổ rác')],
  END(['V-てください · 貸してください · 借りてもいいですか', 'Nですね (xác nhận lại)', 'どんなN · あまり〜ない', 'いつも・よく・ときどき・あまり・ぜんぜん', '【人】と【場所】でV', 'Đọc bảng: gạch từ hỏi + điều kiện, dò hàng → cột, đọc kỹ ※'],
      ['App → Tài liệu → Từ vựng 入門 Bài 10–11', 'Chữ Hán: luyện cách đọc 10 chữ của buổi', 'Ngữ pháp: worksheet 文法ノート Bài 10–11']),
  'Buoi02_TongOn_NhapMon_2.html', False, [], hooks={'listen': hook_listen(2, LSN_B2, RD_B2, rd_bang)}, gone=True)
build(3, range(12, 14), 'Tổng ôn 入門', 'Bài 12 – 13', [
    (['今週', '今度', '来週', '休み', '予定'], 'Lịch hẹn'),
    (['東', '南', '会社', '来ます', '行きます', '乗ります'], 'Đi lại'),
  ], [
    (12, ['❶', '❷', '❸', '❹', '❺'], {'❶': 'Nơi diễn ra sự kiện dùng で, không dùng に.'}),
    (13, ['❸', '❹', '❺', '❻'], {}),
  ], {13: tab2[13]}, [],
  [(15, 'Từ vựng', 'Bài 12–13 + từ khó: tàu xe, ngày tháng, sự kiện'), (15, 'Chữ Hán', '11 chữ: nét viết, Hán Việt, On/Kun, ví dụ'),
   (30, 'Ngữ pháp', '9 mẫu, mỗi mẫu 1 slide + 1 câu luyện: sự kiện, rủ rê, đi để làm gì, phương tiện, thời gian, lên xuống xe'), (15, 'Nghe hiểu', '4 câu: thông báo sự kiện, đi tàu, sân ga'),
   (15, 'Đọc hiểu', 'Cách đọc thông báo, tờ rơi + 5 câu')],
  END(['【日時】に【場所】で【イベント】があります', 'Nに行きます · V(bỏ ます)に行きます', 'V-ませんか · V-ましょう', 'Phương tiện + で · かかります', 'Nに乗ります / Nを降ります · から〜まで'],
      ['App → Tài liệu → Từ vựng 入門 Bài 12–13', 'Chữ Hán: luyện cách đọc 11 chữ của buổi', 'Làm đề: phần 読解 của 1 đề bất kỳ']),
  'Buoi03_TongOn_NhapMon_3.html', False, [], hooks={'vocab': hook_vocab('tau'), 'listen': hook_listen(3, LSN_B3, RD_B3)}, gone=True)
build(4, range(14, 17), 'Tổng ôn 入門', 'Bài 14 – 16', [
    (['大きい', '小さい', '高い', '低い', '安い'], 'Tính từ'),
    (['前', '後ろ', '横', '入口', '出口'], 'Vị trí · lối đi'),
    (['一、二、三、四、五、六、七、八、九、十', '百', '千', '万', '円'], 'Số đếm · tiền'),
  ], [
    (14, ['❷', '❸'], {'❸': 'な-A + な + N · い-A + N'}),
    (15, ['❶', '❷'], {}),
    (16, ['❶', '❷', '❸'], {}),
  ], {16: tab2[16]}, [],
  [(15, 'Từ vựng', 'Bài 14–16 + từ khó: biển báo, thông báo, giá tiền'), (15, 'Chữ Hán', '10 chữ + số đếm: nét viết, Hán Việt, On/Kun'),
   (25, 'Ngữ pháp', '7 mẫu, mỗi mẫu 1 slide + 1 câu luyện: vị trí, tính từ + N, ほしいんですが, cảm tưởng, いくら, こそあど, ずつ'), (15, 'Nghe hiểu', '4 câu: nơi đó thế nào, đồ vật, mua sắm'),
   (20, 'Đọc hiểu', 'Cách đọc biển, bảng giá + 5 câu')],
  END(['Nの【位置】にいます · ナA-な N / イA-い N', 'Nがほしいんですが · 〜ですね！', 'これ・それ・あれ · この・その・あの N · いくら', '【数量】ずつ', 'Đọc giá: 税込・税別, 〜円引, 単品・セット'],
      ['App → Tài liệu → Từ vựng 入門 Bài 14–16', 'Chữ Hán: luyện đọc số và giá tiền', 'Làm đề: phần 読解 của 1 đề bất kỳ']),
  'Buoi04_TongOn_NhapMon_4.html', False, [], hooks={'vocab': hook_vocab('bien'), 'listen': hook_listen(4, LSN_B4, RD_B4)}, gone=True)
build(5, range(17, 19), 'Tổng ôn 入門', 'Bài 17 – 18', [
    (['会います', '入ります', '買います', '旅行します'], 'Động từ'),
    (['階', '押す', '引く', '映画', '温泉'], 'Toà nhà · giải trí'),
    (['日本語', '勉強します'], 'Học tập'),
  ], [
    (17, ['❶', '❷', '❸', '❹', '❺'], {'❸': 'いい → よかったです (không nói いかったです).'}),
    (18, ['❶', '❷', '❸', '❺', '❻'], {'❶': 'Bỏ ます + たいです: 行きます → 行きたいです.'}),
  ], {k: tab2[k] for k in (17, 18)}, [],
  [(15, 'Từ vựng', 'Bài 17–18: việc đã làm, điều muốn làm'), (15, 'Chữ Hán', '11 chữ: nét viết, Hán Việt, On/Kun, ví dụ'),
   (30, 'Ngữ pháp', '10 mẫu, mỗi mẫu 1 slide + 1 câu luyện: quá khứ, 何も・どこにも, たい, どこか, từ nối câu'), (15, 'Nghe hiểu', '4 câu từ いろどり 入門: ngày nghỉ, du lịch'),
   (15, 'Đọc hiểu', 'Cách đọc tin nhắn, email + 5 câu')],
  END(['Quá khứ: ました・でした・かったです・じゃなかったです', '何も・どこにも + phủ định', 'V-たいです · どこか', 'あと・それから・それに・でも'],
      ['App → Tài liệu → Từ vựng 入門 Bài 17–18', 'Chữ Hán: luyện cách đọc + chọn chữ', 'Làm đề: phần 読解 của 1 đề bất kỳ']),
  'Buoi05_TongOn_NhapMon_5.html', False, [], hooks={'listen': hook_listen(5, LSN_B5, RD_B5)}, gone=True)
