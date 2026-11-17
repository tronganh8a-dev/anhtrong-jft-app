"""Buổi 1 lớp cơ bản (17/11/2026): いろどり 初級1 第1課「レストランで働いています」— 90 phút.
Chọn lọc hoạt động trong sách (bỏ bớt), ngữ pháp dạy kỹ có ảnh minh hoạ + luyện tập; trắc nghiệm cho cả từ vựng, chữ Hán, ngữ pháp; có nghe.
Nguồn: いろどり 初級1 第1課 (hội thoại, audio 01-xx, tranh), 文法ノート いろどり (giải thích, câu luyện tập, tranh worksheet Y_image*),
DOCS (chữ Hán: Hán Việt, On/Kun, ví dụ), KanjiVG (nét viết). Bảng tóm tắt, sơ đồ thời gian, câu hỏi chữ số là tự soạn.
Dùng chung CSS/JS với tongon_nhapmon_build.py (exec phần định nghĩa).
Chạy: python3 src/tailieu_src/shokyu1_bai01_build.py → public/tailieu/Buoi01_Shokyu1_Bai01.html"""
import os
R = '/home/claude/anhtrong-jft-app/'
_src = open(R + 'src/tailieu_src/tongon_nhapmon_build.py').read()
exec(_src[:_src.index('# ---------------- BUỔI 1')])
A = R + 'src/tailieu_src/s1b01/'

def fimg(path, w=640):
    im = Image.open(path).convert('RGB')
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=82, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
L = lambda i: fimg(A + f'l{i:02d}.jpg')
Y = lambda i: fimg(R + f'public/app/media/gimg/Y_image{i}.jpg')
def au(t):
    return 'data:audio/mpeg;base64,' + base64.b64encode(open(A + t + '.mp3', 'rb').read()).decode()
AUD = lambda t, lab='': f'<div class="aud"><span>🔊 {t}{(" · " + lab) if lab else ""}</span><audio controls preload="none" src="{au(t)}"></audio></div>'

EXTRA = '''
.aud{display:inline-flex;align-items:center;gap:12px;background:#fff;border-radius:99px;padding:6px 8px 6px 20px;box-shadow:0 6px 18px #0d2b4014;margin:0 12px 12px 0}.aud span{font:700 22px Quicksand,sans-serif;color:#0d5a8c}.aud audio{height:44px;width:330px}
.big2{display:grid;grid-template-columns:1fr 1fr;gap:34px;align-items:start}
.pic{background:#fff;border-radius:22px;padding:12px;box-shadow:0 8px 24px #0d2b4012;text-align:center}.pic img{width:100%;max-height:300px;object-fit:contain;display:block}.pic figcaption{font-size:24px;font-weight:700;color:#0d5a8c;margin-top:6px}
.pic .jpt{font-size:30px;line-height:1.6;margin-top:6px}.pic .jpt rt{font-size:.5em}.pic .vi{font-size:22px;color:#47647a}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}.g5{display:grid;grid-template-columns:repeat(5,1fr);gap:16px}
.g3 .pic img{max-height:260px}.g4 .pic img{max-height:210px}
.lbl{display:inline-block;border-radius:99px;padding:4px 16px;font:800 22px Quicksand,sans-serif;color:#fff;background:#0d5a8c;margin-top:8px}.lbl.p{background:#c42f66}
.pat{background:#0d5a8c;color:#fff;border-radius:22px;padding:22px 30px;font-family:"Klee One",serif;font-weight:600;font-size:48px;line-height:1.5;display:inline-block}.pat rt{font-size:.45em}.pat em{font-style:normal;color:#ffd166}
.pmean{font-size:32px;font-weight:700;color:#0d5a8c;margin:10px 0 16px}
.exl{background:#fff;border-radius:18px;padding:16px 24px;box-shadow:0 6px 18px #0d2b4010;font-size:36px;line-height:1.75;margin-top:14px}.exl rt{font-size:.45em}.exl small{display:block;font-size:24px;color:#47647a;line-height:1.4}
.exp{font-size:28px;line-height:1.6;background:#fff;border-radius:18px;padding:18px 24px;box-shadow:0 6px 18px #0d2b4010;margin-top:14px}.exp b{color:#c42f66}.exp .jpt{font-size:30px}.exp rt{font-size:.5em}
.tline{position:relative;height:150px;margin:20px 10px 10px}.tline .ln{position:absolute;left:0;right:0;top:70px;height:6px;background:#9fb6c8;border-radius:3px}
.tline .pt{position:absolute;top:56px;width:34px;height:34px;border-radius:50%;background:#c42f66;border:6px solid #fff;box-shadow:0 2px 8px #0003;transform:translateX(-50%)}
.tline .tx{position:absolute;top:0;transform:translateX(-50%);font:800 26px Quicksand,"Klee One",sans-serif;white-space:nowrap;color:#0d2b40}.tline .bx{position:absolute;top:104px;transform:translateX(-50%);font:700 24px Quicksand,"Klee One",sans-serif;white-space:nowrap;color:#47647a}
.tline .span{position:absolute;top:62px;height:22px;border-radius:11px;background:#ffd16699;border:3px solid #f2a93b}
.tf{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-top:10px}.tf>div{background:#fff;border-radius:16px;padding:8px 10px;text-align:center;box-shadow:0 6px 18px #0d2b4010}
.tf .v{font-family:"Klee One",serif;font-weight:600;font-size:36px}.tf .a{font-family:"Klee One",serif;font-weight:600;font-size:36px;color:#c42f66}.tf rt{font-size:.45em}
.fill{font-size:34px;line-height:2;background:#fff;border-radius:18px;padding:14px 26px;box-shadow:0 6px 18px #0d2b4010}.fill rt{font-size:.45em}.fill .bl{display:inline-block;min-width:150px;border-bottom:4px solid #c42f66;text-align:center}.fill .bl span{color:#c42f66}
.dlg{font-size:34px;line-height:1.85;background:#fff;border-radius:20px;padding:18px 28px;box-shadow:0 6px 18px #0d2b4010}.dlg rt{font-size:.45em}.dlg b{display:inline-block;width:44px;color:#0d5a8c}.dlg .sw{background:#fff0f5;color:#c42f66;border-radius:10px;padding:0 10px}.dlg small{display:block;font-size:22px;color:#47647a;line-height:1.3;margin:-4px 0 6px 44px}
.ktb2 td{font-size:30px}
.clw{display:flex;flex-wrap:wrap;gap:22px 26px;justify-content:center;align-content:center;flex:1;padding:6px 10px}
.cld{position:relative;border:0;cursor:pointer;background:#fff;min-width:200px;height:132px;padding:10px 30px;border-radius:80px 90px 70px 85px/70px 60px 80px 65px;box-shadow:0 10px 26px #0d5a8c26,inset 0 -8px 0 #e6f1fb;display:flex;flex-direction:column;align-items:center;justify-content:center;transition:transform .2s}
.cld:nth-child(3n){transform:rotate(-2deg)}.cld:nth-child(3n+1){transform:rotate(2deg) translateY(8px)}.cld:hover{transform:scale(1.06)}
.cld i{position:absolute;left:-10px;top:-12px;width:46px;height:46px;border-radius:50%;background:#c42f66;color:#fff;font:800 24px Quicksand,sans-serif;font-style:normal;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 10px #c42f6655}
.cld .cw{font-family:"Klee One",serif;font-weight:600;font-size:52px;line-height:1.1;color:#0d2b40}
.cld .cr2{display:none;font:800 24px Quicksand,"Klee One",sans-serif;color:#0d5a8c;margin-top:4px}.cld .cr2 small{display:block;font-size:16px;color:#c42f66;letter-spacing:1px}
.cld.on .cr2{display:block}.cld.on{background:#fff8e6}
.shf{margin-left:auto;border:0;border-radius:99px;background:#0d5a8c;color:#fff;font:700 22px Quicksand,sans-serif;padding:8px 22px;cursor:pointer}
.ck{font-size:28px!important;line-height:1.6!important}.kdh{margin-top:-8px}
.kdt{font-size:25px!important}.kdt td{padding:8px 12px!important}.kdt .kk{font-size:44px!important}.kdw{font-size:90px!important}.kdv{font-size:34px!important}.kdm{font-size:34px!important;margin:2px 0 12px!important}
.kdn{font-size:24px!important;padding:10px 16px!important;margin-top:10px!important}.kde{font-size:30px!important;padding:8px 16px!important;margin-top:10px!important;line-height:1.6!important}.kde small{font-size:22px!important}
.qbig.sm{font-size:64px}.aud audio{width:230px}.pic .aud{margin:8px 0 0}.pic .aud span{font-size:18px}.pic .aud audio{width:200px;height:38px}
.tline{height:128px;margin:6px 10px 4px;flex-shrink:0}.tline .ln{top:52px}.tline .pt{top:38px}.tline .span{top:44px}.tline .bx{top:84px}
.ktb2 td{padding:8px 18px!important}.exl.c{font-size:30px;padding:10px 20px;margin-top:10px}.pat{font-size:42px;padding:14px 26px}.g4 .pic img{max-height:290px}.ktb2 .jpt{font-size:34px}
'''
HEAD2 = HEAD.replace('</style></head>', EXTRA + '</style></head>', 1)

S = []
CR = '<div class="cr">いろどり 初級1 第1課 · Anh Trọng Dạy JFT · 出典：いろどり 生活の日本語 初級1 (Quỹ Giao lưu Quốc tế Nhật Bản), 文法ノート いろどり · nét viết: KanjiVG (CC BY-SA 3.0) · bảng tóm tắt, sơ đồ, câu hỏi đánh dấu tự soạn</div>'
def sl(t, body, cls=''):
    S.append(f'<section class="slide{(" " + cls) if cls else ""}">{("<h2>" + t + "</h2>") if t else ""}{body}{CR}</section>')
NQ = [0]
def quiz(qhtml, opts, a, expl, src, pic=None, big=None, extra=''):
    NQ[0] += 1; ks = 'abcd'
    ob = ''.join(f'<button class="o" data-k="{ks[i]}"><b>{ks[i]}</b><span class="jp ot">{o}</span><i></i><em></em></button>' for i, o in enumerate(opts))
    op = f'<div class="opts list" data-a="{ks[a]}">{ob}</div>'
    if pic: body = f'<div class="qi"><img src="{pic}">{op}</div>'
    elif big: body = f'<div class="qi"><div class="qbig">{big}</div>{op}</div>'
    else: body = op
    S.append(f'<section class="slide qz{" ls" if extra else ""}"><div class="kk2">Luyện tập {NQ[0]} <span class="src">{src}</span></div><h2 class="jp q">{qhtml}</h2>{extra}{body}<div class="ex{" lex" if extra else ""}"><b>Đáp án: {ks[a]}</b> — {expl}</div>{"<button class=lsb onclick=" + chr(34) + "this.previousElementSibling.classList.toggle(&quot;open&quot;)" + chr(34) + ">📄 Script</button>" if extra else ""}{CR}</section>')
def gq(no, i, src='文法ノート いろどり 初級1 第1課'):
    q = next(p for p in GB1['points'] if p['no'] == no)['quiz'][i]
    quiz(RB(q['q']).replace('（　）', '<u>（　　）</u>'), [RB(o) for o in q['o']], q['a'], RB(q.get('ex_vi', '')), src)
def sec(n, t, j, d, m):
    sl('', f'<div class="sec"><div class="n">{n}</div><div class="t">{t}</div><div class="j">{j}</div><div class="d">{d}</div><div class="tm">{m} phút</div></div>')

GB1 = next(g for g in GRAM if g['lv'] == '初級1' and g['bai'] == 1)
V1 = [w for w in DOCS['vocab']['初級1'] if w['b'] == 1]
K1 = {k['w']: k for k in DOCS['kanji']['初級1']}
JOB = list(zip(range(3, 12), V1))  # (ảnh trong sách, từ)

# ===== 0. Bìa, nội dung
S.append(f'''<section class="slide dark"><div class="cover"><img class="lg" src="{LOGO}"><div class="kk">BUỔI 1 · いろどり 初級1 · 第1課</div>
<h1>レストランで<br><span>働いています</span></h1><p>Tôi đang làm việc ở nhà hàng · Chủ đề: 今の私</p></div>{CR}</section>''')
plan = [(5, 'Khởi động', 'Hôm nay học gì? Nhìn tranh đoán nghề'), (15, 'Từ vựng', 'Công việc · cảm nghĩ · か月/年'), (15, 'Chữ Hán', '10 từ chữ Hán, nét viết'),
        (35, 'Ngữ pháp', '丁寧体/普通体 · になります · に来ました · テ形 · ています'), (15, 'Nghe hiểu', 'Sang Nhật bao lâu? Làm nghề gì?'), (5, 'Luyện nói', 'Giới thiệu công việc của mình')]
sl('Nội dung buổi 1 <small>90 phút</small>', '<div class="plan" style="grid-template-columns:repeat(3,1fr)">' + ''.join(f'<div><b>{m}′</b><h3>{h}</h3><p>{p}</p></div>' for m, h, p in plan) + '</div>')
sl('Khởi động <small>Can-do: nói đơn giản về việc mình đang làm ở Nhật</small>',
   f'<div class="exl" style="margin:0 0 18px">{J("日本に行ったら、したい仕事がありますか？")}<small class="st">Khi sang Nhật, bạn muốn làm công việc gì?</small></div>'
   + '<div class="g5">' + ''.join(f'<figure class="pic"><img src="{L(i)}" style="max-height:170px"></figure>' for i in range(3, 12) if i != 11) + f'<figure class="pic"><img src="{L(11)}" style="max-height:170px"></figure></div>')

# ===== 1. Từ vựng
sec('01', 'Từ vựng', 'ことば', 'Nhìn tranh → đọc tiếng Nhật → nghĩa', 15)
cards = ''.join(f'<div class="kc kv"><img src="{L(i)}" style="height:120px;object-fit:cover;border-radius:12px"><div class="st g1"><div class="w{" sm" if len(w["r"]) > 9 else ""}" style="white-space:normal;font-size:24px;line-height:1.4">{w["wr"]}</div></div><div class="st g2"><div class="m">{html.escape(w["vi"])}</div></div></div>' for i, w in JOB)
sl('Từ vựng <small>【仕事】Công việc</small>', AUD('01-16', 'nghe và nói theo') + f'<div class="vg">{cards}</div>')
FEEL = [('忙しい', 'bận'), ('大変', 'vất vả'), ('疲れる', 'mệt'), ('まあまあ', 'tàm tạm'), ('楽しい', 'vui'), ('おもしろい', 'thú vị'), ('みんな親切', 'mọi người tốt bụng'), ('勉強になる', 'học hỏi được nhiều'), ('生活', 'cuộc sống'), ('慣れる', 'quen')]
sl('Từ vựng <small>Nói cảm nghĩ về công việc, cuộc sống</small>', '<div class="vg">' + ''.join(f'<div class="kc kv noimg"><div class="nw"><div class="w">{J(w)}</div></div><div class="st g2"><div class="m">{v}</div></div></div>' for w, v in FEEL) + '</div>')
KG = [('1か月', 'いっかげつ', 1), ('2か月', 'にかげつ', 0), ('3か月', 'さんかげつ', 0), ('4か月', 'よんかげつ', 0), ('5か月', 'ごかげつ', 0), ('6か月', 'ろっかげつ', 1), ('7か月', 'ななかげつ', 0), ('8か月', 'はちかげつ', 0), ('9か月', 'きゅうかげつ', 0), ('10か月', 'じゅっかげつ', 1)]
NN = [('1年', 'いちねん', 0), ('2年', 'にねん', 0), ('3年', 'さんねん', 0), ('4年', 'よねん', 1), ('5年', 'ごねん', 0), ('7年', 'ななねん／しちねん', 1), ('9年', 'きゅうねん', 1), ('半年', 'はんとし', 1), ('先月', 'せんげつ', 0), ('去年', 'きょねん', 0)]
cell = lambda a, b, h: f'<div style="background:{"#fff0f5" if h else "#fff"}"><div class="v">{a}</div><div class="st" style="font-size:24px;color:{"#c42f66" if h else "#0d5a8c"};font-weight:800">{b}</div></div>'
sl('Từ vựng <small>【期間】khoảng thời gian · ô hồng = cách đọc đặc biệt</small>', AUD('01-11', 'か月') + AUD('01-12', '年') + AUD('01-13', 'mốc quá khứ') +
   '<div class="tf">' + ''.join(cell(*x) for x in KG) + '</div><div class="tf" style="margin-top:14px">' + ''.join(cell(*x) for x in NN) + '</div>')
def shuf(right, wrong, seed):
    opts = [right] + wrong[:3]; k = seed % len(opts); opts = opts[k:] + opts[:k]; return opts, opts.index(right)
for n, (i, w) in enumerate([JOB[2], JOB[5], JOB[7]]):
    o, a = shuf(w['r'], w['rd'], n + 1)
    quiz('Nhìn tranh, chọn cách đọc đúng.', [html.escape(x) for x in o], a, f'<span class="jp">{w["wr"]}</span> – {html.escape(w["vi"])}', 'Từ vựng いろどり 初級1 第1課', pic=L(i))
for n, (q, r, wr) in enumerate([('6か月', 'ろっかげつ', ['ろくかげつ', 'むっかげつ', 'ろっかつき']), ('4年', 'よねん', ['よんねん', 'しねん', 'よっねん']), ('10か月', 'じゅっかげつ', ['じゅうかげつ', 'とおかげつ', 'じゅっかつき'])]):
    o, a = shuf(r, wr, n + 2)
    quiz('Đọc thế nào?', o, a, f'{q} đọc là <b>{r}</b> (câu tự soạn)', 'Câu tự soạn', big=q)

# Trắc nghiệm bối cảnh dùng từ (câu tự soạn, từ của bài)
CTX = [('おじいさんやおばあさんの世話をしています。（　）の仕事です。', ['介護', '建設', '工場'], 0, '世話をする = chăm sóc → 介護の仕事 (công việc chăm sóc người cao tuổi).'),
       ('畑で（　）を作っています。', ['野菜', '料理', '学校'], 0, 'Ở ruộng (畑) → 野菜を作る: trồng rau.'),
       ('A：日本の生活に、もう（　）か？　B：はい、おかげさまで。', ['慣れました', '疲れました', '働きました'], 0, '生活に慣れる: quen với cuộc sống.'),
       ('仕事は大変です。でも、みんな（　）です。', ['親切', 'まだ', '半年'], 0, 'みんな親切です: mọi người tốt bụng.'),
       ('日本に来て、ちょうど（　）になります。6か月です。', ['半年', '1年', '先月'], 0, '6か月 = 半年 (nửa năm); 先月 là mốc thời gian, không đi với になります.'),
       ('今、専門学校に（　）います。プログラミングを勉強しています。', ['通って', '働いて', '作って'], 0, '学校に通う: đi học (đều đặn) ở trường.'),
       ('毎日8時間、立って働きます。とても（　）。', ['疲れます', '慣れます', '通います'], 0, 'Làm việc đứng 8 tiếng → 疲れます (mệt).')]
for n, (q, o, a, e) in enumerate(CTX):
    oo, k = shuf(o[a], [x for i, x in enumerate(o) if i != a], n)
    quiz(J(q).replace('（　）', '<u>（　　）</u>'), [J(x) for x in oo], k, e, 'Chọn từ hợp ngữ cảnh · câu tự soạn')
# ===== 2. Chữ Hán
sec('02', 'Chữ Hán', 'かんじ', 'Nét viết · Hán Việt · On/Kun · ví dụ', 15)
K1['仕事'] = {'w': '仕事', 'r': 'しごと', 'vi': 'Công việc', 'hv': 'SĨ SỰ', 'chars': [{'k': '仕', 'hv': 'SĨ', 'on': 'シ', 'kun': 'つか.える', 'vi': 'phục vụ, làm'}, {'k': '事', 'hv': 'SỰ', 'on': 'ジ', 'kun': 'こと', 'vi': 'việc'}],
              'tip': '仕 (SĨ: phục vụ, có bộ nhân 亻) + 事 (SỰ: việc) = việc mình làm. 事 đọc ごと (biến âm) trong 仕事.', 'ex': {'jp': J('仕事はどうですか？'), 'vi': 'Công việc thế nào? (hội thoại 01-18)'}}
KW = ['学生', '仕事', '学校', '元気', '生活', '忙しい', '去年', '働く', '先週', '作る']
for ii, w in enumerate(KW):
    k = K1[w]; kj = ''.join(c for c in w if c in KVG)
    rows = ''.join(f'<tr><td class="kk">{html.escape(c["k"])}</td><td class="hh">{html.escape(c["hv"])}</td><td>{html.escape(c.get("on") or "–")}</td><td>{html.escape(c.get("kun") or "–")}</td><td class="mm">{html.escape(c.get("vi") or "")}</td></tr>' for c in k['chars'])
    tip = re.sub(r'^\s*(Mẹo nhớ|Mẹo|Ghi nhớ)\s*:\s*', '', k.get('tip') or ''); ex = k.get('ex') or {}
    sl(f'Chữ Hán <small>漢字のことば · {ii + 1}/{len(KW)}</small>',
       f'<div class="kd"><div class="kdl"><div class="kvi" data-w="{kj}"></div><button class="kvr" onclick="kvPlay(this.previousElementSibling,1)">▶ Viết lại</button><button class="kvr" onclick="kvPlay(this.parentNode.querySelector(&quot;.kvi&quot;),.45)">Chậm</button>{rel(w)}</div>'
       f'<div class="kdr"><div class="kdh"><span class="kdw">{html.escape(w)}</span><span class="kdv">{html.escape(k["hv"])}</span></div>'
       f'<div class="st kdm"><span class="jp">{html.escape(k["r"])}</span> · {html.escape(k["vi"])}</div>'
       f'<table class="kdt st"><tr><th>Chữ</th><th>Hán Việt</th><th>Âm On</th><th>Âm Kun</th><th>Nghĩa</th></tr>{rows}</table>'
       + (f'<div class="kdn st"><b>Cách nhớ</b> {html.escape(tip)}</div>' if tip else '')
       + (f'<div class="kde st"><div class="jp">{ex["jp"]}</div><small>{html.escape(ex.get("vi", ""))}</small></div>' if ex.get('jp') else '') + '</div></div>')
RS = [('お元気ですか？', 'Bạn có khoẻ không?'), ('去年、日本に来ました。', 'Năm ngoái tôi đã sang Nhật.'), ('日本の生活に、もう慣れましたか？', 'Bạn đã quen với cuộc sống ở Nhật chưa?'),
      ('いいえ、学生です。今は、日本語学校に通っています。', 'Không, tôi là học sinh. Bây giờ tôi đang học ở trường tiếng Nhật.'), ('介護の仕事をしています。', 'Tôi đang làm công việc chăm sóc người cao tuổi.'), ('先週は、とても忙しかったです。', 'Tuần trước tôi rất bận.')]
for h in (RS[:3], RS[3:]):
    sl('Chữ Hán <small>Tự đọc trước → bấm để xem cách đọc</small>', '<div class="gp" style="min-height:0">' + ''.join(f'<div class="exl" style="margin-top:10px;font-size:34px;padding:10px 22px"><div class="jpt">{html.escape(a)}</div><div class="st" style="font-size:32px">{J(a)}<small>{b}</small></div></div>' for a, b in h) + '</div>')
for n, w in enumerate(['生活', '働く', '去年']):
    k = K1[w]; o, a = shuf(k['r'], k['rd'], n + 1)
    quiz('Chữ Hán này đọc thế nào?', o, a, f'{w} đọc là <b>{k["r"]}</b> ({k["hv"]}) – {k["vi"]}', 'Chữ Hán いろどり 初級1 第1課', big=w)
for n, w in enumerate(['学校', '先週', '忙しい']):
    k = K1[w]; o, a = shuf(w, k['wk'], n + 2)
    quiz('Chọn chữ Hán đúng.', o, a, f'<b>{w}</b> ({k["hv"]}) – {k["vi"]}', 'Chữ Hán いろどり 初級1 第1課', big=k['r'] if len(k['r']) <= 4 else f'<span style="font-size:60px">{k["r"]}</span>')

# Màn "đám mây": chỉ ô nào đọc ô đó (số thứ tự đảo ngẫu nhiên)
CW = KW + ['大学', '高校生', '先生', '来年', '今週', '仕事中']
CW = [w for w in CW if w in K1 or any(v['h'] == w for v in _VW)]
def _rd(w):
    if w in K1: return K1[w]['r'], K1[w]['hv']
    v = next(v for v in _VW if v['h'] == w); return v['y'], v.get('hv', '')
clouds = ''.join(f'<button class="cld" data-r="{html.escape(_rd(w)[0])}"><i></i><span class="cw">{html.escape(w)}</span><span class="cr2">{html.escape(_rd(w)[0])}<small>{html.escape(_rd(w)[1])}</small></span></button>' for w in CW)
sl('Chữ Hán <small>Chỉ ô nào – đọc ô đó · bấm ô để xem cách đọc</small> <button class="shf" onclick="cloudMix(this.closest(&quot;.slide&quot;))">🔀 Đảo lại</button>', f'<div class="clw">{clouds}</div>')
# ===== 3. Ngữ pháp
sec('03', 'Ngữ pháp', 'ぶんぽう', 'Mẫu câu – tranh – giải thích – luyện tập', 35)
P = {p['no']: p for p in GB1['points']}
# ❶
me = P['❶']['more_examples']
sl('Ngữ pháp ❶ <small>丁寧体・普通体 · Thể lịch sự / Thể thông thường</small>',
   '<div class="g3">' + ''.join(f'<figure class="pic"><img src="{L(i)}"><div class="jpt">{RB(e["jp"][2:])}</div><div class="vi st">{html.escape(e["vi"][2:])}</div><span class="lbl{" p" if k else ""} st">{lab}</span>{AUD(t)}</figure>'
                                for i, e, k, lab, t in [(0, me[0], 0, 'Người quen · cả hai 丁寧体', '01-01'), (1, me[1], 1, 'Bạn thân · cả hai 普通体', '01-02'), (2, me[2], 0, 'A là người trên · B nói 丁寧体', '01-03')]) + '</div>' if True else
   '<div class="g3">' + ''.join(f'<figure class="pic"><img src="{L(i)}"><div class="jpt">{RB(e["jp"][2:])}</div><div class="vi st">{html.escape(e["vi"][2:])}</div><span class="lbl{" p" if k else ""} st">{lab}</span></figure>'
                                for i, e, k, lab in [(0, me[0], 0, 'Người quen · cả hai 丁寧体'), (1, me[1], 1, 'Bạn thân · cả hai 普通体'), (2, me[2], 0, 'A là người trên · B nói 丁寧体')]) + '</div>')
sl('Ngữ pháp ❶ <small>Khi nào dùng thể nào?</small>',
   '<div class="big2"><div><div class="g3" style="grid-template-columns:1fr 1fr">'
   f'<figure class="pic"><img src="{L(12)}" style="max-height:200px"><figcaption>Nói với người lớn tuổi hơn</figcaption></figure>'
   f'<figure class="pic"><img src="{L(13)}" style="max-height:200px"><figcaption>Nói với tiền bối</figcaption></figure>'
   f'<figure class="pic"><img src="{L(14)}" style="max-height:200px"><figcaption>Nói với cấp trên</figcaption></figure>'
   f'<figure class="pic"><img src="{L(15)}" style="max-height:200px"><figcaption>Nhân viên → khách</figcaption></figure></div><span class="lbl st" style="font-size:28px">→ dùng 丁寧体 (です・ます)</span></div>'
   '<div><table class="tb2 ktb2"><tr><th></th><th>丁寧体</th><th>普通体</th></tr>'
   f'<tr><td class="h">Danh từ</td><td>{jp("元気です")}</td><td>{jp("元気")}</td></tr>'
   f'<tr><td class="h">Tính từ</td><td>{jp("忙しいです")}</td><td>{jp("忙しい")}</td></tr>'
   f'<tr><td class="h">Động từ</td><td>{jp("飲みますか？")}</td><td>{jp("飲む？")}</td></tr>'
   f'<tr><td class="h">Chào</td><td>{jp("お久しぶりです")}</td><td>{jp("久しぶり")}</td></tr></table>'
   '<div class="exp st">Ở 初級1–2: <b>tự nói được 丁寧体</b> là đủ; 普通体 chỉ cần <b>nghe hiểu</b>.<br>Bạn thân mà cứ nói 丁寧体 → nghe xa cách; người trên mà nói 普通体 → thất lễ.</div></div></div>')
ws = P['❶']['worksheet'][0]['items']
for n, it in enumerate([ws[0], ws[3], ws[4]]):
    ch = it['choices']; ans = ch.index(it['answer'][0])
    quiz(RB(it['q']).replace('＿＿', '<u>（　　）</u>'), [RB(c) for c in ch], ans, 'Người trên / khách / người lớn tuổi hơn → 丁寧体; người dưới, bạn thân → 普通体.', '文法ノート いろどり 初級1 第1課 · 練習', pic=Y(int(it['img'].split('image')[1])))
gq('❶', 1)
# ❷ ❸
sl('Ngữ pháp ❷ <small>【期間】になります · Đã được (bao lâu)</small>',
   f'<div class="pat">【期間】＋ <em>になります</em></div><div class="pmean">Hỏi: <span class="jpt">{J("どのぐらいになりますか？")}</span> → trả lời <b>khoảng thời gian</b></div>'
   '<div class="tline"><div class="ln"></div><div class="span" style="left:12%;width:76%"></div><div class="pt" style="left:12%"></div><div class="pt" style="left:88%;background:#0d5a8c"></div>'
   f'<div class="tx" style="left:12%">{J("日本に来て")}</div><div class="tx" style="left:88%">{J("今")}</div><div class="bx" style="left:50%;color:#c47a00;font-size:30px">{J("1年になります")}</div></div>'
   + ''.join(f'<div class="exl c st">{RB(e["jp"])}<small>{html.escape(e["vi"])}</small></div>' for e in P['❷']['examples'] + P['❷']['more_examples'][1:])
   + '<div class="exp st">Mốc bắt đầu nói bằng <b>thể テ</b>: 日本に来て・仕事を始めて・ここで働いて ＋ 【期間】になります</div>')
sl('Ngữ pháp ❸ <small>【時点】（に）来ました · Đã đến vào lúc…</small>',
   f'<div class="pat">【時点】＋（<em>に</em>）来ました</div><div class="pmean">Hỏi: <span class="jpt">{J("いつ来ましたか？")}</span> → trả lời <b>mốc thời gian</b></div>'
   '<div class="tline"><div class="ln"></div><div class="pt" style="left:22%"></div><div class="pt" style="left:88%;background:#0d5a8c"></div>'
   f'<div class="tx" style="left:22%">{J("去年の9月")}</div><div class="tx" style="left:88%">{J("今")}</div><div class="bx" style="left:22%;color:#c47a00;font-size:30px">{J("に来ました")}</div></div>'
   '<div class="big2"><table class="tb2 ktb2"><tr><th>Có に</th></tr>' + ''.join(f'<tr><td>{jp(x)}</td></tr>' for x in ['9月に来ました', '20日に来ました', '去年の9月に来ました']) + '</table>'
   '<table class="tb2 ktb2"><tr><th>Không có に</th></tr>' + ''.join(f'<tr><td>{jp(x)}</td></tr>' for x in ['去年、来ました', '先月、来ました', '先週、来ました']) + '</table></div>')
sl('So sánh ❷ và ❸ <small>Nghe và điền · 形に注目</small>', AUD('01-10') +
   '<div class="fill">' + '<br>'.join([
       f'{J("日本に来て、どのぐらいに")}<span class="bl"><span class="st">{J("なります")}</span></span>{J("か？")}',
       f'{J("1年に")}<span class="bl"><span class="st">{J("なります")}</span></span>{J("。")}　　{J("ちょうど半年")}<span class="bl"><span class="st">{J("です")}</span></span>{J("。")}',
       f'{J("去年の9月に")}<span class="bl"><span class="st">{J("来ました")}</span></span>{J("。")}　　{J("先月、")}<span class="bl"><span class="st">{J("来ました")}</span></span>{J("。")}']) + '</div>'
   '<div class="big2" style="margin-top:16px"><div class="exp st"><b>どのぐらい？</b> → 【期間】になります<br><span class="jpt">1年・半年・3か月</span></div><div class="exp st"><b>いつ？</b> → 【時点】（に）来ました<br><span class="jpt">去年の9月に・先月</span></div></div>')
gq('❷', 0); gq('❸', 0); gq('❸', 2)
# テ形
TE = [('1グループ', '-う・-つ・-る → って', [('通う', '通って'), ('待つ', '待って'), ('作る', '作って')]), ('1グループ', '-む・-ぶ・-ぬ → んで', [('飲む', '飲んで'), ('遊ぶ', '遊んで'), ('読む', '読んで')]),
      ('1グループ', '-く → いて ・ -ぐ → いで', [('働く', '働いて'), ('聞く', '聞いて'), ('泳ぐ', '泳いで')]), ('1グループ', '-す → して', [('話す', '話して'), ('貸す', '貸して')]),
      ('Ngoại lệ', '行く → 行って', [('行く', '行って')]), ('2グループ', '-る → て', [('見る', '見て'), ('食べる', '食べて'), ('起きる', '起きて')]), ('3グループ', 'bất quy tắc', [('する', 'して'), ('来る', '来て'), ('勉強する', '勉強して')])]
sl('Thể テ <small>テ形 · chia động từ (cần cho ❹ ています)</small>', '<table class="tb2"><tr><th>Nhóm</th><th>Quy tắc</th><th>Ví dụ</th></tr>' + ''.join(
    f'<tr><td class="h">{g}</td><td>{jp(r) if "→" in r and g != "3グループ" else r}</td><td>' + '　'.join(f'{jp(a)} → <em class="st">{jp(b)}</em>' for a, b in ex) + '</td></tr>' for g, r, ex in TE) + '</table>')
TF = [('聞く', '聞いて'), ('買う', '買って'), ('読む', '読んで'), ('乗る', '乗って'), ('行く', '行って'), ('脱ぐ', '脱いで'), ('貸す', '貸して'), ('寝る', '寝て'), ('掃除する', '掃除して'), ('来る', '来て')]
sl('Thể テ <small>Chia nhanh · đọc to cả lớp</small>', '<div class="tf">' + ''.join(f'<div><div class="v">{J(a)}</div><div class="a st">{J(b)}</div></div>' for a, b in TF) + '</div>')
for a, r, w in [('読む', '読んで', ['読って', '読みて']), ('働く', '働いて', ['働って', '働きて']), ('話す', '話して', ['話いて', '話って'])]:
    o, k = shuf(J(r), [J(x) for x in w], len(a))
    quiz(f'Thể テ của 「{J(a)}」 là gì?', o, k, f'{a} → <b>{r}</b> (câu tự soạn)', 'Câu tự soạn')
# ❹
sl('Ngữ pháp ❹ <small>V-ています · Đang (làm) — nói công việc hiện tại</small>',
   f'<div class="pat">V<em>て</em> ＋ います</div><div class="pmean">{J("日本では、何をしていますか？")} · Ở Nhật bạn đang làm gì?</div>'
   '<div class="g4">' + ''.join(f'<figure class="pic"><img src="{Y(i)}"><div class="jpt st">{J(s)}</div></figure>' for i, s in [(12, 'レストランで働いています。'), (11, '工場で働いています。'), (16, '介護の仕事をしています。'), (15, '専門学校に通っています。')]) + '</div>')
sl('Ngữ pháp ❹ <small>Lưu ý khi nói</small>',
   ''.join(f'<div class="exl">{RB(e["jp"])}<small>{html.escape(e["vi"])}</small></div>' for e in P['❹']['more_examples']) +
   '<div class="big2"><div class="exp st">Văn nói hay bỏ い: <span class="jpt">働いています → 働いてます</span></div><div class="exp st">Thể thông thường: <span class="jpt">～ている → ～てる</span><br>(chỉ cần nghe hiểu)</div></div>')
sl('Ngữ pháp ❹ <small>Nhìn tranh, nói câu · 練習</small>', '<div class="g4">' + ''.join(
    f'<figure class="pic"><img src="{Y(i)}"><div class="jpt st">{J(s)}</div></figure>' for i, s in [(10, '建設の仕事をしています。'), (9, '日本語学校で勉強しています。'), (14, 'ホテルで働いています。'), (13, '野菜を作っています。')]) + '</div>')
gq('❹', 0); gq('❹', 1); gq('❹', 2)

# ===== 4. Nghe hiểu
sec('04', 'Nghe hiểu', 'ちょうかい', 'Đọc câu hỏi trước → nghe → chọn', 15)
SCR = {'01-06': ['A：日本に来て、どのぐらいになりますか？', 'B：1年になります。', 'A：そうですか。日本の生活に、もう慣れましたか？', 'B：はい。'],
       '01-07': ['A：日本に来て、どのぐらいですか？', 'B：ちょうど半年です。', 'A：そうですか。日本に慣れましたか？', 'B：はい、なんとか。'],
       '01-08': ['A：日本に来て、どのぐらいですか？', 'B：去年の9月に来ました。', 'A：そうですか。もう慣れましたか？', 'B：はい、おかげさまで。'],
       '01-09': ['A：日本に来て、どのぐらいになりますか？', 'B：私は、先月、来ました。', 'A：そうですか。少し慣れましたか？', 'B：まだ、ちょっと……。'],
       '01-19': ['A：日本では、何をしていますか？', 'B：働いています。', 'A：そうですか。どんな仕事ですか？', 'B：野菜を作っています。', 'A：仕事はどうですか？', 'B：うーん、疲れます。でも、みんな親切です。'],
       '01-20': ['A：日本では、何をしていますか？', 'B：働いています。', 'A：そうですか。どんな仕事ですか？', 'B：介護の仕事をしています。', 'A：仕事はどうですか？', 'B：毎日、大変です。でも、楽しいです。'],
       '01-23': ['A：日本では、何をしていますか？', 'B：学生です。専門学校に通っています。', 'A：何を勉強していますか？', 'B：プログラミングを勉強しています。', 'A：そうですか。勉強はどうですか？', 'B：とてもおもしろいです。']}
sc = lambda t: '<span class="lb">SCRIPT</span><div class="jp">' + '<br>'.join(J(x) for x in SCR[t]) + '</div>'
O4 = ['半年', '1年', '先月', '去年の9月']
for n, (t, a) in enumerate([('01-06', 1), ('01-07', 0), ('01-08', 3), ('01-09', 2)]):
    quiz(f'Người {"①②③④"[n]}: {J("日本に来て、どのぐらいですか。いつ来ましたか。")}', [J(x) for x in O4], a, f'{J(O4[a])}' + sc(t), 'いろどり 初級1 第1課 · 聴解', extra=f'<div class="lsn"><audio controls preload="none" src="{au(t)}"></audio></div>')
jobs = {k: (i, w) for k, (i, w) in zip('abcdefghi', JOB)}
for n, (t, a, opts) in enumerate([('01-19', 'f', 'cfda'), ('01-20', 'd', 'bdeh'), ('01-23', 'h', 'giha')]):
    ob = ''.join(f'<button class="o oi" data-k="{"abcd"[j]}"><img src="{L(jobs[k][0])}"><b>{"abcd"[j]}</b><span class="jp ot">{jobs[k][1]["wr"]}</span><i></i><em></em></button>' for j, k in enumerate(opts))
    NQ[0] += 1; ai = opts.index(a)
    S.append(f'<section class="slide qz ls"><div class="kk2">Luyện tập {NQ[0]} <span class="src">いろどり 初級1 第1課 · 聴解</span></div><h2 class="jp q">{J("日本で何をしていますか。")}<span class="vi-q">Người này đang làm gì ở Nhật?</span></h2>'
             f'<div class="lsn"><audio controls preload="none" src="{au(t)}"></audio></div><div class="opts oimg" data-a="{"abcd"[ai]}" style="grid-template-columns:repeat(4,1fr)">{ob}</div>'
             f'<div class="ex lex"><b>Đáp án: {"abcd"[ai]}</b> — {jobs[a][1]["wr"]}{sc(t)}</div><button class="lsb" onclick="this.previousElementSibling.classList.toggle(&quot;open&quot;)">📄 Script</button>{CR}</section>')

# ===== 5. Luyện nói + kết
sec('05', 'Luyện nói', 'はなす', 'Thay từ, nói về bản thân', 5)
sl('Luyện nói <small>Thay phần màu hồng bằng thông tin của mình</small>', AUD('01-25', 'hội thoại mẫu') +
   '<div class="dlg">' + f'<b>A</b>{J("日本では、何をしていますか？")}<br><b>B</b><span class="sw">{J("工場で働いています")}</span>{J("。")}<small>介護の仕事をしています ／ 野菜を作っています ／ 専門学校に通っています</small>'
   f'<b>A</b>{J("仕事はどうですか？")}<br><b>B</b><span class="sw">{J("とても楽しいです")}</span>{J("。")}<small>大変です ／ 勉強になります ／ 疲れます</small>'
   f'<b>A</b>{J("日本に来て、どのぐらいになりますか？")}<br><b>B</b><span class="sw">{J("1年")}</span>{J("になります。")}<small>半年です ／ 去年の9月に来ました</small></div>')
sl('Tổng kết buổi 1', '<div class="kgr g2"><div class="kcd kb"><h3>Đã học</h3><ul class="ck"><li>丁寧体 ↔ 普通体</li><li>【期間】になります</li><li>【時点】（に）来ました</li><li>Thể テ · V-ています</li><li>10 từ chữ Hán + từ chỉ công việc</li></ul></div>'
   '<div class="kcd kp"><h3>Bài tập về nhà</h3><ul class="ck"><li>App → Tài liệu → Ngữ pháp 初級1 Bài 1: làm worksheet</li><li>Chia thể テ 15 động từ</li><li>Ghi âm giới thiệu công việc (3 câu)</li></ul></div></div>')
S.append(f'''<section class="slide dark"><div class="cover"><img class="lg" src="{LOGO}"><div class="kk">おつかれさまでした！</div><h1>Hết buổi 1<br><span>Buổi sau: 初級1 第2課</span></h1><p>ゲームをするのが好きです</p></div>{CR}</section>''')

used = set(''.join(KW))
out = (HEAD2.replace('<title>Kính ngữ trong JFT-Basic</title>', '<title>Buổi 1 · いろどり 初級1 第1課</title>') + ''.join(S)
       + '<script>window.KVG=' + json.dumps({c: KVG[c] for c in used if c in KVG}, ensure_ascii=False, separators=(',', ':')) + '</script>' + KVGJS + TAIL + VSTEP + '''<script>window.cloudMix=s=>{const w=s.querySelector('.clw');const a=[...w.children];for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}a.forEach(x=>{x.classList.remove('on');w.appendChild(x)});
const n=a.map((_,i)=>i+1);for(let i=n.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[n[i],n[j]]=[n[j],n[i]]}a.forEach((x,i)=>x.querySelector('i').textContent=n[i])};
document.querySelectorAll('.clw').forEach(w=>{cloudMix(w.closest('.slide'));w.querySelectorAll('.cld').forEach(c=>c.onclick=e=>{e.stopPropagation();c.classList.toggle('on')})});</script>''')
open(R + 'public/tailieu/Buoi01_Shokyu1_Bai01.html', 'w').write(out)
print(len(S), 'slides', len(out) // 1024, 'KB')
