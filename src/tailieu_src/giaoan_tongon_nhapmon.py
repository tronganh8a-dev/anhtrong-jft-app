"""Giáo án (lời giảng theo trình tự slide) cho TongOn_NhapMon_ToanDien.html — 17/11/2026.
Bước 1: node /tmp/ga/ex.js  (trích cấu trúc từng slide → /tmp/ga/slides.json)
Bước 2: python3 src/tailieu_src/giaoan_tongon_nhapmon.py → /tmp/ga/ga.html → PDF (playwright)
Dữ liệu: DOCS (từ vựng, chữ Hán), 文法ノート いろどり 入門 (giải thích, ví dụ), bộ đề app (nghe).
Phần "Lời giảng", "Nhấn mạnh", hướng dẫn trò chơi là tự soạn."""
import json, html, re
R = '/home/claude/anhtrong-jft-app/'
_src = open(R + 'src/tailieu_src/tongon_nhapmon_build.py').read()
exec(_src[:_src.index('# ---------------- BUỔI 1')])
SL = json.load(open('/tmp/ga/slides.json'))
VW = {}
for w in VOC: VW.setdefault(w['w'], w)
KK = {k['w']: k for k in KAN}
E = html.escape
def rb(s): return RB(s)

# ---------- ghi chú tự soạn ----------
VNOTE = {
 4: ('Gia đình', ['Đây là cách gọi <b>gia đình mình</b> khi kể với người ngoài: 父・母・兄・姉・弟・妹・夫・妻. Khi nói về gia đình <b>người khác</b> thì dùng dạng kính trọng: お父さん・お母さん・お兄さん・お姉さん・弟さん・妹さん・ご主人・奥さん. Ở trình độ này học viên chỉ cần nghe hiểu dạng kính trọng.',
      '兄・姉 (anh, chị) và 弟・妹 (em trai, em gái): tiếng Việt chỉ có "em", tiếng Nhật tách theo trai/gái nên nhắc học viên nhìn tranh để phân biệt.',
      '私 đọc わたし. 子ども viết chữ ども bằng hiragana là cách viết của sách いろどり.']),
 5: ('Món ăn Nhật', ['Phần lớn là món quen thuộc học viên sẽ gặp khi sống ở Nhật, đề JFT hay dùng làm tranh lựa chọn.',
      '刺身 (cá sống thái lát) khác 寿司 (cơm nắm có cá). 牛丼 = 牛 (bò) + 丼 (tô cơm). 蕎麦 thường viết bằng hiragana そば trên biển quán.',
      'Ôn luôn mẫu 「Nが好きです」 / 「Nはちょっと…」 của Bài 5 khi hỏi học viên thích món nào.']),
 6: ('Gọi món đồ ăn nhanh', ['Toàn bộ là từ katakana gốc tiếng Anh. Cho học viên đọc to và chú ý 2 điểm: trường âm 「ー」 (ハンバーガー, アイスクリーム) và っ nhỏ (フィッシュ, アップル).',
      'Gọi món dùng 「〜、ください」 hoặc 「〜、お願いします」, kèm số lượng 「ひとつ・ふたつ…」 (ngữ pháp Bài 6).']),
 7: ('Nhà ở', ['お風呂 có お ở đầu cho lịch sự, người Nhật hầu như luôn nói お風呂.',
      'Nhiều từ có 2 cách nói: 台所 / キッチン, 居間 / リビング, ベランダ / バルコニー. Đề thi có thể dùng cả hai nên học viên cần nhận ra cả hai.',
      'Dùng với mẫu Bài 7: 「部屋が4つあります」「お風呂があります」.']),
 8: ('Nơi làm việc · vị trí', ['更衣室 (phòng thay đồ), 給湯室 (phòng pha trà, lấy nước nóng), 喫煙所 (khu hút thuốc) là biển báo hay gặp ở công ty và trong đề JFT phần đọc thông tin.',
      'Từ vị trí 上・下・中・横 luôn đi sau 「Nの」: 机の上, かばんの中. Nhấn mạnh thứ tự ngược với tiếng Việt: "trên bàn" → 机の上.']),
 9: ('Thời gian', ['午前 / 午後 đứng <b>trước</b> giờ: 午前9時, 午後3時.',
      'Giờ đọc đặc biệt: 4時 よじ, 7時 しちじ, 9時 くじ. Phút: 1分 いっぷん, 3分 さんぷん, 4分 よんぷん, 6分 ろっぷん, 8分 はっぷん, 10分 じゅっぷん; còn lại ふん.',
      'Thứ trong tuần: 月(Mặt Trăng)・火(Lửa)・水(Nước)・木(Cây)・金(Vàng)・土(Đất)・日(Mặt Trời) + 曜日.']),
 10: ('Đồ dùng văn phòng', ['貸します = cho (người khác) mượn. Muốn nhờ người khác cho mình mượn thì nói 「貸してください」. Đừng nhầm với 借ります (mình đi mượn).',
      'ホチキス (dập ghim), ふせん (giấy nhớ), のり (keo dán) là tên gọi riêng ở Nhật, học viên Việt hay không biết.']),
 11: ('Hoạt động thường ngày', ['Hầu hết là cụm 「Nをします」 hoặc 「Nを + động từ」. Nhấn mạnh trợ từ を chỉ đối tượng của hành động.',
      'Ghép với từ chỉ tần suất của Bài 11: いつも・よく・ときどき + 〜ます, あまり・ぜんぜん + 〜ません.']),
 12: ('Sự kiện · rủ rê', ['飲み会 (buổi nhậu), 忘年会 (tiệc tất niên cuối năm ở công ty), 夏祭り (lễ hội mùa hè) là sự kiện học viên chắc chắn gặp ở Nhật.',
      'Rủ nhau dùng 「〜に行きませんか」 (Bài 12). Nơi diễn ra sự kiện đi với で: 公園で夏祭りがあります.']),
 13: ('Phương tiện đi lại', ['Đi bằng phương tiện dùng で: 電車で来ます, バスで行きます. Ngoại lệ: <b>歩いて</b> (đi bộ) không có で.',
      'Lên xe: 「Nに乗ります」, xuống xe: 「Nを降ります」 (Bài 13). 地下鉄 = 地下 (dưới đất) + 鉄 (sắt).']),
 14: ('Ở nhà ga · khu phố', ['Đây là các biển báo hay xuất hiện trong phần đọc thông tin của JFT: コインロッカー, 自動販売機, 改札, インフォメーション, 商店街.',
      'Hỏi chỗ: 「この近くに、Nはありますか？」 (Bài 14).']),
 15: ('Cửa hàng', ['Dạy theo câu hỏi "mua X ở đâu": 電池 → コンビニ / 100円ショップ; thuốc → ドラッグストア; đồ dùng nhà cửa → ホームセンター; 浴衣 → デパート.',
      'Mẫu Bài 15: 「Nがほしいんですが…」 để nhờ nhân viên tư vấn.']),
 16: ('Tiền Nhật', ['Đọc giá là phần học viên hay sai: 100 ひゃく, 300 さんびゃく, 600 ろっぴゃく, 800 はっぴゃく; 1,000 せん, 3,000 さんぜん, 8,000 はっせん; 10,000 いちまん.',
      'Cho học viên cầm tiền thật hoặc nhìn tranh và đọc to. Hỏi giá dùng 「これ、いくらですか？」 (Bài 16).']),
 17: ('Việc đã làm cuối tuần', ['Toàn bộ ở thể quá khứ 〜ました. Ôn lại cách đổi: 〜ます → 〜ました, 〜ません → 〜ませんでした (Bài 17).',
      '飲みに行きました: V bỏ ます + に行きます = đi để làm V (Bài 12).']),
 18: ('Điều muốn làm', ['〜たいです = muốn làm. Cách chia: bỏ ます + たいです (行きます → 行きたいです).',
      'Chú ý trợ từ: 富士山<b>に</b>登りたい, 京都<b>へ</b>行きたい, 雪<b>が</b>見たい (với たい có thể dùng が thay を).']),
}
GNOTE = {
 (3, '❶'): 'Mẫu câu đầu tiên của tiếng Nhật: 「AはBです」. Nhấn mạnh 「は」 đọc là <b>wa</b>, không đọc ha.',
 (3, '❷'): 'から = từ (nơi xuất phát). Dùng khi giới thiệu quê: 「ベトナムから来ました」.',
 (3, '❹'): 'Câu hỏi chỉ cần thêm か ở cuối và lên giọng. Không cần đảo trật tự từ như tiếng Anh.',
 (3, '❺'): 'も thay vào chỗ của は (không đứng cùng は): 「私もベトナム人です」.',
 (3, '❻'): 'Phủ định của です là じゃないです (văn nói) / ではありません (trang trọng hơn).',
 (4, '❸'): 'Nơi sống dùng に + 住んでいます. Học viên hay nói nhầm 「で住んでいます」.',
 (4, '❹'): 'の nối 2 danh từ, thứ tự ngược tiếng Việt: 「私の母」 = mẹ của tôi.',
 (5, '❶'): 'Thích dùng が, không dùng を: 「うどんが好きです」. Đây là lỗi học viên hay mắc.',
 (5, '❷'): 'Người Nhật ít khi nói thẳng "không thích". 「ちょっと…」 bỏ lửng là cách từ chối nhẹ nhàng, rất hay gặp trong đề hội thoại JFT.',
 (5, '❹'): 'を chỉ đối tượng của hành động: 「ごはんを食べます」. を đọc là <b>o</b>.',
 (5, '❻'): 'Tần suất: いつも, よく đi với khẳng định; あまり đi với phủ định 〜ません.',
 (6, '❸'): 'Số lượng đứng sau danh từ: 「コーヒー、ふたつ」. Đếm đồ vật: ひとつ, ふたつ, みっつ…',
 (7, '❷'): '「場所にNがあります」: nơi chốn + に, vật + が. Số lượng đứng ngay trước あります.',
 (7, '❹'): 'Tính từ đuôi い giữ い + です; tính từ đuôi な bỏ な + です. きれい là な-A.',
 (7, '❺'): 'Phủ định: い-A → bỏ い + くないです (広くないです); な-A → じゃないです. Đặc biệt いい → よくないです.',
 (8, '❶'): 'Nơi diễn ra hành động dùng で, khác với nơi tồn tại dùng に. So sánh: 「食堂で食べます」 / 「食堂にいます」.',
 (8, '❷'): 'Người, con vật dùng います; đồ vật dùng あります. Đây là cặp học viên dễ nhầm nhất ở 入門.',
 (9, '❶'): 'Giờ chính xác + に (8時に起きます); khoảng giờ + ごろ, thường bỏ に (8時ごろ起きます).',
 (9, '❷'): 'から〜まで = từ… đến…, dùng cho cả thời gian và nơi chốn.',
 (10, '❶'): 'Thể て sẽ học kỹ ở 初級1; ở đây chỉ cần nhớ cả cụm 「〜てください」 để nhờ người khác.',
 (11, '❷'): 'どんな + N để hỏi tính chất, loại: 「どんな映画が好きですか」.',
 (12, '❸'): 'Rủ rê lịch sự: 〜ませんか. Đồng ý: 「いいですね」, từ chối: 「すみません、ちょっと…」.',
 (12, '❺'): 'Bỏ ます + に行きます = đi để làm gì: 「飲みに行きます」「買い物に行きます」.',
 (13, '❸'): 'Phương tiện + で. Đi bộ là 歩いて, không có で.',
 (13, '❺'): 'Lên xe: Nに乗ります; xuống xe: Nを降ります. Hai trợ từ khác nhau, đề hay hỏi.',
 (14, '❸'): 'Tính từ bổ nghĩa danh từ: い-A giữ nguyên (高いビル), な-A thêm な (きれいな公園).',
 (16, '❷'): 'この / その / あの phải có danh từ đi sau; これ / それ / あれ đứng một mình.',
 (17, '❶'): 'Quá khứ: 〜ました / 〜ませんでした. Đây là nền tảng cho phần hội thoại về cuối tuần trong đề.',
 (17, '❸'): 'Quá khứ tính từ: い-A → 〜かったです (楽しかったです); な-A → 〜でした. いい → よかったです.',
 (18, '❶'): 'Bỏ ます + たいです. Dùng để nói mong muốn của bản thân, không dùng để hỏi trực tiếp mong muốn của người trên.',
 (18, '❷'): 'どこか (đâu đó) dùng trong câu khẳng định / câu hỏi; どこにも + phủ định = không đi đâu cả.',
}
TNOTE = 'Bảng tổng hợp này là phần em tự soạn để chốt kiến thức. Anh cho học viên đọc to từng dòng, sau đó che cột đáp án (dùng bút che hoặc Memo) để học viên tự nói lại.'

# ---------- dựng ----------
B = []
def blk(n, title, body, kind=''):
    B.append(f'<section class="b {kind}"><div class="hd"><span class="sn">{n}</span><span class="tt">{title}</span></div>{body}</section>')
cur_bai = None
for s in SL:
    n = f'Slide {s["i"]}'; t = s['t']
    if t == 'cover':
        if s['i'] == 1: continue
        cls = 'part pb' if 'PHẦN' in s['txt'] else 'part'
        B.append(f'<div class="{cls}"><span class="sn2">{n}</span> {E(s["txt"]).replace(chr(10), " · ")}</div>')
    elif t == 'sec':
        blk(n, E(s['txt']), f'<p class="op">Slide chuyển phần: {E(s.get("d", ""))}. Nói ngắn gọn mục tiêu phần này rồi sang slide sau.</p>', 'sec')
    elif t == 'vocab':
        b = int(re.search(r'Bài (\d+)', s['h2']).group(1)); g = GB.get(b)
        head, notes = VNOTE.get(b, ('', []))
        rows = ''
        for w in s['w']:
            v = VW.get(w) or next((x for x in VOC if x['r'] == w or x['w'].replace(' ', '') == w.replace(' ', '')), None)
            if not v: rows += f'<tr><td class="jw">{E(w)}</td><td colspan="3"></td></tr>'; continue
            ex = v.get('ex'); exs = f'<div class="exj">{rb(ex[0])}</div><div class="exv">{E(ex[1])}</div>' if ex else ''
            rows += f'<tr><td class="jw">{v["wr"]}</td><td>{E(v["r"])}</td><td><b>{E(v["vi"])}</b>{("<br><small>HV: " + E(v["hv"]) + "</small>") if v.get("hv") else ""}</td><td>{exs}</td></tr>'
        blk(n, f'Từ vựng · Bài {b} {rb(g["title"]) if g else ""} <small>{E(g["title_vi"]) if g else ""}</small>',
            '<p class="op">Thao tác: mở slide chỉ thấy tranh → học viên đoán → bấm lần 1 hiện tiếng Nhật (cả lớp đọc to 2 lần) → bấm lần 2 hiện nghĩa.</p>'
            f'<div class="lg"><b>Chủ đề: {head}</b><ul>' + ''.join(f'<li>{x}</li>' for x in notes) + '</ul></div>'
            f'<table class="vt"><tr><th>Từ</th><th>Cách đọc</th><th>Nghĩa</th><th>Ví dụ (sách)</th></tr>{rows}</table>')
    elif t == 'kanji':
        k = KK.get(s['w']);
        if not k: continue
        chars = ''.join(f'<li><b class="kc">{E(c["k"])}</b> <span class="hv">{E(c["hv"])}</span> · On: {E(c.get("on") or "–")} · Kun: {E(c.get("kun") or "–")} · nghĩa: {E(c.get("vi") or "")}</li>' for c in k['chars'])
        tip = re.sub(r'^\s*(Mẹo nhớ|Mẹo|Ghi nhớ)\s*:\s*', '', k.get('tip') or '')
        rl = rel(k['w']); rl = re.sub(r'<b>Từ liên quan</b>', '', rl).replace('class="krel st"', 'class="krel"')
        ex = k.get('ex') or {}
        blk(n, f'Chữ Hán · <span class="jbig">{E(k["w"])}</span> <span class="hv">{E(k["hv"])}</span>',
            '<p class="op">Thao tác: slide mở ra nét viết tự chạy — cho học viên viết theo trên giấy. Bấm "Chậm" nếu chữ nhiều nét. Sau đó bấm lần lượt: cách đọc → bảng từng chữ → cách nhớ → ví dụ.</p>'
            f'<div class="lg"><p><b>Lời giảng:</b> Từ 「{E(k["w"])}」 đọc là <b>{E(k["r"])}</b>, nghĩa là <b>{E(k["vi"])}</b>, âm Hán Việt <b>{E(k["hv"])}</b>.</p><ul>{chars}</ul>'
            + (f'<p><b>Cách nhớ:</b> {E(tip)}</p>' if tip else '')
            + (f'<p><b>Ví dụ:</b> <span class="jp">{ex["jp"]}</span> — {E(ex.get("vi", ""))}</p>' if ex.get('jp') else '')
            + (f'<p><b>Từ liên quan (mở rộng):</b></p>{rl}' if rl else '') + '</div>')
    elif t == 'kgrid':
        NUM = next((k for k in KK if '、' in k), None)
        ks = [KK[NUM] if w == '一〜十' and NUM else KK[w] for w in s['w'] if w in KK or (w == '一〜十' and NUM)]
        rows = ''.join(f'<tr><td class="jw">{E(k["w"] if "、" not in k["w"] else "一〜十")}</td><td>{E(k["r"])}</td><td>{E(k["hv"])}</td><td>{E(k["vi"])}</td></tr>' for k in ks) if ks else ''.join(f'<tr><td class="jw">{E(w)}</td></tr>' for w in s['w'])
        blk(n, f'Chữ Hán · {E(s["h2"])}', '<p class="op">Thao tác: bấm từng thẻ để hiện cách đọc; nút ✍ Nét trên mỗi thẻ mở nét viết.</p>'
            '<div class="lg"><p>Dạy theo nhóm: cho học viên tìm điểm chung (cùng có 曜日 / cùng là số đếm), rồi đọc nhanh theo thứ tự và đảo thứ tự.</p></div>'
            f'<table class="vt"><tr><th>Chữ</th><th>Cách đọc</th><th>Hán Việt</th><th>Nghĩa</th></tr>{rows}</table>')
    elif t == 'gram':
        b = int(re.search(r'Bài (\d+)', s['h2']).group(1)); g = GB[b]
        body = '<p class="op">Thao tác: mỗi khối là 1 mẫu câu; câu ví dụ hiện trước, bấm để hiện nghĩa tiếng Việt.</p>'
        for no in s['no']:
            p = next(x for x in g['points'] if x['no'] == no)
            exs = ''.join(f'<li><span class="jp">{rb(e["jp"])}</span><br><small>{E(e["vi"])}</small></li>' for e in p['examples'] + p.get('more_examples', []))
            body += (f'<div class="gp"><div class="gpt">{E(no)} <span class="jp">{rb(p["pattern"])}</span> — {E(p["meaning_vi"])}</div>'
                     f'<div class="lg"><b>Lời giảng (theo 文法ノート):</b>' + ''.join(f'<p>{E(x)}</p>' for x in p['explain_vi']) + '</div>'
                     + (f'<div class="nh"><b>Nhấn mạnh:</b> {GNOTE[(b, no)]}</div>' if (b, no) in GNOTE else '')
                     + f'<div class="exs"><b>Ví dụ:</b><ul>{exs}</ul></div></div>')
        blk(n, f'Ngữ pháp · Bài {b} {rb(g["title"])} <small>{E(g["title_vi"])}</small>', body)
    elif t == 'table':
        rows = ''.join('<tr>' + ''.join(f'<td>{E(c)}</td>' for c in r) + '</tr>' for r in s['rows'])
        blk(n, E(s['h2']), f'<p class="op">{TNOTE}</p><table class="vt">{rows}</table>' + (f'<div class="nh">{E(s["pb"])}</div>' if s.get('pb') else ''))
    elif t == 'quiz':
        ks = 'abcd'; op = ''.join(f'<li class="{"ok" if ks[i] == s["a"] else ""}">{ks[i]}. {E(o)}</li>' for i, o in enumerate(s['opts']))
        blk(n, f'Luyện tập · {E(s["src"])}', f'<p class="op">Thao tác: học viên bấm chọn để bình chọn (số phiếu hiện trên từng phương án) → anh bấm "Đáp án".</p>'
            + (f'<p class="qq"><b>{E(s["big"])}</b></p>' if s.get('big') else '') + f'<p class="qq">{E(s["q"])}</p><ul class="op2">{op}</ul><div class="nh">{E(s["ex"])}</div>', 'qz')
    elif t == 'listen':
        ks = 'abcd'; op = ''.join(f'<li class="{"ok" if ks[i] == s["a"] else ""}">{ks[i]}. {E(o)}</li>' for i, o in enumerate(s['opts']))
        blk(n, f'Nghe hiểu · {E(s["src"])}',
            '<p class="op">Cách dạy: (1) Đọc câu hỏi và các phương án trước, gạch chân từ khoá. (2) Nghe lần 1, học viên bình chọn. (3) Nghe lần 2 kiểm tra. (4) Bấm Đáp án, mở 📄 Script, đọc lại từng câu, chỉ ra câu chứa đáp án.</p>'
            f'<p class="qq">{E(s["q"])}</p><ul class="op2">{op}</ul><div class="ls">{s["exh"]}</div>', 'qz')
    elif t == 'speed':
        blk(n, 'Trò chơi · Thử thách tốc độ', '<div class="lg"><p><b>Cách chơi:</b> bấm ▶ Bắt đầu. Tranh hiện ngẫu nhiên, đồng hồ đếm ngược 4 giây; học viên phải nói từ tiếng Nhật trước khi hết giờ. Hết giờ đáp án tự hiện, 2 giây sau sang tranh mới. Nút ⏸ để dừng giải thích, ⏭ để hiện đáp án / sang câu.</p>'
            '<p><b>Gợi ý tổ chức:</b> chia lớp 2 đội, gọi lần lượt từng bạn; đội nào nói đúng nhiều hơn thắng. Lượt 2 có thể giảm còn 3 giây cho kịch tính.</p></div>', 'gm')
    elif t == 'cloud':
        ws = ' · '.join(f'{E(w)} ({E(KK[w]["r"]) if w in KK else ""})' for w in s['w'])
        blk(n, 'Trò chơi · Đám mây chữ Hán', '<div class="lg"><p><b>Cách chơi:</b> anh gọi một số (hoặc chỉ vào một ô), học viên đọc to từ trong ô đó; bấm ô để hiện cách đọc và âm Hán Việt. Nút 🔀 Đảo lại xáo vị trí và số để chơi vòng 2.</p>'
            f'<p><b>Các từ trong màn này:</b> {ws}</p><p><b>Mở rộng:</b> sau khi đọc, hỏi thêm nghĩa hoặc yêu cầu đặt 1 câu ngắn với từ đó.</p></div>', 'gm')
    elif t == 'ptc':
        it = ''.join(f'<li>{E(x["q"])} → <b>{E(x["a"])}</b> <small>({E(x["vi"])})</small></li>' for x in s['items'])
        blk(n, 'Trò chơi · Điền trợ từ', '<div class="lg"><p><b>Cách chơi:</b> học viên đọc câu và nói trợ từ còn thiếu, bấm thẻ để lật đáp án. Sau mỗi thẻ hỏi lại "vì sao dùng trợ từ này".</p></div>'
            f'<ul class="op2">{it}</ul>', 'gm')
    elif t == 'ord':
        blk(n, 'Trò chơi · Sắp xếp câu', f'<div class="lg"><p><b>Cách chơi:</b> học viên đọc nghĩa tiếng Việt, rồi bấm các mảnh theo đúng thứ tự (bấm mảnh đã chọn để trả lại). Bấm ✔ Kiểm tra: khung xanh là đúng, đỏ là sai. 👀 Đáp án hiện câu đúng.</p>'
            f'<p><b>Nghĩa:</b> {E(s["vi"].replace("🇻🇳 ", ""))}</p><p><b>Các mảnh:</b> {" ／ ".join(E(c) for c in s["ch"])}</p><p><b>Câu đúng:</b> <span class="jp">{E(s["sol"])}</span></p>'
            '<p><b>Nhấn mạnh:</b> tiếng Nhật động từ luôn đứng cuối câu; trợ từ đi sau danh từ như một "nhãn" cho biết vai trò của danh từ đó.</p></div>', 'gm')
    else:
        blk(n, E(s.get('h2') or 'Tổng kết'), '<p class="op">Chốt lại kiến thức đã ôn và giao bài tự ôn trên app.</p>')

CSS = '''<style>@page{size:A4;margin:14mm 13mm}
body{font-family:"M PLUS Rounded 1c",sans-serif;color:#0d2b40;font-size:10.5pt;line-height:1.55}
h1{font-size:22pt;color:#0d5a8c;margin:0}.sub{color:#c42f66;font-weight:700;margin:4px 0 10px}.intro{background:#f4f9fe;border-radius:10px;padding:10px 14px;margin-bottom:12px}
.part{background:#0d5a8c;color:#fff;border-radius:12px;padding:14px 18px;font-size:15pt;font-weight:800;margin:6px 0 10px}
.part.pb{page-break-before:always}.sn2{font-size:9pt;background:#fff;color:#0d5a8c;border-radius:99px;padding:1px 8px;margin-right:6px}
.b{border:1px solid #d6e4f0;border-radius:10px;padding:8px 12px;margin:8px 0}.b.sec,.b.qz,.b.gm{break-inside:avoid}.hd{break-after:avoid}.vt tr{break-inside:avoid}.b.sec{background:#f4f9fe}.b.qz{border-color:#f1c6d6}.b.gm{border-color:#f2d58a;background:#fffbf0}
.hd{display:flex;gap:10px;align-items:baseline;border-bottom:1px dashed #d6e4f0;padding-bottom:4px;margin-bottom:6px}.sn{background:#c42f66;color:#fff;border-radius:99px;padding:1px 9px;font-size:9pt;font-weight:800;white-space:nowrap}.tt{font-weight:800;font-size:12pt;color:#0d5a8c}.tt small{color:#6b8296;font-weight:600}
.op{color:#6b8296;font-size:9.5pt;margin:2px 0 6px;font-style:italic}.lg ul{margin:4px 0 4px 18px;padding:0}.lg p{margin:4px 0}
table.vt{width:100%;border-collapse:collapse;font-size:9.5pt;margin-top:6px}.vt th{background:#0d5a8c;color:#fff;text-align:left;padding:4px 6px}.vt td{border-bottom:1px solid #e6eef6;padding:4px 6px;vertical-align:top}
.jw{font-size:12pt;font-weight:700;white-space:nowrap}.jw rt,.jp rt,.exj rt,.gpt rt{font-size:.5em}.exv{color:#6b8296;font-size:9pt}
.jbig{font-size:16pt}.hv{color:#c42f66;font-weight:800;font-size:9.5pt}.kc{font-size:13pt}
.gp{border-left:4px solid #0d5a8c;padding:4px 10px;margin:8px 0}.gpt{font-weight:800;font-size:11.5pt;color:#0d5a8c}.nh{background:#fff8e6;border-left:4px solid #f2a93b;padding:5px 10px;border-radius:6px;margin:5px 0;font-size:10pt}
.exs ul{margin:3px 0 3px 18px;padding:0}.exs li{margin:2px 0}.exs small{color:#6b8296}
.qq{margin:3px 0;font-weight:700}.op2{margin:3px 0 3px 18px;padding:0}.op2 li.ok{color:#2f9e5b;font-weight:800}
.ls{font-size:9.5pt;background:#fafcff;border-radius:8px;padding:6px 10px}.ls .lb{display:block;font-weight:800;color:#c42f66;font-size:8.5pt;margin-top:4px}.ls p{margin:0}.ls .v{color:#6b8296}.ls rt{font-size:.5em}.ls .ans{font-weight:800;color:#2f9e5b}
.krel{display:grid;grid-template-columns:1fr 1fr;gap:2px 14px;font-size:9.5pt}.krel .jp{font-weight:700;font-size:11pt;margin-right:6px}.krel i{font-style:normal;color:#0d5a8c}.krel small{color:#6b8296;margin-left:4px}
</style>'''
FONT = '<link rel="stylesheet" href="file:///tmp/tk/node_modules/@fontsource/m-plus-rounded-1c/500.css"><link rel="stylesheet" href="file:///tmp/tk/node_modules/@fontsource/m-plus-rounded-1c/700.css"><link rel="stylesheet" href="file:///tmp/tk/node_modules/@fontsource/m-plus-rounded-1c/800.css">'
intro = ('<h1>Giáo án · Tổng ôn toàn diện いろどり 入門</h1><div class="sub">Anh Trọng Dạy JFT · đi kèm slide TongOn_NhapMon_ToanDien.html (211 slide) · đọc theo đúng số slide</div>'
         '<div class="intro"><b>Cấu trúc:</b> 2 vòng — Phần 1 (Bài 1–9) và Phần 2 (Bài 10–18). Mỗi vòng: Từ vựng → trò chơi tốc độ → Chữ Hán → đám mây đọc chữ → Ngữ pháp → bảng tổng hợp → điền trợ từ, sắp xếp câu → Nghe hiểu.<br>'
         '<b>Phím tắt trên slide:</b> → / Space: hiện từng phần · Enter: đáp án · A: hiện hết · P: bút · T: gõ chữ · M: memo · F: cỡ chữ.<br>'
         '<b>Nguồn:</b> từ vựng, câu ví dụ, giải thích ngữ pháp theo いろどり 入門 và 文法ノート いろどり; phần "Lời giảng", "Nhấn mạnh", bảng tổng hợp và hướng dẫn trò chơi là tự soạn; câu nghe lấy từ bộ đề trong app.</div>')
open('/tmp/ga/ga.html', 'w').write('<!doctype html><html><head><meta charset="utf-8">' + FONT + CSS + '</head><body>' + intro + ''.join(B) + '</body></html>')
print(len(B), 'blocks')
