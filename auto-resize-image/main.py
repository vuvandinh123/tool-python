#!/usr/bin/env python3
"""
Auto Resize Image - CLI

Usage:
    python3 main.py <directory> [options]

Examples:
    # Preview resize theo width 800 (chỉ hiển thị)
    python3 main.py ./photos -w 800 --preview

    # Resize tất cả ảnh trong folder theo width 800, lưu vào ./out, thêm suffix _sm
    python3 main.py ./photos -w 800 -o ./out --suffix _sm

    # Resize theo scale 0.5 (50% của kích thước gốc)
    python3 main.py ./photos --scale 0.5 -o ./out

    # Resize đệ quy (cả subfolders)
    python3 main.py ./photos -w 1024 -r -o ./out

Options:
    -w --width <px>       : target width in pixels
    -h --height <px>      : target height in pixels
    -s --scale <float>    : scale factor (e.g. 0.5)
    -o --output <path>    : output directory (default: ./resized)
    --keep_ext            : Keep original extension (default True)
    --suffix <text>       : suffix to append before extension (default `_resized`)
    --quality <int>       : JPEG quality 1-95 (default 85)
    -r --recursive        : search images recursively in subfolders
    -p --preview          : preview only (no files written)
    --overwrite           : overwrite files in output if exist
"""

import os
import sys
from pathlib import Path
from PIL import Image
from typing import List, Tuple
import argparse

SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

def collect_images(directory: Path, recursive: bool) -> List[Path]:
    if recursive:
        files = [p for p in directory.rglob('*') if p.is_file() and p.suffix.lower() in SUPPORTED_FORMATS]
    else:
        files = [p for p in directory.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_FORMATS]
    return sorted(files)

def calc_target_size(orig_size: Tuple[int,int], width, height, scale) -> Tuple[int,int]:
    ow, oh = orig_size
    if scale is not None:
        if scale <= 0:
            raise ValueError("Scale must be > 0")
        return max(1, int(ow * scale)), max(1, int(oh * scale))
    if width is not None and height is not None:
        return width, height
    if width is not None:
        # keep aspect ratio
        h = int((width / ow) * oh)
        return width, max(1, h)
    if height is not None:
        w = int((height / oh) * ow)
        return max(1, w), height
    # no resize -> return original
    return ow, oh

def ensure_dir(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

def build_output_path(src: Path, input_base: Path, output_base: Path, suffix: str, keep_ext: bool) -> Path:
    # preserve relative path from input_base
    rel = src.relative_to(input_base)
    parent = output_base.joinpath(rel.parent)
    ensure_dir(parent)
    stem = rel.stem
    ext = rel.suffix if keep_ext else src.suffix
    new_name = f"{stem}{suffix}{ext}"
    return parent.joinpath(new_name)

def resize_and_save(src: Path, dst: Path, size: Tuple[int,int], quality: int, overwrite: bool):
    if dst.exists() and not overwrite:
        raise FileExistsError(f"{dst} already exists (use --overwrite to replace)")
    with Image.open(src) as im:
        # Convert palette/rgba to suitable mode for saving as JPEG if needed
        target_w, target_h = size
        if (im.width, im.height) == (target_w, target_h):
            # same size -> just copy (or save to new path)
            im_copy = im.copy()
            im_copy.save(dst, quality=quality)
            return

        # Use thumbnail or resize? Use resize with ANTIALIAS for exact size.
        # If we want to keep aspect ratio when only one dimension given, caller already computed size.
        resized = im.resize((target_w, target_h), Image.LANCZOS)
        # For JPEG, ensure mode is RGB
        if dst.suffix.lower() in ['.jpg', '.jpeg'] and resized.mode in ('RGBA', 'LA', 'P'):
            bg = Image.new('RGB', resized.size, (255,255,255))
            if resized.mode == 'P':
                resized = resized.convert('RGBA')
            bg.paste(resized, mask=resized.split()[-1] if resized.mode in ('RGBA','LA') else None)
            resized = bg
        # Save with quality for JPEG, else default
        save_kwargs = {}
        if dst.suffix.lower() in ['.jpg', '.jpeg']:
            save_kwargs['quality'] = quality
            save_kwargs['optimize'] = True
        resized.save(dst, **save_kwargs)

def parse_args():
    p = argparse.ArgumentParser(description="Auto resize images (CLI)")
    p.add_argument("directory", help="Input directory with images")
    p.add_argument("-w","--width", type=int, help="Target width in px")
    p.add_argument("-t","--height", type=int, help="Target height in px")
    p.add_argument("--scale", type=float, help="Scale factor (e.g. 0.5)")
    p.add_argument("-o","--output", default="./resized", help="Output directory (default ./resized)")
    p.add_argument("--suffix", default="_resized", help="Suffix appended to filename (default _resized)")
    p.add_argument("--keep_ext", action="store_true", help="Keep original extension (default true behaviour)")
    p.add_argument("--quality", type=int, default=85, help="JPEG quality 1-95 (default 85)")
    p.add_argument("-r","--recursive", action="store_true", help="Process subfolders recursively")
    p.add_argument("-p","--preview", action="store_true", help="Preview only (no files written)")
    p.add_argument("--overwrite", action="store_true", help="Overwrite existing files in output")
    return p.parse_args()

def main():
    args = parse_args()
    input_dir = Path(args.directory).expanduser().resolve()
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"❌ Directory not found: {input_dir}")
        sys.exit(1)

    output_dir = Path(args.output).expanduser().resolve()
    image_files = collect_images(input_dir, args.recursive)
    if not image_files:
        print("⚠️ No images found.")
        sys.exit(0)

    print(f"Found {len(image_files)} images in {input_dir}")
    print(f"Output: {output_dir}")
    print(f"Preview mode: {'ON' if args.preview else 'OFF'}")
    print("-"*60)

    # iterate
    processed = 0
    for src in image_files:
        try:
            target_size = calc_target_size((src.stat().st_size, 0), None, None, None)  # dummy to avoid linter (we compute properly below)
            # open to get original size
            with Image.open(src) as im:
                orig_size = (im.width, im.height)
            target_size = calc_target_size(orig_size, args.width, args.height, args.scale)
            # If target equals original and preview is off and output path equals src and not overwrite -> we'll still copy if output different.
            dst = build_output_path(src, input_dir, output_dir, args.suffix, keep_ext=True)
            # If preview, just print
            if args.preview:
                print(f"[{processed+1}/{len(image_files)}] {src.relative_to(input_dir)}: {orig_size} -> {target_size} -> {dst.relative_to(output_dir)}")
                processed += 1
                continue

            # ensure output dir exists
            ensure_dir(dst.parent)
            # Perform resize & save
            resize_and_save(src, dst, target_size, quality=args.quality, overwrite=args.overwrite)
            print(f"[{processed+1}/{len(image_files)}] {src.relative_to(input_dir)}: {orig_size} -> {target_size} -> {dst.relative_to(output_dir)}")
            processed += 1
        except Exception as e:
            print(f"   ❌ Error processing {src}: {e}")

    print("-"*60)
    print(f"Done. Processed {processed}/{len(image_files)} images.")
    if not args.preview:
        print(f"Saved to: {output_dir}")

if __name__ == "__main__":
    main()
