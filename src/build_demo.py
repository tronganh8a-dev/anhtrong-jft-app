#!/usr/bin/env python3
# Dựng bản DÙNG THỬ (không đăng nhập) → ../demo/public
# Hiện ĐỦ danh mục mọi phần nhưng KHOÁ hết, mỗi phần chỉ mở mục đầu tiên (mục mặc định khi mở tab).
# Mục bị khoá chỉ mang tiêu đề / số đếm (dữ liệu rỗng) – nội dung thật KHÔNG được chép sang bản dùng thử.
import os, json, shutil, re
A = os.path.dirname(os.path.abspath(__file__)) + '/'
P = A + '../public/'; D = A + '../demo/public/'
if os.path.exists(D): shutil.rmtree(D)
os.makedirs(D + 'app/data')
def load(f):
    s = open(P + 'app/data/' + f, encoding='utf-8').read()
    return s[s.index('=') + 1:s.index(';window.EXTLINKS') if 'EXTLINKS' in s else s.rindex(';')]
def save(f, var, obj, extra=''):
    open(D + 'app/data/' + f, 'w', encoding='utf-8').write(f'window.{var}=' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + ';' + extra)
def cp(rel):
    if rel and os.path.exists(P + rel):
        os.makedirs(os.path.dirname(D + rel), exist_ok=True); shutil.copy(P + rel, D + rel)

# Slide bài giảng: mở 初級1 Bài 1
L = json.loads(load('lessons.js')); L0 = next(l for l in L if l['lv'] == 's1' and l['bai'] == min(x['bai'] for x in L if x['lv'] == 's1'))
save('lessons.js', 'LESSONS', L)
for k in ('web', 'slide'): cp(L0.get(k))
S = [q for q in json.loads(load('skills.js')) if q['lv'] == L0['lv'] and q['bai'] == L0['bai']]
save('skills.js', 'SKILLS', S)
# Làm đề: mở đề đầu tiên, các đề khác chỉ giữ tiêu đề + số câu
E = json.loads(load('exams.js'))
save('exams.js', 'EXAMS', [e if i == 0 else {**{k: v for k, v in e.items() if k != 'qs'}, 'qs': [], 'nq': len(e['qs'])} for i, e in enumerate(E)], 'window.EXTLINKS=[];')
# Ngữ pháp (文法ノート): mở bài đầu của 初級1 (mặc định khi mở tab)
G = json.loads(load('grammar.js')); g0 = min(g['bai'] for g in G if g['lv'] == '初級1')
save('grammar.js', 'GRAMMAR', [g if (g['lv'] == '初級1' and g['bai'] == g0) else {**g, 'points': []} for g in G])
# Từ vựng (flashcard): mở 初級1 Bài 1; bài khác chỉ là chỗ giữ (để hiện số từ / nút bài)
VV = json.loads(load('vocab.js')); W = []
for w in VV['words']:
    op = [x for x in w['l'] if x[0] == '初級1' and x[1] == 1]
    if op: W.append({**w, 'l': op})
    for x in w['l']:
        if not (x[0] == '初級1' and x[1] == 1): W.append({'h': '', 'y': '', 'v': '', 'l': [x], 'lock': 1})
EXS = VV.get('ex', []); EX2 = []
for w in W:
    if not w.get('lock') and w.get('x') is not None and w['x'] < len(EXS):
        EX2.append(EXS[w['x']]); w['x'] = len(EX2) - 1
save('vocab.js', 'VOCAB', {'words': W, 'ex': EX2})
# Video: mở video đầu tiên
V = json.loads(load('videos.js'))
save('videos.js', 'VIDEOS', [{**v, 'slides': [], 'learn': []} if i == 0 else {**v, 'yt': '', 'docs': [], 'slides': [], 'learn': []} for i, v in enumerate(V)])
# Tài liệu (từ vựng / chữ Hán / ngữ pháp): mở nhóm đầu của 入門
DD = json.loads(load('docs.js'))
b0 = min(w['b'] for w in DD['vocab']['入門']); gb0 = min(p['bai'] for p in DD['gram']['入門'])
save('docs.js', 'DOCS', dict(
    vocab={k: [w if (k == '入門' and w['b'] == b0) else {'b': w['b'], 'w': '', 'wr': '', 'vi': ''} for w in v] for k, v in DD['vocab'].items()},
    kanji={k: [x if (k == '入門' and i < 20) else {'w': '', 'wr': '', 'r': '', 'vi': ''} for i, x in enumerate(v)] for k, v in DD['kanji'].items()},
    gram={k: [p if (k == '入門' and p['bai'] == gb0) else {'bai': p['bai'], 'n': p.get('n', ''), 'p': '', 'm': ''} for p in v] for k, v in DD['gram'].items()}))
# Bài tập về nhà: mở buổi đầu
H = json.loads(load('hw.js')); save('hw.js', 'HW', H)
cp(H[0]['html']); cp(H[0]['pdf'])
# media: chỉ file dùng trong phần mở
for w in W:
    if w.get('au'): cp(f"app/media/vau/{w['au']}.mp3")
blob = ''.join(open(D + 'app/data/' + f, encoding='utf-8').read() for f in os.listdir(D + 'app/data'))
n = 0
for root, _, fs in os.walk(P + 'app/media'):
    for f in fs:
        rel = os.path.relpath(os.path.join(root, f), P)
        if rel.startswith('app/media/cover/') or rel in blob or f in blob or ('gimg' in rel and '"'+os.path.splitext(f)[0]+'"' in blob):
            cp(rel); n += 1
s = open(P + 'index.html', encoding='utf-8').read()
# Theo buổi học: mở tài liệu đầu tiên
t0 = re.search(r"\{f:'(tailieu/[^']+)'", s).group(1); cp(t0)
FB = 'https://www.facebook.com/anh.trongg.2024/'; TT = 'https://www.tiktok.com/@anhtrong.daygino'
LOCK_CSS = '''<style>
.lockd{position:relative;opacity:.55;filter:grayscale(.35);cursor:pointer!important}.lockd *{pointer-events:none}
.lc.lockd .ttl::before,.vit.lockd .bd b::before,.ec.lockd b::before,.exb.lockd .k::before,.chip.lockd::before,.dk.lockd::before{content:"🔒 "}
.dlock{background:var(--paper);border:1.5px dashed #e3b04b;border-radius:18px;padding:26px 22px;text-align:center;margin:8px 0}
.dlock .ic{font-size:40px}.dlock b{display:block;font-size:19px;margin:6px 0}.dlock p{color:var(--muted);font-weight:600;margin:0 auto 14px;max-width:560px;line-height:1.55}
.dlock .cta{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}.dlock .cta a{border-radius:12px;padding:11px 16px;font-weight:800;text-decoration:none;color:#fff;background:#1877f2}.dlock .cta a.tt{background:#111}
#dmodal{position:fixed;inset:0;z-index:200;background:rgba(15,23,42,.5);display:none;align-items:center;justify-content:center;padding:16px}#dmodal.on{display:flex}
#dmodal .dlock{max-width:480px;width:100%;border-style:solid;box-shadow:0 20px 50px rgba(0,0,0,.3);position:relative}#dmodal .x{position:absolute;right:10px;top:6px;border:0;background:none;font-size:28px;color:var(--muted);cursor:pointer}
.vit .now.soonb{display:none}
</style>'''
PANEL = f'<div class="ic">🔒</div><b>Phần này dành cho học viên khoá học</b><p>Bản dùng thử chỉ mở <b>mục đầu tiên</b> của mỗi phần. Vào lớp để mở toàn bộ: 42 bài slide, 11 đề thi có giải thích, video bài giảng, 3.800+ từ vựng, chữ Hán, ngữ pháp, bài tập về nhà.</p><div class="cta"><a href="{FB}" target="_blank" rel="noopener">💬 Nhắn tin Facebook</a><a class="tt" href="{TT}" target="_blank" rel="noopener">♪ TikTok @anhtrong.daygino</a></div>'
LOCK_JS = '''<div id="dmodal"><div class="dlock"><button class="x" type="button" aria-label="Đóng">×</button>__PANEL__</div></div>
<script>(()=>{const PANEL=`<div class="dlock">__PANEL__</div>`;const M=document.getElementById('dmodal');
M.onclick=e=>{if(e.target===M||e.target.closest('.x'))M.classList.remove('on')};
document.addEventListener('click',e=>{const l=e.target.closest('.lockd');if(l){e.preventDefault();e.stopPropagation();M.classList.add('on')}},true);
const L=(el,on)=>el&&el.classList.toggle('lockd',!!on);
const panel=el=>{if(el&&!el.querySelector(':scope>.dlock'))el.innerHTML=PANEL};
let busy=false,q=false;
function apply(){q=false;busy=true;try{
 document.querySelectorAll('#lgrid .lc').forEach((c,i)=>L(c,!(lvL==='s1'&&i===0)));
 document.querySelectorAll('#dDoc .bgrp .lc').forEach((c,i)=>L(c,i!==0));
 if(window.DOCS&&['vocab','kanji','gram'].includes(dTab)&&document.querySelector('#dGrps .chip')){
  if(dTab==='gram'&&dGrp['gram入門']===undefined){dGrp['gram入門']=Math.min(...DOCS.gram['入門'].map(p=>p.bai));busy=false;renderDocs();return}
  const lv=dLv[dTab],open=dTab==='gram'?1:0,ch=[...document.querySelectorAll('#dGrps .chip')];
  ch.forEach((c,i)=>L(c,!(lv==='入門'&&i===open)));
  if(!(lv==='入門'&&ch[open]&&ch[open].classList.contains('on')))panel(document.getElementById('dBody'))}
 document.querySelectorAll('#examList [data-ex]').forEach(b=>L(b,b.dataset.ex!=='0'));
 const gl=[...document.querySelectorAll('#baiGram .chip')];gl.forEach((c,i)=>L(c,!(gLv==='初級1'&&i===0)));
 if(gl.length&&!(gLv==='初級1'&&gl[0].classList.contains('on')))panel(document.getElementById('gArea'));
 document.querySelectorAll('.vgrid .vit').forEach((c,i)=>L(c,i!==0));
 const vl=[...document.querySelectorAll('#baiVocab .chip')];vl.forEach((c,i)=>L(c,!(vLv==='初級1'&&i===0)));
 if(vl.length&&!(vLv==='初級1'&&vl[0].classList.contains('on'))){panel(document.getElementById('vArea'));const wl=document.getElementById('wl');if(wl&&wl.children.length)wl.innerHTML=''}
 document.querySelectorAll('#hwList .ec').forEach((c,i)=>L(c,i!==0));
}finally{busy=false}}
new MutationObserver(()=>{if(!busy&&!q){q=true;requestAnimationFrame(apply)}}).observe(document.querySelector('main'),{childList:true,subtree:true});
apply()})();</script>'''.replace('__PANEL__', PANEL)
reps = [("$('#logout').onclick=()=>{location.href='/logout'};", "$('#logout').style.display='none';"),
        ('<main>', '<main><div style="background:#fff3b0;border:1px solid #f1c48b;color:#5a4300;border-radius:12px;padding:10px 14px;margin:0 0 14px;font-size:14px"><b>BẢN DÙNG THỬ</b> · Mỗi phần chỉ mở <b>mục đầu tiên</b>, các mục có 🔒 dành cho học viên. Liên hệ <b>Anh Trọng Dạy JFT</b> để vào lớp và mở toàn bộ: 42 bài, 11 đề có giải thích, video bài giảng, 3.800+ từ.</div>'),
        ('<title>', '<title>Dùng thử · '),
        ('</head>', LOCK_CSS + '</head>'),
        ('</body>', LOCK_JS + '</body>')]
for a, b in reps:
    assert s.count(a) >= 1, a; s = s.replace(a, b, 1)
# bỏ mục đăng nhập / đăng ký tài khoản (Prometric) ở trang chủ
s2 = re.sub(r'<a class="pbtn c3"[\s\S]*?</a>\s*<a class="pbtn c4"[\s\S]*?</a>', '', s, count=1)
assert s2 != s, 'không thấy nút đăng ký / đăng nhập'; s = s2
s = s.replace('Chưa có tài khoản Prometric thì đăng ký trước, sau đó đăng nhập để đặt / xem lịch thi.', '')
open(D + 'index.html', 'w', encoding='utf-8').write(s)
print('demo: mở', L0['lv'], 'Bài', L0['bai'], '· đề 1/', len(E), '· ngữ pháp 初級1 Bài', g0, '· từ vựng 初級1 Bài 1 (', sum(1 for w in W if not w.get('lock')), 'từ ) · tài liệu', t0, '·', n, 'media')

# Bản sao trong public/_demo: worker chính (worker.js) phục vụ thư mục này khi truy cập bằng tên miền jft-dungthu.*
DD2 = P + '_demo/'
if os.path.exists(DD2): shutil.rmtree(DD2)
shutil.copytree(D, DD2)
