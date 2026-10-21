# Cách cập nhật app (Anh Trọng Dạy JFT)

Mọi thay đổi đẩy lên nhánh `main` của repo này → Cloudflare tự build lại → khoảng 2–3 phút sau web cập nhật.

## Cách 1 — Nhờ Claude (khuyên dùng)
Mở chat mới với Claude, gửi:
> "Cập nhật app JFT trong repo tronganh8a-dev/anhtrong-jft-app: …(việc cần làm)…"
kèm file/link (đề mới trên luyenthitokutei.com, bài học mới, sửa đáp án…).
Claude clone repo, sửa dữ liệu trong `src/`, chạy build, đẩy lên.

## Cách 2 — Tự làm trên github.com (việc nhỏ)
- **Thay 1 file bài học**: vào `public/lessons/s1` (初級1) / `s2` (初級2) / `sc` (初中級) → *Add file → Upload files* → kéo file mới (trùng tên) → *Commit changes*. Giới hạn 25MB/file.
- **Sửa chữ nhỏ**: mở file → biểu tượng bút ✏️ → sửa → *Commit changes*.

## Tài khoản học sinh
Không nằm trong repo. Sửa trên Cloudflare: app → Settings → Variables and Secrets → `ACCOUNTS` (dạng `ten:matkhau, ten2:matkhau2`) → Deploy.

## Cấu trúc
- `public/` — web chạy thật (index.html, app/data/*.js, app/media/, lessons/)
- `src/` — nguồn để dựng lại dữ liệu:
  - `index_tpl.html` giao diện · `build_index.py` → `public/index.html`
  - `build_data.py` → `public/app/data/*.js` (lessons, vocab, skills, exams, grammar)
  - `raw/lt_exams.json` đề thi (lấy từ luyenthitokutei.com) · `raw/skills_raw.json` luyện kỹ năng · `raw/titles.txt` danh sách bài
  - `vocab/` từ vựng · `gram/out/*.json` ngữ pháp
  - `shrink.py` nén audio trong file bài học trước khi đưa lên (`python3 shrink.py vao.html ra.html`)
- `auth.js`, `worker.js`, `wrangler.jsonc`, `functions/` — đăng nhập phía máy chủ

## Bản dùng thử (không đăng nhập)
- Nằm trong `demo/` (app riêng trên Cloudflare, tên `jft-dungthu`, Root directory = `demo`).
- Dựng lại sau khi cập nhật bản chính: `python3 src/build_demo.py` (初級1 Bài 1–2, Đề 01–02, ngữ pháp 初級1 Bài 1–2, kỹ năng 初級1 Bài 2–3, từ vựng 初級1 Bài 1–2).

## Bài tập về nhà (tab "Bài tập về nhà")
- File làm bài: `public/btvn/BTVN_BuoiXX.html` · bản in: `public/btvn/pdf/BTVN_BuoiXX.pdf` · danh sách: `public/app/data/hw.js`.
- Nguồn dựng: `src/btvn/` (`extract.py` lấy 漢字のことば + script từ web bài học, `gen_btvn.py` sinh câu hỏi, `render.py` xuất HTML/PDF).

## Trọng âm từ vựng
- `src/pitch/add_pitch.py` thêm trường `a` (vị trí hạ giọng) vào `public/app/data/vocab.js` từ `src/pitch/accents_sub.tsv` (trích từ Kanjium, CC BY-SA 4.0). Chạy lại sau mỗi lần `build_data.py`.
