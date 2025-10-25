Dưới đây là phiên bản **tài liệu hoàn chỉnh, gọn gàng và chuyên nghiệp hơn** — theo phong cách Markdown dùng cho GitHub hoặc PyPI 👇

---

# 🖼️ PDF to Images – Công cụ chuyển PDF thành ảnh linh hoạt

## 📘 Giới thiệu

**PDF to Images** là công cụ dòng lệnh (CLI) gọn nhẹ giúp bạn nhanh chóng **chuyển đổi file PDF thành ảnh** với nhiều tùy chọn linh hoạt:

✨ **Tính năng nổi bật**

* Chuyển đổi PDF sang ảnh với **độ phân giải tùy chỉnh (DPI)**
* **Chia đôi trang** linh hoạt (trái–phải hoặc trên–dưới)
* Chỉ **xử lý các trang được chọn**
* Hỗ trợ nhiều **định dạng đầu ra** (`png`, `jpg`, `webp`, …)
* Chế độ **xem trước (`--preview`)** để kiểm tra trước khi tạo file thật

---

## ⚙️ Cài đặt

```bash
git clone https://github.com/vuvandinh123/tool-python.git
cd tool-python/pdf-to-image
pipx install .
```

> 💡 *Khuyến nghị sử dụng [pipx](https://pypa.github.io/pipx/) để cài đặt CLI toàn hệ thống, tránh xung đột môi trường.*

---

## 🚀 Cách sử dụng

```bash
pdf-to-images <pdf_path> [options]
```

Hoặc nếu chạy trực tiếp:

```bash
python3 main.py <pdf_path> [options]
```

---

## 💡 Ví dụ sử dụng

| Mục đích                                                 | Lệnh mẫu                                                                                 |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Chuyển đổi toàn bộ file PDF mặc định                     | `python3 main.py tailieu.pdf`                                                            |
| Chia đôi mỗi trang theo chiều dọc (trái–phải)            | `python3 main.py tailieu.pdf --split vertical`                                           |
| Chỉ xử lý các trang 1, 3 và 5                            | `python3 main.py tailieu.pdf --pages 1,3,5`                                              |
| Chỉ xử lý từ trang 5 đến 8                               | `python3 main.py tailieu.pdf --pages 5-8`                                                |
| Xuất ảnh JPG với độ phân giải 200 DPI và pattern đặt tên | `python3 main.py tailieu.pdf --dpi 200 --format jpg --pattern "output/page_{i:03d}.jpg"` |
| Xem trước danh sách file sẽ tạo mà không xuất thật       | `python3 main.py tailieu.pdf --preview`                                                  |

---

## ⚙️ Tùy chọn chi tiết

| Tham số           | Mô tả                                                                | Mặc định       |
| ----------------- | -------------------------------------------------------------------- | -------------- |
| `--dpi <number>`  | Đặt độ phân giải ảnh đầu ra (DPI)                                    | `300`          |
| `--split <mode>`  | Chia đôi trang: `vertical` (trái–phải) hoặc `horizontal` (trên–dưới) | —              |
| `--pages <list>`  | Chỉ xử lý các trang được chọn, ví dụ: `1,3,5-8`                      | Tất cả         |
| `--pattern <str>` | Mẫu tên file đầu ra, có thể dùng `{i}` làm chỉ số trang              | `page_{i}.png` |
| `--format <ext>`  | Định dạng ảnh đầu ra (`png`, `jpg`, `webp`, …)                       | `png`          |
| `--preview`       | Hiển thị danh sách file sẽ tạo mà không ghi ra ổ đĩa                 | ❌              |

---

## 🧩 Hỗ trợ định dạng

PDF → PNG, JPG, WEBP, BMP, TIFF

---

## 🧰 Gỡ cài đặt

Nếu muốn xóa tool khỏi hệ thống:

```bash
pipx uninstall pdf-to-images
```

## 📄 Giấy phép

Phân phối theo **MIT License**.
Tác giả: [**@vuvandinh123**](https://github.com/vuvandinh123)

---