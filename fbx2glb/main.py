#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

# ------------------------------
#  MÀU CHO LOG CONSOLE
# ------------------------------
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


# ------------------------------
#  HÀM CHẠY LỆNH SHELL
# ------------------------------
def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return False, result.stderr
        return True, result.stdout
    except Exception as e:
        return False, str(e)


# ------------------------------
#  NÉN DRACO
# ------------------------------
def apply_draco(input_glb, output_glb):
    cmd = ["gltf-transform", "draco", input_glb, output_glb]
    return run_cmd(cmd)


# ------------------------------
#  NÉN TEXTURE → KTX2
# ------------------------------
def apply_ktx2(input_glb, output_glb):
    cmd = ["gltf-transform", "etc1s", input_glb, output_glb]
    return run_cmd(cmd)


# ------------------------------
#  CHƯƠNG TRÌNH CHÍNH
# ------------------------------
def main():
    if len(sys.argv) != 3:
        print(RED + "❌ Sai cú pháp!" + RESET)
        print("Cách dùng:")
        print(CYAN + "python3 optimize_glb_folder.py <glb_folder> <output_folder>" + RESET)
        return

    glb_dir = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])

    if not glb_dir.exists():
        print(RED + f"❌ Thư mục GLB không tồn tại: {glb_dir}" + RESET)
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    print(GREEN + "🚀 BẮT ĐẦU NÉN TOÀN BỘ GLB" + RESET)

    glb_files = [f for f in glb_dir.glob("*.glb")]

    if not glb_files:
        print(RED + "❌ Không tìm thấy file GLB nào." + RESET)
        return

    for glb in glb_files:
        name = glb.stem
        temp_glb = out_dir / f"{name}_draco.glb"
        final_glb = out_dir / f"{name}.glb"

        print("\n" + CYAN + f"[>] Xử lý: {name}" + RESET)

        # Skip nếu file đã có
        if final_glb.exists():
            print(YELLOW + f"⏩ Bỏ qua (đã tồn tại): {final_glb.name}" + RESET)
            continue

        # 1) Draco compress
        print("  → Draco compress...")
        ok, msg = apply_draco(str(glb), str(temp_glb))
        if not ok:
            print(RED + f"❌ Lỗi Draco: {msg}" + RESET)
            continue

        # 2) Texture KTX2 compress
        print("  → KTX2 texture optimize...")
        ok, msg = apply_ktx2(str(temp_glb), str(final_glb))
        if not ok:
            print(RED + f"❌ Lỗi KTX2: {msg}" + RESET)
            continue

        print(GREEN + f"✔ Hoàn tất: {final_glb.name}" + RESET)

        # Cleanup
        if temp_glb.exists():
            temp_glb.unlink()

    print("\n" + GREEN + "🎉 DONE – Tất cả GLB đã được tối ưu!" + RESET)


if __name__ == "__main__":
    main()
