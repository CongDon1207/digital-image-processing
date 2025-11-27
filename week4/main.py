import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. Đọc ảnh
img_path = 'input/fingerprint.png'  # Đảm bảo tên file đúng với ảnh của bạn
img = cv2.imread(img_path, 0)

if img is None:
    print("Không tìm thấy ảnh!")
else:
    _, img_binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    k_size = 5 
    kernel = np.ones((k_size, k_size), np.uint8)

    # --- GIAI ĐOẠN 1: OPENING (Xóa nhiễu trắng) ---
    img_erosion = cv2.erode(img_binary, kernel, iterations=1)

    img_opening = cv2.dilate(img_erosion, kernel, iterations=1)

    # --- GIAI ĐOẠN 2: CLOSING (Lấp lỗ đen/đứt gãy) ---
    img_dilation_opening = cv2.dilate(img_opening, kernel, iterations=1)

    img_result = cv2.erode(img_dilation_opening, kernel, iterations=1)

    # --- Hiển thị kết quả ---
    titles = [f'(a) Original Noisy (Otsu)', 
              f'(c) Eroded (Kernel {k_size}x{k_size})', 
              '(d) Opening (A o B)', 
              '(e) Dilation of Opening', 
              '(f) Final Result (Closing)']
    
    images = [img_binary, img_erosion, img_opening, img_dilation_opening, img_result]

    plt.figure(figsize=(16, 10)) 
    for i in range(5):
        plt.subplot(2, 3, i+1)
        plt.imshow(images[i], 'gray')
        plt.title(titles[i], fontsize=10)
        plt.axis('off')
    
    plt.tight_layout()
    plt.show()

    # Lưu ảnh kết quả để kiểm tra kỹ hơn
    cv2.imwrite('fingerprint_clean_v2.jpg', img_result)