import tkinter as tk
from ops import sharpened_filter
from .base import BaseSection

class SharpenSection(BaseSection):
    def __init__(self, parent, controller, selected_operation_var):
        super().__init__(parent, controller, selected_operation_var)
        self.vars = {
            "sharp_alpha": tk.DoubleVar(value=1.0),
            "sharp_ksize": tk.IntVar(value=5),
            "sharp_sigma": tk.DoubleVar(value=1.0),
            "sharp_amount": tk.DoubleVar(value=1.0),
            "sharp_k": tk.DoubleVar(value=1.5),
        }

    def build(self):
        self._build_sharpen_section()

    def get_handlers(self):
        return {
            "sharp_lap": self._run_laplacian_sharpen,
            "sharp_unsharp": self._run_unsharp_mask,
            "sharp_highboost": self._run_high_boost,
            "sharp_sobel": self._run_sobel_sharpen,
        }

    def _build_sharpen_section(self):
        frame = self._build_section("Làm sắc nét (spatial)")
        self._add_selector(frame, "sharp_lap", selector_text="Laplacian sharpen")
        self._add_selector(frame, "sharp_unsharp", selector_text="Unsharp mask")
        self._add_selector(frame, "sharp_highboost", selector_text="High-boost filter")
        self._add_selector(frame, "sharp_sobel", selector_text="Sobel sharpen")

        self._add_scale(
            frame,
            "Alpha / Amount",
            self.vars["sharp_alpha"],
            from_=0.1,
            to=3.0,
            resolution=0.1,
            format_str="%.1f",
        )
        self._add_scale(
            frame,
            "Kích thước kernel",
            self.vars["sharp_ksize"],
            from_=3,
            to=15,
            resolution=1,
            format_str="%d",
        )
        self._add_scale(
            frame,
            "Sigma (Gauss)",
            self.vars["sharp_sigma"],
            from_=0.1,
            to=5.0,
            resolution=0.1,
            format_str="%.1f",
        )
        self._add_scale(
            frame,
            "Amount (unsharp)",
            self.vars["sharp_amount"],
            from_=0.5,
            to=3.0,
            resolution=0.1,
            format_str="%.1f",
        )
        self._add_scale(
            frame,
            "Hệ số k (high-boost)",
            self.vars["sharp_k"],
            from_=1.0,
            to=3.0,
            resolution=0.1,
            format_str="%.1f",
        )

    def _run_laplacian_sharpen(self):
        alpha = float(self.vars["sharp_alpha"].get())
        self.controller.apply_operation(
            lambda img: sharpened_filter.laplacian_sharpen(img, eight_conn=False, alpha=alpha),
            description="Laplacian sharpen",
            use_preview=True,
        )

    def _run_unsharp_mask(self):
        ksize = self._ensure_odd(int(self.vars["sharp_ksize"].get()))
        sigma = float(self.vars["sharp_sigma"].get())
        sigma = None if sigma <= 0 else sigma
        amount = float(self.vars["sharp_amount"].get())
        self.controller.apply_operation(
            lambda img: sharpened_filter.unsharp_mask(img, ksize=ksize, sigma=sigma, amount=amount),
            description="Unsharp mask",
            use_preview=True,
        )

    def _run_high_boost(self):
        ksize = self._ensure_odd(int(self.vars["sharp_ksize"].get()))
        sigma = float(self.vars["sharp_sigma"].get())
        sigma = None if sigma <= 0 else sigma
        k = float(self.vars["sharp_k"].get())
        self.controller.apply_operation(
            lambda img: sharpened_filter.high_boost_sharpen(img, ksize=ksize, sigma=sigma, k=k),
            description="High-boost sharpen",
            use_preview=True,
        )

    def _run_sobel_sharpen(self):
        alpha = float(self.vars["sharp_alpha"].get())
        self.controller.apply_operation(
            lambda img: sharpened_filter.sobel_sharpen(img, alpha=alpha),
            description="Sobel sharpen",
            use_preview=True,
        )
