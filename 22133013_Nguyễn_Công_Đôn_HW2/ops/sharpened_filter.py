import cv2
import numpy as np
from ops.spatial_filters import gauss_filter


def _linear_response(A: np.ndarray, K: np.ndarray) -> np.ndarray:

    K = np.asarray(K, dtype=np.float32)
    kh, kw = K.shape[:2]
    ph, pw = kh // 2, kw // 2

    if A.ndim == 2:
        h, w = A.shape[:2]
        P = np.pad(A, ((ph, ph), (pw, pw)), mode='constant', constant_values=0)
        R = np.zeros((h, w), dtype=np.float32)
        for i in range(h):
            for j in range(w):
                region = P[i:i + kh, j:j + kw]
                R[i, j] = np.sum(region * K)
    else:
        h, w, c = A.shape
        P = np.pad(A, ((ph, ph), (pw, pw), (0, 0)), mode='constant', constant_values=0)
        R = np.zeros((h, w, c), dtype=np.float32)
        for i in range(h):
            for j in range(w):
                for ch in range(c):
                    region = P[i:i + kh, j:j + kw, ch]
                    R[i, j, ch] = np.sum(region * K)

    return R




def laplacian_sharpen(A: np.ndarray,
                      eight_conn: bool = False,
                      alpha: float = 1.0) -> np.ndarray:
    """
    Làm sắc nét bằng Laplacian:
    g = f - alpha * Laplacian(f)

    Tham số:
    - eight_conn: False => kernel 4-neighbors, True => 8-neighbors.
    - alpha: hệ số tăng cường độ sắc nét.
    """
    if eight_conn:
        K = np.array([[1, 1, 1],
                      [1, -8, 1],
                      [1, 1, 1]], dtype=np.float32)
    else:
        K = np.array([[0, 1, 0],
                      [1, -4, 1],
                      [0, 1, 0]], dtype=np.float32)

    L = _linear_response(A, K)                
    F = A.astype(np.float32)
    out = F - float(alpha) * L               
    out = np.clip(out, 0, 255).astype(A.dtype)
    return out


def unsharp_mask(A: np.ndarray,
                 ksize: int = 5,
                 sigma: float | None = None,
                 amount: float = 1.0) -> np.ndarray:
    """
    Unsharp masking cổ điển:
    blur  = Gaussian(f)
    mask  = f - blur
    g     = f + amount * mask

    - amount = 1.0  ~ unsharp mask cơ bản
    - amount > 1.0  => sắc mạnh hơn (gần giống high-boost)
    """
    F = A.astype(np.float32)
    blur = gauss_filter(A, ksize=ksize, sigma=sigma).astype(np.float32)
    mask = F - blur
    out = F + float(amount) * mask
    out = np.clip(out, 0, 255).astype(A.dtype)
    return out



def high_boost_sharpen(A: np.ndarray,
                       ksize: int = 5,
                       sigma: float | None = None,
                       k: float = 1.5) -> np.ndarray:
    """
    High-boost filtering:
    g = k * f - blur(f), với k > 1

    Quan hệ với unsharp:
    g = f + (k-1) * (f - blur(f))

    - k = 1     => không sharpen
    - k ~ 1.2–2 => hay dùng thực tế
    """
    F = A.astype(np.float32)
    blur = gauss_filter(A, ksize=ksize, sigma=sigma).astype(np.float32)
    out = float(k) * F - blur
    out = np.clip(out, 0, 255).astype(A.dtype)
    return out


def sobel_sharpen(A: np.ndarray,
                  alpha: float = 1.0) -> np.ndarray:
    """
    Làm sắc nét bằng biên Sobel:
    Gx, Gy = Sobel(f)
    mag    = sqrt(Gx^2 + Gy^2)
    g      = f + alpha * mag
    """

    Kx = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]], dtype=np.float32)
    Ky = np.array([[-1, -2, -1],
                   [ 0,  0,  0],
                   [ 1,  2,  1]], dtype=np.float32)

    # Tính gradient
    Gx = _linear_response(A, Kx)
    Gy = _linear_response(A, Ky)
    mag = np.sqrt(Gx ** 2 + Gy ** 2)

    F = A.astype(np.float32)
    out = F + float(alpha) * mag
    out = np.clip(out, 0, 255).astype(A.dtype)
    return out
