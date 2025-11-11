import cv2
import numpy as np
from typing import List, Optional
from pathlib import Path
from tranform_ops import fit_resize

def read_image(path: str | Path) -> Optional[np.ndarray]:
    p = Path(path)
    if not p.is_file():
        return None
    
    data = np.fromfile(p, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    resized_img = fit_resize(img)
    return resized_img
