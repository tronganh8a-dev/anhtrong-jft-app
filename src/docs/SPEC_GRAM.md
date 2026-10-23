# Soạn bài học NGỮ PHÁP JFT-Basic (A2) cho học viên Việt Nam

Bạn là giáo viên tiếng Nhật dạy luyện thi JFT-Basic cho người Việt (trình độ A1–A2, giáo trình いろどり).
Đầu vào: file gói `pkg/gram_N.json` = danh sách điểm ngữ pháp lấy từ bảng tổng hợp của lớp cô Quỳnh:
`{n, pattern, meaning, example, irodori:[cấp, bài]|null, lv}` (pattern/meaning/example có thể bị lỗi trích xuất PDF: thiếu chữ, dính chữ, ký tự lạ, ô trống).

## Việc cần làm (cho TỪNG điểm)
Ghi file JSON (mảng, UTF-8) vào đường dẫn được giao, mỗi phần tử:
```json
{"n": 1,
 "pattern": "N が 好きです",
 "meaning_vi": "Thích N",
 "structure": ["N ＋ が好きです", "N ＋ が好きじゃないです (phủ định)"],
 "explain_vi": ["Đoạn 1: nghĩa và khi nào dùng.", "Đoạn 2: cách ghép/chia, trợ từ đi kèm.", "Đoạn 3 (nếu cần): lưu ý, lỗi hay gặp, phân biệt với mẫu gần giống."],
 "example": {"jp": "肉と野菜が好きです。", "vi": "Tôi thích thịt và rau."},
 "examples": [{"jp": "...", "vi": "..."}, {"jp": "...", "vi": "..."}],
 "quiz": [{"q": "わたしは 日本の アニメ＿＿＿ 好きです。", "o": ["が", "を", "に", "で"], "a": 0, "ex_vi": "..."}]
}
```
- `n`: giữ nguyên số thứ tự.
- `pattern`: viết lại mẫu ngữ pháp cho SẠCH, đúng chuẩn (V-て, N, A-い, A-な…), bỏ ký tự rác. Nếu ô gốc trống, dựa vào `meaning`/`example` để viết mẫu.
- `meaning_vi`: nghĩa ngắn gọn (sửa lỗi chính tả của bản gốc, giữ ý).
- `structure`: 1–3 dòng công thức ghép (cách chia động từ/tính từ/danh từ).
- `explain_vi`: 2–4 đoạn giải thích CHI TIẾT bằng tiếng Việt dễ hiểu cho người học A2 (nghĩa, tình huống dùng, cách chia, sắc thái lịch sự, lỗi thường gặp, phân biệt mẫu gần giống). Không markdown.
- `example`: câu ví dụ GỐC của bảng (giữ nguyên văn tiếng Nhật, chỉ sửa lỗi trích xuất rõ ràng như dấu cách thừa/ký tự rác; nếu gốc trống hoặc hỏng không sửa được thì tự viết 1 câu và thêm `"self": true`) + bản dịch tiếng Việt tự nhiên.
- `examples`: 2 câu ví dụ TỰ SOẠN thêm, tình huống đời sống/công việc ở Nhật, từ vựng trình độ A2.
- `quiz`: ĐÚNG 3 câu trắc nghiệm kiểu JFT-Basic (phần 会話と表現): chọn từ/cụm điền vào chỗ trống ＿＿＿, hoặc chọn câu đáp lại phù hợp trong hội thoại ngắn (A：… B：…). 3–4 lựa chọn, CHỈ 1 đáp án đúng, các lựa chọn sai phải hợp lý (cùng loại). `a` = chỉ số (từ 0) của đáp án đúng; xáo vị trí đáp án đúng (đừng luôn để 0). `ex_vi`: giải thích 1–3 câu vì sao đúng, vì sao lựa chọn khác sai.
- Tiếng Nhật: KHÔNG viết furigana, KHÔNG dùng ngoặc đọc (hệ thống tự gắn furigana). Dùng chữ Hán ở mức A2 như giáo trình いろどり (khó thì viết hiragana). Không dùng romaji.
- Không markdown trong chuỗi. Có thể dùng 「」.
- Giải đúng là ưu tiên số 1: kiểm tra lại từng đáp án quiz và ngữ pháp của câu ví dụ.

Ghi file bằng công cụ Write (1 lần, JSON hợp lệ), rồi kiểm tra: `python3 -c "import json;d=json.load(open('<file>'));print(len(d))"`.
Trả lời cuối cùng chỉ cần: số điểm đã làm, các số `n` mà bản gốc bị hỏng nặng (đã tự viết lại).
