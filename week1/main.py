from display import show_each_window, show_channels, show_gray, show_crop
from io_utils import list_img, read_img, select_image_from_list
from export_utils import export_three_formats
from pathlib import Path
from tranform_ops import animate_rotate_shrink

def run_check_read():
    """Kiểm tra đọc ảnh từ thư mục images."""
    images_dir = Path("images")
    paths = list_img(images_dir)
    print(f"Tìm thấy {len(paths)} ảnh trong: {images_dir.resolve()}")
    for i, p in enumerate(paths, 1):
        print(f"{i:02d}-{p.name}")
    if paths:
        sample = read_img(paths[0])
        if sample is None:
            print("Không đọc được ảnh mẫu.")
        else:
            h, w = sample.shape[:2]
            print(f"Ảnh mẫu: {paths[0].name} -> {w}x{h} (BGR)")

def run_export():
    images_dir = Path("images")
    paths = list_img(images_dir)
    print(f"Tìm thấy {len(paths)} ảnh trong: {images_dir.resolve()}")
    if not paths:
        print("Thư mục rỗng.")
        return
    out_png = Path("images_png")
    out_jpg = Path("images_jpg")
    out_bmp = Path("images_bmp")
    
    total, ok_cnt  = export_three_formats(paths, out_png, out_jpg, out_bmp)
    print(f"Hoàn thành: {ok_cnt}/{total} ảnh đã xuất đủ 3 định dạng.")

def run_show_each_window():
    images_dir = Path("images")
    paths = list_img(images_dir)
    print(f"Hiển thị {len(paths)} ảnh (mỗi ảnh một cửa sổ).")
    show_each_window(paths, max_w=900, max_h=700)

def run_split_rgb():
    result = select_image_from_list("images")
    if result is None:
        return
    
    path, img = result
    show_channels(img, title_prefix=path.stem)

def run_gray_only():
    result = select_image_from_list("images")
    if result is None:
        return
    
    path, img = result
    
    show_gray(win_name=f"{path.stem}_GRAY", img = img)

def run_rotate_animation():
    result = select_image_from_list("images")
    if result is None:
        return
    
    path, img = result

    print("Đang chạy hoạt hình (ESC để dừng sớm)...")
    animate_rotate_shrink(
        img_bgr=img,
        steps=50,
        angle_step=15.0,
        scale_step=0.9,
        win_name=f"{path.stem}_ANIM",
        delay_ms=90,
        min_scale=0.001
    )

def run_center_crop():
    result = select_image_from_list("images")
    if result is None:
        return
    
    path, img = result
    show_crop(f"{path.stem}_CROP", img)


def main():
    choice = input(
        "Chọn tác vụ:\n"
        "1=check đọc\n"
        "2=export ảnh ra 3 định dạng\n"
        "3=hiển thị mỗi ảnh 1 cửa sổ\n"
        "4=tách ảnh màu thành 3 kênh (R,G,B)\n"
        "5=chuyển ảnh RGB sang xám\n"
        "6=quay ảnh 50 lần (15°/bước) + thu nhỏ 0.9\n"
        "7=crop trung tâm 1/4 ảnh\n> "
    ).strip()

    tasks = {
        "1": run_check_read,
        "2": run_export,
        "3": run_show_each_window,
        "4": run_split_rgb,
        "5": run_gray_only,
        "6": run_rotate_animation,
        "7": run_center_crop,
    }
    
    task_function = tasks.get(choice)
    if task_function:
        task_function()
    else:
        print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()

