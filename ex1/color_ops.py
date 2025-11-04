# color_ops.py
import cv2
import numpy as np
from typing import Tuple

def bgr_to_rgb(img_bgr: np.ndarray) -> np.ndarray:
    """
    OpenCV đọc BGR. Hàm này đổi sang RGB để đúng nghĩa khi 'split RGB'.
    """
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

def split_rgb(img_bgr: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Trả về 3 ảnh xám tương ứng kênh R, G, B.
    Cách làm: chuyển BGR -> RGB rồi tách kênh.
    """
    rgb = bgr_to_rgb(img_bgr)
    r = rgb[:, :, 0]
    g = rgb[:, :, 1]
    b = rgb[:, :, 2]
    return r, g, b  # mỗi kênh là ảnh 2D (grayscale)

def to_gray(img_bgr: np.ndarray) -> np.ndarray:
    """
    Chuyển ảnh màu BGR sang ảnh xám (1 kênh).
    """
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
