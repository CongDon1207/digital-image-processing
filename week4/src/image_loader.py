import cv2
import numpy as np
from pathlib import Path

def load_binary_image(image_path, invert=False):    
    path_obj = Path(image_path)
    if not path_obj.exists():
        print(f"Lỗi: Không tìm thấy file tại {path_obj.absolute()}")
        return None
    
    img = cv2.imread(str(path_obj), cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print("Lỗi: Không đọc được định dạng ảnh.")
        return None

    thresh_val, binary_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    if invert:
        binary_img = cv2.bitwise_not(binary_img)

    return binary_img

