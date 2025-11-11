Trạng thái hiện tại
- Đã thêm gauss_filter (tuần 2), dùng kernel Gauss + conv_avg.
- Đã sửa bộ lọc median/max/min giữ nguyên kích thước (pad 0).
- Đã sửa negative_image, gamma_transform, piecewise_linear theo công thức chuẩn.
- Đã sửa io_utils.read_image: dùng is_file() và trả Optional.

Tiếp theo / TODO
- (Tùy chọn) Gắn ví dụ gauss_filter vào week2/main.py.
- (Tùy chọn) Cho phép chọn mode pad: 'constant'/'replicate' cho các bộ lọc.

Đường dẫn chính
- week2/filter.py
- week2/main.py

Kiểm tra gần nhất
- Các bộ lọc cửa sổ giữ nguyên kích thước và dtype.
- negative/gamma/piecewise_linear cho kết quả trong [0,255].

Môi trường
- Python + OpenCV (cv2) + NumPy; không thay đổi phụ thuộc.
