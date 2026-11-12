import json,re,html,sys
sys.path.insert(0,'/home/claude/anhtrong-jft-app/src/jft')
from furi import furi
R='/home/claude/anhtrong-jft-app/'
T=open(R+'public/tailieu/Buoi10_KinhNgu.html').read()
LOGO=re.search(r'<img class="lg" src="([^"]+)"',T).group(1)
HEAD=T[:T.index('</style>')]+'''
.st{visibility:hidden;opacity:0;transform:translateY(8px);transition:opacity .35s,transform .35s}.st.sh{visibility:visible;opacity:1;transform:none}
#ann{position:fixed;inset:0;z-index:8;pointer-events:none}.ntx,.nmm{position:absolute;pointer-events:auto;outline:none;font-family:"Klee One","M PLUS Rounded 1c",Quicksand,sans-serif;font-weight:600}
.ntx{color:#e0245e;font-size:34px;min-width:20px;padding:2px 6px;border:2px dashed transparent}.ntx:focus{border-color:#e0245e88}
.nmm{background:#fff3a6;color:#0d2b40;font-size:26px;min-width:180px;min-height:70px;padding:14px 16px 12px;border-radius:6px;box-shadow:0 8px 20px #0d2b4040;transform:rotate(-1.5deg)}.nmm .gr{position:absolute;left:0;right:0;top:0;height:12px;cursor:move;background:#f2d95c;border-radius:6px 6px 0 0}.nmm .tx{outline:none;min-height:40px}.nmm .xx{position:absolute;right:4px;top:-2px;font-size:16px;cursor:pointer;color:#8a6d1a}
body.m-text #pen,body.m-memo #pen{pointer-events:auto;cursor:text}#bar button.on{background:#c42f66}#bar button{white-space:nowrap}
.src{font-size:22px;color:#6b8296;margin-left:12px;font-weight:600}.q u{text-decoration:none;border-bottom:4px solid #c42f66}
.pt{display:grid;grid-template-columns:1fr 1fr;gap:26px;flex:1;align-content:start}.pt .fm{grid-column:1/-1;background:#fff;border-radius:20px;padding:20px 28px;box-shadow:0 8px 24px #0d2b4012;display:flex;flex-wrap:wrap;gap:14px 26px;align-items:center}
.fm .f{font-family:"Klee One","M PLUS Rounded 1c",sans-serif;font-size:36px;font-weight:600;background:#fdeef4;color:#c42f66;border-radius:12px;padding:6px 18px}.fm .m{font-size:26px;color:#33495a}
.exs{background:#fff;border-radius:20px;padding:18px 26px;box-shadow:0 8px 24px #0d2b4012}.exs h4{font-size:22px;color:#0d5a8c;margin:0 0 6px;letter-spacing:1px}.exs .e{margin:10px 0 14px}.exs .j{font-family:"Klee One","M PLUS Rounded 1c",sans-serif;font-size:30px;line-height:1.6}.exs .j b{color:#c42f66}.exs .v{font-size:22px;color:#6b8296}.exs rt{font-size:.45em}
.pb{background:#fff8e6;border-left:8px solid #f2a93b;border-radius:14px;padding:16px 24px;font-size:25px;line-height:1.55}.pb b{color:#c42f66}.pb rt{font-size:.45em}.pb .jp{font-size:27px}
.ov{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.ov div{background:#fff;border-radius:14px;padding:12px 18px;font-size:23px;box-shadow:0 4px 14px #0d2b400d}.ov b{color:#c42f66;margin-right:8px}.ov .jp{font-size:25px}
.sum{width:100%;border-collapse:collapse;font-size:28px}.sum td{padding:14px 18px;border-bottom:1px solid #dbe4ec}.sum td.k{font-family:"Klee One",serif;font-size:32px;white-space:nowrap;color:#0d5a8c;font-weight:600}.sum tr:nth-child(odd) td{background:#fff}
</style></head><body><div id="stage">'''
TAIL=open(R+'src/tailieu_src/buoi15_tail.html').read()
F=lambda s: furi(html.escape(s)).replace('\n','<br>')
def FB(s):  # **x** → <b>
    parts=re.split(r'\*\*(.+?)\*\*',s);return ''.join(F(p) if i%2==0 else '<b>'+F(p)+'</b>' for i,p in enumerate(parts))
CR='<div class="cr">Ngữ pháp trọng tâm JFT-Basic · Anh Trọng Dạy JFT · giải thích và câu ví dụ tự soạn; câu luyện tập lấy từ bộ đề trong app (ghi nguồn) hoặc tự soạn</div>'
GQ=json.load(open('/tmp/kj/gq.json'))
S=[];NQ=[0];OV=[]
S.append(f'<section class="slide dark"><div class="cover"><img class="lg" src="{LOGO}"><div class="kk">Ngữ pháp · 文法 · JFT-Basic</div><h1>Ngữ pháp trọng tâm<br><span>hay ra trong đề JFT</span></h1><p class="jp">会話と表現 — よく出る文型</p></div>{CR}</section>')
OVI=len(S);S.append(None)
def pat(no,title,forms,exs,note):
    OV.append((no,title))
    fm=''.join(f'<span class="f">{F(f)}</span><span class="m">{html.escape(m)}</span>' for f,m in forms)
    ex=''.join(f'<div class="e st"><div class="j">{FB(j)}</div><div class="v">{html.escape(v)}</div></div>' for j,v in exs)
    S.append(f'<section class="slide"><h2>{no}. <span class="jp">{F(title)}</span></h2><div class="pt"><div class="fm">{fm}</div><div class="exs"><h4>VÍ DỤ</h4>{ex}</div><div class="pb st">{note}</div></div>{CR}</section>')
def quiz(qhtml,opts,a,expl,src):
    NQ[0]+=1;ks='①②③④'
    ob=''.join(f'<button class="o" data-k="{ks[i]}"><b>{ks[i]}</b><span class="jp ot">{o}</span><i></i><em></em></button>' for i,o in enumerate(opts))
    S.append(f'<section class="slide qz"><div class="kk2">Luyện tập {NQ[0]} <span class="src">{src}</span></div><h2 class="jp q">{qhtml}</h2><div class="opts list" data-a="{ks[a]}">{ob}</div><div class="ex"><b>Đáp án: {ks[a]} {opts[a]}</b> — {expl}</div>{CR}</section>')
def eq(de,i,expl):
    x=next(g for g in GQ if g['de']==de and g['i']==i)
    opts=[re.sub(r'^\s*[a-d]\.\s*','',o) for o in x['o']]
    t=re.sub(r'(\s|&nbsp;){3,}','　　',x['t']).replace('①','')
    quiz(t,opts,x['a'],expl,f'Nguồn: Đề {de} · câu {i}')
def sq(t,opts,a,expl): quiz(F(t),[F(o) for o in opts],a,expl,'Câu tự soạn')
N=lambda s:s  # plain note helper
def NT(s): # note with 「jp」 furigana
    return re.sub(r'「([^」]+)」',lambda m:'「<span class="jp">'+furi(m.group(1))+'</span>」',s)

pat(1,'〜てもらえませんか・〜ましょうか・〜てもいいですか',[('Vてもらえませんか','nhờ người khác làm cho mình'),('Vましょうか','mình đề nghị làm giúp'),('Vてもいいですか','xin phép mình làm')],
 [('すみません、もう一度**説明してもらえませんか**。','Xin lỗi, anh giải thích lại một lần nữa được không?'),('重そうですね。**持ちましょうか**。','Trông nặng nhỉ. Để tôi xách giúp nhé?'),('窓を**開けてもいいですか**。','Tôi mở cửa sổ được không?')],
 NT('Nhìn câu trả lời của người kia: 「いいですよ」 → A nhờ (<b>〜てもらえませんか</b>) · 「お願いします」「大丈夫です」 → A đề nghị giúp (<b>〜ましょうか</b>) · 「どうぞ」 → A xin phép (<b>〜てもいいですか</b>).'))
eq(1,18,'B trả lời 「いいですよ」 → A nhờ B kiểm tra giúp → チェックしてもらえませんか. 〜ましょうか là A tự làm giúp B, sai.')
eq(26,19,'A thấy B xách nặng, muốn giúp → 手伝いましょうか. B đáp 「だいじょうぶです。ありがとう」 = từ chối lời đề nghị giúp.')
eq(2,14,'A đề nghị mang tờ rơi đến giúp, B đáp 「じゃあ、おねがいします」 → 行きましょうか (mình làm giúp).')
pat(2,'あげる・くれる・もらう',[('Aが Bに Nを あげる','A cho B (hướng ra ngoài)'),('Aが（わたしに）Nを くれる','người khác cho TÔI / người nhà tôi'),('Bが Aに/から Nを もらう','B nhận từ A')],
 [('父が誕生日に時計を**くれました**。','Bố đã tặng tôi đồng hồ vào sinh nhật.'),('友だちに本を貸して**あげました**。','Tôi đã cho bạn mượn sách.'),('先輩に日本語を教えて**もらいました**。','Tôi được đàn anh dạy tiếng Nhật.')],
 '<b>Người nhận là "tôi"</b> và chủ ngữ là người khác → <b>くれる</b>. Chủ ngữ là "tôi" nhận → <b>もらう</b>. Tôi làm cho người khác → <b>Vてあげる</b>. Cùng cách dùng khi đi sau động từ thể て.')
eq(9,13,'Bố (người khác) tặng cho tôi, chủ ngữ là 父が → くれました. もらいました phải là 父に/から もらいました.')
eq(1,20,'Tôi giúp công việc cho bố → 手伝ってあげる (tôi làm cho người khác). くれる dùng khi người khác làm cho tôi.')
pat(3,'意向形 ＋ と思っています',[('Vよう／Vおう ＋ と思っています','định làm, đang có ý định'),('Vる ＋ つもりです','dự định (chắc chắn hơn)')],
 [('来年、N4を**受けよう**と思っています。','Năm sau tôi định thi N4.'),('国に帰ったら、店を**開こう**と思っています。','Về nước tôi định mở cửa hàng.'),('週末は家で**休むつもり**です。','Cuối tuần tôi định nghỉ ở nhà.')],
 NT('Cách chia thể ý chí: 行く→「行こう」 · 書く→「書こう」 · 食べる→「食べよう」 · 建てる→「建てよう」 · する→「しよう」 · 来る→「来よう」. Trước 「と思っています」 không dùng thể từ điển (行くと思っています = tôi nghĩ là (ai đó) sẽ đi).'))
eq(1,21,'Ý định của bản thân → thể ý chí たてよう + と思っています. たてろ là mệnh lệnh, たてられる là bị động/khả năng.')
sq('週末、友だちと映画を（　　）と思っています。',['見よう','見る','見ろ','見られる'],0,'Dự định của tôi → 見よう＋と思っています. 見ろ là mệnh lệnh; 見る＋と思う = "tôi nghĩ là (ai đó) xem".')
pat(4,'〜ために と 〜ように',[('Vる／Nの ＋ ために','để (mục đích, có chủ ý)'),('V khả năng／Vない ＋ ように','để có thể / để không')],
 [('家を**買うために**、貯金しています。','Tôi tiết kiệm để mua nhà.'),('日本語が**話せるように**、毎日練習しています。','Tôi luyện tập mỗi ngày để có thể nói được tiếng Nhật.'),('**忘れないように**、メモします。','Tôi ghi chú để không quên.')],
 NT('Trước <b>ために</b>: động từ có chủ ý ở thể từ điển (買う, 働く, 行く). Trước <b>ように</b>: thể khả năng (「話せる」「出せる」), thể ない, hoặc động từ không chủ ý (「わかる」「見える」). Thấy đuôi 〜える／〜られる／〜ない → chọn ように.'))
eq(1,19,'Trước chỗ trống là 話せる (thể khả năng) → ように. ために không đi với thể khả năng.')
eq(3,24,'ために + động từ thể từ điển có chủ ý → 働くために. 働ける (khả năng) phải đi với ように.')
eq(4,18,'Để (có thể) vứt được rác cỡ lớn → だせるように (thể khả năng + ように). だすように thiếu ý "có thể"; だせるために sai vì ために không đi với thể khả năng.')
pat(5,'〜ようになる・〜ようにしている',[('Vる／V khả năng ＋ ようになりました','đã trở nên (làm được)'),('Vる／Vない ＋ ようにしています','cố gắng duy trì thói quen')],
 [('日本語のニュースが**わかるようになりました**。','Tôi đã hiểu được tin tức tiếng Nhật.'),('はしが上手に**使えるようになりました**。','Tôi đã dùng đũa giỏi rồi.'),('毎日野菜を**食べるようにしています**。','Tôi cố gắng ăn rau mỗi ngày.')],
 '<b>ようになる</b> = sự thay đổi (trước không → bây giờ được), thường ở thì quá khứ 〜ようになりました. <b>ようにしている</b> = mình cố gắng làm đều đặn, thường trả lời câu hỏi "bạn làm gì để khỏe / để giỏi".')
eq(25,23,'Hỏi "bạn làm gì mà lúc nào cũng khỏe" → thói quen cố gắng giữ → 寝るようにしています.')
sq('日本に来て半年になりました。はしが上手に（　　）。',['使えるようになりました','使うようにしています','使えるようにしました','使ってしまいました'],0,'Sự thay đổi: trước không dùng được, nay dùng được → 使えるようになりました.')
pat(6,'〜のに 使います',[('Vる ＋ のに 使います','dùng để làm V'),('N ＋ に 使います','dùng cho N')],
 [('このはさみは、花を**切るのに**使います。','Cái kéo này dùng để cắt hoa.'),('この箱は、ごみを**捨てるのに**使います。','Cái hộp này dùng để vứt rác.'),('このお金は、旅行**に**使います。','Tiền này dùng cho chuyến du lịch.')],
 NT('Hỏi công dụng 「何に使いますか」 → trả lời 「〜のに使います」. Sau động từ phải có 「の」 trước 「に」.'))
eq(8,19,'Nói công dụng của cái kéo → 切るのに使います. つもり là dự định, かもしれません là phỏng đoán.')
pat(7,'〜てしまう・〜ちゃう・〜ちゃだめ',[('Vてしまいました','lỡ làm / đã làm xong (tiếc)'),('Vちゃう・Vじゃう','văn nói của てしまう'),('Vちゃだめ','văn nói của Vてはだめ (không được)')],
 [('電車にかさを**忘れてしまいました**。','Tôi lỡ để quên ô trên tàu.'),('ケーキを全部**食べちゃった**。','Lỡ ăn hết cái bánh rồi.'),('ここでたばこを**吸っちゃだめ**ですよ。','Ở đây không được hút thuốc đâu.')],
 NT('Đổi văn nói: てしまう → ちゃう, でしまう → じゃう (飲んじゃう) · ては → ちゃ, では → じゃ (飲んじゃだめ). Nghe 「〜ちゃだめ」 là lời cấm.'))
eq(21,17,'Sữa chua đã cũ → không được ăn → 食べちゃだめ (= 食べてはだめ).')
sq('駅で財布を（　　）。今から交番に行きます。',['なくしてしまいました','なくしてみました','なくしておきました','なくしてあげました'],0,'Việc không may xảy ra, tiếc nuối → なくしてしまいました. てみる = thử, ておく = làm sẵn.')
pat(8,'様態の「そう」と 伝聞の「そうです」',[('Vます・Aい・Aな ＋ そう','trông có vẻ (nhìn thấy)'),('Thể thường ＋ そうです','nghe nói (truyền đạt)')],
 [('このケーキ、**おいしそう**ですね。','Bánh này trông ngon nhỉ.'),('空が暗いです。雨が**降りそう**です。','Trời tối. Có vẻ sắp mưa.'),('天気予報によると、明日は雨が**降るそうです**。','Theo dự báo, nghe nói mai trời mưa.')],
 NT('Nhìn thấy → bỏ ます / bỏ い + そう: 「終わり」そう, 「でき」そう, 「甘」そう (いい → 「よさそう」). Nghe nói → để nguyên thể thường: 「甘いそうです」 = nghe nói ngọt. Có 「〜によると」「〜って」 → truyền đạt.'))
eq(2,15,'Đoán theo tình hình → Vます bỏ ます + そう: 終わり + そう. 終わるそう là "nghe nói sẽ xong".')
eq(3,25,'Hỏi "có vẻ làm được một mình không?" → できそう (できます bỏ ます + そう).')
eq(27,20,'Nhìn thấy cốc đồ uống, đoán vị → 甘そう (甘い bỏ い + そう). 甘いそうですね = nghe nói ngọt.')
pat(9,'〜たら・〜なら・〜ても',[('Vた ＋ ら','nếu / khi ~ thì'),('N／V ＋ なら','nếu là ~ thì (nhận lời người kia, khuyên)'),('Vて ＋ も','dù ~ cũng')],
 [('雨が**降ったら**、試合は中止です。','Nếu mưa thì trận đấu bị hủy.'),('ラーメン**なら**、駅前の店がおいしいですよ。','Nếu là ramen thì quán trước ga ngon đấy.'),('雨が**降っても**、試合をします。','Dù mưa vẫn thi đấu.')],
 NT('Người kia vừa nói đến một chủ đề, mình khuyên → <b>なら</b> (「おいしい店なら」). Kết quả ngược với điều kiện → <b>ても</b>. Điều kiện bình thường → <b>たら</b>.'))
eq(4,14,'Giả định trời mưa thì làm thế nào → 降ったら. 降っても = dù mưa (không hợp với "どうしますか").')
eq(2,21,'A hỏi "quán ramen ngon", B nhận chủ đề đó rồi giới thiệu → おいしい店なら.')
sq('いくら（　　）、日本語が上手になりません。',['練習しても','練習したら','練習すれば','練習するなら'],0,'いくら〜ても = dù ~ bao nhiêu cũng. Kết quả ngược với điều kiện → ても.')
pat(10,'〜かどうか・疑問詞〜か',[('Thể thường ＋ かどうか','có ~ hay không'),('Từ để hỏi … ＋ か','câu hỏi lồng trong câu')],
 [('明日雨が**降るかどうか**、わかりません。','Không biết mai có mưa hay không.'),('会議が**何時に始まるか**、知っていますか。','Bạn có biết họp bắt đầu lúc mấy giờ không?'),('この服が**似合うかどうか**、着てみます。','Tôi mặc thử xem có hợp không.')],
 NT('Trước 「かどうか」 dùng thể thường (danh từ, tính từ な bỏ だ: 「元気かどうか」). Câu có từ để hỏi (何, どこ, いつ) thì chỉ dùng 「か」, không dùng 「かどうか」.'))
eq(1,22,'Thể thường + かどうか → 降るかどうか. ふれる (khả năng) và ふった (quá khứ) không hợp với "ngày mai".')
pat(11,'受身形（うけみ）',[('Vられる／Vれる','bị / được (ai đó làm gì mình)'),('Nが（ai đó によって）Vられた','được làm ra (vật, công trình)')],
 [('テストでいい点を取って、先生に**ほめられました**。','Được điểm cao nên được thầy khen.'),('電車で足を**踏まれました**。','Bị giẫm vào chân trên tàu.'),('このお寺は400年前に**建てられました**。','Ngôi chùa này được xây 400 năm trước.')],
 NT('Cách chia: 書く→「書かれる」 · ほめる→「ほめられる」 · する→「される」 · 来る→「来られる」. Người làm hành động đi với 「に」. Chú ý: 「見られる」「来られる」 vừa là bị động vừa là khả năng – nhìn ngữ cảnh.'))
sq('テストで100点を取って、先生に（　　）。',['ほめられました','ほめました','ほめさせました','ほめてあげました'],0,'Tôi là người được khen, người khen là 先生に → bị động ほめられました.')
pat(12,'〜たほうがいい・〜ないほうがいい',[('Vた ＋ ほうがいい','nên làm'),('Vない ＋ ほうがいい','không nên làm')],
 [('熱があるなら、早く**寝たほうがいい**ですよ。','Nếu bị sốt thì nên ngủ sớm.'),('9月は台風が多いから、**行かないほうがいい**です。','Tháng 9 nhiều bão nên không nên đi.'),('寒いから、コートを**着て行ったほうがいい**よ。','Trời lạnh nên mặc áo khoác đi thì hơn.')],
 NT('Khuyên làm → thể た (「行った」ほうがいい). Khuyên không làm → thể ない (「行かない」ほうがいい). Câu có lý do xấu (混む, 台風, 危ない) thường đi với ないほうがいい.'))
eq(9,14,'Chủ nhật rất đông → khuyên không nên đi → 行かないほうがいいです.')
eq(3,26,'Tháng 9 là mùa bão → 行かないほうがいい.')
pat(13,'〜んです・〜んですが',[('Thể thường ＋ んです','giải thích lý do, tình huống'),('〜んですが、…','mở lời trước khi nhờ / hỏi')],
 [('どうしたんですか。—頭が**痛いんです**。','Bạn sao vậy? — Tôi bị đau đầu.'),('銀行に**行きたいんですが**、どこにありますか。','Tôi muốn đi ngân hàng, nó ở đâu ạ?'),('あの、パソコンが**動かないんですが**…。','À, máy tính không chạy…')],
 NT('Câu hỏi 「どうしたんですか」 → trả lời bằng 「〜んです」 nêu lý do. Danh từ / tính từ な + 「なんです」 (「休みなんです」).'))
eq(4,23,'Hỏi lý do vừa mới đến → giải thích bằng んです. Vì tuyết lớn nên tàu dừng → 電車が止まったんです.')
pat(14,'可能形（かのうけい）',[('Vえる／Vられる','có thể làm'),('Nが ＋ V khả năng','khả năng đi với が')],
 [('日本語が少し**話せます**。','Tôi nói được một chút tiếng Nhật.'),('明日のパーティーに**来られません**。','Tôi không đến được bữa tiệc ngày mai.'),('太って、服が**着られなく**なりました。','Béo lên nên không mặc được quần áo nữa.')],
 NT('Nhóm 1: 書く→「書ける」, 話す→「話せる」 · Nhóm 2: 食べる→「食べられる」, 着る→「着られる」 · する→「できる」 · 来る→「来られる」(こられる). Phủ định: 来られません／これません (văn nói).'))
eq(3,16,'B đáp "tiếc quá" → Maria không đến được → これません (= 来られません, thể khả năng phủ định).')
eq(5,14,'Cỡ người thay đổi → không mặc vừa nữa → 着られなくなったら (khả năng phủ định + なる + たら).')
pat(15,'敬語：お店で よく聞く表現',[('〜はいかがですか','~ thì thế nào ạ? (gợi ý, mời)'),('〜はどうなさいますか','quý khách muốn thế nào ạ?'),('かしこまりました／少々お待ちください','tôi hiểu rồi / xin chờ một chút')],
 [('こちらのケーキは**いかがですか**。','Bánh này thì sao ạ?'),('お飲み物は**どうなさいますか**。','Đồ uống quý khách chọn gì ạ?'),('**かしこまりました**。**少々お待ちください**。','Vâng ạ. Xin quý khách chờ một chút.')],
 NT('「いかが」 = 「どう」 lịch sự, dùng khi gợi ý / mời. 「なさる」 = 「する」 kính ngữ, dùng khi hỏi khách chọn gì. Nghe khách trả lời một lựa chọn (「大盛りで」) → câu hỏi là 「どうなさいますか」.'))
eq(1,24,'Khách hỏi món gợi ý, nhân viên giới thiệu → 親子丼はいかがですか.')
eq(1,25,'Hỏi khách muốn lượng cơm thế nào → どうなさいますか (khách đáp 「大盛りで」).')
OVH=''.join(f'<div><b>{n}</b><span class="jp">{F(t)}</span></div>' for n,t in OV)
S[OVI]=f'<section class="slide"><h2>15 mẫu ngữ pháp trọng tâm <small>chọn từ bộ đề trong app</small></h2><div class="ov">{OVH}</div><p class="note">Đây là các mẫu xuất hiện nhiều trong phần 会話と表現 của Đề 1–27. Mỗi mẫu: cách nối → ví dụ → điểm cần phân biệt → luyện tập.</p>{CR}</section>'
rows=[('てもらえませんか／ましょうか／てもいいですか','nhìn câu trả lời: いいですよ / お願いします / どうぞ'),('あげる／くれる／もらう','người khác cho tôi → くれる'),('意向形＋と思っています','行こう・食べよう・しよう・来よう'),('ために／ように','khả năng・ない → ように'),('ようになる／ようにしている','thay đổi / thói quen'),('〜のに使います','công dụng'),('てしまう／ちゃう／ちゃだめ','lỡ làm / không được'),('〜そう／〜そうです','nhìn thấy / nghe nói'),('たら／なら／ても','điều kiện / nhận chủ đề / dù'),('かどうか／疑問詞＋か','có … hay không'),('受身','ほめられる・建てられる'),('ほうがいい','Vた / Vない ＋ ほうがいい'),('んです／んですが','giải thích / mở lời'),('可能形','書ける・食べられる・来られる'),('いかがですか／どうなさいますか','mời / hỏi khách chọn')]
for k,(a0,b0) in enumerate([(0,8),(8,15)]):
    S.append(f'<section class="slide"><h2>Tổng kết <small>{k+1}/2</small></h2><table class="sum">'+''.join(f'<tr><td class="k">{F(a)}</td><td>{html.escape(b)}</td></tr>' for a,b in rows[a0:b0])+f'</table>{CR}</section>')
out=HEAD.replace('<title>Kính ngữ trong JFT-Basic</title>','<title>Ngữ pháp trọng tâm JFT-Basic</title>')+''.join(S)+TAIL
open(sys.argv[1] if len(sys.argv)>1 else '/tmp/kj/NguPhap_TrongTam_JFT.html','w').write(out);print(len(S),'slides',NQ[0],'quiz',len(out)//1024,'KB')
