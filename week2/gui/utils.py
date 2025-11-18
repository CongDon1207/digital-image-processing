import cv2
import numpy as np
from PIL import Image, ImageTk

def numpy_to_tk(image: np.ndarray, max_size=(400, 400)) -> ImageTk.PhotoImage:
    if image.ndim == 2:
        array = image
        mode = "L"
    else:
        if image.shape[2] == 3:
            array = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mode = "RGB"
        elif image.shape[2] == 4: 
            array = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
            mode = "RGBA"
        else: 
            raise ValueError("Khong co kieu du lieu nao khop")
    
    pil = Image.fromarray(array.astype(np.uint8), mode)
    if max_size is not None:
        pil.thumbnail(max_size, Image.LANCZOS)
    return ImageTk.PhotoImage(pil)
