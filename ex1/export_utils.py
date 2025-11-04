# export_utils.py
from pathlib import Path
from typing import Iterable, Tuple
import cv2
import numpy as np

from io_utils import read_image  # đã viết ở bước 1

VALID_EXTS = {".png", ".bmp", ".jpg", ".jpeg"}

def ensure_dir(dir_path: str | Path) -> Path:
    """
    Tạo thư mục nếu chưa tồn tại. Trả về Path đã chuẩn hoá.
    """
    p = Path(dir_path).expanduser().resolve()
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_image_unicode(path: str | Path, img: np.ndarray, params: list[int] | None = None) -> bool:
    """
    Ghi ảnh an toàn với đường dẫn Unicode:
    - Dùng cv2.imencode theo phần mở rộng đích ('.png', '.bmp', '.jpg', '.jpeg')
    - Sau đó buf.tofile() để lưu.
    Trả về True/False.
    """
    p = Path(path)
    ext = p.suffix.lower()
    if ext not in VALID_EXTS:
        raise ValueError(f"Phần mở rộng không hỗ trợ: {ext} (hỗ trợ: {VALID_EXTS})")

    # Mặc định set chất lượng JPG hợp lý nếu không truyền params
    if params is None and ext in {".jpg", ".jpeg"}:
        params = [cv2.IMWRITE_JPEG_QUALITY, 95]

    ok, buf = cv2.imencode(ext, img, params or [])
    if not ok:
        return False
    try:
        buf.tofile(str(p))  # an toàn Unicode trên Windows
        return True
    except Exception:
        return False

def export_to_three_formats(
    image_paths: Iterable[Path],
    out_png: str | Path,
    out_bmp: str | Path,
    out_jpg: str | Path,
) -> Tuple[int, int]:
    """
    Đọc từng ảnh trong image_paths và ghi ra 3 định dạng vào 3 thư mục tương ứng.
    Giữ nguyên tên (stem). Trả về (số_ảnh_thành_công, tổng_ảnh_xử_lý).
    """
    out_png = ensure_dir(out_png)
    out_bmp = ensure_dir(out_bmp)
    out_jpg = ensure_dir(out_jpg)

    total = 0
    ok_cnt = 0

    for src in image_paths:
        total += 1
        img = read_image(src)
        if img is None:
            print(f"[WARN] Không đọc được: {src.name}")
            continue

        stem = src.stem
        dst_png = out_png / f"{stem}.png"
        dst_bmp = out_bmp / f"{stem}.bmp"
        dst_jpg = out_jpg / f"{stem}.jpg"

        ok1 = write_image_unicode(dst_png, img)
        ok2 = write_image_unicode(dst_bmp, img)
        ok3 = write_image_unicode(dst_jpg, img)

        if ok1 and ok2 and ok3:
            ok_cnt += 1
            print(f"[OK] {src.name} -> PNG/BMP/JPG")
        else:
            print(f"[ERR] Ghi lỗi: {src.name} (png={ok1}, bmp={ok2}, jpg={ok3})")

    return ok_cnt, total
