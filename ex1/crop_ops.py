# crop_ops.py
import numpy as np

def center_crop_quarter(img_bgr: np.ndarray) -> np.ndarray:
    """
    Cắt phần trung tâm có kích thước bằng 1/4 diện tích ảnh gốc:
    - Theo chiều rộng & cao: giữ 1/2 mỗi chiều (tức W/2 x H/2), nằm giữa ảnh.
    """
    h, w = img_bgr.shape[:2]
    y1 = h // 4
    y2 = 3 * h // 4
    x1 = w // 4
    x2 = 3 * w // 4
    return img_bgr[y1:y2, x1:x2]
