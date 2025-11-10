import cv2
import numpy as np
from typing import Tuple, Iterable
from pathlib import Path
from io_utils import read_img
from color_ops import to_gray, split_rgb
from tranform_ops import fit_resize
from crop_ops import center_crop_quarter

def show_window(win_name: str, img: np.ndarray, window_flag: int = cv2.WINDOW_AUTOSIZE, window_prop: int = cv2.WND_PROP_TOPMOST) -> None:
    cv2.namedWindow(win_name, window_flag)
    cv2.setWindowProperty(win_name, window_prop, 1)
    cv2.imshow(win_name, img)

def show_each_window(paths: Iterable[Path], max_w: int = 1200, max_h: int = 627) -> None:
    windows = []

    try:
        for p in paths:
            img = read_img(p)
            if img is None:
                print(f"[WARN] Không đọc được: {p.name}")
                continue
            new_img = fit_resize(img, max_w, max_h)
            win_name = str(p.name)
            show_window(win_name, new_img)
            windows.append(win_name)

        if not windows:
            print("No image")
            return
        
        print("Đang hiển thị. Nhấn bất kỳ phím nào trong *bất kỳ* cửa sổ để đóng.")
        cv2.waitKey(0)

    finally:
        cv2.destroyAllWindows()



def show_gray(win_name: str, img: np.ndarray, max_w: int = 1200, max_h: int = 627) -> None:
    gray = to_gray(img)
    new_gray = fit_resize(gray, max_w = max_w, max_h = max_h)

    show_window(win_name, new_gray)

    print("Nhấn phím bất kỳ để đóng.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_channels(img: np.ndarray, title_prefix: str = "", max_w: int = 1200, max_h: int = 627) -> None:

    r, g, b = split_rgb(img)
    r = fit_resize(r, max_w = max_w, max_h = max_h)
    g = fit_resize(g, max_w = max_w, max_h = max_h)
    b = fit_resize(b, max_w = max_w, max_h = max_h)

    win_r = f"{title_prefix}_R" if title_prefix else "R"
    win_g = f"{title_prefix}_G" if title_prefix else "G"
    win_b = f"{title_prefix}_B" if title_prefix else "B"

    show_window(win_r, r)
    show_window(win_g, g)
    show_window(win_b, b)

    print("Nhấn phím bất kỳ để đóng.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_crop(win_name: str, img: np.ndarray, max_w: int = 1200, max_h: int = 627) -> None:
    cropped = center_crop_quarter(img)
    new_cropped = fit_resize(cropped, max_w = max_w, max_h = max_h)
    show_window(win_name, new_cropped)

    print("Nhấn phím bất kỳ để đóng.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()




