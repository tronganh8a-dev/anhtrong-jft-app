"""Đề nghe 4 (16/11/2026): JLPT N4 聴解 – cấp độ tầm trung, 28 câu (もんだい1: 8, もんだい2: 7, もんだい3: 5, もんだい4: 8).
Nguồn: video "Nghe tổng hợp N4 cấp độ trung" anh gửi (Part 1 = đề, Part 2 = script + đáp án).
Audio cắt từ Part 1 (bỏ phần tích tắc suy nghĩ), ảnh phương án cắt từng ô (không lấy khung/logo video).
Script chép từ phụ đề Part 2 (đã sửa chính tả, ghép câu); dịch + giải thích do Anh Trọng Dạy JFT soạn.
Cần /tmp/ln4/out/img và /tmp/ln4/out/au. Chạy: python3 src/jft/nghe/build_ln4.py rồi python3 src/build_data.py"""
import json, html, shutil, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from furi import furi
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')) + '/'
IMG = 'app/media/jft/img/'; AU = 'app/media/jft/au/'
SRC = '/tmp/ln4/out/'
if os.path.isdir(SRC):
    for f in os.listdir(SRC + 'img'): shutil.copy(SRC + 'img/' + f, REPO + 'public/' + IMG + f)
    for f in os.listdir(SRC + 'au'): shutil.copy(SRC + 'au/' + f, REPO + 'public/' + AU + f)

J = lambda t: furi(html.escape(t)).replace('\n', '<br>')
def EX(ans, script, dich, gt):
    s = f'<div class="ans">Đáp án đúng: <span class="jp">{J(ans)}</span></div>'
    s += f'<span class="lb">SCRIPT</span><div class="jp">{J(script)}</div>'
    s += f'<span class="lb">DỊCH</span><div>{html.escape(dich).replace(chr(10), "<br>")}</div><span class="lb">GIẢI THÍCH</span><div>{J(gt)}</div>'
    return s
qs = []
MON = {1: 'もんだい1', 2: 'もんだい2', 3: 'もんだい3', 4: 'もんだい4'}

def Q(m, n, q, vi, opts, a, script, dich, gt, pics=False, scene=False):
    """m = もんだい, n = số câu, opts = list text (pics=True: 4 tranh, text là số), a = đáp án 1-based."""
    head = f'<span class="lb">{MON[m]} · {n}番</span><br>'
    t = head + (f'<span class="jp">{J(q)}</span><br>' if q else '') + f'<span class="vi-q">{html.escape(vi)}</span>'
    o = []
    for i, x in enumerate(opts):
        d = {'t': J(x)}
        if pics: d['img'] = IMG + f'ln4_{m}{n}{"abcd"[i]}.jpg'
        o.append(d)
    ans = opts[a - 1] if not pics else f'Tranh {a}'
    qs.append(dict(s='聴解', ins='', gset=None, gimg=None, gau=None, t=t, imgs=[],
                   img=(IMG + f'ln4_{m}{n}.jpg') if scene else None,
                   au=AU + f'ln4_{m}{n}.mp3', o=o, a=[a - 1], ex=EX(ans, script, dich, gt)))

P4 = ['1', '2', '3', '4']; P3 = ['1', '2', '3']

# ===== もんだい1 – 課題理解 =====
Q(1, 1, 'どんな髪にしますか。', 'Người khách sẽ cắt tóc kiểu nào?', P4, 3,
  '（美容院で女の人と男の人が話しています。どんな髪にしますか。）\nA：この写真のように短く切ってください。\nB：耳がちょっと出るくらいですね。かなり短いですが、大丈夫ですか。\nA：うん。\nB：そうですね……この下の方がいいですね。\nA：わかりました。前はどうですか。これくらいでいいですか。\nB：ああ、前ももう少し長い方がいいですね。\nA：じゃあ、この左のがちょうどいいですね。\nB：そうですね。',
  'Ở tiệm làm tóc. – Cắt ngắn như ảnh này giúp tôi. – Ngắn đến mức lộ tai một chút nhỉ. Khá ngắn đấy, có sao không? – Ừ. … – Phía trước thì sao, cỡ này được chưa? – À, phía trước dài thêm một chút thì hơn. – Vậy cái bên trái này là vừa nhỉ. – Đúng vậy.',
  'Hai điều kiện: 「耳がちょっと出る」 (lộ tai một chút) → loại tranh 2, 4 (tóc che tai); 「前ももう少し長い方がいい」 (mái dài hơn) → tranh 3 (mái dài chấm mắt), không phải tranh 1 (mái ngắn). 髪 (PHÁT) = tóc; 耳 (NHĨ) = tai; 短い (ĐOẢN) = ngắn.', pics=True)
Q(1, 2, '男の人はどの携帯電話を買いますか。', 'Người đàn ông mua điện thoại nào?',
  ['軽い携帯電話', 'サイズが大きい携帯電話', 'いろいろできる携帯電話', '写真がきれいに撮れる携帯電話'], 1,
  '（店で男の人と店員が話しています。男の人はどの携帯電話を買いますか。）\n男：あの、スマホを新しくしようと思って。\n店員：わかりました。では、こちらはいかがでしょう。写真がきれいに撮れます。\n男：うんうん。ちょっと重いですね。\n店員：これは軽いですよ。サイズは変わっていませんが、10グラム軽くなったんです。\n男：へえ、そうなんですか。\n店員：あと、これもおすすめです。少し高くなりますが、いろいろできて、とても便利です。\n男：そうですか。でも、そんなに便利でなくてもいいので、こっちにします。',
  'Khách: Tôi định đổi điện thoại mới. – NV: Cái này thì sao ạ? Chụp ảnh đẹp. – Hơi nặng nhỉ. – Cái này nhẹ ạ. Kích thước không đổi nhưng nhẹ hơn 10 gram. – Ồ vậy à. – Cái này cũng nên dùng, đắt hơn chút nhưng làm được nhiều thứ, rất tiện. – Không cần tiện đến vậy, tôi lấy cái này.',
  'Máy chụp ảnh đẹp bị chê 「ちょっと重い」; máy tiện lợi bị từ chối 「そんなに便利でなくてもいい」 → còn lại máy nhẹ (1). Chú ý 「サイズは変わっていません」 → không phải máy cỡ lớn. 軽い (KHINH) = nhẹ ↔ 重い (TRỌNG) = nặng.')
Q(1, 3, '参加したい客は何をしますか。', 'Khách muốn tham gia sẽ làm gì?', P4, 4,
  '（動物園で女の人が話しています。参加したい客は何をしますか。）\n女：皆さん、今日はさくら動物園にお越しいただき、ありがとうございます。1時から、動物園の中を係の者がご案内します。途中、動物に食べ物をやったり、触ったりすることができます。食べ物のお金は百円ですが、参加は無料です。時間は全部で1時間ぐらいです。参加する方は、動物園の入り口の近くにお集まりください。ぜひ、ご家族でご参加ください。以上です。',
  'Cảm ơn quý khách đã đến vườn thú Sakura. Từ 1 giờ, nhân viên sẽ dẫn tham quan. Trên đường có thể cho thú ăn, sờ thú. Tiền đồ ăn 100 yên nhưng tham gia miễn phí. Tổng khoảng 1 tiếng. Ai tham gia xin tập trung gần cổng vào vườn thú.',
  'Câu hỏi 「何をしますか」 = việc phải làm (trước tiên) → 「入り口の近くにお集まりください」 → tranh 4 (tập trung ở cổng). Cho ăn, sờ thú (tranh 1, 2) là việc làm trong lúc tham quan; tham gia miễn phí nên không cần mua vé (tranh 3). 入り口 (NHẬP KHẨU) = lối vào; 集まる (TẬP) = tập trung; 無料 (VÔ LIỆU) = miễn phí.', pics=True)
Q(1, 4, '男の人はこの後すぐ何をしますか。', 'Ngay sau đây người đàn ông làm gì?', P4, 4,
  '（男の人と女の人が話しています。男の人はこの後すぐ何をしますか。）\n女：そろそろ引っ越し会社の人が来るね。この箱も閉めちゃうよ。\n男：ちょっと待って。まだ何冊か入れてない本がある。\n女：どこにあるの？\n男：あそこの机の上。\n女：あ、全部入れて。あ、パソコン、落とさないように気をつけてね。\n男：わかった。この棚のCDも一緒に入れていい？\n女：それはいい。別の箱に入れるから。',
  'Nữ: Sắp đến lúc người công ty chuyển nhà tới rồi. Tôi đóng thùng này lại nhé. – Nam: Đợi chút, còn mấy cuốn sách chưa cho vào. – Ở đâu? – Trên bàn đằng kia. – À, cho hết vào đi. Cẩn thận đừng làm rơi máy tính nhé. – Ừ. CD trên kệ cho chung vào được không? – Cái đó thì thôi, để thùng khác.',
  'Việc ngay sau đây: cho mấy cuốn sách còn lại vào thùng (「まだ何冊か入れてない本」「全部入れて」) → tranh 4. CD thì 「別の箱に入れる」 (để thùng khác) nên không phải tranh 3. 何冊 = mấy cuốn (冊 SÁCH: đếm sách); 箱 (TƯƠNG) = thùng, hộp.', pics=True)
Q(1, 5, '客は何時にどこに集まらなければなりませんか。', 'Khách phải tập trung ở đâu, lúc mấy giờ?', P4, 4,
  '（バスの中で女の人が話しています。客は何時にどこに集まらなければなりませんか。）\n女：皆さん、バスはもうすぐ美術館に着きます。10時から2時間ほど、自由に見て楽しんでください。12時にまたバスが出発しますから、10分前には駐車場に集まってください。今、美術館から駐車場まで歩いて5分ほどかかりますから、ご注意ください。',
  'Xe buýt sắp đến bảo tàng mỹ thuật. Từ 10 giờ, mọi người tự do tham quan khoảng 2 tiếng. 12 giờ xe xuất phát nên hãy tập trung ở bãi đỗ xe trước 10 phút. Từ bảo tàng ra bãi đỗ đi bộ mất khoảng 5 phút, xin lưu ý.',
  '12時に出発 – 「10分前には駐車場に」 → 11:50 ở bãi đỗ xe = tranh 4. Tranh 2 là 12:00 (giờ xe chạy), tranh 1, 3 ở bảo tàng. Con số 5 phút (đi bộ) chỉ là thông tin thêm. 駐車場 (TRÚ XA TRƯỜNG) = bãi đỗ xe; 美術館 (MỸ THUẬT QUÁN) = bảo tàng mỹ thuật.', pics=True)
Q(1, 6, '二人はこの後どの家具を買いますか。', 'Hai người sẽ mua đồ nội thất nào?', P4, 4,
  '（男の人と女の人が家具について話しています。二人はこの後どの家具を買いますか。）\n女：このソファー、すごく気持ちがいいよ。ちょっと座ってみて。\n男：いいよ。ソファーは今必要ないから。それより、テーブルを見ないと。\n女：ああ、そうか。\n男：これはどう？安いよ。\n女：でも、これ、二人しか座れないよ。四人は座れるのがいいな。\n男：わかった。これはちょうどいいんじゃない？\n女：そうだね。値段も安いし。あ、でもこっちの丸い方がいいな。椅子がかわいい。\n男：ちょっと高いよ。\n女：いいの？\n男：いいよ、これぐらい。',
  'Nữ: Sofa này êm lắm, ngồi thử đi. – Nam: Thôi, giờ chưa cần sofa. Phải xem bàn đã. – Cái này thì sao? Rẻ đấy. – Nhưng chỉ 2 người ngồi được. Muốn loại 4 người ngồi được. – Cái này vừa nhỉ? – Ừ, giá cũng rẻ. À nhưng cái tròn này thích hơn, ghế dễ thương. – Hơi đắt đấy. – Được không? – Được, cỡ này thì được.',
  'Loại sofa (1) vì 「今必要ない」; loại bàn 2 người (2); bàn 4 người (3) được khen nhưng sau đó chọn 「こっちの丸い方」 và nam đồng ý 「いいよ、これぐらい」 → tranh 4 (bàn tròn). 家具 (GIA CỤ) = đồ nội thất; 丸い (HOÀN) = tròn; 椅子 = ghế.', pics=True)
Q(1, 7, '男の人は何で行きますか。', 'Người đàn ông sẽ đi bằng gì?', ['自転車', 'タクシー', 'バス', '電車'], 4,
  '（電話で男の人と女の人が話しています。男の人は何で行きますか。）\n男：すみません、約束の11時に遅れそうなんです。\n女：そうですか。今どこですか。\n男：駅前のバス停です。でも、バスが全然来なくて。\n女：ええ。事故で道が混んでいるそうです。\n男：それなら、タクシーもだめですね。\n女：ええ。\n男：自転車を貸してくれるところがあればいいんですが。\n女：まあ、地下鉄がありましたよ。それで近くまで来てください。\n男：え、そうなんですか。あ、じゃあ、そうします。',
  'Nam: Xin lỗi, có lẽ tôi sẽ trễ hẹn 11 giờ. – Bây giờ anh ở đâu? – Ở trạm xe buýt trước ga. Nhưng xe buýt mãi không đến. – Nghe nói đường tắc vì tai nạn. – Vậy taxi cũng không được nhỉ. – Giá có chỗ cho thuê xe đạp thì tốt. – À, có tàu điện ngầm đấy. Anh đi đến gần đây bằng tàu đi. – Ồ vậy à, vậy tôi làm thế.',
  'Xe buýt không đến, taxi cũng tắc đường, xe đạp chỉ là mong muốn (〜ればいいんですが). Chốt: 「地下鉄があります…そうします」 → đi tàu điện (地下鉄 = tàu điện ngầm) → 4 電車. 地下鉄 (ĐỊA HẠ THIẾT); 遅れる (TRÌ) = trễ; 混む = đông, tắc.')
Q(1, 8, '女の人は来週何曜日にアルバイトをしますか。', 'Tuần sau người phụ nữ làm thêm vào những thứ nào?',
  ['火曜日と木曜日', '火曜日と木曜日と金曜日', '火曜日と木曜日と金曜日と土曜日', '火曜日と木曜日と金曜日と土曜日と日曜日'], 3,
  '（女の人と店の人が話しています。女の人は来週何曜日にアルバイトをしますか。）\n店長：田中さん、アルバイトの日のことなんですが。\n女：はい、何でしょうか。\n店長：今、火曜日と木曜日の週2回ですよね。\n女：はい。\n店長：お店がだいぶ忙しくなったから、来週から金曜日にも来てくれませんか。\n女：金曜日ですか。わかりました。\n店長：来てくれますか。よかった。ええ、それと、実は土曜日と日曜日の人が急に来週休みになって。来週だけ土日もお願いしたいんです。\n女：そうですか。日曜日は難しいですが、土曜日ならいいですよ。\n店長：土曜日だけでも。じゃあ、お願いします。',
  'Quản lý: Hiện em làm thứ Ba và thứ Năm, 2 buổi/tuần nhỉ. Quán bận hơn nên từ tuần sau em đến thêm thứ Sáu được không? – Vâng. – Ngoài ra người làm thứ Bảy, Chủ nhật tuần sau đột nhiên nghỉ, chỉ tuần sau thôi, em làm cả thứ Bảy, Chủ nhật được không? – Chủ nhật thì khó, thứ Bảy thì được. – Thứ Bảy thôi cũng được, nhờ em.',
  'Cộng dồn: 火・木 (đang làm) + 金 (từ tuần sau) + 土 (chỉ tuần sau); 日曜日は難しい → không làm. → 3. 〜なら(いいですよ) = nếu là ~ thì được. 曜日: 火 HỎA (thứ Ba), 木 MỘC (thứ Năm), 金 KIM (thứ Sáu), 土 THỔ (thứ Bảy), 日 NHẬT (CN).')

# ===== もんだい2 – ポイント理解 =====
Q(2, 1, '女の人が乗るバスは何分後に出ますか。', 'Xe buýt người phụ nữ đi sẽ chạy sau bao nhiêu phút?', ['10分後', '20分後', '35分後', '50分後'], 2,
  '（女の人と男の人が話しています。女の人が乗るバスは何分後に出ますか。）\n女：すみません、空港へ行くバスは何番ですか。\n男：2番と3番です。\n女：ありがとうございます。何時に出発しますか。\n男：2番のバスは10分後に出発で、空港まで50分くらいかかります。3番のバスは20分後で、35分で行けます。でも、3番のバスの方がちょっと早く着きます。\n女：そうですか。じゃあ、3番のバスに乗ります。',
  'Nữ: Xe buýt ra sân bay là số mấy? – Nam: Số 2 và số 3. – Mấy giờ chạy? – Xe số 2 chạy sau 10 phút, mất khoảng 50 phút đến sân bay. Xe số 3 chạy sau 20 phút, đi mất 35 phút. Xe số 3 đến sớm hơn một chút. – Vậy tôi đi xe số 3.',
  'Chị chọn 「3番のバス」 → xe số 3 chạy 「20分後」. So sánh: số 2: 10 + 50 = 60 phút; số 3: 20 + 35 = 55 phút → đến sớm hơn. 35分 là thời gian đi, không phải giờ xuất phát. (Phương án trong video gốc ghi lệch với audio; app sửa lại theo audio.) 空港 (KHÔNG CẢNG) = sân bay; 出発 (XUẤT PHÁT).')
Q(2, 2, '女の人は誰と行きますか。', 'Người phụ nữ sẽ đi cùng ai?', ['一人で', 'ジョンさんと', 'マリアさんと', 'ジョンさんとマリアさん'], 3,
  '（男の人と女の人が話しています。女の人は誰と行きますか。）\n男：日曜日のコンサートなんだけど、ちょっと都合が悪くなって、行けなくなっちゃったんだ。\n女：ええ、そうなの。\n男：ジョンさんも行けなくなったって、今朝連絡があったんだよ。\n女：ええ、ジョンさんも？\n男：そうなんだ。\n女：うーん。マリアさんは？\n男：彼女は大丈夫。\n女：だから、二人で行ってくるよ。',
  'Nam: Buổi hòa nhạc Chủ nhật, anh có việc bận nên không đi được. – Nữ: Ơ, thế à. – John cũng báo sáng nay là không đi được. – John cũng vậy à? – Ừ. – Còn Maria? – Cô ấy thì được. – Vậy thì hai người (em và Maria) đi nhé.',
  'Người nói (nam) và John đều 「行けなくなった」; Maria 「大丈夫」 → 「二人で」 = chị + Maria → 3. Vなくなっちゃった = trở nên không thể V (đáng tiếc). 都合が悪い = không tiện, bận.')
Q(2, 3, '本が見つからない時、何をしますか。', 'Khi không tìm thấy sách thì làm gì?', ['機械で探す', '係の人に言う', 'ほかの図書館に行く', '本屋で買う'], 2,
  '（図書館で女の人が話しています。本が見つからない時、何をしますか。）\n女：この図書館では、本なら10冊まで15日間借りることができます。もし、ほかの人が予約していなかったら、さらに2週間借りられます。その場合は、もう一度図書館に来るか、電話で連絡してください。本を探す時は、あちらの機械が便利です。もし見つからない時は、係の者に相談してください。この図書館になかったら、ほかの図書館から借りたり、買ったりします。',
  'Thư viện này cho mượn tối đa 10 cuốn trong 15 ngày. Nếu không ai đặt trước có thể mượn thêm 2 tuần, khi đó hãy đến thư viện hoặc gọi điện. Tìm sách thì dùng máy đằng kia. Nếu không tìm thấy, hãy trao đổi với nhân viên phụ trách. Nếu thư viện không có, (thư viện) sẽ mượn từ thư viện khác hoặc mua.',
  '「もし見つからない時は、係の者に相談してください」 → 2. Máy (機械) là để tìm sách lúc đầu; mượn thư viện khác / mua là việc thư viện làm sau đó, người dùng không tự đi. 係 (HỆ) = người phụ trách; 相談 (TƯƠNG ĐÀM) = trao đổi, hỏi ý kiến.')
Q(2, 4, '女の人はいつもどのくらい練習しますか。', 'Người phụ nữ thường luyện tập khoảng bao lâu?', ['30分', '1時間', '2時間', '3時間'], 1,
  '（男の人と女の人が話しています。女の人はいつもどのくらい練習しますか。）\n女：田中さんはギターが上手ですね。どのくらいしているんですか。\n男：そうですね、もう7、8年です。\n女：そうですか。いつもどのくらい練習しているんですか。\n男：あの、学生の時は時間があったので、毎日3時間くらい練習していました。でも、今は1時間くらいです。\n女：そうですか。私もギターが好きですが、そんなに練習していません。しても30分ぐらいです。',
  'Nữ: Anh Tanaka chơi guitar giỏi nhỉ. Anh chơi bao lâu rồi? – Nam: Đã 7, 8 năm. – Thường luyện bao lâu? – Hồi sinh viên có thời gian nên mỗi ngày luyện khoảng 3 tiếng. Bây giờ khoảng 1 tiếng. – Vậy à. Tôi cũng thích guitar nhưng không luyện nhiều vậy. Có luyện cũng chỉ khoảng 30 phút.',
  'Câu hỏi về NGƯỜI PHỤ NỮ: 「しても30分ぐらいです」 → 1. 3時間 (hồi sinh viên) và 1時間 (bây giờ) là của anh Tanaka. 〜ても = dù có ~ thì cũng. 練習 (LUYỆN TẬP).')
Q(2, 5, '学生はどうして謝っていますか。', 'Tại sao sinh viên xin lỗi?',
  ['レポートが遅れるから', 'また電話をかけるから', '先生と約束した日を変えたいから', '先生が忙しいのに電話をかけたから'], 3,
  '（学生が先生の留守番電話にメッセージを入れています。学生はどうして謝っていますか。）\n学生：あ、もしもし、Bクラスのマリアです。あの、昨日お願いしたレポートのご相談についてです。今日、月曜日に予定が入ってしまったので、別の日にお願いしたいと思ってお電話しました。お忙しいのに、本当に申し訳ありません。また、お電話します。失礼します。',
  'Alo, em là Maria lớp B. Về buổi trao đổi bài báo cáo em đã nhờ hôm qua. Hôm nay (thứ Hai) em lỡ có việc nên muốn xin đổi sang ngày khác. Thầy bận mà em làm phiền, thật xin lỗi. Em sẽ gọi lại. Em xin phép.',
  'Lý do chính: 「月曜日に予定が入ってしまったので、別の日にお願いしたい」 = muốn đổi ngày đã hẹn với thầy → 3. 「お忙しいのに」 chỉ là câu xin lỗi lịch sự đi kèm; bài báo cáo không bị trễ. 謝る (TẠ) = xin lỗi; 予定 (DỰ ĐỊNH); 留守番電話 = máy trả lời tự động.')
Q(2, 6, '女の学生は国にいる時、何を勉強していましたか。', 'Khi ở nước mình, nữ sinh đã học gì?', ['医学', '経済', '日本の文化', '日本の小説'], 2,
  '（男の学生と女の学生が話しています。女の学生は国にいる時、何を勉強していましたか。）\n男：マリアさんは大学で何を研究していますか。\n女：私は日本の文化について勉強しています。ジョンさんは？\n男：私は医学を勉強しています。\n女：すごいですね。いつから医者になりたいと思いましたか。\n男：高校生の時です。子供の時は小説家になりたかったんですが。\n女：ええ。私は自分で会社を持ちたいと思っていました。だから、大学で経済を勉強していましたが、日本へ来てから日本の文化に興味を持ちました。\n男：私も興味があります。今度教えてくださいね。',
  'Nam: Maria nghiên cứu gì ở đại học? – Nữ: Tôi học về văn hóa Nhật. Còn John? – Tôi học y. – Giỏi quá. Từ khi nào muốn làm bác sĩ? – Từ cấp 3. Hồi nhỏ thì muốn làm nhà văn. – Tôi thì từng muốn có công ty riêng, nên ở đại học (bên nước) đã học kinh tế. Sang Nhật rồi mới quan tâm đến văn hóa Nhật.',
  'Mấu chốt thời điểm: BÂY GIỜ học 日本の文化, nhưng 「国にいる時」 (trước khi sang Nhật) học 経済 (「大学で経済を勉強していましたが、日本へ来てから…」) → 2. 医学 là của John. 経済 (KINH TẾ); 文化 (VĂN HÓA); 小説 (TIỂU THUYẾT).')
Q(2, 7, '男の学生は昨日何をしていましたか。', 'Hôm qua nam sinh đã làm gì?',
  ['パソコンを直していた', 'レポートを書いていた', 'ベッドで寝ていた', '図書館で勉強していた'], 3,
  '（男の学生と女の学生が話しています。男の学生は昨日何をしていましたか。）\n女：昨日の雷、すごかったですね。\n男：ええ。大丈夫でしたか。\n女：ええ。パソコンでレポートを書いていましたが、心配になったのでやめました。パソコンがおかしくなることがあるそうですね。ジョンさんも雷の時、レポートを書いていましたか。\n男：ええ、あ、いいえ。私はすごく疲れていたので、ベッドで寝ていました。だから、まだ終わっていません。\n女：そうですか。授業が終わった後、図書館へ行きますが、一緒にどうですか。\n男：いいですね。そうしましょう。',
  'Nữ: Sấm sét hôm qua dữ nhỉ. – Nam: Ừ, có sao không? – Tôi đang viết báo cáo trên máy tính nhưng lo nên thôi. Nghe nói máy tính có thể bị hỏng. John lúc sấm sét cũng viết báo cáo à? – Không. Tôi mệt quá nên nằm ngủ trên giường. Vì vậy vẫn chưa xong. – Học xong tôi đi thư viện, đi cùng không? – Hay đấy, đi thôi.',
  'Viết báo cáo là việc của bạn nữ; nam: 「すごく疲れていたので、ベッドで寝ていました」 → 3. Thư viện là kế hoạch sau giờ học (chưa làm). 雷 (LÔI) = sấm sét; 疲れる (BÌ) = mệt.')

# ===== もんだい3 – 発話表現 (tranh + 3 câu nói) =====
GT3 = 'Nhìn tranh, nghe tình huống, chọn câu mà người có mũi tên (→) nên nói.'
Q(3, 1, '教科書を忘れました。隣の人と一緒に見たいです。何と言いますか。', GT3, P3, 3,
  '教科書を忘れました。隣の人と一緒に見たいです。何と言いますか。\n1　さあ、一緒に教科書を見ませんか。\n2　ちょっと、その教科書を見たいんですが。\n3　あの、教科書を見せてくれませんか。',
  'Quên sách giáo khoa, muốn xem chung với người bên cạnh. Nói gì? 1. Nào, cùng xem sách không? 2. Tôi muốn xem cuốn sách đó một chút. 3. À, cho tôi xem sách cùng được không?',
  'Nhờ người khác cho mình xem → 「見せてくれませんか」 (見せる = cho xem). 1 là rủ rê (người có sách mới nói); 2 「見たいんですが」 nghe như muốn giành lấy sách. 教科書 (GIÁO KHOA THƯ); 隣 (LÂN) = bên cạnh.', scene=True)
Q(3, 2, '話が速くてよくわかりませんでした。何と言いますか。', GT3, P3, 3,
  '話が速くてよくわかりませんでした。何と言いますか。\n1　速すぎて困るんですが。\n2　もう一回お願いします。\n3　ちょっと遅く話してくれませんか。',
  'Người kia nói nhanh quá, không hiểu. Nói gì? 1. Nhanh quá nên tôi khó xử. 2. Làm ơn một lần nữa. 3. Nói chậm lại một chút giúp tôi được không?',
  'Vấn đề là 「速くて」 (nói nhanh) → nhờ nói chậm lại: 「遅く話してくれませんか」 → 3 (trong thực tế người Nhật hay nói 「ゆっくり話してくれませんか」). 1 nghe như phàn nàn; 2 nhờ nói lại nhưng nói lại vẫn nhanh thì vẫn không hiểu. Vてくれませんか = nhờ lịch sự. 速い (TỐC) = nhanh.', scene=True)
Q(3, 3, '駅で気分が悪くなりました。近くにいる人に何と言いますか。', GT3, P3, 1,
  '駅で気分が悪くなりました。近くにいる人に何と言いますか。\n1　すみません、駅員を呼んでもらえませんか。\n2　すみません、駅員の手伝いをお願いします。\n3　すみません、駅員に助けてもらってください。',
  'Ở ga thấy khó chịu trong người. Nói gì với người bên cạnh? 1. Xin lỗi, gọi giúp tôi nhân viên nhà ga được không? 2. Xin lỗi, nhờ việc giúp đỡ của nhân viên. 3. Xin lỗi, hãy nhờ nhân viên ga giúp (bạn).',
  'Nhờ người khác làm cho mình → Vてもらえませんか: 「駅員を呼んでもらえませんか」 → 1. Câu 3 「助けてもらってください」 là bảo NGƯỜI KIA đi nhờ nhân viên giúp họ – sai chủ thể. 気分が悪い = khó chịu trong người; 駅員 (DỊCH VIÊN) = nhân viên ga.', scene=True)
Q(3, 4, '友達にパーティーの準備を手伝ってもらいます。何と言いますか。', GT3, P3, 3,
  '今、友達にパーティーの準備を手伝ってもらいます。何と言いますか。\n1　ケーキを買ってしまってください。\n2　ケーキを買ってあげてください。\n3　ケーキを買っておいてください。',
  'Nhờ bạn giúp chuẩn bị tiệc. Nói gì? 1. Hãy mua hết bánh đi. 2. Hãy mua bánh cho (ai đó). 3. Hãy mua sẵn bánh giúp tôi.',
  'Chuẩn bị trước cho bữa tiệc → Vておく (làm sẵn): 「買っておいてください」 → 3. Vてしまう = làm xong hẳn / lỡ làm; Vてあげる = làm cho người khác. 準備 (CHUẨN BỊ).', scene=True)
Q(3, 5, 'みんなで昼ご飯を食べていますが、一人の友達が何も食べません。何と言いますか。', GT3, P3, 2,
  '今、みんなで昼ご飯を食べていますが、一人の友達が何も食べません。何と言いますか。\n1　もう少し食べなさい。\n2　少し食べた方がいいですよ。\n3　食べれば食べるほどおいしいです。',
  'Mọi người đang ăn trưa nhưng một người bạn không ăn gì. Nói gì? 1. Ăn thêm chút nữa đi (mệnh lệnh). 2. Nên ăn một chút đấy. 3. Càng ăn càng ngon.',
  'Khuyên bạn bè → Vた方がいいですよ → 2. 〜なさい là mệnh lệnh của người trên (cha mẹ, thầy cô) với người dưới, không dùng với bạn. 3 không phải lời khuyên. 昼ご飯 (TRÚ PHẠN) = bữa trưa.', scene=True)

# ===== もんだい4 – 即時応答 =====
GT4 = 'Nghe câu nói, chọn câu đáp phù hợp nhất (không có tranh).'
Q(4, 1, '', GT4, P3, 1,
  '男：今晩、うちにいらっしゃいませんか。\n1　ええ、ぜひ。\n2　ええ、いますよ。\n3　ええ、いらっしゃいません。',
  'Tối nay anh/chị đến nhà tôi chơi không? 1. Vâng, nhất định. 2. Vâng, tôi có ở nhà. 3. Vâng, không đến ạ.',
  'いらっしゃいませんか = mời (kính ngữ của 来ませんか). Nhận lời: 「ええ、ぜひ」 → 1. 2 nhầm いらっしゃる = いる (có ở). 3 dùng kính ngữ cho chính mình là sai.')
Q(4, 2, '', GT4, P3, 3,
  '女：牛乳、買っておいてくれる？\n1　うん、置いたよ。\n2　うん、買ったよ。\n3　うん、いいよ。',
  'Mua sẵn sữa giúp em được không? 1. Ừ, để rồi. 2. Ừ, mua rồi. 3. Ừ, được.',
  'Lời nhờ (〜てくれる？) → nhận lời: 「うん、いいよ」 → 3. 2 「買ったよ」 là đã mua rồi, không khớp vì việc nhờ là cho tương lai. 1 nhầm おいて (置く = đặt) với Vておく. 牛乳 (NGƯU NHŨ) = sữa bò.')
Q(4, 3, '', GT4, P3, 1,
  '男：エアコンをつけてもよろしいでしょうか。\n1　ええ、どうぞ。\n2　はい、わかりました。\n3　いいえ、結構です。',
  'Tôi bật điều hòa có được không ạ? 1. Vâng, xin cứ tự nhiên. 2. Vâng, tôi hiểu rồi. 3. Không, không cần đâu.',
  'Xin phép (〜てもよろしいでしょうか) → cho phép: 「ええ、どうぞ」 → 1. わかりました dùng khi nhận chỉ thị; 結構です dùng để từ chối lời mời/đề nghị.')
Q(4, 4, '', GT4, P3, 3,
  '先生：どうして宿題をしてこなかったんですか。\n1　はい、そうすればよかったです。\n2　すみません、よくわかりません。\n3　すみません、時間がなくて。',
  'Thầy: Sao em không làm bài tập về nhà? 1. Vâng, giá mà làm thế thì tốt. 2. Xin lỗi, em không hiểu lắm. 3. Em xin lỗi, em không có thời gian.',
  'Câu hỏi どうして → trả lời lý do: 「時間がなくて」 → 3. Vてくる = làm (rồi mang đến). 宿題 (TÚC ĐỀ) = bài tập về nhà.')
Q(4, 5, '', GT4, P3, 1,
  '客：すみません、注文をお願いします。\n1　はい、少々お待ちください。\n2　いいえ、どういたしまして。\n3　はい、こちらへどうぞ。',
  'Khách: Xin lỗi, cho tôi gọi món. 1. Vâng, xin đợi một chút. 2. Không có gì. 3. Vâng, mời đi lối này.',
  'Nhân viên đáp khách gọi món: 「少々お待ちください」 → 1. どういたしまして đáp lời cảm ơn; こちらへどうぞ khi dẫn chỗ. 注文 (CHÚ VĂN) = gọi món, đặt hàng.')
Q(4, 6, '', GT4, P3, 1,
  '女：新しいのを買ったらどう？\n1　でも、まだ使えるよ。\n2　うん、買ったらいいね。\n3　いや、新しくないよ。',
  'Mua cái mới thì sao? 1. Nhưng vẫn còn dùng được mà. 2. Ừ, mua thì tốt nhỉ. 3. Không, không mới đâu.',
  'Vたらどう？ = khuyên. Đáp hợp lý: phản đối nhẹ nhàng 「でも、まだ使えるよ」 → 1. 2 lặp lại như người khuyên nói; 3 hiểu sai câu hỏi.')
Q(4, 7, '', GT4, P3, 2,
  '男：富士山に登ったことがありますか。\n1　いいえ、登りません。\n2　ええ、ありますよ。\n3　はい、まだありません。',
  'Bạn đã từng leo núi Phú Sĩ chưa? 1. Không, tôi không leo. 2. Có, tôi từng leo rồi. 3. Vâng, vẫn chưa.',
  'Vたことがありますか → trả lời bằng あります／ありません: 「ええ、ありますよ」 → 2. 1 sai dạng (登りません); 3 mâu thuẫn はい với まだありません. 登る (ĐĂNG) = leo.')
Q(4, 8, '', GT4, P3, 2,
  '女：すみません、あの着物を着ているのはどなたですか。\n1　きれいな着物ですね。\n2　田中さんの奥さんですよ。\n3　左から二番目の方です。',
  'Xin lỗi, người đang mặc kimono kia là ai vậy ạ? 1. Kimono đẹp nhỉ. 2. Là vợ anh Tanaka đấy. 3. Là người thứ hai từ trái sang.',
  'どなた = ai (kính ngữ của だれ) → trả lời người đó là ai: 「田中さんの奥さんですよ」 → 2. 3 trả lời câu "người nào/ở đâu" (どの人). 着物 (TRƯỚC VẬT) = kimono; 奥さん (ÁO) = vợ (người khác).')

new = {'id': 'jft-ln4', 'group': 'Luyện nghe JFT', 'title': 'Đề nghe 4', 'name': 'Nghe 4',
       'sub': 'JLPT N4 · cấp độ tầm trung · 28 câu', 'time': 40, 'tag': 'JLPT tầm trung', 'doc': {'f': 'tailieu/DeNghe4_Script_GiaiThich.pdf', 't': 'Script & giải thích (PDF)'}, 'qs': qs}
P = REPO + 'src/raw/jft_exams.json'
d = json.load(open(P, encoding='utf-8'))
d = [e for e in d if e['id'] != 'jft-ln4']
i = next(k for k, e in enumerate(d) if e['id'] == 'jft-ln3')
d.insert(i + 1, new)
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Đề nghe 4:', len(qs), 'câu')
