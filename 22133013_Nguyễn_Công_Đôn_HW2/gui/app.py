import tkinter as tk
from pathlib import Path

from gui.controller import Controller
from gui.components.main_window import MainView
from gui.theme import setup_theme


def run_gui() -> None:
    root = tk.Tk()
    setup_theme(root)
    root.title("Xu ly anh so")
    root.geometry("1000x500")
    root.resizable(True, True)
    root.minsize(1024, 720)
    try:
        root.state("zoomed")
    except tk.TclError:
        try:
            root.attributes("-zoomed", True)
        except tk.TclError:
            root.geometry("1400x900")

    controller = Controller()
    main_view = MainView(root, controller)
    controller.set_view(main_view)

    sample_path = Path("images") / "default.jpg"
    if sample_path.is_file():
        controller.load_image(sample_path)
    else:
        print(f"[WARN] Không tìm thấy ảnh test ở: {sample_path}")

    main_view.pack(fill="both", expand=True)
    root.mainloop()
