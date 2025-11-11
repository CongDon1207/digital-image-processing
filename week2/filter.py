import cv2
import numpy as np

def median_filter(A: np.ndarray, s: int) -> np.ndarray:
    """
    Lọc trung vị giữ nguyên kích thước bằng cách pad 0 xung quanh.
    """
    s = int(s)
    if s < 1:
        return A
    ph = s // 2
    pw = s // 2

    if A.ndim == 2:
        h, w = A.shape[:2]
        P = np.pad(A, ((ph, ph), (pw, pw)), mode='constant', constant_values=0)
        B = np.zeros_like(A)
        for i in range(h):
            for j in range(w):
                sA = P[i:i + s, j:j + s]
                B[i, j] = np.median(sA)
    else:
        h, w, c = A.shape
        P = np.pad(A, ((ph, ph), (pw, pw), (0, 0)), mode='constant', constant_values=0)
        B = np.zeros_like(A)
        for i in range(h):
            for j in range(w):
                for ch in range(c):
                    sA = P[i:i + s, j:j + s, ch]
                    B[i, j, ch] = np.median(sA)
    B = np.clip(B, 0, 255).astype(A.dtype)
    return B

def max_filter(A: np.ndarray, s: int) -> np.ndarray:
    """
    Lọc cực đại giữ nguyên kích thước (pad 0).
    """
    s = int(s)
    if s < 1:
        return A
    ph = s // 2
    pw = s // 2

    if A.ndim == 2:
        h, w = A.shape[:2]
        P = np.pad(A, ((ph, ph), (pw, pw)), mode='constant', constant_values=0)
        B = np.zeros_like(A)
        for i in range(h):
            for j in range(w):
                sA = P[i:i + s, j:j + s]
                B[i, j] = np.max(sA)
    else:
        h, w, c = A.shape
        P = np.pad(A, ((ph, ph), (pw, pw), (0, 0)), mode='constant', constant_values=0)
        B = np.zeros_like(A)
        for i in range(h):
            for j in range(w):
                for ch in range(c):
                    sA = P[i:i + s, j:j + s, ch]
                    B[i, j, ch] = np.max(sA)
    B = np.clip(B, 0, 255).astype(A.dtype)
    return B

def min_filter(A: np.ndarray, s: int) -> np.ndarray:
    """
    Lọc cực tiểu giữ nguyên kích thước (pad 0).
    """
    s = int(s)
    if s < 1:
        return A
    ph = s // 2
    pw = s // 2

    if A.ndim == 2:
        h, w = A.shape[:2]
        P = np.pad(A, ((ph, ph), (pw, pw)), mode='constant', constant_values=0)
        B = np.zeros_like(A)
        for i in range(h):
            for j in range(w):
                sA = P[i:i + s, j:j + s]
                B[i, j] = np.min(sA)
    else:
        h, w, c = A.shape
        P = np.pad(A, ((ph, ph), (pw, pw), (0, 0)), mode='constant', constant_values=0)
        B = np.zeros_like(A)
        for i in range(h):
            for j in range(w):
                for ch in range(c):
                    sA = P[i:i + s, j:j + s, ch]
                    B[i, j, ch] = np.min(sA)
    B = np.clip(B, 0, 255).astype(A.dtype)
    return B

def conv_avg(A: np.ndarray, K: np.ndarray) -> np.ndarray:
 
    kh, kw = K.shape[:2]
    ph, pw = kh // 2, kw // 2  

    K = K / np.sum(K)

    if A.ndim == 2:
        P = np.pad(A, ((ph, ph), (pw, pw)), mode='constant', constant_values=0)
        B = np.zeros_like(A, dtype=float)
        h, w = A.shape
        
        for i in range(h):
            for j in range(w):
                region = P[i:i + kh, j:j + kw]      
                B[i, j] = np.sum(region * K)
    else:
        # Ảnh màu: pad 3 chiều (height, width, channels)
        P = np.pad(A, ((ph, ph), (pw, pw), (0, 0)), mode='constant', constant_values=0)
        B = np.zeros_like(A, dtype=float)
        h, w, c = A.shape
        
        for i in range(h):
            for j in range(w):
                for ch in range(c):
                    region = P[i:i + kh, j:j + kw, ch]      
                    B[i, j, ch] = np.sum(region * K)
    
    B = np.clip(B, 0, 255).astype(A.dtype)
    return B

def gauss_filter(A: np.ndarray, ksize: int = 3, sigma: float | None = None) -> np.ndarray:
    """
    Tham số:
    - A: ảnh đầu vào (xám hoặc màu), dtype giữ nguyên.
    - ksize: kích thước kernel (số lẻ), mặc định 3.
    - sigma: độ lệch chuẩn; nếu None sẽ ước lượng từ ksize.
    """
    k = int(ksize)
    if k < 1:
        return A
    if k % 2 == 0:
        k += 1  # đảm bảo số lẻ

    if sigma is None:
        # xấp xỉ đơn giản, đủ dùng: tỉ lệ theo ksize
        sigma = max(k / 6.0, 1e-6)

    # toạ độ đối xứng quanh 0
    r = k // 2
    x = np.arange(-r, r + 1, dtype=np.float32)
    g1 = np.exp(-(x ** 2) / (2.0 * float(sigma) ** 2))
    # kernel 2D bằng tích ngoài => chuẩn hoá sẽ do conv_avg xử lý
    K = np.outer(g1, g1)

    return conv_avg(A, K.astype(np.float32))
