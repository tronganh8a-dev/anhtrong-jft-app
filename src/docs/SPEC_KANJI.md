# Soạn bài học CHỮ HÁN (từ vựng chữ Hán) cho học viên JFT-Basic người Việt

Đầu vào: `pkg/kanji_N.json` = `{lv, items:[{i, w, r, vi}]}` lấy từ bảng tổng hợp Hán tự của lớp cô Quỳnh
(w = từ có chữ Hán, r = cách đọc hiragana, vi = nghĩa). Có thể có lỗi trích xuất PDF (thiếu/thừa chữ, cách đọc thiếu phần đuôi như 卒業する → そつぎょう).

## Đầu ra (mảng JSON, mỗi item 1 phần tử, giữ thứ tự và `i`):
```json
{"i": 0, "w": "名前", "r": "なまえ", "vi": "Tên",
 "hv": "DANH TIỀN",
 "chars": [{"k": "名", "hv": "DANH", "on": "メイ・ミョウ", "kun": "な", "vi": "tên, nổi tiếng"},
           {"k": "前", "hv": "TIỀN", "on": "ゼン", "kun": "まえ", "vi": "phía trước, trước"}],
 "tip_vi": "Mẹo nhớ ngắn hoặc lưu ý cách đọc (1–2 câu).",
 "ex": {"jp": "ここに名前を書いてください。", "vi": "Hãy viết tên vào đây."}}
```
- `w`, `r`, `vi`: giữ nguyên, CHỈ sửa lỗi rõ ràng (cách đọc phải đọc đúng TOÀN BỘ từ w, kể cả okurigana: 卒業する → そつぎょうする; nghĩa viết hoa chữ đầu, đúng chính tả).
- `hv`: âm Hán Việt VIẾT HOA của từng chữ Hán trong w theo thứ tự (bỏ qua kana). Ví dụ 食べます → "THỰC", 子ども → "TỬ".
- `chars`: mỗi chữ Hán (không lặp) trong w: âm Hán Việt, âm On (katakana, tối đa 2 âm phổ biến), âm Kun (hiragana, tối đa 2, okurigana đặt sau dấu chấm như た.べる), nghĩa tiếng Việt ngắn.
- `tip_vi`: 1–2 câu: mẹo nhớ theo bộ thủ/hình chữ HOẶC lưu ý đọc đặc biệt (âm ghép biến âm, đọc bất quy tắc như 今日 きょう, 大人 おとな). Không bịa nguồn gốc chữ.
- `ex`: 1 câu ví dụ tự soạn, ngắn, A2, có dùng đúng từ w; bản dịch tiếng Việt tự nhiên. Không furigana, không romaji.
- Âm Hán Việt phải CHÍNH XÁC (ví dụ 学 HỌC, 校 HIỆU, 生 SINH, 活 HOẠT, 去 KHỨ, 年 NIÊN, 週 CHU, 元 NGUYÊN, 気 KHÍ, 忙 MANG, 働 ĐỘNG, 作 TÁC, 犬 KHUYỂN, 族 TỘC, 夕 TỊCH, 英 ANH, 習 TẬP, 季 QUÝ, 節 TIẾT, 春 XUÂN). Với chữ Nhật tự tạo (国字) không có âm Hán Việt chuẩn, ghi âm quen dùng trong sách dạy tiếng Nhật ở Việt Nam (ví dụ 働 ĐỘNG, 込 NHẬP/VÀO, 畑 ĐIỀN); nếu không chắc thì ghi "—".

Ghi file bằng công cụ Write (JSON hợp lệ; nếu dài có thể chia 2 lần Write vào 2 file `_a`, `_b` rồi gộp bằng python). Kiểm tra số phần tử bằng python.
Trả lời cuối: số mục đã làm, các `i` đã sửa w/r/vi so với bản gốc (liệt kê ngắn).
