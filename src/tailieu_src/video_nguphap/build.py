"""Dựng slide 9:16 cho video "Toàn bộ ngữ pháp JFT" → /tmp/ngp/slides.html (mỗi slide 1 <section>).
Chạy: python3 build.py  → node render.js (chụp PNG + dựng chuyển trang) → python3 video.py (ghép video + tiếng lật trang)."""
import json, re, html, sys, os
R = '/home/claude/anhtrong-jft-app/'
sys.path.insert(0, R + 'src/jft')
from furi import furi
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content.py')).read())
s = open(R + 'public/app/data/grammar.js', encoding='utf-8').read()
GR = json.JSONDecoder().raw_decode(s[s.index('=') + 1:])[0]
IDX = {(x['lv'], x['bai'], p['no']): p for x in GR for p in x['points']}
PL = lambda t: re.sub(r'\{([^|]+)\|[^}]+\}', r'\1', t)
e = html.escape
def RB(t): return re.sub(r'\{([^|{}]+)\|([^{}]+)\}', r'<ruby>\1<rt>\2</rt></ruby>', e(t))
def JP(t): return RB(t) if '{' in t else furi(e(t))

JPRUN = re.compile(r'[\u3040-\u30ff\u3400-\u9fff\uff5e〜ー々→・／（）]+')
def MIX(t):
    # chữ Việt giữ font Mali, đoạn tiếng Nhật đổi sang Klee One + furigana
    o, k = '', 0
    for m in JPRUN.finditer(t):
        if not re.search(r'[\u3040-\u30ff\u3400-\u9fff]', m.group()): continue
        o += e(t[k:m.start()]) + f'<span class="jp">{JP(m.group())}</span>'; k = m.end()
    return o + e(t[k:])
VN = re.compile(r'[a-zà-ỹđ]{2,}')

def ex_of(key):
    lv, b, no, sub = key
    p = IDX[(lv, b, no)]
    for x in (p.get('examples') or []) + (p.get('more_examples') or []):
        for line in x['jp'].split('\n'):
            if sub in PL(line):
                line = re.sub(r'^\s*[①-⑩]?\s*[ＡＢＣABC][：:]\s*', '', line).strip()
                line = re.sub(r'^\s*[①-⑩]\s*', '', line)
                # câu hội thoại nhiều người trên 1 dòng (A：…　B：…) → lấy đoạn có chữ cần tìm
                parts = re.split(r'\s+[ＡＢＣABC][：:]', line)
                for part in parts:
                    if sub in PL(part): return part.strip()
                return line
    raise SystemExit(f'không tìm thấy câu ví dụ {key}')

IMG = 'file://' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ira') + '/'
FS = '/tmp/fs/node_modules/@fontsource/'
FONTS = ''.join(f'<link rel="stylesheet" href="file://{FS}{f}">' for f in ['mali/400.css', 'mali/500.css', 'mali/600.css', 'mali/700.css', 'klee-one/400.css', 'klee-one/600.css'])
LOGO = 'file://' + R + 'public/app/media/brand/logo-mark.svg'

def top(g):
    right = f'<span class="gnum">Nhóm {g}/12</span>' if g else ''
    return f'<div class="top"><img src="{LOGO}"><span>Anh Trọng Dạy JFT</span>{right}</div>'
def head(sl):
    g = sl['g']
    return (f'<div class="head"><div class="hl"><div class="gb">{g:02d}</div><div><div class="gt{' long' if len(G[g-1]) > 16 else ''}">{e(G[g-1])}</div>'
            f'<div class="sub">{e(sl["sub"])}</div></div></div><img class="ic" src="{IMG}{sl["img"]}.png"></div>')
def bottom(i, n):
    return (f'<div class="bot"><div class="src">出典：いろどり 生活の日本語・文法ノート いろどり（国際交流基金）</div>'
            f'<div class="prog"><i style="width:{(i + 1) / n * 100:.1f}%"></i></div></div>')
def card(it):
    pat, mean, key, vi, tag = it
    exh = ''
    if key:
        exh = f'<div class="ex jp">{JP(ex_of(key))}</div><div class="exv">{e(vi)}</div>'
    return (f'<div class="card"><div class="pr"><span class="pat {'vn' if VN.search(pat) else 'jp'}">{MIX(pat) if VN.search(pat) else JP(pat)}</span><span class="mean">{MIX(mean)}</span><span class="tag">{e(tag)}</span></div>'
            f'{exh}</div>')

def table(rows, cls=''):
    h = rows[0]
    o = '<table class="tb ' + cls + '"><tr>' + ''.join(f'<th class="jp">{JP(c)}</th>' if c else '<th></th>' for c in h) + '</tr>'
    for r in rows[1:]:
        o += '<tr>' + f'<td class="rl">{e(r[0])}</td>' + ''.join(f'<td class="jp">{JP(c)}</td>' for c in r[1:]) + '</tr>'
    return o + '</table>'

TE = [('い・ち・り', 'って', ['買います→買って', '待ちます→待って', '帰ります→帰って']),
      ('み・び・に', 'んで', ['飲みます→飲んで', '遊びます→遊んで', '死にます→死んで']),
      ('き', 'いて', ['書きます→書いて']), ('ぎ', 'いで', ['泳ぎます→泳いで']), ('し', 'して', ['話します→話して']),
      ('Riêng', '', ['行きます→行って'])]

out = []
N = len(S)
for i, sl in enumerate(S):
    k = sl['kind']
    if k == 'title':
        body = (f'{top(0)}<div class="tt"><div class="tk">JFT-Basic · いろどり</div><h1>TOÀN BỘ<br><b>NGỮ PHÁP</b><br>JFT</h1>'
                f'<div class="t10">gói gọn trong 10 phút</div><img src="{IMG}{sl["img"]}.png" class="timg">'
                '<div class="chips"><span>12 nhóm</span><span>~70 mẫu</span><span class="jp">入門 → 初級2</span></div></div>')
    elif k == 'map':
        cells = ''.join(f'<div class="mc"><b>{j + 1:02d}</b><span>{e(t)}</span></div>' for j, t in enumerate(G))
        body = f'{top(0)}<div class="mh">12 nhóm ngữ pháp<br>hay ra trong đề JFT</div><div class="mg">{cells}</div><img class="mimg" src="{IMG}{sl["img"]}.png">'
    elif k == 'items' or k == 'give':
        extra = ''
        if k == 'give':
            extra = ('<div class="gv"><div class="pp me">わたし<small>tôi</small></div><div class="arr">'
                     '<div><b class="jp">あげます</b> <span>→</span></div><div><span>←</span> <b class="jp">もらいます</b> <small>(から／に)</small></div>'
                     '<div><span>←</span> <b class="jp">くれます</b></div></div><div class="pp you">ほかの人<small>người khác</small></div></div>')
        body = f'{top(sl["g"])}{head(sl)}{extra}<div class="cards n{len(sl["items"])}">' + ''.join(card(it) for it in sl['items']) + '</div>'
    elif k == 'conj':
        def cj(x):
            a, b = x.rsplit('|', 1); return f'{JP(a)}<b>{e(b)}</b>'
        trs = ''.join(f'<tr><td class="rl">{e(r[0])}</td><td class="jp">{cj(r[1])}</td><td class="jp">{cj(r[2])}</td></tr>' for r in sl['rows'])
        exs = ''.join(f'<div class="card sm"><div class="ex jp">{JP(ex_of(key))}</div><div class="exv">{e(vi)}</div></div>' for key, vi, tag in sl['ex'])
        body = (f'{top(sl["g"])}{head(sl)}<div class="tw"><table class="tb cj"><tr><th></th><th>Danh từ <small>(N)</small></th><th>Tính từ đuôi い</th></tr>{trs}</table></div>'
                f'<div class="note">Tính từ đuôi な chia giống danh từ:<br><span class="jp">{JP("{静|しず}かです")} → {JP("{静|しず}かじゃないです")}</span><br>'
                f'<span class="jp">いい</span> (tốt) → <b class="jp">よくないです ・ よかったです</b></div><div class="cards">{exs}</div>')
    elif k == 'forms':
        body = (f'{top(sl["g"])}{head(sl)}<div class="tw">{table(sl["rows"], "fm")}</div>'
                '<div class="note">Thể thông thường <span class="jp">（普通形）</span>:<br>thể từ điển · <span class="jp">ない</span> · <span class="jp">た</span> → dùng khi nói chuyện thân mật</div>'
                '<div class="formula"><span class="jp">' + furi('書いて') + '</span> + <span class="jp">ください</span> = mẫu ngữ pháp</div>')
    elif k == 'terule':
        rows = ''.join(f'<div class="tr"><div class="tl {"vn" if a == "Riêng" else "jp"}">{e(a)}</div><div class="ta jp">{"→ " + e(b) if b else ""}</div><div class="tx jp">'
                       + ''.join(f'<span>{JP(x)}</span>' for x in xs) + '</div></div>' for a, b, xs in TE)
        body = (f'{top(sl["g"])}{head(sl)}<div class="te"><div class="teh">Nhóm 1 <small>(âm trước ます)</small></div>{rows}'
                f'<div class="teh">Nhóm 2 <small>bỏ ます thêm て</small></div><div class="tr"><div class="tl jp">ます</div><div class="ta jp">→ て</div><div class="tx jp"><span>{JP("食べます→食べて")}</span><span>{JP("見ます→見て")}</span></div></div>'
                f'<div class="teh">Nhóm 3</div><div class="tr t3"><div class="tx jp"><span>{JP("します→して")}</span><span>{JP("{来|き}ます→{来|き}て")}</span></div></div>'
                '<div class="note">Thể た: đổi y hệt, <b class="jp">て→た</b>　<b class="jp">で→だ</b></div></div>')
    elif k == 'outro':
        cells = ''.join(f'<span>{j + 1}. {e(t)}</span>' for j, t in enumerate(G))
        body = (f'{top(0)}<div class="oh">Ôn mỗi tối<br><b>1 nhóm</b></div><div class="orc">{cells}</div>'
                f'<img src="{IMG}{sl["img"]}.png" class="oimg"><div class="cta">Làm đề thi thử có giải thích<br><b>App Anh Trọng Dạy JFT</b><br><small>link ở trang cá nhân</small></div>')
    out.append(f'<section class="sl k-{k}" id="s{i + 1}">{body}{bottom(i, N)}<div class="cam"></div></section>')

CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'slide.css')).read()
os.makedirs('/tmp/ngp', exist_ok=True)
open('/tmp/ngp/slides.html', 'w').write(f'<!doctype html><html lang="vi"><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body>{"".join(out)}'
    '<script>/* thu nhỏ chữ nếu tràn */document.fonts.ready.then(()=>{document.querySelectorAll(".cards").forEach(c=>{const sec=c.closest(".sl"),lim=sec.getBoundingClientRect().top+1590;let s=1.2;c.style.setProperty("--k",s);'
    'while(c.getBoundingClientRect().bottom>lim&&s>.6){s-=.02;c.style.setProperty("--k",s)}});document.body.dataset.ok=1})</script></body></html>')
json.dump([{'say': x['say'], 'kind': x['kind'], 'g': x.get('g', 0)} for x in S], open('/tmp/ngp/script.json', 'w'), ensure_ascii=False)
print('ok', N, 'slide')
