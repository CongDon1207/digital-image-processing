# digital-image-processing

- Bổ sung hàm lọc `gauss_filter` (tuần 2) sử dụng kernel Gauss và tái sử dụng hàm `conv_avg` để chập, đảm bảo code tối giản, dễ đọc.
 - Sửa logic: `median_filter`/`max_filter`/`min_filter` giữ nguyên kích thước bằng padding (tuần 2).
 - Sửa `negative_image`, `gamma_transform`, `piecewise_linear` (tuần 2) theo công thức chuẩn; `io_utils.read_image` dùng `is_file()` và trả Optional.
