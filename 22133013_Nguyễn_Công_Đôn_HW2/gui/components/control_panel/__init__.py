import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .point import PointSection
from .spatial import SpatialSection
from .histogram import HistogramSection
from .frequency import FrequencySection
from .sharpen import SharpenSection

from gui.theme import COLOR_BG

class ControlPanel(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, padding=8)
        self.controller = controller
        self.selected_operation = tk.StringVar(value="negative")
        self.operation_handlers = {}
        self.vars = {} # Aggregate vars for backward compatibility if needed, or just for access

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        scroll_container = ttk.Frame(self)
        scroll_container.grid(row=0, column=0, sticky='nsew')
        self._build_scroll_area(scroll_container)
        
        self.sections = [
            PointSection(self._scrollable, controller, self.selected_operation),
            SpatialSection(self._scrollable, controller, self.selected_operation),
            HistogramSection(self._scrollable, controller, self.selected_operation),
            FrequencySection(self._scrollable, controller, self.selected_operation),
            SharpenSection(self._scrollable, controller, self.selected_operation),
        ]

        self._build_sections()
        self._build_footer()

    def _build_scroll_area(self, container):
        canvas = tk.Canvas(container, borderwidth=0, highlightthickness=0, bg=COLOR_BG)
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
            style="Title.TLabel"
        ).pack(anchor='w', pady=(0, 8))

        for section in self.sections:
            section.build()
            self.operation_handlers.update(section.get_handlers())
            self.vars.update(section.vars)

    def _build_footer(self):
        footer = ttk.Frame(self)
        footer.grid(row=1, column=0, sticky='ew', pady=(8, 0))
        footer.columnconfigure((0, 1, 2, 3, 4), weight=1)

        ttk.Button(footer, text="Chọn ảnh", command=self.on_select_image, style="Secondary.TButton").grid(row=0, column=0, sticky='ew', padx=2)
        ttk.Button(footer, text="Khôi phục", command=self.controller.restore_original, style="Secondary.TButton").grid(row=0, column=1, sticky='ew', padx=2)
        ttk.Button(footer, text="Áp dụng", command=self.apply_selected).grid(row=0, column=2, sticky='ew', padx=2)
        ttk.Button(footer, text="Lưu ra file", command=self.on_save_image).grid(row=0, column=3, sticky='ew', padx=2)
        ttk.Button(footer, text="Close", command=self.close_app, style="Secondary.TButton").grid(row=0, column=4, sticky='ew', padx=2)

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

    @staticmethod
    def _is_descendant(widget, ancestor) -> bool:
        while widget is not None:
            if widget == ancestor:
                return True
            widget = getattr(widget, 'master', None)
        return False

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
