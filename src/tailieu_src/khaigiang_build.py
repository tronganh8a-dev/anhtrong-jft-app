"""Slide khai giảng khoá JFT-Basic (17/11/2026): giới thiệu kỳ thi, đề thi, thang điểm.
Dùng chung CSS + thanh công cụ với Buoi15 (Buoi10_KinhNgu.html + buoi15_tail.html).
Số liệu theo trang chính thức Quỹ Giao lưu Quốc tế Nhật Bản + Prometric (tra 17/11/2026).
Chạy: python3 src/tailieu_src/khaigiang_build.py → public/tailieu/KhaiGiang_JFTBasic.html"""
import re, html, sys
sys.path.insert(0, '/home/claude/anhtrong-jft-app/src/jft')
from furi import furi
R = '/home/claude/anhtrong-jft-app/'
exec(open(R + 'src/tailieu_src/_head_snip.py').read())  # HEAD, LOGO
HEAD = HEAD.replace('</style></head>', '''
.kgr{display:grid;gap:24px}.kgr.g2{grid-template-columns:1fr 1fr}.kgr.g3{grid-template-columns:repeat(3,1fr)}.kgr.g4{grid-template-columns:repeat(4,1fr)}
.kcd{background:#fff;border-radius:22px;padding:26px 28px;box-shadow:0 8px 24px #0d2b4012;font-size:27px;line-height:1.5}
.kcd h3{font-size:31px;margin-bottom:8px}.kcd .jp{font-family:"Klee One",serif;font-weight:600}
.kcd.kb{border-top:8px solid #0d5a8c}.kcd.kp{border-top:8px solid #c42f66}.kcd.ko{border-top:8px solid #f2a93b}.kcd.kg2{border-top:8px solid #7cb342}
.kbig{font-size:120px;font-weight:800;color:#c42f66;line-height:1}.kbig small{font-size:40px;color:#0d2b40}
.ktb{width:100%;border-collapse:separate;border-spacing:0 10px;font-size:28px}.ktb th{text-align:left;color:#6b8296;font-size:22px;padding:0 18px}
.ktb td{background:#fff;padding:16px 18px}.ktb td:first-child{border-radius:14px 0 0 14px;font-weight:700}.ktb td:last-child{border-radius:0 14px 14px 0}
.ktb .jp{font-family:"Klee One",serif;font-weight:600;font-size:30px}.ktb tr.hl td{background:#fff0f5;color:#c42f66;font-weight:800}
.klv{display:flex;align-items:flex-end;gap:14px;height:330px;margin-top:10px}.klv div{flex:1;border-radius:18px 18px 0 0;color:#fff;padding:18px;font-size:26px;font-weight:700;display:flex;flex-direction:column;justify-content:flex-end}
.klv b{font-size:44px}.kchk{list-style:none;font-size:29px;line-height:1.75}.kchk li:before{content:"✓";color:#c42f66;font-weight:800;margin-right:14px}
.kno li:before{content:"✕";color:#e0245e}.kex{margin-top:10px;background:#f4f8fc;border-radius:14px;padding:12px 16px;font-size:24px}.kex .jp{font-size:28px}
.tag{display:inline-block;background:#0d5a8c;color:#fff;border-radius:30px;padding:4px 18px;font-size:22px;margin-right:8px}
.slide{background:radial-gradient(700px 480px at 8% 12%,#c6e3fa 0,#c6e3fa00 72%),radial-gradient(800px 520px at 92% 88%,#d2eafc 0,#d2eafc00 72%),radial-gradient(600px 420px at 70% 10%,#eef7ff 0,#eef7ff00 70%),#f7fbff}
.slide.dark{background:radial-gradient(900px 620px at 0% 0%,#a9d4f6 0,#a9d4f600 72%),radial-gradient(800px 600px at 100% 100%,#bde0fa 0,#bde0fa00 72%),radial-gradient(700px 500px at 75% 15%,#e6f3ff 0,#e6f3ff00 70%),radial-gradient(600px 500px at 20% 90%,#dcefff 0,#dcefff00 70%),#f4faff;color:#0d2b40}
.slide.dark .cover .kk{color:#c42f66}.slide.dark .cover h1{color:#0d2b40}.slide.dark .cover h1 span{color:#0d5a8c}.slide.dark .cover p{color:#2f5674}.slide.dark .cover ul{color:#0d2b40}
.slide.dark .cr{color:#7d93a5}.slide.dark .cover .lg{box-shadow:0 6px 18px #0d5a8c22}
</style></head>''', 1)
TAIL = open(R + 'src/tailieu_src/buoi15_tail.html').read()
J = lambda s: furi(html.escape(s))
CR = '<div class="cr">Khai giảng khoá luyện thi JFT-Basic · Anh Trọng Dạy JFT · Số liệu: trang chính thức JFT-Basic (Quỹ Giao lưu Quốc tế Nhật Bản) và Prometric, tra ngày 17/11/2026 – có thể thay đổi, xem lại trước khi đăng ký thi</div>'
S = []
def sl(title, sub, body, dark=False):
    S.append(f'<section class="slide{" dark" if dark else ""}"><h2>{title}{f" <small>{sub}</small>" if sub else ""}</h2>{body}{CR}</section>')

# 1. Bìa
S.append(f'''<section class="slide dark"><div class="cover"><img class="lg" src="{LOGO}"><div class="kk">KHAI GIẢNG · 開講式</div>
<h1>Khoá luyện thi<br><span>JFT-Basic</span></h1><p>Hiểu đúng kỳ thi – học đúng trọng tâm – đạt 200 điểm</p>
<ul><li>Kỳ thi JFT-Basic là gì, dùng để làm gì</li><li>Đề thi gồm những phần nào, thi trên máy ra sao</li><li>Thang điểm, mức đỗ, kết quả và thi lại</li><li>Lộ trình học của lớp mình</li></ul></div>{CR}</section>''')

# 2. JFT là gì
sl('JFT-Basic là gì?', '国際交流基金日本語基礎テスト', f'''<div class="kgr g2">
<div class="kcd kb"><h3>Do ai tổ chức?</h3>Quỹ Giao lưu Quốc tế Nhật Bản (<span class="jp">国際交流基金</span> – The Japan Foundation). Đơn vị vận hành thi: <b>Prometric</b>.</div>
<div class="kcd kp"><h3>Đo cái gì?</h3>Tiếng Nhật <b>dùng trong đời sống</b>: đi chợ, đi tàu, đi làm, nghe thông báo, đọc tờ hướng dẫn… Không phải ngữ pháp học thuật như JLPT.</div>
<div class="kcd ko st"><h3>Dành cho ai?</h3>Người nước ngoài chủ yếu sang Nhật <b>để làm việc</b>.</div>
<div class="kcd kg2 st"><h3>Dùng để làm gì?</h3>Chứng minh trình độ tiếng Nhật khi xin tư cách lưu trú: <b><span class="jp">特定技能1号</span></b> (kỹ năng đặc định), <b><span class="jp">育成就労</span></b>, du học / trường tiếng.</div></div>''')

# 3. Hình thức thi
sl('Thi như thế nào?', 'CBT – thi trên máy tính', f'''<div class="kgr g3">
<div class="kcd kb"><h3>Thi trên máy</h3>Làm bài tại trung tâm Prometric. Đề hiện trên màn hình, nghe bằng tai nghe, bấm chuột chọn đáp án.</div>
<div class="kcd kp"><h3>Thi gần như hằng tháng</h3>Ở Nhật và nhiều nước châu Á, trong đó có <b>Việt Nam</b>. Tự đặt lịch trên web Prometric.</div>
<div class="kcd ko"><h3>Lệ phí</h3>Việt Nam: <b>870.000 đồng</b><br>Nhật Bản: <b>10.000 yên</b><br><span style="font-size:21px;color:#6b8296">(theo trang Prometric, 11/2026)</span></div></div>
<div class="pb st">Đề có câu hỏi bằng <b>tiếng Anh</b> và nút <b>"Your Language"</b> để đọc yêu cầu đề bằng <b>tiếng Việt</b>. Nút này chỉ dịch câu hỏi – <b>không dịch bài đọc, bài nghe hay đáp án</b>.</div>''')

# 4. Cấu trúc đề
sl('Cấu trúc đề thi', 'khoảng 50 câu · 60 phút', f'''<table class="ktb"><tr><th>Phần</th><th>Tên tiếng Nhật</th><th>Số câu</th><th>Hỏi gì?</th></tr>
<tr><td>1. Chữ và từ vựng</td><td class="jp">{J("文字と語彙")}</td><td>~12</td><td>Nghĩa, cách dùng từ · đọc chữ Hán · chọn chữ Hán</td></tr>
<tr><td>2. Hội thoại và diễn đạt</td><td class="jp">{J("会話と表現")}</td><td>~12</td><td>Ngữ pháp đúng · câu nói phù hợp tình huống</td></tr>
<tr><td>3. Nghe hiểu</td><td class="jp">{J("聴解")}</td><td>~12</td><td>Hội thoại · cửa hàng, nơi công cộng · thông báo, hướng dẫn</td></tr>
<tr><td>4. Đọc hiểu</td><td class="jp">{J("読解")}</td><td>~12</td><td>Thư, tin nhắn · tìm thông tin trên biển báo, tờ thông báo</td></tr></table>
<div class="pb st">Tổng <b>60 phút</b> cho cả 4 phần, <b>không chia giờ riêng</b> từng phần → phần đầu làm nhanh để dành thời gian cho Nghe và Đọc.</div>''')

# 5-8 từng phần
sl('Phần 1 · 文字と語彙', 'Chữ và từ vựng', f'''<div class="kgr g4">
<div class="kcd kb"><h3>Nhìn tranh chọn từ</h3><div class="kex">Tranh cái kéo → <span class="jp">はさみ</span></div></div>
<div class="kcd kp"><h3>Điền từ vào câu</h3><div class="kex jp">{J("雨なので、（　）をさします。")} → かさ</div></div>
<div class="kcd ko"><h3>Đọc chữ Hán</h3><div class="kex"><span class="jp">{J("花火")}</span> → はなび<br>(không phải はなひ)</div></div>
<div class="kcd kg2"><h3>Chọn chữ Hán</h3><div class="kex">やすみ → <span class="jp">休み</span><br>(không phải 体み)</div></div></div>
<div class="pb st">Phần <b>dễ lấy điểm nhất</b>. Cẩn thận: âm đục ゛, âm ngắt っ, trường âm, chữ Hán giống nhau (休・体, 右・左…).</div>''')
sl('Phần 2 · 会話と表現', 'Hội thoại và diễn đạt', f'''<div class="kgr g2">
<div class="kcd kb"><h3>Chọn ngữ pháp đúng</h3><div class="kex jp">{J("この薬は、熱が（　）ときに飲んでください。")}<br>→ ある</div></div>
<div class="kcd kp"><h3>Chọn câu nói hợp tình huống</h3><div class="kex jp">{J("「足をけがしてしまいました。」「そうですか。（　）。」")}<br>→ {J("お大事に")}</div></div></div>
<div class="pb st">Không cần dịch cả câu: nhìn <b>chữ đứng sát chỗ trống</b> và <b>câu trả lời phía sau</b>. Học thuộc các câu dùng hằng ngày: <span class="jp">{J("お大事に・また今度・〜んですが")}</span>…</div>''')
sl('Phần 3 · 聴解', 'Nghe hiểu', f'''<div class="kgr g3">
<div class="kcd kb"><h3>Hội thoại giao tiếp</h3>Rủ đi chơi, hỏi thăm, nhờ vả, nói chuyện với đồng nghiệp…</div>
<div class="kcd kp"><h3>Cửa hàng, nơi công cộng</h3>Gọi món, đặt bàn, mua đồ, hỏi đường, ở ga tàu…</div>
<div class="kcd ko"><h3>Thông báo, hướng dẫn</h3>Loa ở ga, thông báo động đất, hướng dẫn uống thuốc, nội quy…</div></div>
<div class="kgr g2 st" style="margin-top:24px"><div class="kcd kg2"><h3>Được nghe tối đa 2 lần</h3>Bấm nút phát để nghe, mỗi câu nghe được <b>tối đa 2 lần</b>.</div>
<div class="kcd kp"><h3>Không quay lại được</h3>Trong phần Nghe <b>không được chuyển</b> sang câu trước/sau, không xem lại hay sửa đáp án.</div></div>''')
sl('Phần 4 · 読解', 'Đọc hiểu', f'''<div class="kgr g2">
<div class="kcd kb"><h3>Đoạn văn ngắn</h3>Thư, email, tin nhắn, bài tự giới thiệu… hỏi nội dung chính, ai làm gì.</div>
<div class="kcd kp"><h3>Tìm thông tin</h3>Bảng lịch, tờ thông báo, poster, hướng dẫn cách làm… hỏi ngày giờ, giá tiền, cách đăng ký.</div></div>
<div class="pb st">Đọc <b>câu hỏi trước</b>, rồi quét tìm từ khoá. Phần này nằm <b>cuối bài</b> – lúc gần hết giờ – nên không dịch từng chữ.</div>''')

# 9. Quy tắc trên máy
sl('Quy tắc làm bài trên máy', 'nhớ kỹ trước ngày thi', f'''<div class="kgr g2"><div><ul class="kchk">
<li>Trong <b>cùng một phần</b>: xem lại, sửa đáp án thoải mái</li><li>Có nút <b>Your Language</b> đọc đề bằng tiếng Việt</li><li>Không biết vẫn chọn 1 đáp án – không bỏ trống</li></ul></div>
<div><ul class="kchk kno"><li>Sang <b>phần tiếp theo</b> là <b>khoá</b> phần trước</li><li>Phần Nghe: không quay lại câu trước</li><li>Không có giờ riêng từng phần – tự canh giờ</li></ul></div></div>
<div class="pb st">Trước khi bấm sang phần mới: kiểm tra <b>câu nào cũng đã chọn</b> và đã xem lại các câu còn phân vân.</div>''')

# 10. Thang điểm
sl('Thang điểm và mức đỗ', 'quan trọng nhất', f'''<div class="kgr" style="grid-template-columns:1fr 1.25fr;align-items:center">
<div><div class="kbig">200<small> / 250</small></div><div style="font-size:30px;margin-top:16px">Điểm từ <b>200</b> trở lên = đạt mức <b>A2</b><br>→ dùng cho <b><span class="jp">特定技能1号</span></b></div>
<div class="kex" style="margin-top:20px">Thang điểm: <b>10 – 250</b>. Điểm dưới 145 không hiện số (ghi “＊”).</div></div>
<div class="klv"><div style="height:42%;background:#9fb3c4">dưới 145<b>＊</b></div><div style="height:60%;background:#7cb342">145–174<b>A1</b></div><div style="height:78%;background:#f2a93b">175–199<b>A2.1</b></div><div style="height:100%;background:#c42f66">200–250<b>A2.2 (A2)</b></div></div></div>
<div class="pb st">Từ <b>tháng 8/2026</b> JFT-Basic chia thêm mức <b>A1</b> và <b>A2.1</b> (dùng cho chế độ <span class="jp">育成就労</span>). Đi <b>Tokutei</b> vẫn cần <b>200 điểm</b>.</div>''')
sl('Điểm được tính thế nào?', 'không phải đếm số câu đúng', f'''<div class="kgr g2">
<div class="kcd kb"><h3>Điểm quy đổi</h3>Tổng điểm là điểm đã <b>quy đổi theo độ khó</b> của câu hỏi, không phải "mỗi câu một điểm". Vì vậy không có con số "sai mấy câu thì trượt".</div>
<div class="kcd kp"><h3>Không có điểm liệt từng phần</h3>Chỉ xét <b>tổng điểm</b> cả 4 phần. Phần nào yếu thì phần khác phải bù.</div></div>
<div class="pb st">Phiếu kết quả có ghi <b>tỉ lệ trả lời đúng của từng phần</b> – chỉ để tham khảo, giúp biết mình yếu phần nào.</div>''')

# 11. Kết quả
sl('Kết quả thi', 'biết ngay tại phòng thi', f'''<div class="kgr g3">
<div class="kcd kb"><h3>Ngay khi thi xong</h3>Tổng điểm và mức đạt <b>hiện ngay trên màn hình</b>.</div>
<div class="kcd kp"><h3>Trong 5 ngày làm việc</h3>Có <b>phiếu kết quả chính thức</b> (<span class="jp">判定結果通知書</span>) trên web Prometric, tự in ra.</div>
<div class="kcd ko"><h3>Không hết hạn</h3>Kết quả <b>không có hạn</b>, nhưng chỉ xem được trên web <b>5 năm</b> → in và lưu ngay.</div></div>''')

# 12. Thi lại
sl('Thi lại', 'trượt thì sao?', f'''<div class="kgr g2">
<div class="kcd ko"><h3>Dưới 200 điểm</h3>Được thi lại, nhưng phải <b>cách ít nhất 45 ngày</b> tính từ ngày hôm sau của ngày thi.</div>
<div class="kcd kp"><h3>Đã đạt 200 trở lên</h3><b>Không được thi lại</b> nữa.</div></div>
<div class="pb st">Đã đặt lịch thì <b>không huỷ được</b>, vắng mặt cũng <b>không hoàn lệ phí</b>. 45 ngày chờ thi lại khá lâu → cố gắng đỗ ngay lần đầu.</div>''')

# 13. Đăng ký & ngày thi
sl('Đăng ký và ngày thi', 'các bước', f'''<div class="steps four"><div><b>1</b><h3>Tạo Prometric ID</h3><p>Mỗi người 1 ID. Họ tên, số hộ chiếu, ngày sinh <b>đúng y hộ chiếu</b>.</p></div>
<div><b>2</b><h3>Đặt lịch, trả phí</h3><p>Chọn nơi thi, ngày thi. Hạn đặt/đổi lịch: <b>3 ngày làm việc</b> trước ngày thi.</p></div>
<div><b>3</b><h3>Ngày thi</h3><p>Mang <b>thư xác nhận</b> + <b>giấy tờ tuỳ thân bản gốc</b> còn hạn, có ảnh. Bản photo, ảnh chụp trên điện thoại không được.</p></div>
<div><b>4</b><h3>Nhận kết quả</h3><p>Xem điểm ngay, tải phiếu kết quả trên web sau 5 ngày làm việc.</p></div></div>''')

# 14. Lộ trình lớp
sl('Lộ trình lớp mình', 'học gì – luyện thế nào', f'''<div class="kgr g3">
<div class="kcd kb"><h3>Giáo trình</h3><span class="jp">いろどり 生活の日本語</span> – đúng giáo trình mà đề JFT bám theo.</div>
<div class="kcd kp"><h3>25 buổi × 90 phút</h3>Chữ Hán, từ vựng, ngữ pháp theo buổi · luyện Nghe – Đọc theo dạng đề · bài tập về nhà mỗi buổi.</div>
<div class="kcd ko"><h3>App luyện thi</h3>Làm đề giống máy thi thật (có giải thích từng câu), video bài giảng, flashcard từ vựng, đề nghe.</div></div>
<div class="pb st">Mục tiêu chung của cả lớp: <b>200 điểm ngay lần thi đầu tiên</b>.</div>''')

# 15. Kết
S.append(f'''<section class="slide dark"><div class="cover"><img class="lg" src="{LOGO}"><div class="kk">よろしくお願いします！</div>
<h1>Cùng nhau<br><span>đạt 200 điểm!</span></h1><p>Có câu hỏi gì, nhắn Anh Trọng bất cứ lúc nào.</p>
<ul><li>Facebook: facebook.com/anh.trongg.2024</li><li>TikTok: @anhtrong.daygino</li></ul></div>{CR}</section>''')

out = HEAD.replace('<title>Kính ngữ trong JFT-Basic</title>', '<title>Khai giảng khoá luyện thi JFT-Basic</title>') + ''.join(S) + TAIL
open(R + 'public/tailieu/KhaiGiang_JFTBasic.html', 'w').write(out)
print(len(S), 'slides')
