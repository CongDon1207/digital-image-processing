import cv2
import time
import numpy as np

from IO.image_io import fit_resize
from vis.display import show_window
from ops.spatial_filters import gauss_filter, box_filter
from ops.sharpened_filter import laplacian_sharpen, unsharp_mask
from ops.freq_ops import (
    gaussian_lowpass,
    gaussian_highpass,
    butterworth_lowpass,
    butterworth_highpass,
)

# ============================================================
#  ĐỌC ẢNH
# ============================================================

# Đọc ảnh xám để so sánh cho công bằng
img = cv2.imread("images/image.png", cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError("Không tìm thấy ảnh images/image.png")

# ============================================================
#  1. SO SÁNH SMOOTHING (LÀM MỜ)
# ============================================================

print("=== SO SÁNH SMOOTHING: SPATIAL vs FREQUENCY ===")

# 1.1 Gaussian Low-pass trong FREQUENCY DOMAIN
#     - gaussian_lowpass đã có profile=True để đo chi tiết từng bước (fft, shift, ifft, ...)
out_freq_gauss, times_freq_gauss = gaussian_lowpass(img, D0=30, profile=True)

total_freq_gauss_ms = 0.0
print("\n[Frequency] Gaussian Low-pass (gaussian_lowpass, D0=30):")
for k, v in times_freq_gauss.items():
    t_ms = v * 1000
    print(f"  {k:10s}: {t_ms:8.3f} ms")
    total_freq_gauss_ms += t_ms
print(f"  => Tổng thời gian (FFT + filter + IFFT): {total_freq_gauss_ms:.3f} ms")


# 1.2 Gaussian blur trong SPATIAL DOMAIN (hàm Python gauss_filter của bạn)
t0 = time.perf_counter()
gauss_spatial = gauss_filter(img)
t1 = time.perf_counter()
spatial_gauss_ms = (t1 - t0) * 1000

print("\n[Spatial] Gaussian blur (gauss_filter - Python loops):")
print(f"  Tổng thời gian: {spatial_gauss_ms:.3f} ms")


# 1.3 Box filter trong SPATIAL DOMAIN (làm mờ kiểu trung bình)
t0 = time.perf_counter()
K = np.ones((5, 5), float)
box_spatial = box_filter(img, K)
t1 = time.perf_counter()
spatial_box_ms = (t1 - t0) * 1000

print("\n[Spatial] Box filter (box_filter - Python loops):")
print(f"  Tổng thời gian: {spatial_box_ms:.3f} ms")


# 1.4 Gaussian blur của OpenCV để tham chiếu tốc độ
t0 = time.perf_counter()
gauss_cv = cv2.GaussianBlur(img, (5, 5), 0)
t1 = time.perf_counter()
cv_gauss_ms = (t1 - t0) * 1000

print("\n[Spatial] GaussianBlur OpenCV (cv2.GaussianBlur, ksize=5x5):")
print(f"  Tổng thời gian: {cv_gauss_ms:.3f} ms")


# ============================================================
#  2. SO SÁNH SHARPENING (LÀM SẮC / TĂNG CƯỜNG BIÊN)
# ============================================================

print("\n=== SO SÁNH SHARPENING: SPATIAL vs FREQUENCY ===")

# 2.1 Gaussian High-pass trong FREQUENCY DOMAIN
#     (lọc HPF – kết quả là ảnh chứa chủ yếu high-frequency)
t0 = time.perf_counter()
hp_freq_gauss = gaussian_highpass(img, D0=30)
t1 = time.perf_counter()
freq_hp_gauss_ms = (t1 - t0) * 1000

print("\n[Frequency] Gaussian High-pass (gaussian_highpass, D0=30):")
print(f"  Tổng thời gian: {freq_hp_gauss_ms:.3f} ms")


# 2.2 Butterworth High-pass trong FREQUENCY DOMAIN (ví dụ thêm)
t0 = time.perf_counter()
hp_freq_butter = butterworth_highpass(img, D0=30, n=2)
t1 = time.perf_counter()
freq_hp_butter_ms = (t1 - t0) * 1000

print("\n[Frequency] Butterworth High-pass (butterworth_highpass, D0=30, n=2):")
print(f"  Tổng thời gian: {freq_hp_butter_ms:.3f} ms")


# 2.3 Laplacian sharpening trong SPATIAL DOMAIN
t0 = time.perf_counter()
lap_sharp = laplacian_sharpen(img)
t1 = time.perf_counter()
lap_ms = (t1 - t0) * 1000

print("\n[Spatial] Laplacian sharpening (laplacian_sharpen):")
print(f"  Tổng thời gian: {lap_ms:.3f} ms")


# 2.4 Unsharp masking trong SPATIAL DOMAIN
t0 = time.perf_counter()
unsharp = unsharp_mask(img)
t1 = time.perf_counter()
unsharp_ms = (t1 - t0) * 1000

print("\n[Spatial] Unsharp masking (unsharp_mask):")
print(f"  Tổng thời gian: {unsharp_ms:.3f} ms")


# ============================================================
#  3. HIỂN THỊ KẾT QUẢ ĐỂ SOI MẮT (KHÔNG ẢNH HƯỞNG ĐẾN ĐO TIME)
# ============================================================

# show_window("freq_gauss_LPF", fit_resize(out_freq_gauss))
# show_window("spatial_gauss_filter", fit_resize(gauss_spatial))
# show_window("spatial_box_filter", fit_resize(box_spatial))
# show_window("spatial_gauss_cv2", fit_resize(gauss_cv))

# show_window("freq_gauss_HPF", fit_resize(hp_freq_gauss))
# show_window("freq_butter_HPF", fit_resize(hp_freq_butter))
# show_window("spatial_laplacian_sharp", fit_resize(lap_sharp))
# show_window("spatial_unsharp_mask", fit_resize(unsharp))

# cv2.waitKey(0)
# cv2.destroyAllWindows()
