import tkinter as tk
from ops import freq_ops
from .base import BaseSection

class FrequencySection(BaseSection):
    def __init__(self, parent, controller, selected_operation_var):
        super().__init__(parent, controller, selected_operation_var)
        self.vars = {
            "freq_D0": tk.DoubleVar(value=40.0),
            "freq_n": tk.IntVar(value=2),
        }

    def build(self):
        self._build_freq_section()

    def get_handlers(self):
        return {
            "freq_ilpf": self._run_freq_ilpf,
            "freq_ihpf": self._run_freq_ihpf,
            "freq_bhlpf": self._run_freq_bhlpf,
            "freq_bhhpf": self._run_freq_bhhpf,
            "freq_ghlpf": self._run_freq_ghlpf,
            "freq_ghhpf": self._run_freq_ghhpf,
        }

    def _build_freq_section(self):
        frame = self._build_section("Lọc trong miền tần số")
        self._add_selector(frame, "freq_ilpf", selector_text="Ideal Low-pass (ILPF)")
        self._add_selector(frame, "freq_ihpf", selector_text="Ideal High-pass (IHPF)")
        self._add_selector(frame, "freq_bhlpf", selector_text="Butterworth Low-pass")
        self._add_selector(frame, "freq_bhhpf", selector_text="Butterworth High-pass")
        self._add_selector(frame, "freq_ghlpf", selector_text="Gaussian Low-pass")
        self._add_selector(frame, "freq_ghhpf", selector_text="Gaussian High-pass")

        self._add_scale(
            frame,
            "D0 (tần số cắt)",
            self.vars["freq_D0"],
            from_=5,
            to=100,
            resolution=1,
            format_str="%.0f",
        )
        self._add_scale(
            frame,
            "Bậc Butterworth n",
            self.vars["freq_n"],
            from_=1,
            to=5,
            resolution=1,
            format_str="%d",
        )

    def _run_freq_ilpf(self):
        D0 = float(self.vars["freq_D0"].get())
        self.controller.apply_operation(
            lambda img: freq_ops.ideal_lowpass(img, D0=D0),
            description="Ideal Low-pass (tần số)",
            use_preview=True,
        )

    def _run_freq_ihpf(self):
        D0 = float(self.vars["freq_D0"].get())
        self.controller.apply_operation(
            lambda img: freq_ops.ideal_highpass(img, D0=D0),
            description="Ideal High-pass (tần số)",
            use_preview=True,
        )

    def _run_freq_bhlpf(self):
        D0 = float(self.vars["freq_D0"].get())
        n = int(self.vars["freq_n"].get())
        self.controller.apply_operation(
            lambda img: freq_ops.butterworth_lowpass(img, D0=D0, n=n),
            description="Butterworth Low-pass (tần số)",
            use_preview=True,
        )

    def _run_freq_bhhpf(self):
        D0 = float(self.vars["freq_D0"].get())
        n = int(self.vars["freq_n"].get())
        self.controller.apply_operation(
            lambda img: freq_ops.butterworth_highpass(img, D0=D0, n=n),
            description="Butterworth High-pass (tần số)",
            use_preview=True,
        )

    def _run_freq_ghlpf(self):
        D0 = float(self.vars["freq_D0"].get())
        self.controller.apply_operation(
            lambda img: freq_ops.gaussian_lowpass(img, D0=D0),
            description="Gaussian Low-pass (tần số)",
            use_preview=True,
        )

    def _run_freq_ghhpf(self):
        D0 = float(self.vars["freq_D0"].get())
        self.controller.apply_operation(
            lambda img: freq_ops.gaussian_highpass(img, D0=D0),
            description="Gaussian High-pass (tần số)",
            use_preview=True,
        )
