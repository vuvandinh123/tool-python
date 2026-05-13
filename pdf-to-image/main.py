#!/usr/bin/env python3
"""
PDF to Image Tool

Chuyển đổi file PDF sang ảnh, có thể tùy chọn chia đôi trang (trái-phải hoặc trên-dưới).

Cách sử dụng:
    python3 main.py <pdf_path> [options]

Ví dụ:
    python3 main.py tailieu.pdf
    python3 main.py tailieu.pdf --split vertical
    python3 main.py tailieu.pdf --dpi 200 --pages 1,3,5
    python3 main.py tailieu.pdf --pattern "output/page_{i:03d}.jpg" --format jpg
    python3 main.py tailieu.pdf --preview

Tùy chọn:
    --dpi <number>           Độ phân giải ảnh (mặc định: 300)
    --split <mode>           Chia đôi: "vertical" (trái-phải) hoặc "horizontal" (trên-dưới)
    --pages <list>           Chỉ xử lý các trang, ví dụ: 1,3,5-8
    --pattern <str>          Mẫu tên file đầu ra (mặc định: page_{i}.png)
    --format <ext>           Định dạng ảnh đầu ra: png, jpg, webp (mặc định: png)
    --preview                Hiển thị trước danh sách file sẽ tạo mà không xuất thật
"""

import os
import sys
from pdf2image import convert_from_path, pdfinfo_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError
from PIL import Image

def parse_pages(pages_str):
    """Chuyển '1,3,5-8' thành [1,3,5,6,7,8]"""
    pages = set()
    for part in pages_str.split(','):
        if '-' in part:
            start, end = part.split('-')
            pages.update(range(int(start), int(end) + 1))
        else:
            pages.add(int(part))
    return sorted(pages)

def generate_filename(pattern, index, ext):
    """Sinh tên file theo pattern"""
    from datetime import datetime
    now = datetime.now()
    name = pattern
    name = name.replace("{i}", str(index))
    name = name.replace("{date}", now.strftime("%Y%m%d"))
    name = name.replace("{datetime}", now.strftime("%Y%m%d_%H%M%S"))
    name = name.replace("{timestamp}", str(int(now.timestamp())))
    if not os.path.splitext(name)[1]:
        name += f".{ext}"
    return name

def split_image(img, mode):
    """Chia đôi ảnh theo chiều dọc hoặc ngang"""
    width, height = img.size
    if mode == "vertical":
        mid = width // 2
        return [
            img.crop((0, 0, mid, height)),      # trái
            img.crop((mid, 0, width, height))   # phải
        ]
    elif mode == "horizontal":
        mid = height // 2
        return [
            img.crop((0, 0, width, mid)),       # trên
            img.crop((0, mid, width, height))   # dưới
        ]
    return [img]

def normalize_format(fmt):
    fmt = fmt.lower()
    if fmt == "jpg":
        return "jpeg"
    return fmt

def process_pdf(pdf_path, dpi=300, split_mode=None, pages=None, pattern="page_{i}.png", out_format="png", preview=False):
    if not os.path.exists(pdf_path):
        print(f"❌ Không tìm thấy file: {pdf_path}")
        return

    out_format = normalize_format(out_format)

    print(f"📄 File PDF: {pdf_path}")
    print(f"🔧 Cấu hình: DPI={dpi}, Split={'Không' if not split_mode else split_mode}, Format={out_format}")
    print(f"🧩 Pattern: {pattern}")
    if pages:
        print(f"📑 Trang cần xử lý: {pages}")
    print("=" * 50)

    try:
        pdf_info = pdfinfo_from_path(pdf_path)
        total_pages = int(pdf_info.get("Pages", 0))
    except PDFInfoNotInstalledError:
        print("❌ Thiếu Poppler (pdfinfo/pdftoppm). Hãy cài Poppler trước khi chạy.")
        print("   Ubuntu/Debian: sudo apt install poppler-utils")
        return
    except (PDFPageCountError, ValueError):
        print("❌ Không đọc được số trang PDF. File có thể bị lỗi hoặc không hợp lệ.")
        return
    except Exception as err:
        print(f"❌ Lỗi khi đọc thông tin PDF: {err}")
        return

    if total_pages <= 0:
        print("❌ PDF không có trang hợp lệ để xử lý.")
        return

    if pages:
        target_pages = [page for page in pages if 1 <= page <= total_pages]
        invalid_pages = [page for page in pages if page < 1 or page > total_pages]
        if invalid_pages:
            print(f"⚠️ Bỏ qua trang không hợp lệ: {invalid_pages} (PDF có {total_pages} trang)")
    else:
        target_pages = list(range(1, total_pages + 1))

    if not target_pages:
        print("❌ Không có trang hợp lệ để xử lý.")
        return

    count = 1
    preview_list = []

    if preview:
        for _ in target_pages:
            parts_count = 2 if split_mode in ("vertical", "horizontal") else 1
            for _ in range(parts_count):
                filename = generate_filename(pattern, count, out_format)
                preview_list.append(filename)
                count += 1

        print("\n🧾 Preview file sẽ được tạo:")
        for f in preview_list:
            print(f" - {f}")
        print(f"\n🔍 Tổng cộng: {len(preview_list)} file (chưa tạo thật)")
        return

    print(f"🔄 Đang chuyển đổi {len(target_pages)} trang PDF sang ảnh...")
    for index, page_number in enumerate(target_pages, start=1):
        print(f"   • Trang {page_number} ({index}/{len(target_pages)})")
        try:
            images = convert_from_path(
                pdf_path,
                dpi=dpi,
                fmt=out_format,
                first_page=page_number,
                last_page=page_number,
            )
        except PDFSyntaxError:
            print(f"❌ Lỗi cú pháp PDF ở trang {page_number}. Dừng xử lý.")
            return
        except Exception as err:
            print(f"❌ Không thể chuyển trang {page_number}: {err}")
            return

        if not images:
            print(f"⚠️ Trang {page_number} không tạo được ảnh, bỏ qua.")
            continue

        img = images[0]
        parts = split_image(img, split_mode) if split_mode else [img]
        for part in parts:
            filename = generate_filename(pattern, count, out_format)
            preview_list.append(filename)
            part.save(filename, out_format.upper())
            count += 1

    print(f"\n🎉 Hoàn tất! Đã tạo {count - 1} ảnh.")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    pdf_path = sys.argv[1]
    args = sys.argv[2:]

    # Giá trị mặc định
    dpi = 300
    split_mode = None
    pages = None
    pattern = "page_{i}.png"
    out_format = "png"
    preview = False

    # Xử lý tham số
    for i, arg in enumerate(args):
        if arg == "--dpi" and i + 1 < len(args):
            dpi = int(args[i + 1])
        elif arg == "--split" and i + 1 < len(args):
            split_mode = args[i + 1]
        elif arg == "--pages" and i + 1 < len(args):
            pages = parse_pages(args[i + 1])
        elif arg == "--pattern" and i + 1 < len(args):
            pattern = args[i + 1]
        elif arg == "--format" and i + 1 < len(args):
            out_format = args[i + 1].lower()
        elif arg == "--preview":
            preview = True

    process_pdf(pdf_path, dpi, split_mode, pages, pattern, out_format, preview)

if __name__ == "__main__":
    main()
