"""Bản MẪU sách "Từ vựng いろどり" (bìa + Bài 1 初級1) → /tmp/kb/vocab.html"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

V = load('vocab')
WI = {}
for w in V['words']:
    WI.setdefault(w['h'], w)
NW = len({w['h'] for w in V['words']})

def rb(h, y):
    """ghép furigana theo okurigana: 知り合い/しりあい → {知|し}り{合|あ}い"""
    h = re.sub(r'（.*?）', '', h).strip(); y = re.sub(r'（.*?）', '', y).strip()
    if not any(isk(c) for c in h): return h
    parts = re.findall(r'[一-鿿々]+|[^一-鿿々]+', h)
    pat = ''.join('(.+?)' if isk(p[0]) else re.escape(p) for p in parts)
    m = re.fullmatch(pat, y)
    if not m: return '{' + h + '|' + y + '}'
    o, i = '', 0
    for p in parts:
        if isk(p[0]): i += 1; o += '{' + p + '|' + m.group(i) + '}'
        else: o += p
    return o
def W(h):
    w = WI[h]; suf = '（な）' if '（な）' in w['h'] else ''
    return rb(w['h'], w['y']) + suf, w['v'], w.get('hv', '')

IMG = '/tmp/kb/img/'
LAB = 'いろどり 初級1 · Bài 1'
def item(h, img=None):
    jp, vi, hv = W(h)
    pic = f'<img src="{b64(IMG + img)}">' if img else ''
    return f'<div class="vw{" pic" if img else ""}">{pic}<div class="t"><b class="jp">{J(jp)}</b><span>{e(vi)}</span></div></div>'
def sec(no, jp, vi, items, cls=''):
    return f'<div class="vs {cls}"><div class="vsh"><b>{no}</b><span class="jp">{J(jp)}</span><i>{vi}</i></div><div class="vg">{"".join(items)}</div></div>'

A_ = sec('A', '{再会|さいかい}', 'Gặp lại', [item('久しぶり', 'b01_01.jpg'), item('元気（な）'), item('おかげさまで'), item('知り合い', 'b01_00.jpg'),
                                        item('先輩', 'b01_13.jpg'), item('後輩'), item('慣れる'), item('なんとか'), item('もう'), item('まだ')])
JOBS = [('レストランで{働|はたら}く', 'b01_03.jpg'), ('ホテルで{働|はたら}く', 'b01_04.jpg'), ('{工場|こうじょう}で{働|はたら}く', 'b01_05.jpg'),
        ('{介護|かいご}の{仕事|しごと}をする', 'b01_06.jpg'), ('{建設|けんせつ}の{仕事|しごと}をする', 'b01_07.jpg'), ('{野菜|やさい}を{作|つく}る', 'b01_08.jpg'),
        ('{日本語学校|にほんごがっこう}で{勉強|べんきょう}する', 'b01_09.jpg'), ('{専門学校|せんもんがっこう}に{通|かよ}う', 'b01_10.jpg'), ('{主婦|しゅふ}／{主夫|しゅふ}', 'b01_11.jpg')]
jobs = ''.join(f'<figure><img src="{b64(IMG + f)}"><figcaption class="jp">{J(t)}</figcaption></figure>' for t, f in JOBS)
C_words = ''.join(item(h) for h in ['仕事', '働く', '学生', '勉強する', '通う', 'プログラミング'])
D_ = sec('D', '{感想|かんそう}', 'Cảm nghĩ', [item(h) for h in ['忙しい', '大変（な）', '疲れる', 'まあまあ（な）', '楽しい', 'みんな', '親切（な）', '勉強になる', '毎日']])
B_words = sec('B', '{期間|きかん}', 'Thời gian', [item(h) for h in ['半年', '先月', '先週', '去年', 'ちょうど', '生活']])
MON = [(1, 'いっ'), (2, 'に'), (3, 'さん'), (4, 'よん'), (5, 'ご'), (6, 'ろっ'), (7, 'なな'), (8, 'はち'), (9, 'きゅう'), (10, 'じゅっ'), (11, 'じゅういっ'), (12, 'じゅうに')]
YR = [(1, 'いち'), (2, 'に'), (3, 'さん'), (4, 'よ'), (5, 'ご'), (6, 'ろく'), (7, 'なな'), (8, 'はち'), (9, 'きゅう'), (10, 'じゅう')]
SP = {('m', 1), ('m', 6), ('m', 10), ('m', 11), ('y', 4), ('y', 7), ('y', 9)}
mg = ''.join(f'<div class="cn{" sp" if ("m", n) in SP else ""}"><b>{n}</b><span class="jp">{r}かげつ</span></div>' for n, r in MON)
yg = ''.join(f'<div class="cn{" sp" if ("y", n) in SP else ""}"><b>{n}</b><span class="jp">{r}ねん</span></div>' for n, r in YR)
counters = f'''<div class="cnt"><div class="cnh"><span class="jp">〜か{J("{月|げつ}")}</span><i>tháng</i></div><div class="cng">{mg}</div>
<div class="cnh"><span class="jp">〜{J("{年|ねん}")}</span><i>năm</i></div><div class="cng y">{yg}</div>
<div class="cnx jp">{J("{日本|にほん}に{来|き}て[[1{年|ねん}になります]]。")}</div></div>'''

T1 = {'lv': '初級1', 'bai': 1}
p1 = f'''<section class="pg unit vp">{head('初級1', 1, 'レストランで{働|はたら}いています', 'Tôi đang làm việc ở nhà hàng', 'トピック · {今|いま}の{私|わたし}')}
<div class="vcount"><b>{len([w for w in V['words'] if any(l[0] == '初級1' and l[1] == 1 for l in w['l'])])}</b><span class="jp">語</span></div>
{A_}{B_words}{counters}{foot(LAB, 2)}</section>'''
p2 = f'''<section class="pg unit vp"><div class="vs"><div class="vsh"><b>C</b><span class="jp">{J("{仕事|しごと}")}</span><i>Công việc</i></div>
<div class="jobs">{jobs}</div><div class="vg">{C_words}</div></div>{D_}{foot(LAB, 3)}</section>'''

# luyện tập (tự soạn, câu lấy từ sách)
Q1 = [('b01_04.jpg', 'ホテルで{働|はたら}く'), ('b01_07.jpg', '{建設|けんせつ}の{仕事|しごと}をする'), ('b01_09.jpg', '{日本語学校|にほんごがっこう}で{勉強|べんきょう}する'), ('b01_11.jpg', '{主婦|しゅふ}')]
BANK = ['{慣|な}れ', '{忙|いそが}し', '{疲|つか}れ', 'まあまあ', '{親切|しんせつ}', '{久|ひさ}しぶり']
Q2 = [('お((　　　　))です。お{元気|げんき}ですか？', '久しぶり'), ('{日本|にほん}に((　　　　))ましたか？', '慣れ'),
      ('うーん、((　　　　))ます。でも、みんな{親切|しんせつ}です。', '疲れ'), ('((　　　　))です。でも、{勉強|べんきょう}になります。', 'まあまあ'),
      ('{先週|せんしゅう}は、とても((　　　　))かったです。', '忙し')]
Q3 = ['1か{月|げつ}', '6か{月|げつ}', '10か{月|げつ}', '4{年|ねん}', '7{年|ねん}', '{半年|はんとし}']
A3 = ['いっかげつ', 'ろっかげつ', 'じゅっかげつ', 'よねん', 'ななねん／しちねん', 'はんとし']
q1 = ''.join(f'<div class="pq"><img src="{b64(IMG + f)}"><span class="no">{i + 1}</span><span class="ln"></span></div>' for i, (f, a) in enumerate(Q1))
bank = ''.join(f'<span class="jp">{J(b)}</span>' for b in BANK)
q2 = ''.join(f'<li class="jp">{J(s)}</li>' for s, a in Q2)
q3 = ''.join(f'<div class="rq"><span class="jp">{J(q.replace("{月|げつ}", "月").replace("{年|ねん}", "年").replace("{半年|はんとし}", "半年"))}</span><span class="ln"></span></div>' for q in Q3)
ans = f'''<div class="akb"><div class="akh"><span class="jp">こたえ</span>Đáp án</div>
<p><b>1</b> {"　".join(f"{i+1}. <span class='jp'>{plain(a)}</span>" for i, (f, a) in enumerate(Q1))}</p>
<p><b>2</b> {"　".join(f"{i+1}. <span class='jp'>{a}</span>" for i, (s, a) in enumerate(Q2))}</p>
<p><b>3</b> {"　".join(f"{i+1}. <span class='jp'>{a}</span>" for i, a in enumerate(A3))}</p></div>'''
p3 = f'''<section class="pg unit ex"><div class="sh"><span class="no">✎</span><span class="jp">練習</span><span class="vi">Luyện tập</span></div>
<div class="q"><h4><b>1</b>Nhìn tranh, viết từ.</h4><div class="pqs">{q1}</div></div>
<div class="q"><h4><b>2</b>Chọn từ điền vào ô.</h4><div class="pool w">{bank}</div><ol class="ql one">{q2}</ol></div>
<div class="q"><h4><b>3</b>Đọc thế nào?</h4><div class="rqs">{q3}</div></div>
{ans}{foot(LAB, 4)}</section>'''

CSS = '''
.cover.vc .tblock h1 em{background:linear-gradient(transparent 62%,rgba(243,169,195,.8) 62%,rgba(243,169,195,.8) 90%,transparent 90%)}
.vp .uh{margin-bottom:4mm}
.vcount{position:absolute;top:13mm;right:14mm;display:none}
.vs{margin-bottom:4mm}
.vsh{display:flex;align-items:center;gap:2.6mm;margin-bottom:2mm}
.vsh b{width:7mm;height:7mm;border-radius:50%;background:var(--pink);color:#fff;display:grid;place-items:center;font-size:12px}
.vsh .jp{font-size:17px;color:var(--navy)}.vsh i{font-style:normal;font-weight:700;font-size:13px;color:var(--lv)}
.vsh::after{content:'';flex:1;height:.3mm;background:var(--line)}
.vg{display:grid;grid-template-columns:repeat(3,1fr);gap:1.6mm}
.vw{display:flex;align-items:center;gap:2mm;border:.3mm solid var(--line);border-radius:2mm;padding:1mm 2.4mm;min-height:13mm;background:#fff}
.vw.pic{grid-row:span 2;flex-direction:column;align-items:stretch;padding:1.4mm}
.vw.pic img{width:100%;height:20mm;object-fit:cover;border-radius:1.2mm}
.vw .t{display:flex;flex-direction:column;line-height:1.2}
.vw .t b{font-size:16px;line-height:1.7;color:var(--ink)}
.vw .t span{font-size:10.5px;color:#55657a}
.cnt{border:.4mm solid var(--line);border-radius:2.4mm;padding:2.4mm 3mm;background:#fbfcfd}
.cnh{display:flex;align-items:baseline;gap:2mm;margin:1mm 0}.cnh .jp{font-size:16px;color:var(--navy)}.cnh i{font-style:normal;font-size:11px;font-weight:700;color:var(--lv)}
.cng{display:grid;grid-template-columns:repeat(4,1fr);gap:1.2mm}.cng.y{grid-template-columns:repeat(5,1fr)}
.cn{display:flex;align-items:baseline;gap:1.4mm;border:.3mm solid var(--line);border-radius:1.4mm;padding:.6mm 2mm;background:#fff}
.cn b{font-size:15px;color:var(--navy)}.cn .jp{font-size:12.5px}
.cn.sp{border-color:var(--pink);background:#fdf0f4}.cn.sp .jp{color:var(--pink)}
.cnx{margin-top:2mm;font-size:15px;text-align:center}
.jobs{display:grid;grid-template-columns:repeat(3,1fr);gap:2.4mm;margin-bottom:2.4mm}
.jobs figure{border:.3mm solid var(--line);border-radius:2.2mm;overflow:hidden}
.jobs img{width:100%;height:29mm;object-fit:cover;object-position:center 35%;display:block}
.jobs figcaption{font-size:13.5px;line-height:1.75;text-align:center;padding:.6mm 1mm 1mm}
.pqs{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-left:9mm}
.pq{position:relative;border:.3mm solid var(--line);border-radius:2mm;overflow:hidden;padding-bottom:9mm}
.pq img{width:100%;height:28mm;object-fit:cover}
.pq .no{position:absolute;top:1mm;left:1mm;background:var(--navy);color:#fff;border-radius:1mm;font-size:10px;font-weight:700;padding:0 1.6mm}
.pq .ln{position:absolute;left:3mm;right:3mm;bottom:3mm;border-bottom:.35mm solid #9fb0bf}
.pool.w span{display:inline-flex;align-items:center;width:auto!important;height:auto!important;min-width:0;padding:1mm 3.4mm;font-size:16px;white-space:nowrap;line-height:1.6}
.ql.one{grid-template-columns:1fr}
.blank{display:inline-block;min-width:22mm;border-bottom:.4mm solid #9fb0bf;color:transparent}
.rqs{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm 8mm;margin-left:9mm}
.rq{display:flex;align-items:flex-end;gap:3mm}.rq .jp{font-size:19px;min-width:20mm}.rq .ln{flex:1;border-bottom:.35mm solid #9fb0bf;height:7mm}
'''
body = cover('言葉', 'TỪ VỰNG', NW, '語', 'vc') + p1 + p2 + p3
write('/tmp/kb/vocab.html', body, CSS)
print('ok vocab', NW)
