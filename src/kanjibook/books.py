"""Bộ 3 sách いろどり (入門・初級1・初級2): Chữ Hán · Từ vựng · Ngữ pháp → /tmp/kb/out/<book>.html → pdf.js
Chạy: python3 src/kanjibook/books.py [kanji|vocab|grammar ...] rồi (cd /tmp/tk && node src/kanjibook/pdf.js /tmp/kb/out/kanji.html out.pdf)
Trang được chia tự động trong trình duyệt (khối .brk = sang trang mới, đáp án .akb đặt ở cuối bài)."""
import sys, os, re, json, random, collections, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

OUT = '/tmp/kb/out/'
os.makedirs(OUT, exist_ok=True)
LVS = ['入門', '初級1', '初級2']
LVC = {'入門': 'lv0', '初級1': 'lv1', '初級2': 'lv2'}
D, V, G = load('docs'), load('vocab'), load('grammar')
LS = json.load(open(A + 'lessons.json'))
STK = json.load(open(R + 'src/tailieu_src/kanjivg_strokes.json'))
MEDIA = 'file://' + R + 'public/app/media/'

# ---------- tên bài ----------
TITLE = {('入門', 1): ('おはようございます', 'Chào buổi sáng'), ('入門', 2): ('すみません、よくわかりません', 'Xin lỗi, tôi không hiểu lắm')}
for g in G:
    if g['lv'] in LVS: TITLE[(g['lv'], g['bai'])] = (g['title'], g['title_vi'])
for line in open(R + 'src/raw/titles.txt', encoding='utf-8'):
    p = line.rstrip('\n').split('|'); m = re.search(r'(Shokyu1|Shokyu2)_Bai(\d+)', p[0])
    if m: TITLE.setdefault(({'Shokyu1': '初級1', 'Shokyu2': '初級2'}[m.group(1)], int(m.group(2))), (p[1], p[2]))
FURI_T = {}
try:
    sys.path.insert(0, R + 'src/jft'); from furi import furi as _furi
except Exception: _furi = None
def T(lv, b):
    t, vi = TITLE[(lv, b)]
    if '{' not in t and _furi: t = re.sub(r'<ruby>(.*?)<rt>(.*?)</rt></ruby>', r'{\1|\2}', _furi(t))
    return t, vi

def comp(h):
    """HTML ruby → dạng rút gọn {漢字|かな}"""
    return re.sub(r'<ruby[^>]*>(.*?)<rt>(.*?)</rt></ruby>', r'{\1|\2}', h)
def cap0(s): return s[:1].lower() + s[1:] if s and not s[:2].isupper() else s
def units(c):
    """chuỗi rút gọn → [(base, rt|None)]"""
    out = []
    for m in re.finditer(r'\{([^{}|]+)\|([^{}]*)\}|([^{}])', c):
        out.append((m.group(1), m.group(2)) if m.group(1) else (m.group(3), None))
    return out

# ================= CHỮ HÁN =================
CH = {}
for lv, v in D['kanji'].items():
    for w in v:
        for c in w['chars']: CH.setdefault(c['k'], c)
CH.update({
    '仕': {'hv': 'SĨ', 'on': 'シ', 'kun': 'つか.える', 'vi': 'làm việc, phục vụ'},
    '駅': {'hv': 'DỊCH', 'on': 'エキ', 'kun': '—', 'vi': 'nhà ga'},
    '受': {'hv': 'THỤ', 'on': 'ジュ', 'kun': 'う.ける', 'vi': 'nhận'},
    '付': {'hv': 'PHÓ', 'on': 'フ', 'kun': 'つ.ける・つ.く', 'vi': 'gắn, kèm theo'},
    '門': {'hv': 'MÔN', 'on': 'モン', 'kun': 'かど', 'vi': 'cổng'},
    '耳': {'hv': 'NHĨ', 'on': 'ジ', 'kun': 'みみ', 'vi': 'tai'},
    '郵': {'hv': 'BƯU', 'on': 'ユウ', 'kun': '—', 'vi': 'bưu chính'},
    '局': {'hv': 'CỤC', 'on': 'キョク', 'kun': '—', 'vi': 'cục, cơ quan'}})
DW = {}   # từ của tài liệu (có câu ví dụ, cách đọc nhiễu, chữ nhiễu)
for lv, v in D['kanji'].items():
    for w in v: DW.setdefault(plain(w['w']), w)
VW = {}
for w in V['words']: VW.setdefault(re.sub(r'（.*?）', '', w['h']), w)

def kanji_lessons():
    """[{lv,bai,words:[{c,vi,hv}]}] theo thứ tự sách"""
    L = []
    # 入門: danh sách từ chữ Hán của tài liệu theo thứ tự sách, gán bài theo từ vựng (lấy max chạy)
    vi_ = {}
    for w in V['words']:
        for l in w['l']:
            if l[0] == '入門':
                for k in {re.sub('（.*?）', '', w['h']), w['h']}: vi_.setdefault(k, []).append(l[1])
    cur = 2; by = collections.OrderedDict()
    for w in D['kanji']['入門']:
        b = min(vi_[w['w']]) if w['w'] in vi_ else None
        if b and b > cur: cur = b
        by.setdefault(cur, []).append({'c': comp(w['wr']), 'vi': cap0(w['vi']), 'hv': w['hv']})
    for b, ws in by.items(): L.append({'lv': '入門', 'bai': b, 'words': ws})
    for x in LS:
        if x['lv'] in ('初級1', '初級2'):
            L.append({'lv': x['lv'], 'bai': x['bai'], 'words': [{'c': comp(w['w']), 'vi': w['vi'], 'hv': w['hv']} for w in x['words']]})
    seen = set()
    for x in L:
        ks = []
        for w in x['words']:
            for c in plain(w['c']):
                if isk(c) and c not in ks: ks.append(c)
        x['all'] = ks; x['new'] = [c for c in ks if c not in seen]; seen |= set(ks)
    return L

def stroke_svg(k, upto=None, cls='sf'):
    p = [re.sub(r'\d+\.\d+', lambda m: str(round(float(m.group(0)))), d) for d in STK[k]['p']]; n = len(p) if upto is None else upto
    o = ''.join(f'<path d="{d}" class="{"cur" if i == n - 1 and upto else "old"}"/>' for i, d in enumerate(p[:n]))
    return f'<svg class="{cls}" viewBox="0 0 109 109"><line x1="54.5" y1="0" x2="54.5" y2="109"/><line x1="0" y1="54.5" x2="109" y2="54.5"/>{o}</svg>'

def lesson_sents(lv, b):
    """câu song ngữ trong web bài học (初級1/2) dạng rút gọn"""
    d = {'初級1': 's1', '初級2': 's2'}.get(lv)
    if not d: return []
    f = R + f'public/lessons/{d}/Irodori_{"Shokyu1" if lv == "初級1" else "Shokyu2"}_Bai{b:02d}.html'
    if not os.path.exists(f): return []
    s = re.sub(r'data:[^"]+', '', open(f, encoding='utf-8').read())
    o, seen = [], set()
    for m in re.finditer(r'<p class="jp">(.*?)</p>\s*<p class="vi">(.*?)</p>', s, re.S):
        jp = comp(m.group(1)); jp = re.sub(r'<[^>]+>', '', jp).strip()
        jp = re.sub(r'^[①-⑳]\s*', '', jp); vi = plain(m.group(2)).strip()
        pj = plain(jp)
        if '\n' in jp or not (4 <= len(pj) <= 46) or pj in seen or re.search(r'[a-zA-Z（(【]', pj) or 'Ａ：' in jp: continue
        if not re.search(r'[。？！]$', pj) or re.search(r'ましょう。$|ことができる。$|[＿_]|ください。$', pj): continue
        seen.add(pj); o.append((jp, vi))
    return o

def mark(c, ks, mode='u'):
    """gạch chân các ruby mà mọi chữ đều thuộc ks (mode u: bỏ furigana)"""
    def f(m):
        base, rt = m.group(1), m.group(2)
        if all(ch in ks or not isk(ch) for ch in base) and any(isk(ch) for ch in base): return f'[[{base}]]'
        return m.group(0)
    return re.sub(r'\{([^{}|]+)\|([^{}]*)\}', f, c)

def word_in(sent, word):
    """tìm từ (phần chữ Hán đầu) trong câu rút gọn: trả về (trước, base, rt, sau) hoặc None"""
    stem = re.match(r'[一-鿿々]+', plain(word))
    if not stem: return None
    stem = stem.group(0)
    for m in re.finditer(r'\{([^{}|]+)\|([^{}]*)\}', sent):
        if m.group(1) == stem: return sent[:m.start()], stem, m.group(2), sent[m.end():]
    return None

def kanji_book():
    L = kanji_lessons()
    random.seed(7)
    flows = []; toc = []
    known = []   # từ đã học (để làm câu đố)
    for x in L:
        lv, b = x['lv'], x['bai']; t, tvi = T(lv, b)
        if not x['new']: continue
        lab = f'いろどり {lv} · Bài {b}'; fid = f'k{LVS.index(lv)}{b:02d}'
        toc.append((lv, b, t, tvi, fid))
        blocks = []
        band = ''.join(f'<div class="bk"><b class="jp">{k}</b><small>{CH[k]["hv"]}</small></div>' for k in x['new'])
        # tranh từ tài liệu (từ có chữ Hán của bài)
        pics = [v for v in D['vocab'].get(lv, []) if v.get('b') == b and v.get('img')]
        pics.sort(key=lambda v: -sum(c in x['new'] for c in v['w']))
        tiles = ''.join(f'<figure><img src="{MEDIA}doc/{v["img"]}"><figcaption><p class="jp">{J(mark(comp(v["wr"]), x["new"], "k"))}</p><p class="vi">{e(cap0(v["vi"]))}</p></figcaption></figure>' for v in pics[:6]) if len(pics) >= 3 else ''
        wl = ''.join(f'<div class="kwi"><span class="jp w">{J(w["c"])}</span><span class="m"><small>{e(w["hv"])}</small>{e(w["vi"])}</span></div>' for w in x['words'])
        blocks.append(f'<div class="brk" id="{fid}">{head(lv, b, t, tvi, "")}<div class="band">{band}</div></div>')
        if tiles: blocks.append(f'<div class="tiles">{tiles}</div>')
        blocks.append(f'<div class="kw"><div class="kwh"><span class="jp">漢字のことば</span></div><div class="kwg">{wl}</div></div>')
        # thẻ chữ
        first = True
        for k in x['new']:
            c = CH[k]; n = len(STK[k]['p'])
            ws = [w for w in x['words'] if k in plain(w['c'])][:3]
            if len(ws) < 3:
                ws += [w for w in known if k in plain(w['c']) and w not in ws][:3 - len(ws)]
            wh = ''.join(f'<span class="wc"><b class="jp">{J(w["c"])}</b>{e(w["vi"])}</span>' for w in ws)
            on = '・'.join(y for y in c['on'].split('・') if y and y != '—') or '—'
            kun = '・'.join(y.replace('.', '<i>-</i>') for y in c['kun'].split('・') if y and y != '—') or '—'
            seq = ''.join(stroke_svg(k, i + 1) for i in range(n))
            trace = ''.join(f'<span class="bx tr"><b class="jp">{k}</b></span>' for _ in range(3)) + '<span class="bx"></span>' * 8
            if first: blocks.append('<div class="kwn"><div class="sh"><span class="no">Ⅰ</span><span class="jp">読み方・書き方</span><span class="vi">Đọc và viết</span></div></div>')
            blocks.append(f'''<div class="kcw"><div class="kc"><div class="kl"><div class="big">{stroke_svg(k, cls="bigs")}</div><div class="hv">{c["hv"]}</div><div class="ns">{n} nét</div></div>
<div class="kr"><div class="r1"><span class="mean">{e(c["vi"])}</span><span class="rd"><i>音</i><b class="jp">{on}</b></span><span class="rd"><i>訓</i><b class="jp">{kun}</b></span></div>
<div class="r2">{wh}</div><div class="r3"{f' style="--s:{135 / n - .9:.1f}mm"' if n > 14 else ''}>{seq}</div><div class="r4">{trace}</div></div></div></div>''')
            first = False
        # 使い方
        sents = [(j, v) for j, v in lesson_sents(lv, b) if any(k in plain(j) for k in x['new'])]
        if len(sents) < 4:
            for w in x['words']:
                dw = DW.get(plain(w['c']))
                if dw and dw.get('ex'): sents.append((comp(dw['ex']['jp']), dw['ex']['vi']))
        sents = sents[:9]
        if sents:
            use = [(f'<li><p class="jp">{J(mark(j, x["new"]))}</p><p class="vi">{e(v)}</p></li>') for j, v in sents]
            blocks.append('<div class="kwn"><div class="sh"><span class="no">Ⅱ</span><span class="jp">使い方</span><span class="vi">Dùng trong câu</span></div></div>'); blocks += [f'<ol class="use" style="counter-reset:u {i}">' + ''.join(use[i:i + 3]) + '</ol>' for i in range(0, len(use), 3)]
        # 練習
        ws = [w for w in x['words'] if plain(w['c']) in DW]
        q1, q2, a1, a2 = [], [], [], []
        for i, w in enumerate(ws):
            dw = DW[plain(w['c'])]; s = comp(dw['ex']['jp']) if dw.get('ex') else ''
            r = word_in(s, w['c'])
            if not r: continue
            pre, base, rt, post = r
            if len(q1) <= len(q2) and len(q1) < 6: q1.append(f'<li class="jp">{J(pre + "[[" + base + "]]" + post)}<span class="ans">（　　　　　　　）</span></li>'); a1.append(rt)
            elif len(q2) < 6: q2.append(f'<li class="jp">{J(pre + "[[" + rt + "]]" + post)}<span class="ans">［　　　　　　］</span></li>'); a2.append(base)
        q3, a3, q4, a4 = [], [], [], []
        for w in ws[:12]:
            dw = DW[plain(w['c'])]
            if dw.get('wk') and len(q3) < 6 and len(q3) <= len(q4):
                ch = [dw['w']] + dw['wk'][:2]; random.shuffle(ch)
                q3.append(f'<li><span class="jp qk">{dw["r"]}</span>' + ''.join(f'<span class="op jp">{"abc"[i]}. {o}</span>' for i, o in enumerate(ch)) + '</li>'); a3.append('abc'[ch.index(dw['w'])])
            elif dw.get('rd') and len(q4) < 6:
                ch = [dw['r']] + dw['rd'][:2]; random.shuffle(ch)
                q4.append(f'<li><span class="jp qk">{dw["w"]}</span>' + ''.join(f'<span class="op jp">{"abc"[i]}. {o}</span>' for i, o in enumerate(ch)) + '</li>'); a4.append('abc'[ch.index(dw['r'])])
        qs, ans, n = [], [], 0
        def addq(title, body, a):
            nonlocal n
            n += 1; qs.append(f'<div class="q"><h4><b>{n}</b>{title}</h4>{body}</div>'); ans.append(f'<p><b>{n}</b> ' + '　'.join(f'{i + 1}. <span class="jp">{y}</span>' for i, y in enumerate(a)) + '</p>')
        if q1: addq('Viết cách đọc của từ gạch chân.', f'<ol class="ql">{"".join(q1)}</ol>', a1)
        if q2: addq('Viết chữ Hán cho phần gạch chân.', f'<ol class="ql">{"".join(q2)}</ol>', a2)
        if q3: addq('Chọn cách viết đúng.', f'<ol class="qo">{"".join(q3)}</ol>', a3)
        if q4: addq('Chọn cách đọc đúng.', f'<ol class="qo">{"".join(q4)}</ol>', a4)
        # câu đố: chữ chung của 2 từ
        pool_words = [w for w in known + x['words'] if re.fullmatch(r'\{[一-鿿々]{2,3}\|[^{}]+\}', w['c'])]
        pz, apz = [], []
        for k in x['new']:
            cand = [w for w in pool_words if k in plain(w['c'])]
            uniq = []
            for w in cand:
                if plain(w['c']) not in [plain(u['c']) for u in uniq]: uniq.append(w)
            if len(uniq) >= 2 and len(pz) < 6:
                a_, b_ = uniq[-1], uniq[-2] if len(uniq) > 1 else uniq[0]
                def hole(w):
                    base, rt = re.fullmatch(r'\{(.+)\|(.+)\}', w['c']).groups(); return base.replace(k, '□'), rt
                (h1, r1), (h2, r2) = hole(a_), hole(b_)
                pz.append(f'<div class="pz"><span class="jp">{h1}</span><span class="eq">・</span><span class="jp">{h2}</span><span class="eq">→</span><span class="box"></span><small>{r1}・{r2}</small></div>'); apz.append(k)
        if len(pz) >= 3: addq('Chữ Hán nào điền được vào cả hai ô □?', f'<div class="pzs">{"".join(pz)}</div>', apz)
        if qs:
            blocks.append('<div class="kwn"><div class="sh"><span class="no">Ⅲ</span><span class="jp">練習</span><span class="vi">Luyện tập</span></div></div>')
            blocks += qs
            blocks.append(f'<div class="akb"><div class="akh"><span class="jp">こたえ</span>Đáp án</div>{"".join(ans)}</div>')
        flows.append(f'<div class="flow" data-lab="{lab}" data-lv="{LVC[lv]}">{"".join(blocks)}</div>')
        known += x['words']
    total = sum(len(x['new']) for x in L)
    return flows, toc, total

# ================= TỪ VỰNG =================
def rb(h, y):
    h = re.sub(r'（.*?）', '', h).strip(); y = re.sub(r'（.*?）', '', y).strip()
    if not any(isk(c) for c in h): return h
    parts = re.findall(r'[一-鿿々]+|[^一-鿿々]+', h)
    pat = ''.join('(.+?)' if isk(p[0]) else re.escape(p) for p in parts)
    try: m = re.fullmatch(pat, y)
    except re.error: m = None
    if not m: return '{' + h + '|' + y + '}'
    o, i = '', 0
    for p in parts:
        if isk(p[0]): i += 1; o += '{' + p + '|' + m.group(i) + '}'
        else: o += p
    return o
POS = [('N', '{名詞|めいし}', 'Danh từ'), ('V', '{動詞|どうし}', 'Động từ'), ('A', '{形容詞|けいようし}', 'Tính từ'), ('X', 'その{他|た}', 'Khác')]
def posk(p):
    p = p or ''
    if p.startswith('N'): return 'N'
    if p.startswith('V'): return 'V'
    if 'A' in p: return 'A'
    return 'X'
def vocab_book():
    random.seed(11)
    by = collections.defaultdict(list)
    for w in V['words']:
        for l in w['l']:
            if l[0] in LVS: by[(l[0], l[1])].append((l[2], w))
    flows, toc = [], []
    for lv in LVS:
        for b in range(1, 19):
            ws = [w for _, w in sorted(by.get((lv, b), []), key=lambda t: t[0])]
            if not ws: continue
            t, tvi = T(lv, b); lab = f'いろどり {lv} · Bài {b}'; fid = f'v{LVS.index(lv)}{b:02d}'
            toc.append((lv, b, t, tvi, fid)); blocks = []
            blocks.append(f'<div class="brk" id="{fid}">{head(lv, b, t, tvi, "")}</div>')
            pics = [v for v in D['vocab'].get(lv, []) if v.get('b') == b and v.get('img')]
            for i in range(0, min(len(pics), 12), 3):
                blocks.append('<div class="jobs">' + ''.join(f'<figure><img src="{MEDIA}doc/{v["img"]}"><figcaption><span class="jp">{J(comp(v["wr"]))}</span><small>{e(cap0(v["vi"]))}</small></figcaption></figure>' for v in pics[i:i + 3]) + '</div>')
            # gom số đếm: N + hậu tố giống nhau (≥4 từ)
            cnt = collections.defaultdict(list)
            for w in ws:
                m = re.fullmatch(r'(\d+)(.*)', re.sub(r'（.*?）', '', w['h']))
                if m: cnt[m.group(2)].append((int(m.group(1)), w))
            grids = {k: sorted(v, key=lambda t: t[0]) for k, v in cnt.items() if len(v) >= 4}
            gw = {id(w) for v in grids.values() for _, w in v}
            for pk, pj, pv in POS:
                items = [w for w in ws if posk(w.get('p')) == pk and id(w) not in gw and not w['h'].startswith('～')]
                if not items: continue
                rows = [items[i:i + 3] for i in range(0, len(items), 3)]
                for ri, row in enumerate(rows):
                    hd = f'<div class="vsh"><span class="jp">{J(pj)}</span><i>{pv}</i></div>' if ri == 0 else ''
                    blocks.append(f'<div class="vrow">{hd}<div class="vg">' + ''.join(f'<div class="vw"><div class="t"><b class="jp">{J(rb(w["h"], w["y"]) + ("（な）" if "（な）" in w["h"] else ""))}</b><span>{e(w["v"])}</span></div></div>' for w in row) + '</div></div>')
            for suf, v in grids.items():
                cells = ''.join(f'<div class="cn"><b>{n}</b><span class="jp">{re.sub(r"（.*?）", "", w["y"])}</span></div>' for n, w in v)
                blocks.append(f'<div class="cnt"><div class="cnh"><span class="jp">{"〜" + suf if suf else "すうじ"}</span></div><div class="cng">{cells}</div></div>')
            # luyện tập
            qs, ans, n = [], [], 0
            def addq(title, body, a):
                nonlocal n
                n += 1; qs.append(f'<div class="q"><h4><b>{n}</b>{title}</h4>{body}</div>'); ans.append(f'<p><b>{n}</b> ' + '　'.join(f'{i + 1}. <span class="jp">{y}</span>' for i, y in enumerate(a)) + '</p>')
            P = pics[:]; random.shuffle(P); P = P[:4]
            if len(P) >= 3:
                addq('Nhìn tranh, viết từ.', '<div class="pqs">' + ''.join(f'<div class="pq"><img src="{MEDIA}doc/{v["img"]}"><span class="no">{i + 1}</span><span class="ln"></span></div>' for i, v in enumerate(P)) + '</div>', [v['r'] for v in P])
            fill = []
            for w in ws:
                if w.get('x') is None or not w.get('k') and not any(isk(c) for c in w['h']): continue
                hh = re.sub(r'（.*?）', '', w['h']); s = V['ex'][w['x']][0]
                comp_w = rb(hh, re.sub(r'（.*?）', '', w['y']))
                if comp_w in s and s.count(comp_w) == 1 and hh not in [f[1] for f in fill] and len(plain(s)) < 40:
                    fill.append((s.replace(comp_w, '((　　　　))'), hh, comp_w))
                if len(fill) == 5: break
            if len(fill) >= 3:
                bank = [f[2] for f in fill]; random.shuffle(bank)
                addq('Chọn từ điền vào ô.', '<div class="pool w">' + ''.join(f'<span class="jp">{J(x)}</span>' for x in bank) + '</div><ol class="ql one">' + ''.join(f'<li class="jp">{J(s)}</li>' for s, _, _ in fill) + '</ol>', [f[1] for f in fill])
            rd = [v for v in D['vocab'].get(lv, []) if v.get('b') == b and v.get('rd') and len(v['r']) <= 7 and max(len(y) for y in v['rd'][:2]) <= 8]
            random.shuffle(rd); rd = rd[:6]
            if len(rd) >= 3:
                q, a = [], []
                for v in rd:
                    ch = [v['r']] + v['rd'][:2]; random.shuffle(ch)
                    q.append(f'<li><span class="jp qk">{plain(v["wr"])}</span>' + ''.join(f'<span class="op jp">{"abc"[i]}. {o}</span>' for i, o in enumerate(ch)) + '</li>'); a.append('abc'[ch.index(v['r'])])
                addq('Chọn cách đọc đúng.', f'<ol class="qo">{"".join(q)}</ol>', a)
            if qs:
                blocks.append('<div class="kwn"><div class="sh"><span class="no">✎</span><span class="jp">練習</span><span class="vi">Luyện tập</span></div></div>')
                blocks += qs + [f'<div class="akb"><div class="akh"><span class="jp">こたえ</span>Đáp án</div>{"".join(ans)}</div>']
            flows.append(f'<div class="flow" data-lab="{lab}" data-lv="{LVC[lv]}">{"".join(blocks)}</div>')
    return flows, toc, len({w['h'] for w in V['words']})

# ================= NGỮ PHÁP =================
GIMG = R + 'public/app/media/gimg/'
def formula(p):
    toks = re.split(r'(【[^】]+】|V[-‐]?[^\s、・＋+]*|N\d?|イA[^\s、]*|ナA[^\s、]*|Aい|Aな)', p)
    out = []
    for t in toks:
        t = t.strip()
        if not t: continue
        if re.fullmatch(r'【[^】]+】|V[-‐]?[^\s、・＋+]*|N\d?|イA[^\s、]*|ナA[^\s、]*|Aい|Aな', t): out.append(f'<span class="fx v">{J(t.strip("【】"))}</span>')
        else: out.append(f'<span class="fx">{J(t)}</span>')
    return '<div class="fm">' + '<em>+</em>'.join(out) + '</div>' if len(out) > 1 else ''
def noen(t):
    t = re.sub(r'[ァ-ヶー]+-form\s*', '', t)
    t = re.sub(r'(?<![A-Za-z])(?:[a-z][a-z\-]*|[A-Z][a-z][a-z\-]*)(?:\s+(?:of\s+)?[a-z][a-z\-]*)*\s*', '', t)
    t = re.sub(r'(^|(?<=[＜<【（(]))\s*/\s*', '', t)
    return re.sub(r'\s+(?=[】>＞)）])', '', t).strip()
def grammar_book():
    flows, toc, total = [], [], 0
    for g in G:
        if g['lv'] not in LVS: continue
        lv, b = g['lv'], g['bai']; t, tvi = T(lv, b); lab = f'いろどり {lv} · Bài {b}'; fid = f'g{LVS.index(lv)}{b:02d}'
        toc.append((lv, b, t, tvi, fid)); blocks = [f'<div class="brk" id="{fid}">{head(lv, b, t, tvi, "")}</div>']
        qs, ans = [], []
        for p in g['points']:
            total += 1
            imgs = []
            for wsx in p.get('worksheet') or []:
                for im in wsx.get('images') or []:
                    f = GIMG + im + '.jpg'
                    if os.path.exists(f): imgs.append(f)
            img = f'<img class="gim" src="file://{imgs[0]}">' if imgs else ''
            exs = (p.get('examples') or []) + (p.get('more_examples') or [])
            exs = [x for x in exs if len(plain(x['jp'])) < 60][:2] or exs[:1]
            eh = ''.join(f'<div class="gx"><p class="jp">{J(re.sub(r"^[①-⑩]\s*", "", x["jp"]))}</p><p class="vi">{e(re.sub(r"^[①-⑩]\s*", "", x["vi"]))}</p></div>' for x in exs)
            blocks.append(f'<div class="gc{" wi" if img else ""}"><div class="gch"><b>{p["no"]}</b><span class="jp pat">{J(noen(p["pattern"]))}</span><i>{e(p["meaning_vi"])}</i></div><div class="gb"><div class="gt">{formula(noen(p["pattern"]))}{eh}</div>{img}</div></div>')
            for q in (p.get('quiz') or [])[:2]:
                qs.append(f'<li><p class="jp">{J(q["q"])}</p><div class="ops">' + ''.join(f'<span class="jp">{"abcd"[k]}. {J(o)}</span>' for k, o in enumerate(q['o'])) + '</div></li>'); ans.append("abcd"[q["a"]])
        if qs:
            blocks.append('<div class="kwn"><div class="sh"><span class="no">✎</span><span class="jp">練習</span><span class="vi">Luyện tập</span></div></div>')
            for i in range(0, len(qs), 2):
                blocks.append(f'<ol class="gq" start="{i + 1}" style="counter-reset:g {i}">{"".join(qs[i:i + 2])}</ol>')
            blocks.append(f'<div class="akb"><div class="akh"><span class="jp">こたえ</span>Đáp án</div><p>' + '　'.join(f'{i + 1}. {a}' for i, a in enumerate(ans)) + '</p></div>')
        flows.append(f'<div class="flow" data-lab="{lab}" data-lv="{LVC[lv]}">{"".join(blocks)}</div>')
    return flows, toc, total

# ================= ghép sách =================
def divider(lv, n, unit):
    return f'''<section class="pg divp {LVC[lv]} nofoot"><div class="dvb"><img src="{COV[lv]}"><div><b class="jp">{lv}</b><span>{n} {unit}</span></div></div></section>'''
def toc_page(toc):
    rows = ''
    for lv in LVS:
        items = [x for x in toc if x[0] == lv]
        if not items: continue
        rows += f'<div class="tcl {LVC[lv]}"><div class="tch jp">{lv}</div>' + ''.join(
            f'<div class="tci"><b>{b}</b><span class="jp">{J(t)}</span><i data-p="{fid}"></i></div>' for lv_, b, t, tvi, fid in items) + '</div>'
    return f'<section class="pg tocp nofoot"><div class="toch jp">もくじ</div><div class="tcg">{rows}</div></section>'

PAGINATE = r'''<script>
(async()=>{await document.fonts.ready;
const mm=document.createElement('div');mm.style.height='100mm';document.body.appendChild(mm);const MM=mm.getBoundingClientRect().height/100;mm.remove();
const LIM=(297-13-20)*MM;
for(const flow of [...document.querySelectorAll('.flow')]){
  const lab=flow.dataset.lab,lv=flow.dataset.lv;let pg=null,inner=null;
  const np=()=>{pg=document.createElement('section');pg.className='pg unit '+lv;pg.dataset.lab=lab;inner=document.createElement('div');inner.className='inner';pg.appendChild(inner);flow.before(pg)};
  const bottom=()=>{const l=inner.lastElementChild;if(!l)return 0;return l.getBoundingClientRect().bottom-inner.getBoundingClientRect().top};
  let akb=null;
  for(const b of [...flow.children]){
    if(b.classList.contains('akb')){akb=b;continue}
    if(!pg||b.classList.contains('brk'))np();
    inner.appendChild(b);
    if(bottom()>LIM&&inner.children.length>1){const prev=b.previousElementSibling;np();
      if(prev&&prev.classList.contains('kwn')){inner.appendChild(prev)}
      inner.appendChild(b)}
  }
  if(akb){pg.appendChild(akb);const h=akb.getBoundingClientRect().height;if(bottom()>LIM-h-6*MM){np();pg.appendChild(akb)}}
  flow.remove();
}
const pages=[...document.querySelectorAll('section.pg')];
pages.forEach((p,i)=>{p.dataset.n=i+1;if(p.classList.contains('nofoot')||p.classList.contains('cover'))return;
  const f=document.createElement('div');f.className='ft';f.innerHTML=`<span class="fl">${p.dataset.lab||''}</span><span class="pn">${i+1}</span><span class="fb">Anh Trọng Dạy JFT</span>`;p.appendChild(f)});
document.querySelectorAll('[data-p]').forEach(el=>{const t=document.getElementById(el.dataset.p);const p=t&&t.closest('section.pg');el.textContent=p?p.dataset.n:''});
const over=[];pages.forEach(p=>{const r=p.getBoundingClientRect();p.querySelectorAll('.inner>*,.akb').forEach(c=>{if(c.getBoundingClientRect().bottom>r.bottom-14*MM)over.push(p.dataset.n)})});
window.__over=[...new Set(over)];document.body.dataset.ok=1})();
</script>'''

FULL_CSS = '''
.sf line,.bigs line{stroke:#e6ebf0;stroke-dasharray:none}
.bx::before,.bx::after{background:#e8edf1!important}
.use li,.akb{border-bottom-style:solid}
.inner{position:relative}
.lv0{--lv:#d9567f;--lvl:#fdeef3}.lv1{--lv:#e8912a;--lvl:#fdf1e0}.lv2{--lv:#c99a06;--lvl:#fdf8de}
.unit .uh{margin-bottom:0}.brk .band{margin-bottom:3mm}
.tiles{margin-bottom:3mm}.tiles img{height:30mm;object-fit:contain;background:#fff}
.kw{margin:0 0 3mm}.kcw{margin-bottom:2.6mm}.kcw .sh{margin-bottom:3mm}
.r3 .sf{width:var(--s,8.4mm);height:var(--s,8.4mm)}
.use{margin-bottom:3mm}
.q{margin-bottom:4mm}
.akb{position:absolute;left:14mm;right:14mm;bottom:16mm}
.vrow{margin-bottom:1.6mm}.vsh{margin:2mm 0 2mm}
.vsh{display:flex;align-items:center;gap:3mm}.vsh::after{content:'';flex:1;height:.3mm;background:var(--line)}
.vsh .jp{font-size:16px;color:var(--navy)}.vsh i{font-style:normal;font-weight:700;font-size:12.5px;color:var(--lv)}
.vg{display:grid;grid-template-columns:repeat(3,1fr);gap:1.6mm}
.vw{display:flex;align-items:center;border:.3mm solid var(--line);border-radius:2mm;padding:.8mm 2.4mm;min-height:12.5mm;background:#fff}
.vw .t{display:flex;flex-direction:column;line-height:1.2}.vw .t b{font-size:15.5px;line-height:1.7}.vw .t span{font-size:10.5px;color:#55657a}
.jobs{display:grid;grid-template-columns:repeat(3,1fr);gap:2.4mm;margin:3mm 0 0}
.jobs figure{border:.3mm solid var(--line);border-radius:2.2mm;overflow:hidden;background:#fff}
.jobs img{width:100%;height:28mm;object-fit:contain;display:block;background:#fff}
.jobs figcaption{text-align:center;padding:.4mm 1mm 1.2mm;line-height:1.3}.jobs figcaption .jp{font-size:13.5px;line-height:1.75;display:block}.jobs small{font-size:9.5px;color:var(--mut)}
.cnt{border:.4mm solid var(--line);border-radius:2.4mm;padding:2mm 3mm;background:#fbfcfd;margin:2mm 0}
.cnh .jp{font-size:15px;color:var(--navy)}
.cng{display:grid;grid-template-columns:repeat(4,1fr);gap:1.2mm;margin-top:1mm}
.cn{display:flex;align-items:baseline;gap:1.4mm;border:.3mm solid var(--line);border-radius:1.4mm;padding:.4mm 2mm;background:#fff}.cn b{font-size:14px;color:var(--navy)}.cn .jp{font-size:12px}
.pqs{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-left:9mm}
.pq{position:relative;border:.3mm solid var(--line);border-radius:2mm;overflow:hidden;padding-bottom:9mm}
.pq img{width:100%;height:27mm;object-fit:contain;background:#fff}
.pq .no{position:absolute;top:1mm;left:1mm;background:var(--navy);color:#fff;border-radius:1mm;font-size:10px;font-weight:700;padding:0 1.6mm}
.pq .ln{position:absolute;left:3mm;right:3mm;bottom:3mm;border-bottom:.35mm solid #9fb0bf}
.pool.w span{display:inline-flex;align-items:center;width:auto!important;height:auto!important;padding:.6mm 3mm;font-size:15px;white-space:nowrap;line-height:1.7}
.ql.one{grid-template-columns:1fr}
.blank{display:inline-block;min-width:22mm;border-bottom:.4mm solid #9fb0bf;color:transparent}
.gc{border:.4mm solid var(--line);border-radius:3mm;padding:2.6mm 4mm 3mm;margin-bottom:3.4mm;background:#fff}
.gch{display:flex;align-items:center;gap:3mm;margin-bottom:2mm;flex-wrap:wrap}
.gch b{min-width:8mm;height:8mm;border-radius:4mm;background:var(--navy);color:#fff;display:grid;place-items:center;font-size:13px;padding:0 1.4mm}
.gch .pat{font-size:19px;color:var(--navy);line-height:1.6}.gch i{font-style:normal;font-weight:700;font-size:12.5px;color:var(--lv);margin-left:auto}
.gb{display:flex;gap:4mm}.gt{flex:1;min-width:0}
.gim{width:38mm;height:32mm;object-fit:contain;border-radius:2mm;border:.3mm solid var(--line);background:#fff;flex:0 0 38mm}
.fm{display:flex;align-items:center;gap:1.6mm;margin:0 0 2mm;flex-wrap:wrap}
.fm em{font-style:normal;font-weight:700;color:var(--pink);font-size:16px}
.fx{font-family:'Klee One',serif;font-weight:600;font-size:16px;border:.4mm solid var(--navy);border-radius:1.8mm;padding:0 3mm;line-height:1.75;color:var(--navy)}
.fx.v{background:var(--navy);color:#fff}.fx.v rt{color:#cfe0ee}
.gx{border-left:.8mm solid var(--line);padding:.2mm 0 .2mm 3mm;margin-top:1.4mm}
.gx .jp{font-size:15px;line-height:1.9}.gx .vi{font-size:10.5px;color:var(--mut)}
.gq{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:2.4mm 6mm;margin-bottom:2.4mm}
.gq li{counter-increment:g;position:relative;padding-left:8mm;border-bottom:.3mm dashed var(--line);padding-bottom:1.4mm}
.gq li::before{content:counter(g);position:absolute;left:0;top:1.6mm;width:5.6mm;height:5.6mm;border-radius:50%;background:var(--lvl);color:var(--lv);font-size:10px;font-weight:700;display:grid;place-items:center}
.gq .jp{font-size:13.5px;line-height:1.95}
.ops{display:flex;gap:1.6mm;flex-wrap:wrap}.ops span{font-size:12.5px;border:.3mm solid var(--line);border-radius:1.4mm;padding:0 2mm;line-height:1.9}
/* trang ngăn cấp độ + mục lục */
.divp{display:flex;align-items:center;justify-content:center}
.divp.lv0{background:#f6c3d4}.divp.lv1{background:#f3b357}.divp.lv2{background:#f6d94a}
.dvb{display:flex;flex-direction:column;align-items:center;gap:8mm}
.dvb img{width:92mm;border-radius:2mm;box-shadow:0 3mm 8mm rgba(0,0,0,.22)}
.dvb div{text-align:center;color:var(--navy)}.dvb b{display:block;font-size:54px}.dvb span{font-weight:700;font-size:16px;letter-spacing:.1em}
.tocp{padding:14mm 14mm}
.toch{font-size:30px;color:var(--navy);border-bottom:.6mm solid var(--navy);padding-bottom:2mm;margin-bottom:4mm}
.tcg{columns:2;column-gap:8mm}
.tcl{break-inside:avoid;margin-bottom:4mm}
.tch{font-size:15px;color:#fff;background:var(--lv);border-radius:1.4mm;padding:.4mm 3mm;display:inline-block;margin-bottom:1mm}
.tci{display:flex;align-items:baseline;gap:2mm;font-size:11.5px;border-bottom:.25mm dotted #c9d3dc;padding:.3mm 0}
.tci b{color:var(--lv);min-width:5mm;font-size:11px}.tci .jp{flex:1;font-size:11.5px;line-height:1.7;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.tci i{font-style:normal;font-weight:700;color:var(--navy);font-size:11px}
.tci rt{display:none}
'''

def build(kind):
    if kind == 'kanji': flows, toc, total = kanji_book(); cv = cover('漢字', 'CHỮ HÁN', total, '字', '')
    elif kind == 'vocab': flows, toc, total = vocab_book(); cv = cover('言葉', 'TỪ VỰNG', total, '語', 'vc')
    else: flows, toc, total = grammar_book(); cv = cover('文法', 'NGỮ PHÁP', total, '文型', 'gcv')
    unit = {'kanji': 'bài', 'vocab': 'bài', 'grammar': 'bài'}[kind]
    body = cv + toc_page(toc)
    for lv in LVS:
        fl = [f for f in flows if f'data-lv="{LVC[lv]}"' in f]
        if fl: body += divider(lv, len(fl), unit) + ''.join(fl)
    extra = FULL_CSS
    if kind == 'vocab': extra += '.cover.vc .tblock h1 em{background:linear-gradient(transparent 62%,rgba(243,169,195,.8) 62%,rgba(243,169,195,.8) 90%,transparent 90%)}'
    if kind == 'grammar': extra += '.cover.gcv .tblock h1 em{background:linear-gradient(transparent 62%,rgba(120,180,230,.6) 62%,rgba(120,180,230,.6) 90%,transparent 90%)}'
    write(OUT + f'{kind}.html', body + PAGINATE, extra)
    print(kind, len(flows), 'bài', total)

if __name__ == '__main__':
    for k in (sys.argv[1:] or ['kanji', 'vocab', 'grammar']): build(k)
