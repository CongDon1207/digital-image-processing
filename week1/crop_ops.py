import cv2
import numpy as np

def center_crop_quarter(img: np.ndarray) -> np.ndarray:
    h, w = img.shape[:2]

    x1 = w // 4
    y1 = h // 4

    x2 = x1 * 3
    y2 = y1 * 3

    return img[y1:y2, x1:x2]

