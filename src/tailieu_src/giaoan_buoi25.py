"""Giáo án giáo viên cho Lớp cơ bản Buổi 2–5 (Tổng ôn いろどり 入門 Bài 10–18) — 19/11/2026.
Bước 1: node src/tailieu_src/giaoan_extract2.js Buoi0N_TongOn_NhapMon_N.html /tmp/ga/bN.json   (N = 2..5, chạy trong thư mục có playwright)
Bước 2: python3 src/tailieu_src/giaoan_buoi25.py  → /tmp/ga/GiaoAn_Buoi0N.html → PDF (node /tmp/ga/pdf.js)
Lời giảng từ vựng: giaoan_vocab_notes.py (VEXP). Lời giảng chữ Hán, ngữ pháp, từ khó: giaoan_buoi25_notes.py (KEXP, GSCRIPT, HEXP) — tự soạn.
Giải thích ngữ pháp "theo 文法ノート" và câu ví dụ: 文法ノート いろどり 入門. Câu nghe, câu đọc: bộ đề trong app (đã có đáp án, dịch, giải thích)."""
import json, html, re
R = '/home/claude/anhtrong-jft-app/'
_old = open(R + 'src/tailieu_src/giaoan_tongon_nhapmon.py').read()
_defs = _old[:_old.index('# ---------- dựng ----------')].replace("SL = json.load(open('/tmp/ga/slides.json'))", '')
exec(_defs)   # VOC, KAN, GB, RB, rel, VEXP, VNOTE, GNOTE, TNOTE, VW, KK, E, rb
CSS = re.search(r"CSS = '''(.*?)'''", _old, re.S).group(1)
CSS = CSS.replace('</style>', '.sc{background:#eef7ee;border-left:4px solid #2f9e5b;padding:6px 10px;border-radius:6px;margin:5px 0}.sc b{color:#2f7a48}.nb{background:#f4f9fe;border-left:4px solid #0d5a8c;padding:6px 10px;border-radius:6px;margin:5px 0;font-size:10pt}.tm2{display:inline-block;background:#c42f66;color:#fff;border-radius:99px;padding:0 10px;font-size:9pt;margin-left:6px}.pl{margin:4px 0 4px 18px;padding:0}</style>')
import os, sys
_FD = next((d for d in ('/home/claude/jftlich/f/node_modules/@fontsource/', '/tmp/fs/node_modules/@fontsource/') if os.path.isdir(d + 'm-plus-rounded-1c')), '/tmp/fs/node_modules/@fontsource/')
FONT = ''.join(f'<link rel="stylesheet" href="file://{_FD}m-plus-rounded-1c/{w}.css">' for w in (500, 700, 800))
exec(open(R + 'src/tailieu_src/giaoan_buoi25_notes.py').read())   # GSCRIPT, KEXP, HEXP
HW = {w: (r, h, v) for k in ('tau', 'bien') for (w, r, h, v) in []}
_tb = open(R + 'src/tailieu_src/tongon_nhapmon_build.py').read()
_h = _tb[_tb.index('HARD = {'):_tb.index('def hook_vocab')]
_ns = {}
exec('jp=lambda s:s\n' + _h, _ns)
for key, (t, ws, qs) in _ns['HARD'].items():
    for w, r, h, v in ws: HW[w] = (r, h, v)

TITLE = {2: ('Bài 10 – 11', 'ホチキス貸してください · どんなマンガが好きですか？'), 3: ('Bài 12 – 13', 'いっしょに飲みに行きませんか？ · このバスは空港に行きますか？'),
         4: ('Bài 14 – 16', '大きな建物ですね · 電池がほしいんですが… · これ、いくらですか？'), 5: ('Bài 17 – 18', '映画を見に行きました · 温泉に入りたいです')}
SECOP = {'Từ vựng': 'Mở slide tranh, cho học viên đoán trước khi bấm. Mỗi tranh: đọc mẫu 1 lần, cả lớp đọc theo 2 lần, rồi giảng theo phần "Lời giảng".',
         'Chữ Hán': 'Mỗi chữ 1 slide: nét viết tự chạy khi mở slide, học viên viết theo ra giấy. Giảng theo thứ tự: cách đọc → từng chữ (Hán Việt, On, Kun) → cách nhớ → ví dụ → từ liên quan.',
         'Ngữ pháp': 'Mỗi mẫu 1 slide dạy + 1 câu luyện ngay sau. Trên slide dạy: bấm → để hiện từng ý "Cách dùng", rồi hiện nghĩa từng câu ví dụ. Câu luyện: học viên bình chọn rồi mới bấm Đáp án.',
         'Nghe hiểu': 'Mỗi câu: đọc câu hỏi và phương án trước (30 giây) → nghe lần 1, bình chọn → nghe lần 2 → Đáp án → mở 📄 Script, chỉ ra câu chứa đáp án.',
         'Đọc hiểu': 'Dạy cách đọc trước (slide kỹ năng), sau đó mỗi câu cho học viên tự đọc 1–2 phút rồi bình chọn; chữa bằng nút 📄 Dịch · giải thích.',
         'Đọc bảng thông tin': 'Dạy 4 bước đọc bảng trước, làm mẫu 1 câu cùng lớp, sau đó học viên tự làm từng câu 1–2 phút rồi bình chọn; chữa bằng nút 📄 Dịch · giải thích.'}

def build_ga(no):
    SL = json.load(open(f'/tmp/ga/b{no}.json'))
    B = []
    def blk(n, title, body, kind=''):
        B.append(f'<section class="b {kind}"><div class="hd"><span class="sn">{n}</span><span class="tt">{title}</span></div>{body}</section>')
    plan = []
    for s in SL:
        n = f'Slide {s["i"]}'; t = s['t']
        if t == 'cover':
            if s['i'] == 1: continue
            blk(n, 'Kết thúc buổi', '<p class="op">Slide chào kết. Nhắc lịch buổi sau và bài tập về nhà.</p>', 'sec')
        elif t == 'plan':
            plan = s['items']
            blk(n, 'Nội dung buổi học', '<p class="op">Mở đầu (2 phút): đọc nhanh 5 phần và thời lượng để học viên biết hôm nay học gì.</p><ul class="pl">' + ''.join(f'<li>{E(x).replace(chr(10), " · ")}</li>' for x in s['items']) + '</ul>')
        elif t == 'sec':
            op = SECOP.get(s['txt'], 'Slide chuyển phần: nói ngắn gọn mục tiêu phần này.')
            blk(n, E(s['txt']) + f' <small>{E(s.get("d", ""))}</small>', f'<p class="op">{op}</p>', 'sec')
        elif t == 'vocab' and s['h2'].startswith('Từ khó'):
            items = ''.join(f'<div class="wi"><div class="wh"><span class="jw">{E(w)}</span> <span class="rd">{E(HW[w][0])}</span> — <b>{E(HW[w][2])}</b> · <span class="hv">{E(HW[w][1])}</span></div><div class="we">{E(HEXP.get(w, ""))}</div></div>' for w in s['w'] if w in HW)
            blk(n, E(s['h2']), '<p class="op">Thao tác: bấm lần 1 hiện cách đọc, lần 2 hiện nghĩa. Đây là chữ trên biển báo, thông báo thật — học viên chỉ cần nhận ra và hiểu nghĩa, chưa cần viết.</p>' + items)
        elif t == 'vocab':
            b = int(re.search(r'Bài (\d+)', s['h2']).group(1)); g = GB.get(b)
            head, notes = VNOTE.get(b, ('', []))
            items = ''
            for w in s['w']:
                v = VW.get(w) or next((x for x in VOC if x['r'] == w or x['w'].replace(' ', '') == w.replace(' ', '')), None)
                key = v['w'] if v else w
                ex = v.get('ex') if v else None
                exs = f'<div class="wex"><b>Ví dụ (sách):</b> <span class="jp">{rb(ex[0])}</span> — {E(ex[1])}</div>' if ex else ''
                kc = f' · Hán Việt: <b class="hv">{E(v["hv"])}</b>' if v and v.get('hv') else ''
                items += (f'<div class="wi"><div class="wh"><span class="jw">{v["wr"] if v else E(w)}</span> <span class="rd">{E(v["r"]) if v else ""}</span> — <b>{E(v["vi"]) if v else ""}</b>{kc}</div>'
                          f'<div class="we">{VEXP.get(key, VEXP.get(w, ""))}</div>{exs}</div>')
            blk(n, f'Từ vựng · Bài {b} {rb(g["title"]) if g else ""} <small>{E(g["title_vi"]) if g else ""}</small>',
                '<p class="op">Thao tác: mở slide chỉ thấy tranh → học viên đoán → bấm lần 1 hiện tiếng Nhật (cả lớp đọc to 2 lần) → bấm lần 2 hiện nghĩa. Giảng từng từ theo thứ tự dưới đây.</p>'
                f'<div class="lg"><b>Chủ đề: {head}</b><ul>' + ''.join(f'<li>{x}</li>' for x in notes) + f'</ul></div>{items}')
        elif t == 'kanji':
            k = KK.get(s['w'])
            if not k: continue
            chars = ''.join(f'<li><b class="kc">{E(c["k"])}</b> <span class="hv">{E(c["hv"])}</span> · On: {E(c.get("on") or "–")} · Kun: {E(c.get("kun") or "–")} · nghĩa: {E(c.get("vi") or "")}</li>' for c in k['chars'])
            rl = rel(k['w']); rl = re.sub(r'<b>Từ liên quan</b>', '', rl).replace('class="krel st"', 'class="krel"')
            ex = k.get('ex') or {}
            blk(n, f'Chữ Hán · <span class="jbig">{E(k["w"])}</span> <span class="hv">{E(k["hv"])}</span> <small>{E(k["r"])} · {E(k["vi"])}</small>',
                '<p class="op">Thao tác: nét viết tự chạy khi mở slide — học viên viết theo ra giấy, bấm "Chậm" nếu chữ nhiều nét. Sau đó bấm lần lượt: cách đọc → bảng từng chữ → cách nhớ → ví dụ.</p>'
                f'<div class="sc"><b>Lời giảng:</b> {E(KEXP.get(k["w"], ""))}</div>'
                f'<div class="lg"><p><b>Bảng từng chữ (trên slide):</b></p><ul>{chars}</ul>'
                + (f'<p><b>Ví dụ trên slide:</b> <span class="jp">{ex["jp"]}</span> — {E(ex.get("vi", ""))}</p>' if ex.get('jp') else '')
                + (f'<p><b>Từ liên quan (mở rộng nếu còn thời gian):</b></p>{rl}' if rl else '') + '</div>')
        elif t == 'kgrid':
            NUM = next((k for k in KK if '、' in k), None)
            ks = [KK[NUM] if w == '一〜十' and NUM else KK[w] for w in s['w'] if w in KK or (w == '一〜十' and NUM)]
            rows = ''.join(f'<tr><td class="jw">{E(k["w"] if "、" not in k["w"] else "一〜十")}</td><td>{E(k["r"])}</td><td>{E(k["hv"])}</td><td>{E(KEXP.get(k["w"], k["vi"]))}</td></tr>' for k in ks)
            blk(n, f'Chữ Hán · {E(s["h2"])}', '<p class="op">Thao tác: bấm từng thẻ để hiện cách đọc; nút ✍ Nét trên mỗi thẻ mở nét viết. Cho cả lớp đọc nhanh theo thứ tự, rồi anh đọc giá tiền bất kỳ (380円, 1,600円, 8,000円) để học viên viết số.</p>'
                f'<table class="vt"><tr><th>Chữ</th><th>Cách đọc</th><th>Hán Việt</th><th>Lời giảng</th></tr>{rows}</table>')
        elif t == 'gx':
            b = int(re.search(r'Bài (\d+)', s['h2']).group(1)); g = GB[b]; pno = s['no']
            p = next(x for x in g['points'] if x['no'] == pno)
            exs = ''.join(f'<li><span class="jp">{rb(e["jp"])}</span><br><small>{E(e["vi"]).replace(chr(10), "<br>")}</small></li>' for e in p['examples'] + p.get('more_examples', []))
            blk(n, f'Ngữ pháp · Bài {b} · {E(pno)} <span class="jp">{rb(p["pattern"])}</span> <small>{E(p["meaning_vi"])}</small>',
                '<p class="op">Thao tác: mở slide thấy mẫu câu + ví dụ tiếng Nhật. Bấm → hiện từng ý "Cách dùng", rồi hiện nghĩa từng câu ví dụ. Cho học viên đọc to từng câu ví dụ trước khi hiện nghĩa.</p>'
                f'<div class="sc"><b>Lời giảng:</b> {GSCRIPT.get((b, pno), "")}</div>'
                + (f'<div class="nh"><b>Nhấn mạnh:</b> {GNOTE[(b, pno)]}</div>' if (b, pno) in GNOTE else '')
                + '<div class="lg"><b>Giải thích của 文法ノート (nội dung trên slide):</b>' + ''.join(f'<p>{rb(x)}</p>' for x in p['explain_vi']) + '</div>'
                + f'<div class="exs"><b>Câu ví dụ (sách + 文法ノート) — slide hiện 3 câu đầu, các câu sau anh đọc thêm:</b><ul>{exs}</ul></div>', 'gm2')
        elif t == 'table':
            rows = ''.join('<tr>' + ''.join(f'<td>{E(c)}</td>' for c in r) + '</tr>' for r in s['rows'])
            note = TNOTE if 'Ký hiệu' not in s['h2'] else 'Bấm từng ô để hiện nghĩa. Cho học viên đọc to từng ký hiệu; nhấn mạnh dòng ※ vì đáp án hay nằm ở đó.'
            blk(n, E(s['h2']), f'<p class="op">{note}</p><table class="vt">{rows}</table>' + (f'<div class="nh">{E(s["pb"])}</div>' if s.get('pb') else ''))
        elif t == 'quiz':
            ks = 'abcd'; op = ''.join(f'<li class="{"ok" if ks[i] == s["a"] else ""}">{ks[i]}. {E(o)}</li>' for i, o in enumerate(s['opts']))
            blk(n, f'Luyện tập · {E(s["src"])}', '<p class="op">Thao tác: học viên bấm chọn để bình chọn (số phiếu hiện trên từng phương án) → anh bấm "Đáp án" và đọc giải thích.</p>'
                + (f'<p class="qq"><b>{E(s["big"])}</b></p>' if s.get('big') else '') + f'<p class="qq">{E(s["q"])}</p><ul class="op2">{op}</ul><div class="nh">{E(s["ex"])}</div>', 'qz')
        elif t in ('listen', 'read'):
            ks = 'abcd'; op = ''.join(f'<li class="{"ok" if ks[i] == s["a"] else ""}">{ks[i]}. {E(o)}</li>' for i, o in enumerate(s['opts']))
            how = ('(1) Đọc câu hỏi và các phương án trước, gạch chân từ khoá. (2) Nghe lần 1, học viên bình chọn. (3) Nghe lần 2 để kiểm tra. (4) Bấm Đáp án, mở 📄 Script, đọc lại từng câu và chỉ ra câu chứa đáp án.' if t == 'listen' else
                   '(1) Đọc câu hỏi trước, gạch từ để hỏi và điều kiện. (2) Học viên tự tìm thông tin trong bài 1–2 phút rồi bình chọn. (3) Bấm Đáp án, mở 📄 Dịch · giải thích, khoanh trên ảnh chỗ có đáp án (dùng bút).')
            blk(n, f'{"Nghe hiểu" if t == "listen" else "Đọc hiểu"} · {E(s["src"])}', f'<p class="op">Cách dạy: {how}</p><p class="qq">{E(s["q"])}</p><ul class="op2">{op}</ul><div class="ls">{s["exh"]}</div>', 'qz')
        elif t == 'skill':
            blk(n, E(s['h2']), '<p class="op">Thao tác: bấm để hiện từng ô. Giảng từng bước, mỗi bước lấy ngay một ví dụ trong đề đã làm.</p><ul class="pl">' + ''.join(f'<li>{E(x)}</li>' for x in s['items']) + '</ul>'
                + (f'<div class="nh">{E(s["pb"])}</div>' if s.get('pb') else ''))
        elif t == 'demo':
            blk(n, E(s['h2']), '<p class="op">Làm mẫu cùng lớp: anh vừa nói vừa dùng bút khoanh trên bảng, đi đúng 4 bước. Bấm để hiện từng bước.</p><ul class="pl">' + ''.join(f'<li>{E(x)}</li>' for x in s['items']) + '</ul>')
        else:
            blk(n, E(s.get('h2') or 'Tổng kết').replace('\n', ' '), '<p class="op">Chốt lại kiến thức đã ôn (đọc cột "Đã ôn") và giao bài tập về nhà (cột bên phải). Nhắc học viên ôn trên app trước buổi sau.</p>')
    st, (bai, ttl) = len(SL), TITLE[no]
    intro = (f'<h1>Giáo án · Lớp cơ bản · Buổi {no}</h1><div class="sub">Tổng ôn いろどり 入門 {bai} · {ttl} · Anh Trọng Dạy JFT</div>'
             f'<div class="intro"><b>Slide:</b> app → Tài liệu → Theo buổi học → Lớp cơ bản · Buổi {no} (file Buoi0{no}_TongOn_NhapMon_{no}.html, {st} slide). Giáo án đi theo đúng số slide.<br>'
             '<b>Thời lượng 90 phút:</b> ' + ' · '.join(E(x).replace('\n', ' ') for x in plan) + '<br>'
             '<b>Phím tắt trên slide:</b> → / Space: hiện từng phần · Enter: đáp án · A: hiện hết · P: bút · T: gõ chữ · M: memo · F: cỡ chữ · <b>G: thanh xem nhanh các slide</b> (bấm ảnh nhỏ để nhảy tới).<br>'
             '<b>Cách đọc giáo án:</b> khung xanh lá "Lời giảng" là phần anh nói với lớp; khung vàng "Nhấn mạnh" là chỗ học viên hay sai; khung xám là nội dung có sẵn trên slide.<br>'
             '<b>Nguồn:</b> từ vựng, câu ví dụ, giải thích ngữ pháp theo いろどり 入門 và 文法ノート いろどり (Quỹ Giao lưu Quốc tế Nhật Bản); lời giảng, nhấn mạnh, cách dạy là tự soạn; câu nghe, câu đọc lấy từ bộ đề trong app.</div>')
    out = f'/tmp/ga/GiaoAn_LopCoBan_Buoi0{no}.html'
    open(out, 'w').write('<!doctype html><html><head><meta charset="utf-8">' + FONT + CSS + '</head><body>' + intro + ''.join(B) + '</body></html>')
    miss = [s.get('w') for s in SL if s['t'] == 'kanji' and s.get('w') not in KEXP] + [s.get('no') for s in SL if s['t'] == 'gx' and not GSCRIPT.get((int(re.search(r'Bài (\d+)', s['h2']).group(1)), s['no']))]
    print(out, len(B), 'khối', 'THIẾU lời giảng:' if miss else '', miss or '')

for no in ([int(x) for x in sys.argv[1:]] or (2, 3, 4, 5)): build_ga(no)   # vd: python3 giaoan_buoi25.py 3
