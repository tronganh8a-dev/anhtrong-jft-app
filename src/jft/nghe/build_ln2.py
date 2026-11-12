"""Đề nghe 2 (12/11/2026): tuyển tập 20 câu nghe hiểu (nguồn audio: いろどり / まるごと, cắt từ video "Luyện nghe số 2" anh gửi).
Ảnh phương án cắt từng ô (không lấy khung/logo video), câu hỏi – dịch – giải thích do Anh Trọng Dạy JFT soạn lại.
Cần /tmp/ln2/out/img và /tmp/ln2/out/au (cắt từ video, xem CLAUDE.md). Chạy: python3 src/jft/nghe/build_ln1.py rồi python3 src/build_data.py"""
import json, html, shutil, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from furi import furi
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')) + '/'
IMG = 'app/media/jft/img/'; AU = 'app/media/jft/au/'
SRC = '/tmp/ln2/out/'
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
def L(n, q, vi, opts, a, script, dich, gt, pics=True, part=False):
    t = f'<span class="jp">{J(q)}</span><br><span class="vi-q">{html.escape(vi)}</span>'
    o = [{'t': ('ABC'[i] + '. ' if pics else '') + J(x)} for i, x in enumerate(opts)]
    if pics:
        for i, d in enumerate(o): d['img'] = IMG + f'ln2_{n:02d}{"abc"[i]}.jpg'
    qs.append(dict(s='聴解', ins='', gset=None, gimg=None, gau=None, t=t, imgs=[], img=None,
                   au=AU + f'ln2_L{n:02d}.mp3', o=o, a=[a - 1], ex=EX(opts[a - 1], script, dich, gt, part)))

#DATA
L(1, '二人はいつ、映画を見に行きますか。', 'Hai người sẽ đi xem phim khi nào?',
  ['金曜日', '土曜日', '日曜日'], 1,
  'ヌン：ニアさん、映画、いつがいいですか？\nニア：私は、土曜日がいいです。ヌンさんは？\nヌン：すみません。土曜日はちょっと……。\nニア：私は、日曜日がいいです。\nヌン：あー、私は、日曜日はだめです。すみません。じゃあ、金曜日の夜は？\nニア：金曜日……だいじょうぶです。\nヌン：じゃあ、金曜日にしましょう。',
  'Nun: Nia, đi xem phim hôm nào được? / Nia: Tôi thì thứ Bảy. Còn Nun? / Nun: Xin lỗi, thứ Bảy thì hơi… / Nia: Vậy Chủ nhật. / Nun: Chủ nhật tôi không được. Vậy tối thứ Sáu thì sao? / Nia: Thứ Sáu… được. / Nun: Vậy chọn thứ Sáu nhé.',
  'Hai ngày bị loại: 「土曜日はちょっと……」 (từ chối nhẹ), 「日曜日はだめです」 (không được). Chốt bằng 「金曜日にしましょう」. Câu hỏi "khi nào" → nghe câu cuối có 〜にしましょう.', pics=False)
L(2, 'ミラさんは日本で何をしたいですか。', 'Mira muốn làm gì ở Nhật?',
  ['京都に行く', '雪を見る', 'ハンバーガーを食べる'], 2,
  'これ、ディズニーランドのお土産。ミラさん、どうぞ。\nわあ、清水さん、ありがとうございます。ディズニーランド行きたいです。\n面白いよ。ぜひ行って。ミラさんは、他に日本で何がしたい？\nそうですね。雪が見たいです。あと、温泉に入りたいです。\nへえ、いいね。',
  'Đây là quà Disneyland, tặng Mira. – Cảm ơn anh Shimizu. Tôi muốn đi Disneyland. – Vui lắm, nhất định đi nhé. Ở Nhật Mira còn muốn làm gì nữa? – Tôi muốn ngắm tuyết. Ngoài ra muốn tắm suối nước nóng.',
  '「雪が見たいです」 → tranh B (người đứng giữa tuyết rơi). Mẫu Nが見たい = muốn xem N. Các tranh còn lại (Kyoto, hamburger) không được nhắc đến.')
L(3, 'タムさんの国には、どんな季節がありますか。', 'Ở nước của Tam có những mùa nào?',
  ['夏はとても暑くて、冬はとても寒い', '一年中暑い', '雨季と乾季がある'], 3,
  'A：タムさんの国には、どんな季節がありますか？\nB：雨季と乾季があります。\nA：そうですか。\nB：乾季はとても暑いです。\nA：へー。\nB：でも、雨季は少しすずしくなります。雨がたくさん降ります。',
  'A: Nước của Tam có những mùa nào? / B: Có mùa mưa và mùa khô. Mùa khô rất nóng. Nhưng mùa mưa thì mát hơn một chút. Mưa rất nhiều.',
  '「雨季と乾季があります」 → tranh C (nắng và mưa). 雨季 (VŨ QUÝ, うき) = mùa mưa, 乾季 (CAN QUÝ, かんき) = mùa khô. So sánh Đề nghe 1 câu 9: 四季 (bốn mùa) = tranh A.')
L(4, '何のお祝いですか。', 'Mừng dịp gì vậy?',
  ['誕生日', '結婚', '子どもが生まれた'], 2,
  'A：ご結婚おめでとうございます。\nB：え、あ、ありがとう。\nC：これ、私たちからのプレゼントです。\nB：えー、ありがとう。うれしい。\nA：相手は、どんな人ですか？\nB：うーんと、まあ、普通の人。\nA：かっこいいですか？\nB：うーん、ぜんぜん。でも、すごくおもしろい人。\nC：いいなあ。お幸せに。',
  'A: Chúc mừng chị kết hôn. / B: À, cảm ơn. / C: Đây là quà của chúng tôi. / A: Người kia là người thế nào? / B: Ừm, bình thường thôi. / A: Có đẹp trai không? / B: Hoàn toàn không. Nhưng rất hài hước. / C: Ghen tị quá. Chúc hạnh phúc.',
  'Câu đầu 「ご結婚おめでとうございます」 → tranh B. 相手 (あいて) = người bạn đời. 「お幸せに」 = chúc hạnh phúc, chỉ dùng khi chúc cưới.')
L(5, '皆はアナさんに何をあげますか。', 'Mọi người sẽ tặng gì cho Anna?',
  ['花', 'デジタルフォトフレーム', 'カメラ'], 2,
  'エレノア：あと、アナさんに何かプレゼントをあげませんか？\n周：そうですね。何がいいでしょうか？エレノアさんの国では、どんなものをあげますか？\nエレノア：花とか？\n周：うーん、もっと、思い出に残るものがいいと思います。予算は？\nエレノア：参加者は10人ぐらいだと思いますから、5,000円ぐらいのものですね。\n周：それなら、デジタルフォトフレームはどうですか？\nエレノア：あ、いいですね。',
  'Eleanor: Mình tặng Anna món quà gì không? / Chu: Tặng gì thì hay? Ở nước chị người ta tặng gì? / Eleanor: Hoa chẳng hạn? / Chu: Tôi nghĩ nên tặng thứ để lại kỷ niệm. Ngân sách bao nhiêu? / Eleanor: Khoảng 10 người, nên món khoảng 5.000 yên. / Chu: Vậy khung ảnh kỹ thuật số thì sao? / Eleanor: Hay đấy.',
  'Hoa (花) bị gạt đi: 「もっと、思い出に残るものがいい」. Chốt 「デジタルフォトフレームはどうですか」「いいですね」 → tranh B. Cùng hội thoại với Đề nghe 1 câu 11 (đó hỏi món ăn).', part=True)
L(6, '渡した物は何ですか。', 'Vật đã trao là gì?',
  ['魚のソース', '春巻き', 'お米から作ったお酒'], 3,
  'A：先生、お酒、好きですよね？\nB：うん、大好きだけど……。\nA：これ、スラーソーです。カンボジアのお酒です。先生にプレゼントです。\nB：え、いいの？\nA：お米から作った焼酎です。\nB：へー、焼酎、大好き。ありがとう。\nA：ちょっと強いですから、飲みすぎないでくださいね。',
  'A: Thầy thích rượu phải không ạ? / B: Ừ, rất thích, nhưng mà… / A: Đây là Sraa Sor, rượu của Campuchia. Em tặng thầy. / B: Được à? / A: Là rượu shochu làm từ gạo. / B: Thích shochu lắm. Cảm ơn. / A: Rượu hơi mạnh, thầy đừng uống quá nhiều nhé.',
  'Món quà là rượu Sraa Sor 「お米から作った焼酎」 → tranh C (chai rượu trong, có hộp). Tranh A là chai nước mắm, tranh B là chả giò. 飲みすぎないで = đừng uống quá nhiều (Vすぎる).')
L(7, '沖縄はどんなところですか。', 'Okinawa là nơi như thế nào?',
  ['食べ物がおいしい', '暖かい', '遊園地がある'], 2,
  'A：いつか沖縄に行ってみたいんです。海がきれいですよね。\nB：ええ、きれいですよ。それに暖かいから、春から秋まで泳げますよ。シュノーケリングもできますし。\nA：そうなんですか。\nB：あと、大きい水族館があって、きれいな魚が見られますよ。\nA：行きたいですね。',
  'A: Một ngày nào đó tôi muốn thử đi Okinawa. Biển đẹp nhỉ. / B: Vâng, đẹp lắm. Hơn nữa vì ấm áp nên có thể bơi từ mùa xuân đến mùa thu. Còn lặn ống thở được nữa. Ngoài ra có thủy cung lớn, ngắm cá đẹp.',
  '「暖かいから、春から秋まで泳げます」 → tranh B (biểu đồ nhiệt độ cao quanh năm, người ở biển). Bài không nói về đồ ăn hay khu vui chơi.')
L(8, '自由席は何号車ですか。', 'Ghế tự do là toa số mấy?',
  ['2・3・4・8・9号車', '5・6・7号車', '1号車'], 2,
  '11時42分発特急サンダーバード19号金沢行きは、11番乗り場から発車します。列車は9両で到着します。前から9号車8号車の順でいちばん後ろが1号車です。自由席は5号車、6号車、7号車、指定席は2号車、3号車、4号車、8号車、9号車、グリーン席は1号車です。',
  'Tàu tốc hành Thunderbird số 19 đi Kanazawa, khởi hành 11 giờ 42, xuất phát từ sân ga 11. Tàu có 9 toa, từ phía trước là toa 9, 8… cuối cùng là toa 1. Ghế tự do là toa 5, 6, 7; ghế chỉ định là toa 2, 3, 4, 8, 9; ghế Green là toa 1.',
  '自由席 (TỰ DO TỊCH) = ghế không đặt trước → 5・6・7号車 (tranh B). 指定席 (CHỈ ĐỊNH TỊCH) = ghế đặt trước (tranh A), グリーン席 = ghế hạng sang (tranh C). Bài có nhiều số – chỉ ghi số đi sau từ được hỏi.')
L(9, '電車はどうして運転を見合わせていますか。', 'Tại sao tàu điện phải tạm dừng chạy?',
  ['大雨', '人身事故', '大雪'], 2,
  'アナウンス：お客様にご案内いたします。浦和駅と赤羽駅の間で発生した人身事故の影響で、京浜東北線、高崎線、宇都宮線、上野東京ライン、湘南新宿ラインは、全線で運転を見合わせています。大宮方面へお越しのお客様は、埼京線をご利用ください。\n乗客：すみません、さいたま新都心に行きたいんですけど、京浜東北線、動かないんですか？\n駅員：ええ、申し訳ありません。さいたま新都心なら、埼京線の北与野駅から歩けますよ。',
  'Thông báo: Do ảnh hưởng của tai nạn có người xảy ra giữa ga Urawa và ga Akabane, các tuyến Keihin-Tohoku, Takasaki… đang tạm dừng toàn tuyến. Quý khách đi hướng Omiya xin dùng tuyến Saikyo. / Khách: Tôi muốn đến Saitama-Shintoshin, tuyến Keihin-Tohoku không chạy à? / Nhân viên: Vâng, xin lỗi. Đến Saitama-Shintoshin thì đi bộ từ ga Kita-Yono của tuyến Saikyo được.',
  '「人身事故の影響で」 = do tai nạn có người (người bị tàu đâm) → tranh B (va chạm ở chỗ chắn tàu). 見合わせる = tạm dừng (chạy tàu). 〜の影響で = do ảnh hưởng của ~.', part=True)
L(10, 'エドさんは、これから何をしたいですか。', 'Từ bây giờ Ed muốn làm gì?',
  ['東照宮に行く', '中禅寺湖に行く', '温泉に入る'], 3,
  '坂本：今日は、どこに行きましたか？\nエド：今日は、東照宮に行きました。明日は、中禅寺湖に行くつもりです。\n坂本：おいしいものは、何か食べましたか？\nエド：はい、そばを食べました。ゆばも食べてみたいです。\nエド：あと、温泉に入りたいんですけど、どこで入ったらいいですか？\n坂本：温泉ですか。中禅寺湖のホテルに、日帰りでお風呂に入れるところがあると思いますよ。',
  'Sakamoto: Hôm nay anh đi đâu? / Ed: Hôm nay đi Toshogu. Mai định đi hồ Chuzenji. / Sakamoto: Đã ăn món gì ngon chưa? / Ed: Ăn soba rồi. Muốn thử yuba nữa. Ngoài ra tôi muốn tắm suối nước nóng, nên tắm ở đâu? / Sakamoto: Khách sạn ở hồ Chuzenji có chỗ cho tắm trong ngày.',
  'Cùng bài với Đề nghe 1 câu 18, nhưng câu hỏi khác: 「これから何をしたいですか」 → 「温泉に入りたいんですけど」 → tranh C. 東照宮 là việc đã làm hôm nay (行きました), 中禅寺湖 là dự định (つもり).', part=True)
L(11, '大阪で、何をしましたか。', 'Ở Osaka, người này đã làm gì?',
  ['大阪城と通天閣に行った', '海で泳いだ', 'ケーブルカーに乗った'], 1,
  'A：これ、お菓子、どうぞ。大阪のお土産です。\nB：ありがとうございます。大阪に行ったんですね。どうでしたか？\nA：大阪城とか通天閣とか、いろいろなところに行けて、よかったです。\nB：へー、串カツも食べましたか？\nA：いえ。でも、たこ焼きを食べました。おいしかったです。\nA：あと、あべのハルカスに登りました。すごく高いビルですね。びっくりしました。',
  'A: Bánh kẹo đây, quà Osaka. / B: Cảm ơn. Anh đi Osaka à, thế nào? / A: Đi được nhiều nơi như lâu đài Osaka, tháp Tsutenkaku, vui lắm. / B: Có ăn kushikatsu không? / A: Không, nhưng ăn takoyaki, ngon lắm. Ngoài ra lên tòa Abeno Harukas, cao quá, ngạc nhiên luôn.',
  '「大阪城とか通天閣とか…行けて」 → tranh A (tháp + lâu đài). 〜とか〜とか = nào là ~ nào là ~ (liệt kê ví dụ).')
L(12, 'どんなイベントのお知らせですか。', 'Thông báo về sự kiện gì?',
  ['コンサート', '花火大会', '野菜の販売会'], 3,
  '町役場から、野菜の販売会についてお知らせします。明日、7月28日、日曜日、午前8時30分から、「あおぞら広場」において、地元の農家が生産した新鮮な夏野菜の販売会が行われます。皆様のご来場をお待ちしています。',
  'Ủy ban thị trấn xin thông báo về buổi bán rau. Ngày mai Chủ nhật 28/7, từ 8 giờ 30 sáng, tại quảng trường "Aozora" sẽ có buổi bán rau mùa hè tươi do nông dân địa phương sản xuất. Rất mong quý vị đến tham dự.',
  '「野菜の販売会」 = buổi bán rau → tranh C. 販売 (PHIẾN MẠI) = bán. 〜において = tại ~ (cách nói trang trọng của 〜で).')
L(13, '何について話していますか。', 'Họ đang nói về điều gì?',
  ['魚の販売', 'フリーマーケット', '花火大会'], 2,
  'A：あのう、市役所でフリーマーケットがあるそうですね。\nB：ええ。毎月、第二土曜日に、市役所の前の広場でやってますよ。\nA：第二土曜日？\nB：月の2回目の土曜日です。今月は14日でしたから、次は来月ですね。\nA：あのう、どんなものを売ってますか？\nB：服が多いけど、食器とか、おもちゃとか、いろいろあると思いますよ。\nA：天気が悪かったら、どうなりますか？\nB：雨が降ったら、中のホールでやります。',
  'A: Nghe nói ở tòa thị chính có chợ đồ cũ? / B: Vâng, mỗi tháng vào thứ Bảy thứ hai, ở quảng trường trước tòa thị chính. Tháng này là ngày 14 rồi, nên lần tới là tháng sau. / A: Bán những gì? / B: Nhiều quần áo, ngoài ra có bát đĩa, đồ chơi… / A: Trời xấu thì sao? / B: Mưa thì tổ chức trong hội trường.',
  '「フリーマーケット」 = chợ đồ cũ → tranh B (bày quần áo, đồ chơi). 第二土曜日 = thứ Bảy tuần thứ hai của tháng.')
L(14, 'アルニさんはどんな種類の家に住んでいますか。', 'Aruni đang sống trong loại nhà nào?',
  ['アパート', 'マンション', '古い日本の家'], 1,
  '前田：アルニさんは？\nアルニ：私は、北町のアパートに住んでいます。\nビサル：きれいですか？\nアルニ：はい、きれいです。でも、ちょっと古いです。\nビサル：そうですか。静かですか？\nアルニ：いえ。近くに学校があります。あまり静かじゃないです。',
  'Maeda: Còn Aruni? / Aruni: Tôi sống ở căn hộ (apāto) ở Kitamachi. / Bisal: Có sạch đẹp không? / Aruni: Có, nhưng hơi cũ. / Bisal: Có yên tĩnh không? / Aruni: Không, gần đó có trường học. Không yên tĩnh lắm.',
  '「アパートに住んでいます」 → tranh A (nhà 2 tầng nhiều phòng). アパート = nhà cho thuê thấp tầng, マンション = chung cư cao tầng kiên cố (tranh B). 「ちょっと古い」 không có nghĩa là nhà kiểu Nhật cũ (tranh C).')
L(15, '国際交流フェスティバルのカラオケ大会には、だれが参加できますか。', 'Ai có thể tham gia cuộc thi karaoke của Lễ hội giao lưu quốc tế?',
  ['中学生だけ', '中学生以上ならだれでも（プロ以外）', 'プロの歌手'], 2,
  'ヨス：すみません。今度、国際交流フェスティバルで、カラオケ大会があると聞きました。だれでも参加できますか？\n係の人：カラオケ大会ですね。はい。中学生以上でしたら、だれでも参加できます。でも、プロの方はご遠慮いただいています。\nヨス：えんりょ？\n係の人：プロの人は出られません。\nヨス：わかりました。友だちと2人で出てもいいですか？\n係の人：だいじょうぶですよ。',
  'Yosu: Tôi nghe nói lễ hội giao lưu quốc tế có thi karaoke. Ai cũng tham gia được không? / Nhân viên: Từ học sinh cấp 2 trở lên thì ai cũng tham gia được. Nhưng người chuyên nghiệp thì xin không tham gia. / Yosu: Enryo? / Nhân viên: Người chuyên nghiệp không được tham gia. / Yosu: Hát cùng bạn 2 người được không? / Nhân viên: Được.',
  '「中学生以上でしたら、だれでも参加できます」 = từ cấp 2 trở lên ai cũng được, 「プロの方はご遠慮いただいています」 = trừ người chuyên nghiệp → tranh B (nhiều lứa tuổi). 以上 (DĨ THƯỢNG) = trở lên.', part=True)
L(16, 'お正月休みに、ナンさんは何をしましたか。', 'Trong kỳ nghỉ năm mới, Nan đã làm gì?',
  ['家でテレビを見た', 'ディズニーランドに行った', '家族とお正月を過ごした'], 2,
  '山口：ナンさん、お正月休みは、どうでしたか？\nナン：東京に住んでいる友だちのところに行きました。\nナン：いっしょに、すごく混んでいて、びっくりしました。ディズニーランドに行きましたが、待ち時間がとても長くて、乗り物に3つしか乗れませんでした。\n山口：ああ、それは大変でしたね。\nナン：はい。でも、友だちと久しぶりに会えて、よかったです。',
  'Yamaguchi: Kỳ nghỉ Tết của Nan thế nào? / Nan: Tôi đến chỗ bạn sống ở Tokyo. Cùng đi Disneyland nhưng đông quá, chờ lâu nên chỉ chơi được 3 trò. / Yamaguchi: Vất vả nhỉ. / Nan: Vâng, nhưng lâu rồi mới gặp bạn nên vui.',
  '「ディズニーランドに行きました」 → tranh B. 〜しか〜ない = chỉ ~ (乗り物に3つしか乗れませんでした = chỉ chơi được 3 trò).', part=True)
L(17, 'ひな祭りに、何を食べたり飲んだりしますか。', 'Vào Lễ hội bé gái (Hina matsuri), người ta ăn và uống gì?',
  ['ちらしずしと甘酒', 'おにぎりとお酒', 'ちらしずしとお茶'], 1,
  'A：みなさんも、どうぞ。\nB：わあ、すごい。いただきます。これは何の料理ですか？\nA：ちらしずしです。今日はひな祭りだから、家で作って来たんです。\nB：このおすしは、ひな祭りに食べるんですか？\nA：そう。あと、ひな祭りには、甘酒を飲んだりもしますよ。\nB：え、甘酒って、お酒ですよね？\nA：甘酒は、お酒じゃなくて、お米から作った飲み物です。アルコールは入っていないから、だいじょうぶですよ。',
  'A: Mọi người dùng đi. / B: Đây là món gì? / A: Là chirashizushi. Hôm nay là Hina matsuri nên tôi làm ở nhà mang đến. Ngày Hina matsuri còn uống amazake nữa. / B: Amazake là rượu à? / A: Amazake không phải rượu, là đồ uống làm từ gạo. Không có cồn nên không sao.',
  'Ăn 「ちらしずし」 + uống 「甘酒」 → tranh A (cơm chirashi + chén đồ uống màu trắng). 甘酒 (CAM TỬU) tuy có chữ 酒 nhưng không có cồn – nên không phải tranh B (お酒).', part=True)
L(18, 'なくしたのは、どのスマホですか。', 'Chiếc điện thoại bị mất là chiếc nào?',
  ['赤いカバー・犬の絵', '黒いカバー・犬の絵', '赤いカバー・猫の絵'], 1,
  '徐：あのう、すみません。スマホをなくしてしまったんですけど、届いてませんか？\nスタッフ：スマートフォンですか。お調べしますので、特徴を教えてください。\n徐：えっと……スマホの色は黒で、犬の絵の赤いカバーがついています。\nスタッフ：そうですか。機種は？\n徐：iPhoneです。',
  'Xu: Xin lỗi, tôi làm mất điện thoại, có ai mang đến không? / Nhân viên: Điện thoại thông minh à. Tôi sẽ kiểm tra, anh cho biết đặc điểm. / Xu: Điện thoại màu đen, có ốp màu đỏ in hình con chó. / Nhân viên: Loại máy gì? / Xu: iPhone.',
  'Nghe 2 đặc điểm: ốp 「赤いカバー」 + hình 「犬の絵」 → tranh A. Bẫy: 「スマホの色は黒」 là màu máy (bị ốp che), nên tranh B (ốp đen) sai; tranh C là hình mèo.', part=True)
L(19, 'この島の習慣では、お酒はどのように飲みますか。', 'Theo phong tục của hòn đảo này, người ta uống rượu như thế nào?',
  ['それぞれ自分のコップで飲む', 'みんなで乾杯して飲む', '一つの小さいコップで順番に飲む'], 3,
  'B：あ、でも、この島には、お酒を飲むとき、特別な習慣があるんですよ。\nA：特別な習慣？\nB：はい。「オトーリ」っていって、はじめにだれかがあいさつをしてから、小さいコップにお酒を入れて飲みます。そのあと、そのコップで、順番に全員がお酒を飲むんです。全員が飲んだら、次の人があいさつをして、またみんなで順番にお酒を飲んで……てくり返すんです。\nA：それは、たくさんお酒を飲まなければなりませんか？\nB：いえ、「もう飲めません」って言えば、だいじょうぶです。',
  'B: Ở hòn đảo này có phong tục đặc biệt khi uống rượu. Gọi là "Otori": đầu tiên một người chào mọi người, rót rượu vào chiếc cốc nhỏ và uống. Sau đó cả nhóm lần lượt uống bằng chính chiếc cốc đó. Khi mọi người uống xong, người tiếp theo chào, rồi lại lần lượt uống… cứ lặp lại như vậy. / A: Phải uống nhiều lắm à? / B: Không, nói "tôi không uống thêm được nữa" là được.',
  '「小さいコップにお酒を入れて…そのコップで、順番に全員がお酒を飲む」 → một cốc nhỏ, uống lần lượt → tranh C. 順番に (THUẬN PHIÊN) = lần lượt.', part=True)
L(20, 'ロイさんは、どうしてレジの人に怒られましたか。', 'Tại sao Roy bị nhân viên thu ngân trách?',
  ['お金を払う前にジュースを飲んだから', 'ジュースを持って店を出たから', 'ジュースを買わなかったから'], 1,
  'ロイ：昨日、スーパーでレジに並びました。すごく混んでいました。\nロイ：のどが渇いたから、かごのジュースを開けて飲みました。そのあと、レジでお金を払うとき「これも飲みましたから、お願いします」と言って、空のボトルを出しました。そうしたら、レジの人にすごく怒られました。\n小林：え、お金を払わないで、ジュース飲んだの？\nロイ：はい。\n小林：ああ、それはだめだよ。ちゃんとお金を払ってから飲まなきゃ。',
  'Roy: Hôm qua tôi xếp hàng ở quầy tính tiền siêu thị, đông lắm. Khát nước nên mở chai nước trái cây trong giỏ ra uống. Lúc trả tiền tôi nói "Cái này tôi uống rồi, tính giúp" rồi đưa chai rỗng. Thế là bị nhân viên mắng. / Kobayashi: Hả, chưa trả tiền mà uống à? Không được đâu. Phải trả tiền xong rồi mới uống.',
  '「お金を払わないで、ジュース飲んだ」 → uống trước khi trả tiền → tranh A. 怒られる = bị mắng (thể bị động của 怒る). 払ってから飲まなきゃ = phải trả tiền rồi mới uống.', part=True)

new = {'id': 'jft-ln2', 'group': 'Luyện nghe JFT', 'title': 'Đề nghe 2', 'name': 'Nghe 2',
       'sub': 'Tuyển tập 20 câu nghe hiểu · いろどり', 'time': 30, 'tag': 'Luyện nghe', 'qs': qs}
P = REPO + 'src/raw/jft_exams.json'
d = json.load(open(P, encoding='utf-8'))
d = [e for e in d if e['id'] != 'jft-ln2']
i = next(k for k, e in enumerate(d) if e['id'] == 'jft-ln1')
d.insert(i + 1, new)
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Đề nghe 2:', len(qs), 'câu')
