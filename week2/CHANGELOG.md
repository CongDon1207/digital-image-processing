2025-11-15: Fix ControlPanel initialization and Controller image loading at gui/ - khắc phục TypeError và đồng nhất cách nạp ảnh sample; PR #0 (completed).
2025-11-15: Add đầy đủ control panel gọi ops (negative/log/gamma/lọc/hist) tại gui/views.py + controller API apply/save - người dùng thao tác ảnh trực quan; PR #0 (completed).
2025-11-15: Improve GUI trải nghiệm (panel scroll, radio chọn + 1 nút Áp dụng, preview scale tỉ lệ, Tk zoomed) ở gui/* - dễ dùng khi màn hình nhỏ; PR #0 (completed).
2025-11-15: Optimize preview path (áp dụng lọc/LocalHist trên ảnh thu nhỏ nhưng khi lưu vẫn xử lý ảnh gốc full-res, không sửa thuật toán vòng for trong ops) tại gui/controller.py + gui/views.py - tăng tốc tương tác; PR #0 (completed).
2025-11-15: Fix log transform tối đen bằng cách bổ sung chế độ "Hệ số C tự động" trong control panel và giữ tùy chỉnh thủ công khi cần; PR #0 (completed).
2025-11-15: Allow ControlPanel cuộn bằng bánh xe chuột (bind mousewheel toàn khung, không cần rê lên thanh scrollbar) để thao tác nhanh hơn; PR #0 (completed).
