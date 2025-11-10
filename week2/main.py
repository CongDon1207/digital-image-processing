import numpy as np
from pathlib import Path
import cv2
from io_utils import read_image
from tranform_ops import negative_image, log_transform
from display import show_window

path = 'images/1.jpg'
img = log_transform(path)
show_window("negative_image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

