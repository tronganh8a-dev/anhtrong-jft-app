# Kiểm tra lại phần NGHE (vòng 2)

Đọc SPEC.md và SPEC_LISTEN.md để biết định dạng. Đây là vòng KIỂM TRA: mỗi câu đã có đáp án vòng 1 (`current`).

Gói `pkg/verify_<tag>.json`, mỗi câu có:
- `official_irodori`: lời thoại GỐC của giáo trình いろどり (mỗi mục: track + các dòng [người nói, tiếng Nhật, tiếng Việt]) mà máy
  đoán là KHỚP với audio của câu này (so khớp văn bản tự động — có thể nhầm). Hãy so với `asr_vad` / `asr_window` (2 bản chép lời
  tự động khác nhau của cùng audio) để xác nhận có đúng là audio đó không. Nếu khớp: DÙNG lời gốc làm `script` (chính xác hơn ASR).
  Nếu không khớp: bỏ qua.
- `asr_vad`, `asr_window`: chép lời tự động (có lỗi; `asr_window` cắt theo cửa sổ 10 giây nên ít sót đoạn hơn nhưng có thể lặp chữ ở chỗ nối).
- `current`: đáp án + giải thích vòng 1.
- Ảnh: mở bằng Read khi câu dùng tranh làm lựa chọn.

Việc cần làm cho TỪNG câu: xác minh đáp án `a` bằng lời thoại tốt nhất có được; sửa `script` (ưu tiên lời gốc いろどり nếu khớp, nếu
không thì ghép từ 2 bản ASR cho đầy đủ, đánh dấu (?) chỗ không chắc); sửa `why_vi`/`why_jp`/`trans_vi`/`vocab`/`q_jp` cho khớp; cập nhật
`conf` và `note` (note ghi "Đã đối chiếu lời gốc いろどり <track>" nếu dùng lời gốc).

Đầu ra: ghi file `ans/<tag>_li2.json` — mảng ĐẦY ĐỦ tất cả câu trong gói (kể cả câu không đổi), đúng schema như vòng 1
(n, a, conf, q_jp, why_vi, why_jp, vocab, trans_vi, note, script). Kiểm tra JSON hợp lệ.
Trả lời cuối: liệt kê các câu ĐỔI ĐÁP ÁN (n: cũ → mới, lý do 1 dòng) và số câu đã dùng lời gốc.
