import tkinter as tk
from tkinter import ttk, messagebox
from ops import point_ops
from .base import BaseSection

class PointSection(BaseSection):
    def __init__(self, parent, controller, selected_operation_var):
        super().__init__(parent, controller, selected_operation_var)
        self.vars = {
            "log_c": tk.DoubleVar(value=1.0),
            "log_auto": tk.BooleanVar(value=True),
            "pw_r1": tk.IntVar(value=40),
            "pw_s1": tk.IntVar(value=20),
            "pw_r2": tk.IntVar(value=200),
            "pw_s2": tk.IntVar(value=230),
            "gamma_c": tk.DoubleVar(value=1.0),
            "gamma": tk.DoubleVar(value=1.2),
        }
        self._log_scale_widgets = None

    def build(self):
        self._build_negative_section()
        self._build_log_section()
        self._build_piecewise_section()
        self._build_gamma_section()

    def get_handlers(self):
        return {
            "negative": self._run_negative,
            "log": self._run_log,
            "piecewise": self._run_piecewise,
            "gamma": self._run_gamma,
        }

    def _build_negative_section(self):
        frame = self._build_section("Negative image", op_key="negative")
        ttk.Label(frame, text="Tạo ảnh âm bản của ảnh gốc.").pack(anchor='w')

    def _build_log_section(self):
        frame = self._build_section("Biến đổi Log", op_key="log")
        scale, spin = self._add_scale(
            frame,
            "Hệ số C",
            self.vars["log_c"],
            from_=0.1,
            to=80.0,
            resolution=0.1,
            format_str="%.1f",
        )
        self._log_scale_widgets = (scale, spin)
        ttk.Checkbutton(
            frame,
            text="Sử dụng hệ số tự động",
            variable=self.vars["log_auto"],
            command=self._update_log_controls_state,
        ).pack(anchor='w', pady=(4, 0))
        self._update_log_controls_state()

    def _build_piecewise_section(self):
        frame = self._build_section("Biến đổi Piecewise-Linear", op_key="piecewise")
        self._add_scale(
            frame,
            "Hệ số Thấp - r1",
            self.vars["pw_r1"],
            from_=0,
            to=200,
            resolution=1,
            format_str="%d",
        )
        self._add_scale(
            frame,
            "Hệ số Thấp - s1",
            self.vars["pw_s1"],
            from_=0,
            to=200,
            resolution=1,
            format_str="%d",
        )
        self._add_scale(
            frame,
            "Hệ số Cao - r2",
            self.vars["pw_r2"],
            from_=55,
            to=255,
            resolution=1,
            format_str="%d",
        )
        self._add_scale(
            frame,
            "Hệ số Cao - s2",
            self.vars["pw_s2"],
            from_=55,
            to=255,
            resolution=1,
            format_str="%d",
        )

    def _build_gamma_section(self):
        frame = self._build_section("Biến đổi Gamma", op_key="gamma")
        self._add_scale(
            frame,
            "Hệ số C",
            self.vars["gamma_c"],
            from_=0.1,
            to=5.0,
            resolution=0.1,
            format_str="%.1f",
        )
        self._add_scale(
            frame,
            "Gamma",
            self.vars["gamma"],
            from_=0.1,
            to=5.0,
            resolution=0.1,
            format_str="%.1f",
        )

    def _update_log_controls_state(self):
        if not self._log_scale_widgets:
            return
        state = 'disabled' if self.vars["log_auto"].get() else 'normal'
        for widget in self._log_scale_widgets:
            widget.configure(state=state)

    def _run_negative(self):
        self.controller.apply_operation(point_ops.negative_image, description="Âm bản")

    def _run_log(self):
        if self.vars["log_auto"].get():
            c = None
        else:
            c = max(0.1, float(self.vars["log_c"].get()))
        self.controller.apply_operation(
            lambda img: point_ops.log_transform(img, c=c),
            description="Biến đổi Log",
        )

    def _run_piecewise(self):
        r1 = int(self.vars["pw_r1"].get())
        s1 = int(self.vars["pw_s1"].get())
        r2 = int(self.vars["pw_r2"].get())
        s2 = int(self.vars["pw_s2"].get())

        if not (0 <= r1 <= r2 <= 255 and 0 <= s1 <= s2 <= 255):
            messagebox.showerror("Piecewise-Linear", "Cần đảm bảo 0 ≤ r1 ≤ r2 ≤ 255 và 0 ≤ s1 ≤ s2 ≤ 255.")
            return

        self.controller.apply_operation(
            lambda img: point_ops.piecewise_linear(img, r1, s1, r2, s2),
            description="Piecewise-Linear",
        )

    def _run_gamma(self):
        c = max(0.1, float(self.vars["gamma_c"].get()))
        gamma = max(0.1, float(self.vars["gamma"].get()))
        self.controller.apply_operation(
            lambda img: point_ops.gamma_transform(img, c=c, gamma=gamma),
            description="Biến đổi Gamma",
        )
