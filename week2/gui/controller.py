from IO.image_io import read_image
from gui.image_adapter import numpy_to_tk
from pathlib import Path


class Controller:
    def __init__(self):
        self.view = None
        self.original_image = None
        self.current_image = None

    def set_view(self, view):
        self.view = view

    def load_image(self, path: str | Path) -> None:
        img = read_image(Path(path))
        if img is None:
            return

        self.original_image = img
        self.current_image = img
        self.update_preview()

    def update_preview(self) -> None:
        if self.view is None:
            return
        if self.original_image is None or self.current_image is None:
            return
        
        orig_photo = numpy_to_tk(self.original_image)
        res_photo = numpy_to_tk(self.current_image)

        self.view.preview_panel.update_original(orig_photo)
        self.view.preview_panel.update_result(res_photo)
