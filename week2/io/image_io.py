import cv2
import numpy as np
from typing import List, Optional
from pathlib import Path

def fit_resize(img: np.ndarray, max_w: int = 1200, max_h: int = 900) -> np.ndarray:

    h, w = img.shape[:2]
    scale = min(float(max_h/h) , float(max_w/w), 1.0)
    if scale < 1.0:
        new_size = (int(scale * w), int(scale * h))
        img = cv2.resize(img, new_size, interpolation = cv2.INTER_AREA)
    return img

def read_image(path: str | Path) -> Optional[np.ndarray]:
    p = Path(path)
    if not p.is_file():
        return None
    
    data = np.fromfile(p, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    resized_img = fit_resize(img)
    return resized_img

def to_gray(img: np.ndarray) -> np.ndarray:
    """
    Chuyển ảnh BGR sang ảnh xám.
    """
    if img is None:
        return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

def read_image_and_convert_gray(path: str | Path) -> Optional[np.ndarray]:
    p = Path(path)
    if not p.is_file():
        return None
    
    data = np.fromfile(p, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    resized_img = fit_resize(img)
    gray_img = to_gray(resized_img)
    return gray_img

def save_image(img: np.ndarray, path: str | Path) -> bool:
    """
    Lưu ảnh xuống file. Hỗ trợ đường dẫn Unicode.
    """
    if img is None:
        return False
    
    try:
        p = Path(path)
        ext = p.suffix
        if not ext:
            ext = ".png" # Default extension
            
        success, encoded_img = cv2.imencode(ext, img)
        if success:
            with open(p, "wb") as f:
                encoded_img.tofile(f)
            return True
    except Exception as e:
        print(f"Lỗi khi lưu ảnh: {e}")
        return False
    return False



