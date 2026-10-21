# App học JFT-Basic · Anh Trọng Dạy JFT

Web học JFT-Basic dựa trên いろどり 生活の日本語 (出典：国際交流基金「いろどり 生活の日本語」).
Chạy trên Cloudflare Pages, có đăng nhập phía máy chủ.

## Cấu trúc
- `public/` — toàn bộ web (index.html, app/, lessons/)
- `functions/_middleware.js` — chặn mọi trang nếu chưa đăng nhập

## Cài trên Cloudflare Pages
- Framework preset: **None**
- Build command: *(để trống)*
- Build output directory: **public**
- Biến môi trường (Settings → Variables and Secrets), loại **Secret**:
  - `ACCOUNTS` — danh sách tài khoản, cách nhau dấu phẩy: `lan:Lan2026, minh:Minh2026`
  - `SECRET` — một chuỗi dài bất kỳ (ví dụ 30 ký tự lộn xộn)

## Quản lý học sinh
- Thêm / đổi mật khẩu / khoá bạn nào: sửa `ACCOUNTS` → Save → vào **Deployments** → bản mới nhất → **Retry deployment**.
- Bạn bị xoá khỏi danh sách sẽ bị đăng xuất ngay ở lần bấm tiếp theo.
- Đăng nhập giữ 30 ngày trên mỗi máy.
