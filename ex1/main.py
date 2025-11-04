# main.py
from pathlib import Path
from io_utils import list_images, read_image, select_image_from_list
from export_utils import export_to_three_formats, ensure_dir
from display import show_set_each_window, show_channels, show_gray
from color_ops import split_rgb, to_gray
from transform_ops import animate_rotate_shrink
from crop_ops import center_crop_quarter
import cv2

def run_export():
    images_dir = Path("images")
    paths = list_images(images_dir)
    print(f"Tìm thấy {len(paths)} ảnh trong: {images_dir.resolve()}")
    if not paths:
        print("Thư mục rỗng.")
        return
    out_png = Path("export_png")
    out_bmp = Path("export_bmp")
    out_jpg = Path("export_jpg")
    for d in (out_png, out_bmp, out_jpg):
        ensure_dir(d)
    ok_cnt, total = export_to_three_formats(paths, out_png, out_bmp, out_jpg)
    print(f"Hoàn thành: {ok_cnt}/{total} ảnh đã xuất đủ 3 định dạng.")

def run_show_each_window():
    images_dir = Path("images")
    paths = list_images(images_dir)
    print(f"Hiển thị {len(paths)} ảnh (mỗi ảnh một cửa sổ).")
    show_set_each_window(paths, max_w=900, max_h=700)

def run_split_rgb():
    result = select_image_from_list()
    if result is None:
        return
    
    path, img = result
    r, g, b = split_rgb(img)
    show_channels(r, g, b, title_prefix=path.stem)

def run_gray_only():
    result = select_image_from_list()
    if result is None:
        return
    
    path, img = result
    gray = to_gray(img)
    show_gray(gray, win_name=f"{path.stem}_GRAY")
    print("Nhấn phím bất kỳ để đóng.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def run_rotate_animation():
    result = select_image_from_list()
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
        delay_ms=30,
        min_scale=0.15
    )

def run_center_crop():
    result = select_image_from_list()
    if result is None:
        return
    
    path, img = result
    cropped = center_crop_quarter(img)
    
    win = f"{path.stem}_CROP"
    cv2.namedWindow(win, cv2.WINDOW_AUTOSIZE)
    cv2.setWindowProperty(win, cv2.WND_PROP_TOPMOST, 1)
    cv2.imshow(win, cropped)
    print("Nhấn phím bất kỳ để đóng.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def run_check_read():
    """Kiểm tra đọc ảnh từ thư mục images."""
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