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
  - Bản dùng thử: worker `jft-dungthu` (Root directory = `demo/`), không đăng nhập, mỗi mục chỉ 2 cái.
- Sau mỗi lần push, kiểm tra build:
  `gh api repos/tronganh8a-dev/anhtrong-jft-app/commits/<sha>/check-runs` → cả 2 phải `success`.
  (Từng bị lỗi build ngẫu nhiên → đẩy 1 commit rỗng là build lại được.)

## 2. Các tab trong app
Trang chủ (hero gradient + dải 4 màu sách, lịch thi & link Prometric, hướng dẫn điểm đậu) · **Tài liệu** (trước là "Học qua slide": 4 mục Slide bài giảng / Từ vựng / Chữ Hán / Ngữ pháp, 3 cấp 入門・初級1・初級2) · Làm đề (CBT giống máy thi; chế độ Thi thử / Luyện tập có giải thích, bật tắt furigana) · Ngữ pháp (文法ノート いろどり) · **Video** (thay tab Luyện kỹ năng 23/10) · Từ vựng (flashcard, trọng âm, audio, ví dụ) · Bài tập về nhà (25 buổi).

- **Tài liệu → Từ vựng/Chữ Hán/Ngữ pháp**: dữ liệu từ 7 file PDF tổng hợp của lớp cô Quỳnh (23/10). Nguồn trích: `src/docs/*_src.json`; phần soạn (sửa lỗi trích, âm Hán Việt, phân tích On/Kun, mẹo nhớ, giải thích ngữ pháp, ví dụ tự soạn, 3 câu quiz/mẫu) ở `src/docs/ans/*.json` (theo `src/docs/SPEC_*.md`); `quizfix_*.json` = sửa sau kiểm định. Dựng: `python3 src/build_docs.py` → `public/app/data/docs.js` (tải khi mở tab). Ảnh từ vựng: `public/app/media/doc/<md5>.jpg`. Bài luyện tập tự sinh ở trình duyệt (nhìn tranh chọn từ, chọn nghĩa, chọn cách đọc, chọn chữ Hán) và dùng giao diện CBT `startSkill`.
- **Tài liệu → Theo buổi học** (23/10): file HTML tài liệu từng buổi ở `public/tailieu/` (vd. `Buoi02_*.html`), danh sách khai báo trong mảng `BUOI` của `src/index_tpl.html` (k:'slide' = khung 16:9, k:'web' = khung cao). Thêm buổi mới: chép file vào `public/tailieu/` + thêm 1 dòng vào `BUOI` → build_index.
- **Video**: danh sách ở `src/raw/videos.json` → `python3 src/build_videos.py`. YouTube nhúng với `controls=0`, thanh điều khiển riêng của app, khung iframe kéo cao 90px mỗi đầu để ẩn tiêu đề YouTube. Không chọn được chất lượng (YouTube khoá); anh không dùng R2 (không có thẻ thanh toán).
- **Đăng nhập**: KHÔNG lưu đăng nhập — tải lại trang là phải đăng nhập lại (cookie `jft_once` dùng 1 lần; cookie cũ `jft_keep` bị xoá khi login/logout).
- **Cache**: trang HTML và `/app/data/*` trả `private, no-cache` (ảnh/audio 1 giờ); build_index gắn `?v=<md5>` vào link data → sửa là thấy ngay.
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
  build_demo.py         → demo/public (bản dùng thử: 初級1 Bài 1–2, Đề đầu tiên ×2, kỹ năng 初級1 Bài 2–3…)
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
- Cookie `jft_s` (ký HMAC, 30 ngày) + `jft_user`. Cookie dùng 1 lần `jft_once` (120s) đặt khi đăng nhập: mỗi lần mở/tải lại `/` hoặc `/index.html` đều bắt đăng nhập lại (theo yêu cầu của anh).
- `/app/media/cover/*` công khai (ảnh bìa ở trang đăng nhập). Trang đăng nhập dùng font M PLUS Rounded 1c, có bìa sách + nút Facebook/TikTok.

## 5. Dữ liệu & quy ước
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
- **Cá nhân hoá (lưu tiến độ, bài làm theo tài khoản)**: dự định dùng Cloudflare D1 — chờ anh tạo D1 Database ID + tên tài khoản giáo viên.
- Tuỳ chọn: áp font M PLUS Rounded 1c cho toàn app (đã đề xuất, chưa chốt).
- Video quảng bá/thumbnail còn nhắc "20 đề thi thử" — bộ đề cũ đã xoá.
