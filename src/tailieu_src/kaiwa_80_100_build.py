"""Slide tổng ôn 会話と表現 · câu 80–100 (theo file TỔNG ÔN KAIWA-HYOGEN.pdf: Đề 7 câu 5 → Đề 9 câu 1). 18/11/2026.
Đề bài + đáp án lấy từ bộ đề trong app (src/tailieu_src/kaiwa/cau80_100_raw.json, trích từ dữ liệu làm file PDF);
dịch + giải thích ngắn + bảng ôn là tự soạn (kaiwa/cau80_100_gt.py).
Chạy: python3 src/tailieu_src/kaiwa_80_100_build.py → public/tailieu/TongOn_KaiwaHyogen_80_100.html"""
import re, json, html
R = '/home/claude/anhtrong-jft-app/'
exec(open(R + 'src/tailieu_src/_head_snip.py').read())  # HEAD, LOGO
_kg = open(R + 'src/tailieu_src/khaigiang_build.py').read()
KGCSS = _kg[_kg.index("HEAD = HEAD.replace('</style></head>', '''") + 41:_kg.index("</style></head>''', 1)")]
exec(open(R + 'src/tailieu_src/kaiwa/cau80_100_gt.py').read())  # GT, SUM
TAIL = open(R + 'src/tailieu_src/buoi15_tail.html').read()
Q = json.load(open(R + 'src/tailieu_src/kaiwa/cau80_100_raw.json'))
def rb(s): return re.sub(r'\{([^|{}]+)\|([^{}]+)\}', r'<ruby>\1<rt>\2</rt></ruby>', s)
# sửa lỗi gõ rõ ràng trong đề gốc
FIX = {84: [('B : ありがとうございます', 'A : ありがとうございます')],
       89: [('<rt>ほう</rt>', '<rt>かた</rt>')]}
CSS = KGCSS + '''
.kw .kk2{font-size:24px}
.kwc{display:flex;gap:34px;margin-top:20px;align-items:flex-start}
.kwl{flex:1;min-width:0}
.dlg{background:#fff;border-radius:20px;padding:16px 30px;box-shadow:0 8px 24px #0d2b4012;font-family:"Klee One",serif;font-weight:600;font-size:30px;line-height:2.0;color:#0d2b40}
.dlg p{display:flex;gap:12px;margin:0}.dlg .sp{flex:none;color:#0d5a8c;font-weight:600}.dlg .tx{flex:1}
.dlg rt{font-size:.48em;color:#47647a}
.blk{display:inline-block;min-width:170px;border-bottom:3px solid #c42f66;margin:0 6px;text-align:center;line-height:1.35;vertical-align:baseline}
.fl{visibility:hidden;color:#2f9e5b}.slide.rv .fl{visibility:visible}
.kw .opts.list{margin-top:18px;gap:12px;max-width:none}
.kw .opts.list .o{height:66px;padding:0 24px}.kw .o b{font-size:30px}.kw .o .ot{font-size:30px}.kw .o .ot rt{font-size:.5em}
.kw .opts.list.g2{grid-template-columns:1fr 1fr}
.kw .opts.list.cp{gap:9px}.kw .opts.list.cp .o{height:56px}.kw .opts.list.cp .o .ot,.kw .opts.list.cp .o b{font-size:28px}
.dlg.sm{font-size:27px;line-height:1.85;padding:12px 28px}
.ex.kx{display:block;visibility:hidden;flex:0 0 480px;margin-top:0;font-size:27px;line-height:1.55;border-left:8px solid #2f9e5b;padding:20px 26px}
.ex.kx.on{visibility:visible}
.kx .a{font-size:30px;font-weight:700;color:#2f9e5b;margin-bottom:10px}
.kx .lb{font-size:20px;font-weight:700;letter-spacing:1px;color:#6b8296;margin-top:12px}
.kx p{margin:4px 0 0}.kx u{text-decoration:none;border-bottom:3px solid #f2a93b}.kx b{color:#c42f66;font-family:"Klee One",serif;font-weight:600}.kx rt{font-size:.5em}
.kx .g{font-size:26px}
.sum2{width:100%;border-collapse:collapse;font-size:27px;margin-top:20px;background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 8px 24px #0d2b4012}
.sum2 td{padding:11px 22px;border-bottom:1px solid #e3ebf2}.sum2 tr:last-child td{border:0}
.sum2 td.k{font-family:"Klee One",serif;font-weight:600;font-size:33px;color:#0d2b40;white-space:nowrap}.sum2 td.k rt{font-size:.5em}
.sum2 td.n{color:#6b8296;font-size:22px;text-align:right;white-space:nowrap}
'''
HEADX = HEAD.replace('</style></head>', CSS + '</style></head>', 1).replace('<title>Kính ngữ trong JFT-Basic</title>', '<title>Tổng ôn 会話と表現 · Câu 80–100</title>')
CR = '<div class="cr">Tổng ôn 会話と表現 · câu 80–100 · Anh Trọng Dạy JFT · đề bài: bộ đề thi thử JFT trong app · dịch, giải thích và bảng ôn là tự soạn</div>'
NUM = '①②③④'
BL = r'[（(]\s*[_＿]{2,}\s*[)）]|[（(][\s　]+[)）]|＿{2,}|_{3,}'
S = []
S.append(f'''<section class="slide dark"><div class="cover"><img class="lg" src="{LOGO}"><div class="kk">TỔNG ÔN JFT · 会話と表現</div>
<h1>Hội thoại · Diễn đạt<br><span>Câu 80 – 100</span></h1></div>{CR}</section>''')
for q in Q:
    n = q['n']; lines = q['lines']
    for a, b in FIX.get(n, []):
        lines = [l.replace(a, b) for l in lines]
    if n == 94:  # 係人 bị tách dòng khi trích → ghép lại thành 係の人
        L = []
        for l in lines:
            if re.fullmatch(r'<ruby>係<rt>[^<]*</rt></ruby>', l.strip()): continue
            L.append(re.sub(r'^<ruby>人<rt>[^<]*</rt></ruby>\s*：', '<ruby>係<rt>かかり</rt></ruby>の<ruby>人<rt>ひと</rt></ruby>：', l))
        lines = L
    if n == 98:
        lines = [x for l in lines for x in re.split(r'(?=<ruby>タイ)|(?=タイ<ruby>)', l) if x.strip()]
    ans_txt = re.sub(r'[。\s]+$', '', q['opts'][q['a']])
    body = ''
    for l in lines:
        l = re.sub(BL, f'<span class="blk"><span class="fl">{ans_txt}</span></span>', l, count=1)
        m = re.match(r'^((?:<ruby>[^<]+<rt>[^<]+</rt></ruby>|[^：:<\s]){1,8}?)\s*[：:]\s*(.*)$', l)
        if m: body += f'<p><span class="sp">{m.group(1)}：</span><span class="tx">{m.group(2)}</span></p>'
        else: body += f'<p><span class="tx">{l}</span></p>'
    ks = 'abcd'
    ob = ''.join(f'<button class="o" data-k="{ks[i]}"><b>{NUM[i]}</b><span class="jp ot">{o}</span><i></i><em></em></button>' for i, o in enumerate(q['opts']))
    vi, gt = GT[n]
    plain = re.sub(r'<rt>.*?</rt>|<[^>]+>', '', ''.join(lines))
    dcls = ' sm' if (len(lines) >= 6 or len(plain) > 130) else ''
    olen = max(len(re.sub(r'<rt>.*?</rt>|<[^>]+>', '', o)) for o in q['opts'])
    ocls = (' g2' if olen <= 10 else ' cp') if len(q['opts']) == 4 else ''
    S.append(f'''<section class="slide qz kw"><div class="kk2">Câu {n} <span class="src">{q["de"]} · câu {q["qi"]}</span></div>
<div class="kwc"><div class="kwl"><div class="dlg{dcls}">{body}</div><div class="opts list{ocls}" data-a="{ks[q["a"]]}">{ob}</div></div>
<div class="ex kx"><div class="a">Đáp án {NUM[q["a"]]}</div><div class="lb">DỊCH</div><p>{rb(vi)}</p><div class="lb">GIẢI THÍCH</div><p class="g">{rb(gt)}</p></div></div>{CR}</section>''')
half = (len(SUM) + 1) // 2
for k, part in enumerate([SUM[:half], SUM[half:]]):
    rows = ''.join(f'<tr><td class="k">{rb(p)}</td><td>{m}</td><td class="n">câu {c}</td></tr>' for p, m, c in part)
    S.append(f'<section class="slide"><h2>Ôn nhanh các cách nói vừa gặp <small>({k + 1}/2)</small></h2><table class="sum2">{rows}</table>{CR}</section>')
S.append(f'''<section class="slide dark"><div class="cover"><img class="lg" src="{LOGO}"><div class="kk">おつかれさまでした！</div>
<h1>Hết câu 100<br><span>Làm lại các câu sai trên app</span></h1><p>Làm đề → Ôn tập Kaiwa hyōgen</p></div>{CR}</section>''')
PATCH = "<script>(function(){const a=window.ans;window.ans=function(){a();try{S[cur].classList.add('rv')}catch(e){}}})()</script>"
out = HEADX + ''.join(S) + TAIL.replace('</body>', PATCH + '</body>')
open(R + 'public/tailieu/TongOn_KaiwaHyogen_80_100.html', 'w').write(out)
print(len(S), 'slides', len(out) // 1024, 'KB')
