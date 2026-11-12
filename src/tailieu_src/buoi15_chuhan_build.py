import json,re,html,sys
sys.path.insert(0,'/home/claude/anhtrong-jft-app/src/jft')
from furi import furi
T=open('/home/claude/anhtrong-jft-app/public/tailieu/Buoi10_KinhNgu.html').read()
HEAD=T[:T.index('</style>')]+'''
.kg{display:grid;gap:26px;flex:1;align-content:center}.kg.c2{grid-template-columns:repeat(2,1fr)}.kg.c3{grid-template-columns:repeat(3,1fr)}.kg.c4{grid-template-columns:repeat(4,1fr)}.kg.c5{grid-template-columns:repeat(5,1fr)}
.kc{background:#fff;border-radius:22px;padding:22px 20px 18px;box-shadow:0 8px 24px #0d2b4012;text-align:center;border-top:8px solid #0d5a8c}.kc:nth-child(2){border-color:#c42f66}.kc:nth-child(3){border-color:#f2a93b}.kc:nth-child(4){border-color:#5a9e2f}.kc:nth-child(5){border-color:#7a4fb5}
.kc .k{font-family:"Klee One",serif;font-size:150px;line-height:1.05;color:#0d2b40}.kc .hv{font-size:30px;font-weight:700;color:#c42f66;letter-spacing:1px}.kc .rd{font-size:28px;margin-top:4px}.kc .mn{font-size:24px;color:#47647a;margin-top:2px}.kc .vd{font-size:28px;margin-top:12px;background:#f6f8fb;border-radius:12px;padding:8px}.kc .vd rt{font-size:.45em}
.pb{margin-top:22px;background:#fff8e6;border-left:8px solid #f2a93b;border-radius:14px;padding:16px 26px;font-size:27px;line-height:1.55}.pb b{color:#c42f66}.pb .jp{font-size:30px}
.src{font-size:22px;color:#6b8296;margin-left:12px;font-weight:600}.q u{text-decoration:none;border-bottom:4px solid #c42f66}
.st{visibility:hidden;opacity:0;transform:translateY(8px);transition:opacity .35s,transform .35s}.st.sh{visibility:visible;opacity:1;transform:none}.kc{cursor:pointer}
#ann{position:fixed;inset:0;z-index:8;pointer-events:none}.ntx,.nmm{position:absolute;pointer-events:auto;outline:none;font-family:"Klee One","M PLUS Rounded 1c",Quicksand,sans-serif;font-weight:600}
.ntx{color:#e0245e;font-size:34px;min-width:20px;padding:2px 6px;border:2px dashed transparent}.ntx:focus{border-color:#e0245e88}
.nmm{background:#fff3a6;color:#0d2b40;font-size:26px;min-width:180px;min-height:70px;padding:14px 16px 12px;border-radius:6px;box-shadow:0 8px 20px #0d2b4040;transform:rotate(-1.5deg)}.nmm .gr{position:absolute;left:0;right:0;top:0;height:12px;cursor:move;background:#f2d95c;border-radius:6px 6px 0 0}.nmm .tx{outline:none;min-height:40px}.nmm .xx{position:absolute;right:4px;top:-2px;font-size:16px;cursor:pointer;color:#8a6d1a}
body.m-text #pen,body.m-memo #pen{pointer-events:auto;cursor:text}body.m-memo #pen{cursor:copy}
#bar button.on{background:#c42f66}#bar button{white-space:nowrap}
.sum{width:100%;border-collapse:collapse;font-size:26px}.sum td{padding:9px 16px;border-bottom:1px solid #dbe4ec}.sum td.k{font-family:"Klee One",serif;font-size:38px;white-space:nowrap}.sum tr:nth-child(odd) td{background:#fff}
</style></head><body><div id="stage">'''
LOGO=re.search(r'<img class="lg" src="([^"]+)"',T).group(1)
TAIL=open('/home/claude/anhtrong-jft-app/src/tailieu_src/buoi15_tail.html').read()
F=lambda s: furi(html.escape(s)).replace('\n','<br>')
CR='<div class="cr">Chữ Hán dễ nhầm trong JFT-Basic · Anh Trọng Dạy JFT · giải thích tự soạn; câu luyện tập lấy từ bộ đề trong app (ghi nguồn) hoặc tự soạn</div>'
KQ=json.load(open('/home/claude/anhtrong-jft-app/src/tailieu_src/buoi15_kq.json'))
def ex(id,n): return next(x for x in KQ if x['id']==id and x['n']==n)
S=[]
S.append(f'''<section class="slide dark"><div class="cover"><img class="lg" src="{LOGO}"><div class="kk">Chữ Hán · 漢字 · JFT-Basic</div><h1>Chữ Hán dễ nhầm<br><span>nhìn giống – đọc giống</span></h1><p class="jp">似ている漢字・同じ読み方の漢字</p></div>{CR}</section>''')
S.append(f'''<section class="slide"><h2>Cách phân biệt chữ giống nhau <small>3 bước</small></h2><div class="steps"><div><b>1</b><h3>Tìm phần khác nhau</h3><p>Hai chữ giống nhau thường chỉ khác <b>một bộ</b> hoặc <b>một nét</b>. Che phần giống, nhìn phần khác: 右 có 口, 左 có 工.</p></div><div><b>2</b><h3>Gắn với nghĩa của bộ</h3><p>Bộ cho biết nghĩa: <b>亻</b> người (休, 体, 働), <b>艹</b> cây cỏ (薬, 葉, 菜), <b>雨</b> thời tiết (雪, 雲, 雷), <b>門</b> cửa (間, 聞, 開).</p></div><div><b>3</b><h3>Nhớ theo từ, không nhớ chữ lẻ</h3><p>Học cả từ hay gặp trong đề: <span class="jp">右に曲がる・友だち・薬を飲む・音楽・案内</span>. Gặp từ là nhận ra chữ.</p></div></div><p class="note">Trong đề JFT, các phương án sai thường là chữ "na ná" chữ đúng – thậm chí là chữ không có thật (勿, 夘). Biết chữ đúng viết thế nào là loại được ngay.</p>{CR}</section>''')
def group(title,sub,cards,pb,cols=None):
    c=cols or len(cards)
    h=''.join(f'<div class="kc"><div class="k">{k}</div><div class="st"><div class="hv">{hv}</div><div class="rd jp">{html.escape(rd)}</div><div class="mn">{html.escape(mn)}</div><div class="vd jp">{F(vd) if vd else '&nbsp;'}</div></div></div>' for k,hv,rd,mn,vd in cards)
    S.append(f'<section class="slide"><h2>{title} <small>{sub}</small></h2><div class="kg c{c}">{h}</div><div class="pb st">{pb}</div>{CR}</section>')
NQ=[0]
def quiz(qhtml,opts,a,expl,src):
    NQ[0]+=1
    ks='①②③④'
    ob=''.join(f'<button class="o" data-k="{ks[i]}"><b>{ks[i]}</b><span class="jp ot">{o}</span><i></i><em></em></button>' for i,o in enumerate(opts))
    S.append(f'<section class="slide qz"><div class="kk2">Luyện tập {NQ[0]} <span class="src">{src}</span></div><h2 class="jp q">{qhtml}</h2><div class="opts list" data-a="{ks[a]}">{ob}</div><div class="ex"><b>Đáp án: {ks[a]} {opts[a]}</b> — {expl}</div>{CR}</section>')
def eq(id,n,expl):
    x=ex(id,n);opts=[re.sub(r'^\s*[a-d]\.\s*','',o) for o in x['o']]
    quiz(x['t'],opts,x['a'],expl,f"Nguồn: {x['title']} · câu {x['n']}")
def sq(text,opts,a,expl):
    quiz(F(text).replace('[','<u>').replace(']','</u>') if '[' in text else F(text),[html.escape(o) for o in opts],a,expl,'Câu tự soạn')

# ---- nhóm ----
group('Nhóm 1 · 右・左・友・石','cùng phần 𠂇 ở trên',[('右','HỮU','みぎ','bên phải','右に曲がる'),('左','TẢ','ひだり','bên trái','左側'),('友','HỮU','とも','bạn','友だち'),('石','THẠCH','いし','đá','石の橋')],
 'Cùng nét đầu, khác phần dưới: <b>右</b> có 口 (cái miệng – tay phải cầm đũa đưa vào miệng) · <b>左</b> có 工 · <b>友</b> có 又 · <b>石</b> nét ngang trên dài, không có nét xiên cắt qua.')
eq('jft-y3',10,'みぎ = 右 (HỮU). 在 (TẠI – 在留カード), 石 (THẠCH – đá), 古 (CỔ – ふるい) chỉ giống hình.')
eq('jft-g15',9,'ともだち = 友だち. 右だち, 左だち không có từ này – chỉ là chữ giống hình 友.')
group('Nhóm 2 · 人・入・大・八','vài nét, rất dễ đảo',[('人','NHÂN','ひと・じん','người','日本人'),('入','NHẬP','はいる・いれる','vào','入口'),('大','ĐẠI','おおきい','to','大きい'),('八','BÁT','はち','số 8','八時')],
 '<b>人</b>: nét trái dài hơn · <b>入</b>: nét phải dài, nét trái ngắn tựa vào (đi VÀO) · <b>大</b> = 人 dang tay (thêm nét ngang) · <b>八</b>: hai nét tách rời.')
eq('jft-y2',11,'ひと = 人 (NHÂN). 入 (NHẬP – はいる) đảo chiều nét, 大 có thêm nét ngang, 八 hai nét không chạm nhau.')
group('Nhóm 3 · 休・体・本・林','亻 + 木',[('休','HƯU','やすむ','nghỉ','休み'),('体','THỂ','からだ','cơ thể','体に いい'),('本','BẢN','ほん','sách, gốc','日本'),('林','LÂM','はやし','rừng thưa','林さん')],
 '<b>休</b> = người (亻) dựa vào cây (木) → nghỉ · <b>体</b> = 亻 + 本 (có thêm nét ngang dưới) · <b>本</b> = 木 + một nét gạch ở gốc · <b>林</b> = hai cây.')
eq('jft-y2',10,'やすみ = 休み: người (亻) tựa gốc cây (木) để nghỉ. 体 (THỂ) có thêm nét ngang ở dưới – đó là chữ からだ.')
group('Nhóm 4 · 薬・楽・葉・菜','có 艹 hay không?',[('薬','DƯỢC','くすり','thuốc','薬を飲む'),('楽','LẠC','たのしい・がく','vui, nhạc','楽しい・音楽'),('葉','DIỆP','は','lá','言葉'),('菜','THÁI','さい','rau','野菜')],
 '<b>薬</b> = 艹 (cây cỏ – thuốc làm từ cây) + 楽 · <b>楽</b> KHÔNG có 艹 · <b>葉</b>: 艹 + 世 + 木 · <b>菜</b>: 艹 + 采. Thuốc thì có cỏ, vui thì không.')
eq('jft-y1',10,'くすり = 薬 (DƯỢC) – có bộ 艹. 楽 (LẠC) là thiếu 艹; 葉 (DIỆP – lá), 菜 (THÁI – rau) cũng có 艹 nhưng phần dưới khác.')
eq('jft-f8',10,'おんがく = 音楽 – âm nhạc, chữ 楽 KHÔNG có 艹. 音薬 không có từ này (薬 = thuốc). 音声 (おんせい) = âm thanh giọng nói.')
group('Nhóm 5 · 食・飲・飯・良','bộ 食 (飠)',[('食','THỰC','たべる','ăn','食べ物'),('飲','ẨM','のむ','uống','飲み物'),('飯','PHẠN','はん','cơm','ご飯'),('良','LƯƠNG','よい','tốt','')],
 '<b>食</b> = 人 (mái) + 良 · đứng bên trái thì viết thành <b>飠</b>: 飲 (uống), 飯 (cơm). <b>良</b> thiếu phần 人 ở trên. Ăn: 食べる · uống: 飲む · cơm: ご飯.')
eq('jft-g20',6,'たべます = 食べます. 飲 là uống (のみます), 飼 là nuôi (かいます), 良 thiếu phần mái 人 ở trên.')
group('Nhóm 6 · 物・特・持・待・時','phần bên phải giống nhau',[('物','VẬT','もの','đồ vật','飲み物'),('特','ĐẶC','とく','đặc biệt','特に'),('持','TRÌ','もつ','cầm, mang','持って行く'),('待','ĐÃI','まつ','đợi','待ってください'),('時','THỜI','とき・じ','giờ, lúc','時間')],
 '<b>牛</b> bên trái: 物, 特 · <b>扌</b> (tay): 持 – cầm bằng tay · <b>彳</b> (bước đi): 待 – đứng đợi · <b>日</b> (mặt trời): 時 – thời gian. Phần 寺 giống nhau, nhìn bộ bên trái là ra.')
eq('jft-y1',12,'のみもの = 飲み物. 勿 thiếu bộ 牛, 特 (ĐẶC – とく) là chữ khác; 飯 (PHẠN – cơm) thay cho 飲 là sai.')
group('Nhóm 7 · 店・広・庭・床','bộ 广 (mái nhà)',[('店','ĐIẾM','みせ','cửa hàng','店員'),('広','QUẢNG','ひろい','rộng','広い'),('庭','ĐÌNH','にわ','vườn','庭'),('床','SÀNG','ゆか','sàn nhà','')],
 'Cùng mái nhà 广, khác phần trong: <b>店</b> = 广 + 占 · <b>広</b> = 广 + ム · <b>庭</b> = 广 + 廷 · <b>床</b> = 广 + 木.')
eq('jft-y3',11,'みせ = 店 (ĐIẾM): mái 广 + 占. 床 (ゆか – sàn), 庭 (にわ – vườn), 広 (ひろい – rộng) cùng mái nhưng phần trong khác.')
group('Nhóm 8 · 卵・印','chữ hình quả trứng',[('卵','NOÃN','たまご','trứng','卵焼き'),('印','ẤN','いん・しるし','con dấu, dấu','印鑑')],
 '<b>卵</b>: hai nửa đối xứng, <b>mỗi bên có một chấm</b> (lòng đỏ) · <b>印</b>: bên trái là 𠂤, không có chấm. Các phương án 夘, 卯 trong đề là chữ ít dùng – chỉ để gây nhiễu.',cols=2)
eq('jft-y3',12,'たまご = 卵 – hai bên đều có chấm. 印 (ẤN – con dấu) không có chấm; 夘, 卯 là chữ hiếm, không dùng cho "trứng".')
group('Nhóm 9 · 南・商・両・有','khung giống nhau',[('南','NAM','みなみ','phía nam','南口'),('商','THƯƠNG','しょう','buôn bán','商店'),('両','LƯỠNG','りょう','cả hai','両親'),('有','HỮU','ゆう','có','有名')],
 '<b>南</b>: 十 ở trên + 冂 + 羊 bên trong · <b>商</b>: 亠 ở trên, bên trong có 口 · <b>両</b>: một nét ngang trên, không có 十 · <b>有</b> = 𠂇 + 月.')
eq('jft-y1',11,'みなみ = 南 (NAM). 商 (THƯƠNG – buôn bán), 両 (LƯỠNG – cả hai), 有 (HỮU – 有名) chỉ giống khung.')
group('Nhóm 10 · 困・因・固','bộ 囗 (khung vây)',[('困','KHỐN','こまる','gặp khó khăn','困ったとき'),('因','NHÂN','いん','nguyên nhân','原因'),('固','CỐ','かたい','cứng','')],
 'Cây (<b>木</b>) bị nhốt trong khung không lớn được → <b>困</b> khó khăn · <b>因</b>: trong khung là 大 · <b>固</b>: trong khung là 古.',cols=3)
eq('jft-g15',10,'こまった = 困った: cây 木 bị nhốt trong khung → khó khăn. 因 (trong khung là 大), 固 (trong khung là 古).')
group('Nhóm 11 · 好・安・案','có 女 (người phụ nữ)',[('好','HẢO','すき','thích','好きな食べ物'),('安','AN','やすい','rẻ, yên','安い'),('案','ÁN','あん','phương án','案内')],
 '<b>好</b> = 女 + 子 · <b>安</b> = mái 宀 + 女 → yên ổn, rẻ · <b>案</b> = 安 + 木 ở dưới → 案内 (hướng dẫn). Đề hay gài "安内" – nhớ 案内 phải có 木.',cols=3)
eq('jft-g15',8,'すき = 好き: 女 + 子. 奸, 奴 cũng có 女 nhưng phần bên phải khác, không phải chữ "thích".')
eq('jft-g19',12,'あんない = 案内 – chữ 案 có 木 ở dưới. 安内 sai chữ (thiếu 木), 案肉 sai chữ 内 → 肉 (thịt).')
group('Nhóm 12 · 重・動・働','重 → 動 → 働',[('重','TRỌNG','おもい','nặng','重い荷物'),('動','ĐỘNG','うごく','chuyển động','動く・運動'),('働','ĐỘNG','はたらく','làm việc','働く')],
 'Xây từng lớp: <b>重</b> (nặng) + 力 (sức) → <b>動</b> (dùng sức làm vật nặng chuyển động) + 亻 (người) → <b>働</b> (người làm việc).',cols=3)
eq('jft-g19',11,'おもい = 重い (TRỌNG). 動 là うごく, 働 là はたらく – không có tính từ 動い, 働い.')
group('Nhóm 13 · 東・来・車','có 木 / 十 ở giữa',[('東','ĐÔNG','ひがし','phía đông','東口'),('来','LAI','くる','đến','来週'),('車','XA','くるま','xe','電車')],
 '<b>東</b> = mặt trời (日) mọc sau cây (木) → phía đông · <b>来</b>: 木 có thêm hai chấm, không có 日 · <b>車</b>: giữa là 日 nhưng không có nét xiên.',cols=3)
eq('jft-g20',5,'ひがし = 東: mặt trời 日 sau cây 木. 来 (くる), 南 (みなみ), 西 (にし).')
group('Nhóm 14 · 年・午・牛','khác một nét',[('年','NIÊN','ねん・とし','năm','2024年'),('午','NGỌ','ご','buổi trưa','午後'),('牛','NGƯU','うし・ぎゅう','bò','牛肉')],
 '<b>午</b>: nét dọc KHÔNG nhô lên trên · <b>牛</b>: nét dọc nhô lên trên (sừng bò) · <b>年</b>: nhiều nét hơn, có thêm nét ngang và nét ngắn bên trái.',cols=3)
eq('jft-g21',10,'Năm viết là 年. 午 (午後 – buổi chiều) và 牛 (con bò) chỉ giống hình.')
group('Nhóm 15 · 間・聞・問・開','bộ 門 (cánh cửa)',[('間','GIAN','あいだ・かん','khoảng, giữa','時間'),('聞','VĂN','きく','nghe, hỏi','聞く'),('問','VẤN','もん','câu hỏi','問題'),('開','KHAI','あく','mở','開ける')],
 'Nhìn bên trong cửa 門: <b>日</b> → 間 (ánh mặt trời lọt qua khe cửa) · <b>耳</b> → 聞 (tai áp cửa để nghe) · <b>口</b> → 問 (miệng hỏi) · <b>开</b> → 開 (mở).')
sq('毎朝、ニュースを[きき]ます。',['聞き','間き','問き','開き'],0,'きく = 聞く: tai (耳) áp vào cửa. 間 (GIAN – 時間), 問 (VẤN – 問題), 開 (KHAI – 開ける).')
group('Nhóm 16 · 雨・雪・雲・雷・電','bộ 雨 (mưa)',[('雨','VŨ','あめ','mưa','雨の日'),('雪','TUYẾT','ゆき','tuyết','雪が降る'),('雲','VÂN','くも','mây','雲'),('雷','LÔI','かみなり','sấm','雷'),('電','ĐIỆN','でん','điện','電車')],
 'Tất cả có 雨 ở trên, nhìn phần dưới: <b>ヨ</b> → 雪 · <b>云</b> → 雲 · <b>田</b> → 雷 · <b>田 + nét cong</b> → 電. Sấm và điện đều từ trời, chỉ khác nét đuôi.')
sq('あしたは[ゆき]が降るでしょう。',['雪','雲','雷','電'],0,'ゆき = 雪: 雨 + ヨ. 雲 (くも – mây), 雷 (かみなり – sấm), 電 (でん – điện).')
group('Nhóm 17 · 目・日・白・自・百','đếm nét ngang',[('日','NHẬT','ひ・にち','ngày','毎日'),('目','MỤC','め','mắt','目が痛い'),('白','BẠCH','しろい','trắng','白いシャツ'),('自','TỰ','じ','tự mình','自分'),('百','BÁCH','ひゃく','trăm','百円')],
 '<b>日</b>: 1 nét ngang giữa · <b>目</b>: 2 nét ngang · <b>白</b> = 日 + một chấm trên đầu · <b>自</b> = 目 + một chấm trên đầu · <b>百</b> = 白 + nét ngang trên cùng.')
sq('[しろい]シャツを買いました。',['白い','百い','自い','日い'],0,'しろい = 白い: 日 + một chấm. 百 (trăm) có thêm nét ngang trên, 自 (tự) là 目 + chấm.')
group('Nhóm 18 · 犬・大・太','vị trí dấu chấm',[('大','ĐẠI','おおきい','to','大きい'),('犬','KHUYỂN','いぬ','chó','犬'),('太','THÁI','ふとい','béo, mập','太る')],
 'Cùng là 大 + một chấm: chấm ở <b>trên bên phải</b> → <b>犬</b> (tai chó) · chấm ở <b>dưới, giữa hai chân</b> → <b>太</b>.',cols=3)
sq('うちで[いぬ]をかっています。',['犬','太','大','尤'],0,'いぬ = 犬: chấm ở trên bên phải. 太 có chấm ở dưới (ふとい), 大 không có chấm.')
group('Nhóm 19 · 末・未・天・夫','nét ngang dài hay ngắn',[('末','MẠT','まつ','cuối','週末'),('未','VỊ','み','chưa','未成年'),('天','THIÊN','てん','trời','天気'),('夫','PHU','おっと','chồng','夫')],
 '<b>末</b>: nét ngang trên DÀI hơn (ngọn cây – cuối) · <b>未</b>: nét ngang trên NGẮN hơn (cây chưa lớn – chưa) · <b>天</b>: nét dọc không nhô lên · <b>夫</b>: nét dọc nhô lên trên.')
sq('[しゅうまつ]は何をしますか。',['週末','週未','過末','週本'],0,'しゅうまつ = 週末: chữ 末 nét ngang trên dài hơn. 未 (VỊ – chưa) nét trên ngắn; 過 (QUÁ) khác 週; 本 thiếu nét.')
group('Nhóm 20 · Đọc giống – viết khác','cùng cách đọc, khác chữ',[('着ます','TRƯỚC','きます','mặc (áo)','服を着ます'),('来ます','LAI','きます','đến','日本に来ます'),('見ます','KIẾN','みます','xem','テレビを見ます'),('暑い','THỬ','あつい','nóng (trời)','夏は暑い'),('熱い','NHIỆT','あつい','nóng (vật)','熱いお茶')],
 'Cùng âm thì nhìn <b>từ đi kèm</b>: 服を<b>着ます</b> · 日本に<b>来ます</b> · 駅に<b>着きます</b>(つきます) · テレビを<b>見ます</b> (診ます = bác sĩ khám) · trời <b>暑い</b> · đồ uống <b>熱い</b>. 地震 (động đất) ≠ 自信 (tự tin) – cùng đọc じしん.')
eq('jft-f13',13,'服を「きます」 = 着ます (mặc). 来ます cũng đọc きます nhưng là "đến"; 着きます đọc つきます (đến nơi).')
eq('jft-t1',11,'テレビを見ます (xem). 診ます cũng đọc みます nhưng là bác sĩ khám bệnh; 寝ます (ねます) là ngủ.')
sq('きょうは[あつい]ですね。エアコンをつけましょう。',['暑い','熱い','厚い','圧い'],0,'Nói về thời tiết, nhiệt độ không khí → 暑い (THỬ – có 日). 熱い (NHIỆT) dùng cho đồ vật nóng (お茶, お風呂); 厚い là dày.')
# tổng kết
rows=[('右・左・友・石','口 / 工 / 又 – nhìn phần dưới'),('人・入・大・八','nét nào dài, có chạm nhau không'),('休・体','体 có thêm nét ngang dưới'),('薬・楽','thuốc có 艹, nhạc không'),('食・飲・飯・良','bộ 飠 bên trái'),('物・特・持・待・時','nhìn bộ bên trái: 牛・扌・彳・日'),('店・広・庭・床','cùng 广, khác phần trong'),('卵・印','卵 có hai chấm'),('南・商・両・有','南 có 十 trên đầu'),('困・因・固','trong khung: 木 / 大 / 古'),('好・安・案','案内 có 木')]
rows2=[('重・動・働','重 → +力 → +亻'),('東・来・車','東 có 日 sau 木'),('年・午・牛','牛 nét dọc nhô lên'),('間・聞・問・開','trong cửa: 日 / 耳 / 口 / 开'),('雨・雪・雲・雷・電','phần dưới 雨'),('日・目・白・自・百','đếm nét ngang, xem chấm'),('大・犬・太','vị trí chấm'),('末・未・天・夫','nét ngang dài/ngắn, nét dọc nhô'),('着る・来る・見る・診る','cùng âm → nhìn từ đi kèm'),('暑い・熱い','trời → 暑い, vật → 熱い')]
tb=lambda R:'<table class="sum">'+''.join(f'<tr><td class="k">{a}</td><td>{html.escape(b)}</td></tr>' for a,b in R)+'</table>'
S.append(f'<section class="slide"><h2>Tổng kết <small>1/2</small></h2>{tb(rows)}{CR}</section>')
S.append(f'<section class="slide"><h2>Tổng kết <small>2/2</small></h2>{tb(rows2)}{CR}</section>')
out=HEAD.replace('<title>Kính ngữ trong JFT-Basic</title>','<title>Chữ Hán dễ nhầm trong JFT-Basic</title>')+''.join(S)+TAIL
open('/home/claude/anhtrong-jft-app/public/tailieu/Buoi15_ChuHan_DeNham.html','w').write(out);print(len(S),'slides',NQ[0],'quiz',len(out)//1024,'KB')
