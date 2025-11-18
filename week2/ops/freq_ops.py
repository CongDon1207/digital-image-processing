import numpy as np
import cv2
import time
from typing import Literal


def _build_distance_matrix(rows: int, cols: int) -> np.ndarray:
    """
    Tạo ma trận khoảng cách D(u, v) tới tâm (M/2, N/2) trong miền tần số.

    D(u, v) ~ khoảng cách tần số:
    - gần tâm  => tần số thấp
    - xa tâm   => tần số cao
    """
    # toạ độ dịch tâm về 0
    u = np.arange(rows) - rows / 2.0
    v = np.arange(cols) - cols / 2.0
    U, V = np.meshgrid(u, v, indexing="ij")
    D = np.sqrt(U ** 2 + V ** 2).astype(np.float32)
    return D


def _apply_freq_filter_single_channel(
    A: np.ndarray,
    H: np.ndarray,
    profile: bool = False,
):
    """
    Áp dụng bộ lọc H(u,v) cho 1 kênh ảnh (2D) trong miền tần số.

    Quy trình:
        F      = FFT2(A)
        Fshift = fftshift(F)
        G      = H * Fshift
        g      = ifft2(ifftshift(G))

    Nếu profile=True, trả về (img_back, times_dict)
    trong đó times_dict chứa thời gian từng bước.
    """
    times = {}

    # 1) FFT2
    t0 = time.perf_counter()
    f = np.fft.fft2(A.astype(np.float32))
    t1 = time.perf_counter()
    times["fft2"] = t1 - t0

    # 2) fftshift
    fshift = np.fft.fftshift(f)
    t2 = time.perf_counter()
    times["fftshift"] = t2 - t1

    # 3) Nhân với H(u,v)
    G = fshift * H
    t3 = time.perf_counter()
    times["mul_H"] = t3 - t2

    # 4) ifftshift
    g_ishift = np.fft.ifftshift(G)
    t4 = time.perf_counter()
    times["ifftshift"] = t4 - t3

    # 5) ifft2
    img_back = np.fft.ifft2(g_ishift)
    t5 = time.perf_counter()
    times["ifft2"] = t5 - t4

    # 6) lấy phần thực
    img_back = np.real(img_back)
    t6 = time.perf_counter()
    times["real"] = t6 - t5

    img_back = img_back.astype(np.float32)

    if profile:
        return img_back, times
    else:
        return img_back


def _apply_freq_filter(
    A: np.ndarray,
    H: np.ndarray,
    profile: bool = False,
):
    """
    Áp dụng bộ lọc tần số H(u,v) cho ảnh xám hoặc màu.

    - A: ảnh đầu vào (2D hoặc 3D), uint8 hoặc tương đương.
    - H: ma trận cùng kích thước (h, w), áp dụng cho mọi kênh.
    - profile:
        False -> chỉ trả ảnh.
        True  -> trả (ảnh, times):
                 * xám  -> times là dict
                 * màu -> times là list[dict] cho từng kênh.

    Trả về:
    - Ảnh sau khi lọc (và info thời gian nếu profile=True).
    """
    if A.ndim == 2:
        if profile:
            out, times = _apply_freq_filter_single_channel(A, H, profile=True)
            out = np.clip(out, 0, 255).astype(A.dtype)
            return out, times
        else:
            out = _apply_freq_filter_single_channel(A, H, profile=False)
            out = np.clip(out, 0, 255).astype(A.dtype)
            return out
    else:
        h, w, c = A.shape
        out = np.zeros_like(A, dtype=np.float32)
        all_times = []

        for ch in range(c):
            if profile:
                ch_out, times = _apply_freq_filter_single_channel(
                    A[..., ch], H, profile=True
                )
                all_times.append(times)
            else:
                ch_out = _apply_freq_filter_single_channel(
                    A[..., ch], H, profile=False
                )
            out[..., ch] = ch_out

        out = np.clip(out, 0, 255).astype(A.dtype)

        if profile:
            return out, all_times
        else:
            return out


# ============================================================
#  LOW-PASS FILTERS (Smoothing trong miền tần số)
# ============================================================

def ideal_lowpass(
    A: np.ndarray,
    D0: float,
    profile: bool = False,
):
    """
    Ideal Low-pass Filter (ILPF):

    H(u,v) = 1 nếu D(u,v) <= D0
             0 nếu D(u,v) >  D0

    - A : ảnh đầu vào (xám hoặc màu).
    - D0: bán kính cắt (cutoff frequency).
    - profile: nếu True, trả (ảnh, times).

    Tác dụng:
    - Giữ tần số thấp, xoá tần số cao -> ảnh mờ mạnh, dễ gây ringing.
    """
    if D0 <= 0:
        return (A, {}) if profile else A

    if A.ndim == 2:
        rows, cols = A.shape
    else:
        rows, cols = A.shape[:2]

    D = _build_distance_matrix(rows, cols)
    H = (D <= float(D0)).astype(np.float32)

    if profile:
        return _apply_freq_filter(A, H, profile=True)
    else:
        return _apply_freq_filter(A, H, profile=False)


def butterworth_lowpass(
    A: np.ndarray,
    D0: float,
    n: int = 2,
    profile: bool = False,
):
    """
    Butterworth Low-pass Filter (BLPF):

        H(u,v) = 1 / [1 + (D(u,v)/D0)^(2n)]

    - A : ảnh đầu vào (xám hoặc màu).
    - D0: bán kính cắt.
    - n : bậc Butterworth, n càng lớn biên càng gắt.
    - profile: nếu True, trả (ảnh, times).

    Tác dụng:
    - Làm mờ ảnh, mềm hơn Ideal LPF, ít ringing hơn.
    """
    if D0 <= 0:
        return (A, {}) if profile else A
    n = max(int(n), 1)

    if A.ndim == 2:
        rows, cols = A.shape
    else:
        rows, cols = A.shape[:2]

    D = _build_distance_matrix(rows, cols)
    # tránh chia cho 0
    D_norm = D / float(D0)
    H = 1.0 / (1.0 + (D_norm ** (2 * n)))
    H = H.astype(np.float32)

    if profile:
        return _apply_freq_filter(A, H, profile=True)
    else:
        return _apply_freq_filter(A, H, profile=False)


def gaussian_lowpass(
    A: np.ndarray,
    D0: float,
    profile: bool = False,
):
    """
    Gaussian Low-pass Filter (GLPF):

        H(u,v) = exp( - D(u,v)^2 / (2 * D0^2) )

    - A : ảnh đầu vào (xám hoặc màu).
    - D0: tương tự sigma trong Gaussian theo miền tần số.
    - profile: nếu True, trả (ảnh, times).

    Tác dụng:
    - Làm mờ mượt, hầu như không gây ringing.
    """
    if D0 <= 0:
        return (A, {}) if profile else A

    if A.ndim == 2:
        rows, cols = A.shape
    else:
        rows, cols = A.shape[:2]

    D = _build_distance_matrix(rows, cols)
    H = np.exp(- (D ** 2) / (2.0 * float(D0) ** 2))
    H = H.astype(np.float32)

    if profile:
        return _apply_freq_filter(A, H, profile=True)
    else:
        return _apply_freq_filter(A, H, profile=False)


# ============================================================
#  HIGH-PASS FILTERS (Sharpen trong miền tần số)
# ============================================================

def ideal_highpass(
    A: np.ndarray,
    D0: float,
    profile: bool = False,
):
    """
    Ideal High-pass Filter (IHPF):

    H(u,v) = 0 nếu D(u,v) <= D0
             1 nếu D(u,v) >  D0

    - A : ảnh đầu vào (xám hoặc màu).
    - D0: bán kính cắt.
    - profile: nếu True, trả (ảnh, times).

    Tác dụng:
    - Giữ tần số cao, loại tần số thấp -> nổi biên mạnh, dễ nhiễu & ringing.
    """
    if D0 <= 0:
        return (A, {}) if profile else A

    if A.ndim == 2:
        rows, cols = A.shape
    else:
        rows, cols = A.shape[:2]

    D = _build_distance_matrix(rows, cols)
    H = (D > float(D0)).astype(np.float32)

    if profile:
        return _apply_freq_filter(A, H, profile=True)
    else:
        return _apply_freq_filter(A, H, profile=False)


def butterworth_highpass(
    A: np.ndarray,
    D0: float,
    n: int = 2,
    profile: bool = False,
):
    """
    Butterworth High-pass Filter (BHPF):

        H(u,v) = 1 / [1 + (D0 / D(u,v))^(2n)]

    hoặc tương đương:
        H_hp = 1 - H_lp(Butterworth)

    - A : ảnh đầu vào (xám hoặc màu).
    - D0: bán kính cắt.
    - n : bậc Butterworth.
    - profile: nếu True, trả (ảnh, times).

    Tác dụng:
    - Làm sắc ảnh, nhấn mạnh biên, mềm hơn Ideal HPF.
    """
    if D0 <= 0:
        return (A, {}) if profile else A
    n = max(int(n), 1)

    if A.ndim == 2:
        rows, cols = A.shape
    else:
        rows, cols = A.shape[:2]

    D = _build_distance_matrix(rows, cols)
    # Để tránh chia cho 0 tại tâm, ép D=epsilon
    D_safe = np.where(D == 0, 1e-6, D).astype(np.float32)
    D_ratio = (float(D0) / D_safe) ** (2 * n)
    H = 1.0 / (1.0 + D_ratio)
    H = H.astype(np.float32)

    if profile:
        return _apply_freq_filter(A, H, profile=True)
    else:
        return _apply_freq_filter(A, H, profile=False)


def gaussian_highpass(
    A: np.ndarray,
    D0: float,
    profile: bool = False,
):
    """
    Gaussian High-pass Filter (GHPF):

        H(u,v) = 1 - exp( - D(u,v)^2 / (2 * D0^2) )

    - A : ảnh đầu vào (xám hoặc màu).
    - D0: tham số tần số cắt.
    - profile: nếu True, trả (ảnh, times).

    Tác dụng:
    - Làm sắc ảnh mượt, ít ringing nhất trong các HPF chuẩn.
    """
    if D0 <= 0:
        return (A, {}) if profile else A

    if A.ndim == 2:
        rows, cols = A.shape
    else:
        rows, cols = A.shape[:2]

    D = _build_distance_matrix(rows, cols)
    H_lp = np.exp(- (D ** 2) / (2.0 * float(D0) ** 2))
    H = 1.0 - H_lp
    H = H.astype(np.float32)

    if profile:
        return _apply_freq_filter(A, H, profile=True)
    else:
        return _apply_freq_filter(A, H, profile=False)
