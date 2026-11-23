"""Bản MẪU sách "Ngữ pháp いろどり" (bìa + Bài 1 初級1) → /tmp/kb/grammar.html. Mẫu câu + ví dụ: 文法ノート いろどり."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

G = load('grammar')
NP = sum(len(g['points']) for g in G if g['lv'] in ('入門', '初級1', '初級2'))
P = {x['no']: x for x in [g for g in G if g['lv'] == '初級1' and g['bai'] == 1][0]['points']}
IMG = '/tmp/kb/img/'
LAB = 'いろどり 初級1 · Bài 1'
def ex(jp, vi): return f'<div class="gx"><p class="jp">{J(jp)}</p><p class="vi">{e(vi)}</p></div>'
def card(no, pat, mean, body):
    return f'<div class="gc"><div class="gch"><b>{no}</b><span class="jp pat">{J(pat)}</span><i>{e(mean)}</i></div>{body}</div>'
F = lambda *xs: '<div class="fm">' + '<em>+</em>'.join(xs) + '</div>'
box = lambda t, c='': f'<span class="fx {c}">{J(t)}</span>'

g1 = card('❶', '丁寧体・普通体', 'Lịch sự · Thân mật', f'''<div class="cmp">
<div class="cl"><img src="{b64(IMG + 'b01_02.jpg')}"><div><span class="tag">{J("{丁寧体|ていねいたい}")}</span><p class="jp big">{J("お{久|ひさ}しぶりです。<br>お{元気|げんき}ですか？")}</p><small>{J("{先輩|せんぱい}・{上司|じょうし}・{初|はじ}めての{人|ひと}")}</small></div></div>
<div class="cl b"><img src="{b64(IMG + 'b01_01.jpg')}"><div><span class="tag">{J("{普通体|ふつうたい}")}</span><p class="jp big">{J("{久|ひさ}しぶり。<br>{元気|げんき}？")}</p><small>{J("{友|とも}だち・{家族|かぞく}")}</small></div></div></div>''')
g2 = card('❷', '【期間】になります', 'Đã được (bao lâu)', F(box('{期間|きかん}', 'v'), box('になります')) + f'''
<div class="tline"><span class="pt jp">{J("{来|き}た")}</span><span class="bar"><b class="jp">{J("1{年|ねん}")}</b></span><span class="pt now jp">{J("{今|いま}")}</span></div>
{ex("{日本|にほん}に{来|き}て[[1{年|いちねん}になります]]。", "Tôi đến Nhật được 1 năm rồi.")}{ex("{仕事|しごと}を{始|はじ}めて[[3か{月|げつ}になります]]。", "Đi làm được 3 tháng rồi.")}''')
g3 = card('❸', '【時点】（に）来ました', 'Đến (lúc nào)', F(box('{時点|じてん}', 'v'), box('に'), box('{来|き}ました')) + f'''
<div class="rule"><div class="ok"><b>に</b><span class="jp">{J("{9月|くがつ}に・{日曜日|にちようび}に・{20日|はつか}に")}</span></div>
<div class="ng"><b>✕に</b><span class="jp">{J("{去年|きょねん}・{先月|せんげつ}・{先週|せんしゅう}")}</span></div></div>
{ex("[[{去年|きょねん}の{9月|くがつ}に]]{来|き}ました。", "Tôi sang hồi tháng 9 năm ngoái.")}{ex("[[{先月|せんげつ}]]、{来|き}ました。", "Tôi sang tháng trước.")}''')
JB = [('b01_05.jpg', '{工場|こうじょう}で[[{働|はたら}いています]]。'), ('b01_06.jpg', '{介護|かいご}の{仕事|しごと}を[[しています]]。'), ('b01_10.jpg', '{専門学校|せんもんがっこう}に[[{通|かよ}っています]]。')]
g4 = card('❹', 'V-ています', 'Đang (làm nghề / việc gì)', F(box('V-て', 'v'), box('います')) +
          '<div class="g4">' + ''.join(f'<figure><img src="{b64(IMG + f)}"><figcaption class="jp">{J(t)}</figcaption></figure>' for f, t in JB) + '</div>')
TE = [('い・ち・り', 'って', '{買|か}います → {買|か}って'), ('み・び・に', 'んで', '{飲|の}みます → {飲|の}んで'), ('き', 'いて', '{書|か}きます → {書|か}いて'),
      ('ぎ', 'いで', '{泳|およ}ぎます → {泳|およ}いで'), ('し', 'して', '{話|はな}します → {話|はな}して'), ('{行|い}きます', '', '{行|い}って')]
te = ''.join(f'<tr><td class="jp a">{J(a)}</td><td class="jp b">{"→ " + b if b else ""}</td><td class="jp c">{J(c)}</td></tr>' for a, b, c in TE)
g5 = card('◆', 'テ形', 'Thể て', f'''<div class="te2"><table><tr><th colspan="3">Nhóm 1</th></tr>{te}</table>
<div class="te3"><div><span class="h">Nhóm 2</span><p class="jp">{J("{食|た}べます → {食|た}べて")}</p></div><div><span class="h">Nhóm 3</span><p class="jp">{J("します → して")}</p><p class="jp">{J("{来|き}ます → {来|き}て")}</p></div></div></div>''')

p1 = f'''<section class="pg unit gp">{head('初級1', 1, 'レストランで{働|はたら}いています', 'Tôi đang làm việc ở nhà hàng', 'トピック · {今|いま}の{私|わたし}')}
{g1}{g2}{g3}{foot(LAB, 2)}</section>'''
p2 = f'<section class="pg unit gp">{g4}{g5}{foot(LAB, 3)}</section>'

# luyện tập: câu hỏi 文法ノート (quiz)
QS = [(no, q) for no in ['❶', '❷', '❸', '❹', '◆'] for q in P[no].get('quiz', [])]
qh = ''
for i, (no, q) in enumerate(QS):
    qh += f'<li><p class="jp">{J(q["q"])}</p><div class="ops">' + ''.join(f'<span class="jp">{"abc"[k]}. {J(o)}</span>' for k, o in enumerate(q['o'])) + '</div></li>'
ans = f'''<div class="akb"><div class="akh"><span class="jp">こたえ</span>Đáp án</div>
<p>{"　".join(f"{i+1}. {'abc'[q['a']]}" for i, (no, q) in enumerate(QS))}</p></div>'''
p3 = f'''<section class="pg unit ex"><div class="sh"><span class="no">✎</span><span class="jp">練習</span><span class="vi">Luyện tập</span></div>
<ol class="gq">{qh}</ol>{ans}{foot(LAB, 4)}</section>'''

CSS = '''
.cover.gcv .tblock h1 em{background:linear-gradient(transparent 62%,rgba(120,180,230,.6) 62%,rgba(120,180,230,.6) 90%,transparent 90%)}
.gp .uh{margin-bottom:5mm}
.gc{border:.4mm solid var(--line);border-radius:3mm;padding:3mm 4mm 3.4mm;margin-bottom:4mm;background:#fff}
.gch{display:flex;align-items:center;gap:3mm;margin-bottom:2.6mm}
.gch b{width:9mm;height:9mm;border-radius:50%;background:var(--navy);color:#fff;display:grid;place-items:center;font-size:15px}
.gch .pat{font-size:21px;color:var(--navy)}.gch i{font-style:normal;font-weight:700;font-size:13px;color:var(--lv);margin-left:auto}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.cl{display:flex;gap:3mm;align-items:center;background:#eef5fb;border-radius:2.4mm;padding:2.4mm}
.cl.b{background:#fdf1e0}
.cl img{width:30mm;height:27mm;object-fit:cover;border-radius:1.6mm;background:#fff}
.cl .tag{font-family:'Klee One',serif;font-weight:600;font-size:13px;background:var(--navy);color:#fff;border-radius:1mm;padding:0 2mm}
.cl.b .tag{background:var(--lv)}
.cl .big{font-size:18px;line-height:1.7;margin:1mm 0}
.cl small{font-size:11.5px;color:#55657a;font-family:'Klee One',serif;font-weight:600}
.fm{display:flex;align-items:center;gap:2mm;margin:0 0 3mm}
.fm em{font-style:normal;font-weight:700;color:var(--pink);font-size:18px}
.fx{font-family:'Klee One',serif;font-weight:600;font-size:18px;border:.45mm solid var(--navy);border-radius:2mm;padding:.4mm 3.4mm;line-height:1.7;color:var(--navy)}
.fx.v{background:var(--navy);color:#fff}.fx.v rt{color:#cfe0ee}
.tline{display:flex;align-items:center;gap:2mm;margin:1mm 0 3mm;padding:0 6mm}
.tline .pt{font-size:15px;background:#f1f4f7;border-radius:10mm;padding:0 3mm}.tline .pt.now{background:var(--pink);color:#fff}.tline .pt.now rt{color:#fde}
.tline .bar{flex:1;height:.8mm;background:var(--navy);position:relative;display:flex;justify-content:center}
.tline .bar b{position:absolute;top:-8.5mm;font-size:16px;color:var(--navy)}
.tline .bar::after{content:'';position:absolute;right:-1mm;top:-1.2mm;border:1.6mm solid transparent;border-left-color:var(--navy);border-right:0}
.gx{border-left:.8mm solid var(--line);padding:.4mm 0 .4mm 3mm;margin-top:1.6mm}
.gx .jp{font-size:16px;line-height:1.9}.gx .vi{font-size:10.5px;color:var(--mut)}
.rule{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin-bottom:1mm}
.rule>div{display:flex;align-items:center;gap:2.4mm;border-radius:2mm;padding:1.6mm 3mm}
.rule .ok{background:#e8f5ee}.rule .ng{background:#fdecef}
.rule b{font-family:'Klee One',serif;font-size:16px;color:#1f7a4d}.rule .ng b{color:var(--pink)}
.rule .jp{font-size:14px;line-height:1.8}
.g4{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm}
.g4 figure{border:.3mm solid var(--line);border-radius:2mm;overflow:hidden}
.g4 img{width:100%;height:30mm;object-fit:cover;object-position:center 30%;display:block}
.g4 figcaption{font-size:13.5px;line-height:1.8;text-align:center;padding:.4mm 1mm 1mm}
.te2{display:grid;grid-template-columns:1.6fr 1fr;gap:4mm;align-items:start}
.te2 table{border-collapse:collapse;width:100%}
.te2 th{text-align:left;font-size:11px;color:var(--lv);padding-bottom:1mm}
.te2 td{border-top:.3mm dashed var(--line);padding:.3mm 1.4mm;line-height:1.75}
.te2 .a{font-size:15px;color:var(--navy)}.te2 .b{font-size:15px;color:var(--pink);white-space:nowrap}.te2 .c{font-size:13.5px}
.te3>div{background:#f5f8fb;border-radius:2mm;padding:1.6mm 3mm;margin-bottom:2mm}
.te3 .h{font-size:11px;font-weight:700;color:var(--lv)}.te3 .jp{font-size:14.5px;line-height:1.8}
.gq{list-style:none;counter-reset:g;display:grid;grid-template-columns:1fr 1fr;gap:2.6mm 6mm}
.gq li{counter-increment:g;position:relative;padding-left:8mm;border-bottom:.3mm dashed var(--line);padding-bottom:1.6mm}
.gq li::before{content:counter(g);position:absolute;left:0;top:1.6mm;width:5.6mm;height:5.6mm;border-radius:50%;background:var(--lvl);color:#b8650c;font-size:10px;font-weight:700;display:grid;place-items:center}
.gq .jp{font-size:14px;line-height:1.95}
.ops{display:flex;gap:1.6mm;flex-wrap:wrap}.ops span{font-size:13px;border:.3mm solid var(--line);border-radius:1.4mm;padding:0 2mm;line-height:1.9}
'''
body = cover('文法', 'NGỮ PHÁP', NP, '文型', 'gcv') + p1 + p2 + p3
write('/tmp/kb/grammar.html', body, CSS)
print('ok grammar', NP, len(QS))
