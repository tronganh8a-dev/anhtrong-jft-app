# Làm sạch danh sách TỪ VỰNG (bảng của lớp cô Quỳnh, theo bài giáo trình いろどり)

Đầu vào: `pkg/vocab_N.json` = `{lv, items:[{i, bai, w, r, vi}]}`. Dữ liệu trích từ PDF nên có lỗi:
dính chữ tiếng Việt ("ởnhà"), cột cách đọc lệch sang dòng khác (r không khớp với w), r trống, chữ rác.

## Đầu ra: mảng JSON, mỗi item 1 phần tử, giữ `i`:
```json
{"i": 0, "w": "旅行します", "r": "りょこうします", "vi": "Đi du lịch", "hv": "LỮ HÀNH", "pos": "V"}
```
- `w`: từ/cụm từ tiếng Nhật đúng như bảng (sửa dấu cách thừa, ký tự rác). Không thêm furigana.
- `r`: cách đọc hiragana ĐÚNG của toàn bộ w (katakana giữ katakana; số đọc ra hiragana: 5円 → ごえん). Nếu bảng ghi sai/lệch thì sửa lại cho khớp w. Nếu w toàn kana thì r = "" .
- `vi`: nghĩa tiếng Việt chuẩn chính tả, viết hoa chữ đầu, giữ ý bảng gốc (chỉ sửa lỗi dính chữ, sai chính tả).
- `hv`: âm Hán Việt VIẾT HOA cho các chữ Hán trong w (theo thứ tự, bỏ kana). Không có chữ Hán thì "". Phải chính xác.
- `pos`: loại từ: N (danh từ), V (động từ/cụm động từ), A (tính từ), Adv, Ph (cụm/câu), Num, Other.
- Không bỏ mục nào, không thêm mục.

Ghi file JSON bằng Write (có thể chia nhiều file `_a`, `_b`… nếu dài), kiểm tra số phần tử bằng python.
Trả lời cuối: số mục, danh sách `i` đã sửa w hoặc r (ngắn gọn).
