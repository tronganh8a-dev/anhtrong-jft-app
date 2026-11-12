# Bàn giao: App học & luyện thi JFT — Anh Trọng Dạy JFT

> Dán file này cho trợ lý mới (hoặc mở repo bằng Claude Code: file này tự được đọc).
> Cập nhật lần cuối: 23/10/2026.

## 0. Cách làm việc với anh Trọng Anh
- Trả lời **tiếng Việt, ngắn gọn**, xưng "em", gọi "anh". Báo: đã làm gì, còn thiếu gì — không kể từng bước.
- Yêu cầu mơ hồ → hỏi **1 câu** trước khi làm. Cái gì đã có → gửi lại, đừng làm lại từ đầu.
- Tiếng Nhật lấy **nguyên văn từ sách いろどり**; nội dung tự soạn phải ghi rõ là tự soạn. Có dòng 出典 (nguồn) ở mọi nơi dùng dữ liệu giáo trình.
- Giải thích kanji thì kèm âm Hán Việt.
- **Không** chép dữ liệu Mazii, vnjpclub/Minna no Nihongo. Giữ credit `VOICEVOX:青山龍星` và `Kanjium (CC BY-SA 4.0)`.
- Không tự nhập mật khẩu/token thay anh; anh tự làm trên Cloudflare/GitHub.

## 1. Tổng quan
- App web tĩnh (SPA) học giáo trình **いろどり 生活の日本語** (入門, 初級1, 初級2, 初中級) + luyện thi JFT-Basic.
- Repo: `tronganh8a-dev/anhtrong-jft-app` (private), nhánh `main`.
- Host: **Cloudflare Workers** (Workers Builds tự build khi push `main`, ~2–3 phút):
  - Bản chính: worker `anhtrong-jft-app` → https://anhtrong-jft-app.tronganh8a.workers.dev (có đăng nhập)
  - Bản dùng thử: worker `jft-dungthu` (Root directory = `demo/`), không đăng nhập. Hiện đủ danh mục nhưng KHOÁ (🔒 + popup liên hệ), mỗi phần chỉ mở mục đầu tiên/mặc định; mục khoá chỉ mang tiêu đề, không chép nội dung. Trang chủ bỏ nút Đăng ký/Đăng nhập Prometric. LƯU Ý: worker jft-dungthu thực tế chạy worker.js gốc → worker.js nhận tên miền `jft-dungthu.*` và chỉ phục vụ `public/_demo/` (bản sao demo do build_demo.py tạo), không đăng nhập.
- Sau mỗi lần push, kiểm tra build:
  `gh api repos/tronganh8a-dev/anhtrong-jft-app/commits/<sha>/check-runs` → cả 2 phải `success`.
  (Từng bị lỗi build ngẫu nhiên → đẩy 1 commit rỗng là build lại được.)

## 2. Các tab trong app
Trang chủ (hero gradient + dải 4 màu sách, lịch thi & link Prometric, hướng dẫn điểm đậu) · **Tài liệu** (trước là "Học qua slide": 4 mục Slide bài giảng / Từ vựng / Chữ Hán / Ngữ pháp, 3 cấp 入門・初級1・初級2) · Làm đề (CBT giống máy thi; chế độ Thi thử / Luyện tập có giải thích, bật tắt furigana) · **Video** (thay tab Luyện kỹ năng 23/10) · Từ vựng (flashcard, trọng âm, audio, ví dụ).
- (11/11) Tab **Ngữ pháp** và **Bài tập về nhà** đã gộp vào Tài liệu: Tài liệu có 6 mục Theo buổi học / Slide / Từ vựng / Chữ Hán / Ngữ pháp / Bài tập về nhà. Mục Ngữ pháp = bản 文法ノート いろどり (đủ hơn: 4 cấp, 348 mẫu, có worksheet + audio; khối `#dGram`, `renderGram`); bản ngữ pháp từ PDF cô Quỳnh (`DOCS.gram`, `dGram()`) không còn hiển thị. Bài tập về nhà = khối `#dHw` (`renderHw`), màn xem bài `#hwv` bấm quay lại về Tài liệu.

- **Tài liệu → Từ vựng/Chữ Hán/Ngữ pháp**: dữ liệu từ 7 file PDF tổng hợp của lớp cô Quỳnh (23/10). Nguồn trích: `src/docs/*_src.json`; phần soạn (sửa lỗi trích, âm Hán Việt, phân tích On/Kun, mẹo nhớ, giải thích ngữ pháp, ví dụ tự soạn, 3 câu quiz/mẫu) ở `src/docs/ans/*.json` (theo `src/docs/SPEC_*.md`); `quizfix_*.json` = sửa sau kiểm định. Dựng: `python3 src/build_docs.py` → `public/app/data/docs.js` (tải khi mở tab). Ảnh từ vựng: `public/app/media/doc/<md5>.jpg`. Bài luyện tập tự sinh ở trình duyệt (nhìn tranh chọn từ, chọn nghĩa, chọn cách đọc, chọn chữ Hán) và dùng giao diện CBT `startSkill`.
- **Tài liệu → Theo buổi học** (23/10): file HTML tài liệu từng buổi ở `public/tailieu/` (vd. `Buoi02_*.html`), danh sách khai báo trong mảng `BUOI` của `src/index_tpl.html` (k:'slide' = khung 16:9, k:'web' = khung cao). Thêm buổi mới: chép file vào `public/tailieu/` + thêm 1 dòng vào `BUOI` → build_index.
- **Bút dạ giảng bài** (24/10): nút tròn hồng góc phải ở Tài liệu / khung slide / Ngữ pháp / Từ vựng → thanh công cụ: Chuột, Bút, Highlight (kéo ra dải thẳng, tự nắn ngang), Chữ (bấm rồi gõ, font --mix của app), Memo (giấy ghi chú màu, kéo để di chuyển; bấm vào chữ/memo để sửa), Tẩy (xoá theo nét), 5 màu, 3 cỡ nét, Hoàn tác, Xoá hết, Ẩn nét, Tắt (giống thanh bút của web Gino). Phím: P/H/T/M/E/V, Ctrl+Z, Delete. Trong khung slide: ←/→/PageDown được chuyển tiếp vào slide và tự xoá nét cũ (Ctrl+Z lấy lại). Chạy cả khi toàn màn hình. Code: khối "bút dạ giảng bài" cuối `src/index_tpl.html`. (11/11) Thanh bút kéo được (nút chấm ⋮⋮, bấm đúp = về chỗ cũ), nút xoay ngang/dọc (dọc = lưới 2 cột); vị trí lưu localStorage `pen-bar`. Highlight vẽ trên canvas riêng `#penHl` (mix-blend-mode:multiply, alpha .85) → màu đậm mà chữ vẫn rõ. (12/11) Nút Bút hiện ở MỌI trang của app (trừ màn đăng nhập). Nút **Sổ tay** (phím N) trên thanh bút → khung `#soP` (kéo tiêu đề để di chuyển, kéo góc để đổi cỡ, vị trí lưu `so-pos`): ghi chú có tiêu đề + nội dung + nơi ghi (tự lấy tên trang/đề/video), tìm kiếm, xoá (bấm 2 lần). Lưu theo tài khoản: `GET/POST /api/so` → Durable Object `Phien`, khoá `so` (gộp theo thời điểm sửa `u`, xoá = `{del:1}`); bộ đệm localStorage `jftSo_<user>`.
- **Video**: buổi chưa có video thì để `"yt": ""` → trang hiện "Video sắp có", vẫn có slide/tài liệu; mặc định mở video mới nhất ĐÃ có yt. Danh sách ở `src/raw/videos.json` → `python3 src/build_videos.py`. YouTube nhúng với `controls=0`, thanh điều khiển riêng của app, khung iframe kéo cao 90px mỗi đầu để ẩn tiêu đề YouTube. Không chọn được chất lượng (YouTube khoá); anh không dùng R2 (không có thẻ thanh toán).
- **Đăng nhập**: (12/11) LƯU đăng nhập 5 ngày (`DAYS = 5` trong auth.js; cookie hạn dài hơn bị coi là hết hạn). Bỏ kiểm tra `jft_once` — tải lại trang không phải đăng nhập lại.
- **Cache**: trang HTML và `/app/data/*` trả `private, no-cache` (ảnh/audio 1 giờ); build_index gắn `?v=<md5>` vào link data → sửa là thấy ngay.
- **Video – màn hình lớn + Lý thuyết (06/11/2026)**: bấm phát (máy tính) là tự vào màn hình lớn (`body.cine`, hàm `vBig`). Tab hồng dọc "📖 Lý thuyết buổi học" ở mép phải / nút 📖 trên thanh điều khiển → khung `#vSide` bên phải (các tab tài liệu, ⇔ đổi độ rộng 34/42/52vw, ↗ mở tab riêng, ✕ đóng). Tài liệu lấy từ `slides` của video + mục cùng số buổi trong `BUOI` (hàm `vDocs`; chỉ video đã có yt). Điện thoại: nút 📖 mở tài liệu đầu tiên bằng openDocView. Ảnh bìa video (`#vCover`) được ghim lên khung YouTube khi chưa phát / tạm dừng (kèm "Tiếp tục từ…"), lớp `#vShield` chặn chuột lúc đang phát (bấm = tạm dừng) → không lộ logo, nút, gợi ý video của YouTube. Nút chat AI ẩn khi ở màn hình lớn.
- **Trang video**: trường `slides` trong `videos.json` (đường dẫn `tailieu/...`) → hàng "Slide buổi học" dưới video, bấm mở trong khung xem của app (openDocView).

Link Prometric trên trang chủ:
- Lịch thi ở VN/nước ngoài: https://www.prometric-jp.com/ssw/schedule/jft_basic_overseas/
- Lịch thi ở Nhật: https://www.prometric-jp.com/ssw/schedule/jft_basic_domestic/
- Đăng ký ID: https://j6.prometric-jp.com/IdGet/IdNew?CN=JL&LC=JA
- Đăng nhập: https://j6.prometric-jp.com/Reserve/Login?CN=JL&LC=JA
Liên hệ của anh: Facebook https://www.facebook.com/anh.trongg.2024/ · TikTok @anhtrong.daygino

## 3. Cấu trúc repo
```
public/                 web chạy thật (~930MB)
  index.html            SINH RA từ src/index_tpl.html — đừng sửa tay
  app/data/*.js         lessons, exams, skills, vocab, grammar, hw (SINH RA)
  app/media/            img/, gimg/, au/ (audio bài nghe), vau/ (audio từ vựng), cover/ (bìa sách)
  lessons/s1|s2|sc/     Irodori_<Cấp>_BaiNN.html + _Slide.html
  btvn/                 bài tập về nhà HTML + pdf/
src/
  index_tpl.html        giao diện (HTML/CSS/JS 1 file)
  build_index.py        → public/index.html (bản online: unlock(), logout → /logout, tên user từ cookie jft_user)
  build_data.py         → public/app/data/*.js (tự gọi pitch/add_pitch.py + pitch/add_examples.py ở cuối)
  build_demo.py         → demo/public (bản dùng thử: mở 1 mục đầu mỗi phần, còn lại khoá – lớp khoá chèn bằng JS cuối file)
  raw/lt_exams.json     (đã xoá 22/10 — bộ đề cũ; build_data chạy được khi không có file)
  raw/skills_raw.json   câu luyện kỹ năng (do skills_extract.py sinh)
  raw/titles.txt        danh sách bài
  skills_extract.py     trích câu nghe/đọc từ web bài học (cần các file *_body.html — xem mục 6)
  vocab/, gram/out/     dữ liệu từ vựng, ngữ pháp
  pitch/                trọng âm (Kanjium), câu ví dụ, audio VOICEVOX
  btvn/                 sinh bài tập về nhà (extract.py, gen_btvn.py, render.py)
  shrink.py             nén audio trong file bài học
auth.js / worker.js / functions/_middleware.js / wrangler.jsonc   đăng nhập phía server
demo/                   bản dùng thử (wrangler.jsonc riêng, không có auth)
CAP-NHAT.md             hướng dẫn cập nhật cho anh
```

Quy trình sau khi sửa: `python3 src/build_data.py` (nếu đổi dữ liệu) → `python3 src/build_index.py` → `python3 src/build_demo.py` (nếu muốn bản dùng thử theo) → test local (`cd public && python3 -m http.server 8812`) → commit → push → kiểm tra check-runs.

## 4. Đăng nhập (auth.js)
- Tài khoản học viên: biến môi trường `ACCOUNTS` trên Cloudflare dạng `ten:matkhau, ten2:matkhau2`; khoá ký cookie: `SECRET`. **Không nằm trong repo.** Đổi ở Cloudflare → app → Settings → Variables and Secrets → Deploy.
- Cookie `jft_s` (ký HMAC, 5 ngày từ 12/11) + `jft_user`. `jft_once` vẫn được đặt khi đăng nhập nhưng không còn bắt buộc.
- **1 tài khoản = 1 thiết bị** (06/11; **BẬT mặc định từ 11/11** theo yêu cầu anh — tắt bằng biến môi trường `MOTMAY=0`): cookie `jft_s` = `ten|hethan|phien|chuky`; mỗi lần đăng nhập tạo mã phiên mới, lưu ở Durable Object `Phien` (binding `PHIEN`, migration v2, 1 object/tài khoản). Máy cũ bị đẩy ra khi mở trang, tải `/app/data/*`, gọi `/api/*`, hoặc nhịp `/api/phien` mỗi 60s → `/login?kick=1`. Biến `NHIEUMAY=ten1,ten2` = tài khoản được dùng nhiều máy (vd giáo viên). (12/11) **Dùng cùng lúc 2 thiết bị → đá cả hai + khoá 5 phút** (giống app Gino): mã thiết bị `jft_dev` (cookie 1 năm); `Phien` thêm khoá `cur` {sid,dev,did,at,seen} + `lock`, đường `/claim` `/st` `/touch` `/drop`; máy đang mở app báo hoạt động qua `/api/phien` và mỗi lần mở trang; đăng nhập khi máy KHÁC còn hoạt động trong 2,5 phút (`ACTIVE`) → khoá `LOCK` 5 phút, trang đăng nhập báo số phút còn lại (`?kick=2&l=`).
- **Bảo vệ nội dung** (11/11): auth.js (hàm `bv`) chèn `window.__WM=<tên tài khoản>` + `/app/bv.js` vào MỌI trang HTML đã đăng nhập (app, tailieu, lessons, btvn, iframe) → watermark "tên · Anh Trọng Dạy JFT · ngày giờ" phủ kín màn hình (tự gắn lại nếu bị xoá, theo cả toàn màn hình); chặn chuột phải, bôi đen, copy, kéo ảnh, Ctrl+S/U/P, F12/Ctrl+Shift+I/J/C; In bị chặn (trừ BTVN: in được, watermark in kèm); PrintScreen → màn đen 1,5s. Đổi bv.js thì tăng `?v=` trong auth.js. Bản demo không có.
- `/app/media/cover/*` công khai (ảnh bìa ở trang đăng nhập). Trang đăng nhập dùng font M PLUS Rounded 1c, có bìa sách + nút Facebook/TikTok.

## Tiến độ học theo tài khoản (12/11)
- Lưu: đề đã mở, đề đã làm (số lần, điểm cao nhất/lần cuối), video đã xem (% xa nhất, ✓ khi ≥90% hoặc xem hết). Biến `TD={ex:{id:{o,lo,n,b,l,t}},vid:{id:{p,d,t}}}` trong index_tpl (khối "tiến độ học theo tài khoản"); bộ nhớ đệm localStorage `jftTD_<user>`.
- Máy chủ: `GET/POST /api/tiendo` (auth.js) → Durable Object `Phien` của tài khoản, khoá `td`; hàm `gopTD` gộp kiểu lấy số lớn nhất nên không bao giờ mất tiến độ. Không cần tạo D1.
- Hiển thị: thẻ "Tiến độ học của em" trên trang chủ (`#tdCard`: % tổng = (đề đã làm + video đã xem)/(tổng đề + tổng video có yt), 3 ô Đề đã làm / Đề đã mở / Video đã xem, đề làm gần đây); nhãn trên thẻ đề và thẻ video. Chưa có trang giáo viên xem tiến độ.

## Bài kiểm tra theo buổi (26/10)
- Link làm bài **công khai, không cần đăng nhập**: `/kiemtra/<id>` (vd `/kiemtra/buoi04`) – file `public/kiemtra/<id>.html` (KHÔNG chứa đáp án).
- Nộp: `POST /api/kiemtra/nop` → `kiemtra.js` chấm theo `kiemtra/<id>.json` (đáp án + giải thích, ngoài public/, import qua `kiemtra/tests.js`) → lưu vào Durable Object `KiemTra` (SQLite, binding `KT`, khai báo trong wrangler.jsonc, migration v1).
- Giáo viên xem: `/kiemtra/ketqua` (đăng nhập; nếu đặt biến môi trường `GIAOVIEN=ten1,ten2` thì chỉ các tài khoản đó xem được – CHƯA đặt thì mọi tài khoản đăng nhập đều xem được). Có tải CSV, xoá bài nộp, tỉ lệ đúng từng câu.
- Tạo bài mới: sửa/nhân bản `src/kiemtra/gen.py` (chọn câu, đổi `id`) → chạy → sinh `public/kiemtra/<id>.html` + `kiemtra/<id>.json` + `kiemtra/tests.js`. Thêm link vào `BUOI` trong index_tpl.
- Thử local: `.dev.vars` (ACCOUNTS, GIAOVIEN – không commit) + `npx wrangler dev`.

## Bảng tin trang chủ (27/10)
- Mảng `NEWS` trong `src/index_tpl.html` (id, d=YYYY-MM-DD, tag, t, s, n=số ảnh). Ảnh ở `public/app/media/news/<id>/01.webp…` (khổ 1080×1350, webp q86). Bài < 7 ngày có nhãn MỚI.
- Bấm thẻ → popup xem ảnh (lướt, phím ←/→, Esc, chấm tròn). Markup popup chèn bằng JS (`#nmodal`).

- **Đề 14–24** (08/11/2026): 11 Google Form của anh (không có phần nghe, 375 câu) → id `jft-g14..g24`, ảnh `public/app/media/jft/img/g<form>_<md5>.jpg`. Nguồn + đáp án/giải thích + sửa lỗi ở `src/jft/gform/` (`ans/f*.txt`: `chỉ số|V/K/R|đáp án|dịch|giải thích`, `ans/fixes.py`); chạy lại: `python3 src/jft/gform/merge_app.py` (cần /tmp/gf/img — ảnh gốc tải từ form) rồi build_data.
- **Đề 25** (09/11/2026): đề anh soạn trên YouTube (いろどり 初級1 第1回, 48 câu, CÓ NGHE) → id `jft-y1`. Audio cắt từ video `app/media/jft/au/y1_L01..12.mp3`, bài đọc dựng lại thành ảnh (`src/jft/youtube/make.js`), dữ liệu + giải thích ở `src/jft/youtube/build_y1.py` (cần /tmp/yt/img, /tmp/yt/au).
- **Đề 26** (10/11/2026): video "ĐỀ JFT 2" → id `jft-y2`, audio `y2_L01..12.mp3`, dữ liệu `src/jft/youtube/build_y2.py` (+ make2.js; cần /tmp/yt2/img, /tmp/yt2/au). Đề 25–26 có trường `tag:"Đề mới chuẩn"` → thẻ viền hồng + nhãn. Đề 14–26 đã bỏ trường `short` (trước bị hiện kiểu thẻ "Ôn tập", font lệch).
- **Đề 27** (10/11/2026): video "ĐỀ JFT 3" → id `jft-y3`, audio `y3_L01..12.mp3`, dữ liệu `src/jft/youtube/build_y3.py` (+ make3.js; cần /tmp/yt3/img, /tmp/yt3/au). Video gốc xếp phần Nghe trước, app vẫn xếp Từ vựng → Hội thoại → Nghe → Đọc.
- **Popup đề mới** (10/11): hằng `NEWX={until,ids}` trong index_tpl → hiện khi mở app đến hết ngày `until`, nút "Luyện ngay" mở thẳng đề; popup quảng cáo AI (promoAi) đã TẮT 10/11 theo yêu cầu anh (dòng `return;` đầu khối promoAi trong index_tpl); nút hỏi AI vẫn giữ.
- **Đề thi**: 22/10 anh yêu cầu **xoá toàn bộ bộ đề cũ** (đã xoá `src/raw/lt_exams.json`, tab Làm đề hiện "Bộ đề mới đang được cập nhật"). Anh sẽ gửi **đề mới** → nhập vào app, **bắt buộc có đáp án + giải thích**: làm xong được chấm và xem đáp án đúng kèm giải thích từng câu (trường `ex` của câu hỏi; màn kết quả cần hiện đáp án + giải thích). `HIDE_EXAMS` trong `src/build_data.py` để ẩn tạm đề theo số.
- **Luyện kỹ năng** (517 câu): mỗi câu có `lab` (nhãn HTML có ruby), `labvi`, `au`, `imgs`, `o[]` (t có thể là HTML, img), `a[]`. Đã sửa 21/10 vì trước đó bị lẫn nhãn/tranh/lựa chọn.
- **Từ vựng** (3.817 từ): trọng âm `a` (Kanjium, ~2.589 từ), ví dụ `x` → `VOCAB.ex` (~2.117 từ, trích いろどり), audio `au` → `app/media/vau/<md5>.mp3` (VOICEVOX 青山龍星 ノーマル). Không có tiếng Anh.
- **Bài tập về nhà**: 25 buổi × 90 phút theo lộ trình (buổi 1 = tổng ôn 入門 + Bài 1–2 初級1).

## 6. Những thứ KHÔNG nằm trong repo (ở máy làm việc cũ)
- Thư mục `site/*_body.html` (phần thân web bài học) mà `skills_extract.py` / `btvn/extract.py` đọc — muốn trích lại thì tách từ `public/lessons/*/Irodori_*_BaiNN.html`.
- VOICEVOX core 0.17 + model 15.vvm (sinh audio từ vựng), TTS tiếng Việt piper (thuyết minh video).
- Video quảng bá `AnhTrongJFT_App_QuangBa_v2.mp4` (ngang, không phụ đề; ghi "20 đề"), thumbnail dọc 1080×1440 & ngang, PDF lộ trình 25 buổi, ZIP bài tập — anh giữ các file đã gửi.

## 7. Việc đang chờ
- **Đề thi mới**: chờ anh gửi đề; nhập vào app kèm đáp án + giải thích (xem mục 5). Không dùng vnjpclub/Minna.
- **Cá nhân hoá**: đã lưu tiến độ (12/11, xem mục Tiến độ). Còn có thể làm: trang giáo viên xem tiến độ từng học viên.
- Tuỳ chọn: áp font M PLUS Rounded 1c cho toàn app (đã đề xuất, chưa chốt).
- Video quảng bá/thumbnail còn nhắc "20 đề thi thử" — bộ đề cũ đã xoá.

## Logo thương hiệu (30/10/2026)
- File gốc: `public/app/media/brand/` — `logo-ngang.svg` (nền sáng), `logo-ngang-trang.svg` (nền tối), `logo-mark.svg` / `logo-mark-trang.svg` (chỉ biểu tượng), `icon.svg` + `icon-512/192.png`, `apple-touch-icon.png`, `favicon-32/48.png`, `og.png` (ảnh chia sẻ link 1200×630), `site.webmanifest`; `public/favicon.ico`.
- Màu: xanh #0d5a8c · hồng #c42f66 · chữ #0d2b40 (trùng --blue / --pink của app).
- `/app/media/brand/` và `/favicon.ico` mở công khai (auth.js) để trang đăng nhập, trang kiểm tra dùng được.
- Đang dùng ở: sidebar + form đăng nhập + hero (index_tpl), trang /login (auth.js, kèm og:image), trang kiểm tra (kiemtra/tpl.html, kiemtra.js), BTVN (btvn/render.py), header slide trong tailieu (class `logo lgimg`, nền là icon.svg).

## JLPT N3 (12/11/2026) — tab dùng chung cho 4 app
- Trang độc lập `public/n3/` (index.html + n3.js + n3.css + data/ + img/), app JFT nhúng bằng iframe (nav `n3`, màn `#n3`, nạp khi mở; bản dùng thử thay bằng khung khoá trong build_demo.py). Cùng thư mục được chép sang app Khách sạn, Vệ sinh toà nhà, Chế biến thực phẩm: `bash src/n3/sync.sh "nội dung commit"` (chép + commit + push 3 repo).
- **Luyện đề**: 24 đề. PDF "26 đề thi N3" có 26 bộ (N3-1…N3-16, 16b, 17…23, 25, 26) nhưng N3-2 trùng hệt N3-1 và N3-16b trùng N3-16 → bỏ 2 bộ trùng; `ORDER` trong build.py: Đề k ↔ bộ thứ ORDER[k-1] trong PDF (file raw/ans/fix đặt tên theo số bộ trong PDF, eXX). Mỗi đề: 文字・語彙 (35 câu) + 文法・読解 (39 câu), không có nghe. Chế độ Thi thử (100 phút) / Luyện tập (chấm ngay). Điểm cao nhất lưu localStorage `n3best_<id>`.
  - Trích tự động từ PDF: `src/n3/tools/ext.py` (2 cột/trang, furigana → ruby, gạch chân → `<u>`, ô ★ → ＿＿), `tools/parse.py <chỉ số 0–25>` → `src/n3/raw/eXX.json`; bảng đáp án PDF → `raw/keys_raw.json` (`tools/keys.py`). Cần biến `N3PDF=<đường dẫn PDF>` (PDF không đưa lên repo).
  - Đáp án đã kiểm + dịch + giải thích: `src/n3/ans/eXX.txt` (dòng `A5|3|dịch|giải thích`; A = 文字語彙, B = 文法読解). Sửa phần trích: `src/n3/fix/eXX.json` (`q`: {"B31": {...}}, `qi`: theo vị trí câu trong raw, `rep`: [[cũ,mới]] sửa lỗi chính tả PDF, `g`, `drop`). Giải thích dùng ¶ để xuống dòng, đầu dòng 'Nhãn:' được in đậm. Dựng: `python3 src/n3/build.py [số đề…]` → `public/n3/data/deXX.json` + `index.json` (chỉ đề đủ giải thích mới hiện). Bài đọc 情報検索 (Ⅶ) là ảnh cắt `public/n3/img/n3eXXgN_k.jpg`.
  - Bộ 13 (N3-13) phần 読解 khác định dạng → sau `tools/parse.py 12` phải chạy thêm `tools/parse13.py` (ghép câu 19–39 vào raw/e13.json). Bảng đáp án bộ 10 trích sai → đã nhập tay trong raw/keys_raw.json.
  - Đáp án PDF sai thì em tự giải và sửa (anh dặn 12/11), build.py in ra danh sách câu khác đáp án gốc.
- **Từ vựng Mimikara N3**: 880 từ chép từ bảng "Tổng hợp 880 từ vựng Mimikara N3" (Minato Dorimu, PDF ảnh) → `src/n3/vocab/mimikara.tsv` (số · từ · Hán Việt · cách đọc · nghĩa; sửa vài lỗi rõ ràng của bảng) → `public/n3/data/vocab.json`. Chia phần 40 từ; Bảng từ / Thẻ ghi nhớ / Kiểm tra. (12/11) Mỗi từ có giải thích cách dùng + cụm từ kết hợp + phân biệt (tự soạn, không chép sách) ở `src/n3/vocab/gt/*.txt` (dòng `số|nội dung`, ¶ = xuống dòng) → `python3 src/n3/build_vocab.py` → vocab.json (trường `x`); bấm vào từ trong Bảng từ để mở, hiện cả dưới Thẻ ghi nhớ và sau câu Kiểm tra. Icon = bìa sách `img/mimikara.jpg` (anh gửi).
