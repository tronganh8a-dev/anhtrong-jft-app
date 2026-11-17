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
.gp{margin-top:6px;min-height:690px;grid-auto-rows:1fr}.gp.n2{gap:28px}.gp.n2 .gpi{padding:34px 34px}.gp.n2 .gpi .pt{font-size:44px}.gp.n2 .gpi .eg{font-size:36px}
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
<script>(()=>{const O=document.getElementById('kvo'),BX=O.querySelector('.bx'),NS='http://www.w3.org/2000/svg';let W='',sp=1,tm=[];
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

def build(no, bais, title, sub, kanji, gsel, tables, quizzes_g, plan, ends, fname, basic, listen):
    S = []
    CR = f'<div class="cr">Tổng ôn いろどり 入門 · Buổi {no} · Anh Trọng Dạy JFT · 出典：いろどり 生活の日本語 入門 (Quỹ Giao lưu Quốc tế Nhật Bản), 文法ノート いろどり · nét viết: KanjiVG (CC BY-SA 3.0) · bảng tổng hợp và lưu ý là tự soạn</div>'
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
    S.append(f'''<section class="slide dark"><div class="cover"><img class="lg" src="{LOGO}"><div class="kk">BUỔI {no} · TỔNG ÔN いろどり 入門</div>
<h1>{title}<br><span>{sub}</span></h1><p>Từ vựng · Chữ Hán · Ngữ pháp · 90 phút</p></div>{CR}</section>''')
    sl(f'Nội dung buổi {no} <small>90 phút</small>', '<div class="plan">' + ''.join(f'<div><b>{m}′</b><h3>{h}</h3><p>{p}</p></div>' for m, h, p in plan) + '</div>')

    # 2. Từ vựng
    sl('', f'<div class="sec"><div class="n">01</div><div class="t">Từ vựng</div><div class="j">ことば</div><div class="d">Nhìn tranh – đọc từ – bấm thẻ để xem nghĩa</div><div class="tm">{plan[0][0]} phút</div></div>')
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

    # 3. Chữ Hán
    sl('', f'<div class="sec"><div class="n">02</div><div class="t">Chữ Hán</div><div class="j">かんじ</div><div class="d">Âm Hán Việt · cách đọc · nghĩa · câu ví dụ</div><div class="tm">{plan[1][0]} phút</div></div>')
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
            return f'<div class="kc" style="--ks:{ksz}px">{kb}<div class="k"{" style=white-space:nowrap" if L <= 5 else ""}>{html.escape(k["w"])}</div><div class="st"><div class="hv">{html.escape(k["hv"])}</div><div class="rd jp">{html.escape(k["r"])}</div><div class="mn">{html.escape(k["vi"])}</div>{f"<div class=cs>{cs}</div>" if cs else ""}{ex}</div></div>'
        sl(f'Chữ Hán <small>{gt}</small>', f'<div class="kg c{min(n, 5) if n != 7 else 7}">' + ''.join(kcard(k) for k in ks) + '</div>')
    allk = [k for grp, _ in kanji for k in KAN if k['w'] in grp and k.get('rd')]
    pick = [allk[3], allk[len(allk) // 2], allk[-4]]
    for i, k in enumerate(pick[:2] if basic else pick):
        opts, a = shuf(k['r'], k['rd'], i + 2)
        quiz('Chữ Hán này đọc thế nào?', [html.escape(o) for o in opts], a, f'{html.escape(k["w"])} đọc là <b>{html.escape(k["r"])}</b> ({html.escape(k["hv"])}) – {html.escape(k["vi"])}', 'Chữ Hán いろどり 入門', big=html.escape(k['w']))
    kw = [k for k in allk if k.get('wk')]
    for i, k in enumerate([kw[1], kw[-2]] if not basic else [kw[5]]):
        opts, a = shuf(k['w'], k['wk'], i + 3)
        quiz('Chọn chữ Hán đúng.', [html.escape(o) for o in opts], a, f'<b>{html.escape(k["w"])}</b> ({html.escape(k["hv"])}) – {html.escape(k["vi"])}', 'Chữ Hán いろどり 入門', big=html.escape(k['r']))

    # 4. Ngữ pháp
    sl('', f'<div class="sec"><div class="n">03</div><div class="t">Ngữ pháp</div><div class="j">ぶんぽう</div><div class="d">Mẫu câu – nghĩa – câu ví dụ trong sách</div><div class="tm">{plan[2][0]} phút</div></div>')
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

    # 5. Nghe hiểu (câu lấy từ ngân hàng đề trong app)
    sl('', f'<div class="sec"><div class="n">04</div><div class="t">Nghe hiểu</div><div class="j">ちょうかい</div><div class="d">Đọc câu hỏi trước → nghe → chọn đáp án</div><div class="tm">{plan[3][0]} phút</div></div>')
    for j, (eid, qi) in enumerate(listen):
        e = EXAMS[eid]; q = e['qs'][qi]; ks = 'abcd'; a = q['a'][0]
        hasimg = any(o.get('img') for o in q['o'])
        ob = ''.join(f'<button class="o{" oi" if hasimg else ""}" data-k="{ks[i]}">{f"<img src={chr(34)}{pimg(o[chr(105)+chr(109)+chr(103)], 360)}{chr(34)}>" if o.get("img") else ""}<b>{ks[i]}</b><span class="jp ot">{o["t"]}</span><i></i><em></em></button>' for i, o in enumerate(q['o']))
        op = f'<div class="opts {"oimg" if hasimg else "list"}" data-a="{ks[a]}">{ob}</div>'
        pic = ''.join(f'<img class="lpic" src="{pimg(x)}">' for x in (q.get('imgs') or []))
        body = f'<div class="lsn"><audio controls preload="none" src="{aud(q["au"])}"></audio></div>' + (f'<div class="qi">{pic}{op}</div>' if pic else op)
        S.append(f'<section class="slide qz ls"><div class="kk2">Nghe hiểu {j + 1} <span class="src">Nguồn: {html.escape(e["title"])} · câu {qi + 1} (app luyện thi)</span></div><h2 class="jp q">{q["t"]}</h2>{body}<div class="ex lex">{q.get("ex", "")}</div><button class="lsb" onclick="this.previousElementSibling.classList.toggle(&quot;open&quot;)">📄 Script</button>{CR}</section>')

    # 6. Kết
    sl(f'Tổng kết buổi {no}', ends)
    S.append(f'''<section class="slide dark"><div class="cover"><img class="lg" src="{LOGO}"><div class="kk">おつかれさまでした！</div>
<h1>Hết buổi {no}<br><span>{"Hẹn gặp lại ở buổi 2" if no == 1 else "Buổi sau: いろどり 初級1"}</span></h1>
<p>Ôn lại trên app: Tài liệu → Từ vựng · Chữ Hán · Ngữ pháp (入門)</p></div>{CR}</section>''')
    out = HEAD.replace('<title>Kính ngữ trong JFT-Basic</title>', f'<title>Buổi {no} · Tổng ôn いろどり 入門</title>') + ''.join(S) + '<script>window.KVG=' + json.dumps({c: KVG[c] for c in set(''.join(k['w'] for g_, _ in kanji for k in KAN if k['w'] in g_)) if c in KVG}, ensure_ascii=False, separators=(',', ':')) + '</script>' + KVGJS + TAIL + VSTEP
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
  [(20, 'Từ vựng', 'Bài 4–9: gia đình, món ăn, nhà ở, giờ giấc'), (15, 'Chữ Hán', '32 từ chữ Hán + nét viết'),
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
build(2, range(10, 19), 'Tổng ôn 入門', 'Bài 10 – 18', [
    (['読みます', '聞きます', '見ます', '本', '友だち'], 'Hoạt động'),
    (['何', '年', '月', '日', '今日'], 'Ngày tháng'),
    (['今週', '今度', '来週', '休み', '予定'], 'Lịch hẹn'),
    (['東', '南', '会社', '来ます', '行きます'], 'Đi lại'),
    (['乗ります', '会います', '入ります', '買います', '旅行します'], 'Động từ'),
    (['大きい', '小さい', '高い', '低い', '安い'], 'Tính từ'),
    (['前', '後ろ', '横', '入口', '出口'], 'Vị trí · lối đi'),
    (['階', '押す', '引く', '映画', '温泉'], 'Toà nhà · giải trí'),
    (['一、二、三、四、五、六、七、八、九、十', '百', '千', '万', '円'], 'Số đếm · tiền'),
    (['日本語', '勉強します'], 'Học tập'),
  ], [
    (10, ['❶', '❷', '❸'], {'❶': 'Thể て: học kỹ ở 初級1'}),
    (11, ['❷', '❸', '❹', '❺'], {}),
    (12, ['❶', '❸', '❹', '❺'], {'❶': 'Nơi diễn ra sự kiện dùng で'}),
    (13, ['❶', '❸', '❹', '❺', '❻'], {}),
    (14, ['❶', '❷', '❸'], {'❸': 'な-A + な + N · い-A + N'}),
    (15, ['❶', '❷'], {}),
    (16, ['❶', '❷', '❸'], {}),
    (17, ['❶', '❷', '❸', '❹', '❺'], {'❸': 'いい → よかったです'}),
    (18, ['❶', '❷', '❸', '❹', '❺', '❻'], {'❶': 'Bỏ ます + たいです'}),
  ], tab2, [(10, '❶', 0), (12, '❸', 0), (13, '❸', 0), (14, '❸', 0), (17, '❸', 0), (18, '❶', 0)],
  [(20, 'Từ vựng', 'Bài 10–18: đồ dùng, sở thích, đi lại, mua sắm, du lịch'), (15, 'Chữ Hán', 'Số đếm, tiền, ngày tháng, đi lại + nét viết'),
   (40, 'Ngữ pháp', 'て-ください, rủ rê, trợ từ, こそあ, quá khứ, たい'), (15, 'Nghe hiểu', '4 câu: giá tiền, giờ hẹn, du lịch')],
  '<div class="kgr g2"><div class="kcd kb"><h3>Đã ôn</h3><ul class="ck"><li>V-てください · V-ませんか · V-ましょう</li><li>Trợ từ に・で・へ・を</li><li>こ・そ・あ・ど · いくら</li><li>Quá khứ: ました・でした・かったです</li><li>V-たいです · từ nối câu</li></ul></div>'
  '<div class="kcd kp"><h3>Bài tập về nhà</h3><ul class="ck"><li>App → Tài liệu → Từ vựng 入門 Bài 10–18</li><li>Chữ Hán: luyện cách đọc + chọn chữ</li><li>Làm đề: phần 会話と表現</li></ul></div></div>',
  'Buoi02_TongOn_NhapMon_2.html', False, [('jft-f5', 31), ('jft-y3', 27), ('jft-ln1', 18), ('jft-ln1', 19)])
