"""Đề 28 (12/11/2026): đề tổng hợp sát đề thi thật tháng 11 — ghép câu có sẵn trong ngân hàng đề của app
(giữ nguyên ảnh, audio, đáp án, giải thích của câu gốc). Chủ đề theo phản hồi học viên đi thi:
động đất / sơ tán, rủ đi chơi, thông báo ngày giờ, phiếu giảm giá, đọc kanji, にぎやかで / そうです / すぎて.
Chạy: python3 src/jft/tonghop/build_t1.py  rồi  python3 src/build_data.py"""
import json, copy, os
P = os.path.join(os.path.dirname(__file__), '..', '..', 'raw', 'jft_exams.json')
d = json.load(open(P, encoding='utf-8'))
ex = {e['id']: e for e in d}
PICK = {
 # 12/11: theo ảnh anh gửi → lấy đúng các câu đó trong bộ "Ôn tập từ vựng & Hán tự" (jft-vocab) của app
 '文字と語彙': [('vocab',3),('vocab',4),('vocab',6),('vocab',7),('vocab',19),('vocab',58),('vocab',60),('vocab',61),('vocab',62),
               ('vocab',64),('vocab',65),('vocab',66),('vocab',67),('vocab',68),('vocab',69),('vocab',70),'TS1','TS2'],
 '会話と表現': ['TS3','TS4',('f5',16),('g24',17),('f10',23),('f2',15),('y3',20),('f1',21),('f7',19),('f3',16),('y2',16),('y2',19),('f4',20),('y2',13)],
 '聴解': [('f3',34),('f10',30),('f13',33),('f13',34),('f3',32),('f8',31),('f8',32),('f6',35),('f3',40),('f9',26),('f13',31),('f1',35)],
 '読解': [('f7',37),('f6',48),('f7',46),('f9',40),('f10',49),('f10',50),('g18',39),('f2',39),('g24',36),('g24',37),('f10',39),('g16',31)],
}
R = lambda k, r: f'<ruby>{k}<rt>{r}</rt></ruby>'
TS_NOTE = '<div style="margin-top:6px;color:#8a6d1a;font-size:13px">Câu tự soạn (Anh Trọng Dạy JFT) theo dạng câu học viên gặp khi đi thi.</div>'
def TS(s, t, opts, a, dich, gt, tv=''):
    ex = (f'<div class="ans">Đáp án đúng: <span class="jp">{opts[a]}</span></div><span class="lb">DỊCH</span><div>{dich}</div>'
          f'<span class="lb">GIẢI THÍCH</span><div>{gt}</div>' + (f'<span class="lb">TỪ VỰNG</span><ul>{tv}</ul>' if tv else '') + TS_NOTE)
    return {'s': s, 'ins': '', 'gset': None, 'gimg': None, 'gau': None, 't': t, 'imgs': [], 'img': None, 'au': None,
            'o': [{'t': o} for o in opts], 'a': [a], 'ex': ex, 'src': 'Câu tự soạn'}
TSQ = {
 'TS1': TS('文字と語彙', f'この{R("町","まち")}は{R("人","ひと")}が（　　）、{R("静","しず")}かです。',
          [f'{R("少","すく")}なくて', f'{R("高","たか")}くて', f'{R("汚","きたな")}くて', f'{R("寒","さむ")}くて'], 0,
          'Thị trấn này ít người nên yên tĩnh.',
          f'Vế sau là 「{R("静","しず")}かです」 (yên tĩnh) → lý do hợp lý là người ít: 「{R("人","ひと")}が{R("少","すく")}ない」. Tính từ đuôi い nối câu: bỏ い + くて → {R("少","すく")}なくて. Ngược nghĩa: {R("人","ひと")}が{R("多","おお")}い (đông người).',
          f'<li><span class="jp">{R("少","すく")}ない</span> <b>THIỂU</b> – ít</li><li><span class="jp">{R("静","しず")}か</span> <b>TĨNH</b> – yên tĩnh</li>'),
 'TS2': TS('文字と語彙', f'この{R("紙","かみ")}に、{R("名前","なまえ")}と{R("住所","じゅうしょ")}を（　　）ください。',
          [f'{R("記入","きにゅう")}して', f'{R("注文","ちゅうもん")}して', f'{R("説明","せつめい")}して', f'{R("予約","よやく")}して'], 0,
          'Hãy điền tên và địa chỉ vào tờ giấy này.',
          f'Viết thông tin vào giấy/mẫu đơn = 「{R("記入","きにゅう")}する」. {R("注文","ちゅうもん")} = gọi món/đặt hàng, {R("説明","せつめい")} = giải thích, {R("予約","よやく")} = đặt trước.',
          f'<li><span class="jp">{R("記入","きにゅう")}</span> <b>KÝ NHẬP</b> – điền vào</li><li><span class="jp">{R("住所","じゅうしょ")}</span> <b>TRÚ SỞ</b> – địa chỉ</li>'),
 'TS3': TS('会話と表現', f'A：ここは どこですか。<br>B：さくら{R("通","どお")}りです。この あたりは いろいろな {R("店","みせ")}が あって、（　　）、{R("楽","たの")}しいですよ。<br>A：いいですね。{R("行","い")}って みます。',
          ['にぎやかで', 'にぎやかに', 'にぎやかが', 'にぎやかと'], 0,
          'A: Đây là đâu vậy? / B: Phố Sakura. Khu này có nhiều cửa hàng, nhộn nhịp và vui lắm. / A: Hay quá. Tôi sẽ thử đi.',
          f'Nối 2 tính từ (nhộn nhịp + vui): tính từ đuôi な → bỏ な + で: 「にぎやかで、{R("楽","たの")}しい」. 「にぎやかに」 đi với động từ (にぎやかになる), 「が」「と」 không nối tính từ.'),
 'TS4': TS('会話と表現', f'A：{R("日曜日","にちようび")}、いっしょに {R("野球","やきゅう")}を {R("見","み")}に {R("行","い")}きませんか。<br>B：あ、{R("日曜日","にちようび")}は ちょっと……。<br>A：そうですか。じゃあ、また{R("今度","こんど")}。<br><br>B は どう {R("答","こた")}えましたか。',
          [f'{R("問題","もんだい")}ない と{R("答","こた")}えた', 'いいですよ と{R("答","こた")}えた', f'{R("日曜日","にちようび")}は{R("行","い")}けない と{R("答","こた")}えた'], 2,
          'A: Chủ nhật đi xem bóng chày cùng không? / B: À, chủ nhật thì hơi…… / A: Vậy à. Thế để lần sau nhé.',
          f'「〜は ちょっと……」 là cách từ chối nhẹ nhàng của người Nhật, không nói thẳng 「{R("行","い")}けません」. Nghe thấy 「ちょっと……」 ngập ngừng + người kia đáp 「また{R("今度","こんど")}」 (để lần sau) → B không đi được. Nhận lời thì nói 「いいですね」「ぜひ」.'),
}
# 12/11: anh yêu cầu các câu nghe động đất / sơ tán đổi phương án từ tranh sang chữ
K = lambda t: t  # chữ Nhật dễ, có furigana bên dưới
TXT = {
 ('f3', 34): (['f3_489017677_0.jpg'], {'C': f'{R("机","つくえ")}の{R("下","した")}に{R("隠","かく")}れる', 'B': f'{R("揺","ゆ")}れているときに、{R("急","いそ")}いで{R("火","ひ")}を{R("消","け")}しに{R("行","い")}く', 'A': f'{R("部屋","へや")}のドアを{R("開","あ")}ける'},
              'Phương án (trước là tranh): A = mở cửa phòng · B = vội đi tắt bếp lúc đang rung · C = nấp dưới gầm bàn.'),
 ('f13', 33): ([], {'1': f'{R("大","おお")}きい{R("声","こえ")}で「{R("火事","かじ")}だ！」と{R("知","し")}らせる', '2': f'すぐに{R("逃","に")}げる', '3': f'{R("水","みず")}をかけて{R("火","ひ")}を{R("消","け")}す'},
              'Phương án (trước là tranh): 1 = hô to báo mọi người · 2 = chạy ngay · 3 = dội nước dập lửa.'),
 ('f13', 34): ([], {'1': f'{R("会社","かいしゃ")}の{R("建物","たてもの")}の{R("前","まえ")}', '2': f'{R("公園","こうえん")}', '3': f'{R("会社","かいしゃ")}の{R("前","まえ")}の{R("駐車場","ちゅうしゃじょう")}'},
              'Phương án (trước là tranh): 1 = trước tòa nhà công ty · 2 = công viên (chỗ đất trống) · 3 = bãi đỗ xe trước công ty.'),
}
qs = []
for s, L in PICK.items():
    for it in L:
        if isinstance(it, str):
            qs.append(TSQ[it]); continue
        e, n = it
        q = copy.deepcopy(ex['jft-' + e]['qs'][n - 1]); assert q['s'] == s, (e, n)
        q['src'] = f"{ex['jft-'+e]['title']} · câu {n}"
        if (e, n) in TXT:
            keep, mp, note = TXT[(e, n)]
            q['imgs'] = [x for x in q['imgs'] if x.split('/')[-1] in keep]
            for o in q['o']:
                k = o['t'].strip(); o['t'] = f'{k}. {mp[k]}' if k in mp else o['t']
            q['ex'] = q['ex'].replace('</div>', f'</div><div style="margin:4px 0 8px;color:#0d5a8c;font-size:13px">{note}</div>', 1)
        q['t'] = (q.get('t') or '').replace('泊まりした', '泊まりました')  # sửa lỗi gõ ở câu gốc
        qs.append(q)
new = {'id': 'jft-t1', 'group': 'Đề thi thử JFT-Basic', 'title': 'Đề Thảo Linh', 'name': 'Thảo Linh',
       'sub': 'Sát đề thi thật tháng 11 · có phần nghe', 'time': 60, 'tag': 'Sát đề thật', 'qs': qs}
d = [e for e in d if e['id'] != 'jft-t1']
i = next(k for k, e in enumerate(d) if e['id'] == 'jft-y3')
d.insert(i + 1, new)
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Đề Thảo Linh:', len(qs), 'câu')
