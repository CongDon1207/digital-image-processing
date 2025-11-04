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
