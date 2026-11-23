"""Khoá cấp tốc · Buổi 17 (23/11/2026): Từ vựng khó JFT — nâng cao, 30 phút.
48 từ (4 chủ đề × 3 slide × 4 từ) hay gặp trong đề JFT; sau mỗi 3 slide là 4 câu trắc nghiệm chọn từ (có bình chọn).
Từ, cách đọc, Hán Việt, nghĩa, câu ví dụ: いろどり (public/app/data/vocab.js — trích từ sách; một vài câu lấy từ web bài học).
Câu trắc nghiệm: phần lớn tự soạn (ghi "tự soạn"), 3 câu lấy từ bộ đề trong app (ghi số đề).
Chạy: python3 src/tailieu_src/buoi17_tuvung_kho_build.py → public/tailieu/Buoi17_TuVung_Kho_JFT.html"""
import re, json, html, sys
R = '/home/claude/anhtrong-jft-app/'
exec(open(R + 'src/tailieu_src/_head_snip.py').read())  # HEAD, LOGO
_kg = open(R + 'src/tailieu_src/khaigiang_build.py').read()
KGCSS = _kg[_kg.index("HEAD = HEAD.replace('</style></head>', '''") + 41:_kg.index("</style></head>''', 1)")]
TAIL = open(R + 'src/tailieu_src/buoi15_tail.html').read()
sys.path.insert(0, R + 'src/kanjibook')
from common import load
V = load('vocab')
VW = {}
for w in V['words']:
    VW.setdefault(re.sub('（.*?）', '', w['h']).strip(), w)
e = html.escape
def rb(s):
    return re.sub(r'\{([^|{}]+)\|([^{}]*)\}', lambda m: f'<ruby>{m.group(1)}<rt>{m.group(2)}</rt></ruby>', s)
def wruby(h, y):
    """từ + cách đọc → {漢字|かな}…"""
    y = re.sub(r'（.*?）|\s.*$', '', y).strip()
    if not re.search(r'[一-鿿]', h): return h
    parts = re.findall(r'[一-鿿々]+|[^一-鿿々]+', h)
    pat = ''.join('(.+?)' if re.match(r'[一-鿿]', p) else re.escape(p) for p in parts)
    m = re.fullmatch(pat, y)
    if not m: return '{' + h + '|' + y + '}'
    o, i = '', 0
    for p in parts:
        if re.match(r'[一-鿿]', p): i += 1; o += '{' + p + '|' + m.group(i) + '}'
        else: o += p
    return o

# ---- 4 chủ đề × 12 từ: (từ, nghĩa ngắn — để trống thì lấy của vocab.js, câu ví dụ thay thế (jp, vi) nếu cần) ----
ROUNDS = [
 ('①', 'Thông báo · dịch vụ', 'お知らせ・サービス', [
   ('利用', 'sử dụng (dịch vụ, cơ sở)'), ('案内', 'hướng dẫn, dẫn đường'), ('申し込む', 'đăng ký'), ('受付', 'quầy tiếp nhận, lễ tân'),
   ('無料', 'miễn phí'), ('書類', 'giấy tờ, hồ sơ'), ('募集', 'tuyển, chiêu mộ'), ('販売', 'bán (hàng)'),
   ('飲食', 'ăn uống'), ('禁煙', 'cấm hút thuốc'), ('点検', 'kiểm tra định kỳ'), ('知らせる', 'thông báo, báo cho biết')]),
 ('②', 'Sự cố trong sinh hoạt', '生活のトラブル', [
   ('壊れる', 'bị hỏng'), ('割れる', 'bị vỡ (kính, cốc…)'), ('汚れる', 'bị bẩn'), ('つまる', 'bị tắc'),
   ('なくす', 'làm mất'), ('遅れる', 'bị muộn, trễ'), ('変わる', 'thay đổi'), ('片付ける', 'dọn dẹp, cất gọn'),
   ('断水', 'cúp nước'), ('乗り換える', 'đổi tàu, chuyển xe', ('{今|いま}、{新幹線|しんかんせん}に{乗|の}っています。もうすぐ{岡山駅|おかやまえき}です。{岡山駅|おかやまえき}で{乗|の}り{換|か}えます。', 'Đang đi Shinkansen, sắp tới ga Okayama. Đến ga Okayama sẽ đổi tàu.')),
   ('預ける', 'gửi (đồ, tiền)'), ('返す', 'trả lại')]),
 ('③', 'Thiên tai · an toàn', '災害・安全', [
   ('地震', 'động đất'), ('揺れる', 'rung, lắc', ('{緊急地震速報|きんきゅうじしんそくほう}です。{強|つよ}い{揺|ゆ}れに{警戒|けいかい}してください。', 'Cảnh báo động đất khẩn cấp. Hãy đề phòng rung lắc mạnh.')), ('避難', 'sơ tán, lánh nạn'), ('避難所', 'nơi sơ tán'),
   ('避難訓練', 'diễn tập sơ tán'), ('台風', 'bão'), ('大雪', 'tuyết rơi dày'), ('危ない', 'nguy hiểm'),
   ('非常食', 'đồ ăn dự trữ khẩn cấp'), ('懐中電灯', 'đèn pin'), ('給水車', 'xe cấp nước'), ('逃げる', 'chạy thoát, bỏ chạy')]),
 ('④', 'Phó từ · cảm xúc', '副詞・気持ち', [
   ('だいぶ', 'khá nhiều, đáng kể'), ('ずっと', 'suốt, mãi'), ('ちょうど', 'vừa đúng'), ('そろそろ', 'sắp đến lúc', ('もうこんな{時間|じかん}！　{私|わたし}、そろそろ{帰|かえ}らなくちゃ。', 'Đã giờ này rồi! Mình phải về thôi.')),
   ('もうすぐ', 'sắp, sắp sửa'), ('さっき', 'lúc nãy'), ('けっこう', 'khá là'), ('楽しむ', 'tận hưởng'),
   ('新鮮', 'tươi'), ('心配', 'lo lắng'), ('残念', 'tiếc'), ('慣れる', 'quen với')]),
]
VI_FIX = {'乗り換える': 'Đang đi Shinkansen, sắp tới ga Okayama. Đến ga Okayama sẽ đổi tàu.'}

# ---- câu trắc nghiệm: (câu có （　）, [phương án], chỉ số đúng, dịch, giải thích ngắn, nguồn) ----
QZ = [
 [('{参加|さんか}したい{人|ひと}は、{来週|らいしゅう}の{金曜日|きんようび}までに（　）ください。', ['{申|もう}し{込|こ}んで', '{知|し}らせて', '{案内|あんない}して', '{利用|りよう}して'], 0,
   'Ai muốn tham gia thì hãy đăng ký trước thứ Sáu tuần sau.', '「〜までに申し込む」 = đăng ký trước hạn. 知らせる là báo tin cho người khác, 案内する là hướng dẫn, 利用する là sử dụng.', 'tự soạn'),
  ('この{駐車場|ちゅうしゃじょう}は、お{店|みせ}で{買|か}い{物|もの}をした{人|ひと}は（　）で{使|つか}えます。', ['{無料|むりょう}', '{禁煙|きんえん}', '{販売|はんばい}', '{募集|ぼしゅう}'], 0,
   'Bãi đỗ xe này, ai mua hàng ở cửa hàng thì được dùng miễn phí.', '「無料で使える」 = dùng miễn phí. Ngược nghĩa: 有料 (mất phí).', 'tự soạn'),
  ('{館内|かんない}での（　）は{禁止|きんし}です。{飲|の}み{物|もの}は{休憩室|きゅうけいしつ}でどうぞ。', ['{飲食|いんしょく}', '{点検|てんけん}', '{受付|うけつけ}', '{書類|しょるい}'], 0,
   'Cấm ăn uống trong toà nhà. Đồ uống xin dùng ở phòng nghỉ.', 'Biển báo hay gặp: 「〜での飲食は禁止です」. Câu sau nói đồ uống → chọn 飲食.', 'tự soạn'),
  ('{明日|あした}はエレベーターの（　）があるので、10{時|じ}から12{時|じ}まで{使|つか}えません。', ['{点検|てんけん}', '{販売|はんばい}', '{募集|ぼしゅう}', '{案内|あんない}'], 0,
   'Ngày mai có kiểm tra thang máy nên từ 10 giờ đến 12 giờ không dùng được.', '点検 = kiểm tra máy móc định kỳ (ガス・エレベーター). Vì đang kiểm tra nên “không dùng được”.', 'tự soạn')],
 [('ゴミの{出|だ}し{方|かた}が（　）ので、{気|き}をつけてください。', ['{変|か}わった', 'わかった', '{貸|か}した'], 0,
   'Cách vứt rác đã thay đổi nên hãy chú ý.', '変わる = (quy định) thay đổi. わかる là hiểu, 貸す là cho mượn.', 'Đề 3 · câu 15'),
  ('トイレに{紙|かみ}をたくさん{流|なが}したら、（　）しまいました。', ['つまって', '{割|わ}れて', '{汚|よご}れて', '{遅|おく}れて'], 0,
   'Xả nhiều giấy vào bồn cầu nên bị tắc mất rồi.', 'つまる = (ống, bồn cầu) bị tắc. 割れる dùng cho kính, cốc bị vỡ.', 'tự soạn'),
  ('{落|お}としたコップが（　）、{手|て}をけがしました。', ['{割|わ}れて', 'つまって', '{変|か}わって', '{遅|おく}れて'], 0,
   'Làm rơi cái cốc, cốc vỡ nên bị đứt tay.', 'Cốc, kính, đĩa vỡ ra từng mảnh → 割れる. 壊れる dùng cho máy móc hỏng.', 'tự soạn'),
  ('{旅行|りょこう}の{間|あいだ}、ホテルのフロントに{荷物|にもつ}を（　）。', ['{預|あず}けました', '{返|かえ}しました', '{片付|かたづ}けました', '{乗|の}り{換|か}えました'], 0,
   'Trong chuyến đi, tôi đã gửi hành lý ở quầy lễ tân khách sạn.', '「Nに荷物を預ける」 = gửi đồ cho ai giữ. 返す = trả lại đồ đã mượn.', 'tự soạn')],
 [('{台風|たいふう}が{近|ちか}づいているので、{川|かわ}の{近|ちか}くに{住|す}んでいる{人|ひと}は{早|はや}く（　）してください。', ['{避難|ひなん}', '{点検|てんけん}', '{断水|だんすい}', '{利用|りよう}'], 0,
   'Bão đang đến gần nên ai sống gần sông hãy sơ tán sớm.', '避難する = sơ tán đến nơi an toàn (避難所).', 'tự soạn'),
  ('{停電|ていでん}で{部屋|へや}が{真|ま}っ{暗|くら}です。（　）をつけましょう。', ['{懐中電灯|かいちゅうでんとう}', '{非常食|ひじょうしょく}', '{給水車|きゅうすいしゃ}', '{避難所|ひなんじょ}'], 0,
   'Mất điện nên phòng tối om. Bật đèn pin lên nào.', '「〜をつける」 = bật. Mất điện (停電) → dùng 懐中電灯.', 'tự soạn'),
  ('{地震|じしん}で{建物|たてもの}が{大|おお}きく（　）ら、{机|つくえ}の{下|した}に{入|はい}ってください。', ['{揺|ゆ}れた', '{割|わ}れた', '{逃|に}げた', '{慣|な}れた'], 0,
   'Khi động đất làm toà nhà rung mạnh thì hãy chui xuống gầm bàn.', '地震で揺れる = rung lắc vì động đất. Khi đang rung thì không chạy ra ngoài (逃げる).', 'tự soạn'),
  ('{断水|だんすい}のときは、（　）が{水|みず}を{運|はこ}んで{来|き}ます。ポリタンクを{持|も}って{行|い}きましょう。', ['{給水車|きゅうすいしゃ}', '{救急車|きゅうきゅうしゃ}', '{懐中電灯|かいちゅうでんとう}', '{非常食|ひじょうしょく}'], 0,
   'Khi cúp nước, xe cấp nước sẽ chở nước đến. Hãy mang can nhựa đi.', '給水車 (CẤP THỦY XA) = xe cấp nước. 救急車 = xe cứu thương.', 'tự soạn')],
 [('（　）{暖|あたた}かくなりましたね。', ['だいぶ', 'つよい', 'すごい'], 0,
   'Trời ấm lên nhiều rồi nhỉ.', 'だいぶ + 〜くなりました = đã thay đổi khá nhiều. つよい, すごい không đi trước động từ như vậy.', 'Đề 6 · câu 4'),
  ('もう10{時|じ}ですね。（　）{帰|かえ}りましょうか。', ['そろそろ', 'さっき', 'ちょうど', 'ずっと'], 0,
   'Đã 10 giờ rồi nhỉ. Chúng ta về thôi chứ?', 'そろそろ = đã đến lúc làm gì đó. さっき = lúc nãy (quá khứ).', 'tự soạn'),
  ('{日本|にほん}に{来|き}て{半年|はんとし}です。{仕事|しごと}にもだいぶ（　）きました。', ['{慣|な}れて', '{遅|おく}れて', '{変|か}わって', '{汚|よご}れて'], 0,
   'Sang Nhật được nửa năm. Tôi cũng đã quen với công việc nhiều rồi.', '「Nに慣れる」 = quen với N. 〜てきました = dần dần.', 'tự soạn'),
  ('{楽|たの}しみにしていたコンサートが{中止|ちゅうし}になって、とても（　）です。', ['{残念|ざんねん}', '{心配|しんぱい}', '{新鮮|しんせん}', '{無料|むりょう}'], 0,
   'Buổi hoà nhạc mong chờ bị huỷ, tiếc quá.', '残念 = tiếc (việc đã xảy ra). 心配 = lo (việc sắp tới).', 'tự soạn')],
]

CSS = KGCSS + '''
.vg{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:18px}
.kc.vk{text-align:left;border-top:0;border-left:10px solid #0d5a8c;padding:18px 26px 16px;display:flex;flex-direction:column;gap:6px}
.kc.vk:nth-child(2){border-color:#c42f66}.kc.vk:nth-child(3){border-color:#f2a93b}.kc.vk:nth-child(4){border-color:#5a9e2f}
.vk .wr{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap}
.vk .w{font-family:"Klee One",serif;font-weight:600;font-size:52px;line-height:1.45;color:#0d2b40}.vk .w rt{font-size:.42em;color:#47647a}
.vk .hv{font-size:22px;font-weight:800;color:#c42f66;background:#fdeaf1;border-radius:10px;padding:2px 12px;letter-spacing:.5px}
.vk .lv{margin-left:auto;font-size:18px;color:#8aa0b2;font-weight:700}
.vk .mn{font-size:30px;font-weight:800;color:#0d5a8c}
.vk .vex{margin-top:4px;background:#f4f8fc;border-radius:14px;padding:8px 16px}
.vk .vex .j{font-family:"Klee One",serif;font-weight:600;font-size:25px;line-height:1.85;color:#0d2b40}.vk .vex .j rt{font-size:.5em;color:#6b8296}
.vk .vex .j u{text-decoration:none;border-bottom:3px solid #c42f66}
.vk .vex .v{font-size:20px;color:#55708a;line-height:1.4}
.vk .st{transition:opacity .3s}
.rh{display:flex;align-items:baseline;gap:16px}.rh .no{font-size:30px;color:#c42f66;font-weight:800}
.rh .jp{font-family:"Klee One",serif;font-weight:600;font-size:30px;color:#47647a}
.rmap{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin-top:40px}
.rmap div{background:#fff;border-radius:22px;padding:28px 24px;box-shadow:0 8px 24px #0d2b4012;border-top:8px solid #0d5a8c}
.rmap div:nth-child(2){border-color:#c42f66}.rmap div:nth-child(3){border-color:#f2a93b}.rmap div:nth-child(4){border-color:#5a9e2f}
.rmap b{display:block;font-size:46px;color:#c42f66}.rmap span{display:block;font-size:30px;font-weight:800;color:#0d2b40;margin-top:6px}
.rmap i{display:block;font-style:normal;font-family:"Klee One",serif;font-weight:600;font-size:26px;color:#6b8296;margin-top:4px}
.rmap em{display:block;font-style:normal;font-size:22px;color:#47647a;margin-top:14px}
/* trắc nghiệm (giống Tổng ôn 会話と表現) */
.kw .kk2{font-size:24px}
.kwc{display:flex;gap:34px;margin-top:26px;align-items:flex-start}
.kwl{flex:1;min-width:0}
.dlg{background:#fff;border-radius:20px;padding:22px 32px;box-shadow:0 8px 24px #0d2b4012;font-family:"Klee One",serif;font-weight:600;font-size:36px;line-height:2.1;color:#0d2b40}
.dlg rt{font-size:.46em;color:#47647a}
.blk{display:inline-block;min-width:150px;border-bottom:3px solid #c42f66;margin:0 6px;text-align:center;line-height:1.35;vertical-align:baseline}
.fl{visibility:hidden;color:#2f9e5b}.slide.rv .fl{visibility:visible}
.kw .opts.list{margin-top:22px;gap:14px;max-width:none;grid-template-columns:1fr 1fr}
.kw .opts.list .o{height:74px;padding:0 24px}.kw .o b{font-size:30px}.kw .o .ot{font-size:34px}.kw .o .ot rt{font-size:.46em}
.ex.kx{display:block;visibility:hidden;flex:0 0 470px;margin-top:0;font-size:27px;line-height:1.55;border-left:8px solid #2f9e5b;padding:20px 26px}
.ex.kx.on{visibility:visible}
.kx .a{font-size:30px;font-weight:700;color:#2f9e5b;margin-bottom:10px}.kx .a rt{font-size:.5em}
.kx .lb{font-size:20px;font-weight:700;letter-spacing:1px;color:#6b8296;margin-top:12px}
.kx p{margin:4px 0 0}.kx .g{font-size:25px}
.src{font-size:22px;color:#6b8296;margin-left:12px;font-weight:600}
.qhd{font-size:22px;font-weight:800;color:#fff;background:#c42f66;border-radius:30px;padding:4px 18px;margin-right:12px}
'''
HEADX = HEAD.replace('</style></head>', CSS + '</style></head>', 1)
HEADX = re.sub(r'<title>[^<]*</title>', '<title>Buổi 17 · Từ vựng khó JFT</title>', HEADX, count=1)
CR = '<div class="cr">Khoá cấp tốc JFT · Buổi 17 · Anh Trọng Dạy JFT · Từ vựng và câu ví dụ: 『いろどり 生活の日本語』 ©The Japan Foundation · câu trắc nghiệm ghi “tự soạn” là của lớp</div>'
NUM = '①②③④'
S = []
S.append(f'''<section class="slide dark"><div class="cover"><img class="lg" src="{LOGO}"><div class="kk">KHOÁ CẤP TỐC · BUỔI 17</div>
<h1>Từ vựng khó JFT<br><span>Nâng cao · 48 từ · 30 phút</span></h1></div>{CR}</section>''')
S.append('<section class="slide"><h2>4 chủ đề hôm nay</h2><div class="rmap">' + ''.join(
    f'<div><b>{n}</b><span>{t}</span><i>{rb(j) if "{" in j else j}</i><em>12 từ · 4 câu kiểm tra</em></div>' for n, t, j, _ in ROUNDS) + f'</div>{CR}</section>')

def card(it):
    h, mn = it[0], it[1]
    w = VW[h]
    word = rb(wruby(h, w['y']))
    if len(it) > 2: jp, vi = it[2]
    else:
        jp, vi = V['ex'][w['x']]
        vi = vi or VI_FIX.get(h, '')
    stem = h if not re.search(r'[うくぐすつぬぶむる]$', h) or len(h) < 2 else h[:-1]
    jh = rb(jp)
    # gạch chân từ đang học trong câu (so trên chữ không furigana)
    def ul(m):
        base = re.sub(r'<rt>.*?</rt>|<[^>]+>', '', m.group(0))
        return f'<u>{m.group(0)}</u>' if base and base in h else m.group(0)
    jh = re.sub(r'<ruby>.*?</ruby>', ul, jh) if re.search(r'[一-鿿]', stem) else jh.replace(stem, f'<u>{stem}</u>', 1)
    jh = jh.replace('</u><u>', '')
    lvl = min((l[0], l[1]) for l in w['l'] if l[0] in ('入門', '初級1', '初級2'))
    hv = f'<span class="hv">{w["hv"]}</span>' if w.get('hv') and '-' not in w['hv'] else (f'<span class="hv">{w["hv"].replace(" -", "")}</span>' if w.get('hv') else '')
    return (f'<div class="kc vk"><div class="wr"><span class="w">{word}</span>{hv}<span class="lv">{lvl[0]} · {lvl[1]}</span></div>'
            f'<div class="st"><div class="mn">{e(mn)}</div><div class="vex"><div class="j">{jh}</div><div class="v">{e(vi)}</div></div></div></div>')

for ri, (n, t, j, words) in enumerate(ROUNDS):
    for k in range(3):
        grp = words[k * 4:(k + 1) * 4]
        S.append(f'<section class="slide"><div class="rh"><h2>{n} {t} <small>({k + 1}/3)</small></h2><span class="jp">{rb(j)}</span></div>'
                 f'<div class="vg">' + ''.join(card(it) for it in grp) + f'</div>{CR}</section>')
    for qi, (q, opts, a, vi, gt, src) in enumerate(QZ[ri]):
        ans_txt = rb(opts[a])
        body = rb(q).replace('（　）', f'<span class="blk"><span class="fl">{ans_txt}</span></span>')
        ks = 'abcd'
        ob = ''.join(f'<button class="o" data-k="{ks[i]}"><b>{NUM[i]}</b><span class="jp ot">{rb(o)}</span><i></i><em></em></button>' for i, o in enumerate(opts))
        S.append(f'''<section class="slide qz kw"><div class="kk2"><span class="qhd">Kiểm tra {n}</span>Câu {qi + 1}/4 <span class="src">{src}</span></div>
<div class="kwc"><div class="kwl"><div class="dlg">{body}</div><div class="opts list" data-a="{ks[a]}">{ob}</div></div>
<div class="ex kx"><div class="a">Đáp án {NUM[a]} {ans_txt}</div><div class="lb">DỊCH</div><p>{e(vi)}</p><div class="lb">GIẢI THÍCH</div><p class="g">{rb(e(gt))}</p></div></div>{CR}</section>''')
S.append(f'''<section class="slide dark"><div class="cover"><img class="lg" src="{LOGO}"><div class="kk">おつかれさまでした！</div>
<h1>Hết Buổi 17<br><span>Ôn lại 48 từ trước buổi sau</span></h1></div>{CR}</section>''')
PATCH = "<script>(function(){const a=window.ans;window.ans=function(){a();try{S[cur].classList.add('rv')}catch(e){}}})()</script>"
out = HEADX + ''.join(S) + TAIL.replace('</body>', PATCH + '</body>')
open(R + 'public/tailieu/Buoi17_TuVung_Kho_JFT.html', 'w').write(out)
print(len(S), 'slide', len(out) // 1024, 'KB')
