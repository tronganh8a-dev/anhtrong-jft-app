"""Thay các câu nghe không rõ / sai ở Đề 3–13 (21/11/2026, anh yêu cầu) bằng câu lấy NGẪU NHIÊN từ video "Ngân hàng đề thi nghe 1" anh gửi.
- 24 chỗ: 20 câu đơn + 2 cặp câu dùng chung 1 audio (Đề 4 câu 33–34 = cặp 宅配便, Đề 13 câu 29–30 = cặp 自転車店).
- Audio cắt từ video (lần phát hội thoại, bỏ tiếng chuông), chuẩn hoá ~-20 dBFS → app/media/jft/au/nb1_LNN.mp3;
  ảnh phương án / ảnh tình huống cắt từ khung hình video, phóng to ESRGAN → app/media/jft/img/nb1_NN_k.jpg, nb1_NN_ctx.jpg.
- Script: bài いろどり 初級2 第14課 (14-02, 14-03, 14-04), 初級1 第15課 (15-15) theo sách; các bài khác soạn theo audio (đối chiếu 2 bộ nhận dạng giọng nói).
  Dịch + giải thích do Anh Trọng Dạy JFT soạn. Câu hỏi một số bài viết lại cho rõ người được hỏi (vd. câu Kim / Natalia / Suzuki).
- Câu gốc bị thay được lưu ở src/jft/nghe/bank1_replaced.json (chạy lại script không ghi đè bản lưu).
Cần /tmp/nb/out/img, /tmp/nb/out/au. Chạy: python3 src/jft/nghe/build_bank1.py rồi python3 src/build_data.py"""
import json, html, shutil, os, sys, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from furi import furi
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')) + '/'
IMG = 'app/media/jft/img/'; AU = 'app/media/jft/au/'
SRC = '/tmp/nb/out/'
if os.path.isdir(SRC):
    for f in os.listdir(SRC + 'img'): shutil.copy(SRC + 'img/' + f, REPO + 'public/' + IMG + f)
    for f in os.listdir(SRC + 'au'): shutil.copy(SRC + 'au/' + f, REPO + 'public/' + AU + f)

J = lambda t: furi(html.escape(t)).replace('\n', '<br>')
def EX(ans, script, dich, gt):
    vi = bool(re.search(r'[A-Za-zÀ-ỹ]', ans))
    s = '<div class="ans">Đáp án đúng: ' + (f'<span>{html.escape(ans)}</span>' if vi else f'<span class="jp">{J(ans)}</span>') + '</div>'
    s += f'<span class="lb">SCRIPT</span><div class="jp">{J(script)}</div>'
    s += f'<span class="lb">DỊCH</span><div>{html.escape(dich).replace(chr(10), "<br>")}</div><span class="lb">GIẢI THÍCH</span><div>{J(gt)}</div>'
    return s

Q = {}   # số cảnh trong video → câu hỏi (cặp: 'Na', 'Nb')
def L(k, q, vi, opts, a, ans, script, dich, gt, lead='', pics=0, ctx=False, au=None):
    """pics: số ảnh phương án (nb1_k_1..); opts '' = phương án chỉ có ảnh"""
    jq = (lead + '\n' if lead else '') + q
    t = f'<span class="jp">{J(jq)}</span><br><span class="vi-q">{html.escape(vi)}</span>'
    o = [{'t': J(x) if x else ''} for x in opts]
    if pics:
        for i, d in enumerate(o): d['img'] = IMG + f'nb1_{int(str(k).rstrip("ab")):02d}_{i + 1}.jpg'
    n = int(str(k).rstrip('ab'))
    Q[str(k)] = dict(s='聴解', ins='', gset=None, gimg=None, gau=None, t=t,
                     imgs=[IMG + f'nb1_{n:02d}_ctx.jpg'] if ctx else [], img=None,
                     au=AU + f'nb1_L{(au or n):02d}.mp3', o=o, a=[a - 1], ex=EX(ans, script, dich, gt))

P4 = ['', '', '', '']
# ---------- いろどり 初級2 第14課 ----------
S2 = ('店員：いらっしゃいませ。\n客：すみません、クリーニングをお願いします。\n店員：はい、こちらですね。ズボンが1点でよろしいですか？\n'
      '客：はい。あの、このズボン、ここが汚れてしまったんですが、きれいになりますか？\n店員：あー、けっこう大きなシミですねえ。こちらは何のシミですか？\n'
      '客：カレーです。\n店員：カレーのシミは、落ちにくいんですよ。シミ抜きをしますか？別料金ですが。\n客：シミ抜き……いくらですか？\n'
      '店員：クリーニング代込みで、1,500円になります。\n客：わかりました。じゃあ、それをお願いします。\n店員：お渡しまでに2週間ほどかかりますが、よろしいですか？\n客：はい、だいじょうぶです。')
L(2, 'いくらかかりますか。', 'Hết bao nhiêu tiền?', ['1,200円', '1,500円', '1,550円'], 2, '1,500円', S2,
  'Nhân viên: Xin mời quý khách. / Khách: Xin lỗi, tôi muốn giặt là. / Nhân viên: Vâng, cái này nhỉ. 1 chiếc quần phải không ạ? / Khách: Vâng. Chiếc quần này chỗ này bị bẩn, có sạch được không ạ? / Nhân viên: Vết khá to nhỉ. Vết gì vậy ạ? / Khách: Cà ri. / Nhân viên: Vết cà ri khó sạch lắm. Quý khách có tẩy vết không ạ? Tính phí riêng ạ. / Khách: Tẩy vết… bao nhiêu tiền ạ? / Nhân viên: Gồm cả phí giặt là 1.500 yên. / Khách: Vâng, vậy làm giúp tôi. / Nhân viên: Mất khoảng 2 tuần mới giao được, có được không ạ? / Khách: Vâng, được ạ.',
  '「クリーニング代込みで、1,500円になります」: 込み (こみ) = đã bao gồm → 1.500 yên là tổng cả phí giặt lẫn tẩy vết. 1,200円 và 1,550円 không xuất hiện trong bài, chỉ là số gần giống để thử tai nghe số. シミ抜き = tẩy vết bẩn; 別料金 (BIỆT LIỆU KIM) べつりょうきん = tính phí riêng; 汚れる (Ô) よごれる = bị bẩn. いろどり 初級2 第14課 (14-02).',
  lead='ズボンを持って、クリーニング店に来ました。', ctx=True)
S3 = ('客：すみません、自転車の空気を入れたいんですが……。\n店員：ああ、空気？　空気入れはそこに置いてあるよ。\n客：使ってもいいですか？\n店員：うん、自分で入れてくれる？\n'
      '客：はい……あれ、すみません。使い方が、よくわからないんですが……。空気が入らないんです。\n'
      '店員：どれどれ。ああ、空気を入れるときは、タイヤのキャップをはずさなきゃ。ここに、こうはさんで、あとは、空気を入れて、終わったらキャップをかぶせればいいよ。\n'
      '客：わかりました。……ありがとうございました。終わりました。いくらですか？\n店員：お金はいいよ。\n客：え、いいんですか？　ありがとうございます。\n店員：ついでに、油も差して行く？\n客：あ、はい。ありがとうございます。')
D3 = ('Khách: Xin lỗi, cháu muốn bơm hơi xe đạp… / Chủ tiệm: À, bơm hơi à? Cái bơm để ở đó đấy. / Khách: Cháu dùng được không ạ? / Chủ tiệm: Ừ, cháu tự bơm nhé? / '
      'Khách: Vâng… Ơ, xin lỗi, cháu không rõ cách dùng… Hơi không vào. / Chủ tiệm: Để xem. À, bơm thì phải tháo nắp van lốp ra. Kẹp vào đây thế này, rồi bơm, xong thì đậy nắp lại là được. / '
      'Khách: Cháu hiểu rồi. …Cảm ơn bác. Xong rồi ạ. Bao nhiêu tiền ạ? / Chủ tiệm: Không lấy tiền đâu. / Khách: Ơ, được ạ? Cảm ơn bác. / Chủ tiệm: Nhân tiện tra dầu luôn không? / Khách: À, vâng. Cảm ơn bác.')
L('3a', 'だれが自転車のくうきを入れましたか。', 'Ai đã bơm hơi xe đạp?', ['おきゃくさん', 'じてんしゃ店の人'], 1, 'おきゃくさん', S3, D3,
  'Chủ tiệm nói 「自分で入れてくれる？」 (cháu tự bơm nhé?) → khách tự bơm; chủ tiệm chỉ hướng dẫn cách dùng (キャップをはずさなきゃ = phải tháo nắp). 空気 (KHÔNG KHÍ) くうき = hơi, không khí; 空気入れ = cái bơm. いろどり 初級2 第14課 (14-03).',
  lead='自転車のくうきを入れるために、自転車店に来ました。', ctx=True, au=3)
L('3b', 'りょうきんはいくらでしたか。', 'Phí là bao nhiêu?', ['300円', 'むりょう'], 2, 'むりょう', S3, D3,
  'Khách hỏi いくらですか, chủ tiệm đáp 「お金はいいよ」 = không cần trả tiền → むりょう (無料 – VÔ LIỆU: miễn phí). Khách còn hỏi lại 「え、いいんですか？」 (ơ, được ạ?). Bài không nhắc số 300円. 料金 (LIỆU KIM) りょうきん = phí. いろどり 初級2 第14課 (14-03).',
  lead='自転車のくうきを入れるために、自転車店に来ました。', ctx=True, au=3)
S5 = ('客：すみません、宅配便を送りたいんですが……。\n店員：宅配便ですね。着払いと元払いは、どちらになりますか？\n客：え？　すみません、わかりません……。\n'
      '店員：元払いは、今ここでお金を払います。着払いは、受け取る人がお金を払います。\n客：あ、今お金を払います。\n店員：元払いですね。それでは、こちらの伝票をお書きください。\n'
      '客：……これでいいですか？\n店員：はい、お預かりします。お届けの日時の指定はありますか？　今からですと、明日10日の午前中が最も早いお届けになりますが。\n'
      '客：じゃあ、明日の夜でお願いします。\n店員：19時から21時でよろしいですか？\n客：はい。\n店員：それでは……料金、1,260円になります。')
D5 = ('Khách: Xin lỗi, tôi muốn gửi hàng chuyển phát… / Nhân viên: Chuyển phát nhé. Người nhận trả hay người gửi trả ạ? / Khách: Hả? Xin lỗi, tôi không hiểu… / '
      'Nhân viên: Người gửi trả (元払い) là trả tiền ngay ở đây. Người nhận trả (着払い) là người nhận hàng trả tiền. / Khách: À, tôi trả bây giờ. / Nhân viên: Người gửi trả nhé. Vậy xin điền phiếu gửi này. / '
      'Khách: …Thế này được chưa ạ? / Nhân viên: Vâng, tôi xin nhận. Có chỉ định ngày giờ giao không ạ? Gửi bây giờ thì sớm nhất là sáng mai, ngày 10. / '
      'Khách: Vậy giao tối mai giúp tôi. / Nhân viên: Từ 19 giờ đến 21 giờ được không ạ? / Khách: Vâng. / Nhân viên: Vậy phí là 1.260 yên ạ.')
L('5a', '着払いと元払いのどちらで送りましたか。', 'Đã gửi theo cách người nhận trả tiền hay người gửi trả tiền?', ['ちゃくばらい', 'もとばらい'], 2, 'もとばらい', S5, D5,
  'Nhân viên giải thích: 元払い = trả tiền ngay tại đây; 着払い = người nhận trả. Khách nói 「今お金を払います」, nhân viên xác nhận 「元払いですね」 → もとばらい. 着 (TRƯỚC – đến nơi) ちゃく, 元 (NGUYÊN) もと, 払う (PHẤT) はらう. いろどり 初級2 第14課 (14-04).',
  lead='宅配便で荷物を送るために、コンビニに来ました。', ctx=True, au=5)
L('5b', '荷物は、いつ届きますか。', 'Hàng khi nào đến nơi?', ['きょうの夜', 'あしたの夜', 'あさっての夜'], 2, 'あしたの夜', S5, D5,
  'Nhân viên nói sớm nhất là 「明日10日の午前中」 (sáng mai), nhưng khách chọn 「明日の夜でお願いします」, giao 19–21 giờ → あしたの夜. Đừng chọn theo mốc "sớm nhất" của nhân viên mà theo câu khách chốt. 届く (GIỚI) とどく = đến nơi; 日時の指定 (CHỈ ĐỊNH) = hẹn ngày giờ. いろどり 初級2 第14課 (14-04).',
  lead='宅配便で荷物を送るために、コンビニに来ました。', ctx=True, au=5)

# ---------- hội thoại ----------
L(7, '酒井さんは、結婚して、何が変わりましたか。', 'Anh Sakai kết hôn xong thì điều gì đã thay đổi?', P4, 4, 'Tranh 4 – về nhà sớm hơn trước',
  'A：酒井さん、失礼ですが、ご結婚のきっかけは？\n酒井：きっかけですか？　えっと、妻と私は同じ会社で働いてたんです。\nA：ああ、そうですか。\n'
  '酒井：ええ。会社のパーティーで初めて会って、それからデートするようになりました。\nA：んー、そうですか。結婚して、どうですか？\n'
  '酒井：そうですね……。前より早く家に帰るようになりました。前は外で食事をしていたんですが……。\nA：うちで一緒に夕食ですか。仲がよくていいですね。',
  'A: Anh Sakai, xin lỗi cho hỏi, cơ duyên kết hôn của anh là gì? / Sakai: Cơ duyên à? À, vợ tôi và tôi từng làm cùng công ty. / A: À, vậy à. / Sakai: Vâng. Lần đầu gặp nhau ở bữa tiệc công ty, sau đó bắt đầu hẹn hò. / A: Ừm. Kết hôn rồi thấy thế nào? / Sakai: Để xem… Tôi về nhà sớm hơn trước. Trước đây tôi hay ăn ở ngoài… / A: Giờ ăn tối cùng nhau ở nhà nhỉ. Hai vợ chồng tình cảm thật.',
  'Câu trả lời cho 結婚して、どうですか là 「前より早く家に帰るようになりました」: Vるようになりました = đã trở nên ~ (chỉ sự thay đổi), 前より = so với trước. Tranh 4 (đồng hồ + ngôi nhà) → về nhà sớm. Tranh 1 (học tiếng Thái), tranh 2 (đồng hồ báo thức + tờ báo), tranh 3 (chào hỏi) không được nhắc. きっかけ = cơ duyên, lý do bắt đầu. 結婚 (KẾT HÔN) けっこん.',
  pics=4)
L(9, 'さとうさんがその人のファンになったきっかけは何ですか。', 'Điều gì khiến chị Sato trở thành fan của người đó?', P4, 3, 'Tranh 3 – xem tháp Mặt Trời (太陽の塔)',
  'A：さとうさんは、岡本太郎について、よく知ってますね。太郎の作品、お好きですか？\nさとう：ええ。学生のとき、大阪で太陽の塔を見てから、今までファンです。\n'
  'A：ああ、太陽の塔は岡本太郎の作品ですか。\nさとう：そうです。太郎は絵もかいたし、本も書きました。亡くなるまで、いろいろな作品を作ってたんですよ。\nA：ふーん、すごい芸術家ですね。',
  'A: Chị Sato biết nhiều về Okamoto Taro nhỉ. Chị thích tác phẩm của ông ấy à? / Sato: Vâng. Từ hồi sinh viên xem tháp Mặt Trời ở Osaka, đến giờ tôi vẫn là fan. / A: À, tháp Mặt Trời là tác phẩm của Okamoto Taro à? / Sato: Đúng vậy. Ông ấy vừa vẽ tranh vừa viết sách. Đến lúc mất vẫn sáng tác rất nhiều tác phẩm. / A: Ồ, đúng là nghệ sĩ tài ba.',
  '「大阪で太陽の塔を見てから、今までファンです」: Vてから = từ sau khi ~ → việc xem tháp là cơ duyên → tranh 3. 本も書きました là ông Taro viết sách, không phải chị Sato đọc sách (tranh 2). Tranh 1 (xem TV), tranh 4 (nghe nhạc) không được nhắc. 塔 (THÁP) とう, 作品 (TÁC PHẨM) さくひん, 芸術家 (NGHỆ THUẬT GIA) げいじゅつか = nghệ sĩ.',
  pics=4)
L(10, 'ナターリアさんが日本語の勉強を始めたきっかけは何ですか。', 'Điều gì khiến chị Natalia bắt đầu học tiếng Nhật?', P4, 2, 'Tranh 2 – tập judo',
  'A：ナターリアさんは、どうして日本語の勉強を始めたんですか？\nナターリア：私、中学校のときから柔道を習ってるんです。\nA：柔道！　そのとき、日本語、できましたか？\n'
  'ナターリア：いいえ。でも、柔道のとき、日本語を使います。「一本」とか「技あり」とか。\nA：え、そうなんですか。それで日本語に興味を持ったんですね。\n'
  'ナターリア：そうです。ちょっと話せるようになったので、日本に行って、日本語を使ってみたいです。',
  'A: Sao chị Natalia lại bắt đầu học tiếng Nhật? / Natalia: Tôi tập judo từ hồi cấp hai. / A: Judo! Lúc đó chị biết tiếng Nhật không? / Natalia: Không. Nhưng khi tập judo thì dùng tiếng Nhật, như "ippon", "waza-ari". / A: Ồ, ra vậy. Thế là chị bắt đầu quan tâm đến tiếng Nhật nhỉ. / Natalia: Đúng vậy. Giờ tôi nói được một chút rồi nên muốn sang Nhật dùng thử tiếng Nhật.',
  '「中学校のときから柔道を習ってるんです」「柔道のとき、日本語を使います」 → nhờ judo mà quan tâm tiếng Nhật (日本語に興味を持った) → tranh 2. 一本 (いっぽん), 技あり (わざあり) là thuật ngữ tính điểm trong judo. 柔道 (NHU ĐẠO) じゅうどう, 興味 (HỨNG VỊ) きょうみ = hứng thú, quan tâm. Các tranh khác không được nhắc.',
  pics=4)
L(12, 'このバッグは、前は何でしたか。', 'Chiếc túi này trước đây là gì?', P4, 1, 'Tranh 1 – cà vạt',
  'A：ワンさん、こっちのバッグは何だったと思いますか？\nワン：うーん……ネクタイですね？\nA：そうです。使わなくなったネクタイを、妻がバッグにしたんです。\nワン：へえ、おしゃれですね。',
  'A: Anh Wang, anh nghĩ chiếc túi này trước đây là gì? / Wang: Ừm… cà vạt nhỉ? / A: Đúng vậy. Vợ tôi lấy mấy chiếc cà vạt không dùng nữa làm thành túi. / Wang: Ồ, sành điệu thật.',
  '「使わなくなったネクタイを、妻がバッグにしたんです」: AをBにする = biến A thành B → túi làm từ cà vạt cũ → tranh 1. 何だったと思いますか = anh nghĩ (trước đây) nó là gì? 使わなくなった = không dùng nữa. Chăn (tranh 2), ô (tranh 3), kimono (tranh 4) không được nhắc.',
  pics=4, ctx=True)
L(13, 'ワンさんとよしださんは何について話していますか。', 'Wang và Yoshida đang nói về cái gì?', P4, 4, 'Tranh 4 – cái gối tựa (クッション)',
  'ワン：そのクッション、かわいいですね。\nよしだ：これは、妻が子どもの布団をクッションにしたんです。\nワン：そうですか。前は布団ですか。\nよしだ：ええ。使わなくなったので、クッションにしたんです。',
  'Wang: Cái gối tựa đó dễ thương nhỉ. / Yoshida: Cái này vợ tôi làm từ chăn của con. / Wang: Vậy à. Trước đây là chăn à? / Yoshida: Vâng. Vì không dùng nữa nên làm thành gối tựa.',
  'Câu đầu 「そのクッション、かわいいですね」 nói luôn chủ đề → tranh 4. 布団 (BỐ ĐOÀN) ふとん = chăn đệm là đồ cũ trước khi làm gối, không phải thứ hai người đang xem. Tranh 2 là chiếc túi làm từ cà vạt (chuyện khác). 子ども (TỬ) = con.',
  pics=4)
L(14, 'すずきさんは、子どもの靴がはけなくなったら、どうしますか。', 'Khi con không đi vừa giày nữa, chị Suzuki làm gì?', P4, 1, 'Tranh 1 – đem cho bạn',
  'A：すずきさん、子どもが大きくなって、靴がはけなくなったら、どうしますか？\nすずき：子どもの靴？　私は、近くに住んでる友だちにあげます。\n'
  'A：ああ、友だちに。その友だちにもお子さんがいるんですか？\nすずき：ええ、そうです。\nA：それはいいですね。',
  'A: Chị Suzuki, khi con lớn lên không đi vừa giày nữa thì chị làm gì? / Suzuki: Giày của con à? Tôi đem cho người bạn sống gần nhà. / A: À, cho bạn. Người bạn đó cũng có con à? / Suzuki: Vâng, đúng vậy. / A: Thế thì hay quá.',
  '「近くに住んでる友だちにあげます」 → đem cho bạn → tranh 1. はけなくなる = không đi (giày) được nữa; 靴を履く (LÍ) はく = đi giày. あげる = cho, tặng. Bán ở chợ đồ cũ (tranh 3) hay mang ra cửa hàng cho thuê (tranh 4 – レンタルショップ) không được nhắc.',
  pics=4)
L(16, 'キムさんは、どんなエコ活動をしていますか。', 'Chị Kim đang làm hoạt động bảo vệ môi trường nào?', ['', '', '', '', ''], 4, 'Tranh 4 – không đổ dầu ăn xuống bồn rửa',
  'ワン：キムさん、どんなエコ活動をしていますか？\nキム：エコですか？　そうですね。私は、料理をするとき、台所から油を流さないようにしてますよ。\n'
  'ワン：え、じゃあ、どうやって油を捨てるんですか？\nキム：新聞紙といっしょに袋に入れて捨てます。\nワン：ああ、いい考えですね。私もこれからそうします。',
  'Wang: Chị Kim làm hoạt động bảo vệ môi trường gì? / Kim: Bảo vệ môi trường à? Để xem. Khi nấu ăn, tôi cố gắng không đổ dầu xuống bồn rửa bếp. / Wang: Ơ, vậy chị bỏ dầu thế nào? / Kim: Cho vào túi cùng với giấy báo rồi vứt. / Wang: À, ý hay đấy. Từ giờ tôi cũng làm vậy.',
  '「台所から油を流さないようにしてます」: Vないようにしている = cố gắng không ~ (thói quen). Dầu thấm vào giấy báo rồi bỏ vào túi → tranh 4. 油 (DU) あぶら = dầu, 流す (LƯU) ながす = đổ, xả, 新聞紙 (TÂN VĂN CHỈ) しんぶんし = giấy báo. エコ活動 (HOẠT ĐỘNG) = hoạt động bảo vệ môi trường. Các tranh khác không được nhắc.',
  pics=5)
L(17, '部屋はどうなっていますか。', 'Căn phòng đang ở tình trạng thế nào?', P4, 2, 'Tranh 2 – điều hoà bật, cửa ra vào để mở',
  'A：この部屋、ちょっと暑いですね。\nB：エアコン、ついてます？\nA：ええ、ついてます。\nB：あ、でも、ドアが開いたままですよ。\nA：ああ、開いたままですね。\nB：私が閉めます。\nA：あ、ありがとう。',
  'A: Phòng này hơi nóng nhỉ. / B: Điều hoà có bật không? / A: Có, đang bật. / B: À, nhưng cửa vẫn để mở kìa. / A: À, vẫn để mở nhỉ. / B: Để tôi đóng. / A: À, cảm ơn.',
  'エアコンがついている = điều hoà đang bật; 「ドアが開いたまま」: Vたまま = để nguyên trạng thái (cửa cứ để mở) → điều hoà bật mà cửa mở, khí mát thoát ra ngoài → tranh 2. Tranh 1, 3, 4 cửa ra vào đều đóng (tranh 4 là cửa sổ mở). 開く (KHAI) あく = mở, 閉める (BẾ) しめる = đóng.',
  pics=4)
L(18, '二人は、どのサインについて話していますか。', 'Hai người đang nói về biển báo nào?', ['', '', '', '', ''], 1, 'Tranh 1 – cấm chụp ảnh có đèn flash',
  'A：これ、すばらしい絵ですね。写真、撮ってもいいですか？\nB：たぶん大丈夫だと思いますけど……。でも、あそこに「フラッシュ撮影禁止」って書いてありますね。\n'
  'A：フラッシュ、使っちゃだめですか？\nB：ええ。写真は大丈夫ですが、フラッシュは使わないでくださいね。\nA：はい、わかりました。では……。',
  'A: Bức tranh tuyệt quá nhỉ. Tôi chụp ảnh được không? / B: Chắc là được… Nhưng chỗ kia có ghi "Cấm chụp ảnh dùng đèn flash". / A: Không được dùng flash à? / B: Vâng. Chụp ảnh thì được nhưng đừng dùng flash nhé. / A: Vâng, tôi hiểu rồi.',
  '「フラッシュ撮影禁止」 = cấm chụp có đèn flash: chụp ảnh vẫn được, chỉ không được dùng flash → tranh 1. Tranh 2 撮影禁止 (cấm chụp hẳn) sai vì B nói 写真は大丈夫. Tranh 3 cấm dùng điện thoại, tranh 4 cấm ăn uống, tranh 5 không được chạm. 撮影 (TOÁT ẢNH) さつえい, 禁止 (CẤM CHỈ) きんし; 使っちゃだめ = 使ってはだめ.',
  pics=5)
L(20, '二人は何について話していますか。', 'Hai người đang nói về cái gì?', P4, 2, 'Tranh 2 – quán cà phê trong ngôi nhà kiểu truyền thống',
  'A：ああ、小川さん、ちょっと待って。\n小川：ん？\nA：ここ、外から見ると伝統的な家ですが、中はモダンなカフェなんですよ。\n'
  '小川：え？　じゃあ、この家はカフェなんですか？\nA：はい。最近テレビで紹介されてました。\n小川：ちょっと入ってみてもいいですか？\nA：ええ、いいですよ。入ってみましょう。',
  'A: À, anh Ogawa, chờ chút. / Ogawa: Hả? / A: Chỗ này nhìn từ ngoài là nhà kiểu truyền thống, nhưng bên trong là quán cà phê hiện đại đấy. / Ogawa: Ơ? Vậy ngôi nhà này là quán cà phê à? / A: Vâng. Gần đây được giới thiệu trên TV. / Ogawa: Vào thử một chút được không? / A: Được chứ. Vào thử đi.',
  '「外から見ると伝統的な家ですが、中はモダンなカフェ」 → nhà cổ bên ngoài, bên trong là quán cà phê → tranh 2 (ngôi nhà cổ + tách cà phê, bánh). 伝統的 (TRUYỀN THỐNG ĐÍCH) でんとうてき = truyền thống; 紹介 (THIỆU GIỚI) しょうかい = giới thiệu. Các tranh khác không có quán cà phê.',
  pics=4)
L(22, '二人は何を見て話していますか。', 'Hai người đang xem gì và nói chuyện?', ['', '', '', '', '', '', ''], 2, 'Tranh 2 – chiếc áo (陣羽織) làm từ thảm Ba Tư',
  'A：小川さん、これ、日本の服ですか？\n小川：え？　これですか？　ああ、これはペルシャのじゅうたんですよ。豊臣秀吉が戦争のときに着るために、ペルシャのじゅうたんで作ったそうです。\n'
  'A：その人、有名な人ですか？\n小川：ええ、歴史的にとても有名な人ですよ。\nA：そうですか。でも、どうしてペルシャのものが日本に来たんですか？\n'
  '小川：うーん……16世紀にポルトガルの船で運ばれたそうです。\nA：へえ、そうですか。おもしろいですね。',
  'A: Anh Ogawa, đây là quần áo Nhật à? / Ogawa: Hả? Cái này à? À, đây là thảm Ba Tư đấy. Nghe nói Toyotomi Hideyoshi đã cho làm từ thảm Ba Tư để mặc khi ra trận. / A: Người đó nổi tiếng à? / Ogawa: Vâng, về mặt lịch sử là người rất nổi tiếng. / A: Vậy à. Nhưng sao đồ Ba Tư lại đến Nhật? / Ogawa: Ừm… nghe nói được chở bằng tàu Bồ Đào Nha vào thế kỷ 16. / A: Ồ, thú vị thật.',
  '「日本の服ですか？」「秀吉が戦争のときに着るために…作った」 → thứ họ đang xem là một chiếc áo (陣羽織 – じんばおり, áo khoác mặc ngoài khi ra trận) làm từ thảm Ba Tư → tranh 2. じゅうたん = thảm; 〜そうです = nghe nói; 運ばれた = được chở đến (thể bị động). Các tranh khác là tranh vẽ, đồ vật, kiếm… không phải quần áo. 戦争 (CHIẾN TRANH) せんそう.',
  pics=7)
L(24, 'AモデルとBモデルのどちらを買いますか。', 'Người hỏi sẽ mua mẫu A hay mẫu B?', ['Aモデル', 'Bモデル'], 2, 'Bモデル',
  'A：ジョイさん、新しい音楽プレーヤーは、AとB、どっちがいいですか？\nジョイ：うーん……。\nA：デザインは、どっちがいいと思いますか？\n'
  'ジョイ：Aモデルのほうがいいですよ。Aのほうがかっこいいし、おしゃれです。\nA：じゃあ、どっちが早く届きますか？\nジョイ：それはBモデルです。Bのほうが早く届きますよ。\n'
  'A：そうですか。じゃあ、早くほしいので、Bモデルにします。',
  'A: Joy ơi, máy nghe nhạc mới thì mẫu A hay B tốt hơn? / Joy: Ừm… / A: Về thiết kế thì bạn thấy cái nào đẹp hơn? / Joy: Mẫu A đẹp hơn. Mẫu A vừa ngầu vừa sành điệu. / A: Vậy cái nào giao nhanh hơn? / Joy: Cái đó thì mẫu B. Mẫu B giao nhanh hơn. / A: Vậy à. Vậy tôi muốn có sớm nên chọn mẫu B.',
  'Joy khen thiết kế mẫu A (かっこいいし、おしゃれ), nhưng mẫu B giao nhanh hơn; người mua chốt 「早くほしいので、Bモデルにします」 → B. 〜にします = quyết định chọn ~. 届く (GIỚI) とどく = được giao đến. Dễ chọn nhầm A vì nghe khen A trước – phải nghe đến câu chốt cuối.',
  pics=2)
L(27, '二人は何について話していますか。', 'Taylor và bạn sẽ cùng đi chơi. Hai người đang nói về cái gì?', ['', '', '', '', '', '', ''], 4, 'Tranh 4 – tháp Tokyo Skytree',
  'A：あのう、もう東京スカイツリー、見ましたか？\nB：スカイツリー？\nA：あ、高いタワーです。世界一ですよ。\nB：ああ、タワー。いえ、まだです。\nA：じゃあ、見に行きませんか？　夜景がきれいですよ。\nB：いいですね。行きましょう。',
  'A: Này, bạn đã xem Tokyo Skytree chưa? / B: Skytree? / A: À, là một tòa tháp cao. Cao nhất thế giới đấy. / B: À, tháp. Chưa, tôi chưa xem. / A: Vậy đi xem không? Cảnh đêm đẹp lắm. / B: Hay đấy. Đi thôi.',
  '「東京スカイツリー」「高いタワーです。世界一ですよ」 → tranh 4. Tranh 7 cũng là cảnh thành phố về đêm nhưng không có tháp. 夜景 (DẠ CẢNH) やけい = cảnh đêm; 見に行きませんか = đi xem không? (Vませんか: rủ rê); 世界一 (THẾ GIỚI NHẤT) = nhất thế giới.',
  lead='タイラーさんと友だちは、いっしょに出かけます。', pics=7)
L(28, 'タイラーさんとあべさんは、何時に会いますか。', 'Taylor đi chơi với bạn vào thứ Bảy và Chủ nhật. Taylor và Abe gặp nhau lúc mấy giờ?', ['にちようび　10:10', 'にちようび　10:20', 'にちようび　10:00'], 3, 'にちようび　10:00',
  'タイラー：あべさん、日曜日、待ち合わせはどうしますか？\nあべ：そうですね……。10時にホテルのロビーはどうですか？\nタイラー：10時にホテルのロビーですね。わかりました。\nあべ：じゃあ、また日曜日に。\nタイラー：じゃあ、また。',
  'Taylor: Chị Abe, Chủ nhật mình hẹn gặp thế nào? / Abe: Để xem… 10 giờ ở sảnh khách sạn được không? / Taylor: 10 giờ ở sảnh khách sạn nhỉ. Tôi hiểu rồi. / Abe: Vậy hẹn Chủ nhật nhé. / Taylor: Ừ, hẹn gặp lại.',
  '「10時にホテルのロビー」: chỉ nói 10時 (じゅうじ), không có 分 → đúng 10:00. 10時10分 (じゅっぷん), 10時20分 (にじゅっぷん) không xuất hiện. 待ち合わせ (ĐÃI HỢP) まちあわせ = hẹn gặp nhau; 〜はどうですか = ~ thì thế nào (đề xuất).',
  lead='タイラーさんは、土曜日と日曜日に友だちと出かけます。')
L(29, 'タイラーさんは何をしたいですか。', 'Taylor và Abe đang đi dạo trong phố. Taylor muốn làm gì?', P4, 2, 'Tranh 2 – mua quà lưu niệm',
  'タイラー：あのう、すみません。ちょっと、お土産を買いたいんですが……。\nあべ：お土産ですか？　えーと、じゃあ、食事の前に店に行きましょう。\nタイラー：食事の前？　時間、大丈夫ですか？\nあべ：ええ、大丈夫です。',
  'Taylor: À, xin lỗi. Tôi muốn mua chút quà lưu niệm… / Abe: Quà lưu niệm à? Ừm, vậy mình đi cửa hàng trước khi ăn nhé. / Taylor: Trước khi ăn? Có kịp giờ không? / Abe: Vâng, không sao.',
  '「お土産を買いたいんですが」 → muốn mua quà lưu niệm → tranh 2 (cửa hàng áo thun in chữ Hán, đồ lưu niệm). Vたいんですが = muốn ~ (cách mở lời nhờ vả). お土産 (THỔ SẢN) おみやげ. Tranh 1 (nước uống), 3 (quầy đổi tiền), 4 (sách hướng dẫn) không được nhắc.',
  lead='タイラーさんとあべさんは、町を歩いています。', pics=4)
L(30, 'アニサさんが遅くなる理由は何ですか。', 'Lý do chị Anisa đến muộn là gì?', ['a. 財布を忘れた', 'b. 病院に行く', 'c. 熱がある'], 1, 'a. 財布を忘れた',
  '会社の人：はい、北浦和フーズです。\nアニサ：もしもし、あのう、アニサです。\n会社の人：ああ、アニサさん。\nアニサ：すみません。家に財布を忘れました。これから取りに帰ります。それで、少し遅れます。\n'
  '会社の人：ああ、わかりました。\n（会社で）\nアニサ：おはようございます。遅くなって申し訳ありません。',
  'Người ở công ty: Vâng, công ty Kitaurawa Foods xin nghe. / Anisa: A lô, em là Anisa ạ. / Người ở công ty: À, Anisa. / Anisa: Xin lỗi, em quên ví ở nhà. Giờ em về lấy. Vì vậy em sẽ đến muộn một chút. / Người ở công ty: À, tôi hiểu rồi. / (Ở công ty) Anisa: Chào buổi sáng. Em xin lỗi vì đến muộn.',
  '「家に財布を忘れました。これから取りに帰ります。それで、少し遅れます」 → a. それで = vì vậy (nối lý do → kết quả); 取りに帰る = về lấy. Bài không nhắc bệnh viện hay bị sốt. 財布 (TÀI BỐ) さいふ = ví, 忘れる (VONG) わすれる = quên, 遅れる (TRÌ) おくれる = muộn; 申し訳ありません = xin lỗi (rất lịch sự).',
  pics=3)
L(32, '男の人はどんなことをお願いしましたか。', 'Người đàn ông thỉnh thoảng không hiểu tiếng Nhật. Anh ấy đã nhờ việc gì?', P4, 4, 'Tranh 4 – nhờ chỉ cách dùng từ điển điện tử',
  '男：あのう、ちょっといいですか？\n女：はい、何ですか？\n男：あのう、この電子辞書の使い方、教えてくださいませんか？\n女：電子辞書ねえ……。うーん、私もよくわかりません。すみません。\n男：あ、そうですか。',
  'Nam: À, cho tôi hỏi chút được không? / Nữ: Vâng, gì vậy? / Nam: À, chị chỉ giúp tôi cách dùng từ điển điện tử này được không? / Nữ: Từ điển điện tử à… Ừm, tôi cũng không rành lắm. Xin lỗi nhé. / Nam: À, vậy à.',
  '「この電子辞書の使い方、教えてくださいませんか」: Vてくださいませんか = nhờ một cách lịch sự → tranh 4. Người phụ nữ cũng không biết, nhưng câu hỏi là anh ấy ĐÃ NHỜ việc gì. Tranh 3 (nhờ nói chậm) không được nhắc. 電子辞書 (ĐIỆN TỬ TỪ THƯ) でんしじしょ, 使い方 = cách dùng.',
  lead='男の人は、ときどき日本語がわかりません。', pics=4)
L(35, 'アリさんは国際交流祭りに行きたいですが、困っています。どうして困っていますか。', 'Ali muốn đi lễ hội giao lưu quốc tế nhưng đang gặp khó khăn. Vì sao?', P4, 3, 'Tranh 3 – không biết cách mua vé ở máy bán vé',
  'A：どうしたんですか？\nアリ：あのう……切符の買い方が、よくわかりません。\nA：手伝いましょうか？\nアリ：すみません。えっと、代々木まで行きます。\nA：代々木ですか。まず、お金を入れて……。',
  'A: Anh sao vậy? / Ali: À… tôi không rõ cách mua vé. / A: Để tôi giúp nhé? / Ali: Cảm ơn chị. À, tôi đi đến Yoyogi. / A: Yoyogi à. Trước tiên cho tiền vào…',
  '「切符の買い方が、よくわかりません」 → không biết mua vé → tranh 3 (máy bán vé). Vましょうか = để tôi ~ nhé (đề nghị giúp). 代々木 (よよぎ) là tên ga. Tranh 1 (sân ga), 2 (xem bản đồ, lạc đường), 4 (không hiểu lời nói) không đúng. 切符 (THIẾT PHÙ) きっぷ = vé; 国際交流 (QUỐC TẾ GIAO LƯU).',
  lead='町で困っている旅行者を見かけたので、助けてあげます。', pics=4)
L(37, '何の薬ですか。', 'Đây là thuốc gì?', ['a. 熱を下げる', 'b. せきを抑える', 'c. 痛み止め', 'd. くしゃみ、鼻水を抑える'], 4, 'd. くしゃみ、鼻水を抑える',
  'A：これは、アレルギーの薬です。くしゃみや鼻水を抑えます。\nB：はい。\nA：1日1回、寝る前に飲んでください。\nB：わかりました。',
  'A: Đây là thuốc dị ứng. Giảm hắt hơi, sổ mũi. / B: Vâng. / A: Ngày 1 lần, uống trước khi ngủ. / B: Tôi hiểu rồi.',
  '「アレルギーの薬です。くしゃみや鼻水を抑えます」 → d. 抑える (ỨC) おさえる = làm dịu, kìm lại; 鼻水 (TỊ THUỶ) はなみず = nước mũi. a 熱を下げる = hạ sốt, b せき = ho, c 痛み止め (THỐNG) = thuốc giảm đau. いろどり 初級1 第15課 (15-15).',
  pics=4)

# ---------- chỗ thay (chọn ngẫu nhiên, random.Random(30), không để 2 câu cùng chủ đề vào 1 đề) ----------
SLOTS = {'jft-f3': {38: '22', 39: '13'}, 'jft-f4': {28: '10', 33: '5a', 34: '5b', 35: '24', 36: '29'},
         'jft-f5': {28: '35', 33: '12', 35: '28'}, 'jft-f6': {34: '16', 35: '7'}, 'jft-f7': {25: '9'},
         'jft-f8': {25: '20', 26: '27'}, 'jft-f9': {26: '30'}, 'jft-f10': {26: '37', 29: '17', 31: '14', 33: '2'},
         'jft-f13': {26: '18', 29: '3a', 30: '3b', 31: '32'}}
assert sorted(v for d in SLOTS.values() for v in d.values()) == sorted(Q), 'mỗi câu dùng đúng 1 lần'
BK = REPO + 'src/jft/nghe/bank1_replaced.json'
E = json.load(open(REPO + 'src/raw/jft_exams.json'))
bk = json.load(open(BK)) if os.path.exists(BK) else {}
for e in E:
    for n, k in SLOTS.get(e['id'], {}).items():
        key = f"{e['id']}#{n}"
        old = e['qs'][n - 1]
        if key not in bk:
            assert old['s'] == '聴解' and 'nb1_' not in (old.get('au') or ''), key
            bk[key] = old
        e['qs'][n - 1] = Q[k]
json.dump(bk, open(BK, 'w'), ensure_ascii=False, indent=1)
json.dump(E, open(REPO + 'src/raw/jft_exams.json', 'w'), ensure_ascii=False, indent=1)
for eid, d in SLOTS.items():
    print(eid, ', '.join(f'câu {n} ← cảnh {k}' for n, k in d.items()))
