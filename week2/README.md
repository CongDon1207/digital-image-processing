# Xử lý ảnh số — Week 2

Mục tiêu: Thực hành các phép biến đổi điểm, lọc không gian và xử lý histogram (cân bằng, matching, local equalization) cho ảnh 8-bit.

- Kiến trúc (cao cấp):
  - `ops/`: các phép xử lý lõi (`point_ops.py`, `spatial_filters.py`, `histogram_ops.py`).
- `IO/`: đọc/ghi, tiện ích kích thước (`image_io.py`).
- `vis/`: hiển thị cửa sổ (`display.py`).
- `gui/controller.py`: giữ trạng thái ảnh gốc/hiện tại và cập nhật lại vùng xem qua `numpy_to_tk`.
  - `images/`: dữ liệu ảnh mẫu.
  - `main.py`: điểm vào (đang để trống cho bài tập).

- Stack & Versions (tham chiếu): Python 3.10+, NumPy, OpenCV (`cv2`).
- Quy ước: Toàn bộ xử lý histogram hoạt động trên miền 8-bit `[0,255]`.
