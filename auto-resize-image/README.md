
# 🖼️ Auto Resize Image (resize-images)

**Auto Resize Image** là công cụ dòng lệnh (CLI) giúp **resize ảnh hàng loạt** một cách nhanh chóng và linh hoạt.
Hỗ trợ **xem trước (preview)**, **đệ quy thư mục con**, **giữ tỉ lệ ảnh**, và **lưu kết quả vào thư mục đích tùy chọn**.

---

## 🚀 Cài đặt

```bash
cd auto-resize-image
pipx install .
```

> 💡 *Khuyến nghị dùng [pipx](https://pypa.github.io/pipx/) để cài đặt CLI toàn hệ thống.*

---

## 🧰 Cách sử dụng

```bash
resize-images <directory> [options]
```

---

## 📘 Ví dụ

### 🔍 Xem trước kết quả resize (không lưu)

```bash
resize-images ./photos -w 800 --preview
```

### 💾 Resize tất cả ảnh theo chiều rộng 800px, lưu ra thư mục `./out` và thêm hậu tố `_sm`

```bash
resize-images ./photos -w 800 -o ./out --suffix _sm
```

### 📏 Resize theo tỉ lệ 50% so với ảnh gốc

```bash
resize-images ./photos --scale 0.5 -o ./out
```

### 🗂️ Resize đệ quy toàn bộ thư mục con

```bash
resize-images ./photos -w 1024 -r -o ./out
```

---

## ⚙️ Tuỳ chọn

| Tham số                 | Mô tả                                  | Mặc định    |
| ----------------------- | -------------------------------------- | ----------- |
| `-w`, `--width <px>`    | Chiều rộng mục tiêu (pixel)            | —           |
| `-h`, `--height <px>`   | Chiều cao mục tiêu (pixel)             | —           |
| `-s`, `--scale <float>` | Tỉ lệ so với ảnh gốc (VD: `0.5` = 50%) | —           |
| `-o`, `--output <path>` | Thư mục lưu kết quả                    | `./resized` |
| `--keep_ext`            | Giữ nguyên phần mở rộng ảnh gốc        | ✅           |
| `--suffix <text>`       | Hậu tố thêm vào trước phần mở rộng     | `_resized`  |
| `--quality <int>`       | Chất lượng JPEG (1–95)                 | `85`        |
| `-r`, `--recursive`     | Duyệt đệ quy các thư mục con           | ❌           |
| `-p`, `--preview`       | Chỉ xem trước, không ghi file          | ❌           |
| `--overwrite`           | Ghi đè nếu file đầu ra đã tồn tại      | ❌           |

---

## 🧩 Hỗ trợ định dạng

JPEG, PNG, WEBP, BMP, GIF, TIFF

---
## 🧰 Gỡ cài đặt

Nếu muốn xóa tool khỏi hệ thống:

```bash
pipx uninstall resize-images
```

## 📄 Giấy phép

Phân phối theo giấy phép **MIT License**.

---