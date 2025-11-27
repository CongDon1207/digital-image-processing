import cv2
import sys
from functions import analyze_objects_with_filling

def main():
   

    img_path = 'input/image.png'

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Không đọc được ảnh. Kiểm tra đường dẫn.")
        sys.exit(1)

    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    output_img, n_objects, results_text = analyze_objects_with_filling(binary)

    print(f"Số object: {n_objects}")
    for line in results_text:
        print(line)

    cv2.imshow("Binary input", binary)
    cv2.imshow("Objects analyzed", output_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
