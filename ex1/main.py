# main.py
from pathlib import Path
from io_utils import list_images, read_image
from export_utils import export_to_three_formats, ensure_dir

def run_export():
    images_dir = Path("images")
    paths = list_images(images_dir)
    print(f"Tìm thấy {len(paths)} ảnh trong: {images_dir.resolve()}")
    if not paths:
        print("Thư mục rỗng.")
        return

    # Tạo thư mục đích
    out_png = Path("export_png")
    out_bmp = Path("export_bmp")
    out_jpg = Path("export_jpg")
    for d in (out_png, out_bmp, out_jpg):
        ensure_dir(d)

    ok_cnt, total = export_to_three_formats(paths, out_png, out_bmp, out_jpg)
    print(f"Hoàn thành: {ok_cnt}/{total} ảnh đã xuất đủ 3 định dạng.")

def main():
    # Menu rất đơn giản để bạn chạy từng bước
    # 1 = kiểm tra đọc ảnh (bước 1), 2 = xuất 3 định dạng (bước 2)
    choice = input("Chọn tác vụ (1=check đọc ảnh, 2=export 3 định dạng): ").strip()

    if choice == "1":
        images_dir = Path("images")
        paths = list_images(images_dir)
        print(f"Tìm thấy {len(paths)} ảnh trong: {images_dir.resolve()}")
        for i, p in enumerate(paths, 1):
            print(f"{i:02d}-{p.name}")
        if paths:
            sample = read_image(paths[0])
            if sample is None:
                print("Không đọc được ảnh mẫu.")
            else:
                h, w = sample.shape[:2]
                print(f"Ảnh mẫu: {paths[0].name} -> {w}x{h} (BGR)")
    elif choice == "2":
        run_export()
    else:
        print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()
