import cv2
import numpy as np
from pathlib import Path

def show_window(win_name: str, img: np.ndarray, window_flag: int = cv2.WINDOW_AUTOSIZE, window_prop: int = cv2.WND_PROP_TOPMOST) -> None:
    cv2.namedWindow(win_name, window_flag)
    cv2.setWindowProperty(win_name, window_prop, 1)
    cv2.imshow(win_name, img)
 