import cv2
import numpy as np
from typing import Optional
from pathlib import Path

def fit_resize(img: np.ndarray, max_w: int = 900, max_h: int = 700) -> np.ndarray:

    h, w = img.shape[:2]
    scale = min(float(max_h/h) , float(max_w/w), 1.0)
    if scale < 1.0:
        new_size = (int(scale * w), int(scale * h))
        img = cv2.resize(img, new_size, interpolation = cv2.INTER_AREA)
    return img

def negative_image(img: np.ndarray) -> np.ndarray:
    img = fit_resize(img)
    # Âm bản theo miền giá trị của dtype (uint8 -> 255)
    if np.issubdtype(img.dtype, np.integer):
        max_val = np.iinfo(img.dtype).max
        negative_img = max_val - img
        return negative_img.astype(img.dtype)
    else:
        # Ảnh float: giả định miền [0,1]
        negative_img = 1.0 - img.astype(np.float32)
        return negative_img.astype(img.dtype)



def log_transform(img: np.ndarray, c: Optional[float] = None) -> np.ndarray:
    float_img = img.astype(np.float32)
    max_val = float_img.max()
    if max_val <= 0:
        return np.zeros_like(img)
    
    scale = float(255.0 / np.log1p(max_val)) if c is None else float(c)
    log_img = scale * np.log1p(float_img)
    log_img = np.clip(log_img, 0, 255)
    return log_img.astype(np.uint8)


def gamma_transform(img: np.ndarray, c: Optional[float] = None, gamma: float = 1.0):
    normalize_img = img.astype(np.float32) / 255.0
    scale = 1.0 if c is None else float(c)
    gamma = float(gamma)
    # Đúng công thức: s = c * r^gamma, với r∈[0,1]
    gamma_img = scale * np.power(normalize_img, gamma)
    gamma_img = np.clip(gamma_img, 0.0, 1.0)
    gamma_img = (gamma_img * 255.0).astype(np.uint8)
    return gamma_img



def piecewise_linear(img: np.ndarray, r1: int, s1: int, r2: int, s2: int) -> np.ndarray:
    """
    Biến đổi tuyến tính theo từng đoạn:
      [0, r1] -> [0, s1]
      (r1, r2] -> (s1, s2]
      (r2, 255] -> (s2, 255]
    Dùng để kéo giãn độ tương phản cho ảnh tối/nhạt.

    Công thức 3 đoạn (ghi chú):
      s = {
            (s1/r1) * r,                                 0 ≤ r ≤ r1
            ((s2 - s1)/(r2 - r1)) * (r - r1) + s1,       r1 < r ≤ r2
            ((255 - s2)/(255 - r2)) * (r - r2) + s2,     r2 < r ≤ 255
          }
    Trong đó:
    - [r1, r2]: dải cường độ gốc cần nhấn mạnh.
    - [s1, s2]: dải cường độ đích được kéo, giãn ra.
    """
    r1, s1, r2, s2 = int(r1), int(s1), int(r2), int(s2)
    if not (0 <= r1 <= r2 <= 255 and 0 <= s1 <= s2 <= 255):
        raise ValueError("Require: 0 <= r1 <= r2 <= 255 and 0 <= s1 <= s2 <= 255")
    
    x = img.astype(np.float32)
    y = np.empty_like(x, dtype = np.float32) 

    a1 = (s1 / r1) if r1 > 0 else 0.0
    a2 = ((s2 - s1) / (r2 - r1)) if (r2 - r1) > 0 else 0.0
    a3 = ((255 - s2) / (255 - r2)) if (255 - r2) > 0 else 0.0

    m1 = x <= r1
    m2 = (x > r1) & (x <= r2)
    m3 = x > r2

    y[m1] = a1 * x[m1]
    y[m2] = a2 * (x[m2] - r1) + s1
    y[m3] = a3 * (x[m3] - r2) + s2

    y = np.clip(y, 0, 255)
    return y.astype(np.uint8)




    
