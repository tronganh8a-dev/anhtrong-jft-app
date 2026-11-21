#!/usr/bin/env python3
# Dựng bản DÙNG THỬ (không đăng nhập) → ../demo/public
# Hiện ĐỦ danh mục mọi phần; 19/11: mỗi phần mở 1/3 đầu, Làm đề mở 2 đề đầu (21/11), còn lại KHOÁ (🔒 + popup liên hệ).
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

# 19/11: mỗi phần mở 1/3 đầu (làm tròn lên); Làm đề mở 2 đề đầu (21/11: Đề 1 + Đề 2).
# File nội dung lớn (bài học, tài liệu, BTVN, media) KHÔNG chép sang bản dùng thử nữa: build ghi danh sách file được mở
# vào demo_allow.js, worker.js chỉ phục vụ đúng các file đó từ bản chính cho tên miền jft-dungthu.*
import math
third = lambda n: max(1, math.ceil(n / 3))
ALLOW = set()
def allow(rel):
    if rel and os.path.exists(P + rel): ALLOW.add(rel)
def first(xs): xs = sorted(set(xs)); return xs[:third(len(xs))]
# Slide bài giảng: mỗi cấp mở 1/3 số bài đầu
L = json.loads(load('lessons.js'))
OL = {lv: first(l['bai'] for l in L if l['lv'] == lv) for lv in dict.fromkeys(l['lv'] for l in L)}
save('lessons.js', 'LESSONS', L)
for l in L:
    if l['bai'] in OL[l['lv']]:
        for k in ('web', 'slide'): allow(l.get(k))
S = [q for q in json.loads(load('skills.js')) if q['bai'] in OL.get(q['lv'], [])]
save('skills.js', 'SKILLS', S)
# Làm đề: 21/11 anh chốt mở đủ Đề 1, Đề 2 (Đề 2 = jft-y4, Đề 29 cũ) + 1 đề nghe (Đề nghe 1) + 1 đề từ vựng (Ôn tập từ vựng & Hán tự),
# 4 đề này đưa lên đầu thành nhóm "Làm thử miễn phí" (ngay dưới Đề 1, Đề 2); các đề khác chỉ giữ tiêu đề + số câu
E = json.loads(load('exams.js'))
OPEN_EX = ['jft-y3', 'jft-y4', 'jft-y5', 'jft-ln1', 'jft-ln2', 'jft-vocab']   # 21/11 tối: đề thứ 3 = Đề 30 mới (jft-y5, bản chính là Đề 4) + Đề nghe 2
HIDE_EX = {'jft-f1'}   # 21/11: anh bảo ẩn Đề 27 ở bản dùng thử
_by = {e['id']: e for e in E}
E = [_by[i] for i in OPEN_EX if i in _by] + [e for e in E if e['id'] not in OPEN_EX and e['id'] not in HIDE_EX]
# bản dùng thử: jft-y5 ghi "Đề 3", Đề 3 bản chính (jft-f3) ghi "Đề 4" (dòng "Nguồn: Đề 3/4 · câu x" đổi số theo)
_DT = {'jft-y5': 'Đề 3', 'jft-f3': 'Đề 4'}
for e in E:
    if e['id'] in _DT: e['title'] = _DT[e['id']]
    for q in e.get('qs', []):
        if isinstance(q.get('src'), str): q['src'] = re.sub(r'Đề ([34]) · câu', lambda m: 'Đề ' + ('4' if m.group(1) == '3' else '3') + ' · câu', q['src'])
NEX = sum(1 for i in OPEN_EX if i in _by)
for e in E[:NEX]:
    e['group'] = 'Làm thử miễn phí'
    if e['id'] in ('jft-ln1', 'jft-ln2'): e['name'] = 'nghe ' + e['id'][-1]   # thẻ hiện "Đề nghe 1/2" (không bị đọc thành "Đề 1/2")
save('exams.js', 'EXAMS', [e if i < NEX else {**{k: v for k, v in e.items() if k != 'qs'}, 'qs': [], 'nq': len(e['qs'])} for i, e in enumerate(E)], 'window.EXTLINKS=[];')
# Ngữ pháp (文法ノート): mỗi cấp mở 1/3 số bài đầu
G = json.loads(load('grammar.js'))
OG = {lv: first(g['bai'] for g in G if g['lv'] == lv) for lv in dict.fromkeys(g['lv'] for g in G)}
save('grammar.js', 'GRAMMAR', [g if g['bai'] in OG[g['lv']] else {**g, 'points': []} for g in G])
# Từ vựng (flashcard): mỗi cấp mở 1/3 số bài đầu; bài khác chỉ là chỗ giữ (để hiện số từ / nút bài)
VV = json.loads(load('vocab.js')); W = []
OV = {}
for w in VV['words']:
    for x in w['l']: OV.setdefault(x[0], set()).add(x[1])
OV = {k: first(v) for k, v in OV.items()}
isop = lambda x: x[1] in OV.get(x[0], [])
for w in VV['words']:
    op = [x for x in w['l'] if isop(x)]
    if op: W.append({**w, 'l': op})
    for x in w['l']:
        if not isop(x): W.append({'h': '', 'y': '', 'v': '', 'l': [x], 'lock': 1})
EXS = VV.get('ex', []); EX2 = []
for w in W:
    if not w.get('lock') and w.get('x') is not None and w['x'] < len(EXS):
        EX2.append(EXS[w['x']]); w['x'] = len(EX2) - 1
save('vocab.js', 'VOCAB', {'words': W, 'ex': EX2})
for w in W:
    if w.get('au'): allow(f"app/media/vau/{w['au']}.mp3")
# Video: mỗi khoá mở 1/3 số video đã có (video MỚI NHẤT trước – trang video mặc định mở video mới nhất)
V = json.loads(load('videos.js')); OVID = []
for sr in dict.fromkeys(v.get('series') for v in V):
    has = [v['id'] for v in V if v.get('series') == sr and (v.get('yt') or v.get('gd'))]
    if has: OVID += has[-third(len(has)):]
def vlock(v): return {**{k: x for k, x in v.items() if k != 'gd'}, 'yt': '', 'docs': [], 'slides': [], 'learn': []}
save('videos.js', 'VIDEOS', [v if v['id'] in OVID else vlock(v) for v in V])
for v in V:
    if v['id'] in OVID:
        for x in v.get('slides') or []: allow(x.get('u'))
# Tài liệu › Từ vựng / Chữ Hán: mỗi cấp mở 1/3 số bài (từ vựng) / số nhóm 20 chữ (chữ Hán)
DD = json.loads(load('docs.js'))
ODV = {k: first(w['b'] for w in v) for k, v in DD['vocab'].items()}
ODK = {k: third(math.ceil(len(v) / 20)) for k, v in DD['kanji'].items()}
gb0 = min(p['bai'] for p in DD['gram']['入門'])
save('docs.js', 'DOCS', dict(
    vocab={k: [w if w['b'] in ODV[k] else {'b': w['b'], 'w': '', 'wr': '', 'vi': ''} for w in v] for k, v in DD['vocab'].items()},
    kanji={k: [x if i < ODK[k] * 20 else {'w': '', 'wr': '', 'r': '', 'vi': ''} for i, x in enumerate(v)] for k, v in DD['kanji'].items()},
    gram={k: [p if (k == '入門' and p['bai'] == gb0) else {'bai': p['bai'], 'n': p.get('n', ''), 'p': '', 'm': ''} for p in v] for k, v in DD['gram'].items()}))
# Bài tập về nhà: mở 1/3 số buổi đầu
H = json.loads(load('hw.js')); save('hw.js', 'HW', H)
OHW = first(h['no'] for h in H)
for h in H:
    if h['no'] in OHW: allow(h.get('html')); allow(h.get('pdf'))
s = open(P + 'index.html', encoding='utf-8').read()
# Theo buổi học: mở 1/3 số tài liệu đầu (theo thứ tự hiện trên trang)
bsrc = s[s.index('const BUOI=['):s.index('function renderBuoi')]
items, cur, idx = [], None, 0
for m in re.finditer(r"\{n:(-?\d+),|\{f:'([^']+)'", bsrc):
    if m.group(1) is not None: cur, idx = m.group(1), 0
    else: items.append((f'{cur}|{idx}', m.group(2))); idx += 1
OB = items[:third(len(items))]
for _, f in OB: allow(f)
# 21/11: video kỹ năng làm bài đọc hiểu (đặt dưới nhóm 4 đề làm thử ở tab Làm đề)
DHV = 'app/media/video/DocHieuJFT_KyNang'
allow(DHV + '.mp4'); allow(DHV + '.jpg')
# media trong file HTML được mở (vd ảnh ../app/media/doc/… của tài liệu Buổi 11)
for rel in list(ALLOW):
    if rel.endswith('.html'):
        h = open(P + rel, encoding='utf-8', errors='ignore').read()
        for m in set(re.findall(r'(?<![\w/])(?:\.\./|/)?(app/media/[\w./-]+\.(?:jpg|jpeg|png|webp|gif|svg|mp3|m4a|wav|mp4))', h)): allow(m)
# media được dữ liệu bản dùng thử nhắc tới
blob = ''.join(open(D + 'app/data/' + f, encoding='utf-8').read() for f in os.listdir(D + 'app/data'))
PFX = ['app/media/cover/', 'app/media/news/', 'app/media/brand/', 'n3/', 'app/media/gino/']   # 21/11: mở full JLPT N3
for root, _, fs in os.walk(P + 'app/media'):
    for f in fs:
        rel = os.path.relpath(os.path.join(root, f), P)
        if any(rel.startswith(x) for x in PFX): continue
        if rel in blob or f in blob or (('gimg' in rel or 'vau' in rel) and '"' + os.path.splitext(f)[0] + '"' in blob): ALLOW.add(rel)
open(A + '../demo_allow.js', 'w', encoding='utf-8').write(
    '// SINH RA bởi src/build_demo.py – file bản chính được phép phục vụ cho bản dùng thử (jft-dungthu.*). Đừng sửa tay.\n'
    'export default ' + json.dumps({'p': PFX, 'f': sorted(ALLOW)}, ensure_ascii=False, separators=(',', ':')) + ';\n')
DOPEN = {'les': OL, 'gram': OG, 'voc': OV, 'dv': ODV, 'dk': ODK, 'vid': OVID, 'hw': OHW, 'buoi': [k for k, _ in OB], 'ex': NEX}
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
PANEL = f'<div class="ic">🔒</div><b>Phần này dành cho học viên khoá học</b><p>Bản dùng thử mở <b>6 đề làm thử</b> và <b>1/3 nội dung</b> các phần khác. Vào lớp để mở toàn bộ: slide bài giảng, toàn bộ đề thi có giải thích, video bài giảng, 3.800+ từ vựng, chữ Hán, ngữ pháp, bài tập về nhà.</p><div class="cta"><a href="{FB}" target="_blank" rel="noopener">💬 Nhắn tin Facebook</a><a class="tt" href="{TT}" target="_blank" rel="noopener">♪ TikTok @anhtrong.daygino</a></div>'
LOCK_JS = '''<div id="dmodal"><div class="dlock"><button class="x" type="button" aria-label="Đóng">×</button>__PANEL__</div></div>
<script>(()=>{const PANEL=`<div class="dlock">__PANEL__</div>`;const M=document.getElementById('dmodal');
M.onclick=e=>{if(e.target===M||e.target.closest('.x'))M.classList.remove('on')};
document.addEventListener('click',e=>{const l=e.target.closest('.lockd');if(l){e.preventDefault();e.stopPropagation();M.classList.add('on')}},true);
const L=(el,on)=>el&&el.classList.toggle('lockd',!!on);
const panel=el=>{if(el&&!el.querySelector(':scope>.dlock'))el.innerHTML=PANEL};
let busy=false,q=false;
function apply(){q=false;busy=true;try{const O=window.DOPEN,has=(m,k,v)=>(m[k]||[]).includes(v),act=ch=>{const on=ch.find(c=>c.classList.contains('on'));return !on||on.classList.contains('lockd')};
 document.querySelectorAll('#lgrid .lc').forEach(c=>{const b=c.querySelector('[data-skill]');const[lv,bai]=b?b.dataset.skill.split('|'):[];L(c,!(b&&has(O.les,lv,+bai)))});
 document.querySelectorAll('#dDoc .bgrp .lc').forEach(c=>{const b=c.querySelector('[data-bd]');L(c,!(b&&O.buoi.includes(b.dataset.bd)))});
 if(window.DOCS&&['vocab','kanji'].includes(dTab)){const ch=[...document.querySelectorAll('#dGrps .chip')];if(ch.length){const lv=dLv[dTab];
  ch.forEach(c=>{const g=+c.dataset.g;L(c,!(dTab==='vocab'?has(O.dv,lv,g):g<(O.dk[lv]||0)))});if(act(ch))panel(document.getElementById('dBody'))}}
 document.querySelectorAll('#examList [data-ex]').forEach(b=>L(b,+b.dataset.ex>=O.ex));
 const gl=[...document.querySelectorAll('#baiGram .chip')];gl.forEach(c=>L(c,!has(O.gram,gLv,+c.dataset.b)));
 if(gl.length&&act(gl))panel(document.getElementById('gArea'));
 document.querySelectorAll('.vgrid .vit').forEach(c=>L(c,!O.vid.includes(c.dataset.vid)));
 const vl=[...document.querySelectorAll('#baiVocab .chip')];vl.forEach(c=>L(c,!has(O.voc,vLv,+c.dataset.b)));
 if(vl.length&&act(vl)){panel(document.getElementById('vArea'));const wl=document.getElementById('wl');if(wl&&wl.children.length)wl.innerHTML=''}
 document.querySelectorAll('#hwList .ec').forEach(c=>{const b=c.querySelector('[data-hw]');L(c,!(b&&O.hw.includes(+b.dataset.hw)))});
}finally{busy=false}}
new MutationObserver(()=>{if(!busy&&!q){q=true;requestAnimationFrame(apply)}}).observe(document.querySelector('main'),{childList:true,subtree:true});
apply()})();</script>'''.replace('__PANEL__', PANEL).replace('<script>(()=>{', '<script>window.DOPEN=' + json.dumps(DOPEN, ensure_ascii=False, separators=(',', ':')) + ';(()=>{', 1)
reps = [("$('#logout').onclick=()=>{location.href='/logout'};", "$('#logout').style.display='none';"),
        # 21/11: anh bảo xoá khung vàng "BẢN DÙNG THỬ", thay bằng dòng liên hệ sensei (Facebook + TikTok)
        ('<main>', f'<main><div class="dct"><b>Liên hệ sensei</b><a class="fb" href="{FB}" target="_blank" rel="noopener">Facebook</a><a class="tt" href="{TT}" target="_blank" rel="noopener">TikTok @anhtrong.daygino</a></div>'),
        ('<title>', '<title>Dùng thử · '),
        ('</head>', LOCK_CSS + '</head>'),
        ('</body>', LOCK_JS + '</body>'),
        # JLPT N3: 21/11 anh mở FULL trong bản dùng thử (trước 12/11 chỉ hiện khung khoá) → giữ iframe n3/, worker phục vụ thư mục n3/ của bản chính
        ]
for a, b in reps:
    assert s.count(a) >= 1, a; s = s.replace(a, b, 1)
# bỏ mục đăng nhập / đăng ký tài khoản (Prometric) ở trang chủ
s2 = re.sub(r'<a class="pbtn c3"[\s\S]*?</a>\s*<a class="pbtn c4"[\s\S]*?</a>', '', s, count=1)
assert s2 != s, 'không thấy nút đăng ký / đăng nhập'; s = s2
s = s.replace('Chưa có tài khoản Prometric thì đăng ký trước, sau đó đăng nhập để đặt / xem lịch thi.', '')
s = s.replace('function ggShow(){', 'function ggShow(){return;', 1)  # bản dùng thử: không hiện popup chữ
# 19/11: nhớ video đang xem bằng khoá riêng (khoá cũ có thể trỏ vào video nay đã khoá); trắc nghiệm từ vựng không lấy từ bị khoá (rỗng) làm phương án nhiễu
s = s.replace("store.get('jftVid')", "store.get('jftVidT')").replace("store.set('jftVid',", "store.set('jftVidT',")
_o = 'const others=VOCAB.words.filter(x=>x!==tw&&'; assert _o in s; s = s.replace(_o, 'const others=VOCAB.words.filter(x=>!x.lock&&x!==tw&&')
# 19/11: anh yêu cầu bỏ popup quảng cáo ở bản dùng thử; mở link là vào thẳng màn Làm đề (thanh tab ở dưới)
s = s.replace('</body>', "<script>try{go('exam')}catch(e){}</script>\n</body>", 1)
# 21/11: bản dùng thử bỏ nút bật/tắt furigana — luôn hiện furigana
s = s.replace('</head>', '<style>#furiTg{display:none!important}</style></head>', 1)
s = s.replace('</body>', "<script>try{setFuri(true)}catch(e){document.body.classList.remove('nofuri')}</script>\n</body>", 1)
# 21/11: bỏ chọn "Thi thử như thật" — bấm đề là vào thẳng Luyện tập (chọn câu nào hiện đáp án + giải thích câu đó; có bài dở thì làm tiếp)
_m = "$('#exMode').classList.add('on')});"; assert s.count(_m) == 1; s = s.replace(_m, "startExam(exPick,'practice',dgGet(x.id,true))});")
DHV_CSS = """<style>
.dct{display:flex;flex-wrap:wrap;align-items:center;gap:8px 10px;background:#fff;border:1px solid #e3e9f0;border-radius:14px;padding:10px 14px;margin:0 0 14px;font-size:14px}
.dct b{color:#0d2b40;margin-right:2px}.dct a{border-radius:10px;padding:7px 12px;font-weight:800;text-decoration:none;color:#fff;background:#1877f2}.dct a.tt{background:#111}
.dhv{margin:22px 0 6px}.dhvw{display:grid;grid-template-columns:minmax(0,300px) 1fr;gap:18px;align-items:start}
.dhvw video{width:100%;aspect-ratio:9/16;background:#000;border-radius:16px;display:block;box-shadow:0 8px 24px #0d2b4022}
.dhvt b{display:block;font-size:1.15rem;color:#0d2b40}.dhvt span{display:block;color:var(--muted);font-weight:600;margin-top:4px}
@media(max-width:640px){.dhvw{grid-template-columns:1fr}.dhvw video{max-width:420px;margin:0 auto}}
</style>"""
DHV_HTML = (f'<div id="dhVid" class="dhv"><div class="h2 exgh">Kỹ năng làm bài đọc hiểu</div><div class="dhvw">'
            f'<video controls playsinline preload="none" poster="{DHV}.jpg" src="{DHV}.mp4"></video>'
            '<div class="dhvt"><b>Mẹo làm đọc hiểu JFT</b><span>Video 4 phút · Anh Trọng giảng</span></div></div></div>')
s = s.replace('</head>', DHV_CSS + '</head>', 1)
s = s.replace('</body>', "<script>(()=>{const H=" + json.dumps(DHV_HTML, ensure_ascii=False) + ";const put=()=>{const g=document.querySelector('#examList .exg');if(g&&!document.getElementById('dhVid'))g.insertAdjacentHTML('afterend',H)};"
              "const re=window.renderExams;if(typeof re==='function')window.renderExams=function(){const r=re.apply(this,arguments);put();return r};put()})()</script>\n</body>", 1)
# 21/11: tab "Học Gino" — link bản dùng thử của 5 ngành (tên worker lấy theo check-runs: gino-khachsan-trial, gino-vesinhtoanha-trial, gino-cbtp-app/trial, gino-xaydung/trial, gino-butsuryu-app/trial)
GINO = [('Khách sạn', '宿泊', 'https://gino-khachsan-trial.tronganh8a.workers.dev/', '#0d7d4d', 'ks.jpg'),
        ('Vệ sinh toà nhà', 'ビルクリーニング', 'https://gino-vesinhtoanha-trial.tronganh8a.workers.dev/', '#0d5a8c', 'vstn.jpg'),
        ('Chế biến thực phẩm', '飲食料品製造業', 'https://gino-cbtp-app.tronganh8a.workers.dev/trial/', '#c26a00', 'cbtp.jpg'),
        ('Xây dựng', '建設 · 土木・建築・ライフライン', 'https://gino-xaydung.tronganh8a.workers.dev/trial/', '#5b5f66', 'xd.jpg'),
        ('Logistics · Kho vận', '物流倉庫', 'https://gino-butsuryu-app.tronganh8a.workers.dev/trial/', '#c42f66', 'logi.jpg')]
GM = 'app/media/gino/'   # bìa giáo trình (Xây dựng: logo JAC, Logistics: tranh bìa app — ngành mới chưa có sách) + ảnh giáo viên
GINO_CSS = """<style>
.gnl{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;margin-top:6px}
.gnc{display:flex;gap:14px;align-items:center;background:#fff;border:1px solid #e3e9f0;border-left:6px solid var(--gc);border-radius:16px;padding:12px 14px;text-decoration:none;color:#0d2b40;box-shadow:0 4px 14px #0d2b400d}
.gnc img{width:72px;height:96px;object-fit:cover;border-radius:6px;box-shadow:0 3px 10px #0d2b4026;flex:none;background:#fff}
.gnc .tx{display:flex;flex-direction:column;gap:3px;min-width:0}
.gnc b{font-size:1.12rem}.gnc .jp{color:var(--muted);font-size:.9rem}.gnc span.d{color:var(--muted);font-size:.86rem}
.gnc i{font-style:normal;align-self:flex-start;margin-top:5px;background:var(--gc);color:#fff;font-weight:800;border-radius:10px;padding:6px 12px;font-size:.9rem}
.gnc:hover{transform:translateY(-1px);box-shadow:0 8px 20px #0d2b4018}
.gnp{color:var(--muted);margin:2px 0 4px;font-weight:600}
.gvc{display:grid;grid-template-columns:170px 1fr;gap:20px;align-items:start;background:#fff;border:1px solid #e3e9f0;border-radius:18px;padding:18px;margin-top:22px;box-shadow:0 4px 14px #0d2b400d}
.gvc>img{width:170px;height:227px;object-fit:cover;border-radius:14px}
.gvc h3{margin:0;font-size:1.25rem;color:#0d2b40}.gvc .ro{color:#c42f66;font-weight:800;margin:2px 0 10px}
.gvc ul{list-style:none;margin:0;padding:0;display:grid;gap:9px}.gvc li b{display:block;color:#0d2b40}.gvc li span{color:var(--muted);font-size:.92rem}
.gvc .ct{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}.gvc .ct a{border-radius:10px;padding:8px 13px;font-weight:800;text-decoration:none;color:#fff;background:#1877f2}.gvc .ct a.tt{background:#111}
@media(max-width:640px){.gvc{grid-template-columns:1fr}.gvc>img{width:150px;height:200px}}
</style>"""
GINO_NAV = ('<button class="nav" data-go="gino" type="button"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
            '<path d="M3 21h18M5 21V9l7-5 7 5v12"/><path d="M9 21v-6h6v6"/></svg>Học Gino<span class="jp">特定技能</span></button>')
GV = ('<div class="h2 exgh" style="margin-top:26px">Giáo viên</div><div class="gvc"><img src="' + GM + 'gv.jpg" alt="Anh Trọng">'
      '<div><h3>Vương Trọng Anh</h3><div class="ro">Trọng Anh sensei · Luyện thi Tokutei Gino &amp; JFT-Basic</div><ul>'
      '<li><b>Học bổng Chính phủ Nhật Bản (MEXT)</b><span>Du học tại Đại học Giáo dục Osaka (大阪教育大学), 10/2022 – 08/2023.</span></li>'
      '<li><b>Tốt nghiệp xuất sắc khoa tiếng Nhật, Đại học Hà Nội</b><span>4 lần liên tiếp nhận học bổng khuyến khích học tập.</span></li>'
      '<li><b>JLPT N1 · Boki 3 · IT Passport</b><span class="jp">日本語能力試験N1・簿記3級・ITパスポート</span></li>'
      '<li><b>Kinh nghiệm giảng dạy N5 – N2</b><span>Hiện dạy luyện thi Tokutei Gino và JFT-Basic.</span></li>'
      '<li><b>Tuyển dụng &amp; thủ tục hành chính tại Nhật</b><span>Làm nhân sự, hồ sơ tư cách lưu trú cho người lao động Việt Nam tại Osaka.</span></li>'
      f'</ul><div class="ct"><a href="{FB}" target="_blank" rel="noopener">Nhắn Facebook</a><a class="tt" href="{TT}" target="_blank" rel="noopener">TikTok @anhtrong.daygino</a></div></div></div>')
GINO_SCREEN = ('<section class="screen" id="gino"><div class="topbar"><h1>Học Gino<span class="jp">特定技能1号 · 評価試験</span></h1></div>'
               '<p class="gnp">Học thử miễn phí 5 ngành Tokutei Gino của Anh Trọng: bài học song ngữ Nhật – Việt, đề thi thử có giải thích. Bấm vào ngành để vào học thử, không cần đăng nhập.</p>'
               '<div class="gnl">' + ''.join(f'<a class="gnc" style="--gc:{c}" href="{u}" target="_blank" rel="noopener"><img src="{GM}{im}" alt="{n}" loading="lazy"><span class="tx"><b>{n}</b><span class="jp">{j}</span><span class="d">Bản dùng thử · bài học + đề thi thử</span><i>Vào học thử →</i></span></a>' for n, j, u, c, im in GINO) +
               '</div>' + GV + '</section>')
_nv = s.index('<button class="nav" data-go="n3"'); _nv = s.index('</button>', _nv) + len('</button>')
s = s[:_nv] + GINO_NAV + s[_nv:]
_sc = s.index('<section class="screen" id="n3">'); _sc = s.index('</section>', _sc) + len('</section>')
s = s[:_sc] + GINO_SCREEN + s[_sc:]
s = s.replace('</head>', GINO_CSS + '</head>', 1)
_n = 'Chọn <b>Luyện tập</b> để xem ngay sau từng câu, hoặc <b>Thi thử</b> rồi xem lại sau khi nộp bài.'; assert s.count(_n) == 1
s = s.replace(_n, 'Bấm vào đề là làm luôn: chọn đáp án câu nào là hiện ngay đáp án đúng và giải thích của câu đó.')
open(D + 'index.html', 'w', encoding='utf-8').write(s)
print('demo: bài học', {k: len(v) for k, v in OL.items()}, '· đề', NEX, '/', len(E), '· ngữ pháp', {k: len(v) for k, v in OG.items()},
      '· từ vựng', {k: len(v) for k, v in OV.items()}, '(', sum(1 for w in W if not w.get('lock')), 'từ ) · tài liệu từ vựng', {k: len(v) for k, v in ODV.items()},
      '· chữ Hán (nhóm 20)', ODK, '· video', OVID, '· BTVN', len(OHW), '/', len(H), '· theo buổi học', len(OB), '/', len(items), '·', len(ALLOW), 'file được mở')

# Bản sao trong public/_demo: worker chính (worker.js) phục vụ thư mục này khi truy cập bằng tên miền jft-dungthu.*
DD2 = P + '_demo/'
if os.path.exists(DD2): shutil.rmtree(DD2)
shutil.copytree(D, DD2)
