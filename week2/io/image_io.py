import cv2
import numpy as np
from typing import List, Optional
from pathlib import Path

def fit_resize(img: np.ndarray, max_w: int = 900, max_h: int = 700) -> np.ndarray:

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
