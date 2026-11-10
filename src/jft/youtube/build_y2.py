import json, html, shutil, os, sys
sys.path.insert(0, '/home/claude/anhtrong-jft-app/src/jft')
from furi import furi
REPO = '/home/claude/anhtrong-jft-app/'
IMG = 'app/media/jft/img/'; AU = 'app/media/jft/au/'
for f in os.listdir('/tmp/yt2/img'): shutil.copy('/tmp/yt2/img/' + f, REPO + 'public/' + IMG + f)
for f in os.listdir('/tmp/yt2/au'): shutil.copy('/tmp/yt2/au/' + f, REPO + 'public/' + AU + f)

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
def v(t, o, a, dich, gt, imgs=(), raw=None):
    qs.append(Q(V, raw if raw else J(t), o, a, EX(o[a-1], dich, gt, fu=False), imgs, fu_opt=False))
# ---------- 文字と語彙 ----------
v(PIC, ['目が　かゆい', 'お腹が　痛い', 'せきが　出る', '吐き気が　する'], 3,
  'Tranh: người đàn ông đưa tay lên miệng, ho ra hơi → bị ho.',
  'せきが　出る = bị ho. Cùng nhóm triệu chứng: 目がかゆい (MỤC) = ngứa mắt, お腹が痛い (PHÚC – THỐNG) = đau bụng, 吐き気がする (THỔ KHÍ) = buồn nôn. いろどり 初級1 第15課.', ['y2_v1.jpg'])
v(PIC, ['暖かい', '寒い', 'すずしい', 'じめじめする'], 4,
  'Tranh: ngoài trời mưa, người đổ mồ hôi, cầm quạt → trời ẩm, oi bức.',
  'じめじめする = ẩm ướt, oi (như 蒸し暑い – nóng ẩm). 暖かい (NOÃN) = ấm áp, 寒い (HÀN) = lạnh, すずしい = mát. Mưa + mồ hôi là dấu hiệu của じめじめ. いろどり 初級1 第3課.', ['y2_v2.jpg'])
v(PIC, ['にぎやか（な）', '不便（な）', '便利（な）', '都会'], 2,
  'Tranh: vùng quê, trạm xe buýt với bảng giờ rất thưa → bất tiện.',
  '不便（な）(BẤT TIỆN) = bất tiện; bảng giờ xe buýt chỉ có vài chuyến (バスが少ない). Trái nghĩa 便利（な）. にぎやか = náo nhiệt, 都会 (ĐÔ HỘI) = thành phố lớn. いろどり 初級1 第5課.', ['y2_v3.jpg'])
v('つぎのしんごうを右に（　　）ください。', ['わたって', 'まよって', 'まがって', 'おりて'], 3,
  'Hãy rẽ phải ở đèn giao thông tiếp theo.',
  '右に　まがる = rẽ phải (đi với trợ từ に chỉ hướng). しんごうを　わたる = băng qua đèn giao thông (trợ từ を), 道に　まよう = lạc đường, おりる = xuống xe. Câu chỉ đường – いろどり 初級1 第6課.')
v('えきがちかくて、この町はとても（　　）です。', ['ふべん', 'しずか', 'ひま', 'べんり'], 4,
  'Ga gần nên thị trấn này rất tiện lợi.',
  'Vế trước えきがちかくて (ga gần) là lý do → べんり (便利 – TIỆN LỢI). ふべん là nghĩa ngược lại. しずか = yên tĩnh, ひま = rảnh – không liên quan đến "ga gần". いろどり 初級1 第5課.')
v('レモンはとても（　　）です。', ['あまい', 'からい', 'すっぱい', 'にがい'], 3,
  'Chanh rất chua.',
  'Bốn vị cơ bản: あまい (甘い – ngọt), からい (辛い – cay), すっぱい (chua), にがい (苦い – đắng). Chanh → すっぱい. いろどり 初級1 第12課.')
v('', ['じごと', 'しごと', 'しごど', 'しこと'], 2,
  'Tôi đang làm công việc chăm sóc (điều dưỡng) ở Nhật.',
  '仕事 (SĨ SỰ) đọc là しごと = công việc. Các phương án sai lệch ở âm đục: じごと (し→じ), しごど (と→ど), しこと (ご→こ). 介護 (GIỚI HỘ) = điều dưỡng, chăm sóc.',
  raw='日本で介護の<u>仕事</u>をしています。')
v('', ['じんごう', 'しんご', 'しんごう', 'しんこう'], 3,
  'Hãy băng qua đèn giao thông tiếp theo.',
  '信号 (TÍN HIỆU) đọc là しんごう = đèn giao thông. 号 đọc ごう (trường âm). しんご thiếu う, しんこう sai âm đục, じんごう sai âm đầu.',
  raw='つぎの<u>信号</u>をわたってください。')
v('', ['うまい', 'にがい', 'からい', 'あまい'], 4,
  'Món trứng cuộn này ngọt nhỉ.',
  '甘い (CAM) đọc là あまい = ngọt. Phân biệt chữ Hán các vị: 苦い (KHỔ) にがい = đắng, 辛い (TÂN) からい = cay. うまい = ngon (khẩu ngữ).',
  raw='この卵焼きは<u>甘い</u>ですね。')
v('', ['体', '休', '林', '本'], 2,
  'Ngày mai tôi sẽ xin nghỉ.',
  'やすみ = 休み (HƯU) – người 亻 dựa vào cây 木 để nghỉ. Các chữ trông giống: 体 (THỂ – からだ), 林 (LÂM – はやし), 本 (BẢN – ほん). 休みをとる = xin nghỉ.',
  raw='あしたは<u>やす</u>みをとります。')
v('', ['人', '入', '大', '八'], 1,
  'Người dân thị trấn này hiền hoà.',
  'ひと = 人 (NHÂN). Dễ nhầm: 入 (NHẬP – はいる, nét phải đè lên), 大 (ĐẠI – おおきい), 八 (BÁT – やっつ, hai nét tách rời).',
  raw='この町は<u>ひと</u>がやさしいです。')
v('', ['良べ物', '食べ物', '飯べ物', '食べ持'], 2,
  'Món ăn bạn thích là gì?',
  'たべもの = 食べ物 (THỰC VẬT). 良 (LƯƠNG) thiếu phần mái trên của 食; 飯 (PHẠN – ごはん) có bộ 食 bên trái; 持 (TRÌ – もつ) giống 物 nhưng bộ thủ 扌 khác bộ 牛.',
  raw='すきな<u>たべもの</u>は何ですか。')

# ---------- 会話と表現 ----------
def k(t, o, a, dich, gt):
    qs.append(Q(K, J(t), o, a, EX(o[a-1], dich, gt)))
k('山田：日本に来て、どのぐらいになりますか。\nロン：（　　）。\n山田：そうですか。',
  ['1年にしました', '1年ぐらい行きます', '1年になります', '1年前に来ます'], 3,
  'Yamada: Anh đến Nhật được bao lâu rồi? / Long: Được 1 năm rồi. / Yamada: Vậy à.',
  'Hỏi bằng 〜になりますか thì đáp bằng 〜になります (khoảng thời gian đã trôi qua). 1年前に来ます sai thì (đã đến phải là 来ました). いろどり 初級1 第1課.')
k('木村：週末、何をしましたか。\nニン：友だちとカラオケに（　　）。',
  ['行きました', '行きましょう', '行きたいです', '行きます'], 1,
  'Kimura: Cuối tuần bạn đã làm gì? / Ninh: Tôi đã đi karaoke với bạn.',
  'Câu hỏi 〜しましたか (quá khứ) → trả lời bằng quá khứ 行きました. 行きましょう là rủ rê, 行きたいです là mong muốn, 行きます là tương lai. いろどり 初級1 第2課.')
k('山本：明日の天気はどうですか。\nリン：天気予報によると、晴れる（　　）。',
  ['でしょう', 'ましょう', 'たいです', 'ません'], 1,
  'Yamamoto: Thời tiết ngày mai thế nào? / Rin: Theo dự báo thời tiết thì trời sẽ nắng.',
  'Dự đoán thời tiết: thể thường + でしょう. 天気予報によると (theo dự báo) báo hiệu câu phỏng đoán. ましょう, たいです, ません phải đi với thể ます (晴れ〜), không gắn vào 晴れる. いろどり 初級1 第4課.')
k('通行人：2つ目の信号を左に（　　）。\nミン：2つ目の信号を左ですね。',
  ['曲がりたいです', '曲がりました', '曲がるでしょう', '曲がってください'], 4,
  'Người qua đường: Anh rẽ trái ở đèn giao thông thứ hai. / Minh: Đèn thứ hai rẽ trái nhỉ.',
  'Chỉ đường dùng Vて　ください. Minh nhắc lại để xác nhận → người kia vừa chỉ dẫn. 曲がる (KHÚC) = rẽ. いろどり 初級1 第6課.')
k('鈴木：今度、いっしょに動物園に（　　）。\nアナ：いいですね。ぜひ。',
  ['行かないでください', '行きましたか', '行っていますか', '行きませんか'], 4,
  'Suzuki: Lần tới cùng đi sở thú không? / Ana: Hay đấy. Nhất định rồi.',
  'Rủ rê: Vませんか. 今度 (lần tới) + いっしょに là dấu hiệu lời mời; đáp いいですね。ぜひ = nhận lời. いろどり 初級1 第8課.')
k('アリ：それ、新しい教科書ですか。ちょっと（　　）。\n西村：どうぞ。',
  ['見せてもらえませんか', '見えますか', '見てあげませんか', '見せましたか'], 1,
  'Ali: Đó là sách giáo khoa mới à? Cho tôi xem một chút được không? / Nishimura: Mời anh.',
  'Nhờ người khác cho mình xem: 見せて　もらえませんか (見せる = cho xem). Đáp どうぞ = đưa cho. 見える = nhìn thấy được – khác nghĩa. いろどり 初級1 第9課.')
k('マルコ：重そうですね。（　　）。\n楊：だいじょうぶです。ありがとうございます。',
  ['手伝ってください', '手伝いましたか', '手伝わないで', '手伝いましょうか'], 4,
  'Marco: Trông nặng nhỉ. Để tôi giúp nhé? / Dương: Không sao đâu. Cảm ơn anh.',
  'Đề nghị giúp đỡ: Vましょうか. Thấy người khác mang đồ nặng (重そう) → 手伝いましょうか. Đáp だいじょうぶです = từ chối lịch sự. 手伝ってください là nhờ người khác giúp mình. いろどり 初級1 第11課.')
k('田村：すき焼き、おいしいですね。\nフエン：よかった。（　　）食べてください。',
  ['だんだん', 'なかなか', 'そろそろ', 'どんどん'], 4,
  'Tamura: Sukiyaki ngon quá nhỉ. / Huyền: May quá. Anh cứ ăn nhiều vào nhé.',
  'どんどん = cứ thoải mái, liên tục (mời ăn nhiều). だんだん = dần dần, なかなか = mãi mà (không), khá là, そろそろ = sắp đến lúc. いろどり 初級1 第12課.')
k('アリ：会議の準備は、どうしますか。\n上司：アリさんは机をコの字に（　　）。',
  ['並べたいです', '並べてください', '並びましょう', '並んでいました'], 2,
  'Ali: Chuẩn bị cuộc họp thì làm thế nào ạ? / Cấp trên: Anh Ali hãy xếp bàn thành hình chữ コ.',
  'Cấp trên giao việc → Vて　ください. 並べる (tha động từ – xếp cái gì) đi với 机を; 並ぶ (tự động từ – xếp hàng) không đi với を. コの字 = hình chữ U. いろどり 初級1 第13課.')
k('医者：ご飯は食べていますか。\n郭：いえ、食欲が（　　）……。',
  ['ないと', 'なくて', 'あって', 'なくても'], 2,
  'Bác sĩ: Anh có ăn cơm không? / Quách: Không, tôi không thấy thèm ăn nên…',
  'Nêu lý do bằng thể て: 食欲がなくて (vì không có cảm giác thèm ăn). Câu bỏ lửng …… là cách nói tự nhiên. 食欲 (THỰC DỤC) = cảm giác thèm ăn. いろどり 初級1 第15課.')
k('西田：最近、胃の調子が悪いんです。\n佐藤：お腹を（　　）いいですよ。',
  ['温めたらだめ', '温めると', '温めても', '冷やすと'], 2,
  'Nishida: Gần đây dạ dày tôi không ổn. / Sato: Chườm ấm bụng thì tốt đấy.',
  'Khuyên: Vると　いいですよ. 温める (ÔN) = làm ấm; 冷やす (LÃNH) = làm lạnh – không tốt cho dạ dày. 温めても là "dù có làm ấm". いろどり 初級1 第16課.')
k('ミン：すみません。科学博物館はどこですか。\n通行人：橋を渡って、すぐ右に曲がった（　　）にありますよ。',
  ['ところ', 'もの', 'とき', 'こと'], 1,
  'Minh: Xin lỗi, bảo tàng khoa học ở đâu ạ? / Người qua đường: Qua cầu, rẽ phải ngay là đến chỗ đó.',
  'Chỉ vị trí: Vた　ところに　あります = ở chỗ sau khi làm V. ところ chỉ nơi chốn; もの = đồ vật, とき = lúc, こと = việc. いろどり 初級1 第6課.')

# ---------- 聴解 ----------
def l(n, q, vi, o, a, script, dich, gt):
    t = f'<span class="jp">{J(q)}</span><br><span class="vi-q">{html.escape(vi)}</span>'
    qs.append(Q(L, t, o, a, EX(o[a-1], dich, gt, script), au=AU + f'y2_L{n:02d}.mp3'))
l(1, 'この人はいつ日本に来ましたか。', 'Người này đến Nhật khi nào?',
  ['今年の9月', '去年の9月', '半年前', '先月'], 2,
  'A：日本に来て、どのぐらいですか？\nB：去年の9月に来ました。\nA：そうですか。もう慣れましたか？\nB：はい、おかげさまで。',
  'A: Anh đến Nhật được bao lâu rồi? / B: Tôi đến vào tháng 9 năm ngoái. / A: Vậy à. Đã quen chưa? / B: Rồi, nhờ trời.',
  '去年 (KHỨ NIÊN) = năm ngoái, 今年 = năm nay, 先月 = tháng trước, 半年前 = nửa năm trước. B trả lời rõ 去年の9月.')
l(2, 'タムさんの国の雨季はどうですか。', 'Mùa mưa ở nước của Tâm thế nào?',
  ['とても暑くなる', 'とても寒くなる', '雪がふる', '少しすずしくなって、雨がたくさんふる'], 4,
  'A：タムさんの国には、どんな季節がありますか？\nB：雨季と乾季があります。\nA：そうですか。\nB：乾季はとても暑いです。\nA：へー。\nB：でも、雨季は少しすずしくなります。雨がたくさん降ります。',
  'A: Ở nước anh Tâm có những mùa nào? / B: Có mùa mưa và mùa khô. / A: Vậy à. / B: Mùa khô rất nóng. / A: Ồ. / B: Nhưng mùa mưa thì mát hơn một chút. Mưa rất nhiều.',
  'Câu hỏi về 雨季 (VŨ QUÝ – mùa mưa), không phải 乾季 (CAN QUÝ – mùa khô). とても暑い là nói về 乾季. Sau でも: 雨季は少しすずしくなります.')
l(3, '「南スポーツセンター」はどんなところですか。', '"Trung tâm thể thao Minami" là nơi như thế nào?',
  ['高いけど、広い', '遠いけど、静か', '建物は古いけど、安い', '新しくて、きれい'], 3,
  'A：休みの日にどこか行きたいんですが、いいところがありますか？\nB：そうね……。スポーツは好き？\nA：はい。\nB：じゃあ、「南スポーツセンター」とかはどう？\nA：スポーツセンター？\nB：建物は古いけど、安くていいわよ。\nA：そうですか。',
  'A: Ngày nghỉ tôi muốn đi đâu đó, có chỗ nào hay không ạ? / B: Để xem… Em thích thể thao không? / A: Có. / B: Vậy "Trung tâm thể thao Minami" thì sao? / A: Trung tâm thể thao ạ? / B: Toà nhà thì cũ, nhưng rẻ nên tốt lắm. / A: Vậy ạ.',
  'Câu 建物は古いけど、安くていいわよ khớp với đáp án 3. 〜けど = nhưng (nối điểm xấu và điểm tốt). 古い (CỔ) = cũ, 安い (AN) = rẻ.')
l(4, '金曜日の10時に、まずどこに行きますか。', '10 giờ thứ Sáu, trước tiên đi đến đâu?',
  ['部屋', '門の前', '受付', '駅'], 3,
  'A：では、金曜日の10時に来てください。\nB：金曜日の10時ですね。えーと、場所はどこですか？\nA：受付に来てください。そのあと、部屋に案内します。\nB：わかりました。',
  'A: Vậy anh đến lúc 10 giờ thứ Sáu nhé. / B: 10 giờ thứ Sáu ạ. À, địa điểm ở đâu ạ? / A: Anh đến quầy lễ tân. Sau đó tôi sẽ dẫn anh vào phòng. / B: Tôi hiểu rồi.',
  'まず = trước tiên. 受付に来てください → sau đó (そのあと) mới đến 部屋. 受付 (THỤ PHÓ) = quầy lễ tân, 案内 (ÁN NỘI) = hướng dẫn, dẫn đường.')
l(5, '展覧会はどうでしたか。', 'Buổi triển lãm thế nào?',
  ['人が多かった', 'かんどうした', 'とてもおもしろかった', '難しくて、よくわからなかった'], 4,
  'A：今日の展覧会、どうでしたか？\nB：うーん。ちょっと難しかったです。\nA：あー、現代の作品はねえ。\nB：よくわかりませんでした。',
  'A: Triển lãm hôm nay thế nào? / B: Ừm, hơi khó. / A: À, tác phẩm hiện đại mà. / B: Tôi không hiểu lắm.',
  'うーん + ちょっと難しかった là cảm nhận không tích cực; câu cuối よくわかりませんでした. 展覧会 (TRIỂN LÃM HỘI) = triển lãm, 作品 (TÁC PHẨM) = tác phẩm.')
l(6, 'この人は何をお願いしましたか。', 'Người này đã nhờ việc gì?',
  ['漢字の読み方を教えてほしい', '教科書を貸してほしい', 'メールを送ってほしい', 'メールの日本語をチェックしてほしい'], 4,
  'A：あのう、すみません。\nB：はい。\nA：私のメール、日本語をチェックしてもらえませんか？ちょっと自信がありません。\nB：いいですよ。えーと……。',
  'A: À, xin lỗi. / B: Vâng. / A: Anh xem giúp tiếng Nhật trong email của tôi được không? Tôi hơi không tự tin. / B: Được thôi. Để xem…',
  'Câu nhờ: 〜をチェックしてもらえませんか. Không nhờ gửi (送る) email mà nhờ kiểm tra tiếng Nhật. 自信 (TỰ TÍN) = sự tự tin.')
l(7, 'ノイさんは何を持って行きますか。', 'Noi sẽ mang gì đến?',
  ['おにぎり', 'お茶', 'ケーキ', 'バナナ'], 4,
  'ノイ：私は、何を持って行きましょうか？\n長谷川：じゃあ、ノイさん、デザートはどうですか？\nノイ：そうですねえ、じゃあ、バナナを持って行きます。焼いて食べましょう。\n長谷川：え、バナナ？焼くんですか？\nノイ：はい。おいしいですよ。',
  'Noi: Tôi nên mang gì đến ạ? / Hasegawa: Vậy chị Noi mang món tráng miệng nhé? / Noi: Để xem, vậy tôi mang chuối. Nướng lên ăn nhé. / Hasegawa: Hả, chuối á? Nướng sao? / Noi: Vâng. Ngon lắm đấy.',
  'Noi nói rõ バナナを持って行きます. デザート là gợi ý của Hasegawa; ケーキ không xuất hiện. 焼く = nướng.')
l(8, 'この人はもう少し食べますか。', 'Người này có ăn thêm không?',
  ['食べる。おなかがすいている', '食べない。おいしくない', '食べない。おなかがいっぱい', '食べる。とてもおいしい'], 3,
  'A：お好み焼き、どう？おいしい？\nB：はい、おいしいです。私の国のバインセオに似ています。\nA：もう少し食べる？\nB：あ、だいじょうぶです。もうお腹がいっぱいです。',
  'A: Okonomiyaki thế nào? Ngon không? / B: Vâng, ngon ạ. Giống bánh xèo ở nước tôi. / A: Ăn thêm chút nữa không? / B: À, không sao đâu ạ. Tôi no rồi.',
  'だいじょうぶです ở đây là lời từ chối lịch sự (= không cần), lý do もうお腹がいっぱいです (no rồi). Món ăn vẫn ngon nên 2 sai. 〜に似ています = giống với ~.')
l(9, 'アリさんの仕事は何ですか。', 'Việc của Ali là gì?',
  ['机をコの字に並べて、パソコンとプロジェクタを準備する', '飲み物を用意する', '外のお店に電話する', '資料を人数分コピーする'], 1,
  'アリ：会議の準備は、どうしますか？\n上司：アリさんは、部屋のセッティング、西村さんは、資料の準備をお願いします。アリさんは、部屋の机をコの字に並べて、それからパソコンとプロジェクタを準備してください。西村さんは、資料を人数分コピーして、机の上に1部ずつ並べてください。\n西村：飲み物は用意しますか？\n上司：それは、外のお店に頼んだから、いいです。',
  'Ali: Chuẩn bị họp thì làm thế nào ạ? / Cấp trên: Anh Ali sắp xếp phòng, chị Nishimura chuẩn bị tài liệu. Anh Ali xếp bàn thành hình chữ U, sau đó chuẩn bị máy tính và máy chiếu. Chị Nishimura photo tài liệu đủ số người, đặt mỗi bàn 1 bản. / Nishimura: Có chuẩn bị đồ uống không ạ? / Cấp trên: Cái đó đã nhờ cửa hàng bên ngoài rồi nên không cần.',
  'Hội thoại giao việc cho 2 người – phải nghe đúng tên. 資料をコピー là việc của 西村さん; 飲み物 đã nhờ 外のお店. 準備 (CHUẨN BỊ), 資料 (TƯ LIỆU), 人数分 = đủ số người.')
l(10, 'この人の症状は何ですか。', 'Triệu chứng của người này là gì?',
  ['熱があって、のどが痛い', 'お腹が痛くて、吐き気がする', '目がかゆくて、鼻水が出る', '足をくじいた'], 1,
  'A：今日はどうしましたか？\nB：昨日から38度の熱があって、のどがすごく痛いんです。\nA：そうですか。ご飯は食べてますか？\nB：いえ、食欲がなくて……。',
  'A: Hôm nay anh bị sao? / B: Từ hôm qua tôi sốt 38 độ, họng đau lắm. / A: Vậy à. Anh có ăn cơm không? / B: Không, tôi không thấy thèm ăn…',
  '熱がある = sốt, のどが痛い = đau họng → 1. 食欲がない là phụ, không phải lựa chọn. 足をくじく = trẹo chân. 症状 (CHỨNG TRẠNG) = triệu chứng.')
l(11, '胃の調子が悪いときは、どうするといいですか。', 'Khi dạ dày không ổn thì nên làm gì?',
  ['冷たいものを飲む', 'お腹を温めて、マッサージする', '運動する', 'たくさん食べる'], 2,
  'A：西田さん、どうしたんですか？だいじょうぶですか？\nB：うん、最近、胃の調子が悪いんですよ。\nA：ああ、大変ですね……。お腹を温めるといいですよ。あと、マッサージも。\nB：そうなんですか。やってみます。',
  'A: Anh Nishida sao vậy? Có ổn không? / B: Ừ, gần đây dạ dày tôi không tốt. / A: Ôi, vất vả quá… Chườm ấm bụng thì tốt đấy. Thêm nữa là xoa bóp. / B: Vậy à. Tôi sẽ thử.',
  'Lời khuyên 〜といいですよ: お腹を温める + マッサージ (あと = thêm nữa). 胃 (VỊ) = dạ dày, 調子 (ĐIỀU TỬ) = tình trạng.')
l(12, 'マグカップはどうしましたか。', 'Chiếc cốc (mug) có được như thế nào?',
  ['誕生日に友だちにもらった', '母がくれた', '日本で買った', '自分で作った'], 1,
  'A：そのパンダのマグカップ、かわいいですね。\nB：あ、ありがとうございます。\nA：中国から持って来たんですか？\nB：はい。誕生日に、友だちにもらったんです。\nA：そうですか。',
  'A: Cái cốc hình gấu trúc đó dễ thương nhỉ. / B: À, cảm ơn chị. / A: Mang từ Trung Quốc sang à? / B: Vâng. Bạn tặng tôi vào ngày sinh nhật.',
  '〜にもらう = nhận từ ~ (友だちにもらった = được bạn tặng). 母がくれた cũng là "được tặng" nhưng người tặng sai. 誕生日 (ĐẢN SINH NHẬT) = sinh nhật.')

# ---------- 読解 ----------
def r(q, o, a, img, dich, gt):
    qs.append(Q(R, J(q), o, a, EX(o[a-1], dich, gt), [img]))
r('（1）アナさんは今、どこで働いていますか。', ['大阪のホテル', '東京の工場', '大阪の工場', '東京のホテル'], 1, 'y2_r1.jpg',
  'Ana: Rin ơi, lâu quá không gặp! Bạn khoẻ không? / Ana: Mình làm ở khách sạn ở Osaka từ tháng trước. Công việc bận nhưng vui. / Rin: Ana! Lâu quá không gặp. Mình khoẻ. Mình vẫn làm ở nhà máy ở Tokyo. / Ana: Tháng sau mình lên Tokyo. Cùng đi ăn nhé?',
  'Tin nhắn của アナ: 「先月から大阪のホテルで働いています」. 東京の工場 là chỗ làm của リン (người nhận).')
r('（2）アナさんは来月何をしますか。', ['仕事をやめる', '東京に行く', '工場で働く', '大阪に帰る'], 2, 'y2_r1.jpg',
  '(Xem bản dịch câu trước.)',
  '「来月、東京に行きます」. 来月 (LAI NGUYỆT) = tháng sau, 先月 (TIÊN NGUYỆT) = tháng trước – chú ý không nhầm hai mốc này.')
r('（1）あした、どうしますか。', ['朝早く会社に行く', 'かさを持って会社に行く', '会社を休んで、家にいる', '夜7時に会社に行く'], 3, 'y2_r3.jpg',
  'Người gửi: Bộ phận tổng vụ | Tiêu đề: Về cơn bão. Mọi người, ngày mai bão đến. Từ sáng mưa và gió sẽ rất mạnh. Ngày mai công ty cho nghỉ. Hãy ở nhà, đừng ra ngoài. Ngày kia có đi làm hay không, tối mai 7 giờ sẽ báo qua email.',
  '「あしたは会社を休みにします。家から出ないでください」 → nghỉ và ở nhà. 7時 là giờ gửi email, không phải giờ đến công ty.')
r('（2）あさってのことはいつわかりますか。', ['今日の夜7時', 'あしたの夜7時', 'あしたの朝', 'あさっての朝'], 2, 'y2_r3.jpg',
  '(Xem bản dịch câu trước.)',
  '「あさって会社があるかどうかは、あしたの夜7時にメールで連絡します」. 〜かどうか = có ~ hay không. あした (ngày mai) ≠ あさって (ngày kia).')
r('（1）あしたは何時にどこに集まりますか。', ['8時に会社の門の前', '8時に工場の前', '4時に会社の門の前', '8時に食堂'], 1, 'y2_r5.jpg',
  'Người gửi: Tanaka | Tiêu đề: Tham quan nhà máy ngày mai. Mọi người, ngày mai đi tham quan nhà máy. Tập trung trước cổng công ty lúc 8 giờ sáng. Đi bằng xe buýt. Trong nhà máy không được chụp ảnh. Bữa trưa ăn ở nhà ăn của nhà máy nên không cần mang cơm hộp. Khoảng 4 giờ sẽ về lại công ty.',
  '「朝8時に会社の門の前に集まってください」. 4時 là giờ về công ty; 食堂 là nơi ăn trưa. 集まる (TẬP) = tập trung.')
r('（2）工場見学でしてはいけないことは何ですか。', ['写真をとる', '4時にもどる', '食堂で食べる', 'バスに乗る'], 1, 'y2_r5.jpg',
  '(Xem bản dịch câu trước.)',
  'Vては　いけない = không được làm V ↔ trong bài là Vないでください: 「写真をとらないでください」. Các phương án còn lại đều là việc sẽ làm.')
r('（1）どうやって申し込みますか。', ['当日行く', '電話をする', 'メールを送る', '公民館の受付で書く'], 4, 'y2_r7.jpg',
  'Lớp trải nghiệm trà đạo. Bạn có muốn trải nghiệm trà Nhật không? Thời gian: 8/6 (CN) ① 10:00–11:00 ② 14:00–15:00. Số người: mỗi buổi 10 người. Phí: miễn phí (có kèm bánh). Đăng ký: trước ngày 1/6, viết tên và số điện thoại tại quầy lễ tân nhà văn hoá. Không nhận đăng ký qua điện thoại. ※ Hãy mang tất khi đến.',
  '「公民館の受付で名前と電話番号を書いてください。電話では申し込めません」. 申し込む (THÂN VÀO) = đăng ký, 当日 (ĐƯƠNG NHẬT) = ngay hôm đó.')
r('（2）体験教室について正しいものはどれですか。', ['1日1回だけある', '20人まで参加できる', 'お金はいらない', 'お菓子は自分で持って行く'], 3, 'y2_r7.jpg',
  '(Xem bản dịch câu trước.)',
  '「お金：無料」 → không mất tiền. Có 2 buổi (①②) nên 1 sai; 定員はそれぞれ10人 = mỗi buổi tối đa 10 người; お菓子がつきます = có kèm bánh, không phải tự mang. 無料 (VÔ LIỆU) = miễn phí.')
r('（1）アリさんは何をしますか。', ['ドラッグストアに電話する', 'お金を返す', '倉庫をそうじする', 'トイレットペーパーを買いに行く'], 4, 'y2_r9.jpg',
  'Cấp trên: Anh Ali, xin lỗi. Giấy vệ sinh trong kho hết rồi. / Cấp trên: Trước 3 giờ, anh mua giúp ở hiệu thuốc trước ga được không? Nhờ anh 10 cuộn. / Cấp trên: Tiền thì tôi trả lại sau. Nhớ lấy hoá đơn về nhé. / Ali: Tôi hiểu rồi.',
  '「駅前のドラッグストアで買って来てくれる？」 → đi mua giấy vệ sinh. Vてくれる？ = nhờ (thân mật). お金を返す là việc của cấp trên.')
r('（2）アリさんがもらって来なければならないものは何ですか。', ['トイレットペーパー1こ', 'お金', 'レシート', 'ふくろ'], 3, 'y2_r9.jpg',
  '(Xem bản dịch câu trước.)',
  '「レシートをもらって来てね」. Vなければならない = phải làm V. Số lượng là 10こ chứ không phải 1こ; tiền sẽ được trả lại sau.')
r('（1）寝る前にいいことはどれですか。', ['スマホを見る', 'たくさん食べる', 'ぬるいお風呂に入る', 'コーヒーを飲む'], 3, 'y2_r11.jpg',
  '5 điểm để ngủ ngon: ① Mỗi ngày thức dậy cùng một giờ. ② 3 tiếng trước khi ngủ không ăn quá nhiều. ③ Trước khi ngủ tắm bồn nước ấm (38–40 độ). ④ Trước khi ngủ không xem điện thoại. ⑤ Sau chiều tối không uống cà phê.',
  'Mục ③: 「寝る前にぬるいお風呂に入る」. Các phương án khác đều là việc poster khuyên KHÔNG làm. ぬるい = âm ấm.')
r('（2）このポスターで言っていないことはどれですか。', ['夕方からコーヒーを飲まない', '毎日運動する', '毎日同じ時間に起きる', '寝る前にスマホを見ない'], 2, 'y2_r11.jpg',
  '(Xem bản dịch câu trước.)',
  'Câu hỏi tìm điều KHÔNG có trong poster (言っていない). 運動 (VẬN ĐỘNG) không được nhắc đến. 1 = mục ⑤, 3 = mục ①, 4 = mục ④.')

ex = dict(id='jft-y2', group='Đề thi thử JFT-Basic', title='Đề 26',
          sub='Có phần nghe · いろどり 初級1', time=60, tag='Đề mới chuẩn', qs=qs)
E = json.load(open(REPO + 'src/raw/jft_exams.json'))
E = [e for e in E if e['id'] != 'jft-y2']
for e in E:
    if e['id'].startswith('jft-g') or e['id'].startswith('jft-y'): e.pop('short', None)
    if e['id'] == 'jft-y1': e['tag'] = 'Đề mới chuẩn'
pos = max(i for i, e in enumerate(E) if e['id'] == 'jft-y1') + 1
E = E[:pos] + [ex] + E[pos:]
json.dump(E, open(REPO + 'src/raw/jft_exams.json', 'w'), ensure_ascii=False, indent=1)
print(len(qs), [sum(q['s'] == s for q in qs) for s in (V, K, L, R)])
