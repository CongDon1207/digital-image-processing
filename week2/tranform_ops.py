import cv2
import numpy as np
from io_utils import read_image
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
    negative_img = np.max(img) - img
    return negative_img



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
    normalize_img = img.astype(np.float32) / 255.0  # Tránh tràn khi lũy thừa

    scale = 1.0 if c is None else float(c)
    gamma_img = scale * np.power(normalize_img * gamma)
    gamma_img = np.clip(gamma_img * 255, 0, 255)

    return gamma_img.astype(np.uint8)







    