from pathlib import Path
import cv2
from io_utils import read_image, save_image

def convert_folder_to_gray(input_dir="images", output_dir="gray_images"):
    in_dir = Path(input_dir)
    out_dir = Path(output_dir)
    out_dir.mkdir(exist_ok=True)

    for img_path in in_dir.iterdir():
        if img_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".bmp"]:
            continue
        img = read_image(img_path)
        if img is None:
            print(f"Không đọc được: {img_path.name}")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        out_path = out_dir / img_path.name
        save_image(out_path, gray)
        print(f"Đã chuyển: {img_path.name} → xám")

    print("Hoàn tất!")

if __name__ == "__main__":
    convert_folder_to_gray()
