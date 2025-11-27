import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('./images/thresholding1.png', 0)
img = cv.medianBlur(img, 5)

ret, th1 = cv.threshold(img, 132, 255, cv.THRESH_BINARY)

th2 = cv.adaptiveThreshold(
    img, 255,
    cv.ADAPTIVE_THRESH_MEAN_C,
    cv.THRESH_BINARY,
    11, 2
)

th3 = cv.adaptiveThreshold(
    img, 255,
    cv.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv.THRESH_BINARY,
    11, 2
)

titles = [
    'Original Image',
    'Global Thresholding',
    'Local - Mean Thresholding',
    'Local - Gaussian Thresholding'
]

images = [img, th1, th2, th3]

for i in range(4):
    plt.subplot(2, 2, i + 1)
    plt.imshow(images[i], cmap=plt.cm.gray)
    plt.title(titles[i])
    plt.xticks([])
    plt.yticks([])

plt.show()
