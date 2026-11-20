# Đề 29 (jft-y4) — từ video "Đề 29" anh gửi 20/11/2026 (màn hình CBT, 40 câu: 10 từ vựng · 10 hội thoại · 10 nghe · 10 đọc).
# Ảnh: tranh câu từ vựng + tranh nghe cắt từ video (đã xoá ô chữ a/b/c/d, phóng to ESRGAN), bài đọc dựng lại bằng make4.js.
# Audio nghe: lần phát ĐẦU của mỗi câu trong video (video phát 2 lần) → y4_L01..10.mp3. Script nghe soạn lại từ nhận dạng giọng nói + nghe đối chiếu.
# Cần /tmp/y4/img, /tmp/y4/au. Chạy: python3 src/jft/youtube/build_y4.py → rồi python3 src/build_data.py
import json, html, shutil, os, sys, re
sys.path.insert(0, '/home/claude/anhtrong-jft-app/src/jft')
from furi import furi
REPO = '/home/claude/anhtrong-jft-app/'
IMG = 'app/media/jft/img/'; AU = 'app/media/jft/au/'
for f in os.listdir('/tmp/y4/img'):
    if f.endswith('.jpg'): shutil.copy('/tmp/y4/img/' + f, REPO + 'public/' + IMG + f)
for f in os.listdir('/tmp/y4/au'): shutil.copy('/tmp/y4/au/' + f, REPO + 'public/' + AU + f)

J = lambda t, fu=True: (furi(html.escape(t)) if fu else html.escape(t)).replace('\n', '<br>')
def EX(ans, dich, gt, script=None, fu=True):
    vi = bool(re.search(r'[A-Za-zÀ-ỹ]', ans))   # đáp án dạng "Tranh 2 – …" (tiếng Việt) thì không dùng phông Nhật
    s = f'<div class="ans">Đáp án đúng: ' + (f'<span>{html.escape(ans)}</span>' if vi else f'<span class="jp">{J(ans, fu)}</span>') + '</div>'
    if script: s += f'<span class="lb">SCRIPT</span><div class="jp">{J(script)}</div>'
    s += f'<span class="lb">DỊCH</span><div>{J(dich, False)}</div><span class="lb">GIẢI THÍCH</span><div>{J(gt, False)}</div>'
    return s
def Q(s, t, o, a, ex, imgs=(), au=None, oimg=None, fu_opt=True):
    oo = [{'t': J(x, fu_opt) if x else ''} for x in o]
    if oimg:
        for d, im in zip(oo, oimg): d['img'] = IMG + im
    return dict(s=s, ins='', gset=None, gimg=None, gau=None, t=t, imgs=[IMG + i for i in imgs],
                img=None, au=au, o=oo, a=[a - 1], ex=ex)
def U(before, word, after=''):   # câu có từ gạch chân: furigana cho phần còn lại, KHÔNG cho từ được hỏi
    return J(before) + '<u>' + html.escape(word) + '</u>' + J(after)

V = '文字と語彙'; K = '会話と表現'; L = '聴解'; R = '読解'
PIC = '絵を見て、正しいことばを選んでください。'
qs = []
def v(t, o, a, dich, gt, imgs=(), fu_opt=True):
    qs.append(Q(V, t, o, a, EX(o[a-1], dich, gt, fu=fu_opt), imgs, fu_opt=fu_opt))

# ---------- 文字と語彙 ----------
v(J(PIC), ['やくそくします', 'よていをします', 'やります'], 1,
  'Tranh: hai bàn tay móc ngón út vào nhau → hứa.',
  'やくそく (約束 – ƯỚC THÚC) = lời hứa, cuộc hẹn; やくそくします = hứa. Người Nhật móc ngón út (ゆびきり) khi hứa với nhau. よてい (予定 – DỰ ĐỊNH) = kế hoạch, lịch trình; やります = làm (nói chung).', ['y4_v1.jpg'])
v(J(PIC), ['しゅくだいをします', 'けんがくをします', 'けんかをします'], 3,
  'Tranh: hai đứa trẻ giằng co, giật tóc nhau → cãi nhau, đánh nhau.',
  'けんか (喧嘩 – HUYÊN HOA) = cãi nhau, đánh nhau; けんかをします. Chú ý けんか và けんがく (見学 – KIẾN HỌC = đi tham quan, kiến tập) chỉ khác nhau một âm. しゅくだい (宿題 – TÚC ĐỀ) = bài tập về nhà.', ['y4_v2.jpg'])
v(J(PIC), ['サンドイッチ', 'サラダ', 'カレー'], 1,
  'Tranh: bánh mì kẹp cắt hình tam giác → sandwich.',
  'サンドイッチ = bánh mì kẹp (sandwich). サラダ = rau trộn (salad), カレー = cà ri. Từ ngoại lai viết bằng katakana, chú ý âm ngắt ッ trong サンドイッチ.', ['y4_v3.jpg'])
v(J('毎朝、花に水を（　　）います。'), ['入れて', 'やって', '入って'], 2,
  'Mỗi sáng tôi tưới nước cho hoa.',
  '花に水をやる = tưới nước cho cây, hoa. やる ở đây là "cho" (cho cây uống nước, cho vật nuôi ăn: 犬にえさをやる). 水を入れる (NHẬP) = đổ nước vào (cốc, bình): コップに水を入れる. 入る (はいる) = đi vào, không đi với を. Vています + 毎朝 = việc làm thường ngày.')
v(J('このごろはお金が（　　）大変です。'), ['ないで', 'なくて', 'なくても'], 2,
  'Dạo này không có tiền nên vất vả.',
  'Vなくて (thể て phủ định) nêu nguyên nhân cho cảm giác, trạng thái phía sau: お金がなくて大変です = vì không có tiền nên khổ. 〜ないで = không làm ~ mà / đừng ~ (傘を持たないで出かけた); 〜なくても = dù không ~ cũng được. このごろ = dạo này. (Đề gốc thiếu trợ từ が, app đã thêm vào.)')
v(J('この肉は（　　）、おいしいです。'), ['ひろくて', 'かたい', 'やわらかくて'], 3,
  'Thịt này mềm và ngon.',
  'Nối hai tính từ: tính từ đuôi い bỏ い + くて: やわらかい → やわらかくて. かたい (cứng) không ở thể て nên không nối được, nghĩa cũng ngược. ひろい (広い – QUẢNG) = rộng, không dùng cho thịt. (Đề gốc ghi 「いいです」, app sửa thành 「おいしいです」 cho tự nhiên.)')
v(U('大きな声で呼んだのに', '返事', 'がありません。'), ['しごと', 'べんじ', 'へんじ'], 3,
  'Tôi đã gọi to vậy mà không có tiếng trả lời.',
  '返事 (PHẢN SỰ) đọc là へんじ = sự trả lời, hồi âm. べんじ sai dấu ゛. しごと là 仕事 (SĨ SỰ) = công việc. 〜のに = vậy mà (kết quả trái mong đợi).', fu_opt=False)
v(U('ここは木が倒れているので', '通れません', '。'), ['とおれません', 'とうれません', 'どうれません'], 1,
  'Ở đây cây bị đổ nên không đi qua được.',
  '通る (THÔNG) đọc là とおる = đi qua; 通れる = đi qua được (thể khả năng) → 通れません. Trường âm ở đây viết bằng お (とお), không phải う. Các từ hay gặp cùng kiểu: 大きい おおきい, 遠い とおい, 十 とお. 倒れる (ĐẢO) たおれる = đổ, ngã.', fu_opt=False)
v(J('早くひらがなが（　　）練習をしています。'), ['読めるように', '読める', '読めるために'], 1,
  'Tôi đang luyện tập để sớm đọc được chữ hiragana.',
  'Vる (thể khả năng / không có ý chí) + ように = để (đạt được trạng thái): 読めるように練習する. 〜ために đi với động từ có ý chí: ひらがなを読むために… (không nói 読めるために). 読める đứng một mình không nối được với 練習.', fu_opt=False)
v(J('夜、バスがなくて、友達のうちに（　　）ことがあります。'), ['止まった', '泊まった', '入った'], 2,
  'Có lần buổi tối hết xe buýt nên tôi đã ngủ lại nhà bạn.',
  '泊まる (BẠC) とまる = ngủ lại, trọ qua đêm (〜に泊まる). 止まる (CHỈ) cũng đọc とまる nhưng nghĩa là dừng lại (xe dừng). 入る (NHẬP) = vào. Vたことがあります = đã từng làm.', fu_opt=False)

# ---------- 会話と表現 ----------
def k(t, o, a, dich, gt):
    qs.append(Q(K, J(t), o, a, EX(o[a-1], dich, gt)))
k('ジョイ：日本の人はどうやって食事をしますか。\n田中：はしと茶わんで食事をします。\nジョイ：茶わんは手で（　　）か。\n田中：はい、手で持ちます。ナイフやフォークなども使います。',
  ['まちます', 'もちます', 'めします'], 2,
  'Joy: Người Nhật ăn uống như thế nào? / Tanaka: Ăn bằng đũa và bát cơm. / Joy: Bát thì cầm bằng tay à? / Tanaka: Vâng, cầm bằng tay. Cũng dùng cả dao, nĩa nữa.',
  '持つ (TRÌ) もつ = cầm, mang. Câu trả lời 「手で持ちます」 cho biết đáp án. まつ (待つ – ĐÃI) = đợi; めします (召します) = kính ngữ của 着る・食べる, không hợp. Văn hoá: ở Nhật khi ăn thường cầm bát cơm lên tay. (Đề gốc thiếu か cuối câu hỏi, app đã thêm.)')
k('きゃく：すみません、メコンのカメラはありますか。\n店員：はい、こちらです。\nきゃく：（　　）\n店員：これは五万六千円です。',
  ['いくらになりますか', 'いつになりますか', 'いくつになりますか'], 1,
  'Khách: Xin lỗi, có máy ảnh hãng Mekon không? / Nhân viên: Vâng, đây ạ. / Khách: Giá bao nhiêu ạ? / Nhân viên: Cái này 56.000 yên.',
  'Hỏi giá: いくらですか / いくらになりますか. Câu sau trả lời bằng tiền (五万六千円 ごまんろくせんえん) nên chọn いくら. いつ = khi nào; いくつ = mấy cái / mấy tuổi.')
k('リン：パクさんはお酒をよく飲みますか。\nパク：私はお酒があまり好きではありませんが、ときどき飲みますよ。あなたはどうですか。\nリン：私の家族は、みんなお酒が好きですから、たくさん飲みます。でも、わたしはぜんぜん（　　）。',
  ['のみました', 'のみません', 'のみます'], 2,
  'Rin: Anh Park có hay uống rượu không? / Park: Tôi không thích rượu lắm nhưng thỉnh thoảng cũng uống. Còn chị thì sao? / Rin: Gia đình tôi ai cũng thích rượu nên uống nhiều. Nhưng tôi thì hoàn toàn không uống.',
  'ぜんぜん (全然 – TOÀN NHIÊN) luôn đi với thể phủ định: ぜんぜん飲みません = hoàn toàn không uống. でも báo hiệu ý trái với câu trước (gia đình uống nhiều ↔ tôi không uống). (Đề gốc ghi 「好きでわありません」, đúng phải là 「好きではありません」.)')
k('A：すみません。田中課長いらっしゃいますか。\nB：はい、おります。少々（　　）。',
  ['持つください', 'お持ちください', 'お待ちください'], 3,
  'A: Xin lỗi, trưởng phòng Tanaka có ở đây không ạ? / B: Vâng, có ạ. Xin vui lòng chờ một chút.',
  '少々お待ちください = xin vui lòng đợi một chút (rất hay dùng ở công ty, cửa hàng). お + Vます (bỏ ます) + ください là cách nhờ lịch sự. お持ちください dùng chữ 持 (TRÌ – cầm) = xin hãy cầm/mang theo, khác chữ 待 (ĐÃI – đợi). 持つください sai ngữ pháp. いらっしゃいます (tôn kính) – おります (khiêm nhường) là cách nói của います.')
k('A：（　　）。具合が悪そうですね。\nB：ええ、ちょっと頭がいたくて。\nA：大丈夫ですか。\nB：すみませんが、休んでもいいですか。',
  ['こんにちは', 'どうしたんですか', 'はい'], 2,
  'A: Có chuyện gì vậy? Trông bạn có vẻ không khoẻ. / B: Vâng, tôi hơi đau đầu. / A: Có sao không? / B: Xin lỗi, tôi nghỉ một chút được không?',
  'どうしたんですか = có chuyện gì vậy / bạn bị sao thế — hỏi khi thấy người khác có vẻ khác thường. 具合が悪そう = trông có vẻ không khoẻ (Aい bỏ い + そう). 〜てもいいですか = xin phép. (Đề gốc ghi 「悪いそう」, đúng phải là 「悪そう」.)')
k('A：何がいいですか。\nB：ジュースがいいです。\nA：すみません。ジュースとコーラをお願いします。\n店員：はい、ジュースとコーラですね。（　　）。',
  ['どうぞよろしく', 'かしこまりました', 'はい、そうします'], 2,
  'A: Bạn uống gì? / B: Nước ép là được. / A: Xin lỗi, cho tôi nước ép và cô-la. / Nhân viên: Vâng, nước ép và cô-la ạ. Tôi đã rõ ạ.',
  'かしこまりました = vâng, tôi đã hiểu (nhân viên nói với khách khi nhận yêu cầu, rất lịch sự; thân mật hơn: わかりました). どうぞよろしく = rất mong được giúp đỡ (khi làm quen). はい、そうします = vâng, tôi sẽ làm vậy (khi nghe lời khuyên).')
k('A：好きな季節はいつですか。\nB：秋が一番好きです。\nA：（　　）。\nB：食べ物がおいしいですから。',
  ['どうしたんですか', 'どうしてですか', 'どれですか'], 2,
  'A: Mùa bạn thích là mùa nào? / B: Tôi thích mùa thu nhất. / A: Tại sao vậy? / B: Vì đồ ăn ngon.',
  'どうしてですか = tại sao? — câu trả lời kết thúc bằng 〜から (vì) là dấu hiệu. どうしたんですか = có chuyện gì vậy; どれですか = cái nào. 季節 (QUÝ TIẾT) きせつ = mùa.')
k('田中：もしもし、ジョイさんですか。田中です。\nジョイ：お久しぶりです。田中さん、お元気ですか。\n田中：はい、元気です。こっちは今、雨が降っています。\nジョイ：（　　）。\n田中：そっちはどうですか。\nジョイ：いい天気です。',
  ['だいじょうぶですか', 'いいです', 'たいへんですね'], 3,
  'Tanaka: Alô, Joy đấy à? Tanaka đây. / Joy: Lâu rồi không gặp. Anh Tanaka khoẻ không? / Tanaka: Ừ, khoẻ. Bên này giờ đang mưa. / Joy: Vất vả nhỉ. / Tanaka: Bên đó thế nào? / Joy: Trời đẹp ạ.',
  'たいへんですね = vất vả nhỉ / khổ nhỉ — đáp lại khi nghe chuyện không thuận lợi (trời mưa). だいじょうぶですか hỏi người gặp chuyện như ốm, ngã; いいです = được, không cần. こっち／そっち = bên này / bên đó (văn nói của こちら／そちら).')
k('A：先生は今どちらですか。\nB：先生は今、図書館に（　　）。',
  ['ございます', 'おっしゃいます', 'いらっしゃいます'], 3,
  'A: Thầy giáo bây giờ đang ở đâu ạ? / B: Thầy bây giờ đang ở thư viện ạ.',
  'いらっしゃいます là tôn kính ngữ của います / 行きます / 来ます, dùng cho người trên (thầy cô, cấp trên). ございます = lịch sự của あります (đồ vật). おっしゃいます = tôn kính của 言います. どちら = lịch sự của どこ. 図書館 (ĐỒ THƯ QUÁN) としょかん = thư viện.')
k('A：昨日から少しねつがあって、頭がいたいです。\nB：それは、（　　）。',
  ['おげんきで', 'いけませんね', 'しつれいします'], 2,
  'A: Từ hôm qua tôi hơi sốt và đau đầu. / B: Vậy thì không ổn rồi.',
  'それはいけませんね = thế thì không ổn rồi / tội nghiệp quá — câu đồng cảm khi nghe ai ốm, gặp chuyện không may; sau đó thường nói お大事に (mau khoẻ nhé). おげんきで = giữ sức khoẻ nhé (khi chia tay lâu ngày). しつれいします = xin phép (vào/ra phòng).')

# ---------- 聴解 ----------
def l(n, q, vi, a, ans, script, dich, gt, ctx=None, nopt=4):
    t = f'<span class="jp">{J(q)}</span><br><span class="vi-q">{html.escape(vi)}</span>'
    qs.append(Q(L, t, [''] * nopt, a, EX(ans, dich, gt, script), imgs=[ctx] if ctx else (), au=AU + f'y4_L{n:02d}.mp3',
                oimg=[f'y4_l{n}_{i}.jpg' for i in range(1, nopt + 1)]))
l(1, 'この人はだれと京都に来ましたか。', 'Người đàn ông đến Kyoto cùng với ai?', 4, 'Tranh 4 – vợ và hai con (gia đình 4 người)',
  '（京都は初めてですか。）\n1\n女：あのう、すみません。京都は初めてですか。\n男：ええ、初めてです。すごく楽しみにして来ました。\n女：皆さん、ご家族ですか。\n男：はい、家族4人で来ました。妻と息子と娘です。\n女：そうですか。ゆっくり楽しんでくださいね。',
  'Nữ: À, xin lỗi. Anh đến Kyoto lần đầu à? / Nam: Vâng, lần đầu. Tôi đã rất mong được đến đây. / Nữ: Mọi người là gia đình à? / Nam: Vâng, gia đình 4 người chúng tôi đến. Vợ, con trai và con gái tôi. / Nữ: Vậy à. Chúc cả nhà đi chơi vui vẻ nhé.',
  'Câu then chốt: 家族4人で来ました。妻と息子と娘です → 4 người: chồng, vợ, con trai, con gái → tranh 4. 妻 (THÊ) つま = vợ (mình), 息子 (TỨC TỬ) むすこ = con trai, 娘 (NƯƠNG) むすめ = con gái. Câu mở đầu của bài nghe nhắc lại câu hỏi trong tranh.',
  ctx='y4_l1_ctx.jpg')
l(2, 'カルメンさんは環境のために何をしていますか。', 'Carmen đang làm gì để bảo vệ môi trường?', 1, 'Tranh 1 – dùng máy rửa bát',
  '（何かエコ活動をしていますか。）\n1\nA：カルメンさんは何かエコ活動をしていますか。\nカルメン：私は台所で使う水を減らすようにしてますよ。\nA：え？どうやって？\nカルメン：最近、食洗機を使ってるんです。\nA：なるほど。それは水を減らすのに役に立ちますね。',
  'A: Chị Carmen có làm hoạt động bảo vệ môi trường nào không? / Carmen: Tôi cố gắng giảm lượng nước dùng trong bếp. / A: Ơ? Bằng cách nào? / Carmen: Gần đây tôi dùng máy rửa bát. / A: Ra vậy. Cái đó giúp giảm nước nhỉ.',
  '食洗機 (THỰC TẨY CƠ) しょくせんき = máy rửa bát → tranh 1. エコ活動 = hoạt động bảo vệ môi trường. 減らす (GIẢM) へらす = làm giảm; Vるようにしている = cố gắng duy trì thói quen. 役に立つ = có ích. Các tranh khác: đổ xăng, phân loại rác, đi chợ bằng giỏ — không được nhắc tới.',
  ctx='y4_l2_ctx.jpg')
l(3, '3人は何について話していますか。', 'Ba người đang nói về cái gì?', 1, 'Tranh 1 – bộ kimono',
  'A：こちらをご覧ください。これは16世紀ごろに作られた着物です。武士の奥さんがお祭りのときに着ました。\nB：へえ、武士の奥さんの着物ですか。きれいですね。私も着てみたいです。',
  'A (hướng dẫn viên): Xin mời mọi người xem đây. Đây là bộ kimono được làm vào khoảng thế kỷ 16. Vợ của võ sĩ đã mặc nó vào dịp lễ hội. / B: Ồ, kimono của vợ võ sĩ à. Đẹp quá. Tôi cũng muốn mặc thử.',
  '着物 (TRƯỚC VẬT) きもの = kimono → tranh 1. 着ました (きました) = đã mặc — đồng âm với 来ました (đã đến), nghe theo ngữ cảnh. 16世紀 (THẾ KỶ) = thế kỷ 16, 作られた = được làm ra (bị động), 武士 (VÕ SĨ) ぶし = võ sĩ samurai, ご覧ください = xin mời xem (kính ngữ). Vてみたい = muốn thử làm.',
  ctx='y4_l3_ctx.jpg')
l(4, '野田さんのプレゼントは何でしたか。', 'Quà của anh Noda là gì?', 2, 'Tranh 2 – đồng hồ đeo tay',
  'A：野田さんのプレゼント、何でしたか。\nB：野田さんから、かっこいい時計をもらいました。とてもうれしかったです。ほら、これです。\nA：あ、ほんと、かっこいいですね。',
  'A: Quà của anh Noda là gì vậy? / B: Tôi nhận được từ anh Noda một chiếc đồng hồ rất đẹp. Vui lắm. Này, đây này. / A: À, đúng thật, đẹp quá nhỉ.',
  '時計 (THỜI KẾ) とけい = đồng hồ → tranh 2. 〜から〜をもらいました = nhận ~ từ ai. かっこいい = ngầu, đẹp. ほら、これです = này, cái này đây (đưa ra cho xem).',
  ctx='y4_l4_ctx.jpg')
l(5, 'この人は、穴が開いた靴下をどうしますか。', 'Người này làm gì với chiếc tất bị thủng?', 1, 'Tranh 1 – vứt vào túi rác',
  '（どうしますか。）\n1\nA：あのう、穴が開いて靴下がはけなくなったら、どうしますか。\nB：穴が開いたら、もったいないけど捨てますよ。\nA：そうですか。\nB：ええ。リサイクルとか考えるのが面倒なので、捨てます。',
  'A: À, khi tất bị thủng không đi được nữa thì bạn làm gì? / B: Thủng rồi thì tuy tiếc nhưng tôi vứt đi. / A: Vậy à. / B: Vâng. Nghĩ đến chuyện tái chế các thứ thì phiền nên tôi vứt.',
  '捨てます (XẢ) すてます = vứt bỏ → tranh 1 (bỏ vào túi rác). もったいない = phí, tiếc. 面倒 (MIỄN ĐẢO) めんどう = phiền phức. Tranh 3 (dùng làm giẻ lau) là cách tái chế — người này nói không muốn nghĩ đến tái chế. はく = đi (tất, giày, quần); はけなくなる = không đi được nữa.',
  ctx='y4_l5_ctx.jpg')
l(6, 'キムさんは子どものとき、どうでしたか。', 'Hồi nhỏ, Kim là đứa trẻ như thế nào?', 3, 'Tranh 3 – bị bố mắng',
  'A：キムさんはどんな子どもでしたか。\nキム：そうですね。父がとても厳しかったんです。時々、家に遅く帰って、しかられました。\nA：へえ、キムさん、しかられたんですか。\nキム：ええ。怖かったけど、今ではいい思い出ですよ。',
  'A: Hồi nhỏ anh Kim là đứa trẻ như thế nào? / Kim: Để xem. Bố tôi rất nghiêm khắc. Thỉnh thoảng tôi về nhà muộn và bị mắng. / A: Ồ, anh Kim bị mắng à? / Kim: Vâng. Lúc đó sợ lắm nhưng giờ là kỷ niệm đẹp.',
  'しかられました (叱られる – SẤT, bị động của 叱る) = bị mắng → tranh 3 (người bố đang mắng con). 厳しい (NGHIÊM) きびしい = nghiêm khắc, 思い出 = kỷ niệm. 〜けど = nhưng.',
  ctx='y4_l6_ctx.jpg')
l(7, 'フランスにはどんな食事のマナーがありますか。', 'Ở Pháp có phép lịch sự gì khi ăn?', 1, 'Tranh 1 – không được ăn phát ra tiếng',
  'A：カーラさん、フランスではどんな食事のマナーがありますか。\nカーラ：そうですね。フランスでは……うーん、静かに食べます。\nA：静かに？\nカーラ：はい。食事のとき、音を立てません。例えば、スープは音を立てて飲んじゃだめですよ。\nA：へえ、そうですか。難しそうですね。日本では大丈夫なんですが。',
  'A: Chị Carla, ở Pháp có những phép lịch sự gì khi ăn? / Carla: Để xem. Ở Pháp thì… ừm, ăn trong yên lặng. / A: Yên lặng? / Carla: Vâng. Khi ăn không phát ra tiếng. Ví dụ, không được húp súp thành tiếng đâu. / A: Ồ, vậy à. Có vẻ khó nhỉ. Ở Nhật thì không sao.',
  '音を立てる = phát ra tiếng → tranh 1 (ăn súp phát ra tiếng bị gạch X). 〜ちゃだめ = 〜てはだめ = không được làm. 静か (TĨNH) しずか = yên lặng, 例えば (LỆ) たとえば = ví dụ. 難しそう = có vẻ khó.')
l(8, '2番の注文はどれですか。', 'Món gọi số 2 là cái nào?', 3, 'Tranh 3 – 3 cô-la, 2 nước ép',
  'ご注文、お決まりですか。\n1　コーヒーと紅茶、2つずつお願いします。\n2　コーラ3つとジュース2つ、お願いします。\n3　コーヒーと紅茶1つずつ、あと、ジュース2つお願いします。',
  'Quý khách đã chọn món chưa ạ? / 1: Cho tôi cà phê và trà, mỗi loại 2 cốc. / 2: Cho tôi 3 cô-la và 2 nước ép. / 3: Cho tôi cà phê và trà mỗi loại 1 cốc, thêm 2 nước ép.',
  'Số 2: コーラ3つとジュース2つ → tranh 3. Tranh 2 là gọi món số 1 (2 cà phê, 2 trà); tranh 1 là gọi món số 3. 〜ずつ = mỗi loại ~; あと = thêm nữa. Khi nghe phải ghi nhanh con số theo từng món.',
  ctx='y4_l8_ctx.jpg', nopt=3)
l(9, '斎藤さんはどうして山下選手のファンになりましたか。', 'Vì sao anh Saitō trở thành người hâm mộ tuyển thủ Yamashita?', 1, 'Tranh 1 – xem trận đấu trên tivi',
  'A：斎藤さんは山下選手のファンですか。\n斎藤：ええ。子どものとき、オリンピックの試合をテレビで見てから、ずっとファンです。\nA：オリンピックの試合ですか。\n斎藤：はい。山下はけがをしてましたが、金メダルを取るまで本当に頑張ったんですよ。すごかったなあ。\nA：そうですか。立派ですね。',
  'A: Anh Saitō là fan của tuyển thủ Yamashita à? / Saitō: Vâng. Từ hồi nhỏ xem trận đấu Olympic trên tivi, tôi hâm mộ suốt đến giờ. / A: Trận đấu Olympic à? / Saitō: Vâng. Yamashita bị chấn thương nhưng đã cố gắng hết sức cho đến khi giành huy chương vàng đấy. Tuyệt vời thật. / A: Vậy à. Thật đáng nể.',
  'テレビで見てから、ずっとファンです → trở thành fan sau khi xem trên tivi → tranh 1. Vてから = sau khi làm V. 試合 (THÍ HỢP) しあい = trận đấu, 金メダル = huy chương vàng, 立派 (LẬP PHÁI) りっぱ = đáng khâm phục.',
  ctx='y4_l9_ctx.jpg')
l(10, 'この人は1年に何をしますか。', 'Người này làm gì trong một năm?', 2, 'Tranh 2 – đi xem phim ở rạp',
  '私の町にフランス文化センターがあります。私はセンターで週に2回フランス語を勉強しています。それから、年に4、5回、フランスの映画を見に行きます。とても楽しいです。',
  'Ở thị trấn của tôi có Trung tâm Văn hoá Pháp. Tôi học tiếng Pháp ở trung tâm 2 lần mỗi tuần. Ngoài ra, mỗi năm tôi đi xem phim Pháp 4, 5 lần. Rất vui.',
  '年に4、5回 (một năm 4, 5 lần) + 映画を見に行きます → tranh 2 (rạp chiếu phim). 週に2回 = 2 lần mỗi tuần — là việc học tiếng Pháp, không phải "trong năm". Vに行く = đi để làm V. 文化 (VĂN HOÁ) ぶんか.',
  ctx='y4_l10_ctx.jpg', nopt=3)

# ---------- 読解 ----------
def r(q, o, a, img, dich, gt):
    qs.append(Q(R, J(q), o, a, EX(o[a-1], dich, gt), [img]))
r('カーラさんはどのときまで自分で日本語をならいましたか。', ['大学を卒業するまで', '専門学校を卒業するまで', '高校を卒業するまで'], 3, 'y4_r1.jpg',
  'Carla sinh năm 1989 ở Pháp. Hồi nhỏ, sau khi được bố tặng một cuốn truyện tranh Nhật, cô bắt đầu quan tâm đến Nhật Bản. Hồi cấp 3, sau khi đi du lịch Nhật với gia đình, cô càng thích Nhật hơn. Cho đến khi tốt nghiệp cấp 3, cô tự học tiếng Nhật một mình. Vào đại học, cô học chuyên ngành tiếng Nhật và văn hoá Nhật. Năm 2014 cô du học cao học ở Nhật và sống ở Nhật.',
  '「高校を卒業するまで、一人で日本語を勉強しました」 → tự học (一人で = 自分で) đến khi tốt nghiệp cấp 3. Lên đại học thì học chuyên ngành ở trường, không còn là tự học. 卒業 (TỐT NGHIỆP) そつぎょう, 高校 (CAO HIỆU) = trường cấp 3, 専門学校 = trường dạy nghề — không có trong bài.')
r('正しいものはどれですか。', ['なかむらさんは10回以上京都へ来ました。', 'ルパさんはしょかい京都へきました。', 'キムさんは1回も京都へ来たことがありません。'], 2, 'y4_r2.jpg',
  'Nakamura: Rupa, Kim, hai bạn đến Kyoto lần đầu à? / Rupa: Tôi lần đầu ạ. Rất mong được giúp đỡ. / Kim: Tôi lần thứ hai. Mùa thu năm ngoái tôi đến cùng em gái. Nhưng mùa xuân cũng đẹp nhỉ. / Nakamura: Ừ. Kyoto đến lúc nào cũng vui. / Kim: Chị Nakamura lần thứ mấy rồi? / Nakamura: Chắc lần thứ 7. Ở Kyoto ăn gì cũng ngon, đi đâu cũng có không khí Nhật Bản, hay lắm.',
  'ルパ: 「私ははじめてです」 → lần đầu = しょかい (初回 – SƠ HỒI). Nakamura đến khoảng 7 lần (không phải hơn 10), Kim là lần thứ hai (二回目) nên đã từng đến. (Đề gốc ghi 「何も食べても」「ふいき」, app sửa thành 「何を食べても」「ふんいき」.)')
r('説明にあうのはどれですか。', ['私は去年父に青いネクタイをあげました。', '私は今年父の日に青いシャツをあげます。', '私は去年も今年も父にプレゼントをあげます。', '赤は父の好きな色です。'], 3, 'y4_r3.jpg',
  'Năm ngoái vào Ngày của Cha tôi tặng bố chiếc áo sơ mi màu xanh. Màu xanh là màu bố thích. Năm nay tôi sẽ tặng cà vạt màu xanh.',
  'Năm ngoái tặng áo sơ mi, năm nay tặng cà vạt → năm nào cũng tặng quà cho bố → 3. Câu 1 sai món (năm ngoái là シャツ), câu 2 sai món (năm nay là ネクタイ), câu 4 sai màu (bố thích 青). Màu sắc làm danh từ: 青 (THANH) あお; tính từ: 青い. (Đề gốc ghi 「青いは」 và phương án 3 「去年より今年も…あげたいです」 không rõ nghĩa, app sửa lại cho đúng ý.)')
r('正しいものはどれですか。', ['この人は漢字がとてもじょうずです。', 'この人は日本語は何でも読めます。', 'この人は日本語と日本文化が好きです。'], 3, 'y4_r4.jpg',
  'Tiêu đề: Tình nguyện viên lễ hội Nhật Bản. Gửi chị Fujii Norika, Lần đầu được làm quen. Tôi tên là Julio Gonzales. Tôi muốn làm tình nguyện viên cho lễ hội Nhật Bản. Tôi rất quan tâm đến tiếng Nhật và văn hoá Nhật. Tôi không đọc được nhiều chữ Hán, nhưng nếu là tiếng Nhật đơn giản thì tôi nói được. Tôi sẽ cố gắng, rất mong được giúp đỡ. Julio Gonzales',
  '「日本語と日本文化にとてもきょうみがあります」 (rất quan tâm) ≈ 好きです → 3. 「かんじはあまり読めません」 → câu 1, 2 sai. きょうみ (興味 – HỨNG VỊ) = sự quan tâm, hứng thú. 〜だったら = nếu là ~.')
r('メロスはどうして町に来ましたか。', ['おうさまに会うために', '妹の結婚式の買い物のために', 'メロスのしんせきに会うために'], 2, 'y4_r5.jpg',
  'Melos nổi giận. Anh nghĩ không thể tha thứ cho nhà vua độc ác. Melos không hiểu những chuyện phức tạp. Melos sống vui vẻ ở làng. Nhưng Melos không thể tha thứ cho điều xấu. Melos từ làng đến thành phố tên là Syracuse. Melos không có bố mẹ, cũng không có vợ. Anh sống cùng em gái 16 tuổi. Em gái sắp kết hôn. Melos đến thành phố để mua sắm chuẩn bị cho đám cưới. Đi trong thành phố, Melos thấy thành phố có gì đó lạ. So với lần trước đến, thành phố yên lặng quá. Vì vậy Melos hỏi người trong thành phố.',
  '「結婚式のよういのために買い物をしに町に来たのです」 → 2. よういのために = để chuẩn bị (用意 – DỤNG Ý). Vに来る = đến để làm V. Nhà vua chỉ được nhắc là người Melos giận, không phải lý do đến; bài nói Melos không có người thân ngoài em gái. Bài đọc kể lại đơn giản truyện 『走れメロス』 của 太宰治. (Đề gốc ghi 「シクラス」「おうさまを会う」, app sửa thành 「シラクス」「おうさまに会う」.)')
r('どうしてこの男の人は30分おくれますか。', ['病気ですから', 'バスがこなかったから', '事故があったから'], 3, 'y4_r6.jpg',
  'Thư 1 – Tiêu đề: Đến muộn. Xin lỗi. Vì xe buýt bị tai nạn nên tôi sẽ đến muộn khoảng 30 phút. Vậy hẹn gặp lát nữa. / Thư 2 – Tiêu đề: Re: Đến muộn. Tôi hiểu rồi. Đi cẩn thận nhé.',
  '「バスのじこで、30分ぐらいおくれます」 → じこ = 事故 (SỰ CỐ) = tai nạn → 3. Danh từ + で chỉ nguyên nhân. Xe buýt có tới nhưng bị tai nạn, không phải "không tới". 遅れる (TRÌ) おくれる = muộn; きをつけて = cẩn thận.')
r('レストラン「ハンナ」はどんなレストランですか。', ['ファミリーレストランです。', 'ようしょくのレストランです。', 'アメリカのレストランです。'], 2, 'y4_r7.jpg',
  'Nhà hàng "Hannah". Hannah là nhà hàng món Âu. Đồ ăn rẻ và ngon nên tôi hay đến. Món tôi luôn ăn ở quán này là bò sốt teriyaki. Thịt và nước sốt rất ngon. Nếu được thì hãy đến thử nhé.',
  '「『ハンナ』は洋食のレストランです」 → ようしょく = 洋食 (DƯƠNG THỰC) = món ăn kiểu Âu → 2. Đối lập: 和食 (わしょく) = món Nhật. Bài không nói là nhà hàng gia đình hay nhà hàng Mỹ.')
r('「1番目の男の子」と言うのは何の意味ですか。', ['家族ではじめにうまれた女の子', '家族ではじめにうまれた男の子', '家族の一人っ子'], 2, 'y4_r8.jpg',
  'Ishikawa: Rất vui được làm quen. Tôi là Ishikawa Ichirō. Ichirō nghĩa là "con trai thứ nhất". / Kate: Anh Ishikawa có mấy anh chị em? / Ishikawa: Tôi có 2 em gái. Em gái lớn sống ở Osaka. Em gái nhỏ ở chỗ tên là Saitama. / Kate: Vậy à.',
  '1番目の男の子 = con trai đầu tiên → con trai sinh ra đầu tiên trong nhà → 2. Ishikawa có 2 em gái nên không phải con một (一人っ子). Tên いちろう (一郎): 一 = một, 郎 = con trai. はじめに = đầu tiên; うまれる (生まれる – SINH) = được sinh ra.')
r('女の人はどうやって北海道へ行きますか。', ['ふねで', 'バスで', 'ひこうきで', '車で'], 3, 'y4_r9.jpg',
  'Nam: Kỳ nghỉ hè chị đi đâu? / Nữ: Tôi muốn đi Hokkaido. / Nam: Hay nhỉ. Đi máy bay à? / Nữ: Vâng. Lúc đầu tôi định đi tàu thuỷ hoặc xe buýt. Nhưng mất thời gian quá… Đến nơi rồi tôi định thuê ô tô.',
  'Nam hỏi ひこうきですか → nữ trả lời ええ (vâng) → đi máy bay → 3. ふね, バス là dự định lúc đầu (さいしょは〜と思ったんです) nhưng bỏ vì quá mất thời gian. 車 là phương tiện dùng sau khi đến nơi (むこうに着いたら). Vようと思う = định làm; Vるつもり = dự định.')
r('日本語を学びたいです。どこへ行きますか。', ['7のストール', '2時にステージの前', '10時にステージの前'], 2, 'y4_r10.jpg',
  'Tờ hướng dẫn lễ hội: gian hàng ① món Hàn (bánh xèo Hàn) ② món Nga (bánh piroshki) ③ món Mexico (tacos) ④ món Đức (xúc xích) ⑤ món Malaysia (murtabak) ⑥ đồ thủ công Tây Ban Nha (thêu) ⑦ đồ thủ công Nhật (búp bê kokeshi) ⑧ đồ thủ công Philippines (phụ kiện). Sân khấu (Bài hát và điệu múa thế giới): 10:00–10:30 múa Thái Lan, 11:00–11:30 bài hát Pháp, 14:00–14:30 Lớp tiếng Nhật mini.',
  'Muốn học tiếng Nhật → 「14:00〜14:30 日本語ミニレッスン」 ở sân khấu → 2 giờ chiều, trước sân khấu → 2. Gian hàng số 7 bán búp bê こけし (đồ thủ công), 10 giờ là múa Thái. 学ぶ (HỌC) まなぶ = học. ストール = gian hàng.')

ex = dict(id='jft-y4', group='Đề thi thử JFT-Basic', title='Đề 29', sub='Có phần nghe · 40 câu', time=60, qs=qs)
E = json.load(open(REPO + 'src/raw/jft_exams.json'))
E = [e for e in E if e['id'] != 'jft-y4']
pos = max(i for i, e in enumerate(E) if e['id'] == 'jft-t1') + 1
E = E[:pos] + [ex] + E[pos:]
json.dump(E, open(REPO + 'src/raw/jft_exams.json', 'w'), ensure_ascii=False, indent=1)
print(len(qs), [sum(q['s'] == x for q in qs) for x in (V, K, L, R)])
