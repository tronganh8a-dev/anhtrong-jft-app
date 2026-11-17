"""Tổng ôn TOÀN DIỆN いろどり 入門 (Bài 1–18), không giới hạn thời gian (17/11/2026).
Dùng lại khung tongon_nhapmon_build.py (exec phần định nghĩa) + các trò chơi ôn tập:
  · Thử thách tốc độ: nhìn tranh nói từ (tự chạy, đếm ngược)
  · Đám mây chữ Hán: chỉ ô nào đọc ô đó (số đảo ngẫu nhiên)
  · Điền trợ từ: lật thẻ
  · Sắp xếp câu: bấm các mảnh theo đúng thứ tự
  · Nghe hiểu: câu trong ngân hàng đề của app
Câu trong trò chơi lấy nguyên văn ví dụ 文法ノート いろどり 入門; cách chia mảnh/khoét trợ từ là tự soạn.
Chạy: python3 src/tailieu_src/tongon_nhapmon_full_build.py → public/tailieu/TongOn_NhapMon_ToanDien.html"""
R = '/home/claude/anhtrong-jft-app/'
_src = open(R + 'src/tailieu_src/tongon_nhapmon_build.py').read()
exec(_src[:_src.index('# ---------------- BUỔI 1')])
import random

GAMECSS = '''<style>
.spd{display:grid;grid-template-columns:1fr 360px;gap:30px;align-items:center;flex:1}
.spd .pv{background:#fff;border-radius:26px;height:600px;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px #0d2b401a;position:relative;overflow:hidden}
.spd .pv img{width:auto;height:88%;max-width:94%;object-fit:contain}
.spd .cd{position:absolute;right:18px;top:14px;width:80px;height:80px;border-radius:50%;background:#c42f66;color:#fff;font:800 44px Quicksand,sans-serif;display:flex;align-items:center;justify-content:center}
.spd .side{display:flex;flex-direction:column;gap:16px}.spd .ans{background:#fff;border-radius:22px;padding:22px;min-height:190px;text-align:center;box-shadow:0 8px 24px #0d2b4012}
.spd .ans .w{font-family:"Klee One",serif;font-weight:600;font-size:56px;line-height:1.5}.spd .ans .w rt{font-size:.45em}.spd .ans .m{font-size:28px;color:#c42f66;font-weight:700}
.spd .ans.hid .w,.spd .ans.hid .m{visibility:hidden}.spd .cnt{font:700 24px Quicksand,sans-serif;color:#47647a;text-align:center}
.gbtn{border:0;border-radius:99px;background:#0d5a8c;color:#fff;font:800 26px Quicksand,sans-serif;padding:14px 26px;cursor:pointer}.gbtn.p{background:#c42f66}.gbtn.g{background:#fff;color:#0d5a8c;box-shadow:0 4px 12px #0d5a8c22}
.clw{display:flex;flex-wrap:wrap;gap:22px 26px;justify-content:center;align-content:center;flex:1;padding:6px 10px}
.cld{position:relative;border:0;cursor:pointer;background:#fff;min-width:190px;height:124px;padding:10px 28px;border-radius:80px 90px 70px 85px/70px 60px 80px 65px;box-shadow:0 10px 26px #0d5a8c26,inset 0 -8px 0 #e6f1fb;display:flex;flex-direction:column;align-items:center;justify-content:center;transition:transform .2s}
.cld:nth-child(3n){transform:rotate(-2deg)}.cld:nth-child(3n+1){transform:rotate(2deg) translateY(8px)}.cld:hover{transform:scale(1.06)}
.cld i{position:absolute;left:-10px;top:-12px;width:46px;height:46px;border-radius:50%;background:#c42f66;color:#fff;font:800 24px Quicksand,sans-serif;font-style:normal;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 10px #c42f6655}
.cld .cw{font-family:"Klee One",serif;font-weight:600;font-size:46px;line-height:1.1;color:#0d2b40}
.cld .cr2{display:none;font:800 22px Quicksand,"Klee One",sans-serif;color:#0d5a8c;margin-top:4px}.cld .cr2 small{display:block;font-size:15px;color:#c42f66;letter-spacing:1px}
.cld.on .cr2{display:block}.cld.on{background:#fff8e6}
.shf{margin-left:auto;border:0;border-radius:99px;background:#0d5a8c;color:#fff;font:700 22px Quicksand,sans-serif;padding:8px 22px;cursor:pointer}
.ptc{display:grid;grid-template-columns:1fr 1fr;gap:18px}.ptc button{border:0;background:#fff;border-radius:20px;padding:18px 24px;text-align:left;font-family:"Klee One",serif;font-weight:600;font-size:36px;line-height:1.7;box-shadow:0 8px 22px #0d2b4012;cursor:pointer}
.ptc rt{font-size:.45em}.ptc .bl{display:inline-block;min-width:70px;border-bottom:4px solid #c42f66;text-align:center;color:#c42f66}.ptc .bl span{visibility:hidden}.ptc button.on .bl span{visibility:visible}.ptc button.on{background:#fff8e6}
.ptc small{display:block;font:600 20px Quicksand,sans-serif;color:#47647a;line-height:1.3}
.ord{display:flex;flex-direction:column;gap:22px;flex:1;justify-content:center}.ord .vi{font-size:30px;color:#0d5a8c;font-weight:700}
.ord .line{min-height:96px;background:#fff;border-radius:22px;border:3px dashed #9fb6c8;display:flex;flex-wrap:wrap;gap:12px;padding:14px;align-items:center}
.ord .line.ok{border:3px solid #2f9e5b;background:#e6f6ec}.ord .line.ng{border:3px solid #e0245e;background:#fdecef}
.ord .pool{display:flex;flex-wrap:wrap;gap:14px}.chk{border:0;border-radius:16px;background:#fff;box-shadow:0 6px 16px #0d2b4018;font-family:"Klee One",serif;font-weight:600;font-size:38px;padding:10px 20px;cursor:pointer;line-height:1.5}.chk rt{font-size:.45em}
.line .chk{background:#eaf3fb}.ord .bar{display:flex;gap:14px}.ord .sol{display:none;font-family:"Klee One",serif;font-weight:600;font-size:36px;color:#2f9e5b}.ord .sol rt{font-size:.45em}.ord.show .sol{display:block}
.ls .lpic{max-height:470px}
</style>'''
GAMEJS = '''<script>
(()=>{const sh=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
/* đám mây */
window.cloudMix=s=>{const w=s.querySelector('.clw');const a=sh([...w.children]);a.forEach(x=>{x.classList.remove('on');w.appendChild(x)});const n=sh(a.map((_,i)=>i+1));a.forEach((x,i)=>x.querySelector('i').textContent=n[i])};
document.querySelectorAll('.clw').forEach(w=>{cloudMix(w.closest('.slide'));w.querySelectorAll('.cld').forEach(c=>c.onclick=e=>{e.stopPropagation();c.classList.toggle('on')})});
/* trợ từ */
document.querySelectorAll('.ptc button').forEach(b=>b.onclick=e=>{e.stopPropagation();b.classList.toggle('on')});
/* sắp xếp câu */
document.querySelectorAll('.ord').forEach(o=>{const pool=o.querySelector('.pool'),line=o.querySelector('.line');
 const reset=()=>{o.classList.remove('show');line.className='line';const cs=[...o.querySelectorAll('.chk')];sh(cs).forEach(c=>pool.appendChild(c))};
 o.querySelectorAll('.chk').forEach(c=>c.onclick=e=>{e.stopPropagation();(c.parentNode===pool?line:pool).appendChild(c);line.className='line'});
 o.querySelector('[data-a=ck]').onclick=e=>{e.stopPropagation();const got=[...line.children].map(c=>c.dataset.i).join(',');const need=[...o.querySelectorAll('.chk')].map(c=>+c.dataset.i).sort((a,b)=>a-b).join(',');line.className='line '+(got===need?'ok':'ng')};
 o.querySelector('[data-a=sh]').onclick=e=>{e.stopPropagation();o.classList.add('show')};o.querySelector('[data-a=rs]').onclick=e=>{e.stopPropagation();reset()};reset()});
/* thử thách tốc độ */
document.querySelectorAll('.spd').forEach(g=>{const D=JSON.parse(g.dataset.d);let ord=[],k=-1,tm=null,t=0,run=false;const im=g.querySelector('.pv img'),cd=g.querySelector('.cd'),an=g.querySelector('.ans'),cn=g.querySelector('.cnt');
 const showK=()=>{const d=D[ord[k]];im.src=d.i;an.querySelector('.w').innerHTML=d.w;an.querySelector('.m').textContent=d.m;an.classList.add('hid');cn.textContent=(k+1)+' / '+ord.length};
 const tick=()=>{if(!run)return;t--;cd.textContent=Math.max(t,0);if(t===0){an.classList.remove('hid')}if(t<=-2){next();return}tm=setTimeout(tick,1000)};
 const next=()=>{clearTimeout(tm);if(k+1>=ord.length){run=false;cd.textContent='🎉';return}k++;showK();t=+g.dataset.s;cd.textContent=t;if(run)tm=setTimeout(tick,1000)};
 const start=()=>{ord=sh(D.map((_,i)=>i));k=-1;run=true;next()};
 g.querySelector('[data-a=go]').onclick=e=>{e.stopPropagation();start()};
 g.querySelector('[data-a=ps]').onclick=e=>{e.stopPropagation();run=!run;if(run)tm=setTimeout(tick,1000);else clearTimeout(tm)};
 g.querySelector('[data-a=nx]').onclick=e=>{e.stopPropagation();if(an.classList.contains('hid')){an.classList.remove('hid')}else next()};
 ord=D.map((_,i)=>i);k=0;showK();cd.textContent=g.dataset.s});
})();</script>'''

def speed(S, sl, words, title, sec=4):
    D = [{'i': img(w['img'], 420), 'w': w['wr'], 'm': w['vi']} for w in words]
    sl(f'Thử thách tốc độ <small>{title} · nhìn tranh, nói từ trước khi hết giờ</small>',
       f'<div class="spd" data-s="{sec}" data-d="{html.escape(json.dumps(D, ensure_ascii=False))}"><div class="pv"><img><div class="cd"></div></div>'
       '<div class="side"><div class="ans hid"><div class="w"></div><div class="m"></div></div><div class="cnt"></div>'
       '<button class="gbtn p" data-a="go">▶ Bắt đầu</button><button class="gbtn g" data-a="ps">⏸ Dừng / chạy tiếp</button><button class="gbtn" data-a="nx">⏭ Đáp án / câu sau</button></div></div>')

def cloud(sl, words, title):
    cl = ''.join(f'<button class="cld"><i></i><span class="cw">{html.escape(k["w"])}</span><span class="cr2">{html.escape(k["r"])}<small>{html.escape(k["hv"])}</small></span></button>' for k in words)
    sl(f'Đám mây chữ Hán <small>{title} · chỉ ô nào – đọc ô đó</small> <button class="shf" onclick="cloudMix(this.closest(&quot;.slide&quot;))">🔀 Đảo lại</button>', f'<div class="clw">{cl}</div>')

def particles(sl, items, title):
    cards = ''
    for a, p, b, vi in items:
        cards += f'<button>{J(a)}<span class="bl"><span>{p}</span></span>{J(b)}<small>{vi}</small></button>'
    sl(f'Điền trợ từ <small>{title} · bấm thẻ để lật đáp án</small>', f'<div class="ptc">{cards}</div>')

def order(sl, chunks, vi, n):
    ch = ''.join(f'<button class="chk" data-i="{i}">{J(c)}</button>' for i, c in enumerate(chunks))
    sl(f'Sắp xếp câu {n} <small>Bấm các mảnh theo đúng thứ tự · câu trong 文法ノート いろどり 入門</small>',
       f'<div class="ord"><div class="vi">🇻🇳 {html.escape(vi)}</div><div class="line"></div><div class="pool">{ch}</div>'
       f'<div class="bar"><button class="gbtn" data-a="ck">✔ Kiểm tra</button><button class="gbtn g" data-a="sh">👀 Đáp án</button><button class="gbtn g" data-a="rs">↺ Làm lại</button></div><div class="sol">{J("".join(chunks))}</div></div>')

KANJI = [(['名前', '国', '私', '日本', '家'], 'Bản thân · nhà'), (['父', '母', '子ども', '水', '好き'], 'Gia đình · sở thích'), (['食べます', '飲みます', '魚', '肉'], 'Ăn uống'),
         (['新しい', '広い', '古い'], 'Tính từ'), (['上', '下', '中'], 'Vị trí'), (['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日'], 'Thứ trong tuần'),
         (['朝', '昼', '夜', '時', '分'], 'Thời gian'), (['読みます', '聞きます', '見ます', '本', '友だち'], 'Hoạt động'), (['何', '年', '月', '日', '今日'], 'Ngày tháng'),
         (['今週', '今度', '来週', '休み', '予定'], 'Lịch hẹn'), (['東', '南', '会社', '来ます', '行きます'], 'Đi lại'), (['乗ります', '会います', '入ります', '買います', '旅行します'], 'Động từ'),
         (['大きい', '小さい', '高い', '低い', '安い'], 'Tính từ'), (['前', '後ろ', '横', '入口', '出口'], 'Vị trí · lối đi'), (['階', '押す', '引く', '映画', '温泉'], 'Toà nhà · giải trí'),
         (['一、二、三、四、五、六、七、八、九、十', '百', '千', '万', '円'], 'Số đếm · tiền'), (['日本語', '勉強します'], 'Học tập')]
GSEL = [(3, ['❶', '❷', '❸', '❹', '❺', '❻'], {'❺': 'も thay cho は'}), (4, ['❶', '❷', '❸', '❹'], {}), (5, ['❶', '❷', '❸', '❹', '❺', '❻'], {'❷': 'Từ chối nhẹ nhàng, không nói hết câu'}),
        (6, ['❶', '❷', '❸', '❹'], {}), (7, ['❶', '❷', '❸', '❹', '❺'], {}), (8, ['❶', '❷', '❸', '❹', '❺'], {}), (9, ['❶', '❷', '❸'], {'❶': 'Giờ chính xác + に · khoảng giờ + ごろ'}),
        (10, ['❶', '❷', '❸'], {'❶': 'Thể て: học kỹ ở 初級1'}), (11, ['❶', '❷', '❸', '❹', '❺'], {}), (12, ['❶', '❸', '❹', '❺', '❷'], {'❶': 'Nơi diễn ra sự kiện dùng で'}),
        (13, ['❶', '❷', '❸', '❹', '❺', '❻'], {}), (14, ['❶', '❷', '❸'], {'❸': 'な-A + な + N · い-A + N'}), (15, ['❶', '❷'], {}), (16, ['❶', '❷', '❸'], {}),
        (17, ['❶', '❷', '❸', '❹', '❺'], {'❸': 'いい → よかったです'}), (18, ['❶', '❷', '❸', '❹', '❺', '❻'], {'❶': 'Bỏ ます + たいです'})]
QG = [(3, '❺', 0), (4, '❸', 0), (5, '❹', 0), (6, '❶', 0), (7, '❺', 0), (8, '❷', 0), (9, '❷', 0), (10, '❶', 0), (11, '❹', 0), (12, '❸', 0), (13, '❸', 0), (14, '❸', 0), (15, '❶', 0), (16, '❷', 0), (17, '❸', 0), (18, '❶', 0)]
LISTEN = [('jft-f10', 31), ('jft-y1', 27), ('jft-ln1', 7), ('jft-f5', 31), ('jft-f7', 24), ('jft-y3', 27), ('jft-y2', 27), ('jft-ln1', 18), ('jft-ln1', 19)]

def _tables():
    src = _src[_src.index('tab1 = {'):_src.index("build(1, range(1, 10)")]
    src2 = _src[_src.index('tab2 = {'):_src.index("build(2, range(10, 19)")]
    g = {}; exec(src, globals(), g); exec(src2, globals(), g)
    t = dict(g['tab1']); t.update(g['tab2']); return t
TABLES = _tables()

def h_vocab(S, sl, quiz, CR):
    sl('', '<div class="sec"><div class="n">🎮</div><div class="t">Trò chơi từ vựng</div><div class="j">ゲーム</div><div class="d">Thử thách tốc độ · nhìn tranh nói từ</div></div>')
    rnd = random.Random(7)
    pool1 = [w for w in VOC if w.get('img') and w['b'] <= 9]; pool2 = [w for w in VOC if w.get('img') and w['b'] >= 10]
    speed(S, sl, rnd.sample(pool1, 15), 'Bài 4–9', 4)
    speed(S, sl, rnd.sample(pool2, 15), 'Bài 10–18', 4)
    qs = [w for w in VOC if w.get('rd') and w.get('img')]
    for n, w in enumerate(random.Random(11).sample(qs, 6)):
        o = [w['r']] + w['rd'][:3]; k = n % 4; o = o[k:] + o[:k]
        quiz('Nhìn tranh, chọn cách đọc đúng.', [html.escape(x) for x in o], o.index(w['r']), f'<span class="jp">{w["wr"]}</span> – {html.escape(w["vi"])}', f'Từ vựng いろどり 入門 Bài {w["b"]}', pic=img(w['img']))
def h_kanji(S, sl, quiz, CR):
    KK = {k['w']: k for k in KAN}
    w1 = [KK[w] for g, _ in KANJI[:7] for w in g if w in KK and '、' not in w and '曜日' not in w][:16]
    w2 = [KK[w] for g, _ in KANJI[7:] for w in g if w in KK and '、' not in w]
    random.Random(3).shuffle(w2)
    cloud(sl, w1, 'Bài 1–9'); cloud(sl, w2[:16], 'Bài 10–18 (1)'); cloud(sl, w2[16:32], 'Bài 10–18 (2)')
def h_gram(S, sl, quiz, CR):
    sl('', '<div class="sec"><div class="n">🎮</div><div class="t">Trò chơi ngữ pháp</div><div class="j">ゲーム</div><div class="d">Điền trợ từ · Sắp xếp câu</div></div>')
    particles(sl, [('肉と野菜', 'が', '好きです。', 'Tôi thích thịt và rau.'), ('シリアル', 'を', '食べます。', 'Tôi ăn ngũ cốc.'), ('田中さんは倉庫', 'に', 'います。', 'Anh Tanaka ở trong kho.'),
                   ('ブラジル', 'から', '来ました。', 'Tôi đến từ Brazil.'), ('夫と公園', 'で', 'テニスをします。', 'Tôi chơi tennis cùng chồng ở công viên.'), ('バイク', 'で', '来ます。', 'Tôi đến bằng xe máy.'),
                   ('京都', 'へ', '行きたいです。', 'Tôi muốn đi Kyoto.'), ('ケマラさん', 'も', '、ベトナムからですか？', 'Chị Khemera cũng đến từ Việt Nam à?')], 'Bài 3–18')
    for n, (ch, vi) in enumerate([(['家族は、', 'フィリピンに', '住んでいます。'], 'Gia đình tôi sống ở Philippines.'), (['私は、', '朝ご飯は、', 'あまり', '食べません。'], 'Tôi không mấy khi ăn sáng.'),
                                   (['生ビール3つと、', 'ウーロン茶1つ、', 'お願いします。'], 'Cho tôi 3 bia tươi và 1 trà ô long.'), (['12時から', '1時まで', '昼休みです。'], 'Nghỉ trưa từ 12 giờ đến 1 giờ.'),
                                   (['休みの日は、', 'たいてい、', '映画を', '見ます。'], 'Ngày nghỉ tôi thường xem phim.'), (['ここから、', '12番の', 'バスに', '乗ります。'], 'Từ đây lên xe buýt số 12.'),
                                   (['週末は、', '何も', 'しませんでした。'], 'Cuối tuần tôi đã không làm gì cả.')], 1):
        order(sl, ch, vi, n)

build(0, range(1, 19), 'Tổng ôn toàn diện', 'いろどり 入門 · Bài 1 – 18', KANJI, GSEL, TABLES, QG,
      [('📚', 'Từ vựng', 'Bài 4–18 có tranh + thử thách tốc độ'), ('✍', 'Chữ Hán', 'Từng chữ có nét viết + đám mây đọc chữ'), ('🧩', 'Ngữ pháp', 'Bài 3–18, bảng tổng hợp, điền trợ từ, sắp xếp câu'), ('🎧', 'Nghe hiểu', '10 câu nghe trong bộ đề app')],
      '<div class="kgr g2"><div class="kcd kb"><h3>Đã ôn</h3><ul class="ck"><li>Câu danh từ · động từ ます · tính từ な/い</li><li>あります・います · vị trí · giờ</li><li>て-ください · rủ rê · trợ từ に/で/へ/を</li><li>こそあど · quá khứ · たい · từ nối câu</li></ul></div>'
      '<div class="kcd kp"><h3>Tự ôn trên app</h3><ul class="ck"><li>Tài liệu → Từ vựng · Chữ Hán 入門</li><li>Tài liệu → Ngữ pháp 入門: worksheet</li><li>Làm đề: phần 会話と表現</li></ul></div></div>',
      'TongOn_NhapMon_ToanDien.html', False, LISTEN,
      hooks={'vocab': h_vocab, 'kanji': h_kanji, 'gram': h_gram}, extra_js=GAMECSS + GAMEJS, label='Toàn diện', coverp='Từ vựng · Chữ Hán · Ngữ pháp · Nghe · Trò chơi ôn tập')
