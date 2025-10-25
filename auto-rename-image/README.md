
# 🖼️ Image Batch Renamer

**Công cụ dòng lệnh (CLI) giúp đổi tên và chuyển đổi định dạng ảnh hàng loạt bằng Python.**
Nhanh, tiện, và an toàn — với chế độ xem trước, backup tự động và hỗ trợ pattern linh hoạt.

---

## ✨ Tính năng nổi bật

✅ Đổi tên ảnh hàng loạt theo **mẫu (pattern)** tùy chỉnh
✅ Hỗ trợ các **placeholder thông minh** như `{i}`, `{date}`, `{datetime}`, `{timestamp}`
✅ **Chuyển đổi định dạng ảnh** dễ dàng (VD: `.png → .jpg`)
✅ **Xem trước (`--preview`)** kết quả trước khi áp dụng thật
✅ Tự động **tạo bản sao lưu (backup)** trước khi đổi tên hoặc convert

---

## ⚙️ Cài đặt

### 1️⃣ Clone dự án

```bash
git clone https://github.com/vuvandinh123/image-batch-renamer.git
cd auto-rename-image
```

### 2️⃣ Cài đặt bằng `pipx` (khuyến nghị)

```bash
pipx install .
```

> 💡 *`pipx` giúp cài đặt CLI tool toàn hệ thống mà vẫn tách biệt môi trường Python.*

Sau khi cài đặt xong, bạn có thể dùng lệnh `rename-images` ở **bất kỳ đâu trong terminal**.

---

## 🚀 Cách sử dụng

### Cấu trúc lệnh:

```bash
rename-images <thư_mục> <pattern> [tùy_chọn]
```

### Ví dụ nhanh:

```bash
rename-images ~/Pictures photo_{i}.png
```

→ Toàn bộ ảnh trong thư mục `~/Pictures` sẽ được đổi tên thành:

```
photo_1.png, photo_2.png, photo_3.png, ...
```

---

## 🔤 Placeholder hỗ trợ

| Placeholder   | Ý nghĩa                  | Ví dụ                       |
| ------------- | ------------------------ | --------------------------- |
| `{i}`         | Số thứ tự bắt đầu từ 1   | `photo_1.jpg`               |
| `{i:04d}`     | Số thứ tự có padding 0   | `photo_0001.jpg`            |
| `{date}`      | Ngày hiện tại (YYYYMMDD) | `photo_20251025.jpg`        |
| `{datetime}`  | Ngày + giờ hiện tại      | `photo_20251025_173000.jpg` |
| `{timestamp}` | Unix timestamp           | `photo_1730001112.jpg`      |

---

## 🧩 Tùy chọn thêm

| Tùy chọn          | Mô tả                                       | Ví dụ                                       |
| ----------------- | ------------------------------------------- | ------------------------------------------- |
| `--convert`, `-c` | Convert ảnh sang định dạng trong pattern    | `rename-images ~/img new_{i}.jpg --convert` |
| `--preview`       | Xem trước kết quả mà **không áp dụng thật** | `rename-images ~/img new_{i}.png --preview` |

---

## 🧠 Cách hoạt động

1. Tool quét thư mục và tìm tất cả các ảnh hợp lệ (`.jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp`).
2. Với mỗi ảnh, tool:

   * Sinh tên mới dựa theo `pattern`.
   * Nếu có flag `--preview`, chỉ hiển thị kết quả dự kiến.
   * Nếu không, đổi tên hoặc convert file thật.
   * Tự động tạo thư mục backup `.backup_<timestamp>` lưu bản gốc.

---

## 💾 Ví dụ nâng cao

### 🔄 Đổi tên và convert toàn bộ ảnh PNG sang JPG

```bash
rename-images ./images photo_{i:03d}.jpg --convert
```

### 👀 Xem trước khi áp dụng

```bash
rename-images ./images photo_{i:03d}.jpg --convert --preview
```

### 🗓️ Đổi tên ảnh theo ngày chụp

```bash
rename-images ./images trip_{date}_{i}.png
```

---

## 🧰 Gỡ cài đặt

Nếu muốn xóa tool khỏi hệ thống:

```bash
pipx uninstall rename-images
```

---

## 👨‍💻 Tác giả

**Vũ Văn Định**
📧 Email: [vuvandinh203@gmail.com](mailto:vuvandinh203@gmail.com)
🛠️ Python CLI / Automation Tools

---