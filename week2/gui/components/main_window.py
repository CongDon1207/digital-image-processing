import tkinter as tk
from tkinter import ttk
from gui.components.preview_panel import PreviewPanel
from gui.components.control_panel import ControlPanel

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
