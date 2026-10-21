#!/usr/bin/env python3
# Sinh HTML bài tập (làm trên máy) + HTML in (→ PDF) cho 25 buổi
import json, os, base64, html
B = os.path.dirname(os.path.abspath(__file__)) + '/'
GIMG = B + '../../public/app/media/gimg/'
FD = B + 'fonts/be-vietnam-pro-'  # npm i @fontsource/be-vietnam-pro rồi trỏ tới thư mục files
S = json.load(open(B + 'sessions.json', encoding='utf-8'))
os.makedirs(B + 'out/html', exist_ok=True); os.makedirs(B + 'out/print', exist_ok=True)

def img64(i):
    p = GIMG + i + '.jpg'
    return 'data:image/jpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode() if os.path.exists(p) else None

CSS = r'''
:root{--ink:#17222c;--muted:#5d6b77;--line:#d9e0e6;--soft:#f3f6f8;--navy:#0d4f7c;--acc:#c42f66;--ok:#1d7a4b;--ok-s:#e3f3ea;--ng:#b3261e;--ng-s:#fbe9e7;--bg:#eef2f5;--card:#fff}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--ink:#e6edf2;--muted:#9aa9b4;--line:#2c3945;--soft:#1b2630;--navy:#7bb8e3;--acc:#f07aa4;--ok:#6fd09c;--ok-s:#173226;--ng:#ff8a7a;--ng-s:#3a1d19;--bg:#10171d;--card:#17212a}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Be Vietnam Pro","BVP","Segoe UI",system-ui,-apple-system,sans-serif;font-size:16px;line-height:1.55}
.jp,.jpq,.opt.jp{font-family:"Hiragino Kaku Gothic ProN","Yu Gothic","Noto Sans JP","Noto Sans CJK JP",Meiryo,sans-serif}
ruby{ruby-position:over}rt{font-size:.55em;color:var(--muted)}
body.nofuri rt{visibility:hidden}
.wrap{max-width:860px;margin:0 auto;padding:20px 16px 80px}
header.top{display:flex;align-items:center;gap:12px;margin-bottom:14px}
.logo{width:40px;height:40px;border-radius:10px;background:var(--acc);color:#fff;display:grid;place-items:center;font-weight:700;flex:none}
header.top b{display:block}header.top small{color:var(--muted)}
.hero{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px 22px;margin-bottom:16px}
.hero .k{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);font-weight:600}
.hero h1{margin:6px 0 2px;font-size:28px;line-height:1.25}
.hero h1 .jp{font-weight:600;margin-right:10px}
.hero .sub{color:var(--muted);font-size:14px}
.hero .meta{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px;align-items:center}
.hero input{border:1px solid var(--line);border-radius:10px;padding:9px 12px;font:inherit;background:var(--soft);color:var(--ink);min-width:220px}
.btn{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:10px;padding:9px 14px;font:inherit;font-weight:600;cursor:pointer}
.btn.pri{background:var(--navy);border-color:var(--navy);color:#fff}
.sec{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 20px;margin-bottom:16px}
.sec h2{font-size:19px;margin:0}
.sec h2 .jp{font-size:14px;color:var(--muted);font-weight:500;margin-left:8px}
.sec .ins{color:var(--muted);font-size:14px;margin:4px 0 10px}
.sec .ins .jp{display:block;font-size:13px}
.it{border-top:1px solid var(--line);padding:12px 0}
.it .qh{display:flex;gap:10px}
.it .n{flex:none;min-width:30px;height:26px;border-radius:7px;background:var(--soft);display:grid;place-items:center;font-weight:700;font-size:13px;color:var(--navy)}
.it .q{font-size:18px;line-height:1.9}
.it .q u{text-decoration:none;border-bottom:2px solid var(--ink)}
.it .q .kana{font-size:20px}.it .q .hint{color:var(--muted);font-size:14px;margin-left:6px;font-family:"Be Vietnam Pro",system-ui,sans-serif}
.it .sins{font-size:13px;color:var(--muted);margin-bottom:2px}
.it img.qi{display:block;max-width:260px;max-height:180px;margin:6px 0;border-radius:8px;border:1px solid var(--line)}
.opts{display:grid;gap:8px;margin:8px 0 0 40px}
.opts.cols{grid-template-columns:repeat(auto-fill,minmax(180px,1fr))}
.opt{display:flex;gap:10px;align-items:flex-start;border:1px solid var(--line);border-radius:10px;padding:9px 12px;cursor:pointer;background:var(--card);font-size:16px;line-height:1.7;text-align:left;color:var(--ink);font-family:inherit}
.opt .l{flex:none;width:22px;height:22px;border-radius:50%;border:1.5px solid var(--muted);display:grid;place-items:center;font-size:12px;font-weight:700;margin-top:3px;font-family:"Be Vietnam Pro",system-ui,sans-serif}
.opt.sel{border-color:var(--navy);box-shadow:0 0 0 1px var(--navy) inset}.opt.sel .l{background:var(--navy);border-color:var(--navy);color:#fff}
.opt.right{border-color:var(--ok);background:var(--ok-s)}.opt.wrong{border-color:var(--ng);background:var(--ng-s)}
.fill{margin:8px 0 0 40px}
.fill input,.fill textarea{width:100%;max-width:520px;border:1px solid var(--line);border-radius:10px;padding:9px 12px;font:inherit;font-size:17px;background:var(--soft);color:var(--ink)}
.fill textarea{min-height:64px}
.fill input.right{border-color:var(--ok);background:var(--ok-s)}.fill input.wrong{border-color:var(--ng);background:var(--ng-s)}
.fb{margin:8px 0 0 40px;font-size:14px;color:var(--muted);display:none}
.done .fb{display:block}
.fb b{color:var(--ink)}
.model{display:none;margin:8px 0 0 40px;padding:8px 12px;border-radius:10px;background:var(--soft);font-size:17px}
.model.on{display:block}
.chk{display:flex;gap:10px;align-items:flex-start;padding:8px 0;border-top:1px solid var(--line);cursor:pointer}
.chk input{width:18px;height:18px;margin-top:3px}
.bar{position:sticky;bottom:0;background:var(--card);border-top:1px solid var(--line);padding:10px 16px;display:flex;gap:10px;align-items:center;justify-content:center;flex-wrap:wrap;z-index:5}
.score{font-weight:700}
.res{display:none;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 20px;margin-bottom:16px}
.res.on{display:block}.res .big{font-size:40px;font-weight:800;color:var(--navy)}
.res table{border-collapse:collapse;width:100%;margin-top:8px;font-size:14px}.res td{border-top:1px solid var(--line);padding:6px 0}.res td:last-child{text-align:right;font-weight:600}
footer{color:var(--muted);font-size:12px;margin-top:20px}
@media (max-width:600px){.opts,.fill,.fb,.model{margin-left:0}.hero h1{font-size:23px}.it .q{font-size:17px}}
'''

PRINT_CSS = ''.join(f"@font-face{{font-family:'BVP';font-weight:{w};src:url('{FD}{sub}-{w}-normal.woff2')}}" for w in (400, 500, 600, 700) for sub in ('vietnamese', 'latin', 'latin-ext')) + r'''
@page{size:A4;margin:13mm 14mm 15mm}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{background:#fff;color:#17222c;font-family:'BVP',sans-serif;font-size:9.6pt;line-height:1.5}
.jp,.jpq{font-family:'Noto Sans CJK JP','BVP',sans-serif}
.wrap{max-width:none;padding:0}
.hero{border:0;border-bottom:1.4pt solid #17222c;border-radius:0;padding:0 0 3mm;margin-bottom:4mm}
.hero h1{font-size:19pt}.hero .meta{margin-top:3mm}
.hero .name{border-bottom:.6pt solid #9aa6b0;min-width:70mm;display:inline-block;height:6mm}
.hero .meta span{font-size:9pt;color:#5d6b77}
.sec{border:0;border-radius:0;padding:0;margin-bottom:5mm}
.sec h2{font-size:12pt;border-bottom:.6pt solid #d9e0e6;padding-bottom:1mm}
.sec .ins{font-size:8.6pt;margin:1.5mm 0 1mm}
.it{padding:2.2mm 0;break-inside:avoid;border-top:.5pt solid #e3e8ec}
.it .q{font-size:11pt;line-height:1.85}
.it .n{min-width:7mm;height:5.5mm;font-size:8.5pt;border-radius:1.5mm}
.opts{margin:1mm 0 0 9mm;gap:1mm 6mm;grid-template-columns:repeat(var(--c,1),1fr)}
.opt{border:0;padding:.4mm 0;font-size:10.2pt;line-height:1.65}
.opt .l{width:4.6mm;height:4.6mm;font-size:7.5pt;margin-top:.8mm}
.fill{margin:1.5mm 0 0 9mm}.fill .line{border-bottom:.6pt solid #9aa6b0;height:7mm;max-width:120mm}.fill .line+.line{margin-top:1mm}
.it img.qi{max-width:45mm;max-height:32mm}
.chk{border-top:0;padding:1mm 0;font-size:9.6pt}.chk .box{width:3.6mm;height:3.6mm;border:.7pt solid #7c8b97;border-radius:.6mm;flex:none;margin-top:1mm}
.its.g2{columns:2;column-gap:8mm}.its.g2 .it{break-inside:avoid;display:block}
.ak{page-break-before:always}
.ak h2{font-size:13pt;margin:0 0 2mm}
.ak .sub{color:#5d6b77;font-size:8.5pt;margin-bottom:3mm}
.ak table{border-collapse:collapse;width:100%;font-size:8.4pt}
.ak td{border-top:.5pt solid #e3e8ec;padding:1.1mm 2mm 1.1mm 0;vertical-align:top}
.ak td.n{width:8mm;font-weight:700;color:#0d4f7c}.ak td.a{width:52mm;font-weight:600}
.ak tr.sh td{font-weight:700;padding-top:3mm;border-top:0;color:#5d6b77;font-size:7.6pt;letter-spacing:.08em;text-transform:uppercase}
footer{font-size:7.5pt}
header.top{margin-bottom:3mm}
'''

JS = r'''
const D=JSON.parse(document.getElementById('data').textContent);const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const rb=s=>String(s??'').replace(/\{([^|}]+)\|([^}]+)\}/g,'<ruby>$1<rt>$2</rt></ruby>').replace(/\n/g,'<br>');
const plain=s=>String(s??'').replace(/\{([^|}]+)\|[^}]+\}/g,'$1');
const norm=s=>String(s??'').normalize('NFKC').replace(/[\s。、．，,.!！?？「」『』（）()]/g,'');
const L='ABCD';const PRINT=document.body.classList.contains('print');
const KEY='btvn-'+D.no;let st={};try{st=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}};
st.a=st.a||{};
function render(){let h='';
 D.secs.forEach((s,si)=>{h+=`<section class="sec"><h2>${si+1}. ${esc(s.title)}<span class="jp">${esc(s.jp||'')}</span></h2><div class="ins">${esc(s.ins||'')}${s.ins_jp?`<span class="jp">${esc(s.ins_jp)}</span>`:''}</div><div class="its ${['voc','kw'].includes(s.id)?'g2':''}">`;
  s.items.forEach((it,ii)=>{const id=`${si}_${ii}`;
   if(it.t==='check'){h+=PRINT?`<div class="chk"><span class="box"></span><span>${esc(it.q)}</span></div>`:`<label class="chk"><input type="checkbox" data-ck="${id}" ${st.a[id]?'checked':''}><span>${esc(it.q)}</span></label>`;return}
   h+=`<div class="it" id="it${id}">`;
   if(it.ins&&s.id==='ws')h+=`<div class="sins">${esc(it.ins)}${it.ex_q?` · Ví dụ: <span class="jp">${rb(it.ex_q.q)} → ${rb(it.ex_q.a)}</span>`:''}</div>`;
   if(it.ins&&s.id!=='ws')h+=`<div class="sins">${esc(it.ins)}</div>`;
   h+=`<div class="qh"><span class="n">${it.n}</span><div class="q ${it.tag&&it.tag.includes('jpq')?'jpq':''}">${it.t==='write'?esc(it.q):rb(it.q)}${it.img64?`<img class="qi" src="${it.img64}" alt="Hình minh hoạ bài tập">`:''}</div></div>`;
   if(it.t==='mcq'){const jp=it.tag&&it.tag.includes('jpo');const long=it.o.some(o=>plain(o).length>14);const mx=Math.max(...it.o.map(o=>plain(o).length));const g2=['voc','kw'].includes(s.id);const c=PRINT?(g2?(mx>12?1:(it.o.length===4?2:3)):(mx>30?1:(mx>14?2:(it.o.length===4?4:3)))):(long?1:(it.o.length===4?2:3));
    h+=`<div class="opts ${!long&&!PRINT?'cols':''}" style="--c:${c}">`+it.o.map((o,k)=>`<button type="button" class="opt ${jp?'jp':''}${st.a[id]===k?' sel':''}" data-q="${id}" data-k="${k}"><span class="l">${L[k]}</span><span>${jp?rb(o):esc(o)}</span></button>`).join('')+'</div>'}
   else if(it.t==='fill'){h+=PRINT?`<div class="fill"><div class="line"></div></div>`:`<div class="fill"><input class="jp" data-f="${id}" value="${esc(st.a[id]||'')}" placeholder="Gõ câu trả lời…" autocomplete="off"></div>`}
   else if(it.t==='write'){h+=PRINT?`<div class="fill"><div class="line"></div><div class="line"></div></div>`:`<div class="fill"><textarea class="jp" data-w="${id}" placeholder="Viết câu tiếng Nhật…">${esc(st.a[id]||'')}</textarea><div style="margin-top:6px"><button class="btn" type="button" data-m="${id}">Xem câu mẫu</button></div></div><div class="model jp" id="m${id}">${rb(it.model)}</div>`}
   h+=`<div class="fb" id="fb${id}"></div></div>`});
  h+='</div></section>'});
 $('#body').innerHTML=h;
 if(PRINT){renderKey();return}
 document.querySelectorAll('[data-q]').forEach(b=>b.onclick=()=>{if(st.done)return;const id=b.dataset.q;st.a[id]=+b.dataset.k;save();document.querySelectorAll(`[data-q="${id}"]`).forEach(x=>x.classList.toggle('sel',x===b));prog()});
 document.querySelectorAll('[data-f]').forEach(i=>i.oninput=()=>{st.a[i.dataset.f]=i.value;save();prog()});
 document.querySelectorAll('[data-w]').forEach(i=>i.oninput=()=>{st.a[i.dataset.w]=i.value;save()});
 document.querySelectorAll('[data-m]').forEach(b=>b.onclick=()=>$('#m'+b.dataset.m).classList.toggle('on'));
 document.querySelectorAll('[data-ck]').forEach(c=>c.onchange=()=>{st.a[c.dataset.ck]=c.checked;save()});
 if(st.done)grade();prog()}
function prog(){let n=0,d=0;D.secs.forEach((s,si)=>s.items.forEach((it,ii)=>{if(it.t==='mcq'||it.t==='fill'){n++;const v=st.a[`${si}_${ii}`];if(v!==undefined&&v!=='')d++}}));$('#prog').textContent=`Đã làm ${d}/${n} câu chấm điểm`}
function grade(){let tot=0,ok=0;const per=[];
 D.secs.forEach((s,si)=>{let t=0,o=0;s.items.forEach((it,ii)=>{const id=`${si}_${ii}`,fb=$('#fb'+id),box=$('#it'+id);
  if(it.t==='mcq'){t++;const v=st.a[id];const r=v===it.a;if(r)o++;document.querySelectorAll(`[data-q="${id}"]`).forEach((x,k)=>{x.classList.toggle('right',k===it.a);x.classList.toggle('wrong',k===v&&!r)});
   fb.innerHTML=`${r?'✓ Đúng.':'✗ Đáp án: <b>'+L[it.a]+'</b>.'} ${it.tag&&it.tag.includes('jpo')?'':''}${esc(plain(it.ex||''))}`}
  else if(it.t==='fill'){t++;const v=norm(st.a[id]||'');const r=v&&it.ans.some(a=>norm(a)===v);if(r)o++;const inp=document.querySelector(`[data-f="${id}"]`);inp.classList.toggle('right',!!r);inp.classList.toggle('wrong',!r);
   fb.innerHTML=`${r?'✓ Đúng.':'✗ Đáp án: <b class="jp">'+esc(it.show)+'</b>'} ${esc(it.ex||'')}`}
  else if(it.t==='write'){fb.innerHTML='Tự so với câu mẫu: <span class="jp">'+rb(it.model)+'</span>'}
  if(box)box.classList.add('done')});
  if(t){per.push([s.title,o,t]);tot+=t;ok+=o}});
 $('#res').classList.add('on');$('#res').innerHTML=`<div class="big">${ok}/${tot}</div><div>${esc($('#nm').value||'Học viên')} · Buổi ${D.no} · ${Math.round(ok/tot*100)}%</div><table>${per.map(p=>`<tr><td>${esc(p[0])}</td><td>${p[1]}/${p[2]}</td></tr>`).join('')}</table><p style="color:var(--muted);font-size:13px;margin:10px 0 0">Chụp màn hình kết quả này gửi giáo viên. Câu sai đã tô đỏ, xem giải thích dưới mỗi câu.</p>`;
 $('#res').scrollIntoView({behavior:'smooth'})}
function renderKey(){let h=`<div class="ak"><h2>Đáp án · Buổi ${D.no}</h2><div class="sub">Dành cho giáo viên / tự chấm sau khi làm xong.</div><table>`;
 D.secs.forEach(s=>{if(s.items.every(it=>it.t==='check'))return;h+=`<tr class="sh"><td colspan="3">${esc(s.title)}</td></tr>`;
  s.items.forEach(it=>{if(it.t==='check')return;let a='';
   if(it.t==='mcq')a=`${L[it.a]}. <span class="jp">${rb(it.o[it.a])}</span>`;else if(it.t==='fill')a=`<span class="jp">${esc(it.show)}</span>`;else a=`<span class="jp">${rb(it.model)}</span>`;
   h+=`<tr><td class="n">${it.n}</td><td class="a">${a}</td><td>${esc(plain(it.ex||''))}</td></tr>`})});
 h+='</table></div>';$('#body').insertAdjacentHTML('beforeend',h)}
if(!PRINT){$('#nm').value=st.nm||'';$('#nm').oninput=e=>{st.nm=e.target.value;save()};
 $('#sub').onclick=()=>{st.done=true;save();grade()};
 $('#rs').onclick=()=>{if(confirm('Xoá hết câu trả lời để làm lại?')){st={a:{}};save();$('#res').classList.remove('on');render()}};
 $('#fu').onclick=()=>{document.body.classList.toggle('nofuri');$('#fu').textContent='ふりがな: '+(document.body.classList.contains('nofuri')?'Tắt':'Bật')};
 $('#pr').onclick=()=>window.print()}
render();
'''

def page(s, mode):
    d = json.loads(json.dumps(s))
    for sec in d['secs']:
        for it in sec['items']:
            if it.get('img'): it['img64'] = img64(it['img'])
    title = f'BTVN Buổi {s["no"]:02d} · {s["tv"]}'
    sub = ' · '.join(s['sub'])
    if mode == 'web':
        top = f'''<header class="top"><span class="logo">AT</span><div><b>Anh Trọng Dạy JFT</b><small>Bài tập về nhà · Giáo trình いろどり</small></div></header>
<div class="hero"><div class="k">Buổi {s["no"]:02d} · {html.escape(s["lvj"])} · {html.escape(s["bai"])}</div><h1><span class="jp">{html.escape(s["tj"])}</span>{html.escape(s["tv"])}</h1><div class="sub jp">{html.escape(sub)}</div>
<div class="meta"><input id="nm" placeholder="Họ tên học viên" aria-label="Họ tên học viên"><button class="btn" id="fu" type="button">ふりがな: Bật</button><button class="btn" id="pr" type="button">In</button><span id="prog" style="color:var(--muted);font-size:14px"></span></div></div>
<div class="res" id="res" aria-live="polite"></div>'''
        bar = '<div class="bar"><button class="btn" id="rs" type="button">Làm lại</button><button class="btn pri" id="sub" type="button">Nộp bài & chấm điểm</button></div>'
        css = CSS; bcls = ''
    else:
        top = f'''<header class="top"><span class="logo">AT</span><div><b>Anh Trọng Dạy JFT</b><small>Bài tập về nhà · Giáo trình いろどり</small></div></header>
<div class="hero"><div class="k">Buổi {s["no"]:02d} · {html.escape(s["lvj"])} · {html.escape(s["bai"])} · {s["total"]} câu chấm điểm</div><h1><span class="jp">{html.escape(s["tj"])}</span>{html.escape(s["tv"])}</h1><div class="sub jp">{html.escape(sub)}</div>
<div class="meta"><span>Họ tên:</span><span class="name"></span><span style="margin-left:8mm">Điểm:</span><span class="name" style="min-width:25mm"></span></div></div>'''
        bar = ''; css = CSS + PRINT_CSS; bcls = 'print'
    foot = '<footer>© 2026 Anh Trọng Dạy JFT · 出典：国際交流基金「いろどり 生活の日本語」（ことば・漢字のことば・文法ワークシート・聴解スクリプト）。Câu trắc nghiệm kiểu JFT, câu nhiễu và phần giải thích tiếng Việt do Anh Trọng Dạy JFT soạn.</footer>'
    data = json.dumps(dict(no=s['no'], secs=d['secs']), ensure_ascii=False).replace('</', '<\\/')
    return f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>{css}</style></head>
<body class="{bcls}"><div class="wrap">{top}<div id="body"></div>{foot}</div>{bar}<script type="application/json" id="data">{data}</script><script>{JS}</script></body></html>'''

for s in S:
    fn = f'BTVN_Buoi{s["no"]:02d}'
    open(B + f'out/html/{fn}.html', 'w', encoding='utf-8').write(page(s, 'web'))
    open(B + f'out/print/{fn}.html', 'w', encoding='utf-8').write(page(s, 'print'))
print('ok', len(S))
