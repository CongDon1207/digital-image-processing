# practice OpenCV mini tasks

Mục tiêu: bộ bài tập nhỏ dùng OpenCV để:
- Đọc/hiển thị ảnh, tách kênh màu, chuyển xám.
- Xoay + thu nhỏ ảnh theo từng bước và hiển thị trên cùng cửa sổ.
- Crop trung tâm 1/4 kích thước.
- Xuất ảnh sang PNG/JPG/BMP.

Kiến trúc (mức cao):
- `io_utils.py`: đọc ảnh Unicode‑safe, liệt kê tệp.
- `display.py`: các hàm hiển thị cửa sổ.
- `color_ops.py`: chuyển xám, tách R/G/B.
- `crop_ops.py`: crop trung tâm.
- `tranform_ops.py`: fit resize, xoay + scale, hoạt hình.
- `export_utils.py`: ghi ảnh và xuất đa định dạng.

Stack & Versions:
- Python (phiên bản không ghim trong repo).
- OpenCV (cv2) và NumPy (không ghim phiên bản). Hãy dùng môi trường hiện có và kiểm tra bằng `pip show opencv-python numpy` nếu cần.

Quyết định gần đây:
- Đơn giản hóa `animate_rotate_shrink` để tái sử dụng `rotate_scale_fit`, tránh lặp logic tính canvas.

