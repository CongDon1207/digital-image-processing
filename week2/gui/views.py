import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import numpy as np

from ops import histogram_ops, point_ops, spatial_filters

class PreviewPanel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)

        ttk.Label(self, text = "Ảnh gốc").pack(anchor='w')
        self.original_label = ttk.Label(self)
        self.original_label.pack(fill='both', expand=True, pady=(0,8))

        ttk.Label(self, text="Ảnh kết quả").pack(anchor='w')
        self.result_label = ttk.Label(self)
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

class ControlPanel(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, padding=8)
        self.controller = controller
        self.vars = self._init_vars()
        self.selected_operation = tk.StringVar(value="negative")
        self.operation_handlers = {
            "negative": self._run_negative,
            "log": self._run_log,
            "piecewise": self._run_piecewise,
            "gamma": self._run_gamma,
            "average": self._run_average,
            "gauss": self._run_gauss,
            "median": self._run_median,
            "hist_eq": self._run_hist_equal,
            "hist_local": self._run_hist_local,
        }

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        scroll_container = ttk.Frame(self)
        scroll_container.grid(row=0, column=0, sticky='nsew')
        self._build_scroll_area(scroll_container)
        self._build_sections()
        self._build_footer()

    def _init_vars(self):
        return {
            "log_c": tk.DoubleVar(value=1.0),
            "log_auto": tk.BooleanVar(value=True),
            "pw_r1": tk.IntVar(value=40),
            "pw_s1": tk.IntVar(value=20),
            "pw_r2": tk.IntVar(value=200),
            "pw_s2": tk.IntVar(value=230),
            "gamma_c": tk.DoubleVar(value=1.0),
            "gamma": tk.DoubleVar(value=1.2),
            "avg_size": tk.IntVar(value=3),
            "gauss_size": tk.IntVar(value=5),
            "gauss_sigma": tk.DoubleVar(value=1.0),
            "median_size": tk.IntVar(value=3),
            "hist_local_size": tk.IntVar(value=9),
        }

    def _build_scroll_area(self, container):
        canvas = tk.Canvas(container, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self._scroll_canvas = canvas
        self._scrollable = ttk.Frame(canvas)
        self._canvas_window = canvas.create_window((0, 0), window=self._scrollable, anchor='nw')

        self._scrollable.bind(
            '<Configure>',
            lambda _: canvas.configure(scrollregion=canvas.bbox('all')),
        )
        canvas.bind(
            '<Configure>',
            lambda e: canvas.itemconfigure(self._canvas_window, width=e.width),
        )

        for widget in (self._scrollable, canvas):
            widget.bind('<MouseWheel>', self._on_mousewheel)
            widget.bind('<Button-4>', self._on_mousewheel_linux_up)
            widget.bind('<Button-5>', self._on_mousewheel_linux_down)

        self.bind_all('<MouseWheel>', self._on_mousewheel)
        self.bind_all('<Button-4>', self._on_mousewheel_linux_up)
        self.bind_all('<Button-5>', self._on_mousewheel_linux_down)

    def _build_sections(self):
        ttk.Label(
            self._scrollable,
            text="Công cụ biến đổi",
            font=("Helvetica", 12, "bold"),
        ).pack(anchor='w', pady=(0, 8))

        self._build_negative_section()
        self._build_log_section()
        self._build_piecewise_section()
        self._build_gamma_section()
        self._build_average_section()
        self._build_gauss_section()
        self._build_median_section()
        self._build_hist_section()

    def _build_section(self, title, *, op_key: str | None = None, selector_text: str | None = None):
        frame = ttk.LabelFrame(self._scrollable, text=title, padding=6)
        frame.pack(fill='x', pady=4)
        if op_key:
            self._add_selector(frame, op_key, selector_text)
        return frame

    def _add_selector(self, frame, op_key: str, selector_text: str | None = None):
        text = selector_text or "Chọn phép này"
        ttk.Radiobutton(
            frame,
            text=text,
            variable=self.selected_operation,
            value=op_key,
        ).pack(anchor='e', pady=(0, 4))

    def _add_scale(
        self,
        parent,
        label,
        var,
        *,
        from_,
        to,
        resolution=1.0,
        format_str: str | None = None,
    ):
        row = ttk.Frame(parent)
        row.pack(fill='x', pady=2)
        ttk.Label(row, text=label).pack(anchor='w')
        scale = ttk.Scale(row, variable=var, from_=from_, to=to, orient='horizontal')
        scale.pack(fill='x')

        spin = ttk.Spinbox(
            row,
            textvariable=var,
            from_=from_,
            to=to,
            increment=resolution,
            width=6,
            format=format_str,
        )
        spin.pack(anchor='e', pady=2)
        return scale, spin

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

    def _build_footer(self):
        footer = ttk.Frame(self)
        footer.grid(row=1, column=0, sticky='ew', pady=(8, 0))
        footer.columnconfigure((0, 1, 2, 3, 4), weight=1)

        ttk.Button(footer, text="Chọn ảnh", command=self.on_select_image).grid(row=0, column=0, sticky='ew', padx=2)
        ttk.Button(footer, text="Khôi phục", command=self.controller.restore_original).grid(row=0, column=1, sticky='ew', padx=2)
        ttk.Button(footer, text="Áp dụng", command=self.apply_selected).grid(row=0, column=2, sticky='ew', padx=2)
        ttk.Button(footer, text="Lưu ra file", command=self.on_save_image).grid(row=0, column=3, sticky='ew', padx=2)
        ttk.Button(footer, text="Close", command=self.close_app).grid(row=0, column=4, sticky='ew', padx=2)

    def _on_mousewheel(self, event):
        if not self._pointer_inside(event):
            return
        if event.delta:
            self._scroll_canvas.yview_scroll(int(-event.delta / 120), 'units')
            return 'break'

    def _on_mousewheel_linux_up(self, event):
        if not self._pointer_inside(event):
            return
        self._scroll_canvas.yview_scroll(-1, 'units')
        return 'break'

    def _on_mousewheel_linux_down(self, event):
        if not self._pointer_inside(event):
            return
        self._scroll_canvas.yview_scroll(1, 'units')
        return 'break'

    def _pointer_inside(self, event) -> bool:
        widget = self.winfo_containing(event.x_root, event.y_root)
        return self._is_descendant(widget, self)

    def on_select_image(self):
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff"),
            ("All files", "*.*"),
        ]

        path = filedialog.askopenfilename(title="Chọn ảnh", filetypes=filetypes)
        if path:
            self.controller.load_image(path)

    def on_save_image(self):
        if not self.controller.has_image():
            messagebox.showwarning("Chưa có ảnh", "Chưa có ảnh kết quả để lưu.")
            return

        path = filedialog.asksaveasfilename(
            title="Lưu ảnh",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg"), ("Bitmap", "*.bmp"), ("All files", "*.*")],
        )
        if not path:
            return

        if self.controller.save_current(path):
            messagebox.showinfo("Lưu ảnh", "Đã lưu ảnh kết quả thành công.")

    def close_app(self):
        root = self.winfo_toplevel()
        root.destroy()

    def apply_selected(self):
        op_key = self.selected_operation.get()
        handler = self.operation_handlers.get(op_key)
        if handler is None:
            messagebox.showwarning("Chưa chọn phép", "Vui lòng chọn một phép biến đổi trong panel.")
            return
        handler()

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

    @staticmethod
    def _ensure_odd(size: int) -> int:
        size = max(1, size)
        if size % 2 == 0:
            size += 1
        return size

    def _update_log_controls_state(self):
        widgets = getattr(self, "_log_scale_widgets", None)
        if not widgets:
            return
        state = 'disabled' if self.vars["log_auto"].get() else 'normal'
        for widget in widgets:
            widget.configure(state=state)

    @staticmethod
    def _is_descendant(widget, ancestor) -> bool:
        while widget is not None:
            if widget == ancestor:
                return True
            widget = getattr(widget, 'master', None)
        return False



class MainView(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, padding=8)
        paned = ttk.PanedWindow(self, orient='horizontal')
        self.preview_panel = PreviewPanel(paned)
        self.control_panel = ControlPanel(paned, controller)

        
        paned.add(self.preview_panel, weight=3)
        paned.add(self.control_panel, weight=2)
        paned.pack(fill='both', expand=True)

        # Khi panel thay đổi kích thước cần cập nhật lại preview cho đúng tỉ lệ
        self.preview_panel.bind("<Configure>", lambda _event: controller.update_preview())

