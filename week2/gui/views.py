from tkinter import ttk, filedialog

class PreviewPanel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)

        ttk.Label(self, text = "Ảnh gốc").pack(anchor='w')
        self.original_label = ttk.Label(self)
        self.original_label.pack(fill='both', expand=True, pady=(0,8))

        ttk.Label(self, text="Ảnh kết quả").pack(anchor='w')
        self.result_label = ttk.Label(self)
        self.result_label.pack(fill='both', expand=True)

    def update_original(self, photo_image):
        self.original_label.config(image = photo_image)
        self.original_label.image = photo_image

    def update_result(self, photo_image):
        self.result_label.config(image=photo_image)
        self.result_label.image = photo_image

class ControlPanel(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, padding=8)
        self.controller = controller

        select_btn = ttk.Button(self, text="Chọn ảnh", command=self.on_select_image)
        select_btn.pack(anchor='w')

    def on_select_image(self):
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff"),
            ("All files", "*.*"),
        ]

        path = filedialog.askopenfilename(title="Chọn ảnh", filetypes=filetypes)
        if path:
            self.controller.load_image(path)



class MainView(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, padding=8)
        paned = ttk.PanedWindow(self, orient='horizontal')
        self.preview_panel = PreviewPanel(paned)
        self.control_panel = ControlPanel(paned, controller)

        
        paned.add(self.preview_panel, weight=1)
        paned.add(self.control_panel, weight=1)
        paned.pack(fill='both', expand=True)





