
# 🧰 Python CLI Tools – Bộ công cụ tự động hoá bằng Python

> **Tác giả:** [Vũ Văn Định](https://github.com/vuvandinh123)  
> **Email:** vuvandinh203@gmail.com  
> **Giấy phép:** MIT License  
> **Ngôn ngữ:** Python 3.10+

---

## 🎯 Giới thiệu

**Python CLI Tools** là tập hợp các **công cụ dòng lệnh (Command Line Tools)** nhỏ gọn, mạnh mẽ và dễ dùng — được viết bằng **Python** nhằm phục vụ nhu cầu thao tác file, ảnh và tài liệu một cách nhanh chóng, tiện lợi.

Tất cả các tool đều:
- Cài đặt đơn giản bằng `pipx`
- Có **chế độ preview** (xem trước mà không ghi đè)
- Có **thông báo rõ ràng**, **thực thi nhanh**, và **thân thiện với terminal**

---

## 📦 Danh sách công cụ

| 🧩 Tên Tool | 🔍 Mô tả ngắn | ⚙️ Lệnh CLI | 📄 Thư mục |
|--------------|---------------|--------------|-------------|
| 🖼️ **Auto Resize Image** | Resize ảnh hàng loạt, giữ tỉ lệ, hỗ trợ preview & recursive | `resize-images` | `/auto-resize-image` |
| 📄 **PDF to Images** | Chuyển PDF sang ảnh, chia đôi trang, chọn trang, định dạng tùy chọn | `pdf-to-images` | `/auto-pdf-image` |
| 🏷️ **Image Batch Renamer** | Đổi tên & convert định dạng ảnh hàng loạt theo pattern linh hoạt | `rename-images` | `/image-batch-renamer` |

---

## ⚙️ Cài đặt

### 1️⃣ Clone toàn bộ repo

```bash
git clone https://github.com/vuvandinh123/tool-python.git
cd tool-python
````

### 2️⃣ Cài đặt từng tool (dùng pipx)

```bash
cd auto-resize-image && pipx install .
cd ../auto-pdf-image && pipx install .
cd ../image-batch-renamer && pipx install .
```

> 💡 *Mỗi tool được cài độc lập — bạn có thể chỉ cài tool mình cần.*

---

## 🚀 Sử dụng nhanh

### 🔹 Resize ảnh hàng loạt

```bash
resize-images ./photos -w 800 -o ./out --suffix _sm
```

### 🔹 Chuyển PDF sang ảnh

```bash
pdf-to-images tailieu.pdf --dpi 200 --split vertical --format jpg
```

### 🔹 Đổi tên ảnh theo pattern

```bash
rename-images ./images photo_{i:03d}.jpg --convert
```

---

## 📚 Tài liệu chi tiết

* [🖼️ Auto Resize Image](./auto-resize-image/README.md)
* [📄 PDF to Images](./pdf-to-image/README.md)
* [🏷️ Image Batch Renamer](./auto-rename-image/README.md)

---

## 🔧 Yêu cầu hệ thống

* Python **3.10+**
* Thư viện phụ thuộc: `pillow`, `pdf2image`, `click`, `tqdm`
* Công cụ cài đặt: `pipx`

---


## 👨‍💻 Tác giả

**Vũ Văn Định**
📧 [vuvandinh203@gmail.com](mailto:vuvandinh203@gmail.com)
🐙 [github.com/vuvandinh123](https://github.com/vuvandinh123)
🛠️ Python • DevOps • Automation • CLI Tools

---

## 🪪 Giấy phép

Phát hành theo **MIT License** — tự do sử dụng, sửa đổi và phân phối.

---

⭐ **Nếu bạn thấy hữu ích, hãy để lại một Star trên GitHub để ủng hộ nhé!**

```