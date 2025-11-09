import cv2
import numpy as np
from pathlib import Path
from typing import List, Iterable, Tuple
from io_utils import read_img

VALID_FORMAT = {".png", ".bmp", ".jpg", ".jpeg"}

def ensure_dir(path: str | Path) -> Path:
    p = Path(path).expanduser().resolve()
    p.mkdir(parents = True , exist_ok = True)
    return p

def write_image_unicode(path: str | Path, image: np.ndarray , params: List[int] | None = None) -> bool:
    p = Path(path)

    ext = p.suffix
    if ext not in VALID_FORMAT:
        return False
    
    if ext in [".jpg", ".jpeg"] and params is None:
        params = [cv2.IMWRITE_JPEG_QUALITY, 95]

    ok, buf = cv2.imencode(ext, image, params)
    if not ok: 
        return False
    
    try:
        buf.tofile(str(p))
        return True
    except Exception:
        return False
    
def export_three_formats(paths: Iterable[Path],
                        out_png: str | Path,
                        out_jpg: str | Path,
                        out_bmp: str | Path                                        
) -> Tuple[int, int]:
    
    out_png = ensure_dir(out_png)
    out_jpg = ensure_dir(out_jpg)
    out_bmp = ensure_dir(out_bmp)

    total = 0
    cnt_ok = 0

    for src in paths:
        total += 1
        img = read_img(src)
        if img is None: 
            continue


        stem = src.stem

        dst_png = out_png / f"{stem}.png"
        dst_jpg = out_jpg / f"{stem}.jpg"
        dst_bmp = out_bmp / f"{stem}.bmp"

        png_ok = write_image_unicode(dst_png, img)
        jpg_ok = write_image_unicode(dst_jpg, img)
        bmp_ok = write_image_unicode(dst_bmp, img)

        if png_ok and jpg_ok and bmp_ok:
            cnt_ok += 1
            print(f"[OK] {src.name} -> PNG/BMP/JPG")
        else:
            print(f"[ERR] Ghi lỗi: {src.name} (png={png_ok}, bmp={bmp_ok}, jpg={jpg_ok})")
        
    return total, cnt_ok

    


