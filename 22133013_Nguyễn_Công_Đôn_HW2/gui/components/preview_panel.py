import tkinter as tk
from tkinter import ttk

class PreviewPanel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)

        ttk.Label(self, text="Ảnh gốc", style="Header.TLabel").pack(anchor='w')
        self.original_label = ttk.Label(self, background="#e0e0e0", anchor="center")
        self.original_label.pack(fill='both', expand=True, pady=(0,8))

        ttk.Label(self, text="Ảnh kết quả", style="Header.TLabel").pack(anchor='w')
        self.result_label = ttk.Label(self, background="#e0e0e0", anchor="center")
        self.result_label.pack(fill='both', expand=True)

        self._default_size = (400, 300)

    def update_original(self, photo_image):
        self.original_label.config(image = photo_image)
        self.original_label.image = photo_image

    def update_result(self, photo_image):
        self.result_label.config(image=photo_image)
        self.result_label.image = photo_image

    def get_image_max_size(self) -> tuple[int, int]:
        """Trả về kích thước hiển thị mong muốn dựa trên panel hiện tại."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1 or height <= 1:
            return self._default_size

        usable_width = max(300, width - 16)
        usable_height = max(200, height - 24)
        per_block = max(150, usable_height // 2)
        return (int(usable_width), int(per_block))
