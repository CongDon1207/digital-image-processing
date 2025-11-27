import cv2
import numpy as np
import matplotlib.pyplot as plt 
from pathlib import Path


def show_three_images(img1, title1, img2, title2, img3, title3):
    plt.figure(figsize=(14,5))

    images = [img1, img2, img3]
    titles = [title1, title2, title3]

    for i in range(3):
        plt.subplot(1, 3, i+1)
        plt.title(titles[i])
        plt.imshow(images[i], cmap='gray')
        plt.axis('off')

    plt.tight_layout()
    plt.show()


def show_four_images(img1, title1, img2, title2, img3, title3, img4, title4):
    plt.figure(figsize=(10, 10))

    images = [img1, img2, img3, img4]
    titles = [title1, title2, title3, title4]

    for i in range(4):
        plt.subplot(2, 2, i+1)
        plt.title(titles[i])
        plt.imshow(images[i], cmap='gray')
        plt.axis('off')
    plt.tight_layout()
    plt.show()




