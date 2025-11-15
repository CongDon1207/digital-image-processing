import tkinter as tk
from pathlib import Path

from gui.controller import Controller
from gui.views import MainView


def run_gui() -> None:
    root = tk.Tk()
    root.title("Xu ly anh so")
    root.geometry("1000x500")
    root.resizable(True, True)

    controller = Controller()
    main_view = MainView(root, controller)
    controller.set_view(main_view)

    sample_path = Path("images") / "1.jpg"
    if sample_path.is_file():
        controller.load_image(sample_path)
    else:
        print(f"[WARN] Không tìm thấy ảnh test ở: {sample_path}")

    main_view.pack(fill="both", expand=True)
    root.mainloop()
