"""Tài liệu PDF gửi học viên — Lớp cơ bản JFT · Buổi 3 (いろどり 入門 Bài 12–13), 22/11/2026.
Từ vựng (DOCS + từ khó 'tau') · Chữ Hán (DOCS kanji + thứ tự nét KanjiVG + ô tập viết) · Ngữ pháp (文法ノート いろどり, đủ Bài 12–13)
· Bài tập (đọc từ, chọn chữ Hán, trắc nghiệm ngữ pháp, điền trợ từ, chuyển câu có tranh, hội thoại) · Đáp án.
Chạy: python3 src/tailieu_src/handout_buoi3.py → /tmp/b3/out.html ; node src/tailieu_src/handout_pdf.js /tmp/b3/out.html <ra.pdf>"""
import json, re, html, sys, os
R = '/home/claude/anhtrong-jft-app/'
sys.path.insert(0, R + 'src/jft')
from furi import furi
FS = '/tmp/fs/node_modules/@fontsource/'
OUT = '/tmp/b3/out.html'

def js(f):
    s = open(R + 'public/app/data/' + f, encoding='utf-8').read()
    return json.JSONDecoder().raw_decode(s[s.index('=') + 1:])[0]
D = js('docs.js'); G = js('grammar.js')
KVG = json.load(open(R + 'src/tailieu_src/kanjivg_strokes.json'))
BAIS = (12, 13)
V = [w for w in D['vocab']['入門'] if w['b'] in BAIS]
KW = ['今週', '今度', '来週', '休み', '予定', '東', '南', '会社', '来ます', '行きます', '乗ります']
KD = {k['w']: k for k in D['kanji']['入門'] if k['w'] in KW}
K = [KD[w] for w in KW]
GL = {x['bai']: x for x in G if x['lv'] == '入門' and x['bai'] in BAIS}
HARD = [('改札', 'かいさつ', 'CẢI TRÁT', 'cửa soát vé'), ('快速', 'かいそく', 'KHOÁI TỐC', 'tàu nhanh'),
        ('各駅停車', 'かくえきていしゃ', 'CÁC DỊCH ĐÌNH XA', 'tàu dừng mọi ga'), ('終点', 'しゅうてん', 'CHUNG ĐIỂM', 'ga cuối'),
        ('乗り換え', 'のりかえ', 'THỪA HOÁN', 'chuyển tàu'), ('反対側', 'はんたいがわ', 'PHẢN ĐỐI TRẮC', 'phía đối diện'),
        ('1日', 'ついたち', 'cách đọc đặc biệt', 'ngày mùng 1'), ('20日', 'はつか', 'cách đọc đặc biệt', 'ngày 20'),
        ('入場無料', 'にゅうじょうむりょう', 'NHẬP TRƯỜNG VÔ LIỆU', 'vào cửa miễn phí'), ('問い合わせ先', 'といあわせさき', 'VẤN HỢP TIÊN', 'nơi liên hệ')]
HARDQ = [('改札', 'かいさつ', ['かいさく', 'かいざつ', 'がいさつ'], 'cửa soát vé'), ('終点', 'しゅうてん', ['しゅってん', 'しゅうでん', 'じゅうてん'], 'ga cuối'),
         ('20日', 'はつか', ['にじゅうにち', 'はっか', 'はつび'], 'ngày 20 (cách đọc đặc biệt)')]

e = html.escape
VIX = [(' (shuttle bus)', ''), ('(shuttle bus)', ''), ('Bus Center', 'Trung tâm xe buýt'), ('tennis', 'quần vợt')]
def VI(t):
    for a, b in VIX: t = t.replace(a, b)
    return t
RB = lambda s: re.sub(r'\{([^|{}]+)\|([^{}]+)\}', r'<ruby>\1<rt>\2</rt></ruby>', e(VI(s))).replace('\n', '<br>')
J = lambda s: furi(e(s))
PLAIN = lambda s: re.sub(r'\{([^|]+)\|[^}]+\}', r'\1', s)
def img(path): return 'file://' + R + 'public/' + path
LOGO = 'file://' + R + 'public/app/media/brand/logo-ngang.svg'
LOGOW = 'file://' + R + 'public/app/media/brand/logo-ngang-trang.svg'

# ---------- thứ tự nét (KanjiVG) ----------
def stroke_strip(ch, size=13):
    d = KVG[ch]; P = d['p']; n = len(P); o = []
    for i in range(n):
        g = ''.join(f'<path d="{P[j]}" class="{"cur" if j == i else "old"}"/>' for j in range(i + 1))
        x, y = d['n'][i] if i < len(d['n']) else (0, 0)
        o.append(f'<svg viewBox="0 0 109 109" style="width:{size}mm;height:{size}mm" class="sk"><path d="M54.5 2V107M2 54.5H107" class="gd"/>{g}'
                 f'<circle cx="{x + 3}" cy="{y - 3}" r="7" class="nb"/><text x="{x + 3}" y="{y + 0.5}" class="nt">{i + 1}</text></svg>')
    return f'<div class="strip"><div class="sh"><span class="jp">{ch}</span><small>{n} nét</small></div><div class="sks">{"".join(o)}</div></div>'

# ---------- câu có từ gạch chân (bỏ furigana của từ được hỏi) ----------
def segs(h):
    out = []
    for m in re.finditer(r'<ruby>(.*?)<rt>(.*?)</rt></ruby>|(<[^>]+>)|([^<])', h):
        if m.group(1) is not None: out.append(('r', m.group(1), m.group(2)))
        elif m.group(3): pass
        else: out.append(('c', m.group(4), ''))
    return out
def underline(h, target, repl=None):
    S = segs(h); txt = ''.join(s[1] for s in S); i = txt.find(target)
    if i < 0: return None
    j = i + len(target); o = []; pos = 0; opened = False
    for kind, base, rt in S:
        a, b = pos, pos + len(base); pos = b
        if b <= i or a >= j:
            o.append(f'<ruby>{base}<rt>{rt}</rt></ruby>' if kind == 'r' else base); continue
        pre, mid, post = base[:max(0, i - a)], base[max(0, i - a):min(len(base), j - a)], base[min(len(base), j - a):]
        if pre: o.append(pre)
        if not opened: o.append('<u>' + (repl if repl is not None else '')); opened = True
        if repl is None: o.append(mid)
        if b >= j: o.append('</u>')
        if post: o.append(post)
    return ''.join(o)

# ---------- xáo vị trí đáp án (cố định, cân bằng a/b/c/d) ----------
def place(right, wrong, k):
    opts = [right] + list(wrong)
    pos = k % len(opts); opts.remove(right); opts.insert(pos, right)
    return opts, pos

ABC = 'abcd'
ANS = []   # (phần, [(số, đáp án, giải thích)])

# ====================== HTML ======================
H = []
def sec(no, vi, jp, desc):
    H.append(f'<div class="secb"><div class="no">{no}</div><div><div class="st">{vi} <span class="jp">{jp}</span></div><div class="sd">{desc}</div></div></div>')

# --- Bìa ---
T12, T13 = GL[12], GL[13]
H.append(f'''<section class="cover"><img class="clogo" src="{LOGO}">
<div class="ck">LỚP CƠ BẢN JFT · BUỔI 3</div>
<h1>Tài liệu học tập</h1><div class="csub">Tổng ôn <span class="jp">いろどり 入門</span> · Bài 12 – 13</div>
<div class="lcs"><div class="lc"><b>第12課</b><div class="jp">{RB(T12['title'])}</div><small>{e(T12['title_vi'])}</small></div>
<div class="lc"><b>第13課</b><div class="jp">{RB(T13['title'])}</div><small>{e(T13['title_vi'])}</small></div></div>
<div class="toc"><h3>Nội dung</h3><ol>
<li><b>Từ vựng</b> <span>{len(V)} từ của bài + {len(HARD)} từ khó hay gặp trong đề</span></li>
<li><b>Chữ Hán</b> <span>{len(K)} từ · thứ tự nét · ô tập viết</span></li>
<li><b>Ngữ pháp</b> <span>{sum(1 for b in BAIS for p in GL[b]['points'] if p['no'] != '◆')} mẫu câu · cách dùng trợ từ に・で · bảng tổng hợp</span></li>
<li><b>Bài tập luyện tập</b> <span>từ vựng · chữ Hán · ngữ pháp</span></li>
<li><b>Đáp án</b> <span>có giải thích ngắn</span></li></ol></div>
<div class="goal"><h3>Sau buổi học, em có thể</h3><ul>
<li>Nói và hiểu thông báo sự kiện: <span class="jp">【日時】に【場所】で【イベント】があります</span></li>
<li>Rủ bạn đi chơi, nhận lời hoặc từ chối: <span class="jp">〜ませんか・〜ましょう・〜に行きます</span></li>
<li>Hỏi và trả lời về phương tiện, thời gian đi lại: <span class="jp">〜で来ます・〜かかります・〜から〜まで</span></li>
<li>Đọc được từ tàu xe, ngày tháng hay gặp trong đề JFT</li></ul></div>
<div class="who"><div>Họ tên: <i></i></div><div>Ngày học: <i></i></div></div>
<div class="csrc">出典：いろどり 生活の日本語 入門、文法ノート いろどり（国際交流基金）· Nét viết: KanjiVG (CC BY-SA 3.0)<br>Bảng tổng hợp, cách nhớ, bài trắc nghiệm: Anh Trọng Dạy JFT soạn · Tài liệu dành cho học viên, vui lòng không đăng lại.</div></section>''')

# --- 1. Từ vựng ---
H.append('<section>')
sec('01', 'Từ vựng', 'ことば', 'Nhìn tranh, đọc to từ, nhớ nghĩa. Âm Hán Việt in hoa giúp đoán nghĩa chữ Hán.')
for b in BAIS:
    ws = [w for w in V if w['b'] == b]
    g = GL[b]
    H.append(f'<h2 class="lh"><span>第{b}課 · Bài {b}</span> <span class="jp">{RB(g["title"])}</span></h2><div class="vg">')
    for i, w in enumerate(ws, 1):
        pic = f'<img src="{img("app/media/doc/" + w["img"])}">' if w.get('img') else '<div class="nop"></div>'
        hv = f'<div class="hv">{e(w["hv"])}</div>' if w.get('hv') else ''
        H.append(f'<div class="vc">{pic}<div class="vt"><div class="vw jp{" lg" if len(w["w"]) > 5 else ""}">{w["wr"]}</div>{hv}<div class="vm">{e(w["vi"])}</div></div><span class="vn">{i}</span></div>')
    H.append('</div>')
H.append('<h2 class="lh hard"><span>Từ khó hay gặp trong đề</span> <small>tàu xe · ngày tháng · sự kiện</small></h2><table class="tb"><tr><th>#</th><th>Từ</th><th>Cách đọc</th><th>Hán Việt</th><th>Nghĩa</th></tr>')
for i, (w, r, hv, vi) in enumerate(HARD, 1):
    H.append(f'<tr><td class="c">{i}</td><td class="jp big">{e(w)}</td><td class="jp">{e(r)}</td><td class="hvc">{e(hv)}</td><td>{e(vi)}</td></tr>')
H.append('</table></section>')

# --- 2. Chữ Hán ---
H.append('<section>')
sec('02', 'Chữ Hán', 'かんじ', 'Âm Hán Việt · cách đọc · âm On / Kun · cách nhớ · ví dụ · thứ tự nét')
seen = set()
for i, k in enumerate(K, 1):
    rows = ''.join(f'<tr><td class="jp kk">{e(c["k"])}</td><td class="hvc">{e(c["hv"])}</td><td class="jp">{e(c.get("on") or "–")}</td><td class="jp">{e(c.get("kun") or "–")}</td><td>{e(c.get("vi") or "")}</td></tr>' for c in k['chars'])
    tip = re.sub(r'^\s*(Mẹo nhớ|Mẹo|Ghi nhớ)\s*:\s*', '', k.get('tip') or '')
    ex = k.get('ex') or {}
    strips = ''.join(stroke_strip(c) for c in dict.fromkeys(ch for ch in k['w'] if ch in KVG) if c not in seen)
    for ch in k['w']: seen.add(ch)
    H.append(f'''<div class="kc"><div class="kl"><span class="kno">{i}</span><div class="kw jp" style="font-size:{ {1: 34, 2: 34, 3: 27, 4: 22}.get(len(k['w']), 20)}pt">{e(k["w"])}</div><div class="kr jp">{e(k["r"])}</div><div class="khv">{e(k["hv"])}</div><div class="km">{e(k["vi"])}</div></div>
<div class="kr2"><table class="tb sm"><tr><th>Chữ</th><th>Hán Việt</th><th>Âm On</th><th>Âm Kun</th><th>Nghĩa</th></tr>{rows}</table>
{f'<div class="tip"><b>Cách nhớ</b> {e(tip)}</div>' if tip else ''}
{f'<div class="kex"><span class="jp">{ex["jp"]}</span><small>{e(ex.get("vi", ""))}</small></div>' if ex.get('jp') else ''}
{strips}</div></div>''')
H.append('</section>')
# ô tập viết
CH = list(dict.fromkeys(c for k in K for c in k['w'] if c in KVG))
H.append('<section class="wp">')
H.append('<h2 class="lh"><span>Tập viết chữ Hán</span> <small>Ô đầu: chữ mẫu · 3 ô xám: tô theo · các ô sau: tự viết</small></h2><div class="wg">')
for c in CH:
    hv = next((x['hv'] for k in K for x in k['chars'] if x['k'] == c), '')
    cells = f'<div class="wc m"><span>{c}</span></div>' + ''.join(f'<div class="wc t"><span>{c}</span></div>' for _ in range(3)) + '<div class="wc"></div>' * 6
    H.append(f'<div class="wr"><div class="wl"><b class="jp">{c}</b><small>{e(hv)}</small></div>{cells}</div>')
H.append('</div></section>')

# --- 3. Ngữ pháp ---
H.append('<section>')
sec('03', 'Ngữ pháp', 'ぶんぽう', 'Mẫu câu · nghĩa · cách dùng · ví dụ (文法ノート いろどり)')
NOTE = {(12, '❶'): 'Nơi diễn ra sự kiện dùng で, không dùng に: さくら公園でタイフェスティバルがあります。',
        (12, '❺'): 'Bỏ ます rồi thêm に行きます: 食べます → 食べに行きます. Với danh từ chỉ hoạt động: 買い物に行きます.',
        (13, '❸'): 'Đi bộ không dùng で: 歩いて来ます (không nói 歩いてで).',
        (13, '❺'): 'Lên xe: Nに乗ります · Xuống xe: Nを降ります · Chuyển tàu: Nに乗り換えます.'}
for b in BAIS:
    g = GL[b]
    H.append(f'<h2 class="lh"><span>第{b}課 · Bài {b}</span> <span class="jp">{RB(g["title"])}</span> <small>{e(g["title_vi"])}</small></h2>')
    for p in g['points']:
        xs = [x for x in p.get('explain_vi', []) if x.strip()]
        if p['no'] == '◆':
            H.append(f'<div class="gn"><div class="gnh"><b>Ghi chú</b> <span class="jp">{RB(p["pattern"])}</span> — {e(p["meaning_vi"])}</div><ul>' + ''.join(f'<li>{RB(x)}</li>' for x in xs) + '</ul></div>')
            continue
        exs = (p.get('examples') or []) + (p.get('more_examples') or [])
        note = NOTE.get((b, p['no']))
        H.append(f'''<div class="gp"><div class="gph"><span class="gno">{p["no"]}</span><span class="jp">{RB(p["pattern"])}</span></div><div class="gpm">{e(p["meaning_vi"])}</div>
<div class="gb"><div class="gu"><h4>Cách dùng</h4><ul>{''.join(f'<li>{RB(x)}</li>' for x in xs if not x.rstrip().endswith((':', '：')))}</ul>{f'<div class="gnote">{J(note)}</div>' if note else ''}</div>
<div class="ge"><h4>Ví dụ</h4>{''.join(f'<div class="ex"><div class="jp">{RB(x["jp"])}</div><small>{e(VI(x["vi"])).replace(chr(10), "<br>")}</small></div>' for x in exs)}</div></div></div>''')
TB = [('に', 'Nơi đến · nơi có · lên xe', '空港に行きます · バスに乗ります'), ('で', 'Nơi làm hành động, nơi có sự kiện · phương tiện', '駅で降ります · 電車で来ます'),
      ('へ', 'Hướng đi (= に)', '京都へ行きます'), ('を', 'Rời khỏi (xuống xe)', 'バスを降ります'), ('から・まで', 'Từ … đến …', '駅から会社まで')]
H.append('<div class="keep"><h2 class="lh"><span>Bảng tổng hợp</span> <small>Trợ từ chỉ nơi chốn, phương tiện (tự soạn)</small></h2><table class="tb"><tr><th>Trợ từ</th><th>Nghĩa</th><th>Ví dụ</th></tr>'
         + ''.join(f'<tr><td class="jp big c">{e(a)}</td><td>{e(m)}</td><td class="jp">{J(x)}</td></tr>' for a, m, x in TB) + '</table></div></section>')

# --- 4. Bài tập ---
H.append('<section>')
sec('04', 'Bài tập luyện tập', 'れんしゅう', 'Làm xong rồi mới xem Đáp án ở cuối tài liệu.')
def qopts(opts, cls=''):
    return f'<div class="op{cls}">' + ''.join(f'<span><b>{ABC[i]}</b> {o}</span>' for i, o in enumerate(opts)) + '</div>'
NQ = [0]
def part(title, ins):
    H.append(f'<h3 class="ph">{title}</h3><div class="ins">{ins}</div>')

# A1 – nhìn tranh chọn cách đọc
A = []
part('A1. Nhìn tranh, chọn cách đọc đúng', 'Khoanh tròn a, b, c hoặc d.')
pick = ['電車', '地下鉄', '飛行機', '自転車', '焼肉', '映画', '夏祭り', '忘年会']
H.append('<div class="pg">')
for i, w in enumerate(pick):
    x = next(v for v in V if v['w'] == w); NQ[0] += 1
    opts, a = place(x['r'], x['rd'][:3], i + 1)
    H.append(f'<div class="pq"><img src="{img("app/media/doc/" + x["img"])}"><div><div class="qn">{NQ[0]}. <span class="jp big">{e(w)}</span></div>{qopts([e(o) for o in opts], " col")}</div></div>')
    A.append((NQ[0], ABC[a], f'{w}（{x["r"]}）– {x["vi"]}'))
H.append('</div>')
ANS.append(('A1. Nhìn tranh, chọn cách đọc', A)); A = []
# A2 – nhìn tranh viết từ
part('A2. Nhìn tranh, viết từ tiếng Nhật', 'Viết bằng chữ katakana / hiragana.')
H.append('<div class="pg w">')
for w in ['バス', 'タクシー', 'バイク', 'ハイキング', '船', '車']:
    x = next(v for v in V if v['w'] == w); NQ[0] += 1
    H.append(f'<div class="pw"><img src="{img("app/media/doc/" + x["img"])}"><div class="qn">{NQ[0]}.</div><div class="ln"></div></div>')
    A.append((NQ[0], w + (f'（{x["r"]}）' if x.get('r') else ''), x['vi']))
H.append('</div>')
ANS.append(('A2. Nhìn tranh, viết từ', A)); A = []
# A3 – từ khó
part('A3. Từ hay gặp trong đề — chọn cách đọc đúng', '')
H.append('<div class="ql">')
for i, (w, r, wr, vi) in enumerate(HARDQ):
    NQ[0] += 1; opts, a = place(r, wr, i + 2)
    H.append(f'<div class="q"><span class="qn">{NQ[0]}.</span> <span class="jp big">{e(w)}</span>{qopts([e(o) for o in opts])}</div>')
    A.append((NQ[0], ABC[a], f'{w}（{r}）– {vi}'))
H.append('</div>')
ANS.append(('A3. Từ hay gặp trong đề', A)); A = []

# B1 – đọc chữ Hán gạch chân
part('B1. Chọn cách đọc đúng của từ gạch chân', '')
H.append('<div class="ql">')
for i, k in enumerate(K):
    NQ[0] += 1
    s = underline(k['ex']['jp'], k['w']) or f'<u>{e(k["w"])}</u>'
    opts, a = place(k['r'], k['rd'][:3], i)
    H.append(f'<div class="q"><span class="qn">{NQ[0]}.</span> <span class="jp">{s}</span>{qopts([e(o) for o in opts])}</div>')
    A.append((NQ[0], ABC[a], f'{k["w"]}（{k["r"]}）– {k["hv"]} – {k["vi"]}'))
H.append('</div>')
ANS.append(('B1. Cách đọc chữ Hán', A)); A = []
# B2 – chọn chữ Hán
part('B2. Chọn chữ Hán đúng cho từ gạch chân', '')
H.append('<div class="ql">')
for i, k in enumerate(K):
    NQ[0] += 1
    s = underline(k['ex']['jp'], k['w'], e(k['r'])) or f'<u>{e(k["r"])}</u>'
    opts, a = place(k['w'], k['wk'][:3], i + 2)
    H.append(f'<div class="q"><span class="qn">{NQ[0]}.</span> <span class="jp">{s}</span>{qopts([e(o) for o in opts], " kj")}</div>')
    A.append((NQ[0], ABC[a], f'{k["r"]} → {k["w"]} ({k["hv"]})'))
H.append('</div>')
ANS.append(('B2. Chọn chữ Hán', A)); A = []

# C1 – trắc nghiệm ngữ pháp (câu 2, 3 của mỗi mẫu; câu 1 đã làm trên lớp)
part('C1. Chọn đáp án đúng điền vào （　）', 'Mỗi mẫu ngữ pháp 2 câu.')
H.append('<div class="ql">')
j = 0
for b in BAIS:
    for p in GL[b]['points']:
        for q in (p.get('quiz') or [])[1:3]:
            NQ[0] += 1; j += 1
            right = q['o'][q['a']]; wrong = [o for t, o in enumerate(q['o']) if t != q['a']]
            opts, a = place(right, wrong, j)
            H.append(f'<div class="q"><span class="qn">{NQ[0]}.</span> <span class="jp">{RB(q["q"])}</span>{qopts([RB(o) for o in opts])}</div>')
            A.append((NQ[0], ABC[a], f'<span class="jp">{RB(right)}</span> — {RB(q.get("ex_vi", ""))}'))
H.append('</div>')
ANS.append(('C1. Trắc nghiệm ngữ pháp', A)); A = []

def ws(b, no, kind):
    p = next(p for p in GL[b]['points'] if p['no'] == no)
    return next(w for w in p['worksheet'] if w['kind'] == kind)
def fillq(q):  # （＿＿） → ô trống
    return re.sub(r'（＿＿）|＿＿', '<span class="bl"></span>', RB(q))
def b_multi(it): return it['q'].count('＿＿') > 1

# ví dụ của worksheet: ghi đáp án mẫu ngay trong ô
BLK = r'（＿＿）|＿＿|（\s*[^（）＿]*／[^（）＿]*\s*）'
def nblank(q): return len(re.findall(BLK, PLAIN(q)))
def wsx(w):
    ex = w.get('example') or {}
    if not ex.get('q'): return ''
    a = ex['a']
    if '\n' in a and 'A：' in a: ans = [l.split('：', 1)[1] for l in a.split('\n')]
    elif nblank(ex['q']) > 1: ans = [x.strip() for x in a.split('／')]
    else: ans = [a]
    s = RB(ex['q']); k = [0]
    def rep(m):
        t = ans[k[0]] if k[0] < len(ans) else ''; k[0] += 1
        return f'<span class="bl f">{RB(t)}</span>'
    s = re.sub(BLK, rep, s)
    return f'<div class="wex"><b>Ví dụ</b> <span class="jp">{s}</span></div>'
def alt(x):
    xs = [t.strip() for t in x.split('／') if t.strip()]
    if len(xs) > 1 and len(PLAIN(xs[0])) <= 6: return RB(xs[0]) + f' <small>(hoặc {RB(xs[1])})</small>'
    return RB(xs[0])
def fmt_ans(it):
    an = it['answer']
    if nblank(it['q']) > 1: return '　'.join(f'<b class="cn">{"①②③④⑤⑥⑦⑧⑨⑩"[i]}</b> {alt(x)}' for i, x in enumerate(an))
    return alt(an[0])
def wsblock(title, w, hint='', pics=False, items=None):
    part(title, e(w['ins_vi']) + (f' <b class="jp">{hint}</b>' if hint else ''))
    H.append(wsx(w))
    out = []
    H.append(f'<div class="ql{" pics" if pics else ""}">')
    for it in (items or w['items']):
        NQ[0] += 1
        pic = f'<img src="{img("app/media/gimg/" + it["img"] + ".jpg")}">' if pics and it.get('img') else ''
        H.append(f'<div class="q wq">{pic}<div><span class="qn">{NQ[0]}.</span> <span class="jp">{fillq(it["q"])}</span></div></div>')
        out.append((NQ[0], f'<span class="jp">{fmt_ans(it)}</span>', ''))
    H.append('</div>')
    return out

ANS.append(('C2. Điền trợ từ に・で', wsblock('C2. Điền trợ từ に hoặc で', ws(12, '❶', '整理'), '（に・で）')))
ANS.append(('C3. Điền trợ từ – ngày giờ, nơi chốn, sự kiện', wsblock('C3. Điền trợ từ: ngày giờ, nơi chốn, sự kiện', ws(12, '❶', '練習'), '（に・で・が・×）')))
w = ws(13, '❺', '練習')
ANS.append(('C4. Lên xe, xuống xe', wsblock('C4. Điền trợ từ: lên xe, xuống xe, chuyển tàu', w, '（で・に・を）', items=w['items'][:4])))
ANS.append(('C5. Rủ rê 〜ませんか', wsblock('C5. Đổi sang câu rủ rê 「〜ませんか？」', ws(12, '❸', '練習'))))
ANS.append(('C6. Rủ đi làm gì 〜に行きませんか', wsblock('C6. Nhìn tranh, rủ bạn đi làm việc đó 「V に行きませんか？」', ws(12, '❺', '練習'), pics=True)))
ANS.append(('C7. Phương tiện 〜で来ます', wsblock('C7. Nhìn tranh, trả lời bằng phương tiện 「〜で来ます／行きます」', ws(13, '❸', '練習'), pics=True)))
ANS.append(('C8. から〜まで', wsblock('C8. Tạo hội thoại 「〜から〜まで」', ws(13, '❻', '練習'))))
H.append('</section>')

# --- 5. Đáp án ---
H.append('<section class="ans">')
sec('05', 'Đáp án', 'こたえ', 'Câu trắc nghiệm có giải thích ngắn. Câu tự viết: đáp án gợi ý, viết cách khác đúng ngữ pháp vẫn được.')
for t, items in ANS:
    H.append(f'<h3 class="ph">{t}</h3><table class="at">')
    for n, a, x in items:
        H.append(f'<tr><td class="an">{n}</td><td class="aa">{a}</td><td>{x}</td></tr>' if x else f'<tr><td class="an">{n}</td><td class="aa" colspan="2">{a}</td></tr>')
    H.append('</table>')
H.append('<div class="end">Chúc các em học tốt! · Anh Trọng Dạy JFT · Facebook: anh.trongg.2024 · TikTok: @anhtrong.daygino</div></section>')

CSS = open(R + 'src/tailieu_src/handout.css').read()
fonts = ''.join(f'<link rel="stylesheet" href="file://{FS}{f}">' for f in ['klee-one/400.css', 'klee-one/600.css', 'quicksand/500.css', 'quicksand/600.css', 'quicksand/700.css'])
os.makedirs('/tmp/b3', exist_ok=True)
open(OUT, 'w').write(f'<!doctype html><html lang="vi"><head><meta charset="utf-8">{fonts}<style>{CSS}</style></head><body>{"".join(H)}</body></html>')
print('ok', OUT, 'câu bài tập:', NQ[0])
