# Video "Toàn bộ ngữ pháp JFT trong 10 phút" (22/11/2026) — nội dung slide + lời đọc.
# Câu ví dụ tiếng Nhật lấy NGUYÊN VĂN từ 文法ノート いろどり (grammar.js) theo (cấp, bài, số mẫu, đoạn chữ để tìm câu);
# nghĩa tiếng Việt, cách gom nhóm, bảng chia, lời đọc: Anh Trọng Dạy JFT soạn.
# item = (mẫu, nghĩa, (cấp, bài, số, đoạn tìm câu) hoặc None, dịch câu ví dụ, nguồn)

S = []
def add(**k): S.append(k)

add(kind='title', img='sensei', say=(
    'Toàn bộ ngữ pháp thi JFT, mình gói lại trong khoảng mười phút. '
    'Ngữ pháp JFT nằm trong giáo trình Irodori, từ quyển Nhập môn đến Sơ cấp 2, có hơn hai trăm mẫu. '
    'Nhưng khi vào đề, chúng chỉ xoay quanh mười hai nhóm. Nắm chắc mười hai nhóm này là các bạn hiểu được gần hết câu hội thoại trong đề.'))

add(kind='map', img='study', say=(
    'Mười hai nhóm đó là: trợ từ, danh từ và tính từ, các thể của động từ, nhờ vả và cấm đoán, '
    'mong muốn và rủ rê, sở thích và khả năng, trạng thái và thay đổi, thời gian, lý do và điều kiện, '
    'so sánh, phỏng đoán và nghe nói, và cuối cùng là cho nhận. Mình đi lần lượt từng nhóm nhé.'))

G = ['Trợ từ', 'Danh từ · Tính từ', 'Các thể động từ', 'Nhờ vả · Xin phép · Cấm', 'Mong muốn · Rủ rê · Khuyên',
     'Sở thích · Kinh nghiệm · Khả năng', 'Trạng thái · Thay đổi', 'Thời gian · Trình tự', 'Lý do · Điều kiện',
     'So sánh · Mức độ', 'Phỏng đoán · Nghe nói', 'Cho · Nhận']

# 1. Trợ từ
add(kind='items', g=1, img='study', sub='Trợ từ cơ bản (1)', items=[
    ('は', 'đánh dấu chủ đề của câu', ('入門', 3, '❶', '私はマルシア'), 'Tôi là Márcia.', '入門3'),
    ('が', 'đi với 好き・ある・いる・できる', ('入門', 5, '❶', '肉と野菜が'), 'Tôi thích thịt và rau.', '入門5'),
    ('を', 'đánh dấu đối tượng của hành động', ('入門', 5, '❹', 'シリアル'), 'Tôi ăn ngũ cốc.', '入門5'),
    ('に', 'thời điểm · nơi đến · nơi có người, vật', ('入門', 9, '❶', '5時に'), 'Tôi dậy lúc 5 giờ.', '入門9'),
    ('で', 'nơi diễn ra hành động · phương tiện', ('入門', 8, '❶', '着替え'), 'Thay quần áo ở đây.', '入門8'),
], say=(
    'Nhóm một: trợ từ. は đánh dấu chủ đề, câu đang nói về cái gì. が đi với các từ như 好き, ある, いる, できる. を đánh dấu đối tượng của hành động: ăn cái gì, uống cái gì. に chỉ thời điểm, nơi đến và nơi có người, có vật. Còn で chỉ nơi diễn ra hành động và phương tiện. に và で là cặp hay nhầm nhất trong đề: ở đâu mà có hành động thì dùng で.'))
add(kind='items', g=1, img='study', sub='Trợ từ cơ bản (2)', items=[
    ('へ', 'hướng đi (giống に)', ('入門', 18, '❹', '京都へ'), 'Tôi muốn đi Kyoto.', '入門18'),
    ('と', 'và · cùng với (ai)', ('入門', 11, '❺', '夫と公園'), 'Tôi chơi quần vợt cùng chồng ở công viên.', '入門11'),
    ('も', 'cũng', ('入門', 3, '❺', 'ケマラさんも'), 'Chị Khemera cũng đến từ Việt Nam à?', '入門3'),
    ('の', 'của · nối hai danh từ', ('入門', 4, '❹', '私の母'), 'Đây là mẹ tôi.', '入門4'),
    ('から〜まで', 'từ … đến …', ('入門', 9, '❷', '12時から'), 'Từ 12 giờ đến 1 giờ là giờ nghỉ trưa.', '入門9'),
    ('や', 'liệt kê vài ví dụ', ('初級1', 3, '❻', '海や山'), 'Đi chơi ở biển, ở núi cũng vui.', '初級1・3'),
], say=(
    'Tiếp theo: へ chỉ hướng đi, dùng gần giống に. と là "và", hoặc "cùng với ai". も là "cũng". の nối hai danh từ, nghĩa là "của". から〜まで là từ đâu đến đâu, dùng cho cả giờ giấc lẫn địa điểm. Còn や để liệt kê vài ví dụ, ngụ ý là còn nữa.'))

# 2. Danh từ · Tính từ
add(kind='conj', g=2, img='atsui', sub='Chia danh từ · tính từ', rows=[
    ('Hiện tại', '{学生|がくせい}|です', '{寒|さむ}|いです'),
    ('Phủ định', '{学生|がくせい}|じゃないです', '{寒|さむ}|くないです'),
    ('Quá khứ', '{学生|がくせい}|でした', '{寒|さむ}|かったです'),
    ('QK phủ định', '{学生|がくせい}|じゃなかったです', '{寒|さむ}|くなかったです'),
], ex=[(('入門', 7, '❺', '寮は広く'), 'Ký túc xá không rộng.', '入門7'), (('入門', 17, '❸', '国際フェスティバル'), 'Lễ hội quốc tế rất vui.', '入門17')], say=(
    'Nhóm hai: danh từ và tính từ. Các bạn nhìn bảng: danh từ và tính từ đuôi な chia giống nhau, phủ định là じゃないです, quá khứ là でした. Tính từ đuôi い thì bỏ い: phủ định là くないです, quá khứ là かったです. Riêng いい, nghĩa là tốt, phải đổi thành よくないです, よかったです. Chỗ này rất hay ra trong đề.'))
add(kind='items', g=2, img='atsui', sub='Nối câu · bổ nghĩa', items=[
    ('ナAな N ／ イAい N', 'tính từ đứng trước danh từ', ('入門', 14, '❸', '広い公園'), 'Công viên rộng nhỉ.', '入門14'),
    ('Nで ／ ナAで ／ イAくて、〜', 'và (nối hai câu)', ('初級1', 5, '❶', 'にぎやかで'), 'Thị trấn này rất nhộn nhịp và tiện lợi.', '初級1・5'),
    ('〜けど、〜', 'nhưng', ('初級1', 5, '❷', '都会だけど'), 'Tuy là thành phố nhưng nhiều cây xanh nhỉ.', '初級1・5'),
    ('あまり 〜ない', 'không … lắm', ('入門', 11, '❸', 'スポーツは'), 'Tôi không thích thể thao lắm.', '入門11'),
], say=(
    'Khi tính từ đứng trước danh từ: tính từ な thì thêm な, tính từ い giữ nguyên. Muốn nối hai ý, ví dụ nhộn nhịp và tiện lợi, thì đổi thành で hoặc くて. けど nghĩa là "nhưng". Còn あまり đi với phủ định, nghĩa là "không … lắm".'))

# 3. Các thể động từ
add(kind='forms', g=3, img='taisou', sub='5 thể cơ bản của động từ', rows=[
    ('', 'ます{形|けい}', '{辞書形|じしょけい}', 'ない{形|けい}', 'て{形|けい}', 'た{形|けい}'),
    ('Nhóm 1', '書きます', '書く', '書かない', '書いて', '書いた'),
    ('Nhóm 2', '食べます', '食べる', '食べない', '食べて', '食べた'),
    ('Nhóm 3', 'します', 'する', 'しない', 'して', 'した'),
    ('', '来ます', '来る', '来ない', '来て', '来た'),
], say=(
    'Nhóm ba là xương sống của cả ngữ pháp: các thể của động từ. Thể ます là thể lịch sự. Ngoài ra có thể từ điển, thể ない, thể て, thể た; khi nói chuyện thân mật thì dùng các thể này thay cho ます, gọi chung là thể thông thường. Gần như mẫu ngữ pháp nào cũng là: một thể của động từ, cộng thêm một cái đuôi. Nên thuộc bảng này là học mẫu nào cũng nhanh.'))
add(kind='terule', g=3, img='taisou', sub='Cách đổi sang thể て', say=(
    'Thể て đổi như sau. Nhóm một: âm い, ち, り trước ます đổi thành って. み, び, に đổi thành んで. き thành いて, ぎ thành いで, し thành して. Riêng 行きます là 行って. Nhóm hai chỉ cần bỏ ます thêm て. Nhóm ba: します thành して, 来ます thành 来て. Thể た đổi y hệt, chỉ thay て bằng た.'))

# 4. Nhờ vả · Xin phép · Cấm
add(kind='items', g=4, img='onegai', sub='Nhờ vả · Xin phép', items=[
    ('Vてください', 'hãy làm V', ('入門', 10, '❶', '手伝ってください'), 'Phiền anh/chị giúp tôi một tay.', '入門10'),
    ('Vてもらえませんか', 'nhờ lịch sự: làm V giúp tôi được không', ('初級1', 9, '❹', 'チェック'), 'Bạn kiểm tra tiếng Nhật giúp tôi được không?', '初級1・9'),
    ('Vてもいいですか', 'xin phép: tôi làm V được không', ('初級1', 14, '❸', 'トイレ'), 'Em đi vệ sinh một chút được không ạ?', '初級1・14'),
    ('Vたほうがいいです', 'lời khuyên: nên làm V', ('初級2', 5, '❺', '厚い上着'), 'Bạn nên mang theo áo khoác dày đấy.', '初級2・5'),
], say=(
    'Nhóm bốn: nhờ vả và xin phép, đều đi với thể て. てください là "hãy làm". てもらえませんか là nhờ một cách lịch sự hơn. てもいいですか là xin phép. Thêm một mẫu lời khuyên: thể た cộng ほうがいいです, nghĩa là "nên làm".'))
add(kind='items', g=4, img='dame', sub='Cấm · Bắt buộc', items=[
    ('Vないでください', 'đừng làm V', ('初級1', 15, '❷', '激しい運動'), 'Đừng vận động mạnh nhé.', '初級1・15'),
    ('Vてはいけません', 'không được làm V (cấm)', ('初級2', 10, '❷', '横断歩道'), 'Khi đèn đỏ thì không được băng qua vạch kẻ đường.', '初級2・10'),
    ('Vちゃだめ', 'không được V (văn nói)', ('初級2', 10, '❷', '話しちゃ'), 'Trong xe buýt thì không được nói chuyện nhỉ.', '初級2・10'),
    ('Vなければなりません', 'phải làm V', ('初級1', 14, '❺', '役所'), 'Em phải đi lên ủy ban.', '初級1・14'),
    ('Vなくちゃ', 'phải V (văn nói)', ('初級2', 10, '❸', '食器'), 'Bát đĩa thì phải tự mình dọn chứ.', '初級2・10'),
], say=(
    'Ngược lại là cấm: thể ない cộng でください, nghĩa là "đừng làm". てはいけません là "không được làm", mạnh hơn. Trong hội thoại người ta nói gọn thành ちゃだめ. Còn phải làm gì đó thì dùng なければなりません, nói gọn là なくちゃ. Đề JFT rất hay cho đọc biển báo và nội quy, nên nhóm này phải chắc.'))

# 5. Mong muốn · Rủ rê
add(kind='items', g=5, img='nomikai', sub='Mong muốn', items=[
    ('Vたいです', 'muốn làm V', ('入門', 18, '❶', '炊飯器'), 'Tôi muốn mua nồi cơm điện.', '入門18'),
    ('Nがほしいんですが', 'tôi muốn có N (hỏi nhờ)', ('入門', 15, '❶', '延長コード'), 'Tôi muốn mua dây điện nối dài…', '入門15'),
    ('Vてみたいんですが', 'tôi muốn thử làm V', ('初級1', 10, '❶', '合気道'), 'Tôi muốn thử tập aikido…', '初級1・10'),
    ('Vるつもりです', 'định làm V', ('初級2', 6, '❶', '中禅寺湖'), 'Ngày mai tôi định đi hồ Chuzenji.', '初級2・6'),
    ('Vようと思います', 'tôi tính làm V', ('初級2', 18, '❶', 'タイで'), 'Tương lai tôi định mở công ty riêng ở Thái Lan.', '初級2・18'),
], say=(
    'Nhóm năm: mong muốn. Bỏ ます thêm たいです là "muốn làm". Muốn có đồ vật thì dùng ほしい. てみたい là "muốn thử". Còn dự định thì có つもりです, và thể ý chí cộng と思います.'))
add(kind='items', g=5, img='nomikai', sub='Rủ rê · Đề nghị', items=[
    ('Vませんか', 'rủ: cùng làm V không?', ('入門', 12, '❸', 'いっしょに行きませんか'), 'Đi cùng nhau không?', '入門12'),
    ('Vに行きませんか', 'rủ đi làm V', ('初級1', 8, '❸', '食べに'), 'Đi ăn cùng nhau không?', '初級1・8'),
    ('Vましょう', 'cùng làm V nào', ('入門', 12, '❹', 'また今度'), 'Để lần sau mình cùng đi nhé.', '入門12'),
    ('Vましょうか', 'để tôi làm V nhé (đề nghị giúp)', ('初級1', 10, '❸', '手伝いましょうか'), 'Nếu được thì để tôi giúp nhé?', '初級1・10'),
], say=(
    'Rủ rê: ませんか là "cùng làm không". ましょう là "cùng làm nào". Còn ましょうか, thêm chữ か, là "để tôi làm giúp nhé". ましょう và ましょうか chỉ khác nhau một chữ mà nghĩa khác hẳn, đề rất hay hỏi chỗ này. Từ chối thì người Nhật hay nói 「ちょっと…」 hoặc 「また今度」.'))

# 6. Sở thích · Kinh nghiệm · Khả năng
add(kind='items', g=6, img='tozan', sub='Sở thích · Kinh nghiệm', items=[
    ('趣味はVることです', 'sở thích là làm V', ('初級1', 2, '❶', '趣味は映画'), 'Sở thích của tôi là xem phim.', '初級1・2'),
    ('Vるのが好きです', 'thích làm V', ('初級1', 2, '❷', 'ゲーム'), 'Tôi thích chơi game.', '初級1・2'),
    ('Vたことがあります', 'đã từng làm V', ('初級1', 8, '❷', 'プロレス'), 'Bạn đã từng xem đấu vật chưa?', '初級1・8'),
    ('Vたり Vたりします', 'lúc thì V1, lúc thì V2', ('初級1', 16, '❸', 'テレビを見たり'), 'Ngày nghỉ tôi xem TV, nghe nhạc, thư thả.', '初級1・16'),
], say=(
    'Nhóm sáu: sở thích và kinh nghiệm. Thể từ điển cộng ことです dùng để nói "sở thích là". のが好きです là "thích làm gì". Thể た cộng ことがあります là "đã từng làm". たり〜たり dùng để kể vài việc tiêu biểu, ví dụ ngày nghỉ xem ti vi, nghe nhạc.'))
add(kind='items', g=6, img='tozan', sub='Khả năng', items=[
    ('Nができます', 'biết, có thể làm N', ('初級1', 2, '❻', 'テニスが'), 'Tôi biết chơi quần vợt. Tôi cũng biết chơi đàn piano.', '初級1・2'),
    ('Vることができます', 'có thể làm V', ('初級1', 5, '❸', '一年中'), 'Quanh năm có thể ngắm nhiều loại hoa.', '初級1・5'),
    ('Thể khả năng', '書く→書ける ・ 食べる→食べられる ・ する→できる ・ 来る→来られる', ('初級2', 5, '❶', 'カニ'), 'Ở đó có thể ăn cua, nhím biển tươi ngon đấy.', '初級2・5'),
    ('V方', 'cách làm V', ('初級1', 9, '❺', '辞書の使い方'), 'Hãy chỉ cho tôi cách dùng cuốn từ điển này.', '初級1・9'),
], say=(
    'Khả năng có ba cách nói. Danh từ cộng ができます. Thể từ điển cộng ことができます. Và thể khả năng: nhóm một đổi đuôi う thành える, như 書く thành 書ける; nhóm hai thêm られる; する thành できる, 来る thành 来られる. Thêm một mẫu hay gặp trong bài đọc hướng dẫn: bỏ ます thêm 方, nghĩa là "cách làm".'))

# 7. Trạng thái · Thay đổi
add(kind='items', g=7, img='seichou', sub='Trạng thái', items=[
    ('Vています ①', 'đang làm (việc gì đó lâu dài, nghề nghiệp)', ('初級1', 1, '❹', '介護の仕事'), 'Tôi đang làm việc. Tôi làm công việc điều dưỡng.', '初級1・1'),
    ('Vています ②', 'thói quen, việc làm thường xuyên', ('初級1', 2, '❺', '空手'), 'Tôi học karate từ năm ngoái.', '初級1・2'),
    ('Vています ③', 'đang diễn ra lúc này', ('初級1', 4, '❸', '雨が降って'), 'Bây giờ trời vẫn đang mưa một chút.', '初級1・4'),
    ('Vてあります', 'đã làm sẵn (có người làm)', ('初級2', 13, '❷', 'パンフレット'), 'Chúng tôi có chuẩn bị sẵn tờ rơi nhiều thứ tiếng.', '初級2・13'),
    ('Vたままです', 'vẫn để nguyên như vậy', ('初級2', 15, '❶', '電気がついた'), 'Đèn phòng họp vẫn để bật nguyên đấy.', '初級2・15'),
], say=(
    'Nhóm bảy: trạng thái. ています có ba nghĩa chính: việc đang làm lâu dài như nghề nghiệp, thói quen, và việc đang diễn ra lúc này. てあります là đã có người làm sẵn. たまま là vẫn để nguyên, ví dụ quên tắt đèn, đèn vẫn bật.'))
add(kind='items', g=7, img='seichou', sub='Thay đổi', items=[
    ('Nに ／ ナAに ／ イAく なります', 'trở nên, trở thành', ('初級1', 3, '❶', '暖かく'), 'Mùa xuân hoa anh đào nở. Trời trở nên ấm áp.', '初級1・3'),
    ('Vるようになりました', 'đã có thể làm V (trước không được)', ('初級2', 17, '❶', '話せるように'), 'So với trước, tôi đã nói được nhiều hơn.', '初級2・17'),
    ('Vるようにしています', 'cố gắng duy trì làm V', ('初級1', 16, '❹', '野菜を'), 'Tôi cố gắng ăn nhiều rau nhất có thể.', '初級1・16'),
    ('もうVました ／ まだVていません', 'đã V rồi ／ vẫn chưa V', ('初級2', 8, '❶', '準備は'), 'Chuẩn bị xong chưa? Vẫn chưa xong.', '初級2・8'),
], say=(
    'Thay đổi: danh từ và tính từ な thêm になります, tính từ い đổi thành くなります, nghĩa là "trở nên". ようになりました là "đã làm được", trước đây thì chưa. ようにしています là cố gắng duy trì một thói quen. もう là "đã … rồi", まだ là "vẫn chưa". Chú ý: まだ thì đi với ていません.'))

# 8. Thời gian · Trình tự
add(kind='items', g=8, img='tokei', sub='Khi nào · Trước · Sau', items=[
    ('〜とき、〜', 'khi …', ('初級1', 10, '❺', '暇なとき'), 'Lúc rảnh, tôi xem phim truyền hình Nhật.', '初級1・10'),
    ('Vる前に、〜', 'trước khi V', ('初級1', 15, '❹', '寝る前に'), 'Mỗi ngày uống 1 lần, trước khi đi ngủ.', '初級1・15'),
    ('Vたあと、〜', 'sau khi V', ('初級1', 15, '❹', '飲んだあと'), 'Sau khi uống thì đừng lái xe nhé.', '初級1・15'),
    ('Vてから、〜', 'làm V xong rồi mới …', ('初級2', 4, '❹', 'お好み焼き'), 'Okonomiyaki thì trước tiên trộn đều nhân rồi mới nướng.', '初級2・4'),
], say=(
    'Nhóm tám: thời gian. とき là "khi". 前に là "trước khi", đi với thể từ điển. あと là "sau khi", đi với thể た. てから là làm xong việc này rồi mới làm việc kia. Đề nghe hay hỏi thứ tự: làm gì trước, làm gì sau. Nghe được 前に và あと là trả lời được.'))
add(kind='items', g=8, img='tokei', sub='Cùng lúc · Cho đến khi · Vừa mới', items=[
    ('Vながら、〜', 'vừa V vừa …', ('初級2', 9, '❽', '食事をしながら'), 'Dịp Tết, tôi vừa ăn cơm vừa nói chuyện nhiều với bố mẹ.', '初級2・9'),
    ('Vるまで、〜', 'cho đến khi V', ('初級2', 12, '❶', '店の人が'), 'Xin hãy đợi ở đây cho đến khi nhân viên đến.', '初級2・12'),
    ('Vたばかりです', 'vừa mới V', ('初級2', 1, '❷', '先週'), 'Tôi vừa mới đến Nhật tuần trước.', '初級2・1'),
], say=(
    'ながら là vừa làm việc này vừa làm việc kia. まで là "cho đến khi". たばかりです là "vừa mới", ví dụ vừa mới sang Nhật.'))

# 9. Lý do · Điều kiện
add(kind='items', g=9, img='ame', sub='Lý do', items=[
    ('〜から、〜', 'vì … nên …', ('初級1', 3, '❺', '果物'), 'Vì trái cây ngon nên tôi thích mùa thu.', '初級1・3'),
    ('〜ので、〜', 'vì … nên … (nhẹ nhàng, lịch sự)', ('初級2', 3, '❶', 'ここは安い'), 'Ở đây rẻ nên tôi hay đến.', '初級2・3'),
    ('Nで ／ 〜て、〜', 'do … nên …', ('初級1', 14, '❶', '事故で'), 'Do tai nạn nên tàu điện đang bị trễ.', '初級1・14'),
    ('〜し、〜し', 'vừa … lại … (nêu nhiều lý do)', ('初級2', 2, '❹', '安室'), 'Tôi thích Amuro Namie. Chị ấy vừa ngầu, hát và nhảy lại giỏi.', '初級2・2'),
], say=(
    'Nhóm chín: lý do. から và ので đều là "vì … nên", ので nghe nhẹ nhàng, lịch sự hơn. で và て cũng có thể chỉ lý do, như do tai nạn nên tàu trễ. し dùng khi kể nhiều lý do cùng lúc.'))
add(kind='items', g=9, img='ame', sub='Điều kiện', items=[
    ('〜たら、〜', 'nếu … thì … ／ sau khi … thì …', ('初級2', 7, '❶', '暇だったら'), 'Nếu rảnh thì giúp tôi một chút nhé.', '初級2・7'),
    ('Vると、〜', 'hễ V thì … (kết quả chắc chắn)', ('初級1', 13, '❹', 'カラーコピー'), 'Bấm nút này thì có thể photo màu.', '初級1・13'),
    ('Nなら、〜', 'nếu là N thì …', ('初級2', 4, '❶', 'おいしい店なら'), 'Quán ngon thì phải là quán "Senpo".', '初級2・4'),
    ('〜ても、〜', 'dù … cũng …', ('初級2', 16, '❹', '大きな地震'), 'Dù động đất lớn xảy ra cũng đừng vội vàng chạy đi.', '初級2・16'),
], say=(
    'Điều kiện: たら là "nếu", dùng được trong hầu hết trường hợp. と là hễ làm gì thì chắc chắn xảy ra, hay gặp khi hướng dẫn dùng máy. なら là "nếu là cái đó thì", dùng để đáp lại lời người kia. ても là "dù … cũng". Câu về động đất, sơ tán rất hay ra trong đề, và hay dùng đúng mẫu ても này.'))

# 10. So sánh · Mức độ
add(kind='items', g=10, img='hikaku', sub='So sánh', items=[
    ('AとB、どちらが〜ですか', 'A và B, cái nào … hơn?', ('初級1', 11, '❷', 'ジュースとお茶'), 'Nước ép và trà, bạn thích cái nào?', '初級1・11'),
    ('Nのほうがいいです', 'N thì hơn', ('初級1', 11, '❸', '塩のほう'), 'Tôi thích loại muối hơn.', '初級1・11'),
    ('AよりBのほうが〜', 'B … hơn A', ('初級2', 12, '❸', '若い人'), 'Với người trẻ, màu bạc được ưa chuộng hơn màu trắng.', '初級2・12'),
    ('〜がいちばん〜', '… nhất', ('初級1', 3, '❷', '8月が'), 'Ở Nhật, tháng 8 là nóng nhất.', '初級1・3'),
], say=(
    'Nhóm mười: so sánh. Hỏi: AとB、どちらが, cái nào hơn. Trả lời: のほうが, cái này hơn. より nghĩa là "so với", đứng sau cái bị so sánh. いちばん là "nhất". Chú ý vị trí: cái đứng trước より là cái thua, cái đi với ほうが là cái hơn.'))
add(kind='items', g=10, img='hikaku', sub='Mức độ', items=[
    ('Vすぎます', 'làm V quá nhiều', ('初級1', 16, '❷', '飲みすぎ'), 'Hôm qua tôi uống quá nhiều.', '初級1・16'),
    ('ナA ／ イAすぎます', 'quá …', ('初級2', 11, '❷', '派手すぎ'), 'Màu này hơi quá sặc sỡ.', '初級2・11'),
    ('Vやすいです ／ Vにくいです', 'dễ làm V ／ khó làm V', ('初級2', 12, '❷', '使いにくい'), 'Cái máy hút bụi này nặng, khó dùng nhỉ.', '初級2・12'),
], say=(
    'Mức độ: すぎます là "quá", đi được với động từ lẫn tính từ. やすい là "dễ làm", にくい là "khó làm", gắn sau động từ bỏ ます. Ví dụ 使いやすい là dễ dùng.'))

# 11. Phỏng đoán · Nghe nói
add(kind='items', g=11, img='gossip', sub='Phỏng đoán · Ý kiến', items=[
    ('イA ／ ナA そうです', 'trông có vẻ … (nhìn thấy)', ('初級1', 12, '❶', 'お弁当'), 'Hộp cơm đó trông ngon quá nhỉ.', '初級1・12'),
    ('Vそうです', 'có vẻ sắp …', ('初級1', 13, '❷', '10分'), 'Có vẻ khoảng 10 phút nữa là xong.', '初級1・13'),
    ('〜でしょう', 'có lẽ …', ('初級1', 4, '❹', '明日は晴れ'), 'Ngày mai có lẽ trời nắng.', '初級1・4'),
    ('〜かもしれません', 'không chừng …', ('初級2', 11, '❺', 'バッグ'), 'Không chừng tôi đã bị lấy mất túi rồi.', '初級2・11'),
    ('〜と思います', 'tôi nghĩ là …', ('初級1', 18, '❹', '10人ぐらい'), 'Tôi nghĩ khoảng 10 người.', '初級1・18'),
], say=(
    'Nhóm mười một: phỏng đoán. おいしそうです là "trông có vẻ ngon", nói khi nhìn thấy. Động từ cộng そうです là "có vẻ sắp". でしょう là "có lẽ", hay gặp trong dự báo thời tiết. かもしれません là "không chừng", chắc chắn ít hơn でしょう. と思います là "tôi nghĩ là".'))
add(kind='items', g=11, img='gossip', sub='Nghe nói · Giải thích', items=[
    ('Thể thông thường + そうです', 'nghe nói là …', ('初級1', 18, '❶', '誕生日だそう'), 'Nghe nói hôm nay là sinh nhật người đó.', '初級1・18'),
    ('〜と言っていました', '(ai đó) đã nói là …', ('初級1', 18, '❸', '焼き鳥'), 'Trước đây chị Ana có nói là rất thích yakitori.', '初級1・18'),
    ('〜んです', 'giải thích lý do, hoàn cảnh', ('初級1', 14, '❻', '国の友だち'), 'Bạn ở quê em từ Tokyo đến chơi ạ.', '初級1・14'),
    ('〜んですが…', 'trình bày vấn đề để nhờ giúp', ('初級1', 13, '❶', '窓が開かない'), 'Cửa sổ không mở được ạ…', '初級1・13'),
], say=(
    'Cẩn thận: そうです còn một nghĩa nữa là "nghe nói", khi đứng sau thể thông thường. おいしそう là trông ngon, còn おいしいそう là nghe nói ngon. Đề rất hay cho hai câu này đứng cạnh nhau. と言っていました là "ai đó đã nói". んです dùng để giải thích, và んですが dùng khi trình bày vấn đề để nhờ người khác giúp.'))

# 12. Cho · Nhận
add(kind='give', g=12, img='present', sub='Cho · Nhận đồ vật', items=[
    ('あげます', 'tôi cho người khác', ('初級1', 18, '❷', 'アナさんに何か'), 'Mình tặng chị Ana món quà gì đó không?', '初級1・18'),
    ('もらいます', 'tôi nhận từ người khác', ('初級1', 17, '❷', '父に時計'), 'Tôi nhận đồng hồ từ bố.', '初級1・17'),
    ('くれます', 'người khác cho tôi', ('初級1', 17, '❸', '兄がくれた'), 'Đây là bùa hộ mệnh anh trai tôi tặng.', '初級1・17'),
], say=(
    'Nhóm cuối: cho nhận. あげます là mình cho người khác. もらいます là mình nhận từ người khác, người cho đi với trợ từ に. くれます là người khác cho mình. Nhớ hướng mũi tên: hướng về phía mình thì dùng くれます.'))
add(kind='items', g=12, img='present', sub='Làm giúp ai đó', items=[
    ('Vてあげます', 'tôi làm V cho người khác', ('初級2', 18, '❸', '日本料理'), 'Tôi nấu món Nhật cho bạn bè.', '初級2・18'),
    ('Vてもらいます', 'tôi được ai đó làm V cho', ('初級2', 18, '❹', '写真を撮って'), 'Khi đi du lịch, tôi đã được bạn chụp ảnh cho.', '初級2・18'),
    ('Vてくれます', 'ai đó làm V cho tôi', ('初級2', 18, '❺', '迎えに来て'), 'Anh Yamada đã đến tận ga đón tôi.', '初級2・18'),
], say=(
    'Ba động từ này gắn sau thể て thì thành "làm giúp": てあげます là mình làm cho người khác, てもらいます là được người khác làm cho, てくれます là người khác làm cho mình. Hướng giống hệt phần đồ vật.'))

add(kind='outro', img='goukaku', say=(
    'Vậy là xong mười hai nhóm ngữ pháp JFT. Các bạn lưu video này lại, mỗi tối ôn một nhóm, '
    'rồi làm đề để thấy các mẫu này ra thi như thế nào. Đề thi thử có giải thích từng câu ở app Anh Trọng Dạy JFT, link ở trang cá nhân. '
    'Chúc các bạn thi đỗ!'))
