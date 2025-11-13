import cv2
import numpy as np

def build_lut(array: np.ndarray) -> np.ndarray:
        hist, _ = np.histogram(array, 256, range=(0, 256))
        cdf = np.cumsum(hist).astype(np.float64)
        cdf /= cdf[-1]
        return (cdf * 255).astype(np.uint8)

def equalize_histogram(img: np.ndarray) -> np.ndarray:
    if img.dtype != np.uint8:
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    if img.ndim == 2:  # ảnh xám
        lut = build_lut(img)
        return lut[img]
    else:  # ảnh màu
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        y = ycrcb[..., 0]
        lut = build_lut(y)
        ycrcb[..., 0] = lut[y]
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
    
def match_histogram(source: np.ndarray, reference: np.ndarray) -> np.ndarray:
    if source.ndim != 2 or reference.ndim != 2: 
        raise ValueError("Can anh xam 2 chieu")
    
    src_hist , _ = np.histogram(source.ravel(), bins = 256, range=(0, 256))
    src_cdf = np.cumsum(src_hist).astype(np.float64)
    src_cdf /= src_cdf[-1]

    ref_hist, _ = np.histogram(reference.ravel(), bins=256, range=(0, 256))
    ref_cdf = np.cumsum(ref_hist).astype(np.float64)
    ref_cdf /= ref_cdf[-1]
    
    lut = np.interp(src_cdf, ref_cdf, np.arange(256))
    return lut[source.astype(np.uint8)].astype(np.uint8)



def local_hist_equalization(img: np.ndarray, win_size: int = 8) -> np.ndarray:
    # Đảm bảo dtype và kích thước cửa sổ hợp lệ
    if img.dtype != np.uint8:
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    win_size = int(win_size)
    if win_size < 1:
        return img
    if win_size % 2 == 0:
        win_size += 1

    pad = win_size // 2

    if img.ndim == 3:
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        y = ycrcb[..., 0]
        y_eq = local_hist_equalization(y, win_size)
        ycrcb[..., 0] = y_eq
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR).astype(np.uint8)

    # ảnh xám (ndim == 2)
    h, w = img.shape
    padded = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_REFLECT)
    out = np.zeros_like(img)

    for i in range(h):
        for j in range(w):
            local = padded[i:i + win_size, j:j + win_size]
            lut = build_lut(local)
            out[i, j] = lut[padded[i + pad, j + pad]]

    return out.astype(np.uint8)
              


    



        
