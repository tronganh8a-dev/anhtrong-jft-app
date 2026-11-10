import json, html, shutil, os, sys
sys.path.insert(0, '/home/claude/anhtrong-jft-app/src/jft')
from furi import furi
REPO = '/home/claude/anhtrong-jft-app/'
IMG = 'app/media/jft/img/'; AU = 'app/media/jft/au/'
for f in os.listdir('/tmp/yt3/img'): shutil.copy('/tmp/yt3/img/' + f, REPO + 'public/' + IMG + f)
for f in os.listdir('/tmp/yt3/au'): shutil.copy('/tmp/yt3/au/' + f, REPO + 'public/' + AU + f)

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
v(PIC, ['苦い', '甘い', '辛い', 'すっぱい'], 1,
  'Tranh: người nhăn mặt sau khi uống cà phê đen → đắng.',
  '苦い (KHỔ) にがい = đắng – vị của cà phê đen. 甘い (CAM) あまい = ngọt, 辛い (TÂN) からい = cay, すっぱい = chua. Chú ý 苦い (にがい, đắng) và 苦手 (にがて, không giỏi/không hợp) dùng cùng chữ 苦. いろどり 初級1 第12課.', ['y3_v1.jpg'])
v(PIC, ['雪が　降る', '桜の　花が　咲く', 'もみじが　きれい', 'セミが　鳴く'], 2,
  'Tranh: hàng cây hoa anh đào đang nở → mùa xuân.',
  '桜の花が咲く (ANH – HOA – TIẾU) = hoa anh đào nở, dấu hiệu mùa xuân. Mỗi mùa một hình ảnh: 雪が降る (TUYẾT – GIÁNG) = tuyết rơi (đông), もみじ = lá đỏ (thu), セミが鳴く (MINH) = ve kêu (hè). いろどり 初級1 第3課.', ['y3_v2.jpg'])
v(PIC, ['静か（な）', 'にぎやか（な）', '緑が　多い', '不便（な）'], 2,
  'Tranh: phố đông người, nhiều toà nhà, biển SALE → náo nhiệt.',
  'にぎやか（な）= náo nhiệt, đông vui; trái nghĩa 静か（な）(TĨNH) = yên tĩnh. 緑が多い (LỤC) = nhiều cây xanh, 不便 (BẤT TIỆN) = bất tiện. いろどり 初級1 第5課.', ['y3_v3.jpg'])
v('はしを（　　）、まっすぐ行ってください。', ['のって', 'まがって', 'おりて', 'わたって'], 4,
  'Hãy băng qua cầu rồi đi thẳng.',
  'はしを　わたる (橋を渡る – KIỀU, ĐỘ) = qua cầu. Trợ từ を chỉ nơi đi qua. のる = lên xe (〜に), おりる = xuống xe (〜を), まがる = rẽ (〜を/〜に) – không đi với はし. いろどり 初級1 第6課.')
v('あしたのまちあわせはえきの（　　）にしましょう。', ['はし', 'かど', 'かいさつ', 'しんごう'], 3,
  'Chỗ hẹn ngày mai lấy ở cửa soát vé của ga nhé.',
  'えきの　かいさつ (駅の改札 – CẢI TRÁT) = cửa soát vé của ga, chỗ hẹn gặp quen thuộc ở Nhật. はし = cầu, かど = góc phố, しんごう = đèn giao thông – không thuộc về ga. いろどり 初級1 第7課.')
v('パソコンがうごかないので、（　　）してみてください。', ['さいきどう', 'しゅうり', 'そうじ', 'けんがく'], 1,
  'Máy tính không chạy nên hãy thử khởi động lại xem.',
  'さいきどう (再起動 – TÁI KHỞI ĐỘNG) = khởi động lại. Vてみる = thử làm. しゅうり (修理) = sửa chữa – thường nhờ người khác, không "thử"; そうじ = dọn dẹp, けんがく = tham quan. いろどり 初級1 第13課.')
v('', ['まいび', 'まいじつ', 'まいにち', 'めいにち'], 3,
  'Mỗi ngày tôi học tiếng Nhật.',
  '毎日 (MỖI NHẬT) đọc là まいにち. 日 có nhiều cách đọc (ひ, にち, じつ, び) nhưng trong từ này là にち. めいにち sai âm 毎 (まい).',
  raw='<u>毎日</u>日本語を勉強しています。')
v('', ['べんい', 'へんり', 'びんり', 'べんり'], 4,
  'Thị trấn này nhiều cửa hàng nên tiện lợi.',
  '便利 (TIỆN LỢI) đọc là べんり. Các phương án sai lệch một âm: へんり (thiếu dấu đục), びんり (sai nguyên âm), べんい (sai り). Trái nghĩa: 不便 ふべん.',
  raw='この町は店が多くて<u>便利</u>です。')
v('', ['かいき', 'がいぎ', 'かいぎ', 'かいいぎ'], 3,
  'Nhờ anh chuẩn bị cuộc họp.',
  '会議 (HỘI NGHỊ) đọc là かいぎ = cuộc họp. 議 đọc ぎ (có dấu đục); 会 đọc かい (không đục). かいいぎ thừa い.',
  raw='<u>会議</u>の準備をお願いします。')
v('', ['在', '右', '石', '古'], 2,
  'Hãy rẽ phải ở góc phố tiếp theo.',
  'みぎ = 右 (HỮU). Chữ giống: 在 (TẠI), 石 (THẠCH – いし), 古 (CỔ – ふるい). Phân biệt 右 và 左 (TẢ – ひだり): 右 có 口 ở dưới, 左 có 工.',
  raw='つぎのかどを<u>みぎ</u>にまがってください。')
v('', ['店', '床', '庭', '広'], 1,
  'Thị trấn này nhiều cửa hàng nên tiện lợi.',
  'みせ = 店 (ĐIẾM). Các chữ cùng bộ 广: 床 (SÀNG – ゆか, sàn nhà), 庭 (ĐÌNH – にわ, sân vườn), 広 (QUẢNG – ひろい, rộng). Nhớ: 广 + 占 = 店.',
  raw='この町は<u>みせ</u>が多くてべんりです。')
v('', ['夘', '卵', '印', '卯'], 2,
  'Món ăn này có dùng trứng không?',
  'たまご = 卵 (NOÃN). 卵 có 2 dấu chấm bên trong. 卯 (MÃO) và 夘 không có chấm; 印 (ẤN – しるし) là chữ khác.',
  raw='このりょうりは<u>たまご</u>を使っていますか。')

# ---------- 会話と表現 ----------
def k(t, o, a, dich, gt):
    qs.append(Q(K, J(t), o, a, EX(o[a-1], dich, gt)))
k('山田：日本の生活にもう慣れましたか。\nロン：はい、（　　）。',
  ['おじゃまします', 'おだいじに', 'おまちどおさま', 'おかげさまで'], 4,
  'Yamada: Anh đã quen với cuộc sống ở Nhật chưa? / Long: Vâng, nhờ trời (nhờ mọi người) tôi quen rồi.',
  'Đáp lời hỏi thăm một cách lịch sự: はい、おかげさまで. おじゃまします (khi vào nhà người khác), おだいじに (chúc người ốm mau khoẻ), おまちどおさま (xin lỗi đã để chờ). いろどり 初級1 第1課.')
k('木村：日本語のほかに、何か習っていますか。\nニン：はい、（　　）。',
  ['ギターを習っています', 'ギターを習いましょう', 'ギターをください', 'ギターが上手でした'], 1,
  'Kimura: Ngoài tiếng Nhật, bạn có học gì không? / Ninh: Có, tôi đang học guitar.',
  'Câu hỏi 習っていますか (đang học) → trả lời cùng thể Vています: ギターを習っています. 習いましょう là rủ rê. 習う (TẬP) = học (từ người khác). いろどり 初級1 第2課.')
k('山本：だいぶ暖かく（　　）。\nリン：本当ですね。',
  ['きましたね', 'なりましたね', 'しましたね', 'ありましたね'], 2,
  'Yamamoto: Trời ấm lên nhiều rồi nhỉ. / Rin: Đúng thật.',
  'Diễn tả sự thay đổi: Aく＋なりました (暖かい → 暖かくなりました). だいぶ = khá nhiều. 暖かい (NOÃN) = ấm áp. いろどり 初級1 第4課.')
k('ミン：1つ目の信号を左ですね。\n通行人：いえ、1つ目（　　）、2つ目です。',
  ['でも', 'じゃなくて', 'だから', 'だけど'], 2,
  'Minh: Đèn giao thông thứ nhất rẽ trái nhỉ. / Người qua đường: Không, không phải cái thứ nhất mà là cái thứ hai.',
  'Sửa lại thông tin: A じゃなくて B = không phải A mà là B. でも, だけど = nhưng; だから = vì vậy. いろどり 初級1 第6課.')
k('鈴木：ポートタワー、もう登りましたか。\nアナ：（　　）。\n鈴木：じゃあ、今度行きませんか。',
  ['いいえ、もう登りました', 'はい、登りません', 'はい、まだです', 'いいえ、まだです'], 4,
  'Suzuki: Chị đã lên Port Tower chưa? / Ana: Chưa, tôi chưa lên. / Suzuki: Vậy lần tới cùng đi nhé?',
  'Hỏi もう〜ましたか: nếu chưa làm thì đáp いいえ、まだです. Lời mời 今度行きませんか ở câu sau cho biết Ana chưa đi. Không ghép はい với まだ. 登る (ĐĂNG) = leo lên. いろどり 初級1 第8課.')
k('アリ：すみません。この漢字の読み方を（　　）。\n西村：これですか？「いとう」です。',
  ['教えてもらえませんか', '教えてあげませんか', '教えていますか', '教えましょうか'], 1,
  'Ali: Xin lỗi, chị chỉ cho tôi cách đọc chữ Hán này được không? / Nishimura: Chữ này à? Đọc là "Itō".',
  'Nhờ người khác: Vて　もらえませんか. 教えましょうか là đề nghị chỉ giúp người khác (ngược vai). 読み方 (ĐỘC PHƯƠNG) = cách đọc. いろどり 初級1 第9課.')
k('マルコ：飲み物はビールとワインでいいですか。\nノイ：あのう、すみません。私はお酒が（　　）……。',
  ['好きですから', '飲みますから', 'いいですから', 'だめですから'], 4,
  'Marco: Đồ uống là bia và rượu vang được chứ? / Noi: À, xin lỗi, tôi không uống được rượu nên…',
  'Từ chối khéo: あのう、すみません + 〜がだめですから…… (bỏ lửng câu). Cách nói tránh nói thẳng "không". いろどり 初級1 第11課.')
k('田村：それ、何ですか。\nフエン：チョコレートバニラクリームラテです。\n田村：へー、（　　）。',
  ['甘いそうですね', '甘そうですね', '甘くないですね', '甘かったですね'], 2,
  'Tamura: Cái đó là gì vậy? / Huyền: Là latte kem vani sô-cô-la. / Tamura: Ồ, trông có vẻ ngọt nhỉ.',
  'Nhận xét qua vẻ bề ngoài: Aい bỏ い + そうです (甘い → 甘そう). 甘いそうです là "nghe nói ngọt" (truyền đạt) – không hợp vì Tamura đang nhìn thấy. Tamura chưa uống nên 甘かった sai. いろどり 初級1 第12課.')
k('王：昨日は休んで、（　　）。\n田村：いえ。もうだいじょうぶですか。',
  ['ありがとうございました', 'おめでとうございました', 'いただきました', 'すみませんでした'], 4,
  'Vương: Hôm qua tôi đã nghỉ, xin lỗi anh. / Tamura: Không sao. Anh khoẻ hẳn chưa?',
  'Xin lỗi vì đã nghỉ làm: 休んで、すみませんでした (Vて = lý do). Đáp いえ (không có gì) xác nhận đây là lời xin lỗi. いろどり 初級1 第14課.')
k('薬剤師：これは痛み止めです。痛くて（　　）ときに飲んでください。\n郭：はい。',
  ['がまんできない', '元気な', '眠い', 'おいしい'], 1,
  'Dược sĩ: Đây là thuốc giảm đau. Hãy uống khi đau quá không chịu được. / Quách: Vâng.',
  'がまんできない = không chịu đựng được. 痛くて + がまんできない (vì đau nên không chịu nổi) → lúc uống thuốc giảm đau. 痛み止め (THỐNG – CHỈ) = thuốc giảm đau. いろどり 初級1 第15課.')
k('酒井：健康のために、何か気をつけていますか？\nホセ：はい。お酒を飲み（　　）ようにしています。',
  ['すぎた', 'すぎて', 'すぎる', 'すぎない'], 4,
  'Sakai: Anh có chú ý gì vì sức khoẻ không? / José: Có. Tôi cố gắng không uống rượu quá nhiều.',
  'Vます bỏ ます + すぎる = làm quá mức. Cố gắng tránh: 〜ないようにしています → 飲みすぎないようにしています. 健康 (KIỆN KHANG) = sức khoẻ. いろどり 初級1 第16課.')
k('リン：かさを持って行ったほうがいいですか。\n山本：ええ、天気予報で見ましたが、午後から雨が（　　）。',
  ['降るそうですよ', '降ってください', '降りましょう', '降りたいです'], 1,
  'Rin: Có nên mang ô theo không? / Yamamoto: Có, tôi xem dự báo thời tiết thấy nói chiều nay trời mưa đấy.',
  'Truyền đạt thông tin nghe/xem được: thể thường + そうです (降る → 降るそうです). 天気予報で見ました là nguồn tin. Khác với 甘そう (trông có vẻ) ở câu 8. いろどり 初級1 第4課.')

# ---------- 聴解 ----------
def l(n, q, vi, o, a, script, dich, gt, oimg=None):
    t = f'<span class="jp">{J(q)}</span><br><span class="vi-q">{html.escape(vi)}</span>'
    ans = o[a-1] if o[a-1] else f'phương án {a} (tranh)'
    qs.append(Q(L, t, o, a, EX(ans, dich, gt, script), au=AU + f'y3_L{n:02d}.mp3', oimg=oimg))
l(1, 'この人は日本の生活に慣れましたか。', 'Người này đã quen với cuộc sống ở Nhật chưa?',
  ['まだあまり慣れていない', 'なんとか慣れた', '1年前に慣れた', 'もう慣れた'], 1,
  'A：日本に来て、どのぐらいになりますか？\nB：私は、先月、来ました。\nA：そうですか。少し慣れましたか？\nB：まだ、ちょっと……。',
  'A: Anh đến Nhật được bao lâu rồi? / B: Tôi đến vào tháng trước. / A: Vậy à. Đã quen một chút chưa? / B: Vẫn còn hơi…',
  'まだ、ちょっと…… là cách nói bỏ lửng = chưa quen lắm. 先月 (tháng trước) mới đến nên chưa thể 1年前に慣れた. 慣れる (QUÁN) = quen.')
l(2, 'バヤルさんの国の冬は何度ぐらいになりますか。', 'Mùa đông ở nước của Bayar lạnh khoảng bao nhiêu độ?',
  ['マイナス40度', '4度', 'マイナス4度', '40度'], 1,
  'A：バヤルさんの国には、どんな季節がありますか？\nB：日本と同じです。四季があります。でも、夏はとても暑いです。冬はとても寒いです。\nA：そうですか。\nB：夏は40度、冬はマイナス40度になります。\nA：へー、そうなんですか。',
  'A: Ở nước anh Bayar có những mùa nào? / B: Giống Nhật, có bốn mùa. Nhưng mùa hè rất nóng, mùa đông rất lạnh. / A: Vậy à. / B: Mùa hè 40 độ, mùa đông âm 40 độ. / A: Ồ, vậy sao.',
  'Câu hỏi về 冬 (mùa đông): 冬はマイナス40度. 40度 là mùa hè. マイナス = âm (độ dưới 0). 四季 (TỨ QUÝ) = bốn mùa.')
l(3, '「マリンモール」は日曜日どうですか。', '"Marine Mall" vào Chủ nhật thế nào?',
  ['静か', '人が多い', '安い', '休み'], 2,
  'A：休みの日にどこか行きたいんですが、いいところがありますか？\nB：そうだなあ。この町の人は「マリンモール」によく行くよ。\nA：え、それは何ですか？\nB：ショッピングモール。いろんな店とか、レストランとか、スーパーとかがあるところ。おもしろいけど、日曜日は人が多いかな。\nA：そうですか。一度行ってみます。',
  'A: Ngày nghỉ tôi muốn đi đâu đó, có chỗ nào hay không? / B: Để xem. Người ở thị trấn này hay đi "Marine Mall". / A: Đó là gì vậy? / B: Trung tâm mua sắm, có nhiều cửa hàng, nhà hàng, siêu thị. Thú vị, nhưng Chủ nhật thì chắc đông người. / A: Vậy à. Tôi sẽ đi thử một lần.',
  'Sau けど là điểm cần chú ý: 日曜日は人が多いかな. 〜かな = chắc là (phỏng đoán nhẹ). 一度行ってみます = sẽ đi thử một lần.')
l(4, '何時にどこで会いますか。', 'Gặp nhau lúc mấy giờ, ở đâu?',
  ['8時に駅の改札', '6時半に駅の改札', '6時に駅の改札', '6時半に会社の前'], 2,
  'A：明日の待ち合わせは、何時にどこにしますか？\nB：じゃあ、6時半に、駅の改札でいい？\nA：はい。6時半に駅ですね。\nB：じゃあ、また。',
  'A: Ngày mai hẹn mấy giờ, ở đâu? / B: Vậy 6 giờ rưỡi ở cửa soát vé ga được không? / A: Vâng. 6 giờ rưỡi ở ga nhé. / B: Hẹn gặp lại.',
  '6時半 = 6 giờ rưỡi (半 – BÁN = một nửa). 改札 (CẢI TRÁT) = cửa soát vé. A nhắc lại 6時半に駅ですね để xác nhận.')
l(5, '今度は何をしますか。', 'Lần tới sẽ làm gì?',
  ['プロレスを見に行く', '同じ映画を見る', 'ホラー映画を見に行く', '動物園に行く'], 3,
  'A：映画、よかったですね。\nB：感動しました。本当にすばらしかったです。\nA：じゃあ、また行きましょう。\nB：今度は、ホラー映画を見に行きましょう。\nA：えー。',
  'A: Bộ phim hay nhỉ. / B: Tôi xúc động lắm. Thật sự tuyệt vời. / A: Vậy lại đi tiếp nhé. / B: Lần tới đi xem phim kinh dị nhé. / A: Hả…',
  '今度は (lần tới) + ホラー映画を見に行きましょう. 〜に行く = đi để làm gì. えー thể hiện A hơi ngại nhưng kế hoạch vẫn là phim kinh dị. 感動 (CẢM ĐỘNG) = xúc động.')
l(6, 'この人は何をお願いしましたか。', 'Người này đã nhờ việc gì?',
  ['書類を書いてほしい', '書類をコピーしてほしい', '書類の書き方をもう一度説明してほしい', '漢字の読み方を教えてほしい'], 3,
  'A：すみません。この書類の書き方がよくわかりません。もう一度説明してもらえませんか？\nB：えーと、これはですねえ……。',
  'A: Xin lỗi, tôi không hiểu rõ cách điền giấy tờ này. Anh giải thích lại một lần nữa được không? / B: À, cái này thì…',
  'もう一度説明してもらえませんか = nhờ giải thích lại. Không nhờ viết hộ (書いて). 書類 (THƯ LOẠI) = giấy tờ, 書き方 = cách viết/điền, 説明 (THUYẾT MINH) = giải thích.')
l(7, 'この人は料理を食べますか。どうしてですか。', 'Người này có ăn món đó không? Vì sao?',
  ['食べる。卵が好きだから', '食べる。卵を使っていないから', '食べない。おなかがいっぱいだから', '食べない。卵を使っているから'], 2,
  'A：さあ、どうぞ。\nB：あのう、この料理、卵を使ってますか？\nA：卵？これは使ってませんよ。\nB：あ、じゃあ、だいじょうぶです。いただきます！',
  'A: Nào, mời anh. / B: À, món này có dùng trứng không ạ? / A: Trứng à? Món này không dùng đâu. / B: À, vậy thì không sao. Tôi xin phép ăn!',
  'B hỏi về trứng (có thể vì không ăn được trứng). A trả lời 使ってません → B nói いただきます (sẽ ăn). Vì không có trứng nên ăn → 2.')
l(8, '梅干しはどんな味ですか。', 'Mơ muối có vị như thế nào?',
  ['', '', '', ''], 3,
  'A：それ、何ですか？\nB：これ？梅干し。食べてみる？\nA：はい。\nB：どう？\nA：う、……すみません。すっぱくて、ちょっと苦手です。\nB：あ、そう。',
  'A: Cái đó là gì vậy? / B: Cái này à? Mơ muối. Ăn thử không? / A: Vâng. / B: Thế nào? / A: Ư… xin lỗi. Chua quá, tôi hơi không ăn được. / B: À, vậy à.',
  'すっぱい = chua → tranh 3 (quả chanh). Tranh 1 辛い (cay – ớt), tranh 2 苦い (đắng – cà phê), tranh 4 甘い (ngọt – bánh kem). 梅干し (MAI CAN) = mơ muối.',
  oimg=[f'y3_l8_{i}.jpg' for i in range(1, 5)])
l(9, 'アニサさんはどうして遅れますか。', 'Vì sao Anisa đến muộn?',
  ['病院に行くから', '熱があるから', '家に財布を忘れたから', '道が混んでいるから'], 3,
  '会社の人：はい、北浦和フーズです。\nアニサ：もしもし、あのう、アニサです。\n会社の人：ああ、アニサさん。\nアニサ：すみません。家に財布を忘れました。これから取りに帰ります。それで、少し遅れます。\n会社の人：ああ、わかりました。\n（あとで）\nアニサ：おはようございます。遅くなって、申し訳ありません。',
  'Người công ty: Vâng, Kita-Urawa Foods xin nghe. / Anisa: Alo, à, tôi là Anisa. / Người công ty: À, chị Anisa. / Anisa: Xin lỗi, tôi để quên ví ở nhà. Bây giờ tôi về lấy. Vì vậy sẽ đến muộn một chút. / Người công ty: À, tôi hiểu rồi. (Sau đó) / Anisa: Chào buổi sáng. Tôi xin lỗi vì đã đến muộn.',
  'Lý do ở câu 家に財布を忘れました (quên ví ở nhà) → それで (vì vậy) 少し遅れます. 財布 (TÀI BỐ) = ví, 遅れる (TRÌ) = muộn, 申し訳ありません = xin lỗi (trang trọng).')
l(10, 'この人はどうしましたか。', 'Người này bị sao?',
  ['道で転んで、足をくじいた', '目がかゆい', '熱がある', '頭をぶつけた'], 1,
  'A：今日はどうしましたか？\nB：昨日、道で転んで、足をくじいたんです。\nA：ちょっと触りますよ。ここをこうすると、痛いですか？\nB：痛い！\nA：ああ、じゃあ、レントゲン撮ってみましょうか。',
  'A: Hôm nay anh bị sao? / B: Hôm qua tôi ngã ngoài đường, bị trẹo chân. / A: Tôi chạm vào một chút nhé. Làm thế này có đau không? / B: Đau! / A: À, vậy chụp X-quang thử xem nhé.',
  '転ぶ (CHUYỂN) = ngã, 足をくじく = trẹo chân. 頭をぶつける = va đầu – không có trong bài. レントゲン = chụp X-quang.')
l(11, 'この人はどんな運動をしていますか。', 'Người này đang tập môn thể thao nào?',
  ['水泳', 'ジョギングとヨガ', 'ジムとウォーキング', 'サッカー'], 2,
  'A：最近、何か運動してますか？\nB：そうですねえ、ジョギングしたり、ときどき家でヨガをしたりしてます。\nA：へー、ヨガ。\nB：ええ。寝る前にヨガをすると、よく眠れますよ。\nA：そうなんですか。',
  'A: Gần đây chị có tập môn gì không? / B: Ừm, tôi chạy bộ, thỉnh thoảng tập yoga ở nhà. / A: Ồ, yoga à. / B: Vâng. Tập yoga trước khi ngủ thì ngủ ngon lắm. / A: Vậy sao.',
  'Vたり、Vたりする = liệt kê vài việc tiêu biểu: ジョギングしたり、ヨガをしたり. 水泳 (THUỶ VỊNH) = bơi. 運動 (VẬN ĐỘNG) = vận động.')
l(12, 'かばんはだれが作りましたか。', 'Ai đã làm chiếc túi?',
  ['お兄さん', 'ミャンマーのお母さん', '自分', '友だち'], 2,
  'A：そのかばん、いいね。\nB：そうですか？ありがとうございます。\nA：日本で買ったの？\nB：これは、ミャンマーの母が作ったんです。\nA：お母さんが作ったの？すごいね。',
  'A: Cái túi đó đẹp nhỉ. / B: Vậy ạ? Cảm ơn chị. / A: Mua ở Nhật à? / B: Cái này mẹ tôi ở Myanmar làm đấy ạ. / A: Mẹ em làm à? Giỏi quá.',
  'Nói về mẹ mình: 母 (はは); nói về mẹ người khác/hỏi: お母さん. B nói ミャンマーの母が作った → đáp án 2. 日本で買った là câu hỏi của A, không phải sự thật.')

# ---------- 読解 ----------
def r(q, o, a, img, dich, gt):
    qs.append(Q(R, J(q), o, a, EX(o[a-1], dich, gt), [img]))
r('（1）ソカさんはどんな仕事をしていますか。', ['料理', '歌手', '日本語の先生', '介護'], 4, 'y3_r1.jpg',
  'Thẻ giới thiệu: Tên: Soka. Nước: Campuchia (Phnôm Pênh). Đến Nhật: tháng 4 năm ngoái. Công việc: điều dưỡng (viện dưỡng lão). Sở thích: hát, nấu ăn. Đôi lời: Muốn thuộc thật nhiều bài hát Nhật!',
  'Dòng 仕事: 介護（老人ホーム）. 料理 và 歌 là sở thích (すきなこと), không phải công việc. 介護 (GIỚI HỘ) = điều dưỡng, 老人ホーム = viện dưỡng lão.')
r('（2）ソカさんがしたいことは何ですか。', ['老人ホームを作る', '日本の歌をたくさんおぼえる', '料理を習う', 'プノンペンに帰る'], 2, 'y3_r1.jpg',
  '(Xem bản dịch câu trước.)',
  'Dòng ひとこと: 「日本の歌をたくさんおぼえたいです」. Vたい = muốn làm V. おぼえる (覚える) = nhớ, thuộc.')
r('（1）リンさんはかさをどうしますか。', ['受付のかさを借りる', 'コンビニで買う', '山本さんのかさを借りる', 'かさをささないで帰る'], 1, 'y3_r3.jpg',
  'Yamamoto: Bên ngoài mưa to lắm đấy! / Rin: Ơ, thật ạ? Tôi không mang ô… / Yamamoto: Ở quầy lễ tân có ô đấy. Ô của công ty ai cũng dùng được. / Yamamoto: Ngày mai trả lại ở quầy lễ tân nhé. / Rin: Cảm ơn anh!',
  '「受付にかさがありますよ。会社のかさはだれでも使えます」 → mượn ô ở quầy lễ tân. Ô là của công ty, không phải của Yamamoto. 受付 (THỤ PHÓ) = quầy lễ tân.')
r('（2）かさはいつ返しますか。', ['あした', '今日の夜', '来週', '雨がやんだとき'], 1, 'y3_r3.jpg',
  '(Xem bản dịch câu trước.)',
  '「あした受付に返してくださいね」. 返す (PHẢN) = trả lại.')
r('（1）いちばん早く来る人はだれですか。', ['ロンさん', 'アナさん', 'ソカさん', 'ミンさん'], 1, 'y3_r5.jpg',
  'Lịch nhân viên Lễ hội quốc tế (ngày 10): Minh – quầy tiếp đón 9:30–12:00; Ana – quầy đồ ăn 11:00–15:00; Long – chuẩn bị sân khấu 8:30–10:00; Soka – dọn dẹp 15:00–17:00. ※ Sự kiện từ 10 giờ đến 15 giờ. Nhân viên hãy đến hội trường 15 phút trước giờ bắt đầu công việc.',
  'Giờ bắt đầu sớm nhất là 8:30 của ロン. Chú ý: giờ sự kiện (10時) khác giờ làm của từng người.')
r('（2）アナさんは何時にホールに来ますか。', ['10時45分', '11時15分', '11時', '10時'], 1, 'y3_r5.jpg',
  '(Xem bản dịch câu trước.)',
  'アナ bắt đầu 11:00; quy định đến 15分前 (15 phút trước) → 10:45. 11時 là giờ bắt đầu làm, không phải giờ đến.')
r('（1）ノイさんは何を持って行きますか。', ['飲み物', 'バナナ', 'おにぎり', '肉と野菜'], 2, 'y3_r7.jpg',
  'Người gửi: Hasegawa | Tiêu đề: BBQ tuần sau. Mọi người, về việc chuẩn bị BBQ thứ Bảy tuần sau: Thịt và rau – Dương mua mang đến. Đồ uống – đã nhờ Marco: bia và trà. Cơm nắm – tôi (Hasegawa) làm mang đến. Tráng miệng – Noi mang chuối đến. Cốc và đĩa có ở khu BBQ nên không cần mang. Tập trung 10 giờ ở lối vào công viên Midori. Trời mưa thì huỷ. Tối hôm trước 8 giờ sẽ báo qua email.',
  'Dòng デザート：ノイさんがバナナを持って来ます. 飲み物 = Marco, おにぎり = Hasegawa, 肉と野菜 = Dương.')
r('（2）持って行かなくてもいいものは何ですか。', ['おにぎり', 'お茶', 'コップやお皿', '肉'], 3, 'y3_r7.jpg',
  '(Xem bản dịch câu trước.)',
  'Vなくてもいい = không cần làm V. 「コップやお皿はバーベキュー場にありますから、持って来なくてもだいじょうぶです」.')
r('（1）名前の横には何をしますか。', ['休む日を書く', 'ハンコをおす', 'チームの名前を書く', '理由を書く'], 2, 'y3_r9.jpg',
  'Cách viết đơn xin nghỉ: ① Ô "Bộ phận" trên cùng: viết tên nhóm. ② Ô "Họ tên" bên dưới: viết tên, đóng dấu bên cạnh tên. ③ Ô "Thời gian": viết ngày nghỉ. ④ Ô "Lý do": viết lý do nghỉ. ⑤ Nộp cho anh Tanaka bộ phận tổng vụ trước ngày nghỉ 1 tuần. Khi đột ngột nghỉ vì ốm, hãy gọi điện báo trước 8 giờ sáng.',
  'Mục ②: 「名前の横にハンコをおします」. ハンコをおす = đóng con dấu. 横 (HOÀNH) = bên cạnh.')
r('（2）急に病気で休むとき、どうしますか。', ['朝8時までに電話する', '次の日に休暇届を出す', '1週間前に休暇届を出す', '田中さんにメールする'], 1, 'y3_r9.jpg',
  '(Xem bản dịch câu trước.)',
  'Dòng cuối: 「急に病気で休むときは、朝8時までに電話で連絡してください」. 1週間前 là quy định cho nghỉ có kế hoạch. 急に (CẤP) = đột ngột, 休暇届 (HƯU HẠ GIỚI) = đơn xin nghỉ.')
r('（1）リンさんは毎朝何をしていますか。', ['ご飯を食べない', '30分歩く', 'ヨガをする', 'ジムに行く'], 2, 'y3_r11.jpg',
  'José: Gần đây người tôi nặng nề… Bạn có tập gì không? / Rin: Mình đi gym 2 lần một tuần, và mỗi sáng đi bộ 30 phút. / Rin: Với lại buổi tối cố không ăn quá nhiều. / José: Giỏi quá. Mình đi gym cùng được không? / Rin: Tất nhiên! Thứ Bảy này đi nhé.',
  '「毎朝30分歩いてるよ」. ジム là 週に2回 (2 lần/tuần), không phải mỗi sáng. Trong bài không có ヨガ.')
r('（2）二人は土曜日に何をしますか。', ['いっしょにジムに行く', 'ご飯を食べに行く', 'いっしょに歩く', '病院に行く'], 1, 'y3_r11.jpg',
  '(Xem bản dịch câu trước.)',
  'ホセ hỏi いっしょにジムに行ってもいい？ → リン: 今度の土曜日、行こう. Vてもいい？ = có được làm V không; 行こう = thể ý chí (rủ: cùng đi).')

ex = dict(id='jft-y3', group='Đề thi thử JFT-Basic', title='Đề 27',
          sub='Có phần nghe · いろどり 初級1', time=60, tag='Đề mới chuẩn', qs=qs)
E = json.load(open(REPO + 'src/raw/jft_exams.json'))
E = [e for e in E if e['id'] != 'jft-y3']
pos = max(i for i, e in enumerate(E) if e['id'] == 'jft-y2') + 1
E = E[:pos] + [ex] + E[pos:]
json.dump(E, open(REPO + 'src/raw/jft_exams.json', 'w'), ensure_ascii=False, indent=1)
print(len(qs), [sum(q['s'] == s for q in qs) for s in (V, K, L, R)])
