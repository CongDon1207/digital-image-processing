# Digital Image Processing - Week 2

Ứng dụng xử lý ảnh số hỗ trợ các phép biến đổi điểm, lọc không gian và xử lý histogram.

## Tổng quan
Dự án cung cấp giao diện đồ họa (GUI) để thực hiện các thao tác xử lý ảnh cơ bản:
- **Biến đổi điểm**: Log, Power law, Thresholding.
- **Lọc không gian**: Mean, Median, Gaussian, Laplacian, Sobel, Prewitt.
- **Histogram**: Cân bằng (Equalization), Matching, Local Equalization.

## Kiến trúc
Dự án được tổ chức theo mô hình phân tách logic xử lý và giao diện:
- **`main.py`**: Điểm khởi chạy ứng dụng.
- **`gui/`**: Chứa mã nguồn giao diện (App, Controller, Components).
- **`ops/`**: Chứa các thuật toán xử lý ảnh cốt lõi (Point, Spatial, Histogram, Frequency).
- **`IO/`**: Xử lý đọc/ghi ảnh.
- **`vis/`**: Các tiện ích hiển thị.

## Cài đặt và Chạy
Đảm bảo bạn đã cài đặt Python 3.10+ và các thư viện cần thiết (NumPy, OpenCV, Pillow).

1. Cài đặt thư viện (nếu chưa có):
   ```bash
   pip install numpy opencv-python pillow
   ```

2. Chạy ứng dụng:
   ```bash
   python main.py
   ```
