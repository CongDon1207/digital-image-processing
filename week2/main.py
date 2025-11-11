import numpy as np
from pathlib import Path
import cv2
from io_utils import read_image
from tranform_ops import negative_image, log_transform, piecewise_linear
from display import show_window
from filter import conv_avg, max_filter, min_filter, median_filter

path = 'images/1.jpg'
img_raw = read_image(path)
show_window("raw", img_raw)

# img = median_filter(img_raw, 3)
# show_window("median_filter", img)

# img = min_filter(img_raw, 3)
# show_window("median_filter", img)

img = max_filter(img_raw, 3)
show_window("median_filter", img)

# K = np.array([[1, 1, 1],
#               [1, 1, 1],
#               [1, 1, 1]], dtype=float)
# img = conv_avg(img_raw, K)
# show_window("conv_avg", img)


cv2.waitKey(0)
cv2.destroyAllWindows()






