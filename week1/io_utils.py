import cv2
import numpy as np
from pathlib import Path
from typing import List, Optional
from tranform_ops import fit_resize

FORMAT = {".png", ".bmp", ".jpg", ".jpeg"}

def read_img(path: str | Path) -> Optional[np.ndarray]:
    p = Path(path)
    if not p.is_file():
        return None
    try:
        data = np.fromfile(str(p), dtype = np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        return fit_resize(img)
    except Exception:
        return None
    
def list_img(dir_path: str | Path) -> List[Path]:
    p = Path(dir_path).resolve()
    if not p.is_dir():
        raise FileNotFoundError("Khong tim thay duong dan: ")
    
    files = [f for f in p.iterdir() if f.is_file() and f.suffix in FORMAT]
    return files

def select_image_from_list(dir_path: str | Path) -> Optional[tuple[Path, np.ndarray]]:
    paths = list_img(dir_path)
    if not paths:
        print("Không có ảnh trong thư mục.")
        return None

    print("Danh sách ảnh:")
    for i, p in enumerate(paths, 1):
        print(f"{i:02d} - {p.name}")
    
    selection = input(f"Chọn số thứ tự ảnh (1-{len(paths)}): ").strip()

    try:
        idx = int(selection)
        assert 1 <= idx <= len(paths)
    except Exception:
        print("Lựa chọn không hợp lệ.")
        return None
    
    path = paths[idx - 1]
    img = read_img(path)

    if img is None :
        print("Không đọc được ảnh đã chọn.")
        return None
    
    return path, img


