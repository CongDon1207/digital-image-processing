# display.py
from pathlib import Path
from typing import Iterable, Tuple
import cv2
import numpy as np

from io_utils import read_image

def fit_resize(img: np.ndarray, max_w: int = 900, max_h: int = 700) -> np.ndarray:
    """
    Thu nhỏ ảnh về kích thước tối đa (giữ tỉ lệ). Không phóng to ảnh nhỏ.
    """
    h, w = img.shape[:2]
    scale = min(max_w / w, max_h / h, 1.0)  # <=1: chỉ thu nhỏ
    if scale < 1.0:
        new_size: Tuple[int, int] = (int(w * scale), int(h * scale))
        return cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
    return img

def show_set_each_window(paths: Iterable[Path], max_w: int = 900, max_h: int = 700) -> None:
    """
    Mỗi ảnh -> một cửa sổ mang tên file. Ấn bất kỳ phím để đóng tất cả.
    """
    windows = []
    try:
        for p in paths:
            img = read_image(p)
            if img is None:
                print(f"[WARN] Không đọc được: {p.name}")
                continue
            view = fit_resize(img, max_w=max_w, max_h=max_h)
            win_name = str(p.name)
            cv2.namedWindow(win_name, cv2.WINDOW_AUTOSIZE)  # mỗi ảnh một cửa sổ
            cv2.setWindowProperty(win_name, cv2.WND_PROP_TOPMOST, 1)
            cv2.imshow(win_name, view)
            windows.append(win_name)

        if not windows:
            print("Không có ảnh để hiển thị.")
            return

        print("Đang hiển thị. Nhấn bất kỳ phím nào trong *bất kỳ* cửa sổ để đóng.")
        cv2.waitKey(0)  # chờ người dùng
    finally:
        cv2.destroyAllWindows()

def show_gray(gray: np.ndarray, win_name: str = "gray", max_w: int = 900, max_h: int = 700) -> None:
    """
    Hiển thị ảnh xám trong một cửa sổ.
    """
    # xám là 2D; để fit giống nhau, ta resize qua ảnh xám luôn
    h, w = gray.shape[:2]
    scale = min(max_w / w, max_h / h, 1.0)
    view = gray
    if scale < 1.0:
        view = cv2.resize(gray, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
    cv2.namedWindow(win_name, cv2.WINDOW_AUTOSIZE)
    cv2.setWindowProperty(win_name, cv2.WND_PROP_TOPMOST, 1)
    cv2.imshow(win_name, view)

def show_channels(r: np.ndarray, g: np.ndarray, b: np.ndarray, title_prefix: str = "") -> None:
    """
    Hiển thị ba ảnh kênh (xám) R/G/B ở 3 cửa sổ khác nhau.
    Nhấn phím bất kỳ để đóng.
    """
    win_r = f"{title_prefix}_R" if title_prefix else "R"
    win_g = f"{title_prefix}_G" if title_prefix else "G"
    win_b = f"{title_prefix}_B" if title_prefix else "B"

    show_gray(r, win_r)
    show_gray(g, win_g)
    show_gray(b, win_b)

    print("Đang hiển thị kênh R/G/B. Nhấn phím bất kỳ để đóng.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
