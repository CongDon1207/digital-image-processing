# Xử lý ảnh số — Week 2

Mục tiêu: Thực hành các phép biến đổi điểm, lọc không gian và xử lý histogram (cân bằng, matching, local equalization) cho ảnh 8-bit.

- Kiến trúc (cao cấp):
  - `ops/`: các phép xử lý lõi (`point_ops.py`, `spatial_filters.py`, `histogram_ops.py`).
- `IO/`: đọc/ghi, tiện ích kích thước (`image_io.py`).
- `vis/`: hiển thị cửa sổ (`display.py`).
- `gui/controller.py`: giữ trạng thái ảnh gốc/hiện tại và cập nhật lại vùng xem qua `numpy_to_tk`, cung cấp API áp dụng phép biến đổi độc lập từ ảnh gốc, chạy preview trên ảnh thu nhỏ cho các phép nặng nhưng vẫn lưu file ở độ phân giải đầy đủ.
- `gui/views.py`: Control Panel scrollable với radio chọn phép + một nút “Áp dụng” duy nhất; cung cấp slider tham số và tuỳ chọn "Hệ số C tự động" cho log transform, preview giữ đúng tỉ lệ.
- `gui/app.py`: khởi chạy Tk ở chế độ toàn màn hình (zoomed) để tận dụng không gian preview.
  - `images/`: dữ liệu ảnh mẫu.
  - `main.py`: điểm vào (đang để trống cho bài tập).

- Stack & Versions (tham chiếu): Python 3.10+, NumPy, OpenCV (`cv2`).
- Quy ước: Toàn bộ xử lý histogram hoạt động trên miền 8-bit `[0,255]`.
