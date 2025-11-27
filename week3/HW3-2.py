import cv2
from pathlib import Path
from filter import apply_filter_multipass, normalize_for_display
from display import show_four_images


if __name__ == '__main__':
    image_path = 'images/pcb_xray.png'
    image_pcb = cv2.imread(image_path, 0)

    if image_pcb is None:
        print(f"Không tìm thấy file ảnh: {Path(image_path).name}")
    else:
        print("Đọc ảnh PCB thành công, bắt đầu xử lý HW3-2...")

        D0_val = 30

        img_hp_1   = apply_filter_multipass(image_pcb, D0_val, passes=1)
        img_hp_10  = apply_filter_multipass(image_pcb, D0_val, passes=10)
        img_hp_100 = apply_filter_multipass(image_pcb, D0_val, passes=100)

        show_four_images(
            normalize_for_display(image_pcb),  "Original",
            normalize_for_display(img_hp_1),   "1 pass HPF",
            normalize_for_display(img_hp_10),  "10 passes HPF",
            normalize_for_display(img_hp_100), "100 passes HPF"
        )

        print("Hoàn thành xử lý HW3-2.")