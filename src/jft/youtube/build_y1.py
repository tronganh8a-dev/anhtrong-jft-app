import json, html, shutil, os, sys
sys.path.insert(0, '/home/claude/anhtrong-jft-app/src/jft')
from furi import furi
REPO = '/home/claude/anhtrong-jft-app/'
IMG = 'app/media/jft/img/'; AU = 'app/media/jft/au/'
for f in os.listdir('/tmp/yt/img'): shutil.copy('/tmp/yt/img/' + f, REPO + 'public/' + IMG + f)
for f in os.listdir('/tmp/yt/au'): shutil.copy('/tmp/yt/au/' + f, REPO + 'public/' + AU + f)

J = lambda t, fu=True: (furi(html.escape(t)) if fu else html.escape(t)).replace('\n', '<br>')
def EX(ans, dich, gt, script=None, fu=True):
    s = f'<div class="ans">Đáp án đúng: <span class="jp">{J(ans, fu)}</span></div>'
    if script: s += f'<span class="lb">SCRIPT</span><div class="jp">{J(script)}</div>'
    s += f'<span class="lb">DỊCH</span><div>{J(dich)}</div><span class="lb">GIẢI THÍCH</span><div>{J(gt)}</div>'
    return s
def Q(s, t, o, a, ex, imgs=(), au=None, oimg=None, fu_opt=True):
    oo = [{'t': J(x, fu_opt) if x else ''} for x in o]
    if oimg:
        for d, im in zip(oo, oimg): d['img'] = IMG + im
    return dict(s=s, ins='', gset=None, gimg=None, gau=None, t=t, imgs=[IMG + i for i in imgs],
                img=None, au=au, o=oo, a=[a - 1], ex=ex)

V = '文字と語彙'; K = '会話と表現'; L = '聴解'; R = '読解'
PIC = '絵を見て、正しいことばを選んでください。'
qs = []
# ---------- 文字と語彙 ----------
def v(t, o, a, dich, gt, imgs=(), raw=None):
    qs.append(Q(V, raw if raw else J(t), o, a, EX(o[a-1], dich, gt, fu=False), imgs, fu_opt=False))
v(PIC, ['のどが　痛い', 'せきが　出る', '熱が　ある', '鼻水が　出る'], 3,
  'Tranh: người phụ nữ đặt khăn lạnh trên trán, ngậm nhiệt kế → bị sốt.',
  '熱が　ある (NHIỆT) = bị sốt. Phân biệt các triệu chứng cùng nhóm: のどが痛い = đau họng, せきが出る = bị ho, 鼻水が出る (TỊ THUỶ) = chảy nước mũi. Từ vựng いろどり 初級1 第15課.', ['y1_v1.jpg'])
v(PIC, ['じめじめする', '寒い', '暑い', 'すずしい'], 4,
  'Tranh: gió thổi nhẹ, người cười thoải mái → trời mát.',
  'すずしい = mát mẻ. 寒い (HÀN) = lạnh, 暑い (THỬ) = nóng, じめじめする = ẩm ướt, oi. Từ vựng thời tiết – いろどり 初級1 第3課.', ['y1_v2.jpg'])
v(PIC, ['田舎', '不便（な）', '便利（な）', '静か（な）'], 3,
  'Tranh: khu phố có nhà ga, bệnh viện, cửa hàng ngay cạnh nhau → tiện lợi.',
  '便利（な）(TIỆN LỢI) = tiện lợi; trái nghĩa 不便（な）(BẤT TIỆN). 田舎 (ĐIỀN XÁ) = vùng quê, 静か（な）(TĨNH) = yên tĩnh. Nói về nơi mình sống – いろどり 初級1 第5課.', ['y1_v3.jpg'])
v('ちょっと道に（　　）、おくれます。', ['まがって', 'わすれて', 'まよって', 'わたって'], 3,
  'Tôi bị lạc đường một chút nên sẽ đến muộn.',
  'Cụm cố định: 道に　まよう = lạc đường. 道を　まがる = rẽ (dùng trợ từ を), 道を　わたる = băng qua đường; わすれる = quên. Trợ từ に + lý do đến muộn → まよって. いろどり 初級1 第7課.')
v('この町は人が（　　）、すみやすいです。', ['ふべんで', 'やさしくて', 'つめたくて', 'せまくて'], 2,
  'Thị trấn này người dân hiền hoà nên dễ sống.',
  'Chủ ngữ là 人が → cần tính từ chỉ tính cách người: やさしい = hiền, tốt bụng. つめたい = lạnh lùng (nghĩa xấu, không hợp すみやすい). ふべん = bất tiện, せまい = chật – dùng cho nơi chốn, không cho người. いろどり 初級1 第5課.')
v('わたしはエビの（　　）があるので、食べられません。', ['カロリー', 'レシピ', 'メニュー', 'アレルギー'], 4,
  'Tôi bị dị ứng tôm nên không ăn được.',
  '〜の　アレルギーが　ある = bị dị ứng với ~. カロリー = calo, レシピ = công thức nấu ăn, メニュー = thực đơn. Vế sau 食べられません là manh mối. いろどり 初級1 第11課.')
v('', ['がいしゃ', 'かいしや', 'かいじゃ', 'かいしゃ'], 4,
  'Mỗi sáng tôi đi đến công ty lúc 8 giờ.',
  '会社 (HỘI XÃ) đọc là かいしゃ. Các phương án sai: がいしゃ (sai âm đục), かいしや (や to, không phải ゃ nhỏ), かいじゃ (sai âm đục). Chú ý âm ghép nhỏ ゃ・ゅ・ょ.',
  raw='毎朝8時に<u>会社</u>に行きます。')
v('', ['みぎ', 'ひだり', 'ひだい', 'ひたり'], 2,
  'Hãy rẽ trái ở đèn giao thông thứ hai.',
  '左 (TẢ) đọc là ひだり = bên trái. みぎ là 右 (HỮU) = bên phải – hai chữ hay bị nhầm. ひだい, ひたり là cách đọc sai.',
  raw='2つ目のしんごうを<u>左</u>にまがってください。')
v('', ['やさ', 'のさい', 'やさい', 'やざい'], 3,
  'Thịt và rau thì tôi sẽ mua mang đến.',
  '野菜 (DÃ THÁI) đọc là やさい = rau. 野 đọc や, 菜 đọc さい. やさ thiếu い, やざい sai âm đục, のさい lấy âm 野 = の (cánh đồng) là sai.',
  raw='肉と<u>野菜</u>はわたしが買って行きます。')
v('', ['薬', '楽', '葉', '菜'], 1,
  'Tôi đã nhận thuốc ở bệnh viện.',
  'くすり = 薬 (DƯỢC). Các chữ trông giống: 楽 (LẠC – たのしい), 葉 (DIỆP – は, lá), 菜 (THÁI – rau). 薬 có bộ thảo 艹 ở trên và 楽 ở dưới.',
  raw='びょういんで<u>くすり</u>をもらいました。')
v('', ['南', '商', '両', '有'], 1,
  'Trung tâm thể thao Minami rẻ mà tốt đấy.',
  'みなみ = 南 (NAM) = phía nam. 商 (THƯƠNG), 両 (LƯỠNG), 有 (HỮU) là chữ có hình gần giống. Nhớ 4 hướng: 東 ひがし, 西 にし, 南 みなみ, 北 きた.',
  raw='<u>みなみ</u>スポーツセンターは安くていいですよ。')
v('', ['飲み勿', '飲み特', '飲み物', '飯み物'], 3,
  'Đồ uống cho buổi BBQ thì anh Marco mua.',
  'のみもの = 飲み物 (ẨM VẬT). 飯 (PHẠN – ごはん) khác 飲 ở bên phải; 特 (ĐẶC) và 勿 trông giống 物 nhưng sai. Tương tự: 食べ物 = đồ ăn.',
  raw='バーベキューの<u>のみもの</u>はマルコさんが買います。')

# ---------- 会話と表現 ----------
def k(t, o, a, dich, gt):
    qs.append(Q(K, J(t), o, a, EX(o[a-1], dich, gt)))
k('田中：あ、ミンさん！\nミン：（　　）。お元気ですか。\n田中：はい、おかげさまで。',
  ['ああ、お久しぶりです', 'はじめまして', 'いってきます', 'おやすみなさい'], 1,
  'Tanaka: A, anh Minh! / Minh: À, lâu quá không gặp. Anh khoẻ không? / Tanaka: Vâng, nhờ trời tôi khoẻ.',
  'Gặp lại người quen lâu ngày → お久しぶりです, thường đi với お元気ですか và câu đáp おかげさまで. はじめまして chỉ dùng lần đầu gặp. いってきます (khi ra khỏi nhà), おやすみなさい (chúc ngủ ngon). いろどり 初級1 第1課.')
k('木村：どんな音楽が好きですか。\nニン：（　　）。',
  ['毎日聞きました', 'はい、好きです', 'ギターをひきます', 'Jポップが好きです'], 4,
  'Kimura: Bạn thích loại nhạc nào? / Ninh: Tôi thích J-pop.',
  'Câu hỏi どんな〜が好きですか hỏi "loại nào" → phải trả lời bằng tên loại cụ thể: Jポップが好きです. はい、好きです là câu trả lời cho câu hỏi có/không (〜が好きですか). いろどり 初級1 第2課.')
k('山本：昨日はすごい雨（　　）。\nリン：ええ、風もすごかったですね。',
  ['になりますね', 'ですね', 'でしょう', 'でしたね'], 4,
  'Yamamoto: Hôm qua mưa to quá nhỉ. / Rin: Vâng, gió cũng mạnh quá nhỉ.',
  '昨日 → thì quá khứ: danh từ + でした. Thêm ね để tìm sự đồng tình → でしたね, khớp với câu đáp すごかったですね (cũng quá khứ). ですね, でしょう là hiện tại / phỏng đoán. いろどり 初級1 第4課.')
k('ミン：すみません。郵便局は（　　）。\n通行人：この道をまっすぐ行ってください。',
  ['行きましたか', 'どう行ったらいいですか', 'どこがいいですか', 'どうでしたか'], 2,
  'Minh: Xin lỗi, đến bưu điện thì đi thế nào ạ? / Người qua đường: Anh đi thẳng con đường này.',
  'Hỏi đường: 〜は　どう行ったらいいですか = đi đến ~ thế nào thì được. Câu đáp chỉ đường (まっすぐ行ってください) xác nhận. どうでしたか hỏi cảm nghĩ về việc đã qua. いろどり 初級1 第6課.')
k('ミゲル：もしもし、ミゲルです。今、バスの中です。道がこんでいて、少し（　　）。\n会社の人：わかりました。気をつけて来てください。',
  ['はやくなります', 'まにあいます', 'いそぎます', 'おくれます'], 4,
  'Miguel: Alo, tôi là Miguel. Tôi đang trên xe buýt. Đường đông nên tôi sẽ đến muộn một chút. / Người công ty: Tôi biết rồi. Anh đi cẩn thận nhé.',
  'Lý do 道がこんでいて (tắc đường) → kết quả: おくれます (đến muộn). 少し đi với おくれます rất tự nhiên. まにあいます = kịp giờ (ngược nghĩa). いろどり 初級1 第14課.')
k('アリ：すみません。私のメールの日本語を（　　）。\n西村：いいですよ。',
  ['チェックしてもらえませんか', 'チェックしてあげましょうか', 'チェックしましたか', 'チェックしないでください'], 1,
  'Ali: Xin lỗi, anh xem giúp tiếng Nhật trong email của tôi được không? / Nishimura: Được chứ.',
  'Nhờ người khác làm giúp: Vて　もらえませんか. Đáp いいですよ = đồng ý. Vてあげましょうか là đề nghị giúp người khác (người nói làm), không hợp vì đây là email của chính Ali. いろどり 初級1 第9課.')
k('楊：バーベキューの肉と野菜は、私が買って（　　）。\n長谷川：ありがとうございます。',
  ['いましたよ', '来ましたよ', 'ありますよ', '行きますよ'], 4,
  'Dương: Thịt và rau cho buổi BBQ thì tôi sẽ mua mang đến nhé. / Hasegawa: Cảm ơn chị.',
  'Vて行きます = làm V rồi mang đến / rồi đi (việc sẽ làm). Người nói nhận phần việc cho buổi BBQ sắp tới → 買って行きます. 買って来ました là đã mua về rồi. いろどり 初級1 第11課.')
k('田村：梅干し、どう？\nフエン：すみません。すっぱくて、ちょっと（　　）。',
  ['好きです', '得意です', '上手です', '苦手です'], 4,
  'Tamura: Ăn mơ muối không? / Huyền: Xin lỗi, chua quá nên tôi hơi không hợp ạ.',
  'Từ chối món ăn lịch sự: ちょっと苦手です (KHỔ THỦ – không hợp, không giỏi). すみません + すっぱくて (lý do) báo hiệu câu từ chối. 得意・上手 dùng cho kỹ năng, không dùng cho món ăn. いろどり 初級1 第12課.')
k('アリ：お先に失礼します。\n西村：（　　）。',
  ['お疲れさまでした', 'いらっしゃいませ', 'いってらっしゃい', 'おかえりなさい'], 1,
  'Ali: Tôi xin phép về trước. / Nishimura: Anh vất vả rồi.',
  'Ở chỗ làm, khi đồng nghiệp chào お先に失礼します (về trước) → đáp お疲れさまでした. いってらっしゃい dùng khi tiễn người ra ngoài rồi sẽ quay lại, おかえりなさい khi đón người về. いろどり 初級1 第13課.')
k('医者：いつからですか。\n郭：（　　）。',
  ['おとといからです', '3日間です', '毎日です', '明日までです'], 1,
  'Bác sĩ: Từ khi nào? / Quách: Từ hôm kia ạ.',
  'Câu hỏi いつから → trả lời bằng mốc thời gian + から: おとといから (từ hôm kia). 3日間 trả lời cho どのぐらい, 毎日 cho 頻度, 明日まで cho いつまで. いろどり 初級1 第15課.')
k('佐藤：いつも元気ですね。何かしているんですか。\nリン：毎日朝早く起きて、夜は早く（　　）。',
  ['寝たことがあります', '寝るようにしています', '寝ないようにしています', '寝てしまいました'], 2,
  'Sato: Lúc nào chị cũng khoẻ nhỉ. Chị có làm gì không? / Rin: Mỗi ngày tôi dậy sớm, buổi tối thì cố gắng ngủ sớm.',
  'Thói quen cố gắng duy trì: Vる　ようにしています. 早く + 寝る ようにしています hợp nghĩa. 寝ないようにしています là "cố không ngủ" – ngược nghĩa. 〜たことがあります là kinh nghiệm. いろどり 初級1 第16課.')
k('店員：いらっしゃいませ。\nノイ：すみません。このお刺身、明日まで（　　）。\n店員：いえ、今日中に食べてください。',
  ['もちますか', 'もてますか', 'もらいますか', 'もどりますか'], 1,
  'Nhân viên: Xin mời quý khách. / Noi: Xin lỗi, món sashimi này để được đến mai không? / Nhân viên: Không, quý khách hãy ăn trong hôm nay.',
  'もつ (để được, giữ được – nói về đồ ăn): 明日まで　もちますか = để đến mai có được không. もてます là thể khả năng của もつ "cầm" – khác nghĩa. Câu đáp 今日中に食べてください xác nhận. いろどり 初級1 第11課.')

# ---------- 聴解 ----------
def l(n, q, vi, o, a, script, dich, gt, oimg=None):
    t = f'<span class="jp">{J(q)}</span><br><span class="vi-q">{html.escape(vi)}</span>'
    ans = o[a-1] if o[a-1] else f'phương án {a} (tranh)'
    qs.append(Q(L, t, o, a, EX(ans, dich, gt, script), au=AU + f'y1_L{n:02d}.mp3', oimg=oimg))
l(1, 'この人は日本に来て、どのぐらいですか。', 'Người này đến Nhật được bao lâu rồi?',
  ['2年', '1か月', '半年', '1年'], 4,
  'A：日本に来て、どのぐらいになりますか？\nB：1年になります。\nA：そうですか。日本の生活に、もう慣れましたか？\nB：はい。',
  'A: Anh đến Nhật được bao lâu rồi? / B: Được 1 năm rồi. / A: Vậy à. Anh đã quen với cuộc sống ở Nhật chưa? / B: Rồi.',
  'Mẫu 〜て、どのぐらいになりますか – 〜になります dùng để nói khoảng thời gian đã trôi qua. B trả lời rõ 1年になります.')
l(2, 'ジョーイさんの国にはどんな季節がありますか。', 'Ở nước của Joey có những mùa nào?',
  ['一年中夏で、ずっと暑い', '冬がとても長い', '雨季と乾季がある', '四季がある'], 1,
  'A：ジョーイさんの国には、どんな季節がありますか？\nB：一年中夏です。ずっと暑いです。\nA：そうですか。',
  'A: Ở nước anh Joey có những mùa nào? / B: Quanh năm là mùa hè. Lúc nào cũng nóng. / A: Vậy à.',
  '一年中 (NHẤT NIÊN TRUNG) = quanh năm. Từ cần biết: 四季 (TỨ QUÝ) = bốn mùa, 雨季 (VŨ QUÝ) = mùa mưa, 乾季 (CAN QUÝ) = mùa khô.')
l(3, 'この町のよくないところは何ですか。', 'Điểm không tốt của thị trấn này là gì?',
  ['人が冷たい', 'バスが少ない', '緑が少ない', '店が少ない'], 2,
  'A：この町はどうですか？\nB：この町ですか？緑が多くて、静かでいいですね。\nA：そうですね。\nB：でも、バスが少なくて、ちょっと不便です。\nA：あー、そうですよね。',
  'A: Thị trấn này thế nào? / B: Thị trấn này à? Nhiều cây xanh, yên tĩnh, tốt lắm. / A: Đúng nhỉ. / B: Nhưng xe buýt ít nên hơi bất tiện. / A: À, đúng vậy.',
  'Sau でも (nhưng) thường là điểm xấu: バスが少なくて、ちょっと不便です. 緑が多い là điểm tốt, nên 緑が少ない sai.')
l(4, '明日は何時にどこに集まりますか。', 'Ngày mai tập trung lúc mấy giờ, ở đâu?',
  ['6時半に会社の門の前', '8時に駅の改札', '8時に会社の門の前', '10時に会社の受付'], 3,
  'A：すみません。明日は何時にどこですか？\nB：明日は、朝8時に会社の門の前集合ね。\nA：わかりました。8時に門の前ですね。\nB：じゃあ、また明日。',
  'A: Xin lỗi, ngày mai mấy giờ, ở đâu ạ? / B: Ngày mai tập trung ở trước cổng công ty lúc 8 giờ sáng nhé. / A: Tôi hiểu rồi. 8 giờ trước cổng nhỉ. / B: Hẹn mai gặp lại.',
  '集合 (TẬP HỢP) = tập trung. Câu nhắc lại của A (8時に門の前ですね) xác nhận đáp án. 門 (MÔN) = cổng, 改札 (CẢI TRÁT) = cửa soát vé, 受付 = quầy lễ tân.')
l(5, '二人は動物園で何がよかったと言っていますか。', 'Hai người nói ở sở thú con gì hay?',
  ['パンダとゾウ', 'パンダとサル', 'ライオンとパンダ', 'ゾウとサル'], 2,
  'A：動物園、どうでしたか？\nB：楽しかったです。パンダがかわいかったです。\nA：私はサルがよかったです。\nB：ああ、サルもかわいかったですね。また行きたいです。',
  'A: Sở thú thế nào? / B: Vui lắm. Gấu trúc dễ thương lắm. / A: Tôi thì thích khỉ. / B: À, khỉ cũng dễ thương nhỉ. Tôi muốn đi lại.',
  'B nói パンダ, A nói サル → 2 con. Không có ゾウ (voi) hay ライオン (sư tử) trong hội thoại.')
l(6, 'この人は何をお願いしましたか。', 'Người này đã nhờ việc gì?',
  ['漢字の読み方を教えてほしい', 'メールをチェックしてほしい', '教科書を見せてほしい', '書類の書き方を説明してほしい'], 1,
  'A：あのう、すみません。\nB：はい、何ですか？\nA：この漢字がわかりません。読み方を教えてもらえませんか？\nB：これですか？「いとう」です。\nA：ああ、いとうさんですね。ありがとうございます。',
  'A: À, xin lỗi. / B: Vâng, gì vậy? / A: Tôi không biết chữ Hán này. Anh chỉ cho tôi cách đọc được không? / B: Chữ này à? Đọc là "Itō". / A: À, anh Itō. Cảm ơn anh.',
  'Câu nhờ vả: 読み方を教えてもらえませんか. Đáp án diễn đạt lại bằng 〜てほしい (muốn người khác làm). 読み方 (ĐỘC PHƯƠNG) = cách đọc.')
l(7, 'コップやお皿はどうしますか。', 'Cốc và đĩa thì làm thế nào?',
  ['みんなで買う', 'バーベキュー場にあるので、持って行かない', '長谷川さんが持って行く', 'マルコさんが買う'], 2,
  '長谷川：じゃあ、私はおにぎりを作って行きますね。\n楊：いいですねえ。じゃあ、長谷川さんはおにぎりをお願いします。\nマルコ：コップやお皿は、どうしますか？\n長谷川：それは、バーベキュー場にありますから、だいじょうぶです。',
  'Hasegawa: Vậy tôi sẽ làm cơm nắm mang đến nhé. / Dương: Hay quá. Vậy nhờ chị Hasegawa phần cơm nắm. / Marco: Cốc và đĩa thì sao? / Hasegawa: Cái đó có sẵn ở khu BBQ nên không sao.',
  '〜から、だいじょうぶです = vì ~ nên không cần lo → không phải mang. 長谷川さん mang おにぎり, không phải cốc đĩa.')
l(8, '卵焼きはどうでしたか。', 'Món trứng cuộn thế nào?',
  ['すっぱかった', 'ちょっと苦手だった', '辛くておいしかった', '甘くておいしかった'], 4,
  'A：よかったら、この卵焼き、食べてみてください。\nB：ありがとうございます。……あ、甘くておいしいですね。\nA：もう1つどうですか？\nB：じゃあ、もう1ついただきます。',
  'A: Nếu được thì anh ăn thử món trứng cuộn này đi. / B: Cảm ơn chị. … À, ngọt và ngon quá. / A: Thêm 1 miếng nữa nhé? / B: Vậy tôi xin thêm 1 miếng.',
  '甘い (CAM) = ngọt; 辛い (TÂN) = cay; すっぱい = chua. B còn xin thêm もう1ついただきます → thích món này.')
l(9, '丸いテーブルはどう並べますか。', 'Bàn tròn sắp xếp thế nào?',
  ['3つずつ2列', '9つを1列', '3つずつ3列', '4つずつ3列'], 3,
  'A：テーブルは、どうやって並べますか？\nB：丸いテーブルを9個出して、3つずつ3列に並べてください。\nA：横に3つ並べて3列ですね。\nB：そうです。で、後ろにスペースをあけてください。あと、入口の横、入って左に、四角い長いテーブルを1つ置いてください。\nA：はい。',
  'A: Bàn thì xếp thế nào ạ? / B: Lấy 9 cái bàn tròn ra, xếp mỗi hàng 3 cái, thành 3 hàng. / A: Xếp ngang 3 cái, 3 hàng nhỉ. / B: Đúng. Rồi để trống chỗ phía sau. Thêm nữa, cạnh lối vào, bên trái khi đi vào, đặt 1 bàn dài hình vuông.',
  '〜ずつ = mỗi ~; 列 (LIỆT) = hàng. 9 cái chia 3 cái mỗi hàng → 3 hàng. 四角い長いテーブル là bàn khác, không phải bàn tròn.')
l(10, 'どの絵がこの人の症状ですか。', 'Tranh nào là triệu chứng của người này?',
  ['', '', '', ''], 1,
  'A：今日はどうしましたか？\nB：お腹が痛くて、吐き気がするんです。\nA：いつからですか？\nB：おとといからです。',
  'A: Hôm nay anh bị sao? / B: Tôi đau bụng và buồn nôn. / A: Từ khi nào? / B: Từ hôm kia.',
  'お腹が痛い = đau bụng → tranh 1. 吐き気がする = buồn nôn. Tranh 2: せきが出る (ho), tranh 3: のどが痛い (đau họng), tranh 4: 目がかゆい (ngứa mắt). 症状 (CHỨNG TRẠNG) = triệu chứng.',
  oimg=[f'y1_l10_{i}.jpg' for i in range(1, 5)])
l(11, '久保田さんはこれから何をしますか。', 'Chị Kubota sắp làm gì?',
  ['薬を飲む', 'コーヒーを買いに行く', '病院に行く', '家に帰る'], 2,
  'A：久保田さん、具合が悪そうですね。だいじょうぶですか？\nB：うん、肩がこって、頭が痛いのよ。\nA：そうですか。温かい飲み物を飲むといいですよ。コーヒーとかお茶とか。\nB：そう。じゃあ、ちょっとコーヒー買って来る。',
  'A: Chị Kubota trông không khoẻ nhỉ. Chị có sao không? / B: Ừ, mỏi vai, đau đầu. / A: Vậy à. Uống đồ uống ấm thì tốt đấy. Cà phê hay trà chẳng hạn. / B: Thế à. Vậy chị đi mua cà phê một chút.',
  'Câu cuối quyết định: じゃあ、ちょっとコーヒー買って来る (Vて来る = đi làm V rồi quay lại). 肩がこる = mỏi vai. Không nhắc đến 薬 hay 病院.')
l(12, 'スラーソーは何から作りますか。', 'Rượu Sraa Sor làm từ gì?',
  ['魚', 'お米', 'バナナ', '麦'], 2,
  'A：先生、お酒、好きですよね？\nB：うん、大好きだけど……。\nA：これ、スラーソーです。カンボジアのお酒です。先生にプレゼントです。\nB：え、いいの？\nA：お米から作った焼酎です。\nB：へー、焼酎、大好き。ありがとう。\nA：ちょっと強いですから、飲みすぎないでくださいね。',
  'A: Thầy thích rượu đúng không ạ? / B: Ừ, rất thích, nhưng… / A: Đây là Sraa Sor, rượu Campuchia. Em tặng thầy. / B: Ơ, được sao? / A: Là rượu trắng làm từ gạo. / B: Ồ, thầy rất thích shōchū. Cảm ơn em. / A: Rượu hơi mạnh nên thầy đừng uống nhiều quá nhé.',
  '〜から作る = làm từ (nguyên liệu). お米から作った焼酎 → gạo. 麦 (MẠCH) = lúa mì/lúa mạch – cũng dùng làm 焼酎 nhưng không phải trong bài.')

# ---------- 読解 ----------
def r(q, o, a, img, dich, gt):
    qs.append(Q(R, J(q), o, a, EX(o[a-1], dich, gt), [img]))
r('（1）ミンさんは日本に来て、どのくらいですか。', ['3年', '半年', '1年', '3か月'], 4, 'y1_r1.jpg',
  'Giới thiệu đồng nghiệp mới: Rất vui được gặp. Tôi là Nguyễn Minh, đến từ Hà Nội, Việt Nam. Tôi đến Nhật được 3 tháng. Hiện tôi làm ở bộ phận sản xuất. Công việc còn nhiều điều chưa biết nhưng mọi người tốt bụng nên ngày nào cũng vui. Sở thích là bóng đá. Ngày nghỉ tôi đá bóng với bạn ở công viên. Cùng chơi nhé? Rất mong được giúp đỡ.',
  'Câu 「日本に来て、3か月になります」. Chú ý phân biệt 3か月 (3 tháng) và 3年 (3 năm).')
r('（2）ミンさんについて正しいものはどれですか。', ['仕事はもうぜんぶわかる', 'ハノイで働いている', '休みの日に友だちとサッカーをする', 'しゅみは料理だ'], 3, 'y1_r1.jpg',
  '(Xem bản dịch câu trước.)',
  '「休みの日は公園で友だちとサッカーをします」 → đáp án 3. Sai: 仕事は「まだわからないことが多い」; ハノイは出身地, 今は日本のせいぞう部で働いている; しゅみはサッカー.')
r('（1）いちばん寒い日は何曜日ですか。', ['月曜日', '木曜日', '水曜日', '火曜日'], 3, 'y1_r3.jpg',
  'Thời tiết tuần này: Thứ 2 nắng 18°C 10%; Thứ 3 nhiều mây 15°C 40%; Thứ 4 mưa 12°C 90%; Thứ 5 mưa rồi tạnh 16°C 60%; Thứ 6 nắng 20°C 0%.',
  'Lạnh nhất → nhìn cột 最高気温 (nhiệt độ cao nhất), số nhỏ nhất là 12度 = 水曜日.')
r('（2）かさがいらない日はどれですか。', ['金曜日', '水曜日', '火曜日', '木曜日'], 1, 'y1_r3.jpg',
  '(Xem bản dịch câu trước.)',
  'Không cần ô → ngày nắng, 雨の確率 (xác suất mưa) thấp nhất: 金曜日 晴れ・0%. 雨のち晴れ = mưa sau đó nắng, vẫn có mưa.')
r('（1）ゆかさんはどこで待っていますか。', ['北口の本屋', '北口の改札', '南口の改札の前の本屋', '映画館の中'], 3, 'y1_r5.jpg',
  'Lan: Xin lỗi! Mình bị lạc đường, sẽ đến muộn chút. / Lan: Giờ mình đang ở cửa Bắc ga Sakura. / Yuka: Không sao chứ? Chỗ hẹn là cửa soát vé phía Nam đó. / Lan: Ơ, vậy à! Vậy mình đến cửa Nam ngay. Chắc khoảng 10 phút là tới. / Yuka: OK. Phim chiếu từ 7 giờ nên vẫn kịp. Mình đợi ở hiệu sách trước cửa soát vé nhé.',
  'Tin nhắn cuối: 「改札の前の本屋で待ってるね」, và 改札 là 南口の改札 (chỗ hẹn). 北口 là nơi Lan đang đứng.')
r('（2）ランさんは何時ごろ着きますか。', ['6時45分ごろ', '7時半ごろ', '6時半ごろ', '7時ごろ'], 1, 'y1_r5.jpg',
  '(Xem bản dịch câu trước.)',
  'Lan nhắn lúc 18:35: 「10分ぐらいで着くと思います」 → khoảng 18:45 = 6時45分ごろ. 7時 là giờ chiếu phim, không phải giờ Lan đến.')
r('（1）道具を持って行かなくてもいい教室はどれですか。', ['書道', '合気道', 'ヨガ', '料理'], 1, 'y1_r7.jpg',
  'Lớp học mùa thu – Nhà văn hoá Sakura: Yoga: thứ 3 hằng tuần 10:00–11:00, 500 yên/buổi, mang khăn và nước. Nấu ăn: thứ 5 tuần 1 và 3, 18:30–20:30, 800 yên/buổi, mang tạp dề. Thư pháp: thứ 7 hằng tuần 14:00–15:30, 600 yên/buổi, không cần mang (có cho mượn dụng cụ). Aikido: chủ nhật hằng tuần 9:00–10:30, 2.000 yên/tháng, quần áo vận động được.',
  'Vなくてもいい = không cần làm V. Cột 持ち物: 書道 「いりません（道具はかします）」. 道具 (ĐẠO CỤ) = dụng cụ, かす = cho mượn.')
r('（2）1か月に2回ある教室はどれですか。', ['書道', '合気道', '料理', 'ヨガ'], 3, 'y1_r7.jpg',
  '(Xem bản dịch câu trước.)',
  '第1・第3木曜日 = thứ 5 tuần thứ nhất và tuần thứ ba → 2 lần/tháng = 料理. Các lớp 毎週 (hằng tuần) có khoảng 4 lần/tháng.')
r('（1）ペットボトルを出す前に何をしますか。', ['ふたとラベルをとって、中をあらう', '小さく切る', '紙といっしょに出す', 'そうむ部に連絡する'], 1, 'y1_r9.jpg',
  'Cách bỏ rác: Rác cháy được (giấy, đồ ăn) – mỗi ngày. Chai nhựa – bỏ nắp và nhãn, rửa bên trong – thứ 3, thứ 6. Lon, chai thuỷ tinh – rửa bên trong – thứ 4. Rác lớn – liên lạc bộ phận tổng vụ.',
  'Hàng ペットボトル, cột 注意: 「ふたとラベルをとって、中をあらってください」. そうむ部に連絡 là quy định cho 大きいごみ.')
r('（2）水曜日に出せるものはどれですか。', ['大きいごみ', 'かんともえるごみ', 'ペットボトルだけ', 'ペットボトルとかん'], 2, 'y1_r9.jpg',
  '(Xem bản dịch câu trước.)',
  'Thứ 4 (水) là ngày bỏ かん・びん; もえるごみ bỏ 毎日 (mỗi ngày) nên thứ 4 cũng được → かんともえるごみ. ペットボトル chỉ bỏ 火・金.')
r('（1）ノロウイルスにかんせんする原因は何ですか。', ['野菜をたくさん食べること', '運動しないこと', '生のカキを食べること', '水を飲みすぎること'], 3, 'y1_r11.jpg',
  'Hãy cẩn thận với virus Noro – Trung tâm y tế thành phố. Gần đây ngộ độc thực phẩm do virus Noro đang tăng. Ăn sống hoặc ăn không nấu kỹ các loại sò như hàu có thể bị nhiễm. Khi nhiễm sẽ đau bụng, nôn. Để phòng: rửa tay kỹ bằng xà phòng trước khi nấu ăn và sau khi đi vệ sinh; nấu chín kỹ sò đến tận bên trong (85–90°C trên 90 giây); khi không khoẻ thì không nấu ăn.',
  '「カキなどの貝を生で食べたり…すると、かんせんすることがあります」. 原因 (NGUYÊN NHÂN) = nguyên nhân, かんせん = 感染 (CẢM NHIỄM) = lây nhiễm.')
r('（2）正しいものはどれですか。', ['貝は少し加熱すればいい', '具合が悪いときも料理をしていい', 'トイレのあとは水だけでいい', '料理の前にせっけんで手をあらう'], 4, 'y1_r11.jpg',
  '(Xem bản dịch câu trước.)',
  '「料理の前とトイレのあとは、せっけんでよく手をあらいましょう」 → 4. Sai: 貝は「中までよく」加熱; 具合が悪いときは料理をしない; トイレのあとも せっけん.')

ex = dict(id='jft-y1', group='Đề thi thử JFT-Basic', title='Đề 25',
          sub='Có phần nghe · いろどり 初級1', short='Đề 25', time=60, qs=qs)
E = json.load(open(REPO + 'src/raw/jft_exams.json'))
E = [e for e in E if e['id'] != 'jft-y1']
pos = max(i for i, e in enumerate(E) if e['id'].startswith('jft-g')) + 1
E = E[:pos] + [ex] + E[pos:]
json.dump(E, open(REPO + 'src/raw/jft_exams.json', 'w'), ensure_ascii=False, indent=1)
print(len(qs), [sum(q['s'] == s for q in qs) for s in (V, K, L, R)])
