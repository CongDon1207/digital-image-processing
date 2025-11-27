import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('./images/thresholding1.png', 0)
img = cv.medianBlur(img, 5)

ret, th1 = cv.threshold(
    img, 120, 255,
    cv.THRESH_BINARY + cv.THRESH_OTSU
)

th2 = cv.adaptiveThreshold(
    img, 255,
    cv.ADAPTIVE_THRESH_MEAN_C,
    cv.THRESH_BINARY,
    7, 2
)

titles = [
    'Original',
    'OTSU Threshold',
    'Local Threshold'
]

images = [img, th1, th2]

for i in range(3):
    plt.subplot(1, 3, i + 1)
    plt.imshow(images[i], cmap=plt.cm.gray)
    plt.title(titles[i])
    plt.xticks([])
    plt.yticks([])

plt.show()
