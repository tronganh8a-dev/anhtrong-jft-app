"""Đề nghe 1 (12/11/2026): tuyển tập 20 câu nghe hiểu (nguồn audio: いろどり / まるごと, cắt từ video "Luyện nghe số 1" anh gửi).
Ảnh phương án cắt từng ô (không lấy khung/logo video), câu hỏi – dịch – giải thích do Anh Trọng Dạy JFT soạn lại.
Cần /tmp/ln1/out/img và /tmp/ln1/out/au (cắt từ video, xem CLAUDE.md). Chạy: python3 src/jft/nghe/build_ln1.py rồi python3 src/build_data.py"""
import json, html, shutil, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from furi import furi
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')) + '/'
IMG = 'app/media/jft/img/'; AU = 'app/media/jft/au/'
SRC = '/tmp/ln1/out/'
if os.path.isdir(SRC):
    for f in os.listdir(SRC + 'img'): shutil.copy(SRC + 'img/' + f, REPO + 'public/' + IMG + f)
    for f in os.listdir(SRC + 'au'): shutil.copy(SRC + 'au/' + f, REPO + 'public/' + AU + f)

J = lambda t: furi(html.escape(t)).replace('\n', '<br>')
def EX(ans, script, dich, gt, part=False):
    s = f'<div class="ans">Đáp án đúng: <span class="jp">{J(ans)}</span></div>'
    s += f'<span class="lb">{"SCRIPT (đoạn chính)" if part else "SCRIPT"}</span><div class="jp">{J(script)}</div>'
    s += f'<span class="lb">DỊCH</span><div>{html.escape(dich).replace(chr(10), "<br>")}</div><span class="lb">GIẢI THÍCH</span><div>{J(gt)}</div>'
    return s
qs = []
def L(n, q, vi, opts, a, script, dich, gt, pics=True, part=False, au=None, im=None):
    t = f'<span class="jp">{J(q)}</span><br><span class="vi-q">{html.escape(vi)}</span>'
    o = [{'t': ('ABC'[i] + '. ' if pics else '') + J(x)} for i, x in enumerate(opts)]
    if pics:
        for i, d in enumerate(o): d['img'] = IMG + (im or f'ln1_{n:02d}') + 'abc'[i] + '.jpg'
    qs.append(dict(s='聴解', ins='', gset=None, gimg=None, gau=None, t=t, imgs=[], img=None,
                   au=AU + (au or f'ln1_L{n:02d}') + '.mp3', o=o, a=[a - 1], ex=EX(opts[a - 1], script, dich, gt, part)))

L(1, '公園内で、何をしてはいけませんか。', 'Trong công viên, không được làm gì?',
  ['写真をとる', '食べたり飲んだりする', 'たばこを吸う'], 3,
  '皆様にお願いいたします。公園内は禁煙になっております。小さいお子様もお見えですので、公園内でのおたばこは、ご遠慮くださいませ。ご協力よろしくお願いいたします。',
  'Kính thưa quý vị, chúng tôi có một yêu cầu. Trong công viên cấm hút thuốc. Vì có cả trẻ nhỏ nên xin vui lòng không hút thuốc trong công viên. Rất mong quý vị hợp tác.',
  '「公園内は禁煙」 = trong công viên cấm hút thuốc. 「〜はご遠慮ください」 là cách nói lịch sự của "xin đừng ~" (=〜しないでください), hay gặp trong thông báo. Thông báo không nhắc chụp ảnh hay ăn uống.')
L(2, 'スピーチコンテストで、してはいけないことは何ですか。', 'Trong cuộc thi hùng biện, điều gì không được làm?',
  ['動画をとる', '写真をとる', 'たばこを吸う'], 1,
  '皆様、本日はお忙しい中、スピーチコンテストにおいでくださって、ありがとうございます。始まる前に、皆様にお願いがあります。スピーチコンテスト中、写真の撮影はかまいませんが、動画の撮影はご遠慮ください。また、携帯電話は、電源を切るか、マナーモードに設定し、通話はご遠慮ください。ご協力よろしくお願いいたします。',
  'Cảm ơn quý vị đã đến cuộc thi hùng biện. Trong cuộc thi, quý vị có thể chụp ảnh nhưng xin đừng quay video. Ngoài ra, hãy tắt điện thoại hoặc để chế độ im lặng, và đừng gọi điện.',
  '「写真の撮影はかまいませんが、動画の撮影はご遠慮ください」: chụp ảnh thì được (かまいません = không sao), quay video thì không. Tranh A là máy ảnh + điện thoại quay video → đáp án. Chú ý cặp 写真 (ảnh) – 動画 (video).')
L(3, '二人はいつ、ご飯を食べに行きますか。', 'Hai người sẽ đi ăn cơm khi nào?',
  ['火曜日', '水曜日', '木曜日'], 2,
  'サイド：ムナさん、ご飯、いつがいいですか？\nムナ：私は、火曜日がいいです。サイドさんは？\nサイド：すみません。火曜日はちょっと……。\nムナ：私は、水曜日がいいです。\nサイド：水曜日……だいじょうぶです。\nムナ：じゃあ、水曜日にしましょう。',
  'Saido: Muna, đi ăn hôm nào thì được? / Muna: Tôi thì thứ Ba. Còn Saido? / Saido: Xin lỗi, thứ Ba thì hơi… / Muna: Vậy thứ Tư. / Saido: Thứ Tư… được. / Muna: Vậy chọn thứ Tư nhé.',
  '「火曜日はちょっと……」 = từ chối nhẹ nhàng (thứ Ba không được). Sau đó chốt 「水曜日にしましょう」 (〜にしましょう = quyết định chọn ~).', pics=False)
L(4, '仕事は何時から何時までですか。', 'Công việc từ mấy giờ đến mấy giờ?',
  ['6時～3時半', '9時～6時', '12時～1時'], 2,
  '1日のスケジュールを説明します。仕事は、毎朝9時からです。はじめに、朝礼があります。午前の仕事は、12時までです。12時から1時まで、昼休みです。1時から、午後の仕事です。3時から3時半まで、休み時間です。仕事は、6時までです。ときどき、残業があります。',
  'Tôi giải thích lịch một ngày. Công việc bắt đầu từ 9 giờ sáng. Đầu tiên có họp đầu giờ. Buổi sáng làm đến 12 giờ. 12–1 giờ nghỉ trưa. Từ 1 giờ làm buổi chiều. 3–3 rưỡi nghỉ giải lao. Công việc đến 6 giờ. Thỉnh thoảng làm thêm.',
  'Bài có nhiều mốc giờ – ghi nhanh giờ bắt đầu 「毎朝9時から」 và giờ kết thúc 「6時までです」. 12時～1時 là nghỉ trưa (昼休み), 3時～3時半 là giờ nghỉ (休み時間) – không phải giờ làm việc.', pics=False)
L(5, 'タワットさんは日本で何をしたいですか。', 'Tawatt muốn làm gì ở Nhật?',
  ['山に登る', 'お寺を見る', '神社に行く'], 3,
  'タワットさんは？\n私は新宿の須賀神社に行きたいです。\nえ？須賀神社？どこ？\nあ、アニメの「君の名は。」の神社ですか？\nはい。\nへえ。あと、どら焼きが食べたいです。\nどら焼き？どうして？またアニメですか？\nはい、ドラえもんです。',
  'Còn Tawatt? – Tôi muốn đến đền Suga ở Shinjuku. – Đền Suga? Ở đâu? À, ngôi đền trong anime "Your Name" phải không? – Vâng. Ngoài ra tôi muốn ăn bánh dorayaki. – Lại anime à? – Vâng, Doraemon.',
  '「須賀神社に行きたいです」 → 神社 (đền thần đạo, có cổng 鳥居 torii) = tranh C. Phân biệt: 神社 (じんじゃ, cổng torii) – お寺 (おてら, chùa, có tháp).')
L(6, 'シンさんは週末何をしましたか。', 'Cuối tuần anh Shin đã làm gì?',
  ['温泉に入った', '遊園地に行った', '山に登った'], 1,
  '川口：シンさん、週末、何をしましたか？\nシン：友だちと、別府温泉に行きました。\n川口：へえ、どうでしたか？\nシン：はじめて露天風呂に入りました。気持ちよかったです。それに、景色もきれいでした。\nシン：それから、温泉の近くで、鶏の天ぷらを食べました。おいしかったです。でも、ちょっと高かったです。',
  'Kawaguchi: Cuối tuần anh làm gì? / Shin: Tôi đi suối nước nóng Beppu với bạn. Lần đầu tắm suối ngoài trời, rất dễ chịu, phong cảnh cũng đẹp. Sau đó ăn gà tempura gần suối – ngon nhưng hơi đắt.',
  '「別府温泉に行きました」「露天風呂に入りました」 → tranh A (tắm suối nước nóng ngoài trời). 露天風呂 (ろてんぶろ) = bồn tắm lộ thiên.', part=True)
L(7, '映画はどうでしたか。', 'Bộ phim thế nào?',
  ['とてもおもしろかった', 'よかった', 'まあまあだった'], 3,
  'マリエル：バユさん、休みは、どうでしたか？\nバユ：映画を見に行きました。「ゴジラ」を見ました。\nマリエル：おもしろかったですか？\nバユ：まあまあでした。\nマリエル：そうですか。\nバユ：マリエルさんは？\nマリエル：私は、一日中、掃除と洗濯をしました。大変でした。',
  'Mariel: Kỳ nghỉ của Bayu thế nào? / Bayu: Tôi đi xem phim "Godzilla". / Mariel: Có hay không? / Bayu: Cũng thường thôi. / … Mariel: Tôi dọn dẹp, giặt giũ cả ngày. Vất vả lắm.',
  '「まあまあでした」 = tàm tạm, bình thường → tranh C (tay lắc lư). Thang đánh giá: とても〜 > よかった > まあまあ > あまり〜ない.')
L(8, 'フオンさんは休みの日に何をしますか。', 'Phương làm gì vào ngày nghỉ?',
  ['野球をする', 'バドミントンをする', '家でテレビを見る'], 2,
  'エコ：フオンさんは、休みの日は何をしますか？\nフオン：私は、たいてい友だちとバドミントンをします。私はスポーツが大好きです。\n石川：へえ、バドミントン。どこで？\nフオン：市の体育館でします。毎週、夕方までバドミントンをして、そのあと、みんなでご飯を食べます。本当に楽しいです。',
  'Eko: Ngày nghỉ Phương làm gì? / Phương: Tôi thường chơi cầu lông với bạn. Tôi rất thích thể thao. / Ishikawa: Ở đâu? / Phương: Ở nhà thi đấu của thành phố. Tuần nào cũng chơi đến chiều rồi cùng ăn cơm.',
  '「たいてい友だちとバドミントンをします」 → tranh B. たいてい = thường thì. 体育館 (THỂ DỤC QUÁN) = nhà thi đấu.')
L(9, 'バヤルさんの国には、どんな季節がありますか。', 'Ở nước của Bayar có những mùa như thế nào?',
  ['夏はとても暑くて、冬はとても寒い', '一年中暑い', '晴れの季節と雨の季節がある'], 1,
  'A：バヤルさんの国には、どんな季節がありますか？\nB：日本と同じです。四季があります。でも、夏はとても暑いです。冬はとても寒いです。\nA：そうですか。\nB：夏は40度、冬はマイナス40度になります。\nA：へー、そうなんですか。',
  'A: Nước Bayar có những mùa nào? / B: Giống Nhật, có bốn mùa. Nhưng mùa hè rất nóng, mùa đông rất lạnh. Mùa hè 40 độ, mùa đông âm 40 độ.',
  '「四季があります」「夏は40度、冬はマイナス40度」 → tranh A (biểu đồ nhiệt độ lên rất cao rồi xuống rất thấp). マイナス = âm (dưới 0 độ).')
L(10, '何のお祝いですか。', 'Chúc mừng chuyện gì?',
  ['誕生日', '結婚', '子どもが生まれた'], 3,
  'A：お子さんが生まれたそうですね。\nB：うん、ありがとう。昨日、生まれたんだ。\nA：おめでとうございます。男の子ですか？女の子ですか？\nB：女の子。\nA：そうですか。名前は決めましたか？\nB：ううん、まだ。これから考える。\nA：楽しみですね。',
  'A: Nghe nói anh vừa có em bé? / B: Ừ, cảm ơn. Bé sinh hôm qua. / A: Chúc mừng! Trai hay gái? / B: Con gái. / A: Đã đặt tên chưa? / B: Chưa, giờ mới nghĩ.',
  '「お子さんが生まれた」 = em bé chào đời → tranh C. 〜そうですね (nghe nói ~) dùng để chúc mừng tin vừa nghe. Từ liên quan: 出産 (しゅっさん) = sinh con.')
L(11, '皆は何を食べますか。', 'Mọi người sẽ ăn gì?',
  ['焼き鳥', '焼肉', 'シーフード'], 1,
  'エレノア：アナさんの予定を聞いて、私がみんなに連絡します。\n周：場所はどこがいいでしょうか？\nエレノア：そうですね……アナさん、前に、焼き鳥が大好きだと言ってました。駅前の「たなべ」はどうですか？\n周：じゃあ、あとで予約しますね。',
  'Eleanor: Tôi sẽ hỏi lịch của Anna rồi báo mọi người. / Chu: Địa điểm ở đâu thì được? / Eleanor: Trước đây Anna nói rất thích yakitori. Quán "Tanabe" trước ga thì sao? / Chu: Vậy lát tôi đặt chỗ.',
  'Tiệc chia tay Anna. 「アナさん、前に、焼き鳥が大好きだと言ってました」 → chọn quán yakitori → tranh A. Phần sau của bài nói về quà – xem câu tiếp theo.', part=True)
L(11, '皆はアナさんに何をあげますか。', 'Mọi người sẽ tặng gì cho Anna?',
  ['花', 'デジタルフォトフレーム', 'カメラ'], 2,
  'エレノア：あと、アナさんに何かプレゼントをあげませんか？\n周：そうですね。何がいいでしょうか？エレノアさんの国では、どんなものをあげますか？\nエレノア：花とか？\n周：うーん、もっと、思い出に残るものがいいと思います。予算は？\nエレノア：参加者は10人ぐらいだと思いますから、5,000円ぐらいのものですね。\n周：それなら、デジタルフォトフレームはどうですか？\nエレノア：あ、いいですね。',
  'Eleanor: Mình tặng Anna món quà gì không? / Chu: Tặng gì thì hay? Ở nước chị người ta tặng gì? / Eleanor: Hoa chẳng hạn? / Chu: Tôi nghĩ nên tặng thứ để lại kỷ niệm. Ngân sách bao nhiêu? / Eleanor: Khoảng 10 người, nên món khoảng 5.000 yên. / Chu: Vậy khung ảnh kỹ thuật số thì sao? / Eleanor: Hay đấy.',
  'Hoa (花) bị gạt đi: 「もっと、思い出に残るものがいい」. Chốt 「デジタルフォトフレームはどうですか」「いいですね」 → tranh B. Cùng hội thoại với câu trước (hỏi món ăn).', part=True,
  au='ln1_L11', im='ln2_05')
L(12, 'シハーさんが苦手なのはどれですか。', 'Shihā không ăn được món nào?',
  ['刺身定食', '牛丼', 'ミックスフライ定食'], 1,
  '店員：人気があるのは、お刺身定食です。\n石井：じゃあ、それにします。\nシハー：私は生の魚が苦手なんですが……ほかに何かありますか？\n店員：そうですねえ、フライなどはいかがですか？ミックスフライ定食がおすすめです。\nシハー：じゃあ、それで。',
  'Nhân viên: Món được ưa chuộng là cơm phần sashimi. / Ishii: Vậy tôi chọn món đó. / Shihā: Tôi không ăn được cá sống… có món nào khác không? / Nhân viên: Món chiên thì sao? Tôi gợi ý cơm phần đồ chiên tổng hợp. / Shihā: Vậy chọn món đó.',
  '「生の魚が苦手」 = không ăn được cá sống → món Shihā không ăn được là お刺身定食 (tranh A). 苦手 (にがて) = kém / không thích. Shihā gọi ミックスフライ定食 (tranh C) – đừng nhầm câu hỏi "苦手なのは".', part=True)
L(13, '東京はどんなところですか。', 'Tokyo là nơi như thế nào?',
  ['古い町', '人が多い', '自然が多い'], 2,
  'A：太田さん、前に東京に住んでいたそうですね。どんなところですか？\nB：うーん、やっぱり人が多いよね。電車も混んでいて、ラッシュのときはすごく大変だよ。\nA：そうですか。\nB：でも、遊ぶところがいろいろあるから、一日中遊べるよ。\nA：へー、いいなあ。',
  'A: Nghe nói anh Ota từng sống ở Tokyo. Tokyo thế nào? / B: Đúng là đông người lắm. Tàu cũng đông, giờ cao điểm rất vất vả. Nhưng nhiều chỗ chơi nên chơi cả ngày được.',
  '「やっぱり人が多いよね」「電車も混んでいて」 → tranh B (sân ga đông người). ラッシュ = giờ cao điểm.')
L(14, 'ナディアさんは、どんな宿に泊まりたいですか。', 'Nadia muốn ở chỗ nghỉ như thế nào?',
  ['ホテル', '旅館', '民宿'], 3,
  'B：あのう、日本の旅館に泊まってみたいんですけど、高いですか？\nA：うーん、安いところもあるし、高いところもあるし、いろいろ。\nB：どんなところに泊まったらいいですか？\nA：安いところがいいなら、民宿もいいよ。知ってる？家族でやってる小さな宿。\nB：へー、民宿ですか。\nA：あ、でも、夏休みの時期はすごく混むから、早く計画を立てて、予約したほうがいいよ。',
  'B: Tôi muốn thử ở ryokan Nhật, có đắt không? / A: Có chỗ rẻ, có chỗ đắt. Nếu muốn chỗ rẻ thì minshuku cũng được – nhà nghỉ nhỏ do gia đình kinh doanh. / B: Minshuku à. / A: Mùa hè rất đông, nên lên kế hoạch và đặt sớm.',
  'Nadia muốn chỗ rẻ, được gợi ý 「安いところがいいなら、民宿」 → tranh C (biển 民宿). 旅館 = nhà trọ kiểu Nhật (thường đắt hơn), 民宿 = nhà nghỉ gia đình, rẻ.', part=True)
L(15, 'スキーに行くとき、何を自分で買ったほうがいいですか。', 'Khi đi trượt tuyết, nên tự mua những gì?',
  ['スキー板とウェア', '帽子と手袋', '帽子とスキー板'], 2,
  'A：いいですね。でも、道具とか何も持ってないんです。何を準備したらいいですか？\nB：スキー板とかウェアはスキー場で借りられるから、だいじょうぶだよ。うん。でも、帽子と手袋は、自分で買ったほうがいいよ。\nA：スキー場で買えないんですか？\nB：買えるけど、高いから、こっちで買って、持って行ったほうがいいと思うよ。',
  'A: Tôi không có dụng cụ gì cả. Nên chuẩn bị gì? / B: Ván trượt và quần áo thì thuê được ở khu trượt tuyết. Nhưng mũ và găng tay thì nên tự mua. / A: Ở đó không mua được à? / B: Mua được nhưng đắt, nên mua ở đây rồi mang theo.',
  '「帽子と手袋は、自分で買ったほうがいい」 → tranh B. スキー板・ウェア = 借りられる (thuê được). Vたほうがいい = nên làm V.', part=True)
L(16, '電車は、どうして30分遅れていますか。', 'Tại sao tàu điện bị trễ 30 phút?',
  ['踏切で事故があった', '電車が故障した', '信号が壊れた'], 3,
  'アナウンス：お客様にお知らせいたします。当駅13時9分、高知行きは、信号故障のため、約30分遅れて運転をしております。\nA：あのう、すみません。今のアナウンス、何て言ってましたか？\nB：えっと、電車が30分遅れるそうですよ。信号故障だって。\nA：信号……？\nB：えっと、信号が壊れたんですよ。',
  'Thông báo: Chuyến 13 giờ 9 phút đi Kochi đang chạy trễ khoảng 30 phút do sự cố tín hiệu. / A: Thông báo vừa rồi nói gì vậy? / B: Tàu trễ 30 phút. Nói là hỏng tín hiệu. / A: Tín hiệu…? / B: Tức là đèn tín hiệu bị hỏng.',
  '「信号故障のため」 = do hỏng đèn tín hiệu → tranh C. 〜のため = vì ~ (cách nói trang trọng trong thông báo). 故障 (CỐ CHƯỚNG) = hỏng hóc.', part=True)
L(17, '岡山で乗り換えるとき、新幹線こだま729号は何番線ですか。', 'Đổi tàu ở Okayama, tàu Shinkansen Kodama số 729 ở sân ga số mấy?',
  ['20番線', '21番線', '22番線'], 2,
  'ご乗車ありがとうございました。あと3分ほどで岡山です。お出口は左側、22番線に着きます。乗り換えのご案内をいたします。新幹線、各駅に止まりますこだま729号、博多行き、9時50分、着きました同じホーム、向かい側、21番線です。山陽線普通岡山行き、9時57分、2番線。',
  'Cảm ơn quý khách. Khoảng 3 phút nữa đến Okayama. Cửa ra bên trái, tàu đến sân ga 22. Thông tin đổi tàu: Shinkansen Kodama 729 đi Hakata, 9 giờ 50, ở cùng sân ga, phía đối diện – sân ga 21. Tàu thường tuyến Sanyo 9 giờ 57, sân ga 2.',
  'Chú ý: 「22番線に着きます」 là sân ga tàu mình đang đi sẽ dừng. Kodama 729 ở 「同じホーム、向かい側、21番線」 → 21. Nghe số đi kèm đúng tên tàu được hỏi.', pics=False, part=True)
L(18, 'エドさんは、今日どこに行きましたか。', 'Hôm nay Ed đã đi đâu?',
  ['東照宮', '中禅寺湖', '温泉'], 1,
  '坂本：エドさんは、どちらからですか？\nエド：フィリピンです。でも、今は日本に住んでいます。\n坂本：そうですか。日光に旅行ですか？\nエド：はい、1泊です。\n坂本：今日は、どこに行きましたか？\nエド：今日は、東照宮に行きました。明日は、中禅寺湖に行くつもりです。',
  'Sakamoto: Anh Ed từ đâu đến? / Ed: Philippines, nhưng giờ sống ở Nhật. / Sakamoto: Anh du lịch Nikko à? / Ed: Vâng, ở 1 đêm. / Sakamoto: Hôm nay anh đi đâu? / Ed: Hôm nay tôi đi Toshogu. Mai định đi hồ Chuzenji.',
  '「今日は、東照宮に行きました」 → tranh A. 中禅寺湖 là ngày mai (明日〜つもりです), 温泉 là việc muốn làm sau đó – nghe kỹ thời gian 今日 / 明日.', part=True)
L(18, 'エドさんは、これから何をしたいですか。', 'Từ bây giờ Ed muốn làm gì?',
  ['東照宮に行く', '中禅寺湖に行く', '温泉に入る'], 3,
  '坂本：今日は、どこに行きましたか？\nエド：今日は、東照宮に行きました。明日は、中禅寺湖に行くつもりです。\n坂本：おいしいものは、何か食べましたか？\nエド：はい、そばを食べました。ゆばも食べてみたいです。\nエド：あと、温泉に入りたいんですけど、どこで入ったらいいですか？\n坂本：温泉ですか。中禅寺湖のホテルに、日帰りでお風呂に入れるところがあると思いますよ。',
  'Sakamoto: Hôm nay anh đi đâu? / Ed: Hôm nay đi Toshogu. Mai định đi hồ Chuzenji. / Sakamoto: Đã ăn món gì ngon chưa? / Ed: Ăn soba rồi. Muốn thử yuba nữa. Ngoài ra tôi muốn tắm suối nước nóng, nên tắm ở đâu? / Sakamoto: Khách sạn ở hồ Chuzenji có chỗ cho tắm trong ngày.',
  'Cùng bài với câu trước, nhưng câu hỏi khác: 「これから何をしたいですか」 → 「温泉に入りたいんですけど」 → tranh C. 東照宮 là việc đã làm hôm nay (行きました), 中禅寺湖 là dự định (つもり).', part=True,
  au='ln1_L18', im='ln2_10')
L(19, '盆踊りの前に、何をしますか。', 'Trước khi múa Bon-odori, sẽ làm gì?',
  ['浴衣を着る', 'お酒を飲む', '居酒屋に行く'], 1,
  '杉村：何を着てもいいですよ。あ、でも、娘たちの浴衣があるから、貸しましょうか？\nラウラ：うれしい！\nジーナ：でも、1人で着られますか？\n杉村：私が手伝うから、だいじょうぶ。盆踊りの前に、うちで浴衣を着てから行きましょう。\n杉村：じゃあ、盆踊りが終わったら、いっしょに居酒屋に行きましょう。',
  'Sugimura: Mặc gì cũng được. À, tôi có yukata của con gái, cho mượn nhé? / Laura: Vui quá! / Gina: Nhưng tự mặc được không? / Sugimura: Tôi giúp nên không sao. Trước Bon-odori, mặc yukata ở nhà tôi rồi cùng đi. … Múa xong thì cùng đi izakaya.',
  '「盆踊りの前に、うちで浴衣を着てから行きましょう」 → tranh A. Đi izakaya (tranh C) là SAU khi múa (盆踊りが終わったら). Phân biệt 〜の前に / 〜が終わったら.', part=True)
L(20, '予約はいつですか。', 'Đặt chỗ vào khi nào?',
  ['9日17時（木曜日）', '9日19時（水曜日）', '10日19時（水曜日）'], 2,
  '店員：ご予約ですね。お日にちは、お決まりですか？\nナット：来週の水曜日の夜です。\n店員：9日ですね。何名様ですか？\nナット：6人です。\n店員：お時間は？\nナット：7時はだいじょうぶですか？\n店員：9日の水曜日19時ですね。少々お待ちください……はい、だいじょうぶです。\n店員：それでは、ナット様、9日水曜日、19時から6名様でおまちがいないでしょうか？',
  'Nhân viên: Quý khách đã chọn ngày chưa? / Natt: Tối thứ Tư tuần sau. / Nhân viên: Ngày 9 nhỉ. Mấy người? / Natt: 6 người. / Nhân viên: Mấy giờ? / Natt: 7 giờ được không? / Nhân viên: Thứ Tư ngày 9, 19 giờ… vâng, được ạ.',
  '水曜日 → 9日, 7時 (tối) = 19時 → 9日19時（水曜日）. Đổi giờ: 午後7時 = 19時. 17時 = 5 giờ chiều.', pics=False, part=True)

new = {'id': 'jft-ln1', 'group': 'Luyện nghe JFT', 'title': 'Đề nghe 1', 'name': 'Nghe 1',
       'sub': 'Tuyển tập 20 câu nghe hiểu · いろどり', 'time': 30, 'tag': 'Luyện nghe', 'qs': qs}
P = REPO + 'src/raw/jft_exams.json'
d = json.load(open(P, encoding='utf-8'))
d = [e for e in d if e['id'] != 'jft-ln1']
i = next(k for k, e in enumerate(d) if e['id'] == 'jft-t1')
d.insert(i + 1, new)
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Đề nghe 1:', len(qs), 'câu')
