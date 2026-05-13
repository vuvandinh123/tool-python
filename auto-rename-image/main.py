#!/usr/bin/env python3
"""
Tool đổi tên ảnh hàng loạt với nhiều tùy chọn
Cách sử dụng:
    rename-images <thư_mục> <pattern> [--convert] [--preview] [--start N] [--compress [QUALITY]]
    hoặc (khi chạy trực tiếp file):
    python3 main.py <thư_mục> <pattern> [--convert] [--preview] [--start N] [--compress [QUALITY]]
    
Ví dụ:
    rename-images /home/images photo_{i}.png
    rename-images /home/images IMG_{date}.jpg
    rename-images /home/images picture_{i:04d}.png --convert
    rename-images /home/images picture_{i:04d}.png --preview
    rename-images /home/images image_{i}.jpg --start 0
    rename-images /home/images image_{i}.jpg --compress
    rename-images /home/images image_{i}.jpg --compress 75
    
Pattern hỗ trợ:
    {i} - Số thứ tự (1, 2, 3...)
    {i:04d} - Số thứ tự với padding (0001, 0002...)
    {date} - Ngày tháng hiện tại (YYYYMMDD)
    {datetime} - Ngày giờ hiện tại (YYYYMMDD_HHMMSS)
    {timestamp} - Unix timestamp
"""

import os
import sys
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from PIL import Image
import re

SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

def get_target_extension(pattern):
    ext = Path(pattern).suffix.lower()
    return ext if ext in SUPPORTED_FORMATS else None

def get_image_files(directory, target_ext=None):
    files = []
    for file in sorted(os.listdir(directory)):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            ext = Path(file).suffix.lower()
            if ext in SUPPORTED_FORMATS:
                if target_ext is None or ext == target_ext:
                    files.append(file)
    return files

def convert_image(source_path, target_ext):
    try:
        img = Image.open(source_path)
        if target_ext in ['.jpg', '.jpeg'] and img.mode in ('RGBA', 'LA', 'P'):
            bg = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            bg.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = bg
        return img
    except Exception as e:
        print(f"❌ Lỗi khi convert {source_path}: {e}")
        return None

def get_save_kwargs(ext, compress_quality):
    if compress_quality is None:
        return {}

    quality = max(1, min(100, compress_quality))

    if ext in ['.jpg', '.jpeg']:
        return {'quality': quality, 'optimize': True}
    if ext == '.png':
        compress_level = int(round((100 - quality) * 9 / 100))
        return {'optimize': True, 'compress_level': compress_level}
    if ext == '.webp':
        return {'quality': quality, 'method': 6}
    if ext in ['.tiff', '.bmp']:
        return {'optimize': True}
    return {}

def save_image(img, path, ext, compress_quality=None):
    save_kwargs = get_save_kwargs(ext, compress_quality)
    img.save(path, **save_kwargs)

def generate_filename(pattern, index, total):
    now = datetime.now()
    filename = pattern

    # {i}
    filename = filename.replace('{i}', str(index))
    # {i:04d}
    matches = re.finditer(r'\{i:(\d+)d\}', filename)
    for match in matches:
        width = int(match.group(1))
        filename = filename.replace(match.group(0), str(index).zfill(width))
    # {date}
    filename = filename.replace('{date}', now.strftime('%Y%m%d'))
    # {datetime}
    filename = filename.replace('{datetime}', now.strftime('%Y%m%d_%H%M%S'))
    # {timestamp}
    filename = filename.replace('{timestamp}', str(int(now.timestamp())))

    return filename

def rename_images(directory, pattern, convert_mode=False, preview=False, start_index=1, compress_quality=None):
    if not os.path.isdir(directory):
        print(f"❌ Thư mục không tồn tại: {directory}")
        return
    
    target_ext = get_target_extension(pattern)

    if target_ext:
        print(f"📋 Định dạng đích: {target_ext}")
        if convert_mode:
            print(f"🔄 Chế độ convert: BẬT - Sẽ convert tất cả ảnh sang {target_ext}")
            image_files = get_image_files(directory)
        else:
            print(f"🔄 Chế độ convert: TẮT - Chỉ đổi tên ảnh {target_ext}")
            image_files = get_image_files(directory, target_ext)
    else:
        print(f"⚠️ Không xác định được định dạng từ pattern, sẽ giữ nguyên định dạng gốc")
        image_files = get_image_files(directory)
    
    if not image_files:
        print(f"❌ Không tìm thấy ảnh nào trong thư mục!")
        return

    print(f"✅ Tìm thấy {len(image_files)} ảnh")
    print(f"📁 Thư mục: {directory}")
    print(f"📝 Pattern: {pattern}")
    print(f"🔢 Bắt đầu đánh số từ: {start_index}")
    if compress_quality is not None:
        print(f"🗜️  Nén ảnh: BẬT (mức chất lượng {compress_quality})")
    else:
        print(f"🗜️  Nén ảnh: TẮT")
    print(f"👀 Chế độ Preview: {'BẬT' if preview else 'TẮT'}")
    print("\n" + "="*50)
    
    backup_dir = os.path.join(directory, '.backup_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
    success_count = 0

    total_files = len(image_files)
    for seq, old_filename in enumerate(image_files, start=1):
        idx = start_index + seq - 1
        old_path = os.path.join(directory, old_filename)
        old_ext = Path(old_filename).suffix.lower()
        new_filename = generate_filename(pattern, idx, len(image_files))
        if not get_target_extension(pattern):
            new_filename = Path(new_filename).stem + old_ext
        new_path = os.path.join(directory, new_filename)

        if preview:
            print(f"👁️  [{seq}/{total_files}] Sẽ đổi:")
            print(f"   {old_filename} -> {new_filename}")
            continue

        try:
            if convert_mode and target_ext and old_ext != target_ext:
                print(f"🔄 [{seq}/{total_files}] Convert & Đổi tên:")
                print(f"   {old_filename} -> {new_filename}")
                img = convert_image(old_path, target_ext)
                if img:
                    if not os.path.exists(backup_dir):
                        os.makedirs(backup_dir)
                    shutil.copy2(old_path, os.path.join(backup_dir, old_filename))
                    save_image(img, new_path, target_ext, compress_quality)
                    os.remove(old_path)
                    success_count += 1
                else:
                    print(f"   ⚠️ Bỏ qua do lỗi convert")
            elif compress_quality is not None:
                print(f"🗜️  [{seq}/{total_files}] Nén & Đổi tên:")
                print(f"   {old_filename} -> {new_filename}")
                with Image.open(old_path) as source_img:
                    img = source_img.copy()
                if old_ext in ['.jpg', '.jpeg'] and img.mode in ('RGBA', 'LA', 'P'):
                    bg = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    bg.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = bg
                if not os.path.exists(backup_dir):
                    os.makedirs(backup_dir)
                shutil.copy2(old_path, os.path.join(backup_dir, old_filename))
                save_image(img, new_path, old_ext, compress_quality)
                os.remove(old_path)
                success_count += 1
            else:
                print(f"✏️  [{seq}/{total_files}] Đổi tên:")
                print(f"   {old_filename} -> {new_filename}")
                if not os.path.exists(backup_dir):
                    os.makedirs(backup_dir)
                shutil.copy2(old_path, os.path.join(backup_dir, old_filename))
                os.rename(old_path, new_path)
                success_count += 1
        except Exception as e:
            print(f"   ❌ Lỗi: {e}")

    print("\n" + "="*50)
    if preview:
        print(f"👁️  Đây là chế độ preview — không có thay đổi nào được áp dụng.")
    else:
        print(f"✅ Hoàn thành! Đã xử lý {success_count}/{len(image_files)} ảnh")
        print(f"💾 Backup được lưu tại: {backup_dir}")

def main():
    parser = argparse.ArgumentParser(
        description='Tool đổi tên ảnh hàng loạt với nhiều tùy chọn'
    )
    parser.add_argument('directory', help='Thư mục chứa ảnh')
    parser.add_argument('pattern', help='Pattern đặt tên mới, ví dụ: photo_{i}.jpg')
    parser.add_argument('-c', '--convert', action='store_true', help='Convert ảnh theo đuôi file trong pattern')
    parser.add_argument('-p', '--preview', action='store_true', help='Chỉ xem trước, không ghi thay đổi')
    parser.add_argument('--start', type=int, default=1, help='Số bắt đầu cho {i}, ví dụ 0, 1, n (mặc định: 1)')
    parser.add_argument(
        '-z', '--compress',
        nargs='?',
        const=85,
        type=int,
        help='Bật nén ảnh, có thể truyền mức chất lượng 1-100 (mặc định khi không truyền: 85)'
    )

    args = parser.parse_args()

    if args.compress is not None and not (1 <= args.compress <= 100):
        parser.error('--compress chỉ nhận giá trị từ 1 đến 100')

    print("="*50)
    print("🖼️  TOOL ĐỔI TÊN ẢNH HÀNG LOẠT")
    print("="*50)

    rename_images(
        args.directory,
        args.pattern,
        args.convert,
        args.preview,
        start_index=args.start,
        compress_quality=args.compress
    )

if __name__ == '__main__':
    main()
