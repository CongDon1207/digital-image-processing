# HANDOFF

Current status:
- Control panel mới hỗ trợ scroll, mỗi phép có radio chọn và dùng chung 1 nút “Áp dụng” phía dưới; preview giữ đúng tỉ lệ cho cả ảnh gốc/kết quả.
- Control panel bổ sung checkbox “Hệ số C tự động” cho phép log và hỗ trợ cuộn bằng bánh xe chuột, giúp thao tác nhanh hơn.
- Controller bổ sung API `apply_operation`, `restore_original`, `save_current`, scale ảnh theo kích thước panel và chạy các phép nặng (lọc, local histogram) trên ảnh preview nhỏ để GUI phản hồi nhanh, nhưng khi lưu vẫn áp dụng lại trên ảnh gốc full-res.

Open issues & Next steps:
- Bổ sung hướng dẫn sử dụng cụ thể (mặc định slider/đơn vị) vào README hoặc tooltip GUI, nhất là ý nghĩa radio cho từng phép.
- Viết test unit đơn giản cho controller (`apply_operation`, `save_current`) bằng ảnh giả để bắt lỗi IO.
- Nghiên cứu thêm lịch sử phép biến đổi (stack nhiều bước) nếu yêu cầu bài tập muốn so sánh chuỗi thao tác.

Paths/Artifacts:
- `gui/app.py`: điểm vào GUI, hiện tải ảnh mặc định qua controller.
- `gui/views.py`: khung preview + control panel scrollable (radio chọn phép, slider tham số, 1 nút áp dụng chung, đánh dấu phép nặng dùng preview nhỏ).
- `gui/controller.py`: quản lý trạng thái ảnh gốc/preview, áp dụng phép biến đổi, lưu ảnh full-res.
- `IO/image_io.py`: hàm `read_image` giữ nguyên kiểm soát kích thước.

Latest checks:
- `python3 -m py_compile gui/app.py gui/views.py gui/controller.py ops/point_ops.py ops/spatial_filters.py ops/histogram_ops.py` (pass)

Schemas/Contracts:
- Không có schema hay contract chính thức trong scope hiện tại.

Environment:
- Python 3.12 (system interpreter) trên WSL2.
