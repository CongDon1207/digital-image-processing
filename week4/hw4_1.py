import cv2
import numpy as np
import matplotlib.pyplot as plt


def create_input_image():
    scale = 5
    img = np.ones((100 * scale, 200 * scale), dtype=np.uint8) * 255
    
    cv2.rectangle(img, (30 * scale, 20 * scale), (60 * scale, 80 * scale), 0, -1)
    cv2.rectangle(img, (30 * scale, 50 * scale), (90 * scale, 80 * scale), 0, -1)
    
    center = (150 * scale, 50 * scale)
    radius = 30 * scale
    cv2.ellipse(img, center, (radius, radius), 0, 0, 270, 0, -1, cv2.LINE_AA)
    
    cv2.imwrite('hw4_1_input.png', img)
    print(">> Đã lưu ảnh: 'hw4_input.png'")
    return img


def create_diagonal_kernel():
    kernel = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ], dtype=np.uint8)
    print("\n>> Kernel (3x3):\n", kernel)
    return kernel


def apply_morphology(img, kernel):
    img_inv = cv2.bitwise_not(img)
    
    iterations = 5  # Vì ảnh phóng to gấp 5 lần, ta lặp 5 lần với kernel 3x3 để có hiệu ứng tương đương
    erosion_inv = cv2.erode(img_inv, kernel, iterations=iterations)
    dilation_inv = cv2.dilate(img_inv, kernel, iterations=iterations)
    
    result_erosion = cv2.bitwise_not(erosion_inv)
    result_dilation = cv2.bitwise_not(dilation_inv)
    
    print(f">> Hoàn thành Erosion và Dilation (iterations={iterations}).")
    return result_erosion, result_dilation


def display_results(img, result_erosion, result_dilation):
    titles = ["Anh Goc (Original)", "Ket qua Erosion (Co)", "Ket qua Dilation (Gian)"]
    images = [img, result_erosion, result_dilation]
    
    plt.figure(figsize=(15, 6))
    for i, (image, title) in enumerate(zip(images, titles), 1):
        plt.subplot(1, 3, i)
        plt.imshow(image, cmap='gray', vmin=0, vmax=255)
        plt.title(title)
        plt.axis('off')
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    img = create_input_image()
    kernel = create_diagonal_kernel()
    result_erosion, result_dilation = apply_morphology(img, kernel)
    display_results(img, result_erosion, result_dilation)