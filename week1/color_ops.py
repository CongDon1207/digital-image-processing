import cv2
import numpy as np
from typing import Tuple

def split_rgb(img_bgr: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray] :
    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    r = rgb[:, :, 0]
    g = rgb[:, :, 1]
    b = rgb[:, :, 2]

    return r,g,b

def to_gray(img_bgr: np.ndarray) -> np.ndarray:
    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    
    return gray



