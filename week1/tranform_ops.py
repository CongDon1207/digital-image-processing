import cv2
import numpy as np


def fit_resize(img: np.ndarray, max_w: int = 1200, max_h: int = 627) -> np.ndarray:

    h, w = img.shape[:2]
    scale = min(float(max_h/h) , float(max_w/w), 1.0)
    if scale < 1.0:
        new_size = (int(scale * w), int(scale * h))
        img = cv2.resize(img, new_size, interpolation = cv2.INTER_AREA)
    return img

def rotate_scale_fit(img_bgr: np.ndarray, angle_deg: float, scale: float) -> np.ndarray:
    """
    Quay ảnh quanh tâm + thu nhỏ/phóng to, và MỞ RỘNG canvas để không bị cắt góc.
    Trả về ảnh đã warp với kích thước mới vừa khít.
    """
    (h, w) = img_bgr.shape[:2]
    center = (w / 2.0, h / 2.0)

    # Ma trận quay + scale
    M = cv2.getRotationMatrix2D(center, angle_deg, scale)
    
    # Trong đó s = scale, θ = angle_deg (radian khi suy diễn), (x0,y0) = center
    # Công thức kích thước khung mới (không cắt):
    #   new_w = h*|sinθ| + w*|cosθ|
    #   new_h = h*|cosθ| + w*|sinθ|
    
    cos = abs(M[0, 0])
    sin = abs(M[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))

    # Dời tịnh tiến để tâm ảnh trùng tâm canvas mới
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]

    # Warp
    out = cv2.warpAffine(
        img_bgr, M, (new_w, new_h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REPLICATE  # tránh viền đen gắt
    )
    return out

def animate_rotate_shrink(
    img_bgr: np.ndarray,
    steps: int = 50,
    angle_step: float = 15.0,
    scale_step: float = 0.9,
    win_name: str = "rotate_anim",
    delay_ms: int = 30,
    min_scale: float = 0.001,     
    fixed_canvas: bool = True    # GIỮ KHUNG CỐ ĐỊNH = kích thước ảnh gốc
) -> None:
    """
    Hoạt hình quay + thu nhỏ trên CÙNG MỘT CỬA SỔ.
    - Nếu fixed_canvas=True: luôn warp về (w,h) gốc -> cửa sổ cố định.
    - Nếu fixed_canvas=False: dùng rotate_scale_fit để tự mở rộng canvas và tránh cắt góc.
    - Đặt min_scale để tránh scale quá bé gây khung 0x0.
    - Nhấn ESC để dừng sớm.
    """
    h, w = img_bgr.shape[:2]
    center = (w / 2.0, h / 2.0)

    cv2.namedWindow(win_name, cv2.WINDOW_AUTOSIZE)
    # Đưa cửa sổ lên foreground để hiện ngay
    cv2.setWindowProperty(win_name, cv2.WND_PROP_TOPMOST, 1)

    for i in range(1, steps + 1):
        cur_angle = i * angle_step
        # Thu nhỏ tích lũy nhưng không dưới ngưỡng
        cur_scale = max(scale_step ** i, min_scale)

        # Ma trận quay quanh tâm ảnh gốc
        M = cv2.getRotationMatrix2D(center, cur_angle, cur_scale)

        if fixed_canvas:
            # Giữ size = (w, h) để cửa sổ ổn định, không “gãy khung”
            dst_size = (w, h)
            frame = cv2.warpAffine(
                img_bgr, M, dst_size,
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_REPLICATE
            )
        else:
            # Đơn giản hóa: tái sử dụng helper quay + mở rộng canvas
            frame = rotate_scale_fit(img_bgr, cur_angle, cur_scale)

        cv2.imshow(win_name, frame)
        key = cv2.waitKey(delay_ms) & 0xFF
        if key == 27:  
            break

    cv2.destroyWindow(win_name)
