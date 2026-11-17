import os
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
.kcd{background:#fff;border-radius:22px;padding:30px 30px;box-shadow:0 8px 24px #0d2b4012;font-size:32px;line-height:1.5}
.kcd h3{font-size:34px;margin-bottom:10px;color:#0d5a8c}
.kshw{display:grid;grid-template-columns:1fr 1fr;gap:34px;margin-top:6px}
.kshw.one{grid-template-columns:auto 1fr;align-items:center}.kshw.one .ksh img{height:620px}
.ksh{margin:0}.ksh figcaption{font-size:30px;font-weight:800;color:#0d5a8c;margin:0 0 10px 4px}
.ksh{text-align:center}.ksh figcaption{text-align:left}
.ksh img{height:505px;width:auto;max-width:100%;display:inline-block;border-radius:14px;border:3px solid #0d2b40;box-shadow:0 12px 30px #0d2b4026;background:#fff}
.kshw+.pb{margin-top:20px}.kcd .jp{font-family:"Klee One",serif;font-weight:600}
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
<h1>Khoá luyện thi<br><span>JFT-Basic</span></h1><p>Mục tiêu 200 điểm</p>
<ul><li>Giới thiệu kỳ thi</li><li>Cấu trúc đề thi</li><li>Thang điểm · kết quả · thi lại</li><li>Lộ trình lớp học</li></ul></div>{CR}</section>''')

# 2. JFT là gì
sl('Giới thiệu kỳ thi', '国際交流基金日本語基礎テスト', f'''<div class="kgr g2">
<div class="kcd kb"><h3>Đơn vị tổ chức</h3>Quỹ Giao lưu Quốc tế Nhật Bản · thi tại <b>Prometric</b></div>
<div class="kcd kp"><h3>Nội dung đánh giá</h3>Tiếng Nhật <b>giao tiếp đời sống</b> và công việc</div>
<div class="kcd ko st"><h3>Đối tượng</h3>Người nước ngoài sang Nhật <b>làm việc</b></div>
<div class="kcd kg2 st"><h3>Mục đích sử dụng</h3>Visa <b><span class="jp">特定技能1号</span></b> · <span class="jp">育成就労</span> · du học</div></div>''')

# 3. Hình thức thi
sl('Hình thức thi', 'CBT', f'''<div class="kgr g3">
<div class="kcd kb"><h3>Thi trên máy</h3>Đề trên màn hình · nghe bằng tai nghe · bấm chọn đáp án</div>
<div class="kcd kp"><h3>Lịch thi</h3>Gần như <b>hằng tháng</b> · Việt Nam và Nhật</div>
<div class="kcd ko"><h3>Lệ phí</h3>Việt Nam: <b>870.000đ</b><br>Nhật: <b>10.000 yên</b></div></div>
<div class="pb st">Nút <b>Your Language</b>: đọc yêu cầu đề bằng tiếng Việt (không dịch bài đọc, bài nghe, đáp án)</div>''')

# 4. Cấu trúc đề
sl('Cấu trúc đề thi', '~50 câu · 60 phút', f'''<table class="ktb"><tr><th>Phần</th><th></th><th>Số câu</th><th>Nội dung</th></tr>
<tr><td>1. Chữ – Từ vựng</td><td class="jp">{J("文字と語彙")}</td><td>~12</td><td>Nghĩa từ · đọc / chọn chữ Hán</td></tr>
<tr><td>2. Hội thoại – Diễn đạt</td><td class="jp">{J("会話と表現")}</td><td>~12</td><td>Ngữ pháp · câu nói hợp tình huống</td></tr>
<tr><td>3. Nghe hiểu</td><td class="jp">{J("聴解")}</td><td>~12</td><td>Hội thoại · cửa hàng · thông báo</td></tr>
<tr><td>4. Đọc hiểu</td><td class="jp">{J("読解")}</td><td>~12</td><td>Tin nhắn, thư · tìm thông tin</td></tr></table>
<div class="pb st"><b>60 phút</b> chung cho 4 phần – không chia giờ riêng</div>''')

# 5-8 từng phần: ảnh màn hình bài thi (chụp từ màn làm đề của app, Đề 25)
import base64 as _b64
_KGS=os.path.join(os.path.dirname(os.path.abspath(__file__)),'khaigiang_img')
def SC(n):
    return 'data:image/jpeg;base64,'+_b64.b64encode(open(f'{_KGS}/q{n}.jpg','rb').read()).decode()
def SH(items, tip=''):
    cells=''.join(f'<figure class="ksh"><figcaption>{c}</figcaption><img src="{SC(n)}"></figure>' for c,n in items)
    return f'<div class="kshw">{cells}</div>'+(f'<div class="pb st">{tip}</div>' if tip else '')
sl('Màn hình thi', '', f'''<div class="kshw one"><figure class="ksh"><img src="{SC(0)}"></figure>
<div class="kgr" style="grid-template-columns:1fr;gap:16px">
<div class="kcd kb"><h3>Trên cùng</h3>Số câu · tên phần · thời gian còn lại · <b>Finish Section</b></div>
<div class="kcd kp"><h3>Bên trái</h3>Danh sách câu · bấm để nhảy câu</div>
<div class="kcd ko"><h3>Dưới cùng</h3>⚑ đánh dấu · Back / Next</div></div></div>''')
sl('Phần 1 · 文字と語彙', 'Chữ – Từ vựng (1/2)', SH([('Tranh → từ',0),('Điền từ',3)]))
sl('Phần 1 · 文字と語彙', 'Chữ – Từ vựng (2/2)', SH([('Đọc chữ Hán',6),('Chọn chữ Hán',9)],'Chú ý ゛ っ trường âm · chữ giống nhau (薬・楽・葉)'))
sl('Phần 2 · 会話と表現', 'Hội thoại – Diễn đạt', SH([('Câu nói theo tình huống',12),('Ngữ pháp',22)],'Nhìn <b>câu đáp phía sau</b> chỗ trống'))
sl('Phần 3 · 聴解', 'Nghe hiểu', SH([('Lựa chọn bằng chữ',24),('Lựa chọn bằng tranh',33)],'Bấm ▶ để nghe · tối đa <b>2 lần</b> · không quay lại câu trước'))
sl('Phần 4 · 読解', 'Đọc hiểu', SH([('Bảng thông tin',38),('Thông báo',44)],'Đọc <b>câu hỏi trước</b> → quét từ khoá'))
# 9. Quy tắc trên máy
sl('Quy tắc thi trên máy', '', f'''<div class="kgr g2"><div><ul class="kchk">
<li>Sửa đáp án <b>trong cùng phần</b></li><li>Nút <b>Your Language</b></li><li>Không bỏ trống câu nào</li></ul></div>
<div><ul class="kchk kno"><li>Sang phần mới = <b>khoá</b> phần cũ</li><li>Phần Nghe không quay lại</li><li>Không có giờ riêng từng phần</li></ul></div></div>''')

# 10. Thang điểm
sl('Thang điểm và mức đỗ', '', f'''<div class="kgr" style="grid-template-columns:1fr 1.25fr;align-items:center">
<div><div class="kbig">200<small> / 250</small></div><div style="font-size:30px;margin-top:16px">Đạt mức <b>A2</b> → <b><span class="jp">特定技能1号</span></b></div>
<div class="kex" style="margin-top:20px">Thang <b>10 – 250</b> · dưới 145 ghi “＊”</div></div>
<div class="klv"><div style="height:42%;background:#9fb3c4">dưới 145<b>＊</b></div><div style="height:60%;background:#7cb342">145–174<b>A1</b></div><div style="height:78%;background:#f2a93b">175–199<b>A2.1</b></div><div style="height:100%;background:#c42f66">200–250<b>A2.2 (A2)</b></div></div></div>
<div class="pb st">Mức A1, A2.1 có từ <b>8/2026</b> (cho <span class="jp">育成就労</span>) · Tokutei vẫn cần <b>200</b></div>''')
sl('Cách tính điểm', '', f'''<div class="kgr g2">
<div class="kcd kb"><h3>Điểm quy đổi</h3>Tính theo <b>độ khó</b> từng câu, không phải số câu đúng</div>
<div class="kcd kp"><h3>Điểm liệt</h3><b>Không có</b> · chỉ xét tổng 4 phần</div></div>
<div class="pb st">Phiếu kết quả có <b>tỉ lệ đúng từng phần</b> (tham khảo)</div>''')

# 11. Kết quả
sl('Kết quả thi', '', f'''<div class="kgr g3">
<div class="kcd kb"><h3>Thi xong</h3>Điểm hiện <b>ngay trên màn hình</b></div>
<div class="kcd kp"><h3>Sau 5 ngày làm việc</h3>Phiếu kết quả (<span class="jp">判定結果通知書</span>) trên web Prometric</div>
<div class="kcd ko"><h3>Thời hạn</h3><b>Không hết hạn</b> · web lưu 5 năm → in giữ</div></div>''')

# 12. Thi lại
sl('Thi lại', '', f'''<div class="kgr g2">
<div class="kcd ko"><h3>Dưới 200 điểm</h3>Thi lại sau <b>45 ngày</b></div>
<div class="kcd kp"><h3>Từ 200 điểm</h3><b>Không</b> được thi lại</div></div>
<div class="pb st">Không huỷ lịch · vắng thi không hoàn phí</div>''')

# 13. Đăng ký & ngày thi
sl('Đăng ký và ngày thi', '', f'''<div class="steps four"><div><b>1</b><h3>Prometric ID</h3><p>Thông tin <b>đúng hộ chiếu</b></p></div>
<div><b>2</b><h3>Đặt lịch</h3><p>Trước ngày thi <b>3 ngày làm việc</b></p></div>
<div><b>3</b><h3>Ngày thi</h3><p>Thư xác nhận + <b>giấy tờ gốc</b></p></div>
<div><b>4</b><h3>Kết quả</h3><p>Xem ngay · tải phiếu sau 5 ngày</p></div></div>''')

# 14. Lộ trình lớp
sl('Lộ trình lớp học', '', f'''<div class="kgr g3">
<div class="kcd kb"><h3>Giáo trình</h3><span class="jp">いろどり 生活の日本語</span></div>
<div class="kcd kp"><h3>Thời lượng</h3><b>25 buổi</b> × 90 phút</div>
<div class="kcd ko"><h3>App luyện thi</h3>Đề có giải thích · video · flashcard</div></div>
<div class="pb st">Mục tiêu: <b>200 điểm ngay lần đầu</b></div>''')

# 15. Kết
S.append(f'''<section class="slide dark"><div class="cover"><img class="lg" src="{LOGO}"><div class="kk">よろしくお願いします！</div>
<h1>Cùng nhau<br><span>đạt 200 điểm!</span></h1>
<ul><li>Facebook: facebook.com/anh.trongg.2024</li><li>TikTok: @anhtrong.daygino</li></ul></div>{CR}</section>''')

out = HEAD.replace('<title>Kính ngữ trong JFT-Basic</title>', '<title>Khai giảng khoá luyện thi JFT-Basic</title>') + ''.join(S) + TAIL
open(R + 'public/tailieu/KhaiGiang_JFTBasic.html', 'w').write(out)
print(len(S), 'slides')
