# Bổ sung cho phần NGHE (聴解)

Đọc SPEC.md trước, rồi áp dụng thêm các điểm sau cho câu nghe.

- Gói `pkg/listen_<tag>.json` có thêm trường `asr` cho mỗi câu: bản chép lời TỰ ĐỘNG (máy nhận dạng giọng nói) của file audio,
  dạng các dòng "[giây] câu". Bản này CÓ LỖI (nghe nhầm từ, thiếu chữ, sai kanji, dính câu). Nhiều audio lấy từ giáo trình
  いろどり (Irodori) của Japan Foundation hoặc đề luyện JFT, giọng hội thoại đời sống.
- `audio_missing: true` nghĩa là file audio bị khoá, không có lời — vẫn chọn đáp án hợp lý nhất từ câu hỏi + tranh, ghi `conf:"low"`
  và `note:"Thiếu audio"`, không viết `script`.
- Câu hỏi trong form thường viết bằng tiếng Việt → điền `q_jp` (câu hỏi tiếng Nhật kiểu đề JFT).
- Nhiều câu dùng tranh (ảnh) cho các lựa chọn: `options` chỉ ghi "1/2/3", "a,c", "A/B/C"… — PHẢI mở ảnh để biết mỗi lựa chọn là gì,
  và trong `why_vi` nói rõ lựa chọn đúng là tranh gì.
- Thêm trường `script`: mảng các lượt thoại đã SỬA LỖI hợp lý theo ngữ cảnh: `[{"jp":"A：……","vi":"A: ……"}]`.
  Giữ sát lời gốc; chỗ nào không chắc thì giữ như ASR và đánh dấu (?) ở cuối câu tiếng Nhật. Ghi người nói A/B (hoặc tên nếu biết).
  Nếu nhiều câu dùng chung 1 audio, có thể lặp lại script ở mỗi câu.
- `why_vi` phải chỉ ra câu thoại then chốt dẫn tới đáp án (trích 「…」).
