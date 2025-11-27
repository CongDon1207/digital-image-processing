import tkinter as tk
import numpy as np
from ops import spatial_filters
from .base import BaseSection

class SpatialSection(BaseSection):
    def __init__(self, parent, controller, selected_operation_var):
        super().__init__(parent, controller, selected_operation_var)
        self.vars = {
            "avg_size": tk.IntVar(value=3),
            "gauss_size": tk.IntVar(value=5),
            "gauss_sigma": tk.DoubleVar(value=1.0),
            "median_size": tk.IntVar(value=3),
        }

    def build(self):
        self._build_average_section()
        self._build_gauss_section()
        self._build_median_section()

    def get_handlers(self):
        return {
            "average": self._run_average,
            "gauss": self._run_gauss,
            "median": self._run_median,
        }

    def _build_average_section(self):
        frame = self._build_section("Làm trơn ảnh (lọc trung bình)", op_key="average")
        self._add_scale(
            frame,
            "Kích thước lọc",
            self.vars["avg_size"],
            from_=3,
            to=15,
            resolution=1,
            format_str="%d",
        )

    def _build_gauss_section(self):
        frame = self._build_section("Làm trơn ảnh (lọc Gauss)", op_key="gauss")
        self._add_scale(
            frame,
            "Kích thước lọc",
            self.vars["gauss_size"],
            from_=3,
            to=15,
            resolution=1,
            format_str="%d",
        )
        self._add_scale(
            frame,
            "Hệ số Sigma",
            self.vars["gauss_sigma"],
            from_=0.1,
            to=5.0,
            resolution=0.1,
            format_str="%.1f",
        )

    def _build_median_section(self):
        frame = self._build_section("Làm trơn ảnh (lọc trung vị)", op_key="median")
        self._add_scale(
            frame,
            "Kích thước lọc",
            self.vars["median_size"],
            from_=3,
            to=15,
            resolution=1,
            format_str="%d",
        )

    def _run_average(self):
        size = self._ensure_odd(int(self.vars["avg_size"].get()))
        kernel = np.ones((size, size), dtype=np.float32)
        self.controller.apply_operation(
            lambda img: spatial_filters.box_filter(img, kernel),
            description="Lọc trung bình",
            use_preview=True,
        )

    def _run_gauss(self):
        size = self._ensure_odd(int(self.vars["gauss_size"].get()))
        sigma = float(self.vars["gauss_sigma"].get())
        sigma = None if sigma <= 0 else sigma
        self.controller.apply_operation(
            lambda img: spatial_filters.gauss_filter(img, ksize=size, sigma=sigma),
            description="Lọc Gauss",
            use_preview=True,
        )

    def _run_median(self):
        size = self._ensure_odd(int(self.vars["median_size"].get()))
        self.controller.apply_operation(
            lambda img: spatial_filters.median_filter(img, size),
            description="Lọc trung vị",
            use_preview=True,
        )
