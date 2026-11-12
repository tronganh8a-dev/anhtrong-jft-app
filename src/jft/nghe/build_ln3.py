"""Đề nghe 3 (12/11/2026): tuyển tập 20 câu nghe hiểu (nguồn audio: いろどり / まるごと, cắt từ video "Luyện nghe số 3" anh gửi).
Ảnh phương án cắt từng ô (không lấy khung/logo video), câu hỏi – dịch – giải thích do Anh Trọng Dạy JFT soạn lại.
Cần /tmp/ln3/out/img và /tmp/ln3/out/au (cắt từ video, xem CLAUDE.md). Chạy: python3 src/jft/nghe/build_ln1.py rồi python3 src/build_data.py"""
import json, html, shutil, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from furi import furi
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')) + '/'
IMG = 'app/media/jft/img/'; AU = 'app/media/jft/au/'
SRC = '/tmp/ln3/out/'
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
        for i, d in enumerate(o): d['img'] = IMG + (im or f'ln3_{n:02d}') + 'abc'[i] + '.jpg'
    qs.append(dict(s='聴解', ins='', gset=None, gimg=None, gau=None, t=t, imgs=[], img=None,
                   au=AU + (au or f'ln3_L{n:02d}') + '.mp3', o=o, a=[a - 1], ex=EX(opts[a - 1], script, dich, gt, part)))

#DATA
L(1, 'リンさんは、いつ事務室へ来てくださいと言われましたか。', 'Lin được bảo khi nào hãy đến văn phòng?',
  ['13時半', '14時半', '15時半'], 2,
  'A：もしもし、リンさん。\nB：はい。\nA：あとで、14時半に事務室に来てください。\nB：すみません。何時ですか？\nA：14時半。午後2時半です。\nB：わかりました。',
  'A: Alo, chị Lin. / B: Vâng. / A: Lát nữa hãy đến văn phòng lúc 14 giờ 30. / B: Xin lỗi, mấy giờ ạ? / A: 14 giờ rưỡi. Tức 2 giờ rưỡi chiều. / B: Tôi hiểu rồi.',
  '「14時半」 = 14 giờ 30 = 午後2時半. Giờ 24h ở Nhật hay đi kèm cách nói 午後〜時 – nghe được một trong hai là đủ. 半 (BÁN) = rưỡi.', pics=False)
L(2, '何のお祝いですか。', 'Mừng dịp gì vậy?',
  ['誕生日', '結婚', '子どもが生まれた'], 1,
  'A：今日、私の誕生日なんだ。\nB：へー、お誕生日おめでとうございます。\nC：はいはい、おめでとう、おめでとう。\nA：お祝い、待ってますよ。\nC：お祝いねえ……。\nB：私の国では、誕生日の人がみんなにケーキをごちそうしますよ。\nC：へー、それはいいねえ。\nA：えー！',
  'A: Hôm nay là sinh nhật tôi đấy. / B: Ồ, chúc mừng sinh nhật. / C: Ừ ừ, chúc mừng. / A: Tôi chờ quà đấy nhé. / C: Quà à… / B: Ở nước tôi, người có sinh nhật sẽ mời mọi người ăn bánh. / C: Thế thì hay nhỉ. / A: Hả!',
  '「今日、私の誕生日なんだ」 → tranh A. ごちそうする = đãi, mời ăn. So sánh Đề nghe 1 câu 10 (sinh con) và Đề nghe 2 câu 4 (kết hôn) – cùng câu hỏi 「何のお祝いですか」.')
L(3, '渡した物は何ですか。', 'Vật đã trao là gì?',
  ['魔除けの飾り', '魚のソース', '春巻き'], 1,
  'A：これ、お土産です。\nB：あ、ありがとうございます。\nA：ネパールから持って来た飾りです。\nB：へー。\nA：これは、魔除けです。壁にかけると、悪いものが入って来ません。\nB：そうなんですか。',
  'A: Đây là quà. / B: Cảm ơn bạn. / A: Đồ trang trí tôi mang từ Nepal về. / A: Đây là bùa xua đuổi tà ma. Treo lên tường thì điều xấu không vào nhà được. / B: Vậy à.',
  '「ネパールから持って来た飾り」「魔除けです。壁にかける」 → tranh A (mặt nạ treo tường). 魔除け (MA TRỪ) = bùa trừ tà; 飾り = đồ trang trí; 壁にかける = treo lên tường.')
L(4, '京都はどんなところですか。', 'Kyoto là nơi như thế nào?',
  ['お寺や神社が多い古い町', '人が多い', '遊園地がある'], 1,
  'A：北村さん、京都はどんなところですか？一度行ってみたいんです。\nB：そうだなあ、古い町で、お寺とか神社がたくさん見られるよ。\nA：そうですか。\nB：あと、いろいろな日本のお土産が買えるし、海外からの観光客にもすごく人気があるよね。\nA：そうですよね。',
  'A: Anh Kitamura, Kyoto là nơi thế nào? Tôi muốn đi thử một lần. / B: Là thành phố cổ, có thể tham quan rất nhiều chùa và đền. Ngoài ra mua được nhiều quà Nhật, rất được khách nước ngoài yêu thích.',
  '「古い町で、お寺とか神社がたくさん」 → tranh A (phố cổ, có tháp chùa). Tranh B (đông người) là câu trả lời cho Tokyo ở Đề nghe 1 câu 13.')
L(5, 'さいたま新都心に行くには、どのホームへ行けばいいですか。', 'Để đi đến Saitama-Shintoshin, nên đến sân ga số mấy?',
  ['3・4番線（上野東京ライン）', '5・6番線（湘南新宿ライン）', '7・8番線（埼京線）'], 3,
  '乗客：すみません、さいたま新都心に行きたいんですけど、京浜東北線、動かないんですか？\n駅員：ええ、申し訳ありません。さいたま新都心なら、埼京線の北与野駅から歩けますよ。\n乗客：すみません、何線ですか？\n駅員：埼京線です。8番線から乗ってください。\n乗客：8番線ですね？\n駅員：はい。埼京線で北与野駅まで行ってください。',
  'Khách: Tôi muốn đến Saitama-Shintoshin, tuyến Keihin-Tohoku không chạy à? / Nhân viên: Vâng, xin lỗi. Đến Saitama-Shintoshin thì đi bộ từ ga Kita-Yono của tuyến Saikyo được. / Khách: Tuyến nào ạ? / Nhân viên: Tuyến Saikyo. Hãy lên tàu ở sân ga 8. / Khách: Sân ga 8 nhỉ? / Nhân viên: Vâng, đi tuyến Saikyo đến ga Kita-Yono.',
  '「埼京線です。8番線から乗ってください」 → biển 7・8 埼京線 (C). Cùng thông báo với Đề nghe 2 câu 9 (lý do tàu dừng: 人身事故). Câu hỏi 〜ばいいですか = nên làm thế nào.', part=True)
L(6, 'エドさんは、これから何を食べたいですか。', 'Từ bây giờ Ed muốn ăn gì?',
  ['ゆば', 'そば', 'すし'], 1,
  '坂本：おいしいものは、何か食べましたか？\nエド：はい、そばを食べました。ゆばも食べてみたいです。\n坂本：ああ、日光の名物ですからね。',
  'Sakamoto: Đã ăn món gì ngon chưa? / Ed: Rồi, tôi ăn soba. Tôi cũng muốn ăn thử yuba. / Sakamoto: À, đó là đặc sản Nikko mà.',
  'Câu thứ ba về cùng hội thoại Ed ở Nikko (Đề nghe 1 câu 18–19, Đề nghe 2 câu 10–11). そば là món đã ăn (食べました), muốn ăn là 「ゆばも食べてみたいです」 → tranh A. ゆば = váng đậu, đặc sản Nikko. Vてみたい = muốn thử làm V.', part=True)
L(7, 'Bさんは週末、何をしましたか。', 'B đã làm gì vào cuối tuần?',
  ['ケーブルカーに乗った', '花を見た', '浄土ヶ浜で船に乗った'], 3,
  'A：週末は何をしたの？\nB：友だちと浄土ヶ浜に行って来ました。\nA：浄土ヶ浜か、いいね。どうだった？\nB：海も空もすごくきれいでした。海で泳げたし、船に乗れたし、楽しかったです。\nA：よかったね。\nB：船では、鳥にパンをあげられるんですよ。\nA：ああ、ウミネコね。楽しかった？\nB：ウミネコが近くに来たとき、ちょっとこわかったです。でも、おもしろかったです。',
  'A: Cuối tuần bạn làm gì? / B: Tôi đi Jodogahama với bạn. / A: Thế nào? / B: Biển và trời đều rất đẹp. Bơi được, đi thuyền được, vui lắm. Trên thuyền còn cho chim ăn bánh mì được. / A: À, mòng biển nhỉ. / B: Lúc mòng biển bay đến gần hơi sợ, nhưng thú vị.',
  '浄土ヶ浜 là bãi biển → 「海で泳げたし、船に乗れたし」 → tranh C (thuyền trên biển). 〜し、〜し = liệt kê lý do. 乗れた / 泳げた = thể khả năng quá khứ.', part=True)
L(8, '何について話していますか。', 'Họ đang nói về chuyện gì?',
  ['フリーマーケット', 'お祭りの寄付', '花火大会'], 2,
  'A：あのう、すみません。この封筒と手紙、何ですか？\nB：ああ、お祭りの寄付のお願いですね。\nA：寄付？何ですか、それ？\nB：もうすぐ夏祭りがあるんですよ。そのお祭りのために、1人500円、払うんです。\nA：お金……。あのう、どうやって払いますか？\nB：えっと、この封筒に500円入れて、ここに名前と住所を書いて、お祭りのときに持って行くんです。\nA：へー、そうなんですか。みんな、払いますか？\nB：寄付ですから、払いたい人だけでいいですよ。',
  'A: Phong bì và lá thư này là gì vậy? / B: À, là lời kêu gọi quyên góp cho lễ hội. / A: Quyên góp? / B: Sắp có lễ hội mùa hè. Cho lễ hội đó mỗi người đóng 500 yên. / A: Đóng thế nào? / B: Cho 500 yên vào phong bì, viết tên và địa chỉ, mang theo khi đi lễ hội. / A: Mọi người đều đóng à? / B: Là quyên góp nên ai muốn đóng thì đóng thôi.',
  '「お祭りの寄付のお願い」 → tranh B (phong bì + đồng 500 yên). 寄付 (KÝ PHÓ) = quyên góp, tự nguyện: 「払いたい人だけでいい」. Tranh C (pháo hoa) chỉ gợi "lễ hội" chứ không phải nội dung chính.')
L(9, '成人の日には、何をしますか。', 'Vào Ngày Thành nhân, người ta làm gì?',
  ['市長の話を聞いたり、友だちに会ったりする', '家族とごちそうを食べる', '学校で卒業式をする'], 1,
  'A：昨日、駅前に、着物を着ている人がたくさんいたんですけど、何かお祭りですか？\nB：ああ、昨日は成人の日だったから。\nA：成人の日？\nB：20歳になった人を、お祝いするんだよ。\nA：へー、何をするんですか？\nB：市のホールで成人式があって、市長さんの話を聞いたり……。\nA：それだけなんですか？\nB：うん。でも、まあ、みんなおしゃれをして、特に女性は、着物を着て写真を撮ったり、あと小学校や中学校や高校の友だちと久しぶりに会ったりして、盛り上がるんだよ。',
  'A: Hôm qua trước ga có nhiều người mặc kimono, có lễ hội gì à? / B: À, hôm qua là Ngày Thành nhân. Ngày chúc mừng người tròn 20 tuổi. / A: Họ làm gì? / B: Có lễ trưởng thành ở hội trường thành phố, nghe thị trưởng phát biểu… / A: Chỉ vậy thôi à? / B: Ừ. Nhưng mọi người ăn diện, đặc biệt phụ nữ mặc kimono chụp ảnh, gặp lại bạn cũ tiểu học, cấp 2, cấp 3 sau thời gian dài, nên rất vui.',
  '「市長さんの話を聞いたり…友だちと久しぶりに会ったり」 → tranh A (bục phát biểu + gặp bạn). 〜たり〜たりする = làm nào là ~ nào là ~. 成人 (THÀNH NHÂN) = người trưởng thành (20 tuổi).', part=True)
L(10, 'ジムをはじめて利用するとき、何を受けますか。', 'Khi lần đầu sử dụng phòng tập, sẽ được nhận gì?',
  ['30分のオリエンテーション', '3時間のトレーニング', 'シューズのレンタル'], 1,
  'B：料金は1日560円で3時間までです。3時間以上のご利用は、延長料金が30分につき150円かかります。\nB：それでは、そこの階段を下りたところに更衣室がありますので、そこで着替えてください。それから、ジムでは、室内用のシューズをはいてください。お持ちですか？\nA：はい、あります。\nB：それから、はじめて利用するときは、マシンの使い方など、トレーナーから30分ほどのオリエンテーションを受けていただきます。',
  'B: Phí là 560 yên/ngày, tối đa 3 tiếng. Quá 3 tiếng thì phụ thu 150 yên mỗi 30 phút. Phòng thay đồ ở chỗ xuống cầu thang kia. Trong phòng tập hãy đi giày trong nhà – bạn có mang không? / A: Có. / B: Ngoài ra, lần đầu sử dụng sẽ được huấn luyện viên hướng dẫn khoảng 30 phút về cách dùng máy…',
  '「はじめて利用するときは…30分ほどのオリエンテーションを受けていただきます」 → tranh A. Bẫy: 3時間 là giờ dùng tối đa với phí 560 yên (tranh B); giày thì A đã có (tranh C).', part=True)
L(11, '茶碗蒸しは、どんな料理ですか。', 'Chawanmushi là món ăn như thế nào?',
  ['鶏肉の料理', '鶏肉やエビ、きのこが入った卵の料理', '甘いプリン'], 2,
  'ラン：これは何ですか？\n森：茶碗蒸し。卵の料理です。プリンに似てますけど、甘くなくて、おいしいですよ。だしを使います。\nラン：だし？\n森：えーと、まあ、日本のスープかな。\nラン：へー。中に何が入ってますか？\n森：鶏肉とか、エビとか、きのことかが入ってます。ときどき、銀杏も入れますよ。',
  'Lan: Đây là món gì? / Mori: Chawanmushi, món làm từ trứng. Giống pudding nhưng không ngọt, ngon lắm. Dùng nước dashi. / Lan: Dashi? / Mori: Kiểu súp của Nhật. / Lan: Bên trong có gì? / Mori: Có thịt gà, tôm, nấm… Thỉnh thoảng cho cả hạt ngân hạnh.',
  '「卵の料理」「鶏肉とか、エビとか、きのことか」 → tranh B (chén trứng hấp có tôm, nấm). Bẫy: 「プリンに似てますけど、甘くなくて」 – giống pudding nhưng KHÔNG ngọt, nên không phải tranh C.', part=True)
L(12, 'この薬は、1日に何回飲みますか。', 'Một ngày uống thuốc này mấy lần?',
  ['一回', '二回', '三回'], 3,
  '薬剤師：こちらは咳を抑える薬です。1日3回、食後に飲んでください。\n患者：食後？\n薬剤師：ご飯を食べた後です。\n患者：はい、わかりました。\n薬剤師：飲むと眠くなります。飲んだ後、運転しないでくださいね。\n患者：わかりました。',
  'Dược sĩ: Đây là thuốc giảm ho. Ngày uống 3 lần, sau khi ăn. / Bệnh nhân: Shokugo? / Dược sĩ: Là sau khi ăn cơm. / Bệnh nhân: Vâng. / Dược sĩ: Uống vào sẽ buồn ngủ. Uống xong đừng lái xe nhé. / Bệnh nhân: Vâng.',
  '「1日3回、食後に」 → 3 lần/ngày, sau bữa ăn. 食後 (THỰC HẬU) = sau ăn, trái nghĩa 食前 (しょくぜん) = trước ăn. 咳を抑える = làm dịu cơn ho.', pics=False)
L(13, '薬を飲んだ後、何をしてはいけませんか。', 'Sau khi uống thuốc, không được làm gì?',
  ['ご飯を食べる', '寝る', '車を運転する'], 3,
  '薬剤師：飲むと眠くなります。飲んだ後、運転しないでくださいね。\n患者：わかりました。',
  'Dược sĩ: Uống vào sẽ buồn ngủ. Uống xong đừng lái xe nhé. / Bệnh nhân: Vâng.',
  'Cùng bài với câu 12. 「飲んだ後、運転しないでください」 → không được lái xe (tranh C). Buồn ngủ (眠くなる) là tác dụng phụ chứ không bị cấm; ăn cơm thì phải ăn trước khi uống (食後).', part=True, au='ln3_L12')
L(14, '食べられないのはどれですか。', 'Món nào người này không ăn được?',
  ['エビ', 'タコ', 'わさび'], 1,
  'A：あれ、エビ、食べないんですか？\nB：あ、はい。アレルギーがあるので、食べられないんです。\nA：よかったら、どうぞ。\nB：そうですか。\nA：他の料理は大丈夫ですか？\nB：え、おいしいです。',
  'A: Ơ, bạn không ăn tôm à? / B: Vâng, vì tôi bị dị ứng nên không ăn được. / A: Nếu không ngại thì (món khác) mời bạn. / A: Những món khác thì được chứ? / B: Vâng, ngon lắm.',
  '「エビ…アレルギーがあるので、食べられないんです」 → tranh A. アレルギー = dị ứng. 〜ので = vì ~ (giải thích lý do lịch sự).')
L(15, 'どうやって山に登りましたか。', 'Người này lên núi bằng cách nào?',
  ['バス', '歩いて', 'ケーブルカー'], 2,
  'A：週末に高尾山に行ったんです。\nB：へえ。どうでしたか。\nA：ケーブルカーがすごく混んでいて大変でした。\nB：ああ、この時期は混みますよね。\nA：ええ。だからケーブルカーは諦めて歩いて登りました。\nB：大変でしたね。\nA：疲れたけど景色が綺麗で気持ちよかったです。',
  'A: Cuối tuần tôi đi núi Takao. / B: Thế nào? / A: Cáp treo rất đông, vất vả lắm. / B: Mùa này hay đông nhỉ. / A: Vâng. Vì vậy tôi bỏ ý định đi cáp treo và đi bộ lên núi. / B: Vất vả nhỉ. / A: Mệt nhưng phong cảnh đẹp, dễ chịu.',
  'Bẫy: có nhắc ケーブルカー nhưng 「ケーブルカーは諦めて歩いて登りました」 → đi bộ (tranh B). 諦める (ĐẾ) = từ bỏ. Nghe kỹ động từ sau 「だから」.', part=True)
L(16, '何についてのお知らせですか。', 'Đây là thông báo về việc gì?',
  ['地震', '大雪', '津波'], 1,
  '緊急地震速報です。強い揺れに警戒してください。緊急地震速報が出ました。京都、大阪、滋賀、兵庫、福井、三重、奈良、和歌山、香川に緊急地震速報が出ました。けがをしないように、身を守ってください。倒れやすい家具などからは離れてください。テーブルや机の下に隠れてください。\n……えー、先ほど午前11時41分ごろ、近畿地方で強い揺れを感じました。震源が海底ですと、津波のおそれがあります。海岸から離れてください。',
  'Cảnh báo động đất khẩn cấp. Hãy đề phòng rung lắc mạnh. Đã có cảnh báo động đất khẩn cấp cho Kyoto, Osaka, Shiga, Hyogo, Fukui, Mie, Nara, Wakayama, Kagawa. Hãy bảo vệ bản thân để không bị thương. Tránh xa đồ đạc dễ đổ. Hãy nấp dưới bàn. … Khoảng 11 giờ 41 sáng vừa rồi, vùng Kinki có rung lắc mạnh. Nếu tâm chấn ở đáy biển thì có nguy cơ sóng thần. Hãy tránh xa bờ biển.',
  '「緊急地震速報」 = cảnh báo động đất khẩn → tranh A. Bẫy: cuối bài có 「津波のおそれ」 (có nguy cơ sóng thần) – đó chỉ là khả năng, chủ đề chính vẫn là động đất. 速報 (TỐC BÁO) = tin nhanh.')
L(17, 'アナウンスを聞いて、何をしますか。', 'Sau khi nghe thông báo, sẽ làm gì?',
  ['本棚を押さえる', '机の下に隠れる', '海へ行く'], 2,
  '倒れやすい家具などからは離れてください。テーブルや机の下に隠れてください。……震源が海底ですと、津波のおそれがあります。海岸から離れてください。',
  'Tránh xa đồ đạc dễ đổ. Hãy nấp dưới bàn. … Nếu tâm chấn ở đáy biển thì có nguy cơ sóng thần. Hãy tránh xa bờ biển.',
  'Cùng bài với câu 16. 「テーブルや机の下に隠れてください」 → tranh B. Tranh A (giữ tủ sách) ngược với 「家具からは離れて」 (tránh xa đồ đạc); tranh C ngược với 「海岸から離れて」 (tránh xa bờ biển).', part=True, au='ln3_L16')
L(18, 'アニサさんは、どうして遅れますか。', 'Tại sao Anisa đến muộn?',
  ['寝坊したから', '財布を家に忘れたから', '電車が遅れたから'], 2,
  'A：はい、北村ホールです。\nB：もしもし、あの、アニサです。\nA：ああ、アニサさん。\nB：すみません。家に財布を忘れました。これから取りに帰ります。それで少し遅れます。\nA：あ、わかりました。\n――\nB：おはようございます。遅くなって申し訳ありません。',
  'A: Vâng, sảnh Kitamura đây. / B: Alo, tôi là Anisa. / B: Xin lỗi, tôi để quên ví ở nhà. Bây giờ tôi về nhà lấy. Vì vậy sẽ đến muộn một chút. / A: À, tôi hiểu rồi. / … B: Chào buổi sáng. Xin lỗi vì đến muộn.',
  '「家に財布を忘れました。これから取りに帰ります」 → tranh B (nghĩ đến chiếc ví). Nを忘れる = để quên. 取りに帰る = về lấy (Vます bỏ ます + に + đi/về: mục đích).')
L(19, 'テーブルを捨てるとき、どうしますか。', 'Khi muốn vứt chiếc bàn thì phải làm gì?',
  ['粗大ごみ受付センターに電話して予約する', '燃えるごみの日に出す', '小さく壊して袋に入れる'], 1,
  'ドルジ：あと、今度、古いテーブルを捨てたいんですけど、どうやって捨てればいいですか？\n大家：テーブルは粗大ごみだから、ほかのごみとは出し方が違うんですよ。\nドルジ：そうなんですか。\n大家：ええ。まず、粗大ごみ受付センターというところに電話をして、予約をするんですよ。',
  'Dorji: Ngoài ra, lần tới tôi muốn vứt một chiếc bàn cũ, thì phải vứt thế nào ạ? / Chủ nhà: Bàn là rác cồng kềnh nên cách vứt khác với các loại rác khác. / Dorji: Vậy à. / Chủ nhà: Vâng. Trước tiên gọi điện đến nơi gọi là Trung tâm tiếp nhận rác cồng kềnh và đặt lịch.',
  '「まず、粗大ごみ受付センター…に電話をして、予約をする」 → tranh A. 粗大ごみ (THÔ ĐẠI) = rác cồng kềnh (bàn ghế, tủ…). Đoạn đầu bài nói về thùng carton, chai nhựa – không liên quan câu hỏi.', part=True)
L(20, 'どうして会社では、エアコンの温度を28度に設定するようにしていますか。', 'Tại sao công ty quy định cài điều hòa ở 28 độ?',
  ['リモコンがないから', '節電のため', 'エアコンが苦手な人がいるから'], 2,
  'A：今日、暑いですね。エアコンつけてますか？\nB：ついてますよ。でも、うちの会社、エアコンの温度は、28度に設定するようにしてますから。\nA：え、どうしてですか？\nB：節電のためですよ。設定温度を下げると、電気をたくさん使いますからね。\nA：そうなんですか。でも、暑いんですが、下げちゃだめですか？\nB：まあ、少しなら下げてもいいですよ。でも、エアコンが苦手な人もいるから、ほかの人にも聞いてみてください。',
  'A: Hôm nay nóng nhỉ. Có bật điều hòa không? / B: Có. Nhưng công ty tôi quy định cài điều hòa ở 28 độ. / A: Ơ, tại sao? / B: Để tiết kiệm điện. Hạ nhiệt độ thì tốn nhiều điện. / A: Nhưng nóng quá, không hạ được à? / B: Hạ một chút thì được. Nhưng có người không chịu được điều hòa, nên hãy hỏi cả người khác.',
  '「節電のためですよ」 → tranh B. 節電 (TIẾT ĐIỆN) = tiết kiệm điện. 〜ため = để/vì ~. Bẫy: 「エアコンが苦手な人もいる」 là lý do phải hỏi người khác trước khi hạ nhiệt, không phải lý do đặt 28 độ.')

new = {'id': 'jft-ln3', 'group': 'Luyện nghe JFT', 'title': 'Đề nghe 3', 'name': 'Nghe 3',
       'sub': 'Tuyển tập 20 câu nghe hiểu · いろどり', 'time': 30, 'tag': 'Luyện nghe', 'qs': qs}
P = REPO + 'src/raw/jft_exams.json'
d = json.load(open(P, encoding='utf-8'))
d = [e for e in d if e['id'] != 'jft-ln3']
i = next(k for k, e in enumerate(d) if e['id'] == 'jft-ln2')
d.insert(i + 1, new)
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Đề nghe 3:', len(qs), 'câu')
