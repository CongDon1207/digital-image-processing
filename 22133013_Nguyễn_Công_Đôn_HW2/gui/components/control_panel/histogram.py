import tkinter as tk
from ops import histogram_ops
from .base import BaseSection

class HistogramSection(BaseSection):
    def __init__(self, parent, controller, selected_operation_var):
        super().__init__(parent, controller, selected_operation_var)
        self.vars = {
            "hist_local_size": tk.IntVar(value=9),
        }

    def build(self):
        self._build_hist_section()

    def get_handlers(self):
        return {
            "hist_eq": self._run_hist_equal,
            "hist_local": self._run_hist_local,
        }

    def _build_hist_section(self):
        frame = self._build_section("Cân bằng sáng dùng Histogram")
        self._add_selector(frame, "hist_eq", selector_text="Chọn cân bằng toàn cục")
        self._add_selector(frame, "hist_local", selector_text="Chọn cân bằng cục bộ")
        self._add_scale(
            frame,
            "Kích thước local",
            self.vars["hist_local_size"],
            from_=3,
            to=31,
            resolution=2,
            format_str="%d",
        )

    def _run_hist_equal(self):
        self.controller.apply_operation(
            histogram_ops.equalize_histogram,
            description="Cân bằng histogram",
        )

    def _run_hist_local(self):
        size = self._ensure_odd(int(self.vars["hist_local_size"].get()))
        self.controller.apply_operation(
            lambda img: histogram_ops.local_hist_equalization(img, win_size=size),
            description="Local histogram equalization",
            use_preview=True,
        )
