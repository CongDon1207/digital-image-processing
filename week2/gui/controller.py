from IO.image_io import read_image, fit_resize, save_image
from gui.utils import numpy_to_tk
from pathlib import Path
from tkinter import messagebox
from typing import Callable

import cv2
import numpy as np


class Controller:
    def __init__(self):
        self.view = None
        self.original_image: np.ndarray | None = None
        self.current_image: np.ndarray | None = None
        self.original_path: Path | None = None
        self.preview_base: np.ndarray | None = None
        self.last_operation_func: Callable[[np.ndarray], np.ndarray] | None = None
        self.last_operation_description: str | None = None
        self.last_operation_use_preview: bool = False

    def set_view(self, view):
        self.view = view

    def load_image(self, path: str | Path) -> None:
        img = read_image(Path(path))
        if img is None:
            messagebox.showerror("Lỗi đọc ảnh", "Không thể mở tệp đã chọn.")
            return

        self.original_path = Path(path)
        self.original_image = img.copy()
        self.current_image = img.copy()
        # Ảnh preview nhỏ hơn dùng cho các phép nặng (lọc, local histogram)
        self.preview_base = fit_resize(img, max_w=600, max_h=450)

        self.last_operation_func = None
        self.last_operation_description = None
        self.last_operation_use_preview = False
        self.update_preview()

    def has_image(self) -> bool:
        return self.original_image is not None

    def restore_original(self) -> None:
        if not self.has_image():
            return
        self.current_image = self.original_image.copy()
        self.last_operation_func = None
        self.last_operation_description = None
        self.last_operation_use_preview = False
        self.update_preview()

    def apply_operation(
        self,
        func: Callable[[np.ndarray], np.ndarray],
        *,
        description: str | None = None,
        use_preview: bool = False,
    ) -> None:
        if not self.has_image():
            messagebox.showwarning("Chưa có ảnh", "Vui lòng chọn ảnh đầu vào trước.")
            return

        self.last_operation_func = func
        self.last_operation_description = description
        self.last_operation_use_preview = use_preview

        base_img: np.ndarray | None
        if use_preview and self.preview_base is not None:
            base_img = self.preview_base
        else:
            base_img = self.original_image

        if base_img is None:
            messagebox.showerror("Phép biến đổi", "Không có ảnh nguồn để áp dụng phép biến đổi.")
            return

        try:
            source = base_img.copy()
            result = func(source)
        except Exception as exc:  # pragma: no cover - GUI cảnh báo
            title = description or "Phép biến đổi"
            messagebox.showerror(title, f"{title} thất bại:\n{exc}")
            return

        if result is None:
            messagebox.showerror("Phép biến đổi", "Hàm xử lý không trả về ảnh hợp lệ.")
            return

        self.current_image = result
        self.update_preview()

    def save_current(self, path: str | Path) -> bool:
        if self.current_image is None:
            messagebox.showwarning("Chưa có ảnh", "Không có ảnh kết quả để lưu.")
            return False

        img_to_save: np.ndarray
        if self.last_operation_func is not None and self.last_operation_use_preview:
            if self.original_image is None:
                messagebox.showerror(
                    "Lưu ảnh",
                    "Không tìm thấy ảnh gốc để áp dụng phép biến đổi ở độ phân giải đầy đủ.",
                )
                return False

            try:
                base = self.original_image.copy()
                img_to_save = self.last_operation_func(base)
            except Exception as exc:  # pragma: no cover - GUI cảnh báo
                messagebox.showerror(
                    "Lưu ảnh",
                    f"Lỗi khi áp dụng phép biến đổi trên ảnh gốc:\n{exc}",
                )
                return False
        else:
            img_to_save = self.current_image

        ok = save_image(img_to_save, path)
        if not ok:
            messagebox.showerror("Lưu ảnh", "Không thể ghi tệp đầu ra.")
        return ok

    def update_preview(self) -> None:
        if self.view is None:
            return
        if self.original_image is None or self.current_image is None:
            return

        max_size = self.view.preview_panel.get_image_max_size()
        orig_photo = numpy_to_tk(self.original_image, max_size=max_size)
        res_photo = numpy_to_tk(self.current_image, max_size=max_size)

        self.view.preview_panel.update_original(orig_photo)
        self.view.preview_panel.update_result(res_photo)
