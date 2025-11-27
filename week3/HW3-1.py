import cv2
from pathlib import Path
from filter import gaussian_highpass_filter, gaussian_lowpass_filter, normalize_for_display
from display import show_three_images

if __name__ == '__main__':
    image_path = 'images/handXray.png'
    image_hand = cv2.imread(image_path, 0)

    if image_hand is None:
        print(f"Không tìm thấy file ảnh: {Path(image_path).name}")
    else:
        print("Đọc ảnh thành công, bắt đầu xử lý...")

        D0_val = 25
        img_low       = gaussian_lowpass_filter(image_hand, D0_val)
        img_final_hw1 = gaussian_highpass_filter(img_low, D0_val)

        show_three_images(
            normalize_for_display(image_hand),"Original Image",
            normalize_for_display(img_low), "Gaussian Lowpass (D0={D0_val})",
            normalize_for_display(img_final_hw1), "Gaussian Highpass sau Lowpass (D0={D0_val})"
        )
        print("Hoàn thành xử lý HW3-1.")


