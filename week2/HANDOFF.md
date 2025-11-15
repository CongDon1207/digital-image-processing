# HANDOFF

Current status:
- Giao diện GUI đã gắn controller để cập nhật ảnh preview và nạp ảnh mặc định qua cùng một đầu mối.
- ControlPanel dùng nút chọn file để gọi `Controller.load_image`, tránh lỗi khởi tạo `ttk.Frame` sai `super()`.

Open issues & Next steps:
- Hoàn thiện các control cho điểm ảnh (nút chọn phép biến đổi, cập nhật preview).
- Viết test nhỏ cho controller để đảm bảo `load_image` không bỏ qua ảnh rỗng.
- Cân nhắc bổ sung hướng dẫn sử dụng GUI trong README hoặc tài liệu riêng.

Paths/Artifacts:
- `gui/app.py`: điểm vào GUI, hiện tải ảnh mặc định qua controller.
- `gui/views.py`: khung preview + control, điều khiển chọn file ảnh.
- `gui/controller.py`: quản lý trạng thái ảnh gốc/hiện tại và cập nhật preview.
- `IO/image_io.py`: hàm `read_image` giữ nguyên kiểm soát kích thước.

Latest checks:
- `python3 -m py_compile gui/app.py gui/views.py gui/controller.py` (pass)

Schemas/Contracts:
- Không có schema hay contract chính thức trong scope hiện tại.

Environment:
- Python 3.12 (system interpreter) trên WSL2.
