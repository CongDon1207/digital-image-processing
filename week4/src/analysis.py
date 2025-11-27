import cv2
import numpy as np

class Analysis:
    def __init__(self):
        self.kernel = np.ones((3, 3), np.uint8)

    def manual_connected_components(self, binary_img):
        A = binary_img.copy()
        h, w = A.shape
        stats = []
        num_labels = 0
        labeled_img = np.zeros_like(A)

        while True:
            pixels = np.argwhere(A > 0)
            if len(pixels) == 0:
                break
            
            seed_y, seed_x = pixels[0]
            X = np.zeros_like(A)
            X[seed_y, seed_x] = 255

            while True:
                X_prev = X.copy()
                dilation = cv2.dilate(X, self.kernel, iterations=1)
                X = cv2.bitwise_and(dilation, A)
                if np.array_equal(X, X_prev):
                    break
            
            num_labels += 1
            area = np.sum(X > 0)
            stats.append(area)
            labeled_img[X > 0] = num_labels
            A = cv2.bitwise_xor(A, X)

        return num_labels, stats, labeled_img

    def opencv_connected_components(self, binary_img):
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_img, connectivity=8)
        areas = stats[1:, cv2.CC_STAT_AREA]
        return num_labels - 1, areas, labels
