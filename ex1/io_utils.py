from pathlib import Path
from typing import List, Optional
import cv2
import numpy as np

FORMAT = {".jpg", ".png"}

def list_images(dir_path: str | Path) -> List[Path]:
    p = Path(dir_path).resolve()
    if not p.is_dir():
        raise FileNotFoundError(f"Khong tim thay thu muc: {p}")
    files = [f for f in p.iterdir() if f.is_file() and f.suffix in FORMAT]
    return files

def read_image(path: str | Path) -> Optional[np.ndarray]:
    p = Path(path)
    if not p.is_file():
        return None
    try:
        data = np.fromfile(str(p), dtype=np.uint8)   # đọc bytes raw
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)  # giải mã -> BGR
        return img
    except Exception:
        return None

def select_image_from_list(images_dir: Path = Path("images")) -> Optional[tuple[Path, np.ndarray]]:
    """
    Hiển thị danh sách ảnh và cho phép người dùng chọn một ảnh.
    Trả về (path, img) nếu thành công, None nếu có lỗi.
    """
    paths = list_images(images_dir)
    if not paths:
        print("Không có ảnh trong thư mục.")
        return None

    print("Danh sách ảnh:")
    for i, p in enumerate(paths, 1):
        print(f"{i:02d} - {p.name}")
    
    sel = input(f"Chọn số thứ tự ảnh (1-{len(paths)}): ").strip()
    try:
        idx = int(sel)
        assert 1 <= idx <= len(paths)
    except Exception:
        print("Lựa chọn không hợp lệ.")
        return None

    path = paths[idx - 1]
    img = read_image(path)
    if img is None:
        print("Không đọc được ảnh đã chọn.")
        return None
    
    return (path, img)
