# Đề 30 (jft-y5) — từ video "JFT Mock Test #10 · いろどり 初級1 第10回" anh gửi 21/11/2026 (48 câu: 12 từ vựng · 12 hội thoại · 12 nghe · 12 đọc).
# 21/11 anh chốt: bản chính đổi chỗ với Đề 4 (đề mới hiện là "Đề 4", Đề 4 cũ jft-f4 thành "Đề 30" — làm trong build_data.py);
# bản dùng thử: đề mới nằm trong nhóm Làm thử miễn phí, ghi "Đề 3" (build_demo.py).
# Đáp án theo khung "正解 Answer" cuối mỗi câu của video; script nghe = lời gốc いろどり 初級1 (đối chiếu chữ trong video + nhận dạng giọng nói).
# Ảnh: tranh từ vựng + tranh nghe cắt từ khung hình video (phóng to ESRGAN), bài đọc dựng lại bằng make5.js.
# Cần /tmp/y5/img, /tmp/y5/au. Chạy: python3 src/jft/youtube/build_y5.py → python3 src/build_data.py
import json, html, shutil, os, sys, re
sys.path.insert(0, '/home/claude/anhtrong-jft-app/src/jft')
from furi import furi
REPO = '/home/claude/anhtrong-jft-app/'
IMG = 'app/media/jft/img/'; AU = 'app/media/jft/au/'
for f in os.listdir('/tmp/y5/img'):
    if f.endswith('.jpg'): shutil.copy('/tmp/y5/img/' + f, REPO + 'public/' + IMG + f)
for f in os.listdir('/tmp/y5/au'): shutil.copy('/tmp/y5/au/' + f, REPO + 'public/' + AU + f)

J = lambda t, fu=True: (furi(html.escape(t)) if fu else html.escape(t)).replace('\n', '<br>')
def EX(ans, dich, gt, script=None, fu=True):
    vi = bool(re.search(r'[A-Za-zÀ-ỹ]', ans))
    s = '<div class="ans">Đáp án đúng: ' + (f'<span>{html.escape(ans)}</span>' if vi else f'<span class="jp">{J(ans, fu)}</span>') + '</div>'
    if script: s += f'<span class="lb">SCRIPT</span><div class="jp">{J(script)}</div>'
    s += f'<span class="lb">DỊCH</span><div>{J(dich, False)}</div><span class="lb">GIẢI THÍCH</span><div>{J(gt, False)}</div>'
    return s
def Q(s, t, o, a, ex, imgs=(), au=None, oimg=None, fu_opt=True):
    oo = [{'t': J(x, fu_opt) if x else ''} for x in o]
    if oimg:
        for d, im in zip(oo, oimg): d['img'] = IMG + im
    return dict(s=s, ins='', gset=None, gimg=None, gau=None, t=t, imgs=[IMG + i for i in imgs],
                img=None, au=au, o=oo, a=[a - 1], ex=ex)
def U(before, word, after=''):   # từ gạch chân: furigana cho phần còn lại, KHÔNG cho từ được hỏi
    return J(before) + '<u>' + html.escape(word) + '</u>' + J(after)

V = '文字と語彙'; K = '会話と表現'; L = '聴解'; R = '読解'
PIC = '絵を見て、正しいことばを選んでください。'
qs = []
def v(t, o, a, dich, gt, imgs=(), raw=None, fu_opt=True):
    qs.append(Q(V, raw if raw else J(t), o, a, EX(o[a-1], dich, gt, fu=fu_opt), imgs, fu_opt=fu_opt))

# ---------- 文字と語彙 ----------
v(PIC, ['暖かい', '暑い', 'すずしい', '寒い'], 4,
  'Tranh: người đội mũ len, quàng khăn, ôm người run cầm cập → lạnh.',
  '寒い (HÀN) さむい = lạnh (thời tiết). 暖かい (NOÃN) あたたかい = ấm áp, 暑い (THỬ) あつい = nóng, すずしい = mát mẻ. Bốn tính từ thời tiết hay đi theo mùa: xuân 暖かい, hè 暑い, thu すずしい, đông 寒い. いろどり 初級1 第3課.', ['y5_v1.jpg'])
v(PIC, ['コンサート', 'プロレス', '野球', '映画'], 2,
  'Tranh: hai đô vật trên sàn đấu có dây, khán giả hò reo → đấu vật.',
  'プロレス = đấu vật chuyên nghiệp (võ đài có dây quây). コンサート = buổi hoà nhạc, 野球 (DÃ CẦU) やきゅう = bóng chày, 映画 (ÁNH HOẠ) えいが = phim. いろどり 初級1 第8課 (sở thích, giải trí).', ['y5_v2.jpg'])
v(PIC, ['桜の　花が　咲く', '雪が　降る', 'セミが　鳴く', 'もみじが　きれい'], 4,
  'Tranh: lá đỏ, lá vàng trên núi → mùa thu.',
  'もみじがきれい = lá đỏ đẹp → mùa thu. 桜の花が咲く (ANH – HOA – TIẾU) = hoa anh đào nở (xuân), 雪が降る (TUYẾT – GIÁNG) = tuyết rơi (đông), セミが鳴く (MINH) = ve kêu (hè). いろどり 初級1 第3課.', ['y5_v3.jpg'])
v('きのうはかぜがつよく（　　）、たいへんでした。', ['ふいて', 'なって', 'ふって', 'さいて'], 1,
  'Hôm qua gió thổi mạnh, vất vả lắm.',
  'かぜがふく (風が吹く – PHONG, XUY) = gió thổi; thể て là ふいて. ふって (降る) dùng cho mưa, tuyết: 雨がふる. さいて (咲く) dùng cho hoa. なって (なる) = trở nên, không đi với かぜがつよく. いろどり 初級1 第4課.', fu_opt=False)
v('バーベキューの（　　）はどうしますか。', ['じゅんび', 'よやく', 'しゅくだい', 'せつめい'], 1,
  'Việc chuẩn bị cho tiệc nướng thì làm thế nào?',
  'じゅんび (準備 – CHUẨN BỊ) = sự chuẩn bị: mua thịt, đồ uống… cho tiệc nướng. よやく (予約 – DỰ ƯỚC) = đặt chỗ, しゅくだい (宿題 – TÚC ĐỀ) = bài tập về nhà, せつめい (説明 – THUYẾT MINH) = giải thích. いろどり 初級1 第11課.', fu_opt=False)
v('だんだん日本のせいかつに（　　）きました。', ['つかれて', 'すんで', 'なれて', 'おぼえて'], 3,
  'Dần dần tôi đã quen với cuộc sống ở Nhật.',
  '〜になれる (慣れる – QUÁN) = quen với ~; だんだん〜てきました = dần dần đã ~. つかれる = mệt, すむ = sống (ở đâu: 〜にすむ, không đi với せいかつ), おぼえる = nhớ, học thuộc. いろどり 初級1 第1課.', fu_opt=False)
v('', ['みぎ', 'みき', 'ひだり', 'ひたり'], 1,
  'Hãy rẽ phải ở góc phố tiếp theo.',
  '右 (HỮU) đọc là みぎ = bên phải. ひだり là 左 (TẢ) = bên trái. みき, ひたり là cách đọc sai (thiếu dấu đục). Phân biệt chữ: 右 có 口 bên dưới, 左 có 工.',
  raw=U('つぎのかどを', '右', 'にまがってください。'), fu_opt=False)
v('', ['りょうり', 'りょうい', 'りよおり', 'りょり'], 1,
  'Tôi muốn tham gia lớp học nấu ăn.',
  '料理 (LIỆU LÍ) đọc là りょうり = món ăn, nấu ăn. Chú ý りょ là âm ghép (ょ viết nhỏ) và kéo dài う: りょう・り. Các phương án khác thiếu âm dài hoặc sai âm.',
  raw=U('', '料理', '教室に参加したいです。'), fu_opt=False)
v('', ['けこん', 'けっこう', 'げっこん', 'けっこん'], 4,
  'Chúc mừng anh/chị kết hôn.',
  '結婚 (KẾT HÔN) đọc là けっこん, có âm ngắt っ. けっこう (結構) là từ khác = khá, được rồi. けこん thiếu っ, げっこん sai dấu đục.',
  raw=U('ご', '結婚', 'おめでとうございます。'), fu_opt=False)
v('', ['北', '此', '比', '化'], 1,
  'Tôi đang đợi ở cửa Bắc của ga.',
  'きた = 北 (BẮC); 北口 (きたぐち) = cửa Bắc. Các chữ trông giống: 此 (THỬ), 比 (TỈ – くらべる), 化 (HOÁ). Bốn hướng: 東 ひがし, 西 にし, 南 みなみ, 北 きた.',
  raw=J('えきの') + '<u>きた</u>' + J('口でまっています。'), fu_opt=False)
v('', ['安', '案', '女', '宏'], 1,
  'Mì ramen của quán này rẻ mà ngon.',
  'やすい = 安い (AN) = rẻ; やすくて = thể て của tính từ い để nối câu. 案 (ÁN – kế hoạch) có thêm 木 bên dưới, 女 (NỮ) = phụ nữ, 宏 (HOẰNG) không liên quan. Chữ 安 = mái nhà 宀 + 女.',
  raw=J('このお店のラーメンは') + '<u>やす</u>' + J('くておいしいです。'), fu_opt=False)
v('', ['誕生日', '誕性日', '誕星日', '延生日'], 1,
  'Vào ngày sinh nhật, tôi được bạn tặng một chiếc cốc.',
  'たんじょうび = 誕生日 (ĐẢN SINH NHẬT). Phương án sai thay một chữ: 性 (TÍNH), 星 (TINH – ほし), 延 (DIÊN) trông giống 誕 nhưng thiếu bộ 言. 生 (SINH) trong 誕生日 đọc じょう.',
  raw='<u>たんじょうび</u>' + J('に友だちにマグカップをもらいました。'), fu_opt=False)

# ---------- 会話と表現 ----------
def k(t, o, a, dich, gt):
    qs.append(Q(K, J(t), o, a, EX(o[a-1], dich, gt)))
k('木村：休みの日は何をしていますか。\nニン：たいてい、うちで映画を（　　）、音楽を聞いたりしています。',
  ['見ると', '見て', '見たり', '見るので'], 3,
  'Kimura: Ngày nghỉ chị thường làm gì? / Ninh: Thường thì tôi ở nhà xem phim, nghe nhạc…',
  'Mẫu Vたり、Vたりする = làm A, làm B… (liệt kê vài việc tiêu biểu). Vế sau có 聞いたりしています nên vế trước cũng phải là 見たり. 見て chỉ nối hành động theo thứ tự, 見ると = hễ xem thì, 見るので = vì xem. いろどり 初級1 第2課.')
k('山本：おはようございます。今日はいい天気ですね。\nリン：（　　）。',
  ['どういたしまして', 'どうですか', 'そうですね', 'そうですか'], 3,
  'Yamamoto: Chào buổi sáng. Hôm nay trời đẹp nhỉ. / Linh: Đúng vậy nhỉ.',
  'Người kia nói 〜ですね để tìm sự đồng tình → đáp そうですね (đúng thế nhỉ). そうですか = vậy à (khi nghe thông tin mới), どういたしまして = không có gì (đáp lời cảm ơn), どうですか = thế nào. いろどり 初級1 第4課.')
k('近所の人：この町はどうですか。\nリン：都会ですね。人も店も多くて、（　　）。',
  ['静かです', '不便です', 'さびしいです', 'にぎやかです'], 4,
  'Hàng xóm: Thị trấn này thế nào? / Linh: Đúng là thành phố nhỉ. Người cũng đông, cửa hàng cũng nhiều, náo nhiệt quá.',
  '人も店も多くて → にぎやか (náo nhiệt). Trái nghĩa: 静か (TĨNH) しずか = yên tĩnh, さびしい = vắng vẻ, buồn. 不便 (BẤT TIỆN) ふべん = bất tiện – ngược ý với "nhiều cửa hàng". いろどり 初級1 第5課.')
k('担当者：イベントは17時に始まりますが、スタッフは30分（　　）来てください。\nリン：じゃあ、4時半ですね。',
  ['中に', '前に', '後に', '間に'], 2,
  'Người phụ trách: Sự kiện bắt đầu lúc 17 giờ, nhân viên hãy đến trước 30 phút. / Linh: Vậy là 4 giờ rưỡi nhỉ.',
  '30分前に = trước 30 phút: 17時 − 30分 = 16時30分 (4時半), đúng với câu trả lời của Linh. 後に (HẬU) あとに = sau. 中に, 間に (GIAN) không dùng với khoảng thời gian kiểu này. いろどり 初級1 第7課.')
k('佐藤：日本語の勉強はどうですか。\nミン：読む（　　）は少し難しいです。でも、会話は得意です。',
  ['を', 'の', 'と', 'が'], 2,
  'Sato: Việc học tiếng Nhật thế nào? / Minh: Việc đọc thì hơi khó. Nhưng hội thoại thì tôi giỏi.',
  'Vるの = biến động từ thành danh từ ("việc đọc"); 読むのは難しい = việc đọc thì khó. Không nói 読むをは / 読むとは / 読むがは. 得意 (ĐẮC Ý) とくい = giỏi, sở trường. いろどり 初級1 第9課.')
k('ミン：料理教室はいくらですか。\n受付：1回800円（　　）。',
  ['もらってください', '払ってください', '借りてください', '返してください'], 2,
  'Minh: Lớp nấu ăn bao nhiêu tiền? / Lễ tân: Mỗi buổi anh/chị trả 800 yên.',
  'お金を払う (PHẤT) はらう = trả tiền → 払ってください. もらう = nhận, 借りる (TÁ) かりる = mượn, 返す (PHẢN) かえす = trả lại đồ đã mượn. いろどり 初級1 第10課.')
k('田村：もう少し食べる？\nフエン：あ、だいじょうぶです。もうお腹が（　　）。',
  ['いたいです', 'いっぱいです', 'すいています', 'あいています'], 2,
  'Tamura: Ăn thêm chút nữa không? / Huyền: À, thôi ạ. Tôi no rồi.',
  'お腹がいっぱい = no bụng → từ chối khéo khi được mời thêm. お腹がすいています = đói (ngược nghĩa). お腹がいたい = đau bụng. あいています = (chỗ) đang trống. だいじょうぶです ở đây = thôi, không cần ạ. いろどり 初級1 第12課.')
k('上司：できた？\nアリ：はい、終わりました。これで（　　）。\n上司：うん、OK。お疲れさま。',
  ['いきますか', 'いいですか', 'ほしいですか', 'なりますか'], 2,
  'Cấp trên: Xong chưa? / Ali: Vâng, xong rồi ạ. Thế này được chưa ạ? / Cấp trên: Ừ, OK. Vất vả rồi.',
  'これでいいですか = thế này được chưa ạ? – câu xin xác nhận khi nộp việc. Cấp trên đáp OK nên đây là câu hỏi xác nhận. いきますか = đi không, ほしいですか = có muốn không, なりますか = có trở thành không. いろどり 初級1 第13課.')
k('医者：今日はどうしましたか。\n郭：昨日から熱があって、のどが（　　）。',
  ['痛いんです', '痛かったら', '痛くないです', '痛いでしょう'], 1,
  'Bác sĩ: Hôm nay anh bị sao? / Quách: Từ hôm qua tôi bị sốt, và đau họng.',
  'Khi kể triệu chứng với bác sĩ dùng 〜んです (giải thích tình trạng): のどが痛いんです. 痛かったら = nếu đau, 痛くないです = không đau (ngược ý), 痛いでしょう = chắc là đau (đoán). 痛い (THỐNG) いたい. いろどり 初級1 第15課.')
k('ホセ：昨日、飲み（　　）。ちょっと二日酔いなんです。\n酒井：えー。',
  ['たいです', 'すぎます', 'すぎました', 'ましょう'], 3,
  'José: Hôm qua tôi uống quá nhiều. Hơi bị say rượu ạ. / Sakai: Ôi.',
  'Vます bỏ ます + すぎる = làm quá mức. 昨日 (hôm qua) → thì quá khứ: 飲みすぎました. すぎます là hiện tại, 飲みたいです = muốn uống, 飲みましょう = cùng uống nào. 二日酔い (NHỊ NHẬT TUÝ) ふつかよい = say rượu hôm sau. いろどり 初級1 第16課.')
k('ソカ：先生、これ、カンボジアのお酒です。先生に（　　）。\n先生：え、いいの？',
  ['もらいました', 'あげませんか', 'くれました', 'プレゼントです'], 4,
  'Soka: Thầy ơi, đây là rượu của Campuchia. Em tặng thầy ạ. / Thầy: Ơ, được thật à?',
  'Khi đưa quà: 先生にプレゼントです = đây là quà tặng thầy. もらいました = em đã nhận, くれました = (ai đó) đã cho em – sai hướng cho/nhận. あげませんか = rủ người khác cùng tặng. いろどり 初級1 第17課.')
k('メイ：お子さんが生まれたそうですね。（　　）。\n先輩：ありがとうございます。',
  ['おだいじに', 'おめでとうございます', 'いただきます', 'おつかれさまでした'], 2,
  'Mai: Nghe nói anh mới có em bé. Chúc mừng anh! / Tiền bối: Cảm ơn em.',
  'Chúc mừng tin vui (sinh con, kết hôn…) → おめでとうございます. おだいじに = mau khoẻ nhé (khi ai ốm), いただきます = câu trước khi ăn, おつかれさまでした = vất vả rồi (cuối giờ làm). 〜そうです = nghe nói. いろどり 初級1 第18課.')

# ---------- 聴解 ----------
def l(n, q, vi, o, a, ans, script, dich, gt, oimg=None):
    t = f'<span class="jp">{J(q)}</span><br><span class="vi-q">{html.escape(vi)}</span>'
    qs.append(Q(L, t, o, a, EX(ans, dich, gt, script), au=AU + f'y5_L{n:02d}.mp3', oimg=oimg))
l(1, '日本の秋はどうですか。', 'Mùa thu ở Nhật thế nào?', ['', '', '', ''], 3, 'Tranh 3 – lá đỏ đẹp',
  '春は桜の花が咲きます。暖かくなります。\n梅雨は雨がたくさん降ります。じめじめしています。\n夏は暑いです。セミが鳴きます。学校が休みになります。\n秋はすずしくなります。もみじがきれいです。\n冬は寒いです。雪が降ります。',
  'Mùa xuân hoa anh đào nở, trời ấm lên. Mùa mưa trời mưa nhiều, ẩm ướt. Mùa hè nóng, ve kêu, trường được nghỉ. Mùa thu trời mát, lá đỏ đẹp. Mùa đông lạnh, tuyết rơi.',
  'Nghe đúng đoạn 秋は…: すずしくなります。もみじがきれいです → tranh 3. Tranh 1 là xuân (桜), tranh 2 là hè (セミ), tranh 4 là đông (雪). Bài nghe nói cả 5 mùa, phải bắt đúng từ khoá 秋 (THU) あき. いろどり 初級1 第3課 (03-03).',
  oimg=[f'y5_l1_{i}.jpg' for i in range(1, 5)])
l(2, 'この町のよくないところは何ですか。', 'Điểm không tốt của thị trấn này là gì?', ['', '', '', ''], 1, 'Tranh 1 – người ta lạnh lùng',
  'A：どう？　この町は。\nB：都会ですね。人も店も多くて、にぎやかですね。\nA：そう。\nB：うーん、でも、人がちょっと冷たいです。\nA：そ、そう。',
  'A: Thấy sao, thị trấn này? / B: Đúng là thành phố nhỉ. Người đông, cửa hàng nhiều, náo nhiệt ghê. / A: Vậy à. / B: Ừm, nhưng người ta hơi lạnh lùng. / A: Th… thế à.',
  'Câu hỏi về điểm KHÔNG tốt. Sau でも (nhưng) là ý chê: 人がちょっと冷たい (LÃNH – つめたい: lạnh lùng) → tranh 1. にぎやか (tranh 2) là điểm tốt. Không nói 不便 (tranh 3) hay 緑が少ない (tranh 4). いろどり 初級1 第5課 (05-05).',
  oimg=[f'y5_l2_{i}.jpg' for i in range(1, 5)])
l(3, 'お店はどこにありますか。', 'Cửa hàng ở đâu?', ['銀行の　となり', '黒い　ビルの　となり', 'コンビニの　となり', '駅の　北口の　前'], 2, '黒い　ビルの　となり',
  'A：はい。アジア食材バグースです。\nB：すみません。そちらに行きたいんですが、どう行ったらいいですか？　今、さくら駅の北口にいます。\nA：駅の北口ですね。駅の前の道を渡って、銀行とコンビニの間の道をまっすぐ行ってください。\nB：はい。\nA：それから、1つ目の信号を右に曲がってください。\nB：右ですね。\nA：はい。その道をまっすぐ行って、2つ目の角を左に曲がってください。\nB：はい。\nA：そうすると、黒いビルが見えます。その隣です。\nB：黒いビルの隣ですね。わかりました。ありがとうございます。\nA：お待ちしております。',
  'A: Vâng, cửa hàng thực phẩm châu Á Bagus xin nghe. / B: Xin lỗi, tôi muốn đến cửa hàng, đi thế nào ạ? Tôi đang ở cửa Bắc ga Sakura. / A: Anh băng qua đường trước ga, đi thẳng con đường giữa ngân hàng và cửa hàng tiện lợi. Rồi rẽ phải ở đèn giao thông thứ nhất. Đi thẳng, đến góc thứ hai rẽ trái. Anh sẽ thấy toà nhà màu đen. Cửa hàng ở ngay cạnh đó. / B: Cạnh toà nhà màu đen nhỉ. Cảm ơn ạ.',
  'Câu chốt cuối: 黒いビルが見えます。その隣です → cạnh toà nhà đen. 銀行, コンビニ, 駅の北口 chỉ là mốc trên đường đi, dễ gây nhầm. 隣 (LÂN) となり = bên cạnh, 角 (GIÁC) かど = góc phố, 信号 (TÍN HIỆU) しんごう = đèn giao thông. いろどり 初級1 第6課 (06-12).')
l(4, '誘われた人はどう答えましたか。', 'Người được rủ đã trả lời thế nào?', ['メンバーを　さがすと　言った', '野球が　わからないので、無理だと　言った', 'ぜひ　やりたいと　言った', 'したことが　あると　言った'], 2, '野球が　わからないので、無理だと　言った',
  'A：野球、したことある？\nB：え、ないです。\nA：今度の日曜日、いっしょにやらない？　メンバーが足りなくて……。\nB：えー、無理です。野球、ぜんぜんわかりません。\nA：だいじょうぶ、だいじょうぶ。',
  'A: Đã chơi bóng chày bao giờ chưa? / B: Ơ, chưa ạ. / A: Chủ nhật tới chơi cùng không? Đội đang thiếu người… / B: Ơ, không được đâu. Tôi hoàn toàn không biết bóng chày. / A: Không sao, không sao.',
  'B nói 無理です (VÔ LÍ – むり: không được, không thể) + 野球、ぜんぜんわかりません → phương án 2. B trả lời ないです nên không phải "đã từng chơi"; メンバーが足りない là lời của người rủ. いろどり 初級1 第8課 (08-06).')
l(5, 'この人が苦手なのは何ですか。', 'Người này kém cái gì?', ['会話', '漢字', '文法', '発音'], 4, '発音',
  'A：日本語の勉強はどうですか？\nB：まあまあです。\nA：まあまあ？\nB：私は日本語の発音が苦手です。ベトナム語とぜんぜん違いますから。\nA：そうなんですか。\nB：でも、漢字はおもしろいです。たくさん覚えたいです。\nA：そうですか。',
  'A: Học tiếng Nhật thế nào? / B: Tàm tạm. / A: Tàm tạm? / B: Tôi kém phát âm tiếng Nhật. Vì nó khác hẳn tiếng Việt. / A: Ra vậy. / B: Nhưng chữ Hán thì thú vị. Tôi muốn học thuộc thật nhiều. / A: Vậy à.',
  '発音が苦手です → kém phát âm. 苦手 (KHỔ THỦ) にがて = kém, không giỏi. 漢字 thì おもしろい (thích), không phải 苦手. 発音 (PHÁT ÂM) はつおん, 文法 (VĂN PHÁP) ぶんぽう = ngữ pháp, 会話 (HỘI THOẠI) かいわ. いろどり 初級1 第9課 (09-12).')
l(6, 'マルコさんは何を買って行きますか。', 'Marco sẽ mua gì mang đến?', ['肉と　野菜', 'ビールと　ワインと　お茶', 'お茶だけ', 'ビールだけ'], 2, 'ビールと　ワインと　お茶',
  '楊：じゃあ、マルコさんは飲み物をお願いします。\nマルコ：いいですよ。ビールとワインでいいですか？\nノイ：あのう、すみません。私はお酒がだめですから……。\nマルコ：あ、じゃあ、お茶も買って行きますね。\nノイ：ありがとうございます。',
  'Dương: Vậy anh Marco lo đồ uống nhé. / Marco: Được thôi. Bia và rượu vang được không? / Noi: À, xin lỗi, tôi không uống được rượu bia… / Marco: À, vậy tôi mua thêm cả trà nhé. / Noi: Cảm ơn anh.',
  'Marco định mua ビールとワイン, rồi nói お茶も買って行きます – も = "cũng, thêm" nên mua cả ba: bia, rượu vang và trà. Không phải お茶だけ (chỉ trà). 肉と野菜 là phần người khác lo. お酒がだめ = không uống được rượu. いろどり 初級1 第11課.')
l(7, 'みかんはどうでしたか。', 'Quả quýt thế nào?', ['すっぱかった', '苦かった', '甘かった', '辛かった'], 3, '甘かった',
  'A：みかん、1つどう？　うちの庭でとれたのよ。\nB：じゃあ、いただきます。でも、まだ、ちょっとすっぱそうですね。\nA：そんなことないわよ。甘いわよ。\nB：あ、本当だ。甘い。',
  'A: Ăn một quả quýt không? Hái ở vườn nhà tôi đấy. / B: Vậy cháu xin. Nhưng trông vẫn còn hơi chua nhỉ. / A: Làm gì có. Ngọt lắm đó. / B: A, đúng thật. Ngọt.',
  'すっぱそう chỉ là đoán theo vẻ ngoài (〜そう = trông có vẻ). Ăn rồi thì nói 本当だ。甘い → ngọt. 甘い (CAM) あまい = ngọt, 苦い (KHỔ) にがい = đắng, 辛い (TÂN) からい = cay. いろどり 初級1 第12課 (12-06).')
l(8, '資料はどこに戻しますか。', 'Cất tài liệu lại vào đâu?', ['キャビネットの　左の　扉の　中、いちばん　上の　棚', 'キャビネットの　右の　扉の　中、いちばん　下の　棚', '机の　上', 'キャビネットの　右の　扉の　中、いちばん　上の　棚'], 2, 'キャビネットの　右の　扉の　中、いちばん　下の　棚',
  'A：この資料、どうしますか？\nB：キャビネットに戻しといて。\nA：ええと、キャビネットのどこですか？\nB：上の右の扉を開けて、棚のいちばん下。\nA：わかりました。右のいちばん下ですね。',
  'A: Tài liệu này làm sao ạ? / B: Cất lại vào tủ hồ sơ giúp nhé. / A: Ừm, chỗ nào trong tủ ạ? / B: Mở cửa trên bên phải, ngăn dưới cùng. / A: Em hiểu rồi. Bên phải, ngăn dưới cùng nhỉ.',
  'Câu nhắc lại cuối bài chốt đáp án: 右のいちばん下 → cửa bên phải, ngăn dưới cùng. Chữ 上 trong 上の右の扉 là cửa phía trên của tủ, không phải ngăn trên cùng – dễ bị lừa sang phương án 4. 戻しといて = 戻しておいて (cất lại sẵn). 扉 (PHI) とびら = cánh cửa, 棚 (BẰNG) たな = ngăn kệ. いろどり 初級1 第13課 (13-20).')
l(9, 'ふつうの休みのとき、「理由」には何と書きますか。', 'Khi nghỉ bình thường, ô "Lý do" ghi gì?', ['名前', '総務', '何も　書かない', '私用'], 4, '私用',
  'A：お休みを取るときには、休暇届を出してください。このフォームです。\nB：えっと、どこに何を書きますか？\nA：いちばん上の「所属」のところには、自分の所属チームの名前を書いてください。\nB：じゃあ、私は「総務」ですね。\nA：はい。それから、その下の「氏名」のところに名前を書きます。\nB：はい。\nA：それから、名前の横にハンコを押してください。あ、ハンコ、持ってますか？\nB：はい、作りました。\nA：そうですか。で、「期間」のところは、いつからいつまで何日間休むか書きます。\nB：はい。\nA：その下の「理由」ですが、普通の休みのときは、「私用」と書いてください。\nB：しよう？\nA：「私」という漢字に、「用事」の「用」です。\nB：はい。\nA：それから、ここに休み中の連絡先を書いてください。\nB：えーと、いちばん下は何ですか？\nA：「備考」のところは、普通の休みのときは、何もいりません。\nB：わかりました。いつまでに出しますか？\nA：休みの前の日までに出してください。',
  'A: Khi xin nghỉ thì nộp đơn xin nghỉ phép, là mẫu này. Ô "Bộ phận" trên cùng ghi tên nhóm mình. "Họ tên" ghi tên, bên cạnh đóng dấu. "Thời gian" ghi nghỉ từ khi nào đến khi nào, mấy ngày. Ô "Lý do", nghỉ bình thường thì ghi "việc riêng" (私用). Ở đây ghi thông tin liên lạc trong lúc nghỉ. Ô "Ghi chú" dưới cùng, nghỉ bình thường không cần ghi gì. Nộp chậm nhất ngày trước hôm nghỉ.',
  '理由 (LÍ DO) りゆう → 私用 (TƯ DỤNG) しよう = việc riêng. 総務 (TỔNG VỤ) là tên bộ phận ghi ở ô 所属; 名前 ghi ở ô 氏名; 何も書かない (không ghi gì) là ô 備考 (BỊ KHẢO – ghi chú). Bài dài, nhiều ô – phải nghe đúng chỗ nhắc tới 理由. いろどり 初級1 第14課 (14-19).')
l(10, '二日酔いのときは、何がいちばんいいと言っていますか。', 'Khi say rượu, người ta nói cái gì là tốt nhất?', ['運動すること', '寝ること', '二日酔いの　薬を　飲むこと', 'お酒を　飲むこと'], 2, '寝ること',
  'A：ホセさん、つらそうだね。\nB：はい、昨日、飲みすぎました。ちょっと二日酔いなんです……。\nA：えー。\nB：酒井さんは、二日酔いのときは、どうしていますか？\nA：二日酔いの薬を飲むかな。けっこういいよ。\nB：へー。\nA：でも、寝るのがいちばんいいけどね。\nB：そうですね。',
  'A: José, trông mệt mỏi nhỉ. / B: Vâng, hôm qua tôi uống quá nhiều. Hơi say rượu… / B: Anh Sakai khi say rượu thì làm thế nào? / A: Chắc là uống thuốc giải rượu. Khá hiệu quả đấy. / A: Nhưng ngủ là tốt nhất. / B: Đúng vậy.',
  'Thuốc chỉ là けっこういい (khá tốt). Sau でも mới là ý chính: 寝るのがいちばんいい → ngủ là tốt nhất. いちばん = nhất. Dễ chọn nhầm phương án 3 vì được nhắc trước. いろどり 初級1 第16課 (16-04).')
l(11, 'トゥロンには何が入っていますか。', 'Bánh turon có nhân gì?', ['お米', 'バナナ', 'チョコレート', '魚'], 2, 'バナナ',
  'A：これ、私が作ったお菓子です。みなさん、食べてください。\nB：わー、ありがとう。\nA：トゥロンといいます。フィリピンではとても有名です。バナナが入っています。\nB：へー。いただきます。うん、おいしい！',
  'A: Đây là bánh tôi tự làm. Mọi người ăn đi ạ. / B: Oa, cảm ơn. / A: Bánh tên là turon, ở Philippines rất nổi tiếng. Bên trong có chuối. / B: Ồ. Mình ăn nhé. Ừm, ngon!',
  'バナナが入っています → nhân chuối. 〜が入っている (NHẬP) = có ~ bên trong. お菓子 (QUẢ TỬ) おかし = bánh kẹo. Các phương án khác không được nhắc tới. いろどり 初級1 第17課 (17-09).')
l(12, 'この人は日本に来て、どのぐらいですか。', 'Người này đến Nhật được bao lâu rồi?', ['1か月', '1年', '2年', '半年'], 4, '半年',
  'A：日本に来て、どのぐらいですか？\nB：ちょうど半年です。\nA：そうですか。日本に慣れましたか？\nB：はい、なんとか。',
  'A: Bạn sang Nhật được bao lâu rồi? / B: Vừa tròn nửa năm. / A: Vậy à. Bạn đã quen với Nhật chưa? / B: Vâng, cũng tạm quen.',
  'ちょうど半年 = vừa tròn nửa năm (6 tháng). 半年 (BÁN NIÊN) はんとし. ちょうど = vừa đúng. なんとか = cũng tạm được. いろどり 初級1 第1課 (01-07).')

# ---------- 読解 ----------
def r(q, o, a, img, dich, gt):
    qs.append(Q(R, J(q), o, a, EX(o[a-1], dich, gt), [img]))
D1 = 'Sự kiện trong năm ở thị trấn Midori: tháng 4 ngắm hoa (công viên Midori); tháng 7 lễ hội mùa hè – múa bon (quảng trường trước ga); tháng 8 lễ hội pháo hoa (sông Midori); tháng 10 hội thao (nhà thi đấu thành phố); tháng 12 giã bánh mochi (nhà văn hoá).'
r('（1）花火大会はどこでありますか。', ['みどり川', '駅前広場', '公民館', 'みどり公園'], 1, 'y5_r1.jpg', D1,
  'Dòng 8月: 花火大会（みどり川）→ sông Midori. 花火大会 (HOA HOẢ ĐẠI HỘI) はなびたいかい = lễ hội pháo hoa. Chữ trong ngoặc ( ) là địa điểm. 〜であります = (sự kiện) diễn ra ở ~.')
r('（2）桜を見るイベントは何月ですか。', ['10月', '12月', '7月', '4月'], 4, 'y5_r1.jpg', D1,
  'Ngắm hoa anh đào = お花見 (おはなみ) → dòng 4月. Bảng không ghi chữ 桜, phải biết お花見 là đi ngắm hoa anh đào. 桜 (ANH) さくら.')
D3 = 'Lịch xe buýt từ cửa Bắc ga Sakura đến bệnh viện Sakura (ngày thường): 7 giờ: 10, 40 · 8 giờ: 05, 20, 50 · 9 giờ: 30 · 10 giờ: 30. ※ Thứ Bảy, Chủ nhật mỗi tiếng 1 chuyến. ※ Đến bệnh viện mất 15 phút.'
r('（1）平日、8時15分にバス停に着きました。次のバスは何時ですか。', ['8時20分', '8時50分', '9時30分', '8時05分'], 1, 'y5_r3.jpg', D3,
  'Hàng 8時 có các chuyến 05, 20, 50. Đến lúc 8:15 thì chuyến 8:05 đã đi, chuyến tiếp theo là 8:20. 平日 (BÌNH NHẬT) へいじつ = ngày thường, 次 (THỨ) つぎ = tiếp theo, バス停 = trạm xe buýt.')
r('（2）8時50分のバスに乗ると、病院に何時ごろ着きますか。', ['8時ごろ', '9時5分ごろ', '9時ごろ', '9時30分ごろ'], 2, 'y5_r3.jpg', D3,
  'Dòng ※ 病院まで15分 → 8:50 + 15 phút = 9:05. Đề hay giấu thông tin quan trọng ở dòng ※ cuối bảng. 〜ごろ = khoảng (giờ).')
D5 = 'Trung tâm giao lưu quốc tế thành phố Sakura – "Lớp tiếng Nhật dễ hiểu". Cùng học tiếng Nhật nhé. Ai cũng tham gia được. Lớp: thứ Tư tối 7:00–8:30, thứ Bảy sáng 10:00–11:30. Địa điểm: Trung tâm thị dân tầng 2 phòng 201. Phí: mỗi buổi 200 yên (người lần đầu miễn phí). Đăng ký: liên lạc bằng điện thoại hoặc email trước một ngày. Đồ mang theo: không cần sách giáo khoa, hãy mang vở và bút.'
r('（1）土曜日のクラスは何時に終わりますか。', ['10:00', '11:30', '8:30', '7:00'], 2, 'y5_r5.jpg', D5,
  'Lớp thứ Bảy: 朝10:00〜11:30 → kết thúc lúc 11:30. 10:00 là giờ bắt đầu; 7:00 và 8:30 là lớp thứ Tư. 終わる (CHUNG) おわる = kết thúc.')
r('（2）はじめて参加する人は何をしなければなりませんか。', ['教科書を　買う', '前の　日までに　れんらくする', '200円　はらう', '当日、センターで　もうしこむ'], 2, 'y5_r5.jpg', D5,
  'Dòng もうしこみ: 電話かメールで、前の日までにれんらくしてください → phải liên lạc trước một ngày. Người lần đầu miễn phí nên không trả 200 yên; không cần mua sách (教科書はいりません); không đăng ký ngay tại chỗ. Vなければなりません = phải làm.')
D7 = 'Máy photo đang hỏng. Máy photo tầng 2 không chạy. Đã gọi điện cho bên sửa chữa. Chiều mai họ đến sửa. Trước lúc đó hãy dùng máy photo tầng 3. Ai cần photo màu thì nói với Tanaka ở phòng tổng vụ.'
r('（1）今日、コピーをするときはどうしますか。', ['あしたまで　待つ', '3かいの　コピー機を　使う', '2かいの　コピー機を　使う', '業者に　電話する'], 2, 'y5_r7.jpg', D7,
  'それまでは3かいのコピー機を使ってください → hôm nay dùng máy tầng 3. Máy tầng 2 đang hỏng; việc gọi bên sửa đã làm rồi (電話しました). それまで = cho đến lúc đó (chiều mai). 業者 (NGHIỆP GIẢ) ぎょうしゃ = bên dịch vụ, nhà thầu.')
r('（2）カラーコピーをしたい人はどうしますか。', ['業者に　電話する', 'あしたの　午後　する', '2かいに　行く', '田中さんに　言う'], 4, 'y5_r7.jpg', D7,
  'カラーコピーが必要な人は、そうむ部の田中に言ってください → nói với anh/chị Tanaka. Trong thông báo nội bộ, người trong công ty tự gọi tên đồng nghiệp không kèm さん (田中に), câu trả lời thì thêm さん. 必要 (TẤT YẾU) ひつよう = cần.')
D9 = 'Số điện thoại khi gặp chuyện: 119 – cháy, xe cấp cứu (bệnh đột ngột, bị thương nặng); 110 – cảnh sát (tai nạn, trộm); #7119 – khi không biết có nên gọi xe cấp cứu hay không thì có thể hỏi ý kiến. Khi gọi sẽ được hỏi "Đã xảy ra chuyện gì?", "Ở đâu?". Hãy bình tĩnh trả lời chậm rãi.'
r('（1）友だちが急にたおれました。何番に電話しますか。', ['117', '110', '119', '#7119'], 3, 'y5_r9.jpg', D9,
  'Bạn đột nhiên ngã gục = bệnh đột ngột (急な病気) → gọi xe cấp cứu 119. 110 là cảnh sát; #7119 chỉ để hỏi khi chưa biết có cần xe cấp cứu không; 117 không có trong bảng (là số báo giờ). 急に (CẤP) きゅうに = đột ngột, たおれる = ngã gục.')
r('（2）#7119はどんなときに電話しますか。', ['じこの　とき', 'どろぼうが　入った　とき', 'きゅうきゅう車を　よぶか　どうか　わからない　とき', '火事の　とき'], 3, 'y5_r9.jpg', D9,
  'Dòng #7119: きゅうきゅう車をよぶかどうかわからないとき、相談できます. Tai nạn, trộm → 110; cháy → 119. 〜かどうか = có ~ hay không. 相談 (TƯƠNG ĐÀM) そうだん = hỏi ý kiến, tư vấn.')
D11 = 'Mai 12:10: Nghe nói chị Yamada mới sinh một bé gái! / Emi 12:11: Oa, tốt quá. Cả nhóm cùng tặng quà mừng không? / Mai 12:12: Hay đó. Khoảng bao nhiêu tiền thì được ạ? / Emi 12:13: Với người trong công ty thì mỗi người khoảng 1.000 yên. 5 người mua món 5.000 yên nhé. / Mai 12:14: Vậy em sẽ đi mua ở trung tâm thương mại vào thứ Sáu.'
r('（1）一人いくら出しますか。', ['2,000円', '5,000円', '1,000円', '500円'], 3, 'y5_r11.jpg', D11,
  '一人1,000円ぐらい → mỗi người góp 1.000 yên. 5,000円 là tổng tiền của 5 người (5人で5,000円のもの). 出す (XUẤT) だす = bỏ ra, góp (tiền).')
r('（2）プレゼントはだれが買いに行きますか。', ['5人　みんな', 'えみさん', '山田さん', 'メイさん'], 4, 'y5_r11.jpg', D11,
  'Tin nhắn cuối của メイ: わたしが金曜日にデパートで買って来ます → Mai đi mua. Yamada là người được tặng; Emi chỉ đề xuất số tiền. Vて来ます = đi làm ~ rồi về.')

ex = dict(id='jft-y5', group='Đề thi thử JFT-Basic', title='Đề 30', sub='Có phần nghe · いろどり 初級1', time=60, tag='Đề mới chuẩn', qs=qs)
E = json.load(open(REPO + 'src/raw/jft_exams.json'))
E = [e for e in E if e['id'] != 'jft-y5']
pos = max(i for i, e in enumerate(E) if e['id'] == 'jft-y4') + 1
E = E[:pos] + [ex] + E[pos:]
json.dump(E, open(REPO + 'src/raw/jft_exams.json', 'w'), ensure_ascii=False, indent=1)
print(len(qs), [sum(q['s'] == x for q in qs) for x in (V, K, L, R)])
