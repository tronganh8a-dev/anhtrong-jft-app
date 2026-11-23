"""Bản MẪU sách "Trọn bộ chữ Hán いろどり" (bìa + Bài 1 初級1) → /tmp/kb/sample.html → PDF.
Chạy: python3 src/kanjibook/build_sample.py && (cd /tmp/tk && node <repo>/src/kanjibook/pdf.js /tmp/kb/sample.html /tmp/kb/sample.pdf)
Chữ viết {漢字|かな} = ruby; [[...]] = từ trọng tâm (gạch chân); ((...)) = ô trống điền."""
import json, re, os, html, base64, collections
A = os.path.dirname(os.path.abspath(__file__)) + '/'
R = A + '../../'
FS = '/tmp/fs/node_modules/@fontsource/'
e = html.escape

# ---------- dữ liệu ----------
_s = open(R + 'public/app/data/docs.js', encoding='utf-8').read()
DOCS = json.JSONDecoder().raw_decode(_s[_s.index('=') + 1:].lstrip())[0]
CH, WD = {}, {}
for lv, v in DOCS['kanji'].items():
    for w in v:
        WD.setdefault(w['w'], w)
        for c in w['chars']: CH.setdefault(c['k'], c)
CH['仕'] = {'k': '仕', 'hv': 'SĨ', 'on': 'シ', 'kun': 'つか.える', 'vi': 'làm việc, phục vụ'}
STK = json.load(open(R + 'src/tailieu_src/kanjivg_strokes.json'))
LS = json.load(open(A + 'lessons.json'))
isk = lambda c: '一' <= c <= '鿿' or c == '々'
plain = lambda t: re.sub(r'<rt>.*?</rt>|<[^>]+>', '', t)

def J(t):
    """chuỗi rút gọn → HTML"""
    t = e(t)
    t = re.sub(r'\(\((.*?)\)\)', r'<span class="blank">\1</span>', t)
    t = re.sub(r'\[\[(.*?)\]\]', r'<u class="tg">\1</u>', t)
    return re.sub(r'\{([^{}|]+)\|([^{}]+)\}', r'<ruby>\1<rt>\2</rt></ruby>', t)

# số chữ mới của từng quyển (theo thứ tự xuất hiện)
seen = collections.OrderedDict()
def addk(t, lv):
    for c in plain(t):
        if isk(c) and c not in seen: seen[c] = lv
for w in DOCS['kanji']['入門']: addk(w['w'], '入門')
for x in LS:
    if x['lv'] in ('初級1', '初級2'):
        for w in x['words']: addk(w['w'], x['lv'])
CNT = collections.Counter(seen.values()); TOTAL = len(seen)
NLES = 18 * 3

# ---------- nét viết (KanjiVG CC BY-SA 3.0) ----------
def stroke_svg(k, upto=None, cls='sf'):
    p = STK[k]['p']; n = len(p) if upto is None else upto
    o = ''.join(f'<path d="{d}" class="{"cur" if i == n - 1 and upto else "old"}"/>' for i, d in enumerate(p[:n]))
    return f'<svg class="{cls}" viewBox="0 0 109 109"><line x1="54.5" y1="0" x2="54.5" y2="109"/><line x1="0" y1="54.5" x2="109" y2="54.5"/>{o}</svg>'
def nstroke(k): return len(STK[k]['p'])

# ---------- Bài 1 初級1 ----------
L = [x for x in LS if x['lv'] == '初級1' and x['bai'] == 1][0]
TITLE = '{レストラン|}で{働|はたら}いています'.replace('{レストラン|}', 'レストラン')
TITLE_VI = 'Tôi đang làm việc ở nhà hàng'
KJ = []
for w in L['words']:
    for c in plain(w['w']):
        if isk(c) and c not in KJ: KJ.append(c)
def words_of(k):
    o = []
    for w in L['words']:
        if k in plain(w['w']): o.append((w['w'], w['vi']))
    extra = {'生': [('{先生|せんせい}', 'giáo viên')], '学': [('{大学|だいがく}', 'đại học')], '年': [('{今年|ことし}', 'năm nay')],
             '週': [('{今週|こんしゅう}', 'tuần này')], '先': [('{先生|せんせい}', 'giáo viên')], '気': [('{天気|てんき}', 'thời tiết')],
             '事': [('{食事|しょくじ}', 'bữa ăn')], '校': [], '作': [], '働': [], '忙': [], '活': [], '元': [], '去': [], '仕': []}
    return o, extra.get(k, [])
IMG = '/tmp/kb/img/'
def b64(f):
    return 'data:image/jpeg;base64,' + base64.b64encode(open(f, 'rb').read()).decode()
TILES = [('b01_03.jpg', 'レストランで[[{働|はたら}]]いています。', 'Tôi đang làm ở nhà hàng.'),
         ('b01_05.jpg', '{工場|こうじょう}で[[{働|はたら}]]いています。', 'Tôi đang làm ở nhà máy.'),
         ('b01_06.jpg', '{介護|かいご}の[[{仕事|しごと}]]をしています。', 'Tôi làm công việc chăm sóc người cao tuổi.'),
         ('b01_08.jpg', '{野菜|やさい}を[[{作|つく}]]っています。', 'Tôi đang trồng rau.'),
         ('b01_10.jpg', '[[{学生|がくせい}]]です。{専門|せんもん}[[{学校|がっこう}]]に{通|かよ}っています。', 'Tôi là sinh viên, đang học trường nghề.'),
         ('b01_01.jpg', '{久|ひさ}しぶり。[[{元気|げんき}]]？', 'Lâu quá không gặp. Khoẻ không?')]
USE = [  # 使い方: câu nguyên văn いろどり 初級1 第1課 — từ trọng tâm không có furigana
    ('[[学生]]です。{専門|せんもん}[[学校]]に{通|かよ}っています。', 'Tôi là sinh viên. Tôi đang học trường dạy nghề.'),
    ('Ａ：[[働]]いていますか？　Ｂ：いいえ、[[学生]]です。{今|いま}は、{日本語|にほんご}[[学校]]に{通|かよ}っています。', 'A: Bạn đang đi làm à? — B: Không, tôi là học sinh. Bây giờ tôi đang học ở trường tiếng Nhật.'),
    ('[[去年]]の{9月|くがつ}に{来|き}ました。', 'Tôi sang hồi tháng 9 năm ngoái.'),
    ('レストランで[[働]]いています。とても[[忙]]しいです。', 'Tôi đang làm ở nhà hàng. Rất bận.'),
    ('{介護|かいご}の[[仕事]]をしています。', 'Tôi làm công việc chăm sóc người cao tuổi.'),
    ('{野菜|やさい}を[[作]]っています。', 'Tôi đang trồng rau.'),
    ('[[先週]]は、とても[[忙]]しかったです。', 'Tuần trước tôi rất bận.'),
    ('{日本|にほん}の[[生活]]に、もう{慣|な}れましたか？', 'Bạn đã quen với cuộc sống ở Nhật chưa?'),
    ('お{久|ひさ}しぶりです。お[[元気]]ですか？', 'Lâu quá không gặp. Anh/chị vẫn khoẻ chứ ạ?'),
]
# ---- bài tập (tự soạn) ----
Q1 = [('[[学校]]は{駅|えき}の{近|ちか}くです。', 'がっこう'), ('{母|はは}は[[元気]]です。', 'げんき'), ('{日本|にほん}の[[生活]]は{楽|たの}しいです。', 'せいかつ'),
      ('[[去年]]、{日本|にほん}に{来|き}ました。', 'きょねん'), ('{工場|こうじょう}で[[働]]いています。', 'はたら'), ('[[先週]]、{映画|えいが}を{見|み}ました。', 'せんしゅう')]
Q2 = [('{私|わたし}は[[がくせい]]です。', '学生'), ('[[しごと]]は{何|なん}ですか。', '仕事'), ('{今週|こんしゅう}は[[いそが]]しいです。', '忙'),
      ('{昼|ひる}ご{飯|はん}を[[つく]]ります。', '作'), ('[[きょねん]]の{4月|しがつ}に{来|き}ました。', '去年'), ('お[[げんき]]ですか。', '元気')]
def opts(w):
    x = WD[w]; return x
Q3 = [('学生', 'がくせい'), ('学校', 'がっこう'), ('元気', 'げんき'), ('生活', 'せいかつ'), ('先週', 'せんしゅう'), ('働く', 'はたらく')]
Q4 = [('学生', '{学生|がくせい}'), ('去年', '{去年|きょねん}'), ('忙しい', '{忙|いそが}しい'), ('作る', '{作|つく}る'), ('学校', '{学校|がっこう}'), ('先週', '{先週|せんしゅう}')]
Q5 = '学 生 校 活 元 気 去 年 先 週 仕 事'.split()
Q6 = [('{元|げん}□', '{天|てん}□', '気', 'げんき・てんき'), ('{学|がく}□', '□{活|かつ}', '生', 'がくせい・せいかつ'), ('□{校|こう}', '{大|だい}□', '学', 'がっこう・だいがく'),
      ('{去|きょ}□', '{今|こ}□', '年', 'きょねん・ことし'), ('{先|せん}□', '{今|こん}□', '週', 'せんしゅう・こんしゅう'), ('{仕|し}□', '{食|しょく}□', '事', 'しごと・しょくじ')]

import random
random.seed(1)
def shuf(a):
    a = a[:]; random.shuffle(a); return a

# ---------- trang ----------
def foot(n, side='r'):
    return (f'<div class="ft {side}"><span class="fl">いろどり 初級1 · Bài 1</span><span class="pn">{n}</span>'
            f'<span class="fb">Anh Trọng Dạy JFT</span></div>')

GRID = ''.join(f'<i>{c}</i>' for c in seen)
LOGO = open(R + 'public/app/media/brand/logo-ngang.svg', encoding='utf-8').read()
LOGO = re.sub(r'<\?xml[^>]*>', '', LOGO)
LOGO_W = open(R + 'public/app/media/brand/logo-ngang-trang.svg', encoding='utf-8').read() if os.path.exists(R + 'public/app/media/brand/logo-ngang-trang.svg') else LOGO
COV = {k: b64(R + f'public/app/media/cover/{f}') for k, f in (('入門', 'nyumon.jpg'), ('初級1', 's1.jpg'), ('初級2', 's2.jpg'))}

cover = f'''<section class="pg cover">
<div class="paper"></div>
<div class="kgrid">{GRID}</div>
<div class="fade"></div>
<div class="hero">
  <div class="kan">漢<br>字</div>
  <div class="seal"><span>い<br>ろ<br>ど<br>り</span></div>
</div>
<div class="tblock"><h1><em>CHỮ HÁN</em></h1><div class="lv jp">入門 · 初級1 · 初級2</div></div>
<div class="obi">
  <div class="o o1"><img src="{COV['入門']}"></div>
  <div class="o o2"><img src="{COV['初級1']}"></div>
  <div class="o o3"><img src="{COV['初級2']}"></div>
  <div class="osum"><b>{TOTAL}</b><span class="jp">字</span></div>
</div>
<div class="cbot"><div class="lg">{LOGO}</div></div>
</section>'''

# trang mở bài
band = ''.join(f'<div class="bk"><b class="jp">{k}</b><small>{CH[k]["hv"]}</small></div>' for k in KJ)
tiles = ''.join(f'<figure><img src="{b64(IMG + f)}"><figcaption><p class="jp">{J(jp)}</p><p class="vi">{e(vi)}</p></figcaption></figure>' for f, jp, vi in TILES)
wl = ''.join(f'<div class="kwi"><span class="jp w">{w["w"]}</span><span class="m"><small>{e(w["hv"])}</small>{e(w["vi"])}</span></div>' for w in L['words'])
opener = f'''<section class="pg unit op">
<div class="uh"><div class="un"><small>初級1</small><b>1</b><span>Bài</span></div>
<div class="ut"><div class="tp">トピック · 今の私 — Tôi hiện tại</div><h2 class="jp">{J("レストランで{働|はたら}いています")}</h2><p>{TITLE_VI}</p></div></div>
<div class="band">{band}</div>
<div class="tiles">{tiles}</div>
<div class="kw"><div class="kwh"><span class="jp">漢字のことば</span></div>
<div class="kwg">{wl}</div></div>
{foot(2)}</section>'''

def card(k):
    c = CH[k]; n = nstroke(k)
    ws, ex = words_of(k)
    wh = ''.join(f'<span class="wc"><b class="jp">{w}</b>{e(v)}</span>' for w, v in ws) + ''.join(f'<span class="wc x"><b class="jp">{J(w)}</b>{e(v)}</span>' for w, v in ex)
    on = '・'.join(x for x in c['on'].split('・') if x and x != '—') or '—'
    kun = '・'.join(x.replace('.', '<i>-</i>') for x in c['kun'].split('・') if x and x != '—') or '—'
    seq = ''.join(stroke_svg(k, i + 1) for i in range(n))
    trace = ''.join(f'<span class="bx tr"><b class="jp">{k}</b></span>' for _ in range(3)) + '<span class="bx"></span>' * 8
    return f'''<div class="kc"><div class="kl"><div class="big">{stroke_svg(k, cls="bigs")}</div><div class="hv">{c["hv"]}</div><div class="ns">{n} nét</div></div>
<div class="kr"><div class="r1"><span class="mean">{e(c["vi"])}</span><span class="rd"><i>音</i><b class="jp">{on}</b></span><span class="rd"><i>訓</i><b class="jp">{kun}</b></span></div>
<div class="r2">{wh}</div><div class="r3">{seq}</div><div class="r4">{trace}</div></div></div>'''

def kpage(ks, lab, n, first=False):
    h = (f'<div class="sh"><span class="no">Ⅰ</span><span class="jp">読み方・書き方</span><span class="vi">Đọc và viết</span><span class="ab">{lab}</span></div>'
        )
    return f'<section class="pg unit kp">{h}<div class="kcs">{"".join(card(k) for k in ks)}</div>{foot(n)}</section>'

kps = [kpage(KJ[0:5], '1-A', 3, True), kpage(KJ[5:10], '1-B', 4), kpage(KJ[10:15], '1-C', 5)]

use = ''.join(f'<li><p class="jp">{J(j)}</p><p class="vi">{e(v)}</p></li>' for j, v in USE)
usep = f'''<section class="pg unit up"><div class="sh"><span class="no">Ⅱ</span><span class="jp">使い方</span><span class="vi">Dùng trong câu</span></div>
<ol class="use">{use}</ol>
<div class="tl"><div class="tlh">Thời gian · <span class="jp">時</span></div>
<div class="tlr"><span class="tw jp">{J("{先週|せんしゅう}")}<small>tuần trước</small></span><i>→</i><span class="tw jp">{J("{今週|こんしゅう}")}<small>tuần này</small></span><i>→</i><span class="tw jp">{J("{来週|らいしゅう}")}<small>tuần sau</small></span></div>
<div class="tlr"><span class="tw jp">{J("{去年|きょねん}")}<small>năm ngoái</small></span><i>→</i><span class="tw jp">{J("{今年|ことし}")}<small>năm nay</small></span><i>→</i><span class="tw jp">{J("{来年|らいねん}")}<small>năm sau</small></span></div>
<p class="tln"><span class="jp">今年</span> đọc là <b class="jp">ことし</b> (cách đọc đặc biệt). <span class="jp">去年・先週</span> không đi với trợ từ <span class="jp">に</span>: <span class="jp">{J("{去年|きょねん}、{来|き}ました。")}</span></p></div>
{foot(6)}</section>'''

def q_read():
    return ''.join(f'<li class="jp">{J(s)}<span class="ans">（　　　　　　　）</span></li>' for s, a in Q1)
def q_write():
    return ''.join(f'<li class="jp">{J(s)}<span class="ans">［　　　　　　］</span></li>' for s, a in Q2)
P3 = [(w, r, shuf([w] + WD[w]['wk'][:2])) for w, r in Q3]
P4 = []
for w, r in Q4:
    rr = re.sub(r'\{[^|]+\|([^}]+)\}', r'\1', r); P4.append((w, rr, shuf([rr] + WD[w]['rd'][:2])))
def q_pick():
    return ''.join(f'<li><span class="jp qk">{r}</span>' + ''.join(f'<span class="op jp">{chr(97 + i)}. {x}</span>' for i, x in enumerate(ch)) + '</li>' for w, r, ch in P3)
def q_rd():
    return ''.join(f'<li><span class="jp qk">{plain(w)}</span>' + ''.join(f'<span class="op jp">{chr(97 + i)}. {x}</span>' for i, x in enumerate(ch)) + '</li>' for w, rr, ch in P4)
pool = ''.join(f'<span class="jp">{c}</span>' for c in shuf(Q5))
puz = ''.join(f'<div class="pz"><span class="jp">{J(a)}</span><span class="eq">・</span><span class="jp">{J(b)}</span><span class="eq">→</span><span class="box"></span><small>{h}</small></div>' for a, b, c, h in Q6)
ex1 = f'''<section class="pg unit ex"><div class="sh"><span class="no">Ⅲ</span><span class="jp">練習</span><span class="vi">Luyện tập</span></div>
<div class="q"><h4><b>1</b>Viết cách đọc của từ gạch chân bằng hiragana.</h4><ol class="ql">{q_read()}</ol></div>
<div class="q"><h4><b>2</b>Viết chữ Hán cho phần gạch chân.</h4><ol class="ql">{q_write()}</ol></div>
<div class="q"><h4><b>3</b>Chọn cách viết đúng.</h4><ol class="qo">{q_pick()}</ol></div>
<div class="q"><h4><b>4</b>Chọn cách đọc đúng.</h4><ol class="qo">{q_rd()}</ol></div>
{foot(7)}</section>'''
ex2 = f'''<section class="pg unit ex"><div class="q"><h4><b>5</b>Ghép 2 chữ thành từ đã học. Viết được bao nhiêu từ?</h4><div class="pool">{pool}</div>
<div class="wrbox">{"<span></span>" * 6}</div></div>
<div class="q"><h4><b>6</b>Chữ Hán nào điền được vào cả hai ô □?</h4><div class="pzs">{puz}</div></div>
<div class="tan"><div class="th"><span class="jp">漢字たんけん</span> Khám phá chữ Hán</div>
<div class="tg3">
<div class="tc"><div class="tct"><b class="jp">亻</b>bộ Nhân đứng — con người</div><p><span class="jp k">仕</span> = 亻 + 士 (SĨ) · <span class="jp k">作</span> = 亻 + 乍 · <span class="jp k">働</span> = 亻 + 動 (ĐỘNG: chuyển động)</p><p>Người chuyển động là người đang <b>làm việc</b> — <span class="jp">{J("{働|はたら}く")}</span>.</p></div>
<div class="tc"><div class="tct"><b class="jp">忄</b>bộ Tâm đứng — trái tim</div><p><span class="jp k">忙</span> = 忄 + 亡 (VONG: mất)</p><p>Bận đến mức “mất cả tâm trí” → <span class="jp">{J("{忙|いそが}しい")}</span>.</p></div>
<div class="tc"><div class="tct"><b class="jp">学</b>đọc ガク → ガッ</div><p><span class="jp">{J("{学生|がくせい}")}</span> · <span class="jp">{J("{大学|だいがく}")}</span></p><p>Khi đứng trước <span class="jp">校</span>: ガク + コウ → <b class="jp">がっこう</b> (âm ngắt っ).</p></div>
</div></div>
ANS_SLOT{foot(8)}</section>'''

# đáp án
a3 = ['abc'[ch.index(w)] for w, r, ch in P3]
a4 = ['abc'[ch.index(rr)] for w, rr, ch in P4]
ansp = f'''<div class="akb"><div class="akh"><span class="jp">こたえ</span>Đáp án</div>
<p><b>1</b> {"　".join(f"{i+1}. <span class='jp'>{a}</span>" for i, (s, a) in enumerate(Q1))}</p>
<p><b>2</b> {"　".join(f"{i+1}. <span class='jp'>{a}</span>" for i, (s, a) in enumerate(Q2))}</p>
<p><b>3</b> {"　".join(f"{i+1}. {x}" for i, x in enumerate(a3))}　　<b>4</b> {"　".join(f"{i+1}. {x}" for i, x in enumerate(a4))}</p>
<p><b>5</b> <span class="jp">学生・学校・生活・元気・去年・先週・仕事・先生</span></p>
<p><b>6</b> {"　".join(f"{i+1}. <span class='jp'>{c}</span>" for i, (a, b, c, h) in enumerate(Q6))}</p></div>'''

FONTS = ''.join(f'<link rel="stylesheet" href="file://{FS}{f}">' for f in [
    'klee-one/400.css', 'klee-one/600.css', 'quicksand/400.css', 'quicksand/500.css', 'quicksand/600.css', 'quicksand/700.css',
    'yuji-syuku/400.css', 'shippori-mincho-b1/500.css', 'shippori-mincho-b1/700.css', 'shippori-mincho-b1/800.css'])
CSS = open(A + 'book.css', encoding='utf-8').read()
os.makedirs('/tmp/kb', exist_ok=True)
open('/tmp/kb/sample.html', 'w', encoding='utf-8').write(
    f'<!doctype html><html lang="vi"><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body>'
    + cover + opener + ''.join(kps) + usep + ex1 + ex2.replace('ANS_SLOT', ansp) + '</body></html>')
print('ok', TOTAL, dict(CNT), KJ)
