import cv2
import numpy as np
import matplotlib.pyplot as plt


def draw_star(img, center, outer_radius, n_points, inner_ratio=0.4, color=0):
    angles = np.linspace(-np.pi/2, 2*np.pi - np.pi/2, 2*n_points + 1)[:-1]
    pts = []
    for i, angle in enumerate(angles):
        r = outer_radius if i % 2 == 0 else outer_radius * inner_ratio
        x = int(center[0] + r * np.cos(angle))
        y = int(center[1] + r * np.sin(angle))
        pts.append((x, y))
    cv2.fillPoly(img, [np.array(pts)], color)


def draw_star_of_david(img, center, size, color=0):
    cx, cy = center
    
    pts1 = np.array([
        [cx, cy - size],
        [cx - int(size * 0.866), cy + size // 2],
        [cx + int(size * 0.866), cy + size // 2]
    ])
    
    pts2 = np.array([
        [cx, cy + size],
        [cx - int(size * 0.866), cy - size // 2],
        [cx + int(size * 0.866), cy - size // 2]
    ])
    cv2.fillPoly(img, [pts1], color)
    cv2.fillPoly(img, [pts2], color)


def draw_rounded_rect(img, pt1, pt2, corner_radius, color=0):
    
    x1, y1 = pt1
    x2, y2 = pt2
    
    cv2.rectangle(img, (x1 + corner_radius, y1), (x2 - corner_radius, y2), color, -1)
    cv2.rectangle(img, (x1, y1 + corner_radius), (x2, y2 - corner_radius), color, -1)
    
    cv2.circle(img, (x1 + corner_radius, y1 + corner_radius), corner_radius, color, -1)
    cv2.circle(img, (x2 - corner_radius, y1 + corner_radius), corner_radius, color, -1)
    cv2.circle(img, (x1 + corner_radius, y2 - corner_radius), corner_radius, color, -1)
    cv2.circle(img, (x2 - corner_radius, y2 - corner_radius), corner_radius, color, -1)


def create_input_image():
    img = np.ones((300, 600), dtype=np.uint8) * 255

    draw_star(img, (80, 80), 65, 5, inner_ratio=0.38)
    draw_star_of_david(img, (250, 150), 60)

    cv2.rectangle(img, (380, 20), (560, 180), 0, -1)
    for corner in [(380, 20), (560, 20), (380, 180), (560, 180)]:
        cv2.circle(img, corner, 30, 255, -1)

    center = (100, 230)
    radius = 60
    cv2.circle(img, center, radius, 0, -1)

    rect_center = (center[0] + 55, center[1] - 25)  
    rect_size = (120, 70)       
    angle = 65               

    box = cv2.boxPoints((rect_center, rect_size, angle))
    box = np.int32(box)
    cv2.fillPoly(img, [box], 255)   

    draw_rounded_rect(img, (350, 200), (560, 270), 35)

    cv2.imwrite('hw4_2_input.png', img)
    return img


def extract_boundary(img):
    img_inv = cv2.bitwise_not(img)
    kernel = np.ones((3, 3), np.uint8)
    img_eroded = cv2.erode(img_inv, kernel, iterations=1)
    boundary = img_inv - img_eroded
    return cv2.bitwise_not(boundary)


def display_results(img, boundary):
    titles = ["Anh Goc (Original)", "Bien doi tuong (Boundary)"]
    images = [img, boundary]

    plt.figure(figsize=(12, 5))
    for i, (image, title) in enumerate(zip(images, titles), 1):
        plt.subplot(1, 2, i)
        plt.imshow(image, cmap='gray', vmin=0, vmax=255)
        plt.title(title)
        plt.axis('off')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    img = create_input_image()
    boundary = extract_boundary(img)
    display_results(img, boundary)
